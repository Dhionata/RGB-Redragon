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
    coordinates from the controller matrix. If it is a linear zone, it seamlessly maps
    to the physical K556 full-size mechanical layout.
    """

    def __init__(self, device: Any, zone_index: int = 0) -> None:
        self._device = device
        self._device_name = getattr(device, "name", "OpenRGB Device")
        self._keys: List[KeyCoordinate] = []

        if hasattr(device, "zones") and len(device.zones) > zone_index:
            zone = device.zones[zone_index]
            self._keys = self._extract_from_zone(zone)

        # Fallback to K556 layout if zone extraction yielded no keys
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
    def _extract_from_zone(cls, zone: Any) -> List[KeyCoordinate]:
        keys: List[KeyCoordinate] = []
        matrix_map = getattr(zone, "matrix_map", None)
        mat_w = getattr(zone, "mat_width", None)
        mat_h = getattr(zone, "mat_height", None)

        if matrix_map and mat_w and mat_h and mat_w > 1 and mat_h > 1:
            # Map matrix zone keys
            led_items = []
            for r_idx, row in enumerate(matrix_map):
                for c_idx, led_id in enumerate(row):
                    if led_id is not None:
                        led_items.append((int(led_id), r_idx, c_idx))

            # Sort by LED ID to match device order
            led_items.sort(key=lambda item: item[0])
            for led_id, r_idx, c_idx in led_items:
                norm_x = c_idx / max(1, (mat_w - 1))
                norm_y = r_idx / max(1, (mat_h - 1))
                keys.append(
                    KeyCoordinate(
                        name=f"Key_{led_id}",
                        index=led_id,
                        x=norm_x,
                        y=norm_y,
                        row=r_idx,
                        col=c_idx,
                    )
                )
        return keys
