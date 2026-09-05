"""Harmonic petal geometry and polar boundary calculations."""
from __future__ import annotations
import numpy as np
from openrgb_flowers.math.easing import EasingFunctions


class PetalGeometry:
    """Calculates polar petal boundaries and radial intensity falloffs."""

    @staticmethod
    def compute_petal_radii(
        angles: np.ndarray,
        base_radius: float,
        petal_count: int,
        petal_depth: float,
        rotation: float,
    ) -> np.ndarray:
        """Calculates boundary radius for each angle based on harmonic lobes.

        R(theta) = base_radius * (1.0 + petal_depth * cos(lobes * theta + rotation))
        """
        harmonic = EasingFunctions.petal_harmonic(angles, petal_count, petal_depth, rotation)
        return np.maximum(0.001, base_radius * harmonic)

    @staticmethod
    def compute_falloff(
        distances: np.ndarray,
        boundary_radii: np.ndarray,
        edge_softness: float = 0.25,
    ) -> np.ndarray:
        """Calculates smoothstep edge falloff: 1.0 inside flower, transitioning to 0.0 outside."""
        rel_dist = distances / boundary_radii
        # Smooth falloff near the petal boundary
        inner_edge = max(0.0, 1.0 - edge_softness)
        outer_edge = 1.0 + edge_softness * 0.5
        falloff = 1.0 - EasingFunctions.smoothstep(inner_edge, outer_edge, rel_dist)
        return falloff
