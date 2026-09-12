#include "openrgb_flowers/hardware/redragon_k556_transmitter.hpp"

#ifdef _WIN32
#include <windows.h>
#include <setupapi.h>
#include <hidsdi.h>
#endif

#include <algorithm>
#include <cstring>
#include <iostream>

namespace openrgb_flowers::hardware {

RedragonK556Transmitter::RedragonK556Transmitter(std::string device_path)
    : device_path_(std::move(device_path)) {
    for (size_t c = 0; c < NUM_CHUNKS; ++c) {
        size_t n_keys = (c < 7) ? CHUNK_SIZE : 6;
        size_t n_bytes = n_keys * 3;
        auto& pkt = packets_[c];
        pkt.fill(0);
        pkt[0] = 0x01;
        pkt[1] = CMD_CUSTOM_CHUNK;
        pkt[2] = 0x00;
        pkt[3] = static_cast<uint8_t>((c >> 8) & 0xFF);
        pkt[4] = static_cast<uint8_t>(c & 0xFF);
        pkt[5] = static_cast<uint8_t>(n_bytes);
    }
}

RedragonK556Transmitter::~RedragonK556Transmitter() {
    disconnect();
}

void RedragonK556Transmitter::format_mode_packet(uint8_t* packet_out, int brightness) {
    std::memset(packet_out, 0, PACKET_SIZE);
    packet_out[0] = 0x01;
    packet_out[1] = CMD_KEYBOARD_LIGHT;
    packet_out[5] = 0x0E;
    packet_out[6] = MODE_CUSTOM;
    packet_out[7] = static_cast<uint8_t>(std::clamp(brightness, 0, 4));
    packet_out[8] = 3;   // Speed
    packet_out[9] = 255; // Foreground Red
    packet_out[16] = 1;  // FullColor RGB
    packet_out[17] = 0;  // Light ON
}

void RedragonK556Transmitter::format_init_packet(uint8_t* packet_out) {
    std::memset(packet_out, 0, PACKET_SIZE);
    packet_out[0] = 0x01;
    packet_out[1] = CMD_CUSTOM_CHUNK;
    packet_out[2] = 0x20;
}

void RedragonK556Transmitter::format_chunk_packet(
    uint8_t* packet_out,
    size_t chunk_idx,
    const core::models::ColorRGB* colors,
    size_t total_keys
) {
    std::memset(packet_out, 0, PACKET_SIZE);
    size_t n_keys = (chunk_idx < 7) ? CHUNK_SIZE : 6;
    size_t n_bytes = n_keys * 3;

    packet_out[0] = 0x01;
    packet_out[1] = CMD_CUSTOM_CHUNK;
    packet_out[2] = 0x00;
    packet_out[3] = static_cast<uint8_t>((chunk_idx >> 8) & 0xFF);
    packet_out[4] = static_cast<uint8_t>(chunk_idx & 0xFF);
    packet_out[5] = static_cast<uint8_t>(n_bytes);

    size_t start_key = chunk_idx * CHUNK_SIZE;
    for (size_t k = 0; k < n_keys; ++k) {
        size_t key_idx = start_key + k;
        if (key_idx < total_keys && colors != nullptr) {
            packet_out[6 + k * 3 + 0] = colors[key_idx].r;
            packet_out[6 + k * 3 + 1] = colors[key_idx].g;
            packet_out[6 + k * 3 + 2] = colors[key_idx].b;
        } else {
            packet_out[6 + k * 3 + 0] = 0;
            packet_out[6 + k * 3 + 1] = 0;
            packet_out[6 + k * 3 + 2] = 0;
        }
    }
}

bool RedragonK556Transmitter::is_connected() const {
    return connected_ && device_handle_ != nullptr;
}

bool RedragonK556Transmitter::connect() {
#ifdef _WIN32
    if (is_connected()) return true;

    GUID hid_guid;
    HidD_GetHidGuid(&hid_guid);

    HDEVINFO dev_info = SetupDiGetClassDevsW(&hid_guid, nullptr, nullptr, DIGCF_PRESENT | DIGCF_DEVICEINTERFACE);
    if (dev_info == INVALID_HANDLE_VALUE) {
        return false;
    }

    SP_DEVICE_INTERFACE_DATA dev_interface_data;
    dev_interface_data.cbSize = sizeof(SP_DEVICE_INTERFACE_DATA);

    std::string matched_path;

    for (DWORD i = 0; SetupDiEnumDeviceInterfaces(dev_info, nullptr, &hid_guid, i, &dev_interface_data); ++i) {
        DWORD required_size = 0;
        SetupDiGetDeviceInterfaceDetailW(dev_info, &dev_interface_data, nullptr, 0, &required_size, nullptr);
        if (required_size == 0) continue;

        std::vector<BYTE> detail_buf(required_size);
        auto detail_data = reinterpret_cast<PSP_DEVICE_INTERFACE_DETAIL_DATA_W>(detail_buf.data());
        detail_data->cbSize = sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA_W);

        if (SetupDiGetDeviceInterfaceDetailW(dev_info, &dev_interface_data, detail_data, required_size, nullptr, nullptr)) {
            HANDLE handle = CreateFileW(
                detail_data->DevicePath,
                GENERIC_READ | GENERIC_WRITE,
                FILE_SHARE_READ | FILE_SHARE_WRITE,
                nullptr,
                OPEN_EXISTING,
                0,
                nullptr
            );

            if (handle != INVALID_HANDLE_VALUE) {
                HIDD_ATTRIBUTES attrs;
                attrs.Size = sizeof(HIDD_ATTRIBUTES);
                if (HidD_GetAttributes(handle, &attrs)) {
                    if (attrs.VendorID == VID && attrs.ProductID == PID) {
                        // Check if interface matches or if explicit path was given
                        std::wstring wpath(detail_data->DevicePath);
                        std::string apath(wpath.begin(), wpath.end());

                        bool is_target_if = (apath.find("&mi_02") != std::string::npos ||
                                             apath.find("&mi_0002") != std::string::npos ||
                                             apath.find("&col02") != std::string::npos ||
                                             (!device_path_.empty() && apath == device_path_));

                        if (is_target_if || matched_path.empty()) {
                            matched_path = apath;
                            device_handle_ = handle;
                            if (is_target_if) {
                                break;
                            }
                        }
                    }
                }
                if (device_handle_ != handle) {
                    CloseHandle(handle);
                }
            }
        }
    }

    SetupDiDestroyDeviceInfoList(dev_info);

    if (device_handle_ == nullptr || device_handle_ == INVALID_HANDLE_VALUE) {
        connected_ = false;
        device_handle_ = nullptr;
        return false;
    }

    // Switch to Custom LED Mode (Mode 10)
    uint8_t mode_pkt[PACKET_SIZE];
    format_mode_packet(mode_pkt, 4);
    DWORD written = 0;
    WriteFile(device_handle_, mode_pkt, PACKET_SIZE, &written, nullptr);

    // Send Activation packet (0x09 0x20)
    uint8_t init_pkt[PACKET_SIZE];
    format_init_packet(init_pkt);
    WriteFile(device_handle_, init_pkt, PACKET_SIZE, &written, nullptr);

    connected_ = true;
    return true;
#else
    return false;
#endif
}

void RedragonK556Transmitter::set_hardware_brightness(int level) {
#ifdef _WIN32
    if (!is_connected()) return;
    uint8_t mode_pkt[PACKET_SIZE];
    format_mode_packet(mode_pkt, level);
    DWORD written = 0;
    WriteFile(device_handle_, mode_pkt, PACKET_SIZE, &written, nullptr);
#endif
}

void RedragonK556Transmitter::disconnect() {
#ifdef _WIN32
    if (device_handle_ != nullptr && device_handle_ != INVALID_HANDLE_VALUE) {
        CloseHandle(device_handle_);
        device_handle_ = nullptr;
    }
#endif
    connected_ = false;
}

bool RedragonK556Transmitter::send_frame(const core::models::RenderFrame& frame) {
    if (!is_connected()) return false;

#ifdef _WIN32
    const core::models::ColorRGB* cols = frame.data();
    size_t total_keys = static_cast<size_t>(frame.led_count);

    for (size_t c = 0; c < NUM_CHUNKS; ++c) {
        auto& pkt = packets_[c];
        size_t n_keys = (c < 7) ? CHUNK_SIZE : 6;
        size_t start_key = c * CHUNK_SIZE;

        for (size_t k = 0; k < n_keys; ++k) {
            size_t key_idx = start_key + k;
            if (key_idx < total_keys) {
                pkt[6 + k * 3 + 0] = cols[key_idx].r;
                pkt[6 + k * 3 + 1] = cols[key_idx].g;
                pkt[6 + k * 3 + 2] = cols[key_idx].b;
            } else {
                pkt[6 + k * 3 + 0] = 0;
                pkt[6 + k * 3 + 1] = 0;
                pkt[6 + k * 3 + 2] = 0;
            }
        }

        DWORD written = 0;
        BOOL ok = WriteFile(device_handle_, pkt.data(), PACKET_SIZE, &written, nullptr);
        if (!ok || written != PACKET_SIZE) {
            // Fallback to HidD_SetOutputReport as used by hidapi on Windows
            if (!HidD_SetOutputReport(device_handle_, pkt.data(), PACKET_SIZE)) {
                connected_ = false;
                return false;
            }
        }
    }
    return true;
#else
    return false;
#endif
}

} // namespace openrgb_flowers::hardware
