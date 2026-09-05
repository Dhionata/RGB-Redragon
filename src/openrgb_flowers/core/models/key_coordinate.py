"""Model representing physical key position on a keyboard matrix."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KeyCoordinate:
    """Represents a physical LED key coordinate on the keyboard surface.

    Coordinates (x, y) are normalized to [0.0, 1.0] across the keyboard width and height,
    enabling resolution-independent floral propagation calculations.
    """

    name: str
    index: int
    x: float
    y: float
    row: int
    col: int

    def __post_init__(self) -> None:
        if not (0.0 <= self.x <= 1.0):
            object.__setattr__(self, "x", max(0.0, min(1.0, float(self.x))))
        if not (0.0 <= self.y <= 1.0):
            object.__setattr__(self, "y", max(0.0, min(1.0, float(self.y))))
