"""Keyboard spatial coordinate transformation and aspect ratio correction."""
from __future__ import annotations
import numpy as np


class SpatialGrid:
    """Handles 2D spatial coordinate mapping with physical aspect ratio correction.

    Standard full-size mechanical keyboards (like the Redragon K556) have an aspect ratio
    of approximately 3.7:1 (width to height). Without aspect ratio correction, radial effects
    would stretch into tall ellipses. This class normalizes coordinates so that blooms are
    geometrically circular and natural across physical keys.
    """

    DEFAULT_ASPECT_RATIO = 3.7  # Width / Height of full-size 104-key keyboard

    def __init__(self, aspect_ratio: float = DEFAULT_ASPECT_RATIO) -> None:
        self._aspect_ratio = max(0.5, float(aspect_ratio))

    @property
    def aspect_ratio(self) -> float:
        """Returns the physical aspect ratio."""
        return self._aspect_ratio

    def correct_aspect_ratio(
        self,
        x_coords: np.ndarray,
        y_coords: np.ndarray,
        center_x: float,
        center_y: float,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Calculates aspect-corrected dx, dy, euclidean distances, and polar angles.

        Args:
            x_coords: Normalized x positions in [0, 1]
            y_coords: Normalized y positions in [0, 1]
            center_x: Bloom origin x in [0, 1]
            center_y: Bloom origin y in [0, 1]

        Returns:
            (dx_corrected, dy, distances, angles)
        """
        dx = (x_coords - center_x) * self._aspect_ratio
        dy = y_coords - center_y
        distances = np.hypot(dx, dy)
        angles = np.arctan2(dy, dx)
        return dx, dy, distances, angles
