"""Inspect real NumPy evidence without importing the simulator or policy stack."""

import argparse
from collections.abc import Mapping
from pathlib import Path
from typing import Literal

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict

from vla_grounding.evidence import write_report

type EvidenceArray = NDArray[np.generic]


class ArrayInspection(BaseModel):
    """Describe representation statistics without treating text or masks as continuous data."""

    model_config = ConfigDict(strict=True, frozen=True, extra="ignore")

    name: str
    shape: tuple[int, ...]
    dtype: str
    kind: Literal["boolean", "integer", "floating", "text"]
    minimum: float | None
    maximum: float | None
    all_finite: bool | None
    true_count: int | None


def inspect_array(name: str, value: EvidenceArray) -> ArrayInspection:
    """Summarize a nonempty numeric/text array; reject object and complex evidence."""
    if value.size == 0:
        raise ValueError(f"Cannot inspect empty evidence array: name={name}, shape={value.shape}")
    minimum: float | None = None
    maximum: float | None = None
    finite: bool | None = None
    true_count: int | None = None
    kind: Literal["boolean", "integer", "floating", "text"]
    if value.dtype.kind == "b":
        kind = "boolean"
        true_count = int(np.count_nonzero(value))
    elif value.dtype.kind in "iu":
        kind = "integer"
        minimum, maximum = float(value.min()), float(value.max())
        finite = True
    elif value.dtype.kind == "f":
        kind = "floating"
        finite = bool(np.isfinite(value).all())
        if not finite:
            raise ValueError(
                f"Nonfinite evidence: name={name}, shape={value.shape}, dtype={value.dtype}"
            )
        minimum, maximum = float(value.min()), float(value.max())
    elif value.dtype.kind in "US":
        kind = "text"
    else:
        raise TypeError(f"Unsupported evidence dtype: name={name}, dtype={value.dtype}")
    return ArrayInspection(
        name=name,
        shape=tuple(value.shape),
        dtype=str(value.dtype),
        kind=kind,
        minimum=minimum,
        maximum=maximum,
        all_finite=finite,
        true_count=true_count,
    )


def inspect_arrays(arrays: Mapping[str, EvidenceArray]) -> tuple[ArrayInspection, ...]:
    """Return ordered diagnostics without modifying any input arrays."""
    if not arrays:
        raise ValueError("Evidence archive contains no arrays.")
    return tuple(inspect_array(name, value) for name, value in sorted(arrays.items()))


def inspect_archive(path: Path) -> tuple[ArrayInspection, ...]:
    """Read an NPZ with pickle disabled and validate every saved array."""
    with np.load(path, allow_pickle=False) as archive:
        arrays: dict[str, EvidenceArray] = {name: archive[name] for name in archive.files}
    return inspect_arrays(arrays)


def write_inspection(source: Path, output: Path) -> None:
    """Create an exclusive diagnostic report for an actual saved archive."""
    rows = inspect_archive(source)
    write_report(
        output,
        {"source": str(source), "arrays": [row.model_dump(mode="json") for row in rows]},
    )


def main() -> None:
    """Inspect evidence with NumPy installed, using explicit input/output paths."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    write_inspection(args.input, args.output)


if __name__ == "__main__":
    main()
