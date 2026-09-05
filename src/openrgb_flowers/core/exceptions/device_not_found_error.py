"""Exception raised when a requested RGB keyboard or controller cannot be found."""
from __future__ import annotations
from openrgb_flowers.core.exceptions.base_exception import OpenRGBFlowersError


class DeviceNotFoundError(OpenRGBFlowersError):
    """Raised when the specified device or any keyboard cannot be found."""
    pass
