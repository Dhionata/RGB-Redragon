#include "openrgb_flowers/effects/petal_geometry.hpp"
#include "openrgb_flowers/math/easing.hpp"

#include <algorithm>

namespace openrgb_flowers::effects {

float PetalGeometry::compute_petal_radius(
    float angle,
    float base_radius,
    int petal_count,
    float petal_depth,
    float rotation
) {
    float harmonic = math::EasingFunctions::petal_harmonic(angle, petal_count, petal_depth, rotation);
    return std::max(0.001f, base_radius * harmonic);
}

float PetalGeometry::compute_falloff(
    float distance,
    float boundary_radius,
    float edge_softness
) {
    float boundary = std::max(1e-5f, boundary_radius);
    float rel_dist = distance / boundary;
    float inner_edge = std::max(0.0f, 1.0f - edge_softness);
    float outer_edge = 1.0f + edge_softness * 0.5f;
    return 1.0f - math::EasingFunctions::smoothstep(inner_edge, outer_edge, rel_dist);
}

void PetalGeometry::compute_petal_radii_batch(
    const float* angles,
    float* out_radii,
    size_t count,
    float base_radius,
    int petal_count,
    float petal_depth,
    float rotation
) {
    for (size_t i = 0; i < count; ++i) {
        out_radii[i] = compute_petal_radius(angles[i], base_radius, petal_count, petal_depth, rotation);
    }
}

void PetalGeometry::compute_falloff_batch(
    const float* distances,
    const float* boundary_radii,
    float* out_falloffs,
    size_t count,
    float edge_softness
) {
    for (size_t i = 0; i < count; ++i) {
        out_falloffs[i] = compute_falloff(distances[i], boundary_radii[i], edge_softness);
    }
}

} // namespace openrgb_flowers::effects
