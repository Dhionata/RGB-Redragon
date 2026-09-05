"""Tests for PetalGeometry and FlowerInstance."""
import numpy as np
from openrgb_flowers.effects.petal_geometry import PetalGeometry
from openrgb_flowers.effects.flower_instance import FlowerInstance
from openrgb_flowers.effects.palettes.sakura_palette import SakuraPalette


def test_petal_radii_calculation():
    angles = np.array([0.0, np.pi], dtype=np.float32)
    radii = PetalGeometry.compute_petal_radii(angles, base_radius=0.4, petal_count=4, petal_depth=0.2, rotation=0.0)
    assert len(radii) == 2
    assert radii[0] > 0.4
    assert radii[1] > 0.4


def test_flower_lifecycle():
    palette = SakuraPalette()
    flower = FlowerInstance(
        center_x=0.5,
        center_y=0.5,
        palette=palette,
        petal_count=5,
        max_radius=0.4,
        lifespan=3.0,
    )
    assert flower.is_alive()
    assert flower.age == 0.0

    # Advance halfway
    flower.update(1.5)
    assert flower.is_alive()
    assert 0.45 < flower.get_lifecycle_phase() < 0.55
    assert flower.get_intensity_envelope() > 0.8

    # Advance past lifespan
    flower.update(2.0)
    assert not flower.is_alive()


def test_flower_evaluate():
    palette = SakuraPalette()
    flower = FlowerInstance(center_x=0.5, center_y=0.5, palette=palette, max_radius=0.4, lifespan=3.0)
    flower.update(1.0)

    # Point right at center vs far away
    x = np.array([0.5, 0.95], dtype=np.float32)
    y = np.array([0.5, 0.95], dtype=np.float32)
    intensities, colors = flower.evaluate(x, y)

    assert intensities[0] > 0.5  # High intensity at center
    assert intensities[1] == 0.0  # Zero intensity far away
    assert colors.shape == (2, 3)
