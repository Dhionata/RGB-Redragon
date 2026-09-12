#pragma once

#include "openrgb_flowers/core/interfaces/i_color_palette.hpp"
#include <functional>
#include <map>
#include <memory>
#include <string>
#include <vector>

namespace openrgb_flowers::effects::palettes {

/**
 * @brief Factory and registry for available floral palettes.
 */
class PaletteRegistry {
public:
    using PaletteCreator = std::function<std::unique_ptr<core::interfaces::IColorPalette>()>;

    static std::shared_ptr<core::interfaces::IColorPalette> get(const std::string& name);
    static std::vector<std::string> list_available();
    static bool has(const std::string& name);
};

} // namespace openrgb_flowers::effects::palettes
