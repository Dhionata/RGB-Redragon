#include "openrgb_flowers/effects/palettes/lotus_palette.hpp"

namespace openrgb_flowers::effects::palettes {

LotusPalette::LotusPalette()
    : BaseColorPalette("lotus", {
        {0.00f, core::models::ColorRGB(255, 200, 20)},  // Saffron gold pistil
        {0.25f, core::models::ColorRGB(255, 60, 140)},  // Rich magenta petal
        {0.65f, core::models::ColorRGB(180, 80, 230)},  // Mystic violet body
        {0.85f, core::models::ColorRGB(100, 200, 240)}, // Aquatic cyan dewdrop edge
        {1.00f, core::models::ColorRGB(220, 245, 255)}, // Translucent water mist
    }) {}

} // namespace openrgb_flowers::effects::palettes
