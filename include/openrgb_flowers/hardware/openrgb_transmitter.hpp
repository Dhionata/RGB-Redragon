#pragma once

#include "openrgb_flowers/core/interfaces/i_frame_transmitter.hpp"
#include <cstdint>
#include <string>
#include <vector>

namespace openrgb_flowers::hardware {

/**
 * @brief High-speed frame transmitter communicating directly with the OpenRGB SDK via Winsock2 TCP socket.
 */
class OpenRGBTransmitter : public core::interfaces::IFrameTransmitter {
public:
    static constexpr uint32_t PACKET_REQUEST_CONTROLLER_COUNT = 0;
    static constexpr uint32_t PACKET_REQUEST_CONTROLLER_DATA = 1;
    static constexpr uint32_t PACKET_REQUEST_PROTOCOL_VERSION = 40;
    static constexpr uint32_t PACKET_SET_CLIENT_NAME = 50;
    static constexpr uint32_t PACKET_RGBCONTROLLER_UPDATELEDS = 1050;

    OpenRGBTransmitter(
        std::string host = "127.0.0.1",
        int port = 6742,
        std::string device_name = "",
        int device_index = -1,
        std::string client_name = "Flowers Blooming"
    );
    ~OpenRGBTransmitter() override;

    bool connect() override;
    void disconnect() override;
    [[nodiscard]] bool is_connected() const override;
    bool send_frame(const core::models::RenderFrame& frame) override;

    // Helper for formatting UPDATELEDS packet buffer (for tests and zero-allocation socket writes)
    static void format_update_leds_packet(
        std::vector<uint8_t>& buffer,
        uint32_t device_id,
        const core::models::ColorRGB* colors,
        size_t count
    );

    static std::vector<uint8_t> build_update_leds_packet(
        uint32_t device_id,
        const core::models::ColorRGB* colors,
        size_t count
    );

private:
    bool send_all(const uint8_t* data, size_t length);
    bool recv_all(uint8_t* data, size_t length);

    std::string host_{"127.0.0.1"};
    int port_{6742};
    std::string target_name_;
    int target_index_{-1};
    std::string client_name_{"Flowers Blooming"};

    uintptr_t socket_fd_{~0ULL}; // INVALID_SOCKET
    bool connected_{false};
    uint32_t device_id_{0};
    std::vector<uint8_t> send_buffer_;
};

} // namespace openrgb_flowers::hardware
