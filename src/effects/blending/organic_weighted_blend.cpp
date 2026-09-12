#include "openrgb_flowers/effects/blending/organic_weighted_blend.hpp"

#include <algorithm>
#include <cmath>
#include <vector>

namespace openrgb_flowers::effects::blending {

std::string OrganicWeightedBlend::get_name() const {
    return "weighted";
}

void OrganicWeightedBlend::blend_layers(
    const core::models::ColorRGB* base_colors,
    const std::vector<std::vector<core::models::ColorRGB>>& layer_colors,
    const std::vector<std::vector<float>>& layer_intensities,
    core::models::ColorRGB* out_colors,
    size_t led_count
) const {
    if (layer_colors.empty()) {
        for (size_t i = 0; i < led_count; ++i) {
            out_colors[i] = base_colors[i];
        }
        return;
    }

    accum_r_.assign(led_count, 0.0f);
    accum_g_.assign(led_count, 0.0f);
    accum_b_.assign(led_count, 0.0f);
    total_weight_.assign(led_count, 0.0f);
    max_intensity_.assign(led_count, 0.0f);

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
            total_weight_[i] += w;
            if (w > max_intensity_[i]) {
                max_intensity_[i] = w;
            }
        }
    }

    for (size_t i = 0; i < led_count; ++i) {
        float mix_r = 0.0f, mix_g = 0.0f, mix_b = 0.0f;
        if (total_weight_[i] > 1e-5f) {
            mix_r = accum_r_[i] / total_weight_[i];
            mix_g = accum_g_[i] / total_weight_[i];
            mix_b = accum_b_[i] / total_weight_[i];
        }

        float alpha = std::clamp(max_intensity_[i], 0.0f, 1.0f);
        float inv_alpha = 1.0f - alpha;

        float base_rf = static_cast<float>(base_colors[i].r);
        float base_gf = static_cast<float>(base_colors[i].g);
        float base_bf = static_cast<float>(base_colors[i].b);

        float final_r = base_rf * inv_alpha + mix_r * alpha;
        float final_g = base_gf * inv_alpha + mix_g * alpha;
        float final_b = base_bf * inv_alpha + mix_b * alpha;

        out_colors[i] = core::models::ColorRGB(
            static_cast<uint8_t>(std::clamp(std::round(final_r), 0.0f, 255.0f)),
            static_cast<uint8_t>(std::clamp(std::round(final_g), 0.0f, 255.0f)),
            static_cast<uint8_t>(std::clamp(std::round(final_b), 0.0f, 255.0f))
        );
    }
}

} // namespace openrgb_flowers::effects::blending
