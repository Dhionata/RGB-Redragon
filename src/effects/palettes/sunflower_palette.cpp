#include "openrgb_flowers/effects/palettes/sunflower_palette.hpp"

namespace openrgb_flowers::effects::palettes {

SunflowerPalette::SunflowerPalette()
    : BaseColorPalette("sunflower", {
        {0.00f, core::models::ColorRGB(90, 45, 15)},    // Roasted chocolate stamen
        {0.20f, core::models::ColorRGB(210, 105, 10)},  // Deep amber transition
        {0.55f, core::models::ColorRGB(255, 170, 0)},   // Rich golden sunflower petal
        {0.85f, core::models::ColorRGB(255, 220, 30)},  // Radiant sunny yellow
        {1.00f, core::models::ColorRGB(255, 245, 140)}, // Sunlit bright tip
    }) {}

} // namespace openrgb_flowers::effects::palettes
