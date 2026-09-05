"""Provence Lavender color palette."""
from openrgb_flowers.effects.palettes.base_palette import BaseColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB


class LavenderPalette(BaseColorPalette):
    """Provence Lavender: Deep midnight amethyst -> Floral violet -> Delicate lilac mist."""

    def __init__(self) -> None:
        super().__init__(
            name="lavender",
            stops=[
                (0.0, ColorRGB(95, 25, 140)),   # Deep royal amethyst
                (0.3, ColorRGB(147, 88, 204)),  # Purple floral petal
                (0.65, ColorRGB(186, 140, 245)),# Lilac bloom
                (0.85, ColorRGB(215, 185, 255)),# Soft periwinkle
                (1.0, ColorRGB(240, 230, 255)), # Morning mist tip
            ],
        )
