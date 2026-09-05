"""Screen blend mode strategy."""
from __future__ import annotations
import numpy as np
from openrgb_flowers.core.interfaces.i_blend_strategy import IBlendStrategy


class ScreenBlend(IBlendStrategy):
    """Photographic Screen blend mode: 1 - (1 - A) * (1 - B)."""

    def get_name(self) -> str:
        return "screen"

    def blend_layers(
        self,
        base_colors: np.ndarray,
        layer_colors: list[np.ndarray],
        layer_intensities: list[np.ndarray],
    ) -> np.ndarray:
        result = base_colors.astype(np.float32) / 255.0

        for col, inten in zip(layer_colors, layer_intensities):
            layer_norm = (col.astype(np.float32) / 255.0) * inten[:, np.newaxis]
            result = 1.0 - (1.0 - result) * (1.0 - layer_norm)

        return np.clip(result * 255.0, 0, 255).astype(np.uint8)
