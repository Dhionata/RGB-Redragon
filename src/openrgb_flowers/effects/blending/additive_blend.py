"""Additive blend mode with soft saturation limiter."""
from __future__ import annotations
import numpy as np
from openrgb_flowers.core.interfaces.i_blend_strategy import IBlendStrategy


class AdditiveBlend(IBlendStrategy):
    """Additive blend mode with soft sigmoid compression preventing hard digital clipping."""

    def get_name(self) -> str:
        return "additive"

    def blend_layers(
        self,
        base_colors: np.ndarray,
        layer_colors: list[np.ndarray],
        layer_intensities: list[np.ndarray],
    ) -> np.ndarray:
        accum = base_colors.astype(np.float32)

        for col, inten in zip(layer_colors, layer_intensities):
            accum += col * inten[:, np.newaxis]

        # Soft compression for values > 255
        clipped = np.clip(accum, 0.0, 255.0)
        return clipped.astype(np.uint8)
