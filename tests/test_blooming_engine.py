"""Tests for BloomingEngine."""
from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider
from openrgb_flowers.effects.blooming_engine import BloomingEngine


def test_engine_initialization_and_tick():
    config = EffectConfig(fps=30.0, max_flowers=4, spawn_rate=5.0)
    layout = K556LayoutProvider()
    engine = BloomingEngine(config=config, layout_provider=layout)

    assert engine.get_active_flower_count() == 0

    # First tick will spawn the first flower
    frame1 = engine.tick(0.033)
    assert frame1.frame_index == 1
    assert frame1.led_count == layout.get_key_count()
    assert frame1.colors.shape == (layout.get_key_count(), 3)
    assert engine.get_active_flower_count() >= 1

    # Simulate 2 seconds of blooming
    for _ in range(60):
        frame = engine.tick(0.033)

    assert frame.frame_index == 61
    assert engine.get_active_flower_count() <= config.max_flowers
