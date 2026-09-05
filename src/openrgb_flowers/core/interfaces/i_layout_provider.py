"""Interface for keyboard physical layout providers."""
from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np
from openrgb_flowers.core.models.key_coordinate import KeyCoordinate


class ILayoutProvider(ABC):
    """Contract for mapping keyboard keys to physical 2D coordinates."""

    @abstractmethod
    def get_device_name(self) -> str:
        """Returns the device model name (e.g., 'Redragon K556RGB-M')."""
        pass

    @abstractmethod
    def get_key_count(self) -> int:
        """Returns the total number of addressable LEDs/keys."""
        pass

    @abstractmethod
    def get_coordinates(self) -> List[KeyCoordinate]:
        """Returns list of all key coordinate objects."""
        pass

    @abstractmethod
    def get_coordinate_arrays(self) -> Tuple[np.ndarray, np.ndarray]:
        """Returns (x_array, y_array) of normalized coordinates of shape (N,)."""
        pass
