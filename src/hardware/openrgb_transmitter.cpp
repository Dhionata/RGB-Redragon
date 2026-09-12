#include "openrgb_flowers/hardware/openrgb_transmitter.hpp"

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#define SOCKET int
#define INVALID_SOCKET -1
#define closesocket close
#endif

#include <cstring>
#include <iostream>

namespace openrgb_flowers::hardware {

namespace {

#ifdef _WIN32
struct WinsockInit {
    WinsockInit() {
        WSADATA wsa;
        WSAStartup(MAKEWORD(2, 2), &wsa);
    }
    ~WinsockInit() {
        WSACleanup();
    }
};

static WinsockInit s_winsock_init;
#endif

} // anonymous namespace

OpenRGBTransmitter::OpenRGBTransmitter(
    std::string host,
    int port,
    std::string device_name,
    int device_index,
    std::string client_name
) : host_(std::move(host)),
    port_(port),
    target_name_(std::move(device_name)),
    target_index_(device_index),
    client_name_(std::move(client_name)) {}

OpenRGBTransmitter::~OpenRGBTransmitter() {
    disconnect();
}

bool OpenRGBTransmitter::is_connected() const {
    return connected_ && socket_fd_ != static_cast<uintptr_t>(INVALID_SOCKET);
}

bool OpenRGBTransmitter::send_all(const uint8_t* data, size_t length) {
    size_t sent = 0;
    while (sent < length) {
        int res = ::send(
            static_cast<SOCKET>(socket_fd_),
            reinterpret_cast<const char*>(data + sent),
            static_cast<int>(length - sent),
            0
        );
        if (res <= 0) {
            connected_ = false;
            return false;
        }
        sent += static_cast<size_t>(res);
    }
    return true;
}

bool OpenRGBTransmitter::recv_all(uint8_t* data, size_t length) {
    size_t received = 0;
    while (received < length) {
        int res = ::recv(
            static_cast<SOCKET>(socket_fd_),
            reinterpret_cast<char*>(data + received),
            static_cast<int>(length - received),
            0
        );
        if (res <= 0) {
            connected_ = false;
            return false;
        }
        received += static_cast<size_t>(res);
    }
    return true;
}

void OpenRGBTransmitter::format_update_leds_packet(
    std::vector<uint8_t>& buffer,
    uint32_t device_id,
    const core::models::ColorRGB* colors,
    size_t count
) {
    uint32_t payload_size = static_cast<uint32_t>(sizeof(uint32_t) + sizeof(uint16_t) + count * 4);
    size_t total_size = 16 + payload_size;

    if (buffer.size() != total_size) {
        buffer.resize(total_size);
    }

    // 16-byte OpenRGB Header:
    // Magic: "ORGB"
    buffer[0] = 'O'; buffer[1] = 'R'; buffer[2] = 'G'; buffer[3] = 'B';
    std::memcpy(&buffer[4], &device_id, sizeof(uint32_t));
    uint32_t pkt_type = PACKET_RGBCONTROLLER_UPDATELEDS;
    std::memcpy(&buffer[8], &pkt_type, sizeof(uint32_t));
    std::memcpy(&buffer[12], &payload_size, sizeof(uint32_t));

    // Payload:
    std::memcpy(&buffer[16], &payload_size, sizeof(uint32_t));
    auto num_leds_16 = static_cast<uint16_t>(count);
    std::memcpy(&buffer[20], &num_leds_16, sizeof(uint16_t));

    // LED colors
    size_t offset = 22;
    for (size_t i = 0; i < count; ++i) {
        buffer[offset + 0] = colors ? colors[i].r : 0;
        buffer[offset + 1] = colors ? colors[i].g : 0;
        buffer[offset + 2] = colors ? colors[i].b : 0;
        buffer[offset + 3] = 0; // alpha/padding
        offset += 4;
    }
}

std::vector<uint8_t> OpenRGBTransmitter::build_update_leds_packet(
    uint32_t device_id,
    const core::models::ColorRGB* colors,
    size_t count
) {
    std::vector<uint8_t> packet;
    format_update_leds_packet(packet, device_id, colors, count);
    return packet;
}

bool OpenRGBTransmitter::connect() {
    if (is_connected()) return true;

    SOCKET sock = ::socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        return false;
    }

    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(static_cast<u_short>(port_));
    if (inet_pton(AF_INET, host_.c_str(), &server_addr.sin_addr) <= 0) {
        closesocket(sock);
        return false;
    }

    // Connect with 2-second timeout
#ifdef _WIN32
    DWORD timeout = 2000;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, reinterpret_cast<const char*>(&timeout), sizeof(timeout));
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, reinterpret_cast<const char*>(&timeout), sizeof(timeout));
#endif

    if (::connect(sock, reinterpret_cast<sockaddr*>(&server_addr), sizeof(server_addr)) != 0) {
        closesocket(sock);
        return false;
    }

    socket_fd_ = static_cast<uintptr_t>(sock);
    connected_ = true;

    // 1. Send Protocol Version handshake (version 4)
    uint32_t client_version = 4;
    uint8_t proto_header[20];
    proto_header[0] = 'O'; proto_header[1] = 'R'; proto_header[2] = 'G'; proto_header[3] = 'B';
    uint32_t dev0 = 0;
    uint32_t type_proto = PACKET_REQUEST_PROTOCOL_VERSION;
    uint32_t size_proto = 4;
    std::memcpy(&proto_header[4], &dev0, 4);
    std::memcpy(&proto_header[8], &type_proto, 4);
    std::memcpy(&proto_header[12], &size_proto, 4);
    std::memcpy(&proto_header[16], &client_version, 4);
    send_all(proto_header, 20);

    // Read protocol response header + payload
    uint8_t resp_header[16];
    if (recv_all(resp_header, 16)) {
        uint32_t resp_size = 0;
        std::memcpy(&resp_size, &resp_header[12], 4);
        if (resp_size > 0) {
            std::vector<uint8_t> dump(resp_size);
            recv_all(dump.data(), resp_size);
        }
    }

    // 2. Send Client Name
    std::string name_with_null = client_name_ + '\0';
    uint32_t name_len = static_cast<uint32_t>(name_with_null.size());
    std::vector<uint8_t> name_packet(16 + name_len);
    name_packet[0] = 'O'; name_packet[1] = 'R'; name_packet[2] = 'G'; name_packet[3] = 'B';
    std::memcpy(&name_packet[4], &dev0, 4);
    uint32_t type_name = PACKET_SET_CLIENT_NAME;
    std::memcpy(&name_packet[8], &type_name, 4);
    std::memcpy(&name_packet[12], &name_len, 4);
    std::memcpy(&name_packet[16], name_with_null.data(), name_len);
    send_all(name_packet.data(), name_packet.size());

    // Target device ID defaults to 0 (or device_index if specified)
    device_id_ = (target_index_ >= 0) ? static_cast<uint32_t>(target_index_) : 0;

    return true;
}

void OpenRGBTransmitter::disconnect() {
    if (socket_fd_ != static_cast<uintptr_t>(INVALID_SOCKET)) {
        closesocket(static_cast<SOCKET>(socket_fd_));
        socket_fd_ = static_cast<uintptr_t>(INVALID_SOCKET);
    }
    connected_ = false;
}

bool OpenRGBTransmitter::send_frame(const core::models::RenderFrame& frame) {
    if (!is_connected()) return false;

    format_update_leds_packet(send_buffer_, device_id_, frame.data(), static_cast<size_t>(frame.led_count));
    return send_all(send_buffer_.data(), send_buffer_.size());
}

} // namespace openrgb_flowers::hardware
