#include "openrgb_flowers/core/models/color_hsv.hpp"

#include <algorithm>
#include <cmath>

namespace openrgb_flowers::core::models {

ColorHSV::ColorHSV(float hue, float sat, float val) {
    h = std::fmod(hue, 360.0f);
    if (h < 0.0f) {
        h += 360.0f;
    }
    s = std::clamp(sat, 0.0f, 1.0f);
    v = std::clamp(val, 0.0f, 1.0f);
}

ColorRGB ColorHSV::to_rgb() const {
    float c = v * s;
    float h_prime = h / 60.0f;
    float x = c * (1.0f - std::fabs(std::fmod(h_prime, 2.0f) - 1.0f));
    float m = v - c;

    float r1 = 0.0f, g1 = 0.0f, b1 = 0.0f;
    if (h_prime >= 0.0f && h_prime < 1.0f) {
        r1 = c; g1 = x; b1 = 0.0f;
    } else if (h_prime >= 1.0f && h_prime < 2.0f) {
        r1 = x; g1 = c; b1 = 0.0f;
    } else if (h_prime >= 2.0f && h_prime < 3.0f) {
        r1 = 0.0f; g1 = c; b1 = x;
    } else if (h_prime >= 3.0f && h_prime < 4.0f) {
        r1 = 0.0f; g1 = x; b1 = c;
    } else if (h_prime >= 4.0f && h_prime < 5.0f) {
        r1 = x; g1 = 0.0f; b1 = c;
    } else {
        r1 = c; g1 = 0.0f; b1 = x;
    }

    return ColorRGB::from_normalized(r1 + m, g1 + m, b1 + m);
}

ColorHSV ColorHSV::from_rgb(const ColorRGB& rgb) {
    auto [r_norm, g_norm, b_norm] = rgb.to_normalized();

    float c_max = std::max({r_norm, g_norm, b_norm});
    float c_min = std::min({r_norm, g_norm, b_norm});
    float delta = c_max - c_min;

    float hue = 0.0f;
    if (delta > 1e-6f) {
        if (c_max == r_norm) {
            hue = 60.0f * std::fmod((g_norm - b_norm) / delta, 6.0f);
        } else if (c_max == g_norm) {
            hue = 60.0f * (((b_norm - r_norm) / delta) + 2.0f);
        } else {
            hue = 60.0f * (((r_norm - g_norm) / delta) + 4.0f);
        }
    }
    if (hue < 0.0f) {
        hue += 360.0f;
    }

    float sat = (c_max > 1e-6f) ? (delta / c_max) : 0.0f;
    float val = c_max;

    return ColorHSV(hue, sat, val);
}

std::tuple<float, float, float> ColorHSV::to_tuple() const {
    return {h, s, v};
}

} // namespace openrgb_flowers::core::models
