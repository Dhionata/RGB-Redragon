"""Domain exceptions for openrgb-flowers."""
from openrgb_flowers.core.exceptions.base_exception import OpenRGBFlowersError
from openrgb_flowers.core.exceptions.connection_error import OpenRGBConnectionError
from openrgb_flowers.core.exceptions.hardware_connection_error import HardwareConnectionError
from openrgb_flowers.core.exceptions.device_not_found_error import DeviceNotFoundError
from openrgb_flowers.core.exceptions.invalid_layout_error import InvalidLayoutError
from openrgb_flowers.core.exceptions.configuration_error import ConfigurationError

__all__ = [
    "OpenRGBFlowersError",
    "OpenRGBConnectionError",
    "HardwareConnectionError",
    "DeviceNotFoundError",
    "InvalidLayoutError",
    "ConfigurationError",
]
