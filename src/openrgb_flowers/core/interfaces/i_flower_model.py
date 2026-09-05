"""Interface for single flower entity."""
from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette


class IFlowerModel(ABC):
    """Contract for an individual blooming flower instance."""

    @abstractmethod
    def update(self, dt: float) -> bool:
        """Updates flower simulation age. Returns True if alive, False if completed."""
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        """Checks if flower is still within active lifecycle."""
        pass

    @abstractmethod
    def get_center(self) -> Tuple[float, float]:
        """Returns the (x, y) normalized coordinate center."""
        pass

    @abstractmethod
    def get_palette(self) -> IColorPalette:
        """Returns the palette assigned to this flower."""
        pass

    @abstractmethod
    def evaluate(self, x_coords: np.ndarray, y_coords: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Evaluates flower intensities and RGB colors across coordinates.

        Returns:
            Tuple of:
                - intensities: shape (N,) float array in [0.0, 1.0]
                - colors: shape (N, 3) float array in [0.0, 255.0]
        """
        pass
