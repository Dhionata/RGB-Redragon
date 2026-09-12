#include "openrgb_flowers/effects/palettes/rose_palette.hpp"

namespace openrgb_flowers::effects::palettes {

RosePalette::RosePalette()
    : BaseColorPalette("rose", {
        {0.00f, core::models::ColorRGB(180, 10, 30)},    // Deep ruby stamen
        {0.25f, core::models::ColorRGB(220, 20, 60)},   // Crimson velvet core
        {0.60f, core::models::ColorRGB(255, 45, 85)},   // Radiant scarlet petal
        {0.85f, core::models::ColorRGB(255, 110, 130)}, // Coral blush rim
        {1.00f, core::models::ColorRGB(255, 180, 190)}, // Soft blossom edge
    }) {}

} // namespace openrgb_flowers::effects::palettes
