"""Tests for RGB and HSV color domain models."""
import pytest
from openrgb_flowers.core.models.color_rgb import ColorRGB
from openrgb_flowers.core.models.color_hsv import ColorHSV


def test_color_rgb_clamping():
    c = ColorRGB(-10, 300, 128)
    assert c.r == 0
    assert c.g == 255
    assert c.b == 128


def test_color_rgb_normalization():
    c = ColorRGB(255, 0, 128)
    norm = c.to_normalized()
    assert norm[0] == 1.0
    assert norm[1] == 0.0
    assert abs(norm[2] - 128 / 255.0) < 1e-4


def test_color_rgb_hex_conversion():
    c = ColorRGB(255, 105, 180)
    assert c.to_hex() == "#FF69B4"
    parsed = ColorRGB.from_hex("#FF69B4")
    assert parsed.r == 255
    assert parsed.g == 105
    assert parsed.b == 180


def test_color_hsv_to_rgb():
    # Pure Red: H=0, S=1, V=1
    hsv_red = ColorHSV(0.0, 1.0, 1.0)
    rgb_red = hsv_red.to_rgb()
    assert rgb_red.r == 255
    assert rgb_red.g == 0
    assert rgb_red.b == 0

    # Pure Green: H=120, S=1, V=1
    hsv_green = ColorHSV(120.0, 1.0, 1.0)
    rgb_green = hsv_green.to_rgb()
    assert rgb_green.r == 0
    assert rgb_green.g == 255
    assert rgb_green.b == 0


def test_color_rgb_to_hsv_roundtrip():
    original = ColorRGB(200, 100, 50)
    hsv = ColorHSV.from_rgb(original)
    recovered = hsv.to_rgb()
    assert abs(recovered.r - original.r) <= 1
    assert abs(recovered.g - original.g) <= 1
    assert abs(recovered.b - original.b) <= 1
