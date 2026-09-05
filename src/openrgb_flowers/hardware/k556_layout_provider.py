"""Physical 2D layout mapping provider for Redragon K556RGB-M (ANSI 104 keys)."""
from __future__ import annotations
from typing import List, Tuple
import numpy as np
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.models.key_coordinate import KeyCoordinate


class K556LayoutProvider(ILayoutProvider):
    """High-precision physical 2D layout model for the Redragon K556RGB-M mechanical keyboard.

    Maps all 104 ANSI mechanical keys with their exact physical millimeter-proportional
    spacing, including the F-row gaps, navigation cluster island, arrow cluster, and numeric keypad.
    """

    DEVICE_NAME = "Redragon K556RGB-M"

    def __init__(self) -> None:
        self._keys: List[KeyCoordinate] = self._build_k556_layout()
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
    def _build_k556_layout(cls) -> List[KeyCoordinate]:
        """Constructs 104 keys with physical normalized coordinates."""
        # Total keyboard width is approx 22.5 key-units (U), height is 6.5 U.
        total_w = 22.5
        total_h = 6.2

        keys: List[KeyCoordinate] = []
        led_idx = 0

        # Row 0: Function Keys (Y center ~ 0.5 U)
        y_r0 = 0.5 / total_h
        r0_defs = [
            ("Escape", 0.5),
            # Gap
            ("F1", 2.0), ("F2", 3.0), ("F3", 4.0), ("F4", 5.0),
            # Gap
            ("F5", 6.5), ("F6", 7.5), ("F7", 8.5), ("F8", 9.5),
            # Gap
            ("F9", 11.0), ("F10", 12.0), ("F11", 13.0), ("F12", 14.0),
            # Gap
            ("PrintScreen", 15.5), ("ScrollLock", 16.5), ("Pause", 17.5),
        ]
        for name, x_u in r0_defs:
            keys.append(KeyCoordinate(name=name, index=led_idx, x=x_u / total_w, y=y_r0, row=0, col=int(x_u)))
            led_idx += 1

        # Row 1: Number Row (Y center ~ 1.7 U)
        y_r1 = 1.7 / total_h
        r1_defs = [
            ("Grave", 0.5), ("1", 1.5), ("2", 2.5), ("3", 3.5), ("4", 4.5),
            ("5", 5.5), ("6", 6.5), ("7", 7.5), ("8", 8.5), ("9", 9.5),
            ("0", 10.5), ("Minus", 11.5), ("Equal", 12.5), ("Backspace", 14.0),
            # Nav
            ("Insert", 15.5), ("Home", 16.5), ("PageUp", 17.5),
            # Numpad
            ("NumLock", 19.0), ("NumSlash", 20.0), ("NumAsterisk", 21.0), ("NumMinus", 22.0),
        ]
        for name, x_u in r1_defs:
            keys.append(KeyCoordinate(name=name, index=led_idx, x=x_u / total_w, y=y_r1, row=1, col=int(x_u)))
            led_idx += 1

        # Row 2: QWERTY Row (Y center ~ 2.7 U)
        y_r2 = 2.7 / total_h
        r2_defs = [
            ("Tab", 0.75), ("Q", 2.0), ("W", 3.0), ("E", 4.0), ("R", 5.0),
            ("T", 6.0), ("Y", 7.0), ("U", 8.0), ("I", 9.0), ("O", 10.0),
            ("P", 11.0), ("LeftBracket", 12.0), ("RightBracket", 13.0), ("Backslash", 14.25),
            # Nav
            ("Delete", 15.5), ("End", 16.5), ("PageDown", 17.5),
            # Numpad
            ("Num7", 19.0), ("Num8", 20.0), ("Num9", 21.0), ("NumPlus", 22.0),
        ]
        for name, x_u in r2_defs:
            keys.append(KeyCoordinate(name=name, index=led_idx, x=x_u / total_w, y=y_r2, row=2, col=int(x_u)))
            led_idx += 1

        # Row 3: Home Row (Y center ~ 3.7 U)
        y_r3 = 3.7 / total_h
        r3_defs = [
            ("CapsLock", 0.88), ("A", 2.25), ("S", 3.25), ("D", 4.25), ("F", 5.25),
            ("G", 6.25), ("H", 7.25), ("J", 8.25), ("K", 9.25), ("L", 10.25),
            ("Semicolon", 11.25), ("Apostrophe", 12.25), ("Enter", 13.88),
            # Numpad
            ("Num4", 19.0), ("Num5", 20.0), ("Num6", 21.0),
        ]
        for name, x_u in r3_defs:
            keys.append(KeyCoordinate(name=name, index=led_idx, x=x_u / total_w, y=y_r3, row=3, col=int(x_u)))
            led_idx += 1

        # Row 4: Shift Row (Y center ~ 4.7 U)
        y_r4 = 4.7 / total_h
        r4_defs = [
            ("LeftShift", 1.12), ("Z", 2.75), ("X", 3.75), ("C", 4.75), ("V", 5.75),
            ("B", 6.75), ("N", 7.75), ("M", 8.75), ("Comma", 9.75), ("Period", 10.75),
            ("Slash", 11.75), ("RightShift", 13.38),
            # Arrow
            ("UpArrow", 16.5),
            # Numpad
            ("Num1", 19.0), ("Num2", 20.0), ("Num3", 21.0), ("NumEnter", 22.0),
        ]
        for name, x_u in r4_defs:
            keys.append(KeyCoordinate(name=name, index=led_idx, x=x_u / total_w, y=y_r4, row=4, col=int(x_u)))
            led_idx += 1

        # Row 5: Bottom Row (Y center ~ 5.7 U)
        y_r5 = 5.7 / total_h
        r5_defs = [
            ("LeftControl", 0.62), ("LeftWindows", 1.88), ("LeftAlt", 3.12),
            ("Space", 7.0),
            ("RightAlt", 10.88), ("RightWindows", 12.12), ("Menu", 13.38), ("RightControl", 14.38),
            # Arrows
            ("LeftArrow", 15.5), ("DownArrow", 16.5), ("RightArrow", 17.5),
            # Numpad
            ("Num0", 19.5), ("NumPeriod", 21.0),
        ]
        for name, x_u in r5_defs:
            keys.append(KeyCoordinate(name=name, index=led_idx, x=x_u / total_w, y=y_r5, row=5, col=int(x_u)))
            led_idx += 1

        return keys

    @classmethod
    def find_coordinate_by_name(cls, raw_name: str) -> KeyCoordinate | None:
        """Looks up physical coordinate by standard key or OpenRGB LED name."""
        clean = (
            raw_name.lower()
            .replace("key:", "")
            .replace("numpad", "num")
            .replace("arrow", "")
            .replace(" ", "")
            .replace("_", "")
            .replace("-", "")
        )
        for k in cls._build_k556_layout():
            k_clean = (
                k.name.lower()
                .replace("arrow", "")
                .replace(" ", "")
                .replace("_", "")
                .replace("-", "")
            )
            if clean == k_clean:
                return k
        return None
