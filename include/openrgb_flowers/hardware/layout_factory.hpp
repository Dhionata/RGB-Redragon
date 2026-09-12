#pragma once

#include "openrgb_flowers/core/interfaces/i_layout_provider.hpp"
#include "openrgb_flowers/core/interfaces/i_frame_transmitter.hpp"
#include <memory>

namespace openrgb_flowers::hardware {

/**
 * @brief Factory resolving layout provider based on transmitter type.
 */
class LayoutFactory {
public:
    static std::shared_ptr<core::interfaces::ILayoutProvider> create_layout(
        const std::shared_ptr<core::interfaces::IFrameTransmitter>& transmitter
    );
};

} // namespace openrgb_flowers::hardware
