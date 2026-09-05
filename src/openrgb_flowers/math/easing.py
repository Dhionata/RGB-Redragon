"""Smooth easing and harmonic mathematical functions."""
from __future__ import annotations
import numpy as np


class EasingFunctions:
    """Mathematical smoothing and harmonic functions for organic natural animations."""

    @staticmethod
    def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
        """GLSL-equivalent smoothstep interpolation for smooth edge falloffs."""
        diff = edge1 - edge0
        if abs(diff) < 1e-9:
            return np.where(x >= edge1, 1.0, 0.0).astype(np.float32)
        t = np.clip((x - edge0) / diff, 0.0, 1.0)
        return t * t * (3.0 - 2.0 * t)

    @staticmethod
    def ease_out_cubic(t: float | np.ndarray) -> float | np.ndarray:
        """Cubic deceleration curve."""
        return 1.0 - np.power(1.0 - t, 3.0)

    @staticmethod
    def ease_in_out_cubic(t: float | np.ndarray) -> float | np.ndarray:
        """Smooth S-curve acceleration and deceleration."""
        return np.where(t < 0.5, 4.0 * t * t * t, 1.0 - np.power(-2.0 * t + 2.0, 3.0) / 2.0)

    @staticmethod
    def petal_harmonic(
        angles: np.ndarray,
        lobes: int,
        depth: float,
        rotation: float,
    ) -> np.ndarray:
        """Calculates multi-petal polar modulation factor: (1.0 + depth * cos(lobes * theta + rot))."""
        return 1.0 + depth * np.cos(lobes * angles + rotation)
