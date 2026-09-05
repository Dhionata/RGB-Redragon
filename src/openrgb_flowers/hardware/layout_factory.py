"""Factory for resolving and instantiating keyboard layout providers."""
from __future__ import annotations
from typing import Any, Optional
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider
from openrgb_flowers.hardware.k556_matrix_layout_provider import K556MatrixLayoutProvider
from openrgb_flowers.hardware.openrgb_zone_layout_provider import OpenRGBZoneLayoutProvider


class LayoutFactory:
    """Factory producing the optimal layout provider."""

    @classmethod
    def create_layout(
        cls,
        device: Optional[Any] = None,
        prefer_k556_physical: bool = False,
        use_hardware_matrix: bool = False,
    ) -> ILayoutProvider:
        """Resolves layout provider for given device or hardware model."""
        if use_hardware_matrix:
            return K556MatrixLayoutProvider()

        if device is None:
            return K556LayoutProvider()

        if prefer_k556_physical:
            dev_leds = len(getattr(device, "leds", []))
            if dev_leds == 0 or dev_leds == 104:
                return K556LayoutProvider()
            if dev_leds == 132:
                return K556MatrixLayoutProvider()

        # Dynamic extraction from OpenRGB device (matrix zone or name-matched linear zone)
        provider = OpenRGBZoneLayoutProvider(device)
        if provider.get_key_count() > 0:
            return provider

        return K556LayoutProvider()
