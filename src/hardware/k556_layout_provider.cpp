#include "openrgb_flowers/hardware/k556_layout_provider.hpp"
#include <tuple>

namespace openrgb_flowers::hardware {

K556LayoutProvider::K556LayoutProvider() {
    constexpr float total_w = 22.5f;
    constexpr float total_h = 6.2f;

    keys_.reserve(104);
    x_coords_.reserve(104);
    y_coords_.reserve(104);

    int led_idx = 0;

    auto add_row = [&](int row_num, float y_center_u, const std::vector<std::pair<std::string, float>>& defs) {
        float ny = y_center_u / total_h;
        for (const auto& [name, x_u] : defs) {
            float nx = x_u / total_w;
            keys_.emplace_back(name, led_idx, nx, ny, row_num, static_cast<int>(x_u));
            x_coords_.push_back(nx);
            y_coords_.push_back(ny);
            ++led_idx;
        }
    };

    // Row 0: Function Keys
    add_row(0, 0.5f, {
        {"Escape", 0.5f},
        {"F1", 2.0f}, {"F2", 3.0f}, {"F3", 4.0f}, {"F4", 5.0f},
        {"F5", 6.5f}, {"F6", 7.5f}, {"F7", 8.5f}, {"F8", 9.5f},
        {"F9", 11.0f}, {"F10", 12.0f}, {"F11", 13.0f}, {"F12", 14.0f},
        {"PrintScreen", 15.5f}, {"ScrollLock", 16.5f}, {"Pause", 17.5f}
    });

    // Row 1: Number Row
    add_row(1, 1.7f, {
        {"Grave", 0.5f}, {"1", 1.5f}, {"2", 2.5f}, {"3", 3.5f}, {"4", 4.5f},
        {"5", 5.5f}, {"6", 6.5f}, {"7", 7.5f}, {"8", 8.5f}, {"9", 9.5f},
        {"0", 10.5f}, {"Minus", 11.5f}, {"Equal", 12.5f}, {"Backspace", 14.0f},
        {"Insert", 15.5f}, {"Home", 16.5f}, {"PageUp", 17.5f},
        {"NumLock", 19.0f}, {"NumSlash", 20.0f}, {"NumAsterisk", 21.0f}, {"NumMinus", 22.0f}
    });

    // Row 2: QWERTY Row
    add_row(2, 2.7f, {
        {"Tab", 0.75f}, {"Q", 2.0f}, {"W", 3.0f}, {"E", 4.0f}, {"R", 5.0f},
        {"T", 6.0f}, {"Y", 7.0f}, {"U", 8.0f}, {"I", 9.0f}, {"O", 10.0f},
        {"P", 11.0f}, {"LeftBracket", 12.0f}, {"RightBracket", 13.0f}, {"Backslash", 14.25f},
        {"Delete", 15.5f}, {"End", 16.5f}, {"PageDown", 17.5f},
        {"Num7", 19.0f}, {"Num8", 20.0f}, {"Num9", 21.0f}, {"NumPlus", 22.0f}
    });

    // Row 3: Home Row
    add_row(3, 3.7f, {
        {"CapsLock", 0.88f}, {"A", 2.25f}, {"S", 3.25f}, {"D", 4.25f}, {"F", 5.25f},
        {"G", 6.25f}, {"H", 7.25f}, {"J", 8.25f}, {"K", 9.25f}, {"L", 10.25f},
        {"Semicolon", 11.25f}, {"Apostrophe", 12.25f}, {"Enter", 13.88f},
        {"Num4", 19.0f}, {"Num5", 20.0f}, {"Num6", 21.0f}
    });

    // Row 4: Shift Row
    add_row(4, 4.7f, {
        {"LeftShift", 1.12f}, {"Z", 2.75f}, {"X", 3.75f}, {"C", 4.75f}, {"V", 5.75f},
        {"B", 6.75f}, {"N", 7.75f}, {"M", 8.75f}, {"Comma", 9.75f}, {"Period", 10.75f},
        {"Slash", 11.75f}, {"RightShift", 13.38f},
        {"UpArrow", 16.5f},
        {"Num1", 19.0f}, {"Num2", 20.0f}, {"Num3", 21.0f}, {"NumEnter", 22.0f}
    });

    // Row 5: Bottom Row
    add_row(5, 5.7f, {
        {"LeftControl", 0.62f}, {"LeftWindows", 1.88f}, {"LeftAlt", 3.12f},
        {"Space", 7.0f},
        {"RightAlt", 10.88f}, {"RightWindows", 12.12f}, {"Menu", 13.38f}, {"RightControl", 14.38f},
        {"LeftArrow", 15.5f}, {"DownArrow", 16.5f}, {"RightArrow", 17.5f},
        {"Num0", 19.5f}, {"NumPeriod", 21.0f}
    });
}

std::string K556LayoutProvider::get_device_name() const {
    return "Redragon K556RGB-M";
}

size_t K556LayoutProvider::get_key_count() const {
    return keys_.size();
}

const std::vector<core::models::KeyCoordinate>& K556LayoutProvider::get_coordinates() const {
    return keys_;
}

const float* K556LayoutProvider::get_x_coords() const {
    return x_coords_.data();
}

const float* K556LayoutProvider::get_y_coords() const {
    return y_coords_.data();
}

} // namespace openrgb_flowers::hardware
