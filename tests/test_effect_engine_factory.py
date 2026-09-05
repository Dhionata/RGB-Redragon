"""Unit tests for EffectEngineFactory."""
import pytest

from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.effects.effect_engine_factory import EffectEngineFactory
from openrgb_flowers.effects.blooming_engine import BloomingEngine
from openrgb_flowers.effects.random_blend_engine import RandomBlendEngine
from openrgb_flowers.hardware.k556_matrix_layout_provider import K556MatrixLayoutProvider


def test_create_blooming_engine():
    layout = K556MatrixLayoutProvider()
    config = EffectConfig(effect_type="blooming")
    engine = EffectEngineFactory.create_engine("blooming", config, layout)
    assert isinstance(engine, BloomingEngine)


def test_create_random_blend_engine():
    layout = K556MatrixLayoutProvider()
    config = EffectConfig(effect_type="random_blend")
    engine = EffectEngineFactory.create_engine("random_blend", config, layout)
    assert isinstance(engine, RandomBlendEngine)


def test_create_engine_fallback():
    layout = K556MatrixLayoutProvider()
    config = EffectConfig()
    engine = EffectEngineFactory.create_engine("unknown_effect", config, layout)
    assert isinstance(engine, BloomingEngine)
