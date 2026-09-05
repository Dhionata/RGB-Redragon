"""Nordic Aurora Borealis organic color palette."""
from openrgb_flowers.effects.palettes.base_palette import BaseColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB


class AuroraPalette(BaseColorPalette):
    """Aurora Borealis: Vivid Polar Green -> Emerald -> Turquoise -> Royal Violet."""

    def __init__(self) -> None:
        super().__init__(
            name="aurora",
            stops=[
                (0.0, ColorRGB(0, 255, 135)),    # Polar Green
                (0.3, ColorRGB(96, 239, 255)),   # Turquoise
                (0.6, ColorRGB(0, 180, 216)),    # Deep Ice Blue
                (0.85, ColorRGB(123, 44, 191)),  # Royal Violet
                (1.0, ColorRGB(224, 86, 253)),   # Radiant Magenta
            ],
        )
