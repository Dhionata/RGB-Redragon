"""Wild Sunflower color palette."""
from openrgb_flowers.effects.palettes.base_palette import BaseColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB


class SunflowerPalette(BaseColorPalette):
    """Wild Sunflower: Rich chocolate center -> Warm amber -> Luminous golden yellow."""

    def __init__(self) -> None:
        super().__init__(
            name="sunflower",
            stops=[
                (0.0, ColorRGB(90, 45, 15)),    # Roasted chocolate stamen
                (0.2, ColorRGB(210, 105, 10)),  # Deep amber transition
                (0.55, ColorRGB(255, 170, 0)),  # Rich golden sunflower petal
                (0.85, ColorRGB(255, 220, 30)), # Radiant sunny yellow
                (1.0, ColorRGB(255, 245, 140)), # Sunlit bright tip
            ],
        )
