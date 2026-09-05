"""Sacred Lotus Pond color palette."""
from openrgb_flowers.effects.palettes.base_palette import BaseColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB


class LotusPalette(BaseColorPalette):
    """Sacred Lotus: Saffron stamen -> Rich magenta body -> Mystic violet & cyan water dew."""

    def __init__(self) -> None:
        super().__init__(
            name="lotus",
            stops=[
                (0.0, ColorRGB(255, 200, 20)),  # Saffron gold pistil
                (0.25, ColorRGB(255, 60, 140)),  # Rich magenta petal
                (0.65, ColorRGB(180, 80, 230)),  # Mystic violet body
                (0.85, ColorRGB(100, 200, 240)), # Aquatic cyan dewdrop edge
                (1.0, ColorRGB(220, 245, 255)),  # Translucent water mist
            ],
        )
