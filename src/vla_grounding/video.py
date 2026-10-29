"""Capture real upstream renders and verify a locally encoded MP4."""

from pathlib import Path

import av
import gymnasium as gym
import numpy as np
from lerobot.utils.io_utils import write_video
from numpy.typing import NDArray


class VideoRecorder:
    """Adapt the upstream render callback to synchronous local video evidence."""

    def __init__(self, path: Path, fps: int) -> None:
        self.path: Path = path
        self.fps: int = fps
        self.frames: list[NDArray[np.uint8]] = []

    def capture(self, env: gym.vector.VectorEnv) -> None:
        """Receive a callback after reset and every upstream simulator step."""
        frame: NDArray[np.uint8] = env.call("render")[0]
        if not isinstance(frame, np.ndarray) or frame.ndim != 3 or frame.shape[2] != 3:
            raise ValueError("Simulator render callback must return an RGB HWC numpy array.")
        if frame.dtype != np.uint8:
            raise TypeError(f"Simulator render must use uint8; received {frame.dtype}")
        self.frames.append(frame.copy())

    def save(self) -> int:
        """Write via LeRobot and decode every frame; visual content needs separate review."""
        if len(self.frames) < 2:
            raise ValueError(
                f"Smoke video requires at least two real frames; received {len(self.frames)}"
            )
        if self.path.exists():
            raise FileExistsError(f"Video evidence already exists: {self.path}")
        write_video(self.path, self.frames, self.fps)
        with av.open(str(self.path), mode="r") as container:
            count = sum(1 for _frame in container.decode(video=0))
        if count != len(self.frames):
            raise ValueError(
                f"Video round trip lost frames: encoded={len(self.frames)}, decoded={count}"
            )
        return count
