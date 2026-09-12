#pragma once

#include "openrgb_flowers/core/models/color_rgb.hpp"
#include <cstddef>
#include <vector>

namespace openrgb_flowers::math {

/**
 * @brief High-performance mathematical utilities for color processing and transformations.
 */
class FastColorMath {
public:
    static void hsv_to_rgb(float h, float s, float v, float& r, float& g, float& b);

    static core::models::ColorRGB apply_brightness_gamma(
        const core::models::ColorRGB& in,
        float brightness,
        float gamma = 1.0f,
        float saturation = 1.0f
    );

    static void apply_brightness_gamma_buffer(
        const core::models::ColorRGB* src,
        core::models::ColorRGB* dst,
        size_t count,
        float brightness,
        float gamma = 1.0f,
        float saturation = 1.0f
    );

    static core::models::ColorRGB lerp(const core::models::ColorRGB& c1, const core::models::ColorRGB& c2, float t);
};

} // namespace openrgb_flowers::math
