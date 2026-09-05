"""Tests for vectorized FastColorMath and EasingFunctions."""
import numpy as np
from openrgb_flowers.math.fast_color import FastColorMath
from openrgb_flowers.math.easing import EasingFunctions
from openrgb_flowers.math.spatial_grid import SpatialGrid


def test_hsv_to_rgb_vectorized():
    h = np.array([0.0, 60.0, 120.0, 180.0, 240.0, 300.0], dtype=np.float32)
    s = np.ones(6, dtype=np.float32)
    v = np.ones(6, dtype=np.float32)

    rgb = FastColorMath.hsv_to_rgb_vectorized(h, s, v)
    assert rgb.shape == (6, 3)

    # Red
    assert np.allclose(rgb[0], [255, 0, 0], atol=1.0)
    # Yellow
    assert np.allclose(rgb[1], [255, 255, 0], atol=1.0)
    # Green
    assert np.allclose(rgb[2], [0, 255, 0], atol=1.0)
    # Cyan
    assert np.allclose(rgb[3], [0, 255, 255], atol=1.0)
    # Blue
    assert np.allclose(rgb[4], [0, 0, 255], atol=1.0)
    # Magenta
    assert np.allclose(rgb[5], [255, 0, 255], atol=1.0)


def test_smoothstep():
    x = np.array([-1.0, 0.0, 0.5, 1.0, 2.0], dtype=np.float32)
    s = EasingFunctions.smoothstep(0.0, 1.0, x)
    assert s[0] == 0.0
    assert s[1] == 0.0
    assert s[2] == 0.5
    assert s[3] == 1.0
    assert s[4] == 1.0


def test_petal_harmonic():
    angles = np.array([0.0, np.pi / 4.0, np.pi / 2.0], dtype=np.float32)
    h = EasingFunctions.petal_harmonic(angles, lobes=4, depth=0.2, rotation=0.0)
    # At 0 rad: cos(0) = 1 -> 1.0 + 0.2 = 1.2
    assert abs(h[0] - 1.2) < 1e-4
    # At pi/4 rad: cos(4 * pi / 4) = cos(pi) = -1 -> 1.0 - 0.2 = 0.8
    assert abs(h[1] - 0.8) < 1e-4


def test_spatial_grid_aspect_ratio():
    grid = SpatialGrid(aspect_ratio=3.7)
    x = np.array([0.5, 0.6], dtype=np.float32)
    y = np.array([0.5, 0.5], dtype=np.float32)
    dx, dy, dists, _ = grid.correct_aspect_ratio(x, y, center_x=0.5, center_y=0.5)

    assert dists[0] == 0.0
    # Corrected dx should be 0.1 * 3.7 = 0.37
    assert abs(dists[1] - 0.37) < 1e-4
