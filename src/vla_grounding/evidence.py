"""Write local development evidence without replacing previous observations."""

import json
from collections.abc import Mapping
from hashlib import sha256
from pathlib import Path

type JsonValue = str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]


def source_hashes(workspace: Path) -> dict[str, JsonValue]:
    """Identify the exact dirty source/configuration/lock snapshot without creating a commit."""
    paths = [
        workspace / "pyproject.toml",
        workspace / "uv.lock",
        workspace / ".python-version",
        *sorted((workspace / "src").rglob("*.py")),
        *sorted((workspace / "configs").glob("*.json")),
    ]
    return {
        path.relative_to(workspace).as_posix(): sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


def write_report(path: Path, report: Mapping[str, JsonValue]) -> None:
    """Create a JSON report exclusively so a rerun cannot overwrite evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
