#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/math/fast_color.hpp"
#include "openrgb_flowers/math/easing.hpp"
#include "openrgb_flowers/math/spatial_grid.hpp"

using namespace openrgb_flowers::math;
using namespace openrgb_flowers::core::models;

TEST_CASE(Math, FastColorHSVtoRGB) {
    float r = 0, g = 0, b = 0;
    FastColorMath::hsv_to_rgb(0.0f, 1.0f, 1.0f, r, g, b);
    EXPECT_NEAR(r, 255.0f, 1.0f);
    EXPECT_NEAR(g, 0.0f, 1.0f);
    EXPECT_NEAR(b, 0.0f, 1.0f);

    FastColorMath::hsv_to_rgb(240.0f, 1.0f, 1.0f, r, g, b);
    EXPECT_NEAR(r, 0.0f, 1.0f);
    EXPECT_NEAR(g, 0.0f, 1.0f);
    EXPECT_NEAR(b, 255.0f, 1.0f);
}

TEST_CASE(Math, BrightnessGamma) {
    ColorRGB white(255, 255, 255);
    ColorRGB half = FastColorMath::apply_brightness_gamma(white, 0.5f, 1.0f, 1.0f);
    EXPECT_NEAR(half.r, 128, 2);
    EXPECT_NEAR(half.g, 128, 2);
    EXPECT_NEAR(half.b, 128, 2);

    ColorRGB zero = FastColorMath::apply_brightness_gamma(white, 0.0f, 1.0f, 1.0f);
    EXPECT_EQ(zero.r, 0);
    EXPECT_EQ(zero.g, 0);
    EXPECT_EQ(zero.b, 0);
}

TEST_CASE(Math, EasingFunctions) {
    EXPECT_EQ(EasingFunctions::smoothstep(0.0f, 1.0f, 0.0f), 0.0f);
    EXPECT_EQ(EasingFunctions::smoothstep(0.0f, 1.0f, 1.0f), 1.0f);
    EXPECT_NEAR(EasingFunctions::smoothstep(0.0f, 1.0f, 0.5f), 0.5f, 0.01f);

    EXPECT_NEAR(EasingFunctions::ease_out_cubic(0.0f), 0.0f, 0.01f);
    EXPECT_NEAR(EasingFunctions::ease_out_cubic(1.0f), 1.0f, 0.01f);

    // Harmonic lobes: at angle 0 with rotation 0, cos(0) == 1, factor is 1 + depth
    float h = EasingFunctions::petal_harmonic(0.0f, 5, 0.2f, 0.0f);
    EXPECT_NEAR(h, 1.2f, 0.01f);
}

TEST_CASE(Math, SpatialGridAspectCorrection) {
    SpatialGrid grid(3.7f);
    EXPECT_NEAR(grid.aspect_ratio(), 3.7f, 0.01f);

    auto [dx, dy, dist, angle] = grid.correct_aspect_ratio_single(0.6f, 0.5f, 0.5f, 0.5f);
    EXPECT_NEAR(dx, 0.1f * 3.7f, 0.001f);
    EXPECT_NEAR(dy, 0.0f, 0.001f);
    EXPECT_NEAR(dist, 0.37f, 0.001f);
}
