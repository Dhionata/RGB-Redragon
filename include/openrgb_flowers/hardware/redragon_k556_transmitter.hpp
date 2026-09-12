#pragma once

#include "openrgb_flowers/core/interfaces/i_frame_transmitter.hpp"
#include <array>
#include <cstdint>
#include <string>
#include <vector>

namespace openrgb_flowers::hardware {

/**
 * @brief High-performance direct USB HID transmitter for Redragon K556RGB-M (VID: 0x2E3C, PID: 0xC365).
 */
class RedragonK556Transmitter : public core::interfaces::IFrameTransmitter {
public:
    static constexpr uint16_t VID = 0x2E3C;
    static constexpr uint16_t PID = 0xC365;
    static constexpr int TARGET_INTERFACE = 2;

    static constexpr size_t CHUNK_SIZE = 18;
    static constexpr size_t TOTAL_KEYS = 132;
    static constexpr size_t NUM_CHUNKS = 8;
    static constexpr size_t PACKET_SIZE = 65;

    static constexpr uint8_t CMD_KEYBOARD_LIGHT = 0x07;
    static constexpr uint8_t CMD_CUSTOM_CHUNK = 0x09;
    static constexpr uint8_t MODE_CUSTOM = 10;

    explicit RedragonK556Transmitter(std::string device_path = "");
    ~RedragonK556Transmitter() override;

    bool connect() override;
    void disconnect() override;
    [[nodiscard]] bool is_connected() const override;
    bool send_frame(const core::models::RenderFrame& frame) override;

    void set_hardware_brightness(int level);

    // Static helper to build packet buffers for testing and zero-allocation transmission
    static void format_chunk_packet(
        uint8_t* packet_out,
        size_t chunk_idx,
        const core::models::ColorRGB* colors,
        size_t total_keys
    );

    static void format_mode_packet(uint8_t* packet_out, int brightness = 4);
    static void format_init_packet(uint8_t* packet_out);

private:
    std::string device_path_;
    void* device_handle_{nullptr};
    bool connected_{false};

    // Pre-allocated contiguous packets (8 x 65 bytes)
    std::array<std::array<uint8_t, PACKET_SIZE>, NUM_CHUNKS> packets_{};
};

} // namespace openrgb_flowers::hardware
