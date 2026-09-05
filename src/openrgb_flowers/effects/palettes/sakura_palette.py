"""Japanese Sakura (Cherry Blossom) color palette."""
from openrgb_flowers.effects.palettes.base_palette import BaseColorPalette
from openrgb_flowers.core.models.color_rgb import ColorRGB


class SakuraPalette(BaseColorPalette):
    """Sakura Blossom: Golden stamen center -> Vibrant floral pink -> Soft ivory petal tips."""

    def __init__(self) -> None:
        super().__init__(
            name="sakura",
            stops=[
                (0.0, ColorRGB(255, 215, 64)),   # Warm golden stamen
                (0.2, ColorRGB(255, 105, 180)),  # Hot pink petal throat
                (0.55, ColorRGB(255, 182, 193)), # Soft cherry blossom pink
                (0.85, ColorRGB(255, 230, 240)), # Delicate petal blush
                (1.0, ColorRGB(245, 250, 255)),  # Frost ivory petal tip
            ],
        )
