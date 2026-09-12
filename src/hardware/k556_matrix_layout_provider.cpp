#include "openrgb_flowers/hardware/k556_matrix_layout_provider.hpp"
#include <map>

namespace openrgb_flowers::hardware {

namespace {

const std::map<std::pair<int, int>, std::string>& get_key_names() {
    static const std::map<std::pair<int, int>, std::string> names = {
        // Row 0 (F-row & Media)
        {{0, 0}, "Escape"},
        {{0, 2}, "F1"}, {{0, 3}, "F2"}, {{0, 4}, "F3"}, {{0, 5}, "F4"},
        {{0, 7}, "F5"}, {{0, 8}, "F6"}, {{0, 9}, "F7"}, {{0, 10}, "F8"},
        {{0, 11}, "F9"}, {{0, 12}, "F10"}, {{0, 13}, "F11"}, {{0, 14}, "F12"},
        {{0, 15}, "PrintScreen"}, {{0, 16}, "ScrollLock"}, {{0, 17}, "Pause"},

        // Row 1 (Number row & Nav top & Numpad top)
        {{1, 0}, "Grave"}, {{1, 1}, "1"}, {{1, 2}, "2"}, {{1, 3}, "3"}, {{1, 4}, "4"},
        {{1, 5}, "5"}, {{1, 6}, "6"}, {{1, 7}, "7"}, {{1, 8}, "8"}, {{1, 9}, "9"}, {{1, 10}, "0"},
        {{1, 11}, "Minus"}, {{1, 12}, "Equal"}, {{1, 14}, "Backspace"},
        {{1, 15}, "Insert"}, {{1, 16}, "Home"}, {{1, 17}, "PageUp"},
        {{1, 18}, "NumLock"}, {{1, 19}, "NumSlash"}, {{1, 20}, "NumAsterisk"}, {{1, 21}, "NumMinus"},

        // Row 2 (QWERTY row)
        {{2, 0}, "Tab"}, {{2, 1}, "Q"}, {{2, 2}, "W"}, {{2, 3}, "E"}, {{2, 4}, "R"},
        {{2, 5}, "T"}, {{2, 6}, "Y"}, {{2, 7}, "U"}, {{2, 8}, "I"}, {{2, 9}, "O"}, {{2, 10}, "P"},
        {{2, 11}, "LeftBracket"}, {{2, 12}, "RightBracket"},
        {{2, 15}, "Delete"}, {{2, 16}, "End"}, {{2, 17}, "PageDown"},
        {{2, 18}, "Num7"}, {{2, 19}, "Num8"}, {{2, 20}, "Num9"}, {{2, 21}, "NumPlus"},

        // Row 3 (Home row)
        {{3, 0}, "CapsLock"}, {{3, 2}, "A"}, {{3, 3}, "S"}, {{3, 4}, "D"}, {{3, 5}, "F"},
        {{3, 6}, "G"}, {{3, 7}, "H"}, {{3, 8}, "J"}, {{3, 9}, "K"}, {{3, 10}, "L"},
        {{3, 11}, "Semicolon"}, {{3, 12}, "Apostrophe"}, {{3, 13}, "Backslash"}, {{3, 14}, "Enter"},
        {{3, 18}, "Num4"}, {{3, 19}, "Num5"}, {{3, 20}, "Num6"},

        // Row 4 (Shift row & Arrow Up)
        {{4, 0}, "LeftShift"}, {{4, 1}, "IntlBackslash"}, {{4, 2}, "Z"}, {{4, 3}, "X"}, {{4, 4}, "C"},
        {{4, 5}, "V"}, {{4, 6}, "B"}, {{4, 7}, "N"}, {{4, 8}, "M"}, {{4, 9}, "Comma"}, {{4, 10}, "Period"},
        {{4, 11}, "Slash"}, {{4, 12}, "IntlRo"}, {{4, 14}, "RightShift"},
        {{4, 16}, "UpArrow"},
        {{4, 18}, "Num1"}, {{4, 19}, "Num2"}, {{4, 20}, "Num3"}, {{4, 21}, "NumEnter"},

        // Row 5 (Bottom row & Arrows)
        {{5, 0}, "LeftControl"}, {{5, 1}, "LeftWindows"}, {{5, 2}, "LeftAlt"}, {{5, 6}, "Space"},
        {{5, 10}, "RightAlt"}, {{5, 11}, "Fn"}, {{5, 12}, "Menu"}, {{5, 13}, "RightControl"},
        {{5, 15}, "LeftArrow"}, {{5, 16}, "DownArrow"}, {{5, 17}, "RightArrow"},
        {{5, 18}, "Num0"}, {{5, 20}, "NumPeriod"}
    };
    return names;
}

} // anonymous namespace

K556MatrixLayoutProvider::K556MatrixLayoutProvider() {
    keys_.reserve(TOTAL_KEYS);
    x_coords_.reserve(TOTAL_KEYS);
    y_coords_.reserve(TOTAL_KEYS);

    const auto& name_map = get_key_names();
    float max_c = static_cast<float>(COLS - 1);
    float max_r = static_cast<float>(ROWS - 1);

    int idx = 0;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            std::string name;
            auto it = name_map.find({r, c});
            if (it != name_map.end()) {
                name = it->second;
            }

            float nx = static_cast<float>(c) / max_c;
            float ny = static_cast<float>(r) / max_r;

            keys_.emplace_back(name, idx, nx, ny, r, c);
            x_coords_.push_back(nx);
            y_coords_.push_back(ny);
            ++idx;
        }
    }
}

std::string K556MatrixLayoutProvider::get_device_name() const {
    return "Redragon K556RGB-M (Hardware Matrix)";
}

size_t K556MatrixLayoutProvider::get_key_count() const {
    return TOTAL_KEYS;
}

const std::vector<core::models::KeyCoordinate>& K556MatrixLayoutProvider::get_coordinates() const {
    return keys_;
}

const float* K556MatrixLayoutProvider::get_x_coords() const {
    return x_coords_.data();
}

const float* K556MatrixLayoutProvider::get_y_coords() const {
    return y_coords_.data();
}

} // namespace openrgb_flowers::hardware
