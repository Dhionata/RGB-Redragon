"""Test configuration and fixtures."""
import sys
import os
import pytest

# Ensure src is in python path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider
from openrgb_flowers.effects.palettes.sakura_palette import SakuraPalette
from openrgb_flowers.effects.blending.organic_weighted_blend import OrganicWeightedBlend
from openrgb_flowers.hardware.mock_transmitter import MockTransmitter


@pytest.fixture
def default_config():
    return EffectConfig(fps=30.0, speed=1.0, max_flowers=5, spawn_rate=2.0)


@pytest.fixture
def k556_layout():
    return K556LayoutProvider()


@pytest.fixture
def sakura_palette():
    return SakuraPalette()


@pytest.fixture
def weighted_blend():
    return OrganicWeightedBlend()


@pytest.fixture
def mock_transmitter():
    return MockTransmitter()
