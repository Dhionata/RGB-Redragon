#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/core/models/color_rgb.hpp"
#include "openrgb_flowers/core/models/color_hsv.hpp"
#include "openrgb_flowers/core/models/key_coordinate.hpp"
#include "openrgb_flowers/core/models/render_frame.hpp"

using namespace openrgb_flowers::core::models;

TEST_CASE(ColorModels, RGBHexConversion) {
    ColorRGB c1(255, 128, 64);
    EXPECT_EQ(c1.to_hex(), "#FF8040");

    ColorRGB c2 = ColorRGB::from_hex("#FF8040");
    EXPECT_EQ(c2.r, 255);
    EXPECT_EQ(c2.g, 128);
    EXPECT_EQ(c2.b, 64);

    ColorRGB c3 = ColorRGB::from_hex("04080C");
    EXPECT_EQ(c3.r, 4);
    EXPECT_EQ(c3.g, 8);
    EXPECT_EQ(c3.b, 12);
}

TEST_CASE(ColorModels, RGBNormalized) {
    ColorRGB c = ColorRGB::from_normalized(1.0f, 0.5f, 0.0f);
    EXPECT_EQ(c.r, 255);
    EXPECT_NEAR(c.g, 128, 1);
    EXPECT_EQ(c.b, 0);

    auto [rn, gn, bn] = c.to_normalized();
    EXPECT_NEAR(rn, 1.0f, 0.01f);
    EXPECT_NEAR(gn, 0.5f, 0.01f);
    EXPECT_NEAR(bn, 0.0f, 0.01f);
}

TEST_CASE(ColorModels, HSVToRGBRoundtrip) {
    ColorHSV red_hsv(0.0f, 1.0f, 1.0f);
    ColorRGB red_rgb = red_hsv.to_rgb();
    EXPECT_EQ(red_rgb.r, 255);
    EXPECT_EQ(red_rgb.g, 0);
    EXPECT_EQ(red_rgb.b, 0);

    ColorHSV roundtrip = ColorHSV::from_rgb(red_rgb);
    EXPECT_NEAR(roundtrip.h, 0.0f, 0.1f);
    EXPECT_NEAR(roundtrip.s, 1.0f, 0.01f);
    EXPECT_NEAR(roundtrip.v, 1.0f, 0.01f);

    ColorHSV green_hsv(120.0f, 1.0f, 1.0f);
    ColorRGB green_rgb = green_hsv.to_rgb();
    EXPECT_EQ(green_rgb.r, 0);
    EXPECT_EQ(green_rgb.g, 255);
    EXPECT_EQ(green_rgb.b, 0);
}

TEST_CASE(ColorModels, KeyCoordinateClamping) {
    KeyCoordinate k("Esc", 0, -0.5f, 1.5f, 0, 0);
    EXPECT_EQ(k.x, 0.0f);
    EXPECT_EQ(k.y, 1.0f);
}

TEST_CASE(ColorModels, RenderFrameBuffer) {
    std::vector<ColorRGB> buffer = {
        ColorRGB(255, 0, 0),
        ColorRGB(0, 255, 0),
        ColorRGB(0, 0, 255)
    };
    RenderFrame frame(1.5, 42, buffer);
    EXPECT_EQ(frame.led_count, 3);
    EXPECT_EQ(frame.raw_size(), 3 * sizeof(ColorRGB));
    EXPECT_EQ(frame.data()[0].r, 255);
    EXPECT_EQ(frame.data()[1].g, 255);
    EXPECT_EQ(frame.data()[2].b, 255);
}
