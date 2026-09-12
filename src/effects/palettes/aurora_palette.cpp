#include "openrgb_flowers/effects/palettes/aurora_palette.hpp"

namespace openrgb_flowers::effects::palettes {

AuroraPalette::AuroraPalette()
    : BaseColorPalette("aurora", {
        {0.00f, core::models::ColorRGB(0, 255, 135)},    // Polar Green
        {0.30f, core::models::ColorRGB(96, 239, 255)},   // Turquoise
        {0.60f, core::models::ColorRGB(0, 180, 216)},    // Deep Ice Blue
        {0.85f, core::models::ColorRGB(123, 44, 191)},   // Royal Violet
        {1.00f, core::models::ColorRGB(224, 86, 253)},   // Radiant Magenta
    }) {}

} // namespace openrgb_flowers::effects::palettes
