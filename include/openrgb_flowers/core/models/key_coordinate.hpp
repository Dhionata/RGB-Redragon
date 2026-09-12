#pragma once

#include <string>

namespace openrgb_flowers::core::models {

/**
 * @brief Represents a physical LED key coordinate on the keyboard surface.
 */
class KeyCoordinate {
public:
    std::string name;
    int index{0};
    float x{0.0f};
    float y{0.0f};
    int row{0};
    int col{0};

    KeyCoordinate() = default;
    KeyCoordinate(std::string key_name, int idx, float posX, float posY, int r, int c);
};

} // namespace openrgb_flowers::core::models
