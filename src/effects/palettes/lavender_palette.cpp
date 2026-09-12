#include "openrgb_flowers/effects/palettes/lavender_palette.hpp"

namespace openrgb_flowers::effects::palettes {

LavenderPalette::LavenderPalette()
    : BaseColorPalette("lavender", {
        {0.00f, core::models::ColorRGB(95, 25, 140)},   // Deep royal amethyst
        {0.30f, core::models::ColorRGB(147, 88, 204)},  // Purple floral petal
        {0.65f, core::models::ColorRGB(186, 140, 245)}, // Lilac bloom
        {0.85f, core::models::ColorRGB(215, 185, 255)}, // Soft periwinkle
        {1.00f, core::models::ColorRGB(240, 230, 255)}, // Morning mist tip
    }) {}

} // namespace openrgb_flowers::effects::palettes
