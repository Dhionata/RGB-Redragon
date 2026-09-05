"""Base class for multi-stop floral gradient palettes."""
from __future__ import annotations
from typing import List, Tuple
import numpy as np
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB


class BaseColorPalette(IColorPalette):
    """Abstract base palette interpolating across multiple floral gradient stops."""

    def __init__(
        self,
        name: str,
        stops: List[Tuple[float, ColorRGB]],
    ) -> None:
        self._name = name
        # Sort stops by position in [0, 1]
        self._stops = sorted(stops, key=lambda s: s[0])
        self._positions = np.array([s[0] for s in self._stops], dtype=np.float32)
        self._colors_array = np.array([s[1].to_tuple() for s in self._stops], dtype=np.float32)

    def get_name(self) -> str:
        return self._name

    def sample(self, t: float) -> ColorRGB:
        t_clamped = max(0.0, min(1.0, float(t)))
        if t_clamped <= self._positions[0]:
            c = self._colors_array[0]
            return ColorRGB(int(c[0]), int(c[1]), int(c[2]))
        if t_clamped >= self._positions[-1]:
            c = self._colors_array[-1]
            return ColorRGB(int(c[0]), int(c[1]), int(c[2]))

        idx = int(np.searchsorted(self._positions, t_clamped))
        p0, p1 = self._positions[idx - 1], self._positions[idx]
        factor = (t_clamped - p0) / (p1 - p0 + 1e-7)
        c0, c1 = self._colors_array[idx - 1], self._colors_array[idx]
        interpolated = c0 * (1.0 - factor) + c1 * factor
        return ColorRGB(int(round(interpolated[0])), int(round(interpolated[1])), int(round(interpolated[2])))

    def sample_vectorized(self, t_array: np.ndarray) -> np.ndarray:
        """Vectorized gradient lookup across array of t values in [0, 1]. Returns shape (N, 3)."""
        t_clamped = np.clip(t_array, 0.0, 1.0)
        n = len(t_clamped)
        result = np.zeros((n, 3), dtype=np.float32)

        # Interpolate along each color channel
        for ch in range(3):
            result[:, ch] = np.interp(t_clamped, self._positions, self._colors_array[:, ch])

        return result

    def get_center_color(self) -> ColorRGB:
        c = self._colors_array[0]
        return ColorRGB(int(c[0]), int(c[1]), int(c[2]))

    def get_petal_color(self) -> ColorRGB:
        mid_idx = len(self._colors_array) // 2
        c = self._colors_array[mid_idx]
        return ColorRGB(int(c[0]), int(c[1]), int(c[2]))

    def get_tip_color(self) -> ColorRGB:
        c = self._colors_array[-1]
        return ColorRGB(int(c[0]), int(c[1]), int(c[2]))
