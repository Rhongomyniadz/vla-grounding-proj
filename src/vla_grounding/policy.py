"""Connect a fully local SmolVLA checkpoint to its saved processor pipelines."""

from copy import deepcopy
from typing import TypedDict, Unpack

import torch
from lerobot.policies import make_pre_post_processors
from lerobot.policies.smolvla.configuration_smolvla import SmolVLAConfig
from lerobot.policies.smolvla.modeling_smolvla import ActionSelectKwargs, SmolVLAPolicy
from lerobot.processor import PolicyProcessorPipeline
from lerobot.utils.constants import ACTION

from vla_grounding.assets import AssetBundle
from vla_grounding.simulator import EnvironmentObservation


class PolicySelection(TypedDict):
    """Associate one actual queue selection with its full originating prediction."""

    normalized_action: torch.Tensor
    new_chunk: torch.Tensor | None
    chunk_index: int
    chunk_offset: int


class RecordedSmolVLA(SmolVLAPolicy):
    """Observe the pinned chunk boundary while retaining upstream select_action semantics.

    LeRobot 0.6.1 selects through _get_action_chunk, not predict_action_chunk.
    This version-specific external adapter captures that return without another
    prediction, RNG draw, queue implementation or mutation of upstream source.
    """

    def reset(self) -> None:
        """Reset upstream queues and the prediction evidence together."""
        super().reset()
        self.prediction_count: int = 0
        self.last_chunk: torch.Tensor | None = None

    def _get_action_chunk(
        self,
        batch: dict[str, torch.Tensor],
        noise: torch.Tensor | None,
        **kwargs: Unpack[ActionSelectKwargs],
    ) -> torch.Tensor:
        """Capture each real model prediction exactly once before queue truncation."""
        chunk = super()._get_action_chunk(batch, noise, **kwargs)
        expected = (1, self.config.chunk_size, 7)
        if tuple(chunk.shape) != expected or not torch.isfinite(chunk).all().item():
            raise ValueError(
                f"Invalid normalized predicted chunk: expected={expected}, got={chunk.shape}"
            )
        self.prediction_count += 1
        self.last_chunk = chunk.detach().cpu().clone()
        return chunk


class ActionDecoder:
    """Validate real policy actions before the simulator sees them."""

    def __init__(self, processor: PolicyProcessorPipeline[torch.Tensor, torch.Tensor]) -> None:
        self.processor: PolicyProcessorPipeline[torch.Tensor, torch.Tensor] = processor

    def __call__(self, action: torch.Tensor) -> torch.Tensor:
        """Keep checkpoint unnormalization and reject invalid executed actions."""
        if not torch.isfinite(action).all().item():
            raise ValueError(
                "Policy returned nonfinite normalized actions; simulator stepping stopped."
            )
        decoded: torch.Tensor = self.processor(action.clone())
        if decoded.shape != (1, 7) or not torch.isfinite(decoded).all().item():
            raise ValueError(
                f"Decoded action must be finite (1, 7); received shape={decoded.shape}"
            )
        return decoded


class PolicyConnector:
    """Load strict full checkpoint weights and preserve its action queue and normalizers."""

    def __init__(self, assets: AssetBundle, device: str) -> None:
        config = SmolVLAConfig.from_pretrained(assets.policy.path, local_files_only=True)
        if not isinstance(config, SmolVLAConfig):
            raise TypeError(f"Expected SmolVLA checkpoint config; received {type(config).__name__}")
        expected = {
            "observation.state": (8,),
            "observation.images.camera1": (3, 256, 256),
            "observation.images.camera2": (3, 256, 256),
        }
        actual = {key: feature.shape for key, feature in config.input_features.items()}
        if actual != expected or config.output_features["action"].shape != (7,):
            raise ValueError(
                f"Checkpoint public features differ from the pinned interface: {actual}"
            )
        config.device = device
        config.push_to_hub = False
        config.pretrained_path = assets.policy.path
        config.vlm_model_name = assets.vlm.path
        config.load_vlm_weights = False
        if config.rtc_config is not None and config.rtc_config.enabled:
            raise ValueError(
                "Pilot episodes require the synchronous action queue; RTC is unsupported."
            )
        self.model: RecordedSmolVLA = RecordedSmolVLA.from_pretrained(
            assets.policy.path, config=config, local_files_only=True, strict=True
        )
        self.rename_map: dict[str, str] = {
            "observation.images.image": "observation.images.camera1",
            "observation.images.image2": "observation.images.camera2",
        }
        self.preprocessor, postprocessor = make_pre_post_processors(
            policy_cfg=config,
            pretrained_path=assets.policy.path,
            preprocessor_overrides={
                "device_processor": {"device": device},
                "rename_observations_processor": {"rename_map": self.rename_map},
                "tokenizer_processor": {"tokenizer_name": assets.vlm.path},
            },
            postprocessor_overrides={"device_processor": {"device": "cpu"}},
        )
        self.decoder: ActionDecoder = ActionDecoder(postprocessor)
        self.selection_calls: int = 0

    def select_action(self, observation: dict[str, torch.Tensor]) -> PolicySelection:
        """Use the real upstream queue and report its prediction/offset without resampling."""
        before = self.model.prediction_count
        self.selection_calls += 1
        with torch.inference_mode():
            action = self.model.select_action(deepcopy(observation))
        if tuple(action.shape) != (1, 7) or not torch.isfinite(action).all().item():
            raise ValueError(f"Invalid selected normalized action: {action.shape}")
        return {
            "normalized_action": action,
            "new_chunk": self.model.last_chunk if self.model.prediction_count > before else None,
            "chunk_index": self.model.prediction_count - 1,
            "chunk_offset": self.model.config.n_action_steps - len(self.model._queues[ACTION]) - 1,
        }

    def prepare_observation(self, observation: EnvironmentObservation) -> dict[str, torch.Tensor]:
        """Tokenize and normalize a copy, then validate required public tensor contracts."""
        processed = self.preprocessor(deepcopy(observation))
        tensors: dict[str, torch.Tensor] = {
            key: value for key, value in processed.items() if isinstance(value, torch.Tensor)
        }
        expected = {
            "observation.state": (1, 8),
            "observation.images.camera1": (1, 3, 256, 256),
            "observation.images.camera2": (1, 3, 256, 256),
            "observation.language.tokens": (1, self.model.config.tokenizer_max_length),
            "observation.language.attention_mask": (1, self.model.config.tokenizer_max_length),
        }
        for key, shape in expected.items():
            value = tensors[key]
            if tuple(value.shape) != shape or not torch.isfinite(value).all().item():
                raise ValueError(
                    f"Invalid processed feature {key}; expected={shape}, actual={value.shape}"
                )
        return tensors

    def predict_chunk(self, observation: dict[str, torch.Tensor]) -> torch.Tensor:
        """Return a diagnostic normalized chunk without consuming its first action."""
        with torch.inference_mode():
            chunk: torch.Tensor = self.model.predict_action_chunk(deepcopy(observation))
        expected = (1, self.model.config.chunk_size, 7)
        if tuple(chunk.shape) != expected or not torch.isfinite(chunk).all().item():
            raise ValueError(
                f"Predicted chunk must be finite {expected}; received shape={chunk.shape}"
            )
        return chunk

    def reset(self) -> None:
        """Clear cached actions and both processors before a new episode."""
        self.model.reset()
        self.preprocessor.reset()
        self.decoder.processor.reset()
        self.selection_calls = 0
