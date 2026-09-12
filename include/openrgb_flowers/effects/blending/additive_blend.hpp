#pragma once

#include "openrgb_flowers/core/interfaces/i_blend_strategy.hpp"

namespace openrgb_flowers::effects::blending {

/**
 * @brief Additive blend mode.
 */
class AdditiveBlend : public core::interfaces::IBlendStrategy {
public:
    [[nodiscard]] std::string get_name() const override;

    void blend_layers(
        const core::models::ColorRGB* base_colors,
        const std::vector<std::vector<core::models::ColorRGB>>& layer_colors,
        const std::vector<std::vector<float>>& layer_intensities,
        core::models::ColorRGB* out_colors,
        size_t led_count
    ) const override;

private:
    mutable std::vector<float> accum_r_;
    mutable std::vector<float> accum_g_;
    mutable std::vector<float> accum_b_;
};

} // namespace openrgb_flowers::effects::blending
