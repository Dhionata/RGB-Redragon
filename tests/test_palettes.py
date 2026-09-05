"""Tests for floral palettes and registry."""
from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry
import numpy as np


def test_palette_registry_lookup():
    available = PaletteRegistry.list_available()
    assert "sakura" in available
    assert "rose" in available
    assert "lotus" in available
    assert "sunflower" in available
    assert "lavender" in available
    assert "rainbow" in available

    sakura = PaletteRegistry.get("sakura")
    assert sakura.get_name() == "sakura"


def test_palette_sampling():
    for name in PaletteRegistry.list_available():
        palette = PaletteRegistry.get(name)
        c_center = palette.get_center_color()
        c_petal = palette.get_petal_color()
        c_tip = palette.get_tip_color()

        assert 0 <= c_center.r <= 255
        assert 0 <= c_petal.g <= 255
        assert 0 <= c_tip.b <= 255

        t_arr = np.linspace(0.0, 1.0, 10, dtype=np.float32)
        samples = palette.sample_vectorized(t_arr)
        assert samples.shape == (10, 3)
        assert np.all((samples >= 0.0) & (samples <= 255.0))
