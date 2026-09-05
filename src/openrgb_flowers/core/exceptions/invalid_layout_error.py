"""Exception raised when physical keyboard layout parsing or mapping fails."""
from __future__ import annotations
from openrgb_flowers.core.exceptions.base_exception import OpenRGBFlowersError


class InvalidLayoutError(OpenRGBFlowersError):
    """Raised when keyboard physical layout definition or matrix mapping is invalid."""
    pass
