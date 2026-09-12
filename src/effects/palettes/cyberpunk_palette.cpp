#include "openrgb_flowers/effects/palettes/cyberpunk_palette.hpp"

namespace openrgb_flowers::effects::palettes {

CyberpunkPalette::CyberpunkPalette()
    : BaseColorPalette("cyberpunk", {
        {0.00f, core::models::ColorRGB(0, 240, 255)},    // Electric Neon Cyan
        {0.30f, core::models::ColorRGB(255, 0, 128)},    // Hot Magenta
        {0.60f, core::models::ColorRGB(255, 230, 0)},    // Acid Yellow
        {0.85f, core::models::ColorRGB(157, 0, 255)},    // Electric Violet
        {1.00f, core::models::ColorRGB(0, 255, 170)},    // Neon Mint Green
    }) {}

} // namespace openrgb_flowers::effects::palettes
