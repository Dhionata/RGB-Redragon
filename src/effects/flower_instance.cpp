#include "openrgb_flowers/effects/flower_instance.hpp"
#include "openrgb_flowers/effects/petal_geometry.hpp"
#include "openrgb_flowers/math/easing.hpp"

#include <algorithm>
#include <cmath>

namespace openrgb_flowers::effects {

FlowerInstance::FlowerInstance(
    float center_x,
    float center_y,
    std::shared_ptr<core::interfaces::IColorPalette> palette,
    int petal_count,
    float max_radius,
    float lifespan,
    float rotation,
    float petal_depth,
    math::SpatialGrid grid
) : center_x_(center_x),
    center_y_(center_y),
    palette_(std::move(palette)),
    petal_count_(petal_count),
    max_radius_(max_radius),
    lifespan_(std::max(0.5f, lifespan)),
    age_(0.0f),
    rotation_(rotation),
    petal_depth_(petal_depth),
    grid_(grid) {}

bool FlowerInstance::update(float dt) {
    age_ += dt;
    return is_alive();
}

bool FlowerInstance::is_alive() const {
    return age_ < lifespan_;
}

std::pair<float, float> FlowerInstance::get_center() const {
    return {center_x_, center_y_};
}

float FlowerInstance::get_lifecycle_phase() const {
    return std::min(1.0f, age_ / lifespan_);
}

float FlowerInstance::get_current_radius() const {
    float progress = get_lifecycle_phase();
    float growth_t = std::min(1.0f, progress / 0.65f);
    float expansion = math::EasingFunctions::ease_out_cubic(growth_t);
    return max_radius_ * expansion;
}

float FlowerInstance::get_intensity_envelope() const {
    float p = get_lifecycle_phase();
    if (p < 0.2f) {
        return math::EasingFunctions::ease_in_out_cubic(p / 0.2f);
    } else if (p < 0.65f) {
        return 1.0f;
    } else {
        float fade_t = (p - 0.65f) / 0.35f;
        return 1.0f - math::EasingFunctions::ease_in_out_cubic(fade_t);
    }
}

void FlowerInstance::evaluate(
    const float* x_coords,
    const float* y_coords,
    float* out_intensities,
    core::models::ColorRGB* out_colors,
    size_t count
) const {
    float current_radius = get_current_radius();
    float envelope = get_intensity_envelope();

    if (current_radius < 0.01f || envelope < 0.01f) {
        for (size_t i = 0; i < count; ++i) {
            out_intensities[i] = 0.0f;
            out_colors[i] = core::models::ColorRGB(0, 0, 0);
        }
        return;
    }

    for (size_t i = 0; i < count; ++i) {
        auto [dx, dy, dist, angle] = grid_.correct_aspect_ratio_single(
            x_coords[i], y_coords[i], center_x_, center_y_
        );

        float boundary_radius = PetalGeometry::compute_petal_radius(
            angle, current_radius, petal_count_, petal_depth_, rotation_
        );

        float falloff = PetalGeometry::compute_falloff(dist, boundary_radius, 0.3f);
        float intensity = falloff * envelope;
        out_intensities[i] = intensity;

        float grad_pos = std::clamp(dist / (boundary_radius + 1e-6f), 0.0f, 1.0f);
        out_colors[i] = palette_->sample(grad_pos);
    }
}

} // namespace openrgb_flowers::effects
