#pragma once

#include "openrgb_flowers/core/models/color_rgb.hpp"
#include <tuple>

namespace openrgb_flowers::core::models {

/**
 * @brief Represents a color in HSV space (Hue: 0-360, Saturation: 0-1, Value: 0-1).
 */
class ColorHSV {
public:
    float h{0.0f};
    float s{0.0f};
    float v{0.0f};

    ColorHSV() = default;
    ColorHSV(float hue, float sat, float val);

    [[nodiscard]] ColorRGB to_rgb() const;
    static ColorHSV from_rgb(const ColorRGB& rgb);

    [[nodiscard]] std::tuple<float, float, float> to_tuple() const;
};

} // namespace openrgb_flowers::core::models
