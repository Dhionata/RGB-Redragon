"""Unit tests for RandomBlendEngine."""
import numpy as np
import pytest

from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.effects.random_blend_engine import RandomBlendEngine
from openrgb_flowers.hardware.k556_matrix_layout_provider import K556MatrixLayoutProvider
from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry


def test_random_blend_engine_initialization():
    layout = K556MatrixLayoutProvider()
    config = EffectConfig(effect_type="random_blend", speed=1.5, brightness=0.8)
    engine = RandomBlendEngine(config=config, layout_provider=layout)

    assert engine.get_active_flower_count() == 132
    assert engine.get_config() == config


def test_random_blend_engine_tick_outputs_valid_frame():
    layout = K556MatrixLayoutProvider()
    config = EffectConfig(effect_type="random_blend", palette_name="rainbow", speed=2.0)
    engine = RandomBlendEngine(config=config, layout_provider=layout)

    frame1 = engine.tick(0.033)
    assert frame1.frame_index == 1
    assert frame1.led_count == 132
    assert frame1.colors.shape == (132, 3)
    assert frame1.colors.dtype == np.uint8

    # Ensure keys are illuminated (not all black)
    assert np.mean(frame1.colors) > 0

    # Advance several frames
    frame2 = engine.tick(0.033)
    assert frame2.frame_index == 2
    # Progress changed
    assert not np.array_equal(frame1.colors, frame2.colors)


def test_random_blend_engine_reset():
    layout = K556MatrixLayoutProvider()
    config = EffectConfig(effect_type="random_blend")
    engine = RandomBlendEngine(config=config, layout_provider=layout)

    for _ in range(10):
        engine.tick(0.05)

    assert engine._frame_count == 10
    engine.reset()
    assert engine._frame_count == 0
    assert engine._sim_time == 0.0


def test_random_blend_engine_brightness_clamping():
    layout = K556MatrixLayoutProvider()
    config = EffectConfig(effect_type="random_blend", brightness=0.0)
    engine = RandomBlendEngine(config=config, layout_provider=layout)

    frame = engine.tick(0.033)
    # 0.0 brightness should output all zeros
    assert np.all(frame.colors == 0)
