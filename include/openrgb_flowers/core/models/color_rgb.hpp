#pragma once

#include <cstdint>
#include <string>
#include <tuple>

namespace openrgb_flowers::core::models {

/**
 * @brief Immutable 24-bit RGB Color Model with conversion and packing.
 */
class ColorRGB {
public:
    uint8_t r{0};
    uint8_t g{0};
    uint8_t b{0};

    constexpr ColorRGB() = default;
    constexpr ColorRGB(uint8_t red, uint8_t green, uint8_t blue)
        : r(red), g(green), b(blue) {}

    static ColorRGB from_normalized(float norm_r, float norm_g, float norm_b);
    static ColorRGB from_hex(const std::string& hex_str);

    [[nodiscard]] std::tuple<uint8_t, uint8_t, uint8_t> to_tuple() const;
    [[nodiscard]] std::tuple<float, float, float> to_normalized() const;
    [[nodiscard]] std::string to_hex() const;

    constexpr bool operator==(const ColorRGB& other) const = default;
};

} // namespace openrgb_flowers::core::models
