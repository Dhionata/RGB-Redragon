#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/effects/blending/organic_weighted_blend.hpp"
#include "openrgb_flowers/effects/blending/additive_blend.hpp"
#include "openrgb_flowers/effects/blending/screen_blend.hpp"

using namespace openrgb_flowers::effects::blending;
using namespace openrgb_flowers::core::models;

TEST_CASE(Blending, OrganicWeightedEmptyLayers) {
    OrganicWeightedBlend blender;
    ColorRGB base[2] = {ColorRGB(10, 20, 30), ColorRGB(40, 50, 60)};
    ColorRGB out[2];

    std::vector<std::vector<ColorRGB>> colors;
    std::vector<std::vector<float>> intensities;
    blender.blend_layers(base, colors, intensities, out, 2);

    EXPECT_EQ(out[0].r, 10);
    EXPECT_EQ(out[0].g, 20);
    EXPECT_EQ(out[0].b, 30);
    EXPECT_EQ(out[1].r, 40);
    EXPECT_EQ(out[1].g, 50);
    EXPECT_EQ(out[1].b, 60);
}

TEST_CASE(Blending, OrganicWeightedMix) {
    OrganicWeightedBlend blender;
    ColorRGB base[1] = {ColorRGB(0, 0, 0)};
    ColorRGB out[1];

    std::vector<std::vector<ColorRGB>> colors = {
        {ColorRGB(255, 0, 0)},
        {ColorRGB(0, 255, 0)}
    };
    std::vector<std::vector<float>> intensities = {
        {1.0f},
        {1.0f}
    };

    blender.blend_layers(base, colors, intensities, out, 1);
    // Equal 50/50 mix of Red and Green with full alpha gives Yellow (128, 128, 0)
    EXPECT_NEAR(out[0].r, 128, 2);
    EXPECT_NEAR(out[0].g, 128, 2);
    EXPECT_EQ(out[0].b, 0);
}

TEST_CASE(Blending, AdditiveBlendMode) {
    AdditiveBlend blender;
    ColorRGB base[1] = {ColorRGB(50, 50, 50)};
    ColorRGB out[1];

    std::vector<std::vector<ColorRGB>> colors = {
        {ColorRGB(100, 150, 200)}
    };
    std::vector<std::vector<float>> intensities = {
        {1.0f}
    };

    blender.blend_layers(base, colors, intensities, out, 1);
    EXPECT_EQ(out[0].r, 150);
    EXPECT_EQ(out[0].g, 200);
    EXPECT_EQ(out[0].b, 250);
}

TEST_CASE(Blending, ScreenBlendMode) {
    ScreenBlend blender;
    EXPECT_EQ(blender.get_name(), "screen");

    // Base color: 128 (approx 0.502 normalized)
    // Layer color: 128 with intensity 1.0 (approx 0.502)
    // Screen formula: 1 - (1 - 0.502) * (1 - 0.502) = 1 - 0.248 = 0.752 -> ~192
    ColorRGB base[1] = {ColorRGB(128, 0, 0)};
    ColorRGB out[1];

    std::vector<std::vector<ColorRGB>> colors = {
        {ColorRGB(128, 0, 0)}
    };
    std::vector<std::vector<float>> intensities = {
        {1.0f}
    };

    blender.blend_layers(base, colors, intensities, out, 1);
    EXPECT_NEAR(out[0].r, 192, 2);
    EXPECT_EQ(out[0].g, 0);
    EXPECT_EQ(out[0].b, 0);
}
