"""High-performance vectorized color conversions using NumPy."""
from __future__ import annotations
import numpy as np


class FastColorMath:
    """Vectorized mathematical utilities for high-throughput color processing."""

    @staticmethod
    def hsv_to_rgb_vectorized(h: np.ndarray, s: np.ndarray, v: np.ndarray) -> np.ndarray:
        """Converts vectorized HSV arrays to RGB float array of shape (N, 3) in [0.0, 255.0].

        Args:
            h: Hue array in degrees [0.0, 360.0), shape (N,)
            s: Saturation array in [0.0, 1.0], shape (N,)
            v: Value/Brightness array in [0.0, 1.0], shape (N,)

        Returns:
            np.ndarray of shape (N, 3) with RGB values in [0.0, 255.0]
        """
        h_norm = (h % 360.0) / 60.0
        i = np.floor(h_norm).astype(np.int32) % 6
        f = h_norm - np.floor(h_norm)

        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))

        n = len(h)
        rgb = np.zeros((n, 3), dtype=np.float32)

        # Vectorized sector assignment
        mask0 = (i == 0)
        mask1 = (i == 1)
        mask2 = (i == 2)
        mask3 = (i == 3)
        mask4 = (i == 4)
        mask5 = (i == 5)

        rgb[mask0, 0] = v[mask0]
        rgb[mask0, 1] = t[mask0]
        rgb[mask0, 2] = p[mask0]

        rgb[mask1, 0] = q[mask1]
        rgb[mask1, 1] = v[mask1]
        rgb[mask1, 2] = p[mask1]

        rgb[mask2, 0] = p[mask2]
        rgb[mask2, 1] = v[mask2]
        rgb[mask2, 2] = t[mask2]

        rgb[mask3, 0] = p[mask3]
        rgb[mask3, 1] = q[mask3]
        rgb[mask3, 2] = v[mask3]

        rgb[mask4, 0] = t[mask4]
        rgb[mask4, 1] = p[mask4]
        rgb[mask4, 2] = v[mask4]

        rgb[mask5, 0] = v[mask5]
        rgb[mask5, 1] = p[mask5]
        rgb[mask5, 2] = q[mask5]

        return rgb * 255.0

    @staticmethod
    def lerp_rgb_arrays(c1: np.ndarray, c2: np.ndarray, t: np.ndarray) -> np.ndarray:
        """Linear interpolation between two RGB arrays (N, 3) with weights t (N, 1)."""
        t_col = np.clip(t, 0.0, 1.0)
        if len(t_col.shape) == 1:
            t_col = t_col[:, np.newaxis]
        return c1 * (1.0 - t_col) + c2 * t_col

    @staticmethod
    def apply_brightness_gamma(
        rgb_array: np.ndarray,
        brightness: float,
        gamma: float = 1.0,
        saturation: float = 1.0,
    ) -> np.ndarray:
        """Applies saturation scaling, brightness scaling, and gamma correction returning uint8 array of shape (N, 3)."""
        arr = rgb_array.copy()

        # 1. Saturation adjustment via luminance vector projection
        if abs(saturation - 1.0) > 0.01:
            luma = arr[:, 0] * 0.299 + arr[:, 1] * 0.587 + arr[:, 2] * 0.114
            arr = luma[:, np.newaxis] + (arr - luma[:, np.newaxis]) * float(saturation)

        # 2. Brightness scaling
        b = max(0.0, min(1.0, float(brightness)))
        scaled = np.clip(arr * (b / 255.0), 0.0, 1.0)

        # 3. Gamma correction (optional)
        if abs(gamma - 1.0) > 0.01:
            scaled = np.power(scaled, gamma)

        return (scaled * 255.0).astype(np.uint8)
