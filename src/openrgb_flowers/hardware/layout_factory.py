"""Factory for resolving and instantiating keyboard layout providers."""
from __future__ import annotations
from typing import Any, Optional
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider
from openrgb_flowers.hardware.openrgb_zone_layout_provider import OpenRGBZoneLayoutProvider


class LayoutFactory:
    """Factory producing the optimal layout provider."""

    @classmethod
    def create_layout(
        cls,
        device: Optional[Any] = None,
        prefer_k556_physical: bool = True,
    ) -> ILayoutProvider:
        """Resolves layout provider for given device or hardware model."""
        if prefer_k556_physical or device is None:
            return K556LayoutProvider()

        # Try dynamic extraction from OpenRGB device zone
        provider = OpenRGBZoneLayoutProvider(device)
        if provider.get_key_count() > 0:
            return provider

        return K556LayoutProvider()
