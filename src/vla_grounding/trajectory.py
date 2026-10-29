"""Persist typed numeric evidence as exclusive, compressed, pickle-free archives."""

from collections.abc import Mapping
from pathlib import Path

import numpy as np

from vla_grounding.inspection import EvidenceArray, inspect_arrays


def save_arrays(path: Path, arrays: Mapping[str, EvidenceArray]) -> None:
    """Validate arrays before writing; leave existing evidence untouched on repeated paths."""
    inspect_arrays(arrays)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        np.savez_compressed(stream, **arrays)
