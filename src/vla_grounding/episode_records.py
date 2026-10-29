"""Portable, validated development episode contracts and stop decisions."""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

type StopReason = Literal["success", "environment_terminated", "environment_truncated", "timeout"]


class EpisodeCase(BaseModel):
    """Require an explicit canonical pilot case; language interventions arrive in Week 5."""

    model_config = ConfigDict(strict=True, frozen=True, extra="ignore")

    episode_id: Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9-]{0,63}$")]
    task_name: Annotated[str, Field(min_length=1)]
    instruction: Annotated[str, Field(min_length=1)]
    initial_state_index: Annotated[int, Field(ge=0)]
    environment_seed: Annotated[int, Field(ge=0)]
    policy_seed: Annotated[int, Field(ge=0)]
    max_steps: Annotated[int, Field(ge=1, le=280)]


class StepSignals(BaseModel):
    """Represent one native simulator transition without collapsing its flags."""

    model_config = ConfigDict(strict=True, frozen=True, extra="ignore")

    reward: float
    success: bool
    terminated: bool
    truncated: bool


class EpisodeResult(BaseModel):
    """Describe a completed pilot; infrastructure exceptions never produce this record."""

    model_config = ConfigDict(strict=True, frozen=True, extra="ignore")

    episode_id: str
    stop_reason: StopReason
    requested_goal_success: bool
    steps: Annotated[int, Field(gt=0)]
    policy_calls: Annotated[int, Field(gt=0)]
    predicted_chunks: Annotated[int, Field(gt=0)]
    duration_seconds: Annotated[float, Field(ge=0)]
    video_frames: Annotated[int, Field(ge=2)]
    state_file: str
    transitions_directory: str
    video: str


def read_case(path: Path) -> EpisodeCase:
    """Reject missing/coerced case fields before target resources are allocated."""
    return EpisodeCase.model_validate_json(path.read_text(encoding="utf-8"))


def stop_reason(signals: StepSignals, steps: int, max_steps: int) -> StopReason | None:
    """Preserve terminal observations; success takes precedence at the step limit."""
    if steps < 1 or max_steps < 1 or steps > max_steps:
        raise ValueError(f"Invalid step accounting: steps={steps}, max_steps={max_steps}")
    if signals.success:
        return "success"
    if signals.terminated:
        return "environment_terminated"
    if signals.truncated:
        return "environment_truncated"
    if steps == max_steps:
        return "timeout"
    return None
