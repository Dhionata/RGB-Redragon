"""Hardware matrix 6x22 layout provider for Redragon K556RGB-M (132 positions)."""
from __future__ import annotations
from typing import List, Tuple
import numpy as np
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.models.key_coordinate import KeyCoordinate


class K556MatrixLayoutProvider(ILayoutProvider):
    """Full 6x22 hardware matrix layout provider for the Redragon K556RGB-M keyboard.

    Directly matches the microcontroller LED addressing space of 132 positions (6 rows x 22 columns),
    allowing zero-copy row-major chunking when sending frames directly via USB HID.
    """

    DEVICE_NAME = "Redragon K556RGB-M (Hardware Matrix)"
    ROWS = 6
    COLS = 22
    TOTAL_KEYS = ROWS * COLS  # 132

    # Mapping of (row, col) to standard key identifier from hardware firmware table
    MATRIX_KEY_NAMES: dict[tuple[int, int], str] = {
        # Row 0 (F-row & Media)
        (0, 0): "Escape",
        (0, 2): "F1", (0, 3): "F2", (0, 4): "F3", (0, 5): "F4",
        (0, 7): "F5", (0, 8): "F6", (0, 9): "F7", (0, 10): "F8",
        (0, 11): "F9", (0, 12): "F10", (0, 13): "F11", (0, 14): "F12",
        (0, 15): "PrintScreen", (0, 16): "ScrollLock", (0, 17): "Pause",

        # Row 1 (Number row & Nav top & Numpad top)
        (1, 0): "Grave", (1, 1): "1", (1, 2): "2", (1, 3): "3", (1, 4): "4",
        (1, 5): "5", (1, 6): "6", (1, 7): "7", (1, 8): "8", (1, 9): "9", (1, 10): "0",
        (1, 11): "Minus", (1, 12): "Equal", (1, 14): "Backspace",
        (1, 15): "Insert", (1, 16): "Home", (1, 17): "PageUp",
        (1, 18): "NumLock", (1, 19): "NumSlash", (1, 20): "NumAsterisk", (1, 21): "NumMinus",

        # Row 2 (QWERTY row)
        (2, 0): "Tab", (2, 1): "Q", (2, 2): "W", (2, 3): "E", (2, 4): "R",
        (2, 5): "T", (2, 6): "Y", (2, 7): "U", (2, 8): "I", (2, 9): "O", (2, 10): "P",
        (2, 11): "LeftBracket", (2, 12): "RightBracket",
        (2, 15): "Delete", (2, 16): "End", (2, 17): "PageDown",
        (2, 18): "Num7", (2, 19): "Num8", (2, 20): "Num9", (2, 21): "NumPlus",

        # Row 3 (Home row)
        (3, 0): "CapsLock", (3, 2): "A", (3, 3): "S", (3, 4): "D", (3, 5): "F",
        (3, 6): "G", (3, 7): "H", (3, 8): "J", (3, 9): "K", (3, 10): "L",
        (3, 11): "Semicolon", (3, 12): "Apostrophe", (3, 13): "Backslash", (3, 14): "Enter",
        (3, 18): "Num4", (3, 19): "Num5", (3, 20): "Num6",

        # Row 4 (Shift row & Arrow Up)
        (4, 0): "LeftShift", (4, 1): "IntlBackslash", (4, 2): "Z", (4, 3): "X", (4, 4): "C",
        (4, 5): "V", (4, 6): "B", (4, 7): "N", (4, 8): "M", (4, 9): "Comma", (4, 10): "Period",
        (4, 11): "Slash", (4, 12): "IntlRo", (4, 14): "RightShift",
        (4, 16): "UpArrow",
        (4, 18): "Num1", (4, 19): "Num2", (4, 20): "Num3", (4, 21): "NumEnter",

        # Row 5 (Bottom row & Arrows)
        (5, 0): "LeftControl", (5, 1): "LeftWindows", (5, 2): "LeftAlt", (5, 6): "Space",
        (5, 10): "RightAlt", (5, 11): "Fn", (5, 12): "Menu", (5, 13): "RightControl",
        (5, 15): "LeftArrow", (5, 16): "DownArrow", (5, 17): "RightArrow",
        (5, 18): "Num0", (5, 20): "NumPeriod",
    }

    def __init__(self) -> None:
        self._keys: List[KeyCoordinate] = self._build_matrix_layout()
        self._key_count = len(self._keys)
        self._x_array = np.array([k.x for k in self._keys], dtype=np.float32)
        self._y_array = np.array([k.y for k in self._keys], dtype=np.float32)

    def get_device_name(self) -> str:
        return self.DEVICE_NAME

    def get_key_count(self) -> int:
        return self._key_count

    def get_coordinates(self) -> List[KeyCoordinate]:
        return self._keys

    def get_coordinate_arrays(self) -> Tuple[np.ndarray, np.ndarray]:
        return self._x_array, self._y_array

    @classmethod
    def _build_matrix_layout(cls) -> List[KeyCoordinate]:
        """Builds all 132 key coordinate entries matching row-major hardware matrix."""
        keys: List[KeyCoordinate] = []
        max_col = float(cls.COLS - 1)
        max_row = float(cls.ROWS - 1)

        idx = 0
        for r in range(cls.ROWS):
            for c in range(cls.COLS):
                name = cls.MATRIX_KEY_NAMES.get((r, c), "")
                norm_x = c / max_col
                norm_y = r / max_row
                keys.append(KeyCoordinate(
                    name=name,
                    index=idx,
                    x=norm_x,
                    y=norm_y,
                    row=r,
                    col=c,
                ))
                idx += 1

        return keys
