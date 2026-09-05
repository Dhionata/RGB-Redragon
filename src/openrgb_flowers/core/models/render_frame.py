"""Model representing a single rendered lighting frame."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class RenderFrame:
    """Encapsulates a rendered frame with high-performance NumPy color buffer.

    colors array has shape (N, 3) and dtype uint8, where N is the number of keyboard LEDs.
    """

    timestamp: float
    frame_index: int
    colors: np.ndarray
    led_count: int

    def __post_init__(self) -> None:
        if self.colors.dtype != np.uint8:
            self.colors = np.clip(self.colors, 0, 255).astype(np.uint8)
        if len(self.colors.shape) != 2 or self.colors.shape[1] != 3:
            raise ValueError(f"Colors buffer must have shape (N, 3), got {self.colors.shape}")
        if self.colors.shape[0] != self.led_count:
            raise ValueError(f"Colors length {self.colors.shape[0]} does not match led_count {self.led_count}")
