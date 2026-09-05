"""Dynamic layout adapter extracting 2D physical coordinates from OpenRGB zone data."""
from __future__ import annotations
from typing import Any, List, Optional, Tuple
import numpy as np
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.models.key_coordinate import KeyCoordinate
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider


class OpenRGBZoneLayoutProvider(ILayoutProvider):
    """Adapts live OpenRGB Zone data to the ILayoutProvider contract.

    If the device provides a matrix zone (ZoneType.MATRIX), it computes exact normalized
    coordinates from the controller matrix. If it is a linear zone or missing matrix data,
    it dynamically maps each LED by name to the physical K556 ANSI mechanical layout.
    Guarantees that keys are strictly ordered by index 0..total_leds-1 without shifting.
    """

    def __init__(self, device: Any, zone_index: int = 0) -> None:
        self._device = device
        self._device_name = getattr(device, "name", "OpenRGB Device")
        self._keys: List[KeyCoordinate] = []

        if device is not None:
            self._keys = self._extract_layout_from_device(device, zone_index)

        # Fallback to K556 layout if extraction yielded no keys
        if not self._keys:
            fallback = K556LayoutProvider()
            self._keys = fallback.get_coordinates()

        self._x_array = np.array([k.x for k in self._keys], dtype=np.float32)
        self._y_array = np.array([k.y for k in self._keys], dtype=np.float32)

    def get_device_name(self) -> str:
        return self._device_name

    def get_key_count(self) -> int:
        return len(self._keys)

    def get_coordinates(self) -> List[KeyCoordinate]:
        return self._keys

    def get_coordinate_arrays(self) -> Tuple[np.ndarray, np.ndarray]:
        return self._x_array, self._y_array

    @classmethod
    def _extract_layout_from_device(cls, device: Any, zone_index: int = 0) -> List[KeyCoordinate]:
        zones = getattr(device, "zones", [])
        dev_leds = getattr(device, "leds", [])
        total_leds = len(dev_leds)

        zone = zones[zone_index] if len(zones) > zone_index else None
        matrix_map = getattr(zone, "matrix_map", None) if zone else None
        mat_w = getattr(zone, "mat_width", None) if zone else None
        mat_h = getattr(zone, "mat_height", None) if zone else None

        # Determine total expected LEDs
        if total_leds == 0 and zone:
            total_leds = getattr(zone, "num_leds", 0)

        # Case 1: Matrix Zone is available
        if matrix_map and mat_w and mat_h and mat_w > 1 and mat_h > 1:
            matrix_dict: dict[int, tuple[int, int]] = {}
            for r_idx, row in enumerate(matrix_map):
                for c_idx, led_id in enumerate(row):
                    if led_id is not None:
                        matrix_dict[int(led_id)] = (r_idx, c_idx)

            if matrix_dict:
                max_id = max(matrix_dict.keys())
                target_count = max(total_leds, max_id + 1)
                keys: List[KeyCoordinate] = []

                for led_idx in range(target_count):
                    raw_led = dev_leds[led_idx] if led_idx < len(dev_leds) else None
                    name = getattr(raw_led, "name", f"Key_{led_idx}")

                    if led_idx in matrix_dict:
                        r_idx, c_idx = matrix_dict[led_idx]
                        norm_x = c_idx / max(1.0, float(mat_w - 1))
                        norm_y = r_idx / max(1.0, float(mat_h - 1))
                        row = r_idx
                        col = c_idx
                    else:
                        # Missing from matrix (e.g. logo or indicator): match name or fallback
                        named_coord = K556LayoutProvider.find_coordinate_by_name(name)
                        if named_coord:
                            norm_x = named_coord.x
                            norm_y = named_coord.y
                            row = named_coord.row
                            col = named_coord.col
                        else:
                            norm_x = led_idx / max(1.0, float(target_count - 1))
                            norm_y = 1.0
                            row = int(mat_h)
                            col = led_idx % int(mat_w)

                    keys.append(
                        KeyCoordinate(
                            name=name,
                            index=led_idx,
                            x=norm_x,
                            y=norm_y,
                            row=row,
                            col=col,
                        )
                    )
                return keys

        # Case 2: Linear zone with named LEDs (or fallback to ANSI key name matching)
        if total_leds > 0:
            keys = []
            for led_idx in range(total_leds):
                raw_led = dev_leds[led_idx] if led_idx < len(dev_leds) else None
                name = getattr(raw_led, "name", f"Key_{led_idx}")
                named_coord = K556LayoutProvider.find_coordinate_by_name(name)

                if named_coord:
                    norm_x = named_coord.x
                    norm_y = named_coord.y
                    row = named_coord.row
                    col = named_coord.col
                else:
                    norm_x = led_idx / max(1.0, float(total_leds - 1))
                    norm_y = 0.5
                    row = 0
                    col = led_idx

                keys.append(
                    KeyCoordinate(
                        name=name,
                        index=led_idx,
                        x=norm_x,
                        y=norm_y,
                        row=row,
                        col=col,
                    )
                )
            return keys

        return []
