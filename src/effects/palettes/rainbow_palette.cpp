#include "openrgb_flowers/effects/palettes/rainbow_palette.hpp"
#include "openrgb_flowers/math/fast_color.hpp"

#include <cmath>

namespace openrgb_flowers::effects::palettes {

RainbowPalette::RainbowPalette(float base_hue) {
    set_base_hue(base_hue);
}

std::string RainbowPalette::get_name() const {
    return "rainbow";
}

core::models::ColorRGB RainbowPalette::sample(float t) const {
    float hue = std::fmod(base_hue_ + t * 360.0f, 360.0f);
    if (hue < 0.0f) hue += 360.0f;
    float r = 0.0f, g = 0.0f, b = 0.0f;
    math::FastColorMath::hsv_to_rgb(hue, 1.0f, 1.0f, r, g, b);
    return core::models::ColorRGB(
        static_cast<uint8_t>(r),
        static_cast<uint8_t>(g),
        static_cast<uint8_t>(b)
    );
}

void RainbowPalette::sample_vector(const float* t_array, core::models::ColorRGB* out_colors, size_t count) const {
    for (size_t i = 0; i < count; ++i) {
        out_colors[i] = sample(t_array[i]);
    }
}

core::models::ColorRGB RainbowPalette::get_center_color() const {
    return sample(0.0f);
}

core::models::ColorRGB RainbowPalette::get_petal_color() const {
    return sample(0.5f);
}

core::models::ColorRGB RainbowPalette::get_tip_color() const {
    return sample(1.0f);
}

float RainbowPalette::get_base_hue() const {
    return base_hue_;
}

void RainbowPalette::set_base_hue(float hue) {
    base_hue_ = std::fmod(hue, 360.0f);
    if (base_hue_ < 0.0f) base_hue_ += 360.0f;
}

} // namespace openrgb_flowers::effects::palettes
