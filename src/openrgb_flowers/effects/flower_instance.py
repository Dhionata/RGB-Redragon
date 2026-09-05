"""Individual blooming flower model with organic lifecycle."""
from __future__ import annotations
from typing import Tuple
import numpy as np
from openrgb_flowers.core.interfaces.i_flower_model import IFlowerModel
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette
from openrgb_flowers.effects.petal_geometry import PetalGeometry
from openrgb_flowers.math.spatial_grid import SpatialGrid
from openrgb_flowers.math.easing import EasingFunctions


class FlowerInstance(IFlowerModel):
    """Encapsulates the lifecycle, petal geometry, and color propagation of a single blooming flower."""

    def __init__(
        self,
        center_x: float,
        center_y: float,
        palette: IColorPalette,
        petal_count: int = 5,
        max_radius: float = 0.45,
        lifespan: float = 3.2,
        rotation: float = 0.0,
        petal_depth: float = 0.22,
        spatial_grid: SpatialGrid | None = None,
    ) -> None:
        self._center_x = float(center_x)
        self._center_y = float(center_y)
        self._palette = palette
        self._petal_count = int(petal_count)
        self._max_radius = float(max_radius)
        self._lifespan = max(0.5, float(lifespan))
        self._age = 0.0
        self._rotation = float(rotation)
        self._petal_depth = float(petal_depth)
        self._spatial_grid = spatial_grid or SpatialGrid()

    @property
    def age(self) -> float:
        return self._age

    @property
    def lifespan(self) -> float:
        return self._lifespan

    def update(self, dt: float) -> bool:
        """Advances flower age by dt seconds. Returns True if alive."""
        self._age += dt
        return self.is_alive()

    def is_alive(self) -> bool:
        return self._age < self._lifespan

    def get_center(self) -> Tuple[float, float]:
        return (self._center_x, self._center_y)

    def get_palette(self) -> IColorPalette:
        return self._palette

    def get_lifecycle_phase(self) -> float:
        """Returns normalized lifecycle progress in [0.0, 1.0]."""
        return min(1.0, self._age / self._lifespan)

    def get_current_radius(self) -> float:
        """Calculates current physical expansion radius based on growth curve."""
        progress = self.get_lifecycle_phase()
        # Fast expansion in opening phase (0.0 -> 0.6), slowing down at full bloom
        growth_t = min(1.0, progress / 0.65)
        expansion = float(EasingFunctions.ease_out_cubic(growth_t))
        return self._max_radius * expansion

    def get_intensity_envelope(self) -> float:
        """Calculates temporal brightness envelope (budding -> peak bloom -> gentle wilt)."""
        p = self.get_lifecycle_phase()
        if p < 0.2:
            # Budding: smooth fade in
            return float(EasingFunctions.ease_in_out_cubic(p / 0.2))
        elif p < 0.65:
            # Peak bloom
            return 1.0
        else:
            # Wilting & dissolving: soft decay
            fade_t = (p - 0.65) / 0.35
            return float(1.0 - EasingFunctions.ease_in_out_cubic(fade_t))

    def evaluate(self, x_coords: np.ndarray, y_coords: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Evaluates intensities and RGB colors across all keyboard key coordinates."""
        current_radius = self.get_current_radius()
        envelope = self.get_intensity_envelope()

        if current_radius < 0.01 or envelope < 0.01:
            n = len(x_coords)
            return np.zeros(n, dtype=np.float32), np.zeros((n, 3), dtype=np.float32)

        # Aspect-ratio corrected distances and angles
        _, _, distances, angles = self._spatial_grid.correct_aspect_ratio(
            x_coords, y_coords, self._center_x, self._center_y
        )

        # Calculate petal boundary radii
        boundary_radii = PetalGeometry.compute_petal_radii(
            angles, current_radius, self._petal_count, self._petal_depth, self._rotation
        )

        # Calculate spatial falloff
        falloff = PetalGeometry.compute_falloff(distances, boundary_radii, edge_softness=0.3)
        intensities = falloff * envelope

        # Sample colors along radial gradient: center (0.0) -> petal body -> tip (1.0)
        grad_pos = np.clip(distances / (boundary_radii + 1e-6), 0.0, 1.0)
        colors = self._palette.sample_vectorized(grad_pos)

        return intensities.astype(np.float32), colors.astype(np.float32)
