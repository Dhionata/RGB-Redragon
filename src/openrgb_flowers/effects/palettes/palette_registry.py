"""Registry and factory for floral palettes."""
from __future__ import annotations
from typing import Dict, List, Type
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette
from openrgb_flowers.effects.palettes.sakura_palette import SakuraPalette
from openrgb_flowers.effects.palettes.rose_palette import RosePalette
from openrgb_flowers.effects.palettes.lotus_palette import LotusPalette
from openrgb_flowers.effects.palettes.sunflower_palette import SunflowerPalette
from openrgb_flowers.effects.palettes.lavender_palette import LavenderPalette
from openrgb_flowers.effects.palettes.rainbow_palette import RainbowPalette
from openrgb_flowers.effects.palettes.cyberpunk_palette import CyberpunkPalette
from openrgb_flowers.effects.palettes.aurora_palette import AuroraPalette


class PaletteRegistry:
    """Registry providing thread-safe retrieval and instantiation of palettes."""

    _PALETTES: Dict[str, Type[IColorPalette]] = {
        "sakura": SakuraPalette,
        "rose": RosePalette,
        "lotus": LotusPalette,
        "sunflower": SunflowerPalette,
        "lavender": LavenderPalette,
        "rainbow": RainbowPalette,
        "cyberpunk": CyberpunkPalette,
        "aurora": AuroraPalette,
    }

    @classmethod
    def get(cls, name: str) -> IColorPalette:
        """Retrieves a palette instance by name (case-insensitive)."""
        clean_name = name.strip().lower()
        if clean_name not in cls._PALETTES:
            available = ", ".join(cls.list_available())
            raise KeyError(f"Unknown palette '{name}'. Available: {available}")
        return cls._PALETTES[clean_name]()

    @classmethod
    def list_available(cls) -> List[str]:
        """Returns list of registered palette names."""
        return list(cls._PALETTES.keys())

    @classmethod
    def register(cls, name: str, palette_cls: Type[IColorPalette]) -> None:
        """Registers a custom user or community palette."""
        cls._PALETTES[name.strip().lower()] = palette_cls
