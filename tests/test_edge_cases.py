"""Explicit tests for edge cases, boundaries, and error conditions."""
import pytest
import numpy as np

from openrgb_flowers.core.models.color_rgb import ColorRGB
from openrgb_flowers.core.models.color_hsv import ColorHSV
from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.core.models.key_coordinate import KeyCoordinate
from openrgb_flowers.core.exceptions import ConfigurationError, DeviceNotFoundError
from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry
from openrgb_flowers.effects.flower_instance import FlowerInstance
from openrgb_flowers.effects.petal_geometry import PetalGeometry
from openrgb_flowers.effects.blooming_engine import BloomingEngine
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider
from openrgb_flowers.hardware.mock_transmitter import MockTransmitter
from openrgb_flowers.effects.blending.organic_weighted_blend import OrganicWeightedBlend


def test_color_rgb_invalid_hex():
    with pytest.raises(ValueError):
        ColorRGB.from_hex("invalid")
    with pytest.raises(ValueError):
        ColorRGB.from_hex("#12345")  # Too short


def test_color_hsv_boundary_angles():
    # Negative angle wraps around
    hsv_neg = ColorHSV(-60.0, 1.0, 1.0)
    assert hsv_neg.h == 300.0

    # Over 360 wraps around
    hsv_over = ColorHSV(450.0, 1.0, 1.0)
    assert hsv_over.h == 90.0


def test_key_coordinate_out_of_bounds_clamping():
    k = KeyCoordinate(name="Test", index=0, x=-0.5, y=1.5, row=0, col=0)
    assert k.x == 0.0
    assert k.y == 1.0


def test_effect_config_invalid_boundaries():
    # FPS <= 0
    with pytest.raises(ConfigurationError):
        EffectConfig(fps=0.0).validate()

    # FPS > 120
    with pytest.raises(ConfigurationError):
        EffectConfig(fps=240.0).validate()

    # Speed <= 0
    with pytest.raises(ConfigurationError):
        EffectConfig(speed=0.0).validate()

    # Brightness out of range
    with pytest.raises(ConfigurationError):
        EffectConfig(brightness=-0.1).validate()
    with pytest.raises(ConfigurationError):
        EffectConfig(brightness=1.5).validate()

    # Saturation out of range
    with pytest.raises(ConfigurationError):
        EffectConfig(saturation=-0.5).validate()
    with pytest.raises(ConfigurationError):
        EffectConfig(saturation=4.0).validate()


    # Petals invalid
    with pytest.raises(ConfigurationError):
        EffectConfig(petal_options=[1]).validate()


def test_palette_registry_unknown():
    with pytest.raises(KeyError) as exc_info:
        PaletteRegistry.get("nonexistent_flower")
    assert "Available" in str(exc_info.value)


def test_flower_instance_zero_radius():
    palette = PaletteRegistry.get("sakura")
    # Flower at age 0 with 0 dt has 0 radius
    flower = FlowerInstance(center_x=0.5, center_y=0.5, palette=palette, max_radius=0.4, lifespan=3.0)
    x = np.array([0.5], dtype=np.float32)
    y = np.array([0.5], dtype=np.float32)
    intensities, colors = flower.evaluate(x, y)
    assert intensities[0] == 0.0
    assert colors[0, 0] == 0.0


def test_organic_weighted_blend_empty_layers():
    blend = OrganicWeightedBlend()
    base = np.full((5, 3), 50.0, dtype=np.float32)
    result = blend.blend_layers(base, [], [])
    assert result.shape == (5, 3)
    assert np.all(result == 50)


def test_engine_reset():
    config = EffectConfig(fps=30.0, max_flowers=3)
    layout = K556LayoutProvider()
    engine = BloomingEngine(config=config, layout_provider=layout)

    # Spawn blooms
    for _ in range(20):
        engine.tick(0.1)
    assert engine.get_active_flower_count() > 0

    engine.reset()
    assert engine.get_active_flower_count() == 0
