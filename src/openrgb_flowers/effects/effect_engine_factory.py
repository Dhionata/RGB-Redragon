"""Factory for instantiating lighting effect engines following SOLID Open/Closed principle."""
from __future__ import annotations
from typing import Optional

from openrgb_flowers.core.interfaces.i_effect_engine import IEffectEngine
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette
from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.effects.blooming_engine import BloomingEngine
from openrgb_flowers.effects.random_blend_engine import RandomBlendEngine
from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry


class EffectEngineFactory:
    """Factory responsible for instantiating effect engines."""

    EFFECT_BLOOMING = "blooming"
    EFFECT_RANDOM_BLEND = "random_blend"

    AVAILABLE_EFFECTS = [
        EFFECT_BLOOMING,
        EFFECT_RANDOM_BLEND,
    ]

    @classmethod
    def create_engine(
        cls,
        effect_name: str,
        config: EffectConfig,
        layout_provider: ILayoutProvider,
        palette: Optional[IColorPalette] = None,
    ) -> IEffectEngine:
        """Instantiates the requested effect engine.

        Args:
            effect_name: Identifier ('blooming', 'random_blend', etc.)
            config: Effect configuration instance
            layout_provider: Target hardware layout provider
            palette: Optional custom palette instance (defaults to config.palette_name)
        """
        clean_name = effect_name.strip().lower().replace("-", "_").replace(" ", "_")

        resolved_palette = palette or PaletteRegistry.get(config.palette_name)

        if clean_name in ("random_blend", "random", "blend", "chaos", "matrix_blend", "all_keys"):
            return RandomBlendEngine(
                config=config,
                layout_provider=layout_provider,
                palette=resolved_palette,
            )

        # Default fallback is organic blooming
        return BloomingEngine(
            config=config,
            layout_provider=layout_provider,
            palette=resolved_palette,
        )
