#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/hardware/redragon_k556_transmitter.hpp"
#include "openrgb_flowers/hardware/openrgb_transmitter.hpp"
#include "openrgb_flowers/hardware/mock_transmitter.hpp"
#include <cstring>

using namespace openrgb_flowers::hardware;
using namespace openrgb_flowers::core::models;

TEST_CASE(HardwarePackets, RedragonModePacketFormat) {
    uint8_t pkt[65];
    RedragonK556Transmitter::format_mode_packet(pkt, 4);

    EXPECT_EQ(pkt[0], 0x01); // Report ID
    EXPECT_EQ(pkt[1], 0x07); // CMD_KEYBOARD_LIGHT
    EXPECT_EQ(pkt[5], 0x0E); // Payload length 14 bytes
    EXPECT_EQ(pkt[6], 10);   // Mode 10 (Custom LED)
    EXPECT_EQ(pkt[7], 4);    // Hardware brightness 4
    EXPECT_EQ(pkt[16], 1);   // FullColor RGB
    EXPECT_EQ(pkt[17], 0);   // Power ON
}

TEST_CASE(HardwarePackets, RedragonInitPacketFormat) {
    uint8_t pkt[65];
    RedragonK556Transmitter::format_init_packet(pkt);

    EXPECT_EQ(pkt[0], 0x01); // Report ID
    EXPECT_EQ(pkt[1], 0x09); // CMD_CUSTOM_CHUNK
    EXPECT_EQ(pkt[2], 0x20); // Subcommand 0x20
}

TEST_CASE(HardwarePackets, RedragonChunkPackets) {
    std::vector<ColorRGB> colors(132, ColorRGB(255, 128, 64));
    uint8_t pkt[65];

    // Chunk 0 (18 keys = 54 bytes)
    RedragonK556Transmitter::format_chunk_packet(pkt, 0, colors.data(), colors.size());
    EXPECT_EQ(pkt[0], 0x01);
    EXPECT_EQ(pkt[1], 0x09);
    EXPECT_EQ(pkt[4], 0);    // Chunk index 0
    EXPECT_EQ(pkt[5], 54);   // 18 keys * 3 bytes = 54
    EXPECT_EQ(pkt[6], 255);  // Key 0 Red
    EXPECT_EQ(pkt[7], 128);  // Key 0 Green
    EXPECT_EQ(pkt[8], 64);   // Key 0 Blue

    // Chunk 7 (6 keys = 18 bytes)
    RedragonK556Transmitter::format_chunk_packet(pkt, 7, colors.data(), colors.size());
    EXPECT_EQ(pkt[4], 7);    // Chunk index 7
    EXPECT_EQ(pkt[5], 18);   // 6 keys * 3 bytes = 18
}

TEST_CASE(HardwarePackets, OpenRGBPacketHeader) {
    std::vector<ColorRGB> colors = {ColorRGB(255, 0, 0), ColorRGB(0, 255, 0)};
    auto pkt = OpenRGBTransmitter::build_update_leds_packet(0, colors.data(), colors.size());

    // Total size: 16 (header) + 4 (size) + 2 (num_leds) + 2 * 4 (colors) = 30 bytes
    EXPECT_EQ(pkt.size(), 30);

    // Header magic "ORGB"
    EXPECT_EQ(pkt[0], 'O');
    EXPECT_EQ(pkt[1], 'R');
    EXPECT_EQ(pkt[2], 'G');
    EXPECT_EQ(pkt[3], 'B');

    // Packet type is 1050 (RGBCONTROLLER_UPDATELEDS)
    uint32_t pkt_type = 0;
    std::memcpy(&pkt_type, &pkt[8], sizeof(uint32_t));
    EXPECT_EQ(pkt_type, 1050);
}

TEST_CASE(HardwarePackets, MockTransmitter) {
    MockTransmitter mock;
    EXPECT_FALSE(mock.is_connected());
    mock.connect();
    EXPECT_TRUE(mock.is_connected());

    RenderFrame f(1.0, 1, {ColorRGB(1, 2, 3)});
    EXPECT_TRUE(mock.send_frame(f));
    EXPECT_EQ(mock.get_transmitted_frames(), 1);
    EXPECT_EQ(mock.get_last_frame().led_count, 1);

    mock.disconnect();
    EXPECT_FALSE(mock.is_connected());
}
