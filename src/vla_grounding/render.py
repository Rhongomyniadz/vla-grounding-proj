"""Render both real cameras without allocating policy weights."""

import argparse
from pathlib import Path

from vla_grounding.assets import read_assets
from vla_grounding.bootstrap import prepare_simulator
from vla_grounding.config import read_config
from vla_grounding.evidence import write_report
from vla_grounding.runtime import check_target


def main() -> None:
    """Save raw observation and correctly oriented camera PNGs from one target reset."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--assets", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    config = read_config(args.config)
    report = check_target(config, Path.cwd())
    assets = read_assets(args.assets)
    config_file = prepare_simulator(Path.cwd(), assets.simulator, config.cuda_device)

    import numpy as np
    from PIL import Image

    from vla_grounding.inspection import write_inspection
    from vla_grounding.simulator import SimulatorConnector

    args.output_dir.mkdir(parents=True, exist_ok=False)
    simulator = SimulatorConnector(config, config.smoke_steps)
    try:
        raw = simulator.reset(config.seed)
        processed = simulator.prepare_observation(raw, simulator.instruction())
        for name in ("image", "image2"):
            Image.fromarray(np.flip(raw["pixels"][name][0], axis=(0, 1))).save(
                args.output_dir / f"{name}.png"
            )
        np.savez_compressed(
            args.output_dir / "observation.npz",
            image=raw["pixels"]["image"],
            image2=raw["pixels"]["image2"],
            state=processed["observation.state"].cpu().numpy(),
        )
        write_inspection(args.output_dir / "observation.npz", args.output_dir / "inspection.json")
        write_report(
            args.output_dir / "render.json",
            {
                "runtime": report,
                "config": config.model_dump(mode="json"),
                "assets": assets.simulator.model_dump(mode="json"),
                "libero_config": str(config_file),
                "instruction": simulator.instruction(),
                "rendering_backend": "egl",
                "cameras": ["image.png", "image2.png"],
                "policy_verified": False,
            },
        )
    finally:
        simulator.close()
    print(f"Camera check passed. Inspect both PNGs before policy inference: {args.output_dir}")


if __name__ == "__main__":
    main()
