#include "openrgb_flowers/effects/palettes/sakura_palette.hpp"

namespace openrgb_flowers::effects::palettes {

SakuraPalette::SakuraPalette()
    : BaseColorPalette("sakura", {
        {0.00f, core::models::ColorRGB(255, 215, 64)},   // Warm golden stamen
        {0.20f, core::models::ColorRGB(255, 105, 180)},  // Hot pink petal throat
        {0.55f, core::models::ColorRGB(255, 182, 193)},  // Soft cherry blossom pink
        {0.85f, core::models::ColorRGB(255, 230, 240)},  // Delicate petal blush
        {1.00f, core::models::ColorRGB(245, 250, 255)},  // Frost ivory petal tip
    }) {}

} // namespace openrgb_flowers::effects::palettes
