#pragma once

#include "openrgb_flowers/core/models/color_rgb.hpp"
#include <cstdint>
#include <vector>

namespace openrgb_flowers::core::models {

/**
 * @brief Encapsulates a rendered frame with contiguous ColorRGB buffer.
 */
class RenderFrame {
public:
    double timestamp{0.0};
    uint64_t frame_index{0};
    std::vector<ColorRGB> colors;
    int led_count{0};

    RenderFrame() = default;
    RenderFrame(double ts, uint64_t idx, std::vector<ColorRGB> cols);

    [[nodiscard]] const ColorRGB* data() const;
    [[nodiscard]] const uint8_t* raw_bytes() const;
    [[nodiscard]] size_t raw_size() const;
};

} // namespace openrgb_flowers::core::models
