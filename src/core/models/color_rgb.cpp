#include "openrgb_flowers/core/models/color_rgb.hpp"

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <stdexcept>

namespace openrgb_flowers::core::models {

ColorRGB ColorRGB::from_normalized(float norm_r, float norm_g, float norm_b) {
    auto clamp_val = [](float v) -> uint8_t {
        float c = std::clamp(v, 0.0f, 1.0f);
        return static_cast<uint8_t>(std::round(c * 255.0f));
    };
    return ColorRGB(clamp_val(norm_r), clamp_val(norm_g), clamp_val(norm_b));
}

ColorRGB ColorRGB::from_hex(const std::string& hex_str) {
    std::string clean = hex_str;
    if (!clean.empty() && clean[0] == '#') {
        clean = clean.substr(1);
    }
    if (clean.length() != 6) {
        throw std::invalid_argument("Invalid hex color string: " + hex_str);
    }

    auto parse_byte = [](const std::string& sub) -> uint8_t {
        unsigned int val = 0;
        std::stringstream ss;
        ss << std::hex << sub;
        ss >> val;
        return static_cast<uint8_t>(val);
    };

    uint8_t r = parse_byte(clean.substr(0, 2));
    uint8_t g = parse_byte(clean.substr(2, 2));
    uint8_t b = parse_byte(clean.substr(4, 2));
    return ColorRGB(r, g, b);
}

std::tuple<uint8_t, uint8_t, uint8_t> ColorRGB::to_tuple() const {
    return {r, g, b};
}

std::tuple<float, float, float> ColorRGB::to_normalized() const {
    return {r / 255.0f, g / 255.0f, b / 255.0f};
}

std::string ColorRGB::to_hex() const {
    std::stringstream ss;
    ss << '#' << std::uppercase << std::hex << std::setfill('0')
       << std::setw(2) << static_cast<int>(r)
       << std::setw(2) << static_cast<int>(g)
       << std::setw(2) << static_cast<int>(b);
    return ss.str();
}

} // namespace openrgb_flowers::core::models
