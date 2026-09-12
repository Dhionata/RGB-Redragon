#pragma once

#include "openrgb_flowers/core/interfaces/i_frame_transmitter.hpp"
#include <memory>
#include <string>

namespace openrgb_flowers::hardware {

/**
 * @brief Factory resolving and creating appropriate hardware frame transmitter.
 */
class TransmitterFactory {
public:
    static std::shared_ptr<core::interfaces::IFrameTransmitter> create_transmitter(
        const std::string& driver_name,
        const std::string& host = "127.0.0.1",
        int port = 6742,
        const std::string& device_name = "",
        int device_index = -1
    );
};

} // namespace openrgb_flowers::hardware
