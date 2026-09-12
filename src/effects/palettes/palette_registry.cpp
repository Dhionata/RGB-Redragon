#include "openrgb_flowers/effects/palettes/palette_registry.hpp"
#include "openrgb_flowers/effects/palettes/sakura_palette.hpp"
#include "openrgb_flowers/effects/palettes/rose_palette.hpp"
#include "openrgb_flowers/effects/palettes/lotus_palette.hpp"
#include "openrgb_flowers/effects/palettes/sunflower_palette.hpp"
#include "openrgb_flowers/effects/palettes/lavender_palette.hpp"
#include "openrgb_flowers/effects/palettes/rainbow_palette.hpp"
#include "openrgb_flowers/effects/palettes/cyberpunk_palette.hpp"
#include "openrgb_flowers/effects/palettes/aurora_palette.hpp"

#include <algorithm>
#include <cctype>
#include <stdexcept>

namespace openrgb_flowers::effects::palettes {

namespace {

std::string to_lower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c) {
        return static_cast<char>(std::tolower(c));
    });
    return s;
}

} // anonymous namespace

std::shared_ptr<core::interfaces::IColorPalette> PaletteRegistry::get(const std::string& name) {
    std::string key = to_lower(name);
    if (key == "sakura") return std::make_shared<SakuraPalette>();
    if (key == "rose") return std::make_shared<RosePalette>();
    if (key == "lotus") return std::make_shared<LotusPalette>();
    if (key == "sunflower") return std::make_shared<SunflowerPalette>();
    if (key == "lavender") return std::make_shared<LavenderPalette>();
    if (key == "rainbow") return std::make_shared<RainbowPalette>();
    if (key == "cyberpunk") return std::make_shared<CyberpunkPalette>();
    if (key == "aurora") return std::make_shared<AuroraPalette>();

    throw std::invalid_argument("Unknown palette: " + name);
}

std::vector<std::string> PaletteRegistry::list_available() {
    return {
        "sakura",
        "rose",
        "lotus",
        "sunflower",
        "lavender",
        "rainbow",
        "cyberpunk",
        "aurora"
    };
}

bool PaletteRegistry::has(const std::string& name) {
    std::string key = to_lower(name);
    const auto list = list_available();
    return std::find(list.begin(), list.end(), key) != list.end();
}

} // namespace openrgb_flowers::effects::palettes
