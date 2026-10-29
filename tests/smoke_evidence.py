"""Exercise real NPZ/JSON I/O, external case validation and development stop decisions."""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from pydantic import ValidationError

from vla_grounding.episode_records import EpisodeCase, StepSignals, read_case, stop_reason
from vla_grounding.inspection import inspect_archive
from vla_grounding.trajectory import save_arrays


def check_archives(directory: Path) -> None:
    """Round-trip real numeric/mask/text arrays and reject unsafe/invalid evidence."""
    values = np.arange(16, dtype=np.float32).reshape(2, 8)
    original = values.copy()
    archive = directory / "observation.npz"
    save_arrays(
        archive,
        {
            "state": values,
            "mask": np.array([[True, False]], dtype=np.bool_),
            "tokens": np.array([[1, 7]], dtype=np.int64),
            "instruction": np.array(["test inspection"], dtype=np.str_),
        },
    )
    rows = {row.name: row for row in inspect_archive(archive)}
    if rows["state"].shape != (2, 8) or rows["state"].maximum != 15.0:
        raise AssertionError(f"Array statistics are incorrect: {rows}")
    if rows["mask"].true_count != 1 or rows["instruction"].minimum is not None:
        raise AssertionError("Masks/text were treated as continuous state.")
    np.testing.assert_array_equal(values, original)
    try:
        save_arrays(archive, {"state": values})
    except FileExistsError:
        pass
    else:
        raise AssertionError("Existing trajectory evidence was overwritten.")
    output = directory / "inspection.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "vla_grounding.inspection",
            "--input",
            str(archive),
            "--output",
            str(output),
        ],
        cwd=directory,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0 or not output.exists():
        raise AssertionError(f"Real inspector CLI failed: {completed.stderr}")
    invalid = directory / "nonfinite.npz"
    np.savez_compressed(invalid, state=np.array([np.nan]))
    rejected = subprocess.run(
        [
            sys.executable,
            "-m",
            "vla_grounding.inspection",
            "--input",
            str(invalid),
            "--output",
            str(directory / "invalid.json"),
        ],
        cwd=directory,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if rejected.returncode == 0 or (directory / "invalid.json").exists():
        raise AssertionError("Nonfinite input produced a successful inspection report.")


def check_cases(directory: Path, cases: tuple[Path, ...]) -> None:
    """Read actual pilot inputs and verify explicit success/termination/timeout semantics."""
    for path in cases:
        case = read_case(path)
        invalid = json.loads(case.model_dump_json())
        invalid["policy_seed"] = "42"
        try:
            EpisodeCase.model_validate(invalid)
        except ValidationError:
            pass
        else:
            raise AssertionError("External case coerced a string seed to integer.")
    expected = (
        (StepSignals(reward=0.0, success=False, terminated=False, truncated=False), 1, None),
        (StepSignals(reward=0.0, success=False, terminated=False, truncated=False), 2, "timeout"),
        (StepSignals(reward=1.0, success=True, terminated=True, truncated=False), 2, "success"),
        (
            StepSignals(reward=0.0, success=False, terminated=True, truncated=False),
            1,
            "environment_terminated",
        ),
        (
            StepSignals(reward=0.0, success=False, terminated=False, truncated=True),
            1,
            "environment_truncated",
        ),
    )
    for signals, steps, reason in expected:
        if stop_reason(signals, steps, 2) != reason:
            raise AssertionError(f"Wrong development stop decision: {signals}, steps={steps}")
    if sys.platform == "win32":
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "vla_grounding.episode",
                "--config",
                str(cases[0].parent / "week-01.json"),
                "--case",
                str(cases[0]),
                "--assets",
                str(directory / "missing-assets.json"),
                "--output-dir",
                str(directory / "target-run"),
            ],
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        if result.returncode == 0 or "inside Ubuntu/WSL2" not in result.stderr:
            raise AssertionError(f"Episode CLI crossed the Windows target boundary: {result}")
        if (directory / "target-run").exists():
            raise AssertionError("A rejected Windows episode created target results.")


def main() -> None:
    """Run portable evidence smoke checks with declared NumPy/Pydantic dependencies."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases-dir", required=True, type=Path)
    args = parser.parse_args()
    cases = tuple(sorted(args.cases_dir.resolve(strict=True).glob("week-02-case-*.json")))
    if len(cases) != 3:
        raise ValueError(f"Expected three pilot case inputs: directory={args.cases_dir}")
    with tempfile.TemporaryDirectory() as name:
        directory = Path(name)
        check_archives(directory)
        check_cases(directory, cases)
    print("PASS: real array/CLI round-trip, evidence preservation, case/stop/target boundaries")


if __name__ == "__main__":
    main()
