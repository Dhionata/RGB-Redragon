"""Exception raised when direct USB HID or hardware communication fails."""
from __future__ import annotations
from openrgb_flowers.core.exceptions.base_exception import OpenRGBFlowersError


class HardwareConnectionError(OpenRGBFlowersError):
    """Raised when connecting or communicating with physical USB HID hardware fails."""
    pass
