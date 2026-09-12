#pragma once

#include "openrgb_flowers/core/models/color_rgb.hpp"
#include <string>
#include <vector>

namespace openrgb_flowers::core::interfaces {

/**
 * @brief Interface contract for color blending strategies across multiple floral layers.
 */
class IBlendStrategy {
public:
    virtual ~IBlendStrategy() = default;

    [[nodiscard]] virtual std::string get_name() const = 0;

    virtual void blend_layers(
        const models::ColorRGB* base_colors,
        const std::vector<std::vector<models::ColorRGB>>& layer_colors,
        const std::vector<std::vector<float>>& layer_intensities,
        models::ColorRGB* out_colors,
        size_t led_count
    ) const = 0;
};

} // namespace openrgb_flowers::core::interfaces
