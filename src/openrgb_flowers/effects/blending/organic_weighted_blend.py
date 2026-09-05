"""Organic weighted blending strategy."""
from __future__ import annotations
import numpy as np
from openrgb_flowers.core.interfaces.i_blend_strategy import IBlendStrategy


class OrganicWeightedBlend(IBlendStrategy):
    """Blends multiple floral layers organically based on petal intensities.

    Instead of blowing out to harsh white (clipping) like raw additive blending,
    this strategy mixes colors proportionally in linear color space and smoothly
    accumulates luminance, giving vibrant petal depth and natural botanical blending.
    """

    def get_name(self) -> str:
        return "weighted"

    def blend_layers(
        self,
        base_colors: np.ndarray,
        layer_colors: list[np.ndarray],
        layer_intensities: list[np.ndarray],
    ) -> np.ndarray:
        if not layer_colors:
            return np.clip(base_colors, 0, 255).astype(np.uint8)

        n = base_colors.shape[0]
        # Total weights accumulated across all active petals
        accum_color = np.zeros((n, 3), dtype=np.float32)
        total_weight = np.zeros((n, 1), dtype=np.float32)
        max_intensity = np.zeros((n, 1), dtype=np.float32)

        for col, inten in zip(layer_colors, layer_intensities):
            w = inten[:, np.newaxis]
            accum_color += col * w
            total_weight += w
            max_intensity = np.maximum(max_intensity, w)

        has_blooms = total_weight > 1e-5
        # Weighted floral mix
        floral_mix = np.zeros_like(accum_color)
        floral_mix[has_blooms[:, 0]] = accum_color[has_blooms[:, 0]] / total_weight[has_blooms[:, 0]]

        # Alpha blend between background and floral mix using max intensity
        alpha = np.clip(max_intensity, 0.0, 1.0)
        final_color = base_colors * (1.0 - alpha) + floral_mix * alpha

        return np.clip(final_color, 0, 255).astype(np.uint8)
