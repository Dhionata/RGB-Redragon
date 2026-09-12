#pragma once

#include "openrgb_flowers/core/models/render_frame.hpp"

namespace openrgb_flowers::core::interfaces {

/**
 * @brief Interface contract for hardware frame transmitters.
 */
class IFrameTransmitter {
public:
    virtual ~IFrameTransmitter() = default;

    virtual bool connect() = 0;
    virtual void disconnect() = 0;
    [[nodiscard]] virtual bool is_connected() const = 0;
    virtual bool send_frame(const models::RenderFrame& frame) = 0;
};

} // namespace openrgb_flowers::core::interfaces
