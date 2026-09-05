"""Tests for K556 physical layout mapping."""
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider


def test_k556_layout_structure():
    provider = K556LayoutProvider()
    assert provider.get_device_name() == "Redragon K556RGB-M"
    assert provider.get_key_count() == 104

    coords = provider.get_coordinates()
    assert len(coords) == 104

    # Ensure all coordinates are bounded in [0, 1]
    x_arr, y_arr = provider.get_coordinate_arrays()
    assert len(x_arr) == 104
    assert len(y_arr) == 104
    assert (x_arr >= 0.0).all() and (x_arr <= 1.0).all()
    assert (y_arr >= 0.0).all() and (y_arr <= 1.0).all()

    # Verify key names exist
    names = [k.name for k in coords]
    assert "Escape" in names
    assert "Space" in names
    assert "Enter" in names
    assert "NumLock" in names
