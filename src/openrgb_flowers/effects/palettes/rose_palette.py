"""Rose Garden color palette."""
from openrgb_flowers.effects.palettes.base_palette import BaseColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB


class RosePalette(BaseColorPalette):
    """Velvet Rose: Dark crimson ruby center -> Deep scarlet body -> Fiery coral edge."""

    def __init__(self) -> None:
        super().__init__(
            name="rose",
            stops=[
                (0.0, ColorRGB(180, 10, 30)),   # Deep ruby stamen
                (0.25, ColorRGB(220, 20, 60)),  # Crimson velvet core
                (0.6, ColorRGB(255, 45, 85)),   # Radiant scarlet petal
                (0.85, ColorRGB(255, 110, 130)),# Coral blush rim
                (1.0, ColorRGB(255, 180, 190)), # Soft blossom edge
            ],
        )
