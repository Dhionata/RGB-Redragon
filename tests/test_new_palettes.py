"""Unit tests for Cyberpunk and Aurora palettes."""
import pytest

from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry
from openrgb_flowers.effects.palettes.cyberpunk_palette import CyberpunkPalette
from openrgb_flowers.effects.palettes.aurora_palette import AuroraPalette


def test_cyberpunk_palette_sampling():
    pal = PaletteRegistry.get("cyberpunk")
    assert isinstance(pal, CyberpunkPalette)
    assert pal.get_name() == "cyberpunk"

    c_start = pal.sample(0.0)
    assert c_start.r == 0
    assert c_start.g == 240
    assert c_start.b == 255

    c_mid = pal.sample(0.5)
    assert 0 <= c_mid.r <= 255
    assert 0 <= c_mid.g <= 255
    assert 0 <= c_mid.b <= 255


def test_aurora_palette_sampling():
    pal = PaletteRegistry.get("aurora")
    assert isinstance(pal, AuroraPalette)
    assert pal.get_name() == "aurora"

    c_start = pal.sample(0.0)
    assert c_start.r == 0
    assert c_start.g == 255
    assert c_start.b == 135
