"""Connection exception raised when OpenRGB communication fails."""
from __future__ import annotations
from openrgb_flowers.core.exceptions.base_exception import OpenRGBFlowersError


class OpenRGBConnectionError(OpenRGBFlowersError):
    """Raised when connection to OpenRGB server fails or drops."""
    pass
