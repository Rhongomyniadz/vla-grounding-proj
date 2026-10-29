"""Validate external Week 1 configuration without importing the GPU stack."""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class WeekOneConfig(BaseModel):
    """Required settings from the portable development smoke configuration."""

    model_config = ConfigDict(strict=True, frozen=True, extra="ignore")

    expected_gpu: Annotated[str, Field(min_length=1)]
    cuda_device: Annotated[int, Field(ge=0)]
    minimum_free_disk_gib: Annotated[int, Field(gt=0)]
    suite: Literal["libero_spatial"]
    task_id: Annotated[int, Field(ge=0, lt=10)]
    seed: Annotated[int, Field(ge=0)]
    image_size: Literal[256]
    smoke_steps: Annotated[int, Field(ge=2, le=32)]
    control_fps: Literal[20]
    policy_revision: Annotated[str, Field(pattern=r"^[0-9a-f]{40}$")]
    vlm_revision: Annotated[str, Field(min_length=1)]
    simulator_assets_revision: Annotated[str, Field(min_length=1)]


def read_config(path: Path) -> WeekOneConfig:
    """Reject missing fields and coerced values; ignore unrelated external fields."""
    return WeekOneConfig.model_validate_json(path.read_text(encoding="utf-8"))
