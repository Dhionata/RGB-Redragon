#pragma once

#include "openrgb_flowers/core/interfaces/i_color_palette.hpp"
#include "openrgb_flowers/math/spatial_grid.hpp"
#include <memory>
#include <utility>
#include <vector>

namespace openrgb_flowers::effects {

/**
 * @brief Encapsulates the lifecycle, petal geometry, and color propagation of a single blooming flower.
 */
class FlowerInstance {
public:
    FlowerInstance(
        float center_x,
        float center_y,
        std::shared_ptr<core::interfaces::IColorPalette> palette,
        int petal_count = 5,
        float max_radius = 0.45f,
        float lifespan = 3.2f,
        float rotation = 0.0f,
        float petal_depth = 0.22f,
        math::SpatialGrid grid = math::SpatialGrid()
    );

    bool update(float dt);
    [[nodiscard]] bool is_alive() const;

    [[nodiscard]] std::pair<float, float> get_center() const;
    [[nodiscard]] float get_lifecycle_phase() const;
    [[nodiscard]] float get_current_radius() const;
    [[nodiscard]] float get_intensity_envelope() const;

    void evaluate(
        const float* x_coords,
        const float* y_coords,
        float* out_intensities,
        core::models::ColorRGB* out_colors,
        size_t count
    ) const;

private:
    float center_x_{0.5f};
    float center_y_{0.5f};
    std::shared_ptr<core::interfaces::IColorPalette> palette_;
    int petal_count_{5};
    float max_radius_{0.45f};
    float lifespan_{3.2f};
    float age_{0.0f};
    float rotation_{0.0f};
    float petal_depth_{0.22f};
    math::SpatialGrid grid_;
};

} // namespace openrgb_flowers::effects
