#pragma once

#include "openrgb_flowers/core/models/key_coordinate.hpp"
#include <string>
#include <vector>

namespace openrgb_flowers::core::interfaces {

/**
 * @brief Interface contract for keyboard hardware and 2D spatial layouts.
 */
class ILayoutProvider {
public:
    virtual ~ILayoutProvider() = default;

    [[nodiscard]] virtual std::string get_device_name() const = 0;
    [[nodiscard]] virtual size_t get_key_count() const = 0;
    [[nodiscard]] virtual const std::vector<models::KeyCoordinate>& get_coordinates() const = 0;
    [[nodiscard]] virtual const float* get_x_coords() const = 0;
    [[nodiscard]] virtual const float* get_y_coords() const = 0;
};

} // namespace openrgb_flowers::core::interfaces
