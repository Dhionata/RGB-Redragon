"""Interface for layer blending algorithms."""
from abc import ABC, abstractmethod
import numpy as np


class IBlendStrategy(ABC):
    """Contract for color blending strategies across multiple floral layers."""

    @abstractmethod
    def get_name(self) -> str:
        """Returns the name of the blend mode."""
        pass

    @abstractmethod
    def blend_layers(
        self,
        base_colors: np.ndarray,
        layer_colors: list[np.ndarray],
        layer_intensities: list[np.ndarray],
    ) -> np.ndarray:
        """Blends multiple layers onto a base color array.

        Args:
            base_colors: shape (N, 3) background colors in [0, 255].
            layer_colors: list of (N, 3) layer color arrays in [0, 255].
            layer_intensities: list of (N,) layer intensity weights in [0.0, 1.0].

        Returns:
            Blended color array of shape (N, 3) uint8 in [0, 255].
        """
        pass
