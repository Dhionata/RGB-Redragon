#pragma once

#include "openrgb_flowers/core/models/color_rgb.hpp"
#include <string>
#include <vector>

namespace openrgb_flowers::core::models {

/**
 * @brief Strongly-typed configuration for the Flowers Blooming effect.
 */
class EffectConfig {
public:
    std::string effect_type{"blooming"};
    float fps{30.0f};
    float speed{1.0f};
    int max_flowers{7};
    float spawn_rate{1.4f};
    std::vector<int> petal_options{4, 5, 6, 8};
    std::string palette_name{"sakura"};
    std::string blend_mode{"weighted"};
    ColorRGB background_color{4, 8, 12};
    bool ambient_pulse{true};
    float brightness{1.0f};
    float saturation{1.0f};
    float gamma{1.0f};
    std::string host{"127.0.0.1"};
    int port{6742};
    std::string device_name{""};
    int device_index{-1};

    EffectConfig() = default;

    void validate() const;

    [[nodiscard]] std::string to_json(int indent = 2) const;
    static EffectConfig from_json(const std::string& json_str);
    static EffectConfig load_json_file(const std::string& file_path);
    void save_json_file(const std::string& file_path) const;
};

} // namespace openrgb_flowers::core::models
