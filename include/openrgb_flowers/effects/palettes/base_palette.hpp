#pragma once

#include "openrgb_flowers/core/interfaces/i_color_palette.hpp"
#include <string>
#include <utility>
#include <vector>

namespace openrgb_flowers::effects::palettes {

/**
 * @brief Multi-stop floral gradient palette with fast linear interpolation.
 */
class BaseColorPalette : public core::interfaces::IColorPalette {
public:
    BaseColorPalette(std::string name, std::vector<std::pair<float, core::models::ColorRGB>> stops);

    [[nodiscard]] std::string get_name() const override;
    [[nodiscard]] core::models::ColorRGB sample(float t) const override;
    void sample_vector(const float* t_array, core::models::ColorRGB* out_colors, size_t count) const override;

    [[nodiscard]] core::models::ColorRGB get_center_color() const override;
    [[nodiscard]] core::models::ColorRGB get_petal_color() const override;
    [[nodiscard]] core::models::ColorRGB get_tip_color() const override;

protected:
    std::string name_;
    std::vector<std::pair<float, core::models::ColorRGB>> stops_;
};

} // namespace openrgb_flowers::effects::palettes
