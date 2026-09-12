#pragma once

#include "openrgb_flowers/core/interfaces/i_color_palette.hpp"

namespace openrgb_flowers::effects::palettes {

/**
 * @brief Dynamic chromatic rainbow bloom cycling seamlessly across the floral spectrum.
 */
class RainbowPalette : public core::interfaces::IColorPalette {
public:
    explicit RainbowPalette(float base_hue = 0.0f);

    [[nodiscard]] std::string get_name() const override;
    [[nodiscard]] core::models::ColorRGB sample(float t) const override;
    void sample_vector(const float* t_array, core::models::ColorRGB* out_colors, size_t count) const override;

    [[nodiscard]] core::models::ColorRGB get_center_color() const override;
    [[nodiscard]] core::models::ColorRGB get_petal_color() const override;
    [[nodiscard]] core::models::ColorRGB get_tip_color() const override;

    [[nodiscard]] float get_base_hue() const;
    void set_base_hue(float hue);

private:
    float base_hue_{0.0f};
};

} // namespace openrgb_flowers::effects::palettes
