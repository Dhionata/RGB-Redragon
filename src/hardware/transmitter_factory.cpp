#include "openrgb_flowers/hardware/transmitter_factory.hpp"
#include "openrgb_flowers/hardware/redragon_k556_transmitter.hpp"
#include "openrgb_flowers/hardware/openrgb_transmitter.hpp"
#include "openrgb_flowers/hardware/mock_transmitter.hpp"

#include <algorithm>
#include <cctype>
#include <iostream>

namespace openrgb_flowers::hardware {

namespace {

std::string to_lower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c) {
        return static_cast<char>(std::tolower(c));
    });
    return s;
}

} // anonymous namespace

std::shared_ptr<core::interfaces::IFrameTransmitter> TransmitterFactory::create_transmitter(
    const std::string& driver_name,
    const std::string& host,
    int port,
    const std::string& device_name,
    int device_index
) {
    std::string key = to_lower(driver_name);

    if (key == "mock" || key == "simulation") {
        return std::make_shared<MockTransmitter>();
    }

    if (key == "redragon" || key == "hid") {
        return std::make_shared<RedragonK556Transmitter>();
    }

    if (key == "openrgb" || key == "tcp") {
        return std::make_shared<OpenRGBTransmitter>(host, port, device_name, device_index);
    }

    // "auto" detection
    // 1. Try Redragon Direct USB HID
    auto redragon = std::make_shared<RedragonK556Transmitter>();
    if (redragon->connect()) {
        std::cout << "[Driver] Auto-detected Redragon K556RGB-M via Direct USB HID.\n";
        return redragon;
    }

    // 2. Try OpenRGB SDK
    auto openrgb = std::make_shared<OpenRGBTransmitter>(host, port, device_name, device_index);
    if (openrgb->connect()) {
        std::cout << "[Driver] Connected to OpenRGB SDK server at " << host << ":" << port << ".\n";
        return openrgb;
    }

    // 3. Fallback to mock transmitter with notice
    std::cout << "[Driver] No physical Redragon K556 or OpenRGB server found. Running in simulation mode.\n";
    auto mock = std::make_shared<MockTransmitter>();
    mock->connect();
    return mock;
}

} // namespace openrgb_flowers::hardware
