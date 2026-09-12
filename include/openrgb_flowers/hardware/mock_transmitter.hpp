#pragma once

#include "openrgb_flowers/core/interfaces/i_frame_transmitter.hpp"
#include <cstdint>

namespace openrgb_flowers::hardware {

/**
 * @brief In-memory mock frame transmitter for simulations and unit tests.
 */
class MockTransmitter : public core::interfaces::IFrameTransmitter {
public:
    MockTransmitter() = default;

    bool connect() override;
    void disconnect() override;
    [[nodiscard]] bool is_connected() const override;
    bool send_frame(const core::models::RenderFrame& frame) override;

    [[nodiscard]] uint64_t get_transmitted_frames() const;
    [[nodiscard]] const core::models::RenderFrame& get_last_frame() const;

private:
    bool connected_{false};
    uint64_t transmitted_frames_{0};
    core::models::RenderFrame last_frame_;
};

} // namespace openrgb_flowers::hardware
