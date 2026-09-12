#pragma once

#include "openrgb_flowers/core/interfaces/i_layout_provider.hpp"
#include <vector>

namespace openrgb_flowers::hardware {

/**
 * @brief High-precision physical 2D layout model for the Redragon K556RGB-M mechanical keyboard (104 ANSI keys).
 */
class K556LayoutProvider : public core::interfaces::ILayoutProvider {
public:
    K556LayoutProvider();

    [[nodiscard]] std::string get_device_name() const override;
    [[nodiscard]] size_t get_key_count() const override;
    [[nodiscard]] const std::vector<core::models::KeyCoordinate>& get_coordinates() const override;
    [[nodiscard]] const float* get_x_coords() const override;
    [[nodiscard]] const float* get_y_coords() const override;

private:
    std::vector<core::models::KeyCoordinate> keys_;
    std::vector<float> x_coords_;
    std::vector<float> y_coords_;
};

} // namespace openrgb_flowers::hardware
