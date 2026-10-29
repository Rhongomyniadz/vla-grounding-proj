"""Run a short upstream interface smoke check, without a project episode loop."""

import argparse
from pathlib import Path

from vla_grounding.assets import read_assets
from vla_grounding.bootstrap import prepare_simulator
from vla_grounding.config import read_config
from vla_grounding.evidence import write_report
from vla_grounding.runtime import check_target


def main() -> None:
    """Save a real diagnostic prediction and a separate bounded upstream rollout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--assets", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    config = read_config(args.config)
    runtime = check_target(config, Path.cwd())
    assets = read_assets(args.assets)
    prepare_simulator(Path.cwd(), assets.simulator, config.cuda_device)

    import numpy as np
    import torch
    from lerobot.scripts.lerobot_eval import rollout
    from lerobot.utils.random_utils import set_seed

    from vla_grounding.inspection import write_inspection
    from vla_grounding.policy import PolicyConnector
    from vla_grounding.simulator import SimulatorConnector
    from vla_grounding.video import VideoRecorder

    args.output_dir.mkdir(parents=True, exist_ok=False)
    simulator = SimulatorConnector(config, config.smoke_steps)
    try:
        set_seed(config.seed)
        policy = PolicyConnector(assets, f"cuda:{config.cuda_device}")
        raw = simulator.reset(config.seed)
        instruction = simulator.instruction()
        environment = simulator.prepare_observation(raw, instruction)
        processed = policy.prepare_observation(environment)
        set_seed(config.seed)
        chunk = policy.predict_chunk(processed)
        decoded = policy.decoder(chunk[:, 0])
        np.savez_compressed(
            args.output_dir / "prediction.npz",
            raw_image=raw["pixels"]["image"],
            raw_image2=raw["pixels"]["image2"],
            eef_position=raw["robot_state"]["eef"]["pos"],
            eef_quaternion=raw["robot_state"]["eef"]["quat"],
            gripper_qpos=raw["robot_state"]["gripper"]["qpos"],
            **{key: value.detach().cpu().numpy() for key, value in processed.items()},
            normalized_chunk=chunk.detach().cpu().numpy(),
            decoded_first_action=decoded.detach().cpu().numpy(),
        )
        write_inspection(args.output_dir / "prediction.npz", args.output_dir / "inspection.json")
        policy.reset()
        simulator.close()
        simulator = SimulatorConnector(config, config.smoke_steps)
        recorder = VideoRecorder(args.output_dir / "smoke.mp4", config.control_fps)
        set_seed(config.seed)
        with torch.inference_mode():
            data = rollout(
                env=simulator.env,
                policy=policy.model,
                env_preprocessor=simulator.preprocessor,
                env_postprocessor=simulator.postprocessor,
                preprocessor=policy.preprocessor,
                postprocessor=policy.decoder,
                seeds=[config.seed],
                return_observations=False,
                render_callback=recorder.capture,
            )
        actions: torch.Tensor = data["action"]
        if actions.ndim != 3 or actions.shape[0] != 1 or actions.shape[2] != 7:
            raise ValueError(f"Upstream smoke returned invalid executed actions: {actions.shape}")
        if not torch.isfinite(actions).all().item():
            raise ValueError("Upstream smoke returned nonfinite executed actions.")
        if not torch.allclose(actions[:, 0], decoded, rtol=1e-4, atol=1e-5):
            raise ValueError(
                "Diagnostic first action differs from the upstream rollout's first action. "
                "Inspect initial states, preprocessing, and sampling seeds before using this trace."
            )
        np.savez_compressed(args.output_dir / "executed-actions.npz", actions=actions.cpu().numpy())
        frames = recorder.save()
        write_report(
            args.output_dir / "smoke.json",
            {
                "scope": "development-interface-smoke",
                "runtime": runtime,
                "config": config.model_dump(mode="json"),
                "assets": assets.model_dump(mode="json"),
                "instruction": instruction,
                "rename_map": policy.rename_map,
                "chunk_size": policy.model.config.chunk_size,
                "n_action_steps": policy.model.config.n_action_steps,
                "executed_steps": actions.shape[1],
                "decoded_video_frames": frames,
                "diagnostic_prediction": "prediction.npz",
                "rollout_actions": "executed-actions.npz",
                "video": "smoke.mp4",
                "rendering_backend": "egl",
                "human_video_inspection_complete": False,
                "task_success_measured": False,
            },
        )
    finally:
        simulator.close()
    print(f"Interface smoke passed. Play the video and inspect saved tensors: {args.output_dir}")


if __name__ == "__main__":
    main()
