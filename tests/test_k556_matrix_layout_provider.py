"""Unit tests for K556MatrixLayoutProvider (132 keys hardware matrix)."""
import numpy as np
import pytest
from openrgb_flowers.hardware.k556_matrix_layout_provider import K556MatrixLayoutProvider


def test_matrix_layout_key_count():
    layout = K556MatrixLayoutProvider()
    assert layout.get_key_count() == 132
    assert len(layout.get_coordinates()) == 132


def test_matrix_layout_coordinate_arrays():
    layout = K556MatrixLayoutProvider()
    x_arr, y_arr = layout.get_coordinate_arrays()

    assert isinstance(x_arr, np.ndarray)
    assert isinstance(y_arr, np.ndarray)
    assert x_arr.shape == (132,)
    assert y_arr.shape == (132,)
    assert x_arr.dtype == np.float32
    assert y_arr.dtype == np.float32

    assert np.all(x_arr >= 0.0) and np.all(x_arr <= 1.0)
    assert np.all(y_arr >= 0.0) and np.all(y_arr <= 1.0)


def test_matrix_layout_known_keys():
    layout = K556MatrixLayoutProvider()
    coords = layout.get_coordinates()

    # Index 0: (row 0, col 0) -> Escape
    assert coords[0].name == "Escape"
    assert coords[0].row == 0
    assert coords[0].col == 0

    # Index 6 * 22 has 6 rows: row 5 col 6 is Space: index = 5 * 22 + 6 = 116
    assert coords[116].name == "Space"
    assert coords[116].row == 5
    assert coords[116].col == 6
