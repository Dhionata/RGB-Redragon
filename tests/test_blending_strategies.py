"""Tests for layer blending strategies."""
import numpy as np
from openrgb_flowers.effects.blending.organic_weighted_blend import OrganicWeightedBlend
from openrgb_flowers.effects.blending.screen_blend import ScreenBlend
from openrgb_flowers.effects.blending.additive_blend import AdditiveBlend


def test_organic_weighted_blend():
    strategy = OrganicWeightedBlend()
    base = np.zeros((3, 3), dtype=np.float32)
    col1 = np.full((3, 3), 255.0, dtype=np.float32)
    col2 = np.full((3, 3), 100.0, dtype=np.float32)
    inten1 = np.array([1.0, 0.5, 0.0], dtype=np.float32)
    inten2 = np.array([0.0, 0.5, 1.0], dtype=np.float32)

    blended = strategy.blend_layers(base, [col1, col2], [inten1, inten2])
    assert blended.shape == (3, 3)
    # Item 0: 100% layer 1
    assert np.all(blended[0] >= 250)
    # Item 2: 100% layer 2
    assert np.all(blended[2] == 100)


def test_screen_blend():
    strategy = ScreenBlend()
    base = np.full((1, 3), 128.0, dtype=np.float32)
    layer = np.full((1, 3), 128.0, dtype=np.float32)
    inten = np.array([1.0], dtype=np.float32)

    blended = strategy.blend_layers(base, [layer], [inten])
    # 1 - (1 - 0.5)*(1 - 0.5) = 0.75 * 255 = 191
    assert abs(blended[0, 0] - 191) <= 2


def test_additive_blend():
    strategy = AdditiveBlend()
    base = np.full((1, 3), 150.0, dtype=np.float32)
    layer = np.full((1, 3), 150.0, dtype=np.float32)
    inten = np.array([1.0], dtype=np.float32)

    blended = strategy.blend_layers(base, [layer], [inten])
    # Should cap at 255
    assert blended[0, 0] == 255
