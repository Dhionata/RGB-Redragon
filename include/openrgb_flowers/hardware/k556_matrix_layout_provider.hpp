#pragma once

#include "openrgb_flowers/core/interfaces/i_layout_provider.hpp"
#include <vector>

namespace openrgb_flowers::hardware {

/**
 * @brief Full 6x22 hardware matrix layout provider for the Redragon K556RGB-M keyboard (132 positions).
 */
class K556MatrixLayoutProvider : public core::interfaces::ILayoutProvider {
public:
    static constexpr int ROWS = 6;
    static constexpr int COLS = 22;
    static constexpr size_t TOTAL_KEYS = ROWS * COLS; // 132

    K556MatrixLayoutProvider();

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
