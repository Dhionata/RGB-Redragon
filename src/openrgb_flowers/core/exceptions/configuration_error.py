"""Exception raised when configuration parameters fail boundary validation."""
from __future__ import annotations
from openrgb_flowers.core.exceptions.base_exception import OpenRGBFlowersError


class ConfigurationError(OpenRGBFlowersError):
    """Raised when configuration values are outside valid operational ranges."""
    pass
