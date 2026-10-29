"""Execute one real target episode and audit chunk/action/frame/result alignment."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

from vla_grounding.episode_records import EpisodeResult
from vla_grounding.inspection import inspect_archive


def audit_episode(directory: Path) -> None:
    """Require a real completed bundle and reconcile every executed action with its chunk."""
    report = json.loads((directory / "episode.json").read_text(encoding="utf-8"))
    if report["completed"] is not True:
        raise AssertionError(f"Episode did not report completion: {directory}")
    result = EpisodeResult.model_validate(report["result"])
    if result.policy_calls != result.steps or result.video_frames != result.steps + 1:
        raise AssertionError(f"Counter/frame mismatch: {result}")
    transitions = sorted((directory / result.transitions_directory).glob("*.json"))
    if len(transitions) != result.steps:
        raise AssertionError(f"Transition coverage mismatch: {len(transitions)}, {result.steps}")
    chunks = 0
    for index, path in enumerate(transitions):
        step = json.loads(path.read_text(encoding="utf-8"))
        if step["step"] != index or step["video_frame_after"] != index + 1:
            raise AssertionError(f"Transition/frame order mismatch: {path}")
        chunks += int(step["new_prediction"])
        inspect_archive(directory / step["arrays"])
        with np.load(directory / step["arrays"], allow_pickle=False) as arrays:
            with np.load(directory / step["chunk"], allow_pickle=False) as chunk:
                np.testing.assert_allclose(
                    arrays["normalized_action"],
                    chunk["normalized_chunk"][:, step["chunk_offset"]],
                    rtol=1e-5,
                    atol=1e-6,
                )
            np.testing.assert_array_equal(arrays["decoded_action"], arrays["executed_action"])
    if (
        chunks != result.predicted_chunks
        or len(list((directory / "chunks").glob("*.npz"))) != chunks
    ):
        raise AssertionError(f"Prediction count mismatch: observed={chunks}, result={result}")


def main() -> None:
    """Run the actual target CLI, then audit its evidence; never substitute a simulated policy."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--assets", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    subprocess.run(
        [
            sys.executable,
            "-m",
            "vla_grounding.episode",
            "--config",
            str(args.config),
            "--case",
            str(args.case),
            "--assets",
            str(args.assets),
            "--output-dir",
            str(args.output_dir),
        ],
        check=True,
    )
    audit_episode(args.output_dir)
    print(f"PASS: real episode chunk/action/frame/coverage audit: {args.output_dir}")


if __name__ == "__main__":
    main()
