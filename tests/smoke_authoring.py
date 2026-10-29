"""Exercise real authoring CLI behavior without importing the target ML stack."""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_authoring(config: Path, output: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    """Invoke the installed command from a directory outside the source checkout."""
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "vla_grounding.authoring",
            "--config",
            str(config),
            "--output",
            str(output),
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def check_cli_round_trip(config: Path, directory: Path) -> None:
    """Verify installed imports, portable configuration, and honest evidence scope."""
    output = directory / "authoring.json"
    result = run_authoring(config, output, directory)
    if result.returncode != 0:
        raise AssertionError(f"Authoring CLI failed: {result.stderr}")
    report = json.loads(output.read_text(encoding="utf-8"))
    if report["scope"] != "authoring-only" or report["target_runtime_verified"] is not False:
        raise AssertionError(f"Authoring evidence incorrectly claims target validation: {report}")
    original = output.read_bytes()
    repeated = run_authoring(config, output, directory)
    if repeated.returncode == 0 or output.read_bytes() != original:
        raise AssertionError("A repeated command overwrote existing evidence.")


def check_rejected_configuration(config: Path, directory: Path) -> None:
    """Require a nonzero exit and no evidence when external input has an invalid type."""
    invalid = directory / "invalid.json"
    settings = json.loads(config.read_text(encoding="utf-8"))
    settings["seed"] = "42"
    invalid.write_text(json.dumps(settings), encoding="utf-8")
    output = directory / "invalid-output.json"
    result = run_authoring(invalid, output, directory)
    if result.returncode == 0 or output.exists() or "seed" not in result.stderr:
        raise AssertionError(f"Invalid configuration was not rejected clearly: {result}")


def check_windows_boundary(config: Path, directory: Path) -> None:
    """On a real Windows host, reject target execution before importing torch."""
    output = directory / "target.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "vla_grounding.runtime",
            "--config",
            str(config),
            "--output",
            str(output),
        ],
        cwd=directory,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if result.returncode == 0 or output.exists() or "inside Ubuntu/WSL2" not in result.stderr:
        raise AssertionError(
            f"Target execution was not rejected at the platform boundary: {result}"
        )


def main() -> None:
    """Run meaningful command-level checks using real files and real subprocesses."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    config = args.config.resolve(strict=True)
    with tempfile.TemporaryDirectory() as name:
        directory = Path(name)
        check_cli_round_trip(config, directory)
        check_rejected_configuration(config, directory)
        if sys.platform == "win32":
            check_windows_boundary(config, directory)
            print("PASS: Windows rejects target commands before ML imports")
        print("PASS: authoring CLI, external input validation, and evidence preservation")


if __name__ == "__main__":
    main()
