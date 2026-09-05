"""Custom typed exceptions for OpenRGB Flowers Blooming."""


class OpenRGBFlowersError(Exception):
    """Base exception for all errors in the OpenRGB Flowers Blooming library."""
    pass


class OpenRGBConnectionError(OpenRGBFlowersError):
    """Raised when communication with the OpenRGB SDK server fails or drops."""
    pass


class DeviceNotFoundError(OpenRGBFlowersError):
    """Raised when the requested RGB keyboard/device cannot be found."""
    pass


class InvalidLayoutError(OpenRGBFlowersError):
    """Raised when keyboard physical coordinate layout definition is invalid."""
    pass


class ConfigurationError(OpenRGBFlowersError):
    """Raised when invalid effect configuration parameters are provided."""
    pass
