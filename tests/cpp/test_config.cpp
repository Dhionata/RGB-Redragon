#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/core/models/effect_config.hpp"
#include "openrgb_flowers/core/json_helper.hpp"

using namespace openrgb_flowers::core::models;

TEST_CASE(Config, ValidationDefaults) {
    EffectConfig cfg;
    EXPECT_TRUE(cfg.fps >= 1.0f && cfg.fps <= 120.0f);
    cfg.validate(); // Should not throw
}

TEST_CASE(Config, ValidationInvalidFPS) {
    EffectConfig cfg;
    cfg.fps = 0.0f;
    EXPECT_THROW(cfg.validate(), std::invalid_argument);
}

TEST_CASE(Config, ValidationInvalidSpeed) {
    EffectConfig cfg;
    cfg.speed = -1.0f;
    EXPECT_THROW(cfg.validate(), std::invalid_argument);
}

TEST_CASE(Config, ValidationInvalidEffectType) {
    EffectConfig cfg;
    cfg.effect_type = "invalid_effect";
    EXPECT_THROW(cfg.validate(), std::invalid_argument);
}

TEST_CASE(Config, ValidationInvalidBlendMode) {
    EffectConfig cfg;
    cfg.blend_mode = "invalid_blend";
    EXPECT_THROW(cfg.validate(), std::invalid_argument);
}

TEST_CASE(Config, JsonRoundtrip) {
    EffectConfig cfg;
    cfg.effect_type = "random_blend";
    cfg.palette_name = "cyberpunk";
    cfg.speed = 2.5f;
    cfg.brightness = 0.8f;
    cfg.ambient_pulse = false;
    cfg.petal_options = {5, 6, 7};

    std::string json_str = cfg.to_json(2);
    EXPECT_FALSE(json_str.empty());

    EffectConfig parsed = EffectConfig::from_json(json_str);
    EXPECT_EQ(parsed.effect_type, "random_blend");
    EXPECT_EQ(parsed.palette_name, "cyberpunk");
    EXPECT_NEAR(parsed.speed, 2.5f, 0.01f);
    EXPECT_NEAR(parsed.brightness, 0.8f, 0.01f);
    EXPECT_FALSE(parsed.ambient_pulse);
    EXPECT_EQ(parsed.petal_options.size(), 3);
    EXPECT_EQ(parsed.petal_options[0], 5);
    EXPECT_EQ(parsed.petal_options[1], 6);
    EXPECT_EQ(parsed.petal_options[2], 7);
}

TEST_CASE(Config, JsonSpecialCharactersEscaping) {
    using namespace openrgb_flowers::core;
    JsonObject obj;
    obj["windows_path"] = JsonValue("C:\\Users\\test\\folder\\config.json");
    obj["quote_text"] = JsonValue("Flowers \"Blooming\" Special");
    obj["newline_text"] = JsonValue("Line 1\nLine 2\tTabbed");

    std::string serialized = JsonValue(obj).serialize(2);
    JsonValue parsed = JsonValue::parse(serialized);

    EXPECT_TRUE(parsed.is_object());
    EXPECT_EQ(parsed.get("windows_path").as_string(), "C:\\Users\\test\\folder\\config.json");
    EXPECT_EQ(parsed.get("quote_text").as_string(), "Flowers \"Blooming\" Special");
    EXPECT_EQ(parsed.get("newline_text").as_string(), "Line 1\nLine 2\tTabbed");
}

TEST_CASE(Config, JsonUnicodeEscapeAndControlChars) {
    using namespace openrgb_flowers::core;

    // Test unicode escape sequence decoding \u0041 ('A')
    std::string json_unicode = "{\"unicode_val\": \"Hello \\u0041\\u0042\\u0043\"}";
    JsonValue parsed = JsonValue::parse(json_unicode);
    EXPECT_EQ(parsed.get("unicode_val").as_string(), "Hello ABC");

    // Test control characters round-trip via \u00XX escaping
    JsonObject obj;
    obj["ctrl"] = JsonValue(std::string("Escape\x1b[31mRed\x1b[0m"));
    std::string serialized = JsonValue(obj).serialize(0);
    JsonValue parsed2 = JsonValue::parse(serialized);
    EXPECT_EQ(parsed2.get("ctrl").as_string(), "Escape\x1b[31mRed\x1b[0m");

    // Test invalid number throwing
    EXPECT_THROW(JsonValue::parse("{\"num\": -}"), std::runtime_error);
}
