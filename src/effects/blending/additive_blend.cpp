#include "openrgb_flowers/effects/blending/additive_blend.hpp"

#include <algorithm>
#include <cmath>
#include <vector>

namespace openrgb_flowers::effects::blending {

std::string AdditiveBlend::get_name() const {
    return "additive";
}

void AdditiveBlend::blend_layers(
    const core::models::ColorRGB* base_colors,
    const std::vector<std::vector<core::models::ColorRGB>>& layer_colors,
    const std::vector<std::vector<float>>& layer_intensities,
    core::models::ColorRGB* out_colors,
    size_t led_count
) const {
    accum_r_.resize(led_count);
    accum_g_.resize(led_count);
    accum_b_.resize(led_count);

    for (size_t i = 0; i < led_count; ++i) {
        accum_r_[i] = static_cast<float>(base_colors[i].r);
        accum_g_[i] = static_cast<float>(base_colors[i].g);
        accum_b_[i] = static_cast<float>(base_colors[i].b);
    }

    size_t num_layers = layer_colors.size();
    for (size_t l = 0; l < num_layers; ++l) {
        const auto& col_layer = layer_colors[l];
        const auto& int_layer = layer_intensities[l];
        size_t n = std::min({led_count, col_layer.size(), int_layer.size()});

        for (size_t i = 0; i < n; ++i) {
            float w = int_layer[i];
            accum_r_[i] += col_layer[i].r * w;
            accum_g_[i] += col_layer[i].g * w;
            accum_b_[i] += col_layer[i].b * w;
        }
    }

    for (size_t i = 0; i < led_count; ++i) {
        out_colors[i] = core::models::ColorRGB(
            static_cast<uint8_t>(std::clamp(std::round(accum_r_[i]), 0.0f, 255.0f)),
            static_cast<uint8_t>(std::clamp(std::round(accum_g_[i]), 0.0f, 255.0f)),
            static_cast<uint8_t>(std::clamp(std::round(accum_b_[i]), 0.0f, 255.0f))
        );
    }
}

} // namespace openrgb_flowers::effects::blending
