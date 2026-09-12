#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/effects/palettes/palette_registry.hpp"
#include "openrgb_flowers/effects/palettes/rainbow_palette.hpp"
#include "openrgb_flowers/effects/palettes/sakura_palette.hpp"

using namespace openrgb_flowers::effects::palettes;
using namespace openrgb_flowers::core::models;

TEST_CASE(Palettes, RegistryList) {
    auto list = PaletteRegistry::list_available();
    EXPECT_TRUE(list.size() >= 8);
    EXPECT_TRUE(PaletteRegistry::has("sakura"));
    EXPECT_TRUE(PaletteRegistry::has("rainbow"));
    EXPECT_TRUE(PaletteRegistry::has("cyberpunk"));
    EXPECT_TRUE(PaletteRegistry::has("aurora"));
    EXPECT_FALSE(PaletteRegistry::has("non_existent_palette"));
}

TEST_CASE(Palettes, SakuraSampling) {
    auto pal = PaletteRegistry::get("sakura");
    EXPECT_EQ(pal->get_name(), "sakura");

    ColorRGB center = pal->sample(0.0f);
    // Sakura center is warm golden stamen (255, 215, 64)
    EXPECT_EQ(center.r, 255);
    EXPECT_EQ(center.g, 215);
    EXPECT_EQ(center.b, 64);

    ColorRGB tip = pal->sample(1.0f);
    // Sakura tip is frost ivory (245, 250, 255)
    EXPECT_EQ(tip.r, 245);
    EXPECT_EQ(tip.g, 250);
    EXPECT_EQ(tip.b, 255);
}

TEST_CASE(Palettes, RainbowDynamicHue) {
    RainbowPalette rainbow(0.0f);
    ColorRGB c0 = rainbow.sample(0.0f); // Hue 0 (Red)
    EXPECT_EQ(c0.r, 255);
    EXPECT_EQ(c0.g, 0);
    EXPECT_EQ(c0.b, 0);

    rainbow.set_base_hue(120.0f);
    ColorRGB c_green = rainbow.sample(0.0f); // Hue 120 (Green)
    EXPECT_EQ(c_green.r, 0);
    EXPECT_EQ(c_green.g, 255);
    EXPECT_EQ(c_green.b, 0);
}
