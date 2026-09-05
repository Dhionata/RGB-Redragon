"""Cyberpunk high-contrast neon chromatic palette."""
from openrgb_flowers.effects.palettes.base_palette import BaseColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB


class CyberpunkPalette(BaseColorPalette):
    """Cyberpunk: Electric Cyan -> Hot Magenta -> Acid Yellow -> Deep Violet."""

    def __init__(self) -> None:
        super().__init__(
            name="cyberpunk",
            stops=[
                (0.0, ColorRGB(0, 240, 255)),    # Electric Neon Cyan
                (0.3, ColorRGB(255, 0, 128)),   # Hot Magenta
                (0.6, ColorRGB(255, 230, 0)),   # Acid Yellow
                (0.85, ColorRGB(157, 0, 255)),  # Electric Violet
                (1.0, ColorRGB(0, 255, 170)),   # Neon Mint Green
            ],
        )
