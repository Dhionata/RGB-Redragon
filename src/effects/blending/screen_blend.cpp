#include "openrgb_flowers/effects/blending/screen_blend.hpp"

#include <algorithm>
#include <cmath>
#include <vector>

namespace openrgb_flowers::effects::blending {

std::string ScreenBlend::get_name() const {
    return "screen";
}

void ScreenBlend::blend_layers(
    const core::models::ColorRGB* base_colors,
    const std::vector<std::vector<core::models::ColorRGB>>& layer_colors,
    const std::vector<std::vector<float>>& layer_intensities,
    core::models::ColorRGB* out_colors,
    size_t led_count
) const {
    res_r_.resize(led_count);
    res_g_.resize(led_count);
    res_b_.resize(led_count);

    for (size_t i = 0; i < led_count; ++i) {
        res_r_[i] = base_colors[i].r / 255.0f;
        res_g_[i] = base_colors[i].g / 255.0f;
        res_b_[i] = base_colors[i].b / 255.0f;
    }

    size_t num_layers = layer_colors.size();
    for (size_t l = 0; l < num_layers; ++l) {
        const auto& col_layer = layer_colors[l];
        const auto& int_layer = layer_intensities[l];
        size_t n = std::min({led_count, col_layer.size(), int_layer.size()});

        for (size_t i = 0; i < n; ++i) {
            float inten = int_layer[i];
            float l_r = (col_layer[i].r / 255.0f) * inten;
            float l_g = (col_layer[i].g / 255.0f) * inten;
            float l_b = (col_layer[i].b / 255.0f) * inten;

            res_r_[i] = 1.0f - (1.0f - res_r_[i]) * (1.0f - l_r);
            res_g_[i] = 1.0f - (1.0f - res_g_[i]) * (1.0f - l_g);
            res_b_[i] = 1.0f - (1.0f - res_b_[i]) * (1.0f - l_b);
        }
    }

    for (size_t i = 0; i < led_count; ++i) {
        out_colors[i] = core::models::ColorRGB(
            static_cast<uint8_t>(std::clamp(std::round(res_r_[i] * 255.0f), 0.0f, 255.0f)),
            static_cast<uint8_t>(std::clamp(std::round(res_g_[i] * 255.0f), 0.0f, 255.0f)),
            static_cast<uint8_t>(std::clamp(std::round(res_b_[i] * 255.0f), 0.0f, 255.0f))
        );
    }
}

} // namespace openrgb_flowers::effects::blending
