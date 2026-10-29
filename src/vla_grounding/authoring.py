"""Check the coding machine; this command makes no target-runtime claims."""

import argparse
import platform
import sys
from pathlib import Path

from vla_grounding.config import read_config
from vla_grounding.evidence import JsonValue, write_report


def check_authoring(config_path: Path, output_path: Path) -> None:
    """Validate portable settings and record the actual authoring interpreter."""
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError(f"Authoring requires Python 3.12; received {sys.version}")
    config = read_config(config_path)
    report: dict[str, JsonValue] = {
        "scope": "authoring-only",
        "python": sys.version,
        "executable": sys.executable,
        "system": platform.system(),
        "machine": platform.machine(),
        "config": config.model_dump(mode="json"),
        "target_runtime_verified": False,
    }
    write_report(output_path, report)
    print(f"Authoring check passed. Target CUDA/rendering remain unverified. Report: {output_path}")


def main() -> None:
    """Accept explicit configuration and report paths on any coding machine."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    check_authoring(args.config, args.output)


if __name__ == "__main__":
    main()
