#pragma once

#include "openrgb_flowers/core/models/color_rgb.hpp"
#include <string>
#include <vector>

namespace openrgb_flowers::core::interfaces {

/**
 * @brief Interface contract for floral color palettes.
 */
class IColorPalette {
public:
    virtual ~IColorPalette() = default;

    [[nodiscard]] virtual std::string get_name() const = 0;
    [[nodiscard]] virtual models::ColorRGB sample(float t) const = 0;
    virtual void sample_vector(const float* t_array, models::ColorRGB* out_colors, size_t count) const = 0;

    [[nodiscard]] virtual models::ColorRGB get_center_color() const = 0;
    [[nodiscard]] virtual models::ColorRGB get_petal_color() const = 0;
    [[nodiscard]] virtual models::ColorRGB get_tip_color() const = 0;
};

} // namespace openrgb_flowers::core::interfaces
