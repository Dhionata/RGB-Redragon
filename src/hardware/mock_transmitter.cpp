#include "openrgb_flowers/hardware/mock_transmitter.hpp"

namespace openrgb_flowers::hardware {

bool MockTransmitter::connect() {
    connected_ = true;
    return true;
}

void MockTransmitter::disconnect() {
    connected_ = false;
}

bool MockTransmitter::is_connected() const {
    return connected_;
}

bool MockTransmitter::send_frame(const core::models::RenderFrame& frame) {
    if (!connected_) return false;
    ++transmitted_frames_;
    last_frame_ = frame;
    return true;
}

uint64_t MockTransmitter::get_transmitted_frames() const {
    return transmitted_frames_;
}

const core::models::RenderFrame& MockTransmitter::get_last_frame() const {
    return last_frame_;
}

} // namespace openrgb_flowers::hardware
