#pragma once

#include <cstddef>

namespace openrgb_flowers::effects {

/**
 * @brief Harmonic petal geometry and polar boundary calculations.
 */
class PetalGeometry {
public:
    static float compute_petal_radius(
        float angle,
        float base_radius,
        int petal_count,
        float petal_depth,
        float rotation
    );

    static float compute_falloff(
        float distance,
        float boundary_radius,
        float edge_softness = 0.25f
    );

    static void compute_petal_radii_batch(
        const float* angles,
        float* out_radii,
        size_t count,
        float base_radius,
        int petal_count,
        float petal_depth,
        float rotation
    );

    static void compute_falloff_batch(
        const float* distances,
        const float* boundary_radii,
        float* out_falloffs,
        size_t count,
        float edge_softness = 0.25f
    );
};

} // namespace openrgb_flowers::effects
