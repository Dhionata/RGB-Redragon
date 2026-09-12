#include "openrgb_flowers/math/spatial_grid.hpp"

#include <algorithm>
#include <cmath>

namespace openrgb_flowers::math {

SpatialGrid::SpatialGrid(float aspect_ratio)
    : aspect_ratio_(std::max(0.5f, aspect_ratio)) {}

float SpatialGrid::aspect_ratio() const {
    return aspect_ratio_;
}

std::tuple<float, float, float, float> SpatialGrid::correct_aspect_ratio_single(
    float x, float y, float center_x, float center_y
) const {
    float dx = (x - center_x) * aspect_ratio_;
    float dy = y - center_y;
    float dist = std::hypot(dx, dy);
    float angle = std::atan2(dy, dx);
    return {dx, dy, dist, angle};
}

void SpatialGrid::correct_aspect_ratio_batch(
    const float* x_coords,
    const float* y_coords,
    float center_x,
    float center_y,
    float* out_dx,
    float* out_dy,
    float* out_distances,
    float* out_angles,
    size_t count
) const {
    for (size_t i = 0; i < count; ++i) {
        float dx = (x_coords[i] - center_x) * aspect_ratio_;
        float dy = y_coords[i] - center_y;
        if (out_dx) out_dx[i] = dx;
        if (out_dy) out_dy[i] = dy;
        if (out_distances) out_distances[i] = std::hypot(dx, dy);
        if (out_angles) out_angles[i] = std::atan2(dy, dx);
    }
}

} // namespace openrgb_flowers::math
