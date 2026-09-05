"""Interface for floral color palettes."""
from abc import ABC, abstractmethod
import numpy as np
from openrgb_flowers.core.models.color_rgb import ColorRGB


class IColorPalette(ABC):
    """Defines contract for floral color palettes."""

    @abstractmethod
    def get_name(self) -> str:
        """Returns the unique name of the palette."""
        pass

    @abstractmethod
    def sample(self, t: float) -> ColorRGB:
        """Samples the palette color at position t in [0.0, 1.0]."""
        pass

    @abstractmethod
    def sample_vectorized(self, t_array: np.ndarray) -> np.ndarray:
        """Vectorized color sampling returning shape (N, 3) float array in [0, 255]."""
        pass

    @abstractmethod
    def get_center_color(self) -> ColorRGB:
        """Returns the floral center (stamen) color."""
        pass

    @abstractmethod
    def get_petal_color(self) -> ColorRGB:
        """Returns the primary petal color."""
        pass

    @abstractmethod
    def get_tip_color(self) -> ColorRGB:
        """Returns the petal edge/tip accent color."""
        pass
