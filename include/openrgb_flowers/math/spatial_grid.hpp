#pragma once

#include <tuple>
#include <vector>

namespace openrgb_flowers::math {

/**
 * @brief Handles 2D spatial coordinate mapping with physical aspect ratio correction.
 */
class SpatialGrid {
public:
    static constexpr float DEFAULT_ASPECT_RATIO = 3.7f;

    explicit SpatialGrid(float aspect_ratio = DEFAULT_ASPECT_RATIO);

    [[nodiscard]] float aspect_ratio() const;

    [[nodiscard]] std::tuple<float, float, float, float> correct_aspect_ratio_single(
        float x, float y, float center_x, float center_y
    ) const;

    void correct_aspect_ratio_batch(
        const float* x_coords,
        const float* y_coords,
        float center_x,
        float center_y,
        float* out_dx,
        float* out_dy,
        float* out_distances,
        float* out_angles,
        size_t count
    ) const;

private:
    float aspect_ratio_{DEFAULT_ASPECT_RATIO};
};

} // namespace openrgb_flowers::math
