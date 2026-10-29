"""Run one explicit canonical development episode with aligned evidence and no autoreset."""

import argparse
from pathlib import Path
from time import perf_counter

from vla_grounding.assets import AssetBundle, read_assets
from vla_grounding.bootstrap import prepare_simulator
from vla_grounding.config import WeekOneConfig, read_config
from vla_grounding.episode_records import EpisodeCase, EpisodeResult, read_case, stop_reason
from vla_grounding.evidence import source_hashes, write_report
from vla_grounding.runtime import check_target


def run_episode(
    config: WeekOneConfig, case: EpisodeCase, assets: AssetBundle, output: Path
) -> EpisodeResult:
    """Execute only the canonical pilot goal and persist each real transition before continuing.

    Bootstrap must have run before importing this function's runtime dependencies.
    An exception leaves request/state/completed transitions for diagnosis, raises its
    original error and creates no completed episode report. No resume is implemented.
    """
    import torch
    from lerobot.utils.random_utils import set_seed
    from tqdm import tqdm

    from vla_grounding.inspection import EvidenceArray, write_inspection
    from vla_grounding.policy import PolicyConnector
    from vla_grounding.simulator import RawObservation, SimulatorConnector
    from vla_grounding.trajectory import save_arrays
    from vla_grounding.video import VideoRecorder

    def observation_arrays(raw: RawObservation) -> dict[str, EvidenceArray]:
        """Copy native fields because vector stepping can reuse observation buffers."""
        return {
            "image": raw["pixels"]["image"].copy(),
            "image2": raw["pixels"]["image2"].copy(),
            "eef_position": raw["robot_state"]["eef"]["pos"].copy(),
            "eef_quaternion": raw["robot_state"]["eef"]["quat"].copy(),
            "gripper_qpos": raw["robot_state"]["gripper"]["qpos"].copy(),
        }

    simulator = SimulatorConnector(config, case.max_steps)
    try:
        raw, states = simulator.reset_case(case)
        save_arrays(output / "initial-state.npz", states)
        write_report(
            output / "state.json",
            {
                "case": case.model_dump(mode="json"),
                "state_hashes": {
                    key: value for key, value in simulator.state_identity(states).items()
                },
            },
        )
        set_seed(case.policy_seed)
        policy = PolicyConnector(assets, f"cuda:{config.cuda_device}")
        policy.reset()
        set_seed(case.policy_seed)
        recorder = VideoRecorder(output / "episode.mp4", config.control_fps)
        recorder.capture(simulator.env)
        reason = None
        steps = 0
        started = perf_counter()
        for index in tqdm(range(case.max_steps), desc=case.episode_id):
            before = observation_arrays(raw)
            processed = policy.prepare_observation(
                simulator.prepare_observation(raw, case.instruction)
            )
            torch.cuda.synchronize(config.cuda_device)
            inference_started = perf_counter()
            selection = policy.select_action(processed)
            torch.cuda.synchronize(config.cuda_device)
            inference_seconds = perf_counter() - inference_started
            decoded = policy.decoder(selection["normalized_action"])
            raw, signals, executed = simulator.step(decoded)
            recorder.capture(simulator.env)
            arrays: dict[str, EvidenceArray] = {
                **{f"before.raw.{key}": value for key, value in before.items()},
                **{
                    f"before.policy.{key}": value.detach().cpu().numpy().copy()
                    for key, value in processed.items()
                },
                **{f"after.raw.{key}": value for key, value in observation_arrays(raw).items()},
                "normalized_action": selection["normalized_action"].detach().cpu().numpy(),
                "decoded_action": decoded.detach().cpu().numpy(),
                "executed_action": executed.detach().cpu().numpy(),
            }
            new_chunk = selection["new_chunk"]
            chunk_file = f"chunks/{selection['chunk_index']:06d}.npz"
            if new_chunk is not None:
                save_arrays(output / chunk_file, {"normalized_chunk": new_chunk.numpy()})
            transition_file = f"transitions/{index:06d}.npz"
            save_arrays(output / transition_file, arrays)
            write_report(
                output / f"transitions/{index:06d}.json",
                {
                    "step": index,
                    "instruction": case.instruction,
                    "signals": signals.model_dump(mode="json"),
                    "chunk_index": selection["chunk_index"],
                    "chunk_offset": selection["chunk_offset"],
                    "new_prediction": new_chunk is not None,
                    "inference_seconds": inference_seconds,
                    "chunk": chunk_file,
                    "arrays": transition_file,
                    "video_frame_before": index,
                    "video_frame_after": index + 1,
                },
            )
            steps = index + 1
            reason = stop_reason(signals, steps, case.max_steps)
            if reason is not None:
                break
        if reason is None:
            raise RuntimeError(f"Episode ended without a stop decision: episode={case.episode_id}")
        duration_seconds = perf_counter() - started
        frames = recorder.save()
        if frames != steps + 1:
            raise ValueError(f"Video/step alignment failed: frames={frames}, steps={steps}")
        if steps != policy.selection_calls or steps != simulator.executed_actions:
            raise ValueError(
                f"Counter mismatch: recorded={steps}, policy={policy.selection_calls}, "
                f"executed={simulator.executed_actions}"
            )
        write_inspection(output / "transitions/000000.npz", output / "inspection.json")
        result = EpisodeResult(
            episode_id=case.episode_id,
            stop_reason=reason,
            requested_goal_success=signals.success,
            steps=steps,
            policy_calls=policy.selection_calls,
            predicted_chunks=policy.model.prediction_count,
            duration_seconds=duration_seconds,
            video_frames=frames,
            state_file="initial-state.npz",
            transitions_directory="transitions",
            video="episode.mp4",
        )
    finally:
        simulator.close()
    return result


def main() -> None:
    """Validate explicit inputs/platform, create a fresh run, then publish completion last."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--assets", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    config = read_config(args.config)
    case = read_case(args.case)
    runtime = check_target(config, Path.cwd())
    assets = read_assets(args.assets)
    prepare_simulator(Path.cwd(), assets.simulator, config.cuda_device)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    write_report(
        args.output_dir / "request.json",
        {
            "scope": "development-canonical-episode",
            "config": config.model_dump(mode="json"),
            "case": case.model_dump(mode="json"),
            "runtime": runtime,
            "assets": assets.model_dump(mode="json"),
            "source_hashes": source_hashes(Path.cwd()),
            "completed": False,
        },
    )
    result = run_episode(config, case, assets, args.output_dir)
    write_report(
        args.output_dir / "episode.json",
        {"completed": True, "result": result.model_dump(mode="json")},
    )
    print(f"Completed {case.episode_id}: {result.stop_reason}; evidence={args.output_dir}")


if __name__ == "__main__":
    main()
