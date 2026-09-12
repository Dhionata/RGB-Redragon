#include "openrgb_flowers/math/fast_color.hpp"

#include <algorithm>
#include <cmath>

namespace openrgb_flowers::math {

void FastColorMath::hsv_to_rgb(float h, float s, float v, float& r, float& g, float& b) {
    float h_clamped = std::fmod(h, 360.0f);
    if (h_clamped < 0.0f) h_clamped += 360.0f;
    float s_clamped = std::clamp(s, 0.0f, 1.0f);
    float v_clamped = std::clamp(v, 0.0f, 1.0f);

    float c = v_clamped * s_clamped;
    float h_prime = h_clamped / 60.0f;
    float x = c * (1.0f - std::fabs(std::fmod(h_prime, 2.0f) - 1.0f));
    float m = v_clamped - c;

    float r1 = 0.0f, g1 = 0.0f, b1 = 0.0f;
    if (h_prime < 1.0f) {
        r1 = c; g1 = x; b1 = 0.0f;
    } else if (h_prime < 2.0f) {
        r1 = x; g1 = c; b1 = 0.0f;
    } else if (h_prime < 3.0f) {
        r1 = 0.0f; g1 = c; b1 = x;
    } else if (h_prime < 4.0f) {
        r1 = 0.0f; g1 = x; b1 = c;
    } else if (h_prime < 5.0f) {
        r1 = x; g1 = 0.0f; b1 = c;
    } else {
        r1 = c; g1 = 0.0f; b1 = x;
    }

    r = (r1 + m) * 255.0f;
    g = (g1 + m) * 255.0f;
    b = (b1 + m) * 255.0f;
}

core::models::ColorRGB FastColorMath::apply_brightness_gamma(
    const core::models::ColorRGB& in,
    float brightness,
    float gamma,
    float saturation
) {
    float rf = static_cast<float>(in.r);
    float gf = static_cast<float>(in.g);
    float bf = static_cast<float>(in.b);

    // Saturation adjustment via luminance projection
    if (std::fabs(saturation - 1.0f) > 0.01f) {
        float luma = rf * 0.299f + gf * 0.587f + bf * 0.114f;
        rf = luma + (rf - luma) * saturation;
        gf = luma + (gf - luma) * saturation;
        bf = luma + (bf - luma) * saturation;
    }

    // Brightness scaling
    float b = std::clamp(brightness, 0.0f, 1.0f) / 255.0f;
    rf = std::clamp(rf * b, 0.0f, 1.0f);
    gf = std::clamp(gf * b, 0.0f, 1.0f);
    bf = std::clamp(bf * b, 0.0f, 1.0f);

    // Gamma correction
    if (std::fabs(gamma - 1.0f) > 0.01f) {
        rf = std::pow(rf, gamma);
        gf = std::pow(gf, gamma);
        bf = std::pow(bf, gamma);
    }

    auto to_u8 = [](float val) -> uint8_t {
        return static_cast<uint8_t>(std::clamp(std::round(val * 255.0f), 0.0f, 255.0f));
    };

    return core::models::ColorRGB(to_u8(rf), to_u8(gf), to_u8(bf));
}

void FastColorMath::apply_brightness_gamma_buffer(
    const core::models::ColorRGB* src,
    core::models::ColorRGB* dst,
    size_t count,
    float brightness,
    float gamma,
    float saturation
) {
    for (size_t i = 0; i < count; ++i) {
        dst[i] = apply_brightness_gamma(src[i], brightness, gamma, saturation);
    }
}

core::models::ColorRGB FastColorMath::lerp(
    const core::models::ColorRGB& c1,
    const core::models::ColorRGB& c2,
    float t
) {
    float factor = std::clamp(t, 0.0f, 1.0f);
    float inv = 1.0f - factor;
    auto r = static_cast<uint8_t>(std::round(c1.r * inv + c2.r * factor));
    auto g = static_cast<uint8_t>(std::round(c1.g * inv + c2.g * factor));
    auto b = static_cast<uint8_t>(std::round(c1.b * inv + c2.b * factor));
    return core::models::ColorRGB(r, g, b);
}

} // namespace openrgb_flowers::math
