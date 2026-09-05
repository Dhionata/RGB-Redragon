"""Chromatic Rainbow Bloom color palette."""
from __future__ import annotations
import numpy as np
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB
from openrgb_flowers.math.fast_color import FastColorMath


class RainbowPalette(IColorPalette):
    """Dynamic rainbow bloom that cycles seamlessly across the entire floral spectrum."""

    def __init__(self, base_hue: float = 0.0) -> None:
        self._name = "rainbow"
        self._base_hue = float(base_hue) % 360.0

    def get_name(self) -> str:
        return self._name

    def sample(self, t: float) -> ColorRGB:
        hue = (self._base_hue + float(t) * 360.0) % 360.0
        sat = 1.0
        val = 1.0
        rgb_arr = FastColorMath.hsv_to_rgb_vectorized(
            np.array([hue], dtype=np.float32),
            np.array([sat], dtype=np.float32),
            np.array([val], dtype=np.float32),
        )
        c = rgb_arr[0]
        return ColorRGB(int(c[0]), int(c[1]), int(c[2]))

    def sample_vectorized(self, t_array: np.ndarray) -> np.ndarray:
        hues = (self._base_hue + t_array * 360.0) % 360.0
        sats = np.ones_like(t_array, dtype=np.float32)
        vals = np.ones_like(t_array, dtype=np.float32)
        return FastColorMath.hsv_to_rgb_vectorized(hues, sats, vals)

    def get_center_color(self) -> ColorRGB:
        return self.sample(0.0)

    def get_petal_color(self) -> ColorRGB:
        return self.sample(0.5)

    def get_tip_color(self) -> ColorRGB:
        return self.sample(1.0)
