"""Connect to the pinned LeRobot LIBERO simulator and its native processors."""

from hashlib import sha256
from typing import TypedDict

import gymnasium as gym
import numpy as np
import torch
from lerobot.envs.configs import LiberoEnv
from lerobot.envs.libero import LiberoEnv as NativeLiberoEnv
from lerobot.envs.utils import NEW_ROLLOUT_OPTION, preprocess_observation
from numpy.typing import NDArray

from vla_grounding.config import WeekOneConfig
from vla_grounding.episode_records import EpisodeCase, StepSignals

type FloatArray = NDArray[np.float32] | NDArray[np.float64]
type EnvironmentObservation = dict[str, torch.Tensor | list[str]]


class EndEffector(TypedDict):
    """Required native pose components, before conversion to axis-angle."""

    pos: FloatArray
    quat: FloatArray


class Gripper(TypedDict):
    """Required native gripper joint positions."""

    qpos: FloatArray


class RobotState(TypedDict):
    """Required robot state fields consumed by the upstream LIBERO processor."""

    eef: EndEffector
    gripper: Gripper


class CameraViews(TypedDict):
    """Native uint8 camera batches from a single vectorized environment."""

    image: NDArray[np.uint8]
    image2: NDArray[np.uint8]


class RawObservation(TypedDict):
    """Required native inputs; unrelated simulator fields remain upstream-owned."""

    pixels: CameraViews
    robot_state: RobotState


def environment_config(config: WeekOneConfig, episode_length: int) -> LiberoEnv:
    """Make a bounded development task with explicit relative control and camera order."""
    return LiberoEnv(
        task=config.suite,
        task_ids=[config.task_id],
        fps=config.control_fps,
        episode_length=episode_length,
        obs_type="pixels_agent_pos",
        render_mode="rgb_array",
        camera_name="agentview_image,robot0_eye_in_hand_image",
        init_states=True,
        hard_reset=True,
        camera_name_mapping={"agentview_image": "image", "robot0_eye_in_hand_image": "image2"},
        observation_height=config.image_size,
        observation_width=config.image_size,
        is_libero_plus=False,
        control_mode="relative",
    )


def require_camera(image: NDArray[np.uint8], image_size: int) -> None:
    """Reject malformed, blank, or constant native camera batches."""
    expected = (1, image_size, image_size, 3)
    if image.shape != expected or image.dtype != np.uint8:
        raise ValueError(
            f"Camera must be uint8 {expected}; got shape={image.shape}, dtype={image.dtype}"
        )
    if np.ptp(image) == 0:
        raise ValueError(
            "Camera rendered a constant image; inspect EGL and simulator asset loading."
        )


class SimulatorConnector:
    """Own one synchronous LIBERO environment and its native processor boundary."""

    def __init__(self, config: WeekOneConfig, episode_length: int) -> None:
        self.config: LiberoEnv = environment_config(config, episode_length)
        environment = self.config.create_envs(n_envs=1, use_async_envs=False)[config.suite][
            config.task_id
        ]
        if not isinstance(environment, gym.vector.SyncVectorEnv):
            raise TypeError(
                f"Expected synchronous LIBERO environment; received {type(environment)}"
            )
        self.env: gym.vector.SyncVectorEnv = environment
        self.preprocessor, self.postprocessor = self.config.get_env_processors()
        self.image_size: int = config.image_size
        self.executed_actions: int = 0

    def reset_case(self, case: EpisodeCase) -> tuple[RawObservation, dict[str, FloatArray]]:
        """Select a bounds-checked pinned benchmark state; retain pre/post-settling evidence.

        LeRobot 0.6.1 exposes init_state_id but applies modulo internally. Check
        its loaded state table first to avoid silently substituting another state.
        Arbitrary saved-state restoration and repeatability comparisons are Week 3 work.
        """
        native = self.env.envs[0].unwrapped
        if not isinstance(native, NativeLiberoEnv):
            raise TypeError(f"Expected pinned LIBERO wrapper; received {type(native)}")
        if native.task != case.task_name or native.task_description != case.instruction:
            raise ValueError(
                f"Pilot requires canonical task/text: task={native.task!r}, "
                f"instruction={native.task_description!r}, case={case.model_dump()}"
            )
        states = native._init_states
        if not isinstance(states, np.ndarray) or states.ndim != 2:
            raise TypeError("Pinned LIBERO initial states must be a two-dimensional numpy table.")
        if case.initial_state_index >= len(states):
            raise IndexError(
                f"Initial state out of range: index={case.initial_state_index}, count={len(states)}"
            )
        selected: FloatArray = states[case.initial_state_index].copy()
        if not np.isfinite(selected).all():
            raise ValueError(f"Nonfinite initial state: index={case.initial_state_index}")
        native.init_state_id = case.initial_state_index
        raw = self.reset(case.environment_seed)
        if native._env is None:
            raise RuntimeError("LIBERO reset did not allocate its native simulator.")
        if native._env.check_success():
            raise ValueError(f"Pilot goal is already satisfied at reset: episode={case.episode_id}")
        settled: FloatArray = np.asarray(native._env.get_sim_state()).copy()
        return raw, {"selected_initial_state": selected, "settled_simulator_state": settled}

    def state_identity(self, states: dict[str, FloatArray]) -> dict[str, str]:
        """Hash exact dtype, shape and bytes; these identities do not assert repeatability."""
        return {
            name: sha256(
                str((value.dtype.str, value.shape)).encode() + value.tobytes(order="C")
            ).hexdigest()
            for name, value in states.items()
        }

    def reset(self, seed: int) -> RawObservation:
        """Reset native policy inputs; advance LIBERO's upstream initial-state index."""
        self.preprocessor.reset()
        self.postprocessor.reset()
        self.executed_actions = 0
        raw, _info = self.env.reset(seed=[seed], options={NEW_ROLLOUT_OPTION: True})
        self.validate_observation(raw)
        return raw

    def validate_observation(self, raw: RawObservation) -> None:
        """Check native camera and robot-state contracts on reset and every step."""
        require_camera(raw["pixels"]["image"], self.image_size)
        require_camera(raw["pixels"]["image2"], self.image_size)
        components: tuple[tuple[str, FloatArray, tuple[int, int]], ...] = (
            ("eef.pos", raw["robot_state"]["eef"]["pos"], (1, 3)),
            ("eef.quat", raw["robot_state"]["eef"]["quat"], (1, 4)),
            ("gripper.qpos", raw["robot_state"]["gripper"]["qpos"], (1, 2)),
        )
        for name, value, shape in components:
            if not isinstance(value, np.ndarray) or value.shape != shape:
                raise ValueError(
                    f"Native robot state {name} must be a numpy array with shape={shape}"
                )
            if not np.issubdtype(value.dtype, np.floating) or not np.isfinite(value).all():
                raise ValueError(
                    f"Native robot state {name} must contain finite floating-point values."
                )

    def step(self, action: torch.Tensor) -> tuple[RawObservation, StepSignals, torch.Tensor]:
        """Execute one decoded action and keep terminal observations before NEXT_STEP reset."""
        transition = self.postprocessor({"action": action.clone()})
        control: torch.Tensor = transition["action"]
        if tuple(control.shape) != (1, 7) or not torch.isfinite(control).all().item():
            raise ValueError(f"Environment action must be finite (1, 7); received {control.shape}")
        raw, reward, terminated, truncated, info = self.env.step(control.detach().cpu().numpy())
        self.validate_observation(raw)
        success = info["is_success"]
        for name, value in (
            ("is_success", success),
            ("terminated", terminated),
            ("truncated", truncated),
        ):
            if not isinstance(value, np.ndarray) or value.shape != (1,) or value.dtype != np.bool_:
                raise TypeError(f"Invalid single-environment {name}: {value!r}")
        if reward.shape != (1,) or not np.isfinite(reward).all():
            raise ValueError(f"Invalid finite single-environment reward: {reward!r}")
        self.executed_actions += 1
        return (
            raw,
            StepSignals(
                reward=float(reward[0]),
                success=bool(success[0]),
                terminated=bool(terminated[0]),
                truncated=bool(truncated[0]),
            ),
            control.detach().cpu().clone(),
        )

    def prepare_observation(self, raw: RawObservation, instruction: str) -> EnvironmentObservation:
        """Reuse native image conversion, 180-degree rotation and pose-to-state conversion."""
        observation = preprocess_observation(raw)
        observation["task"] = [instruction]
        processed: EnvironmentObservation = self.preprocessor(observation)
        state = processed["observation.state"]
        if not isinstance(state, torch.Tensor):
            raise TypeError("LIBERO processor did not return an observation.state tensor.")
        if state.shape != (1, 8) or not torch.isfinite(state).all().item():
            raise ValueError(
                f"LIBERO robot state must be finite (1, 8); received shape={state.shape}"
            )
        return processed

    def instruction(self) -> str:
        """Require benchmark language rather than silently substituting empty text."""
        value = self.env.call("task_description")[0]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"LIBERO returned an invalid task description: {value!r}")
        return value

    def close(self) -> None:
        """Release simulator and EGL resources even after downstream errors."""
        self.env.close()
