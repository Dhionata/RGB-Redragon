#include "tests/cpp/test_framework.hpp"
#include "openrgb_flowers/effects/blooming_engine.hpp"
#include "openrgb_flowers/effects/random_blend_engine.hpp"
#include "openrgb_flowers/effects/effect_engine_factory.hpp"
#include "openrgb_flowers/hardware/k556_matrix_layout_provider.hpp"
#include "openrgb_flowers/core/models/effect_config.hpp"

using namespace openrgb_flowers::effects;
using namespace openrgb_flowers::hardware;
using namespace openrgb_flowers::core::models;

TEST_CASE(Engines, BloomingEngineTick) {
    EffectConfig cfg;
    cfg.fps = 30.0f;
    cfg.speed = 1.0f;
    cfg.max_flowers = 3;
    cfg.spawn_rate = 1.0f;

    auto layout = std::make_shared<K556MatrixLayoutProvider>();
    BloomingEngine engine(cfg, layout);

    EXPECT_EQ(engine.get_active_flower_count(), 0);

    // First tick should immediately spawn first bloom
    auto frame1 = engine.tick(0.033f);
    EXPECT_EQ(frame1.led_count, 132);
    EXPECT_EQ(frame1.frame_index, 1);
    EXPECT_TRUE(engine.get_active_flower_count() >= 1);

    // Reset should clear flowers
    engine.reset();
    EXPECT_EQ(engine.get_active_flower_count(), 0);
}

TEST_CASE(Engines, RandomBlendEngineContinuousIllumination) {
    EffectConfig cfg;
    cfg.effect_type = "random_blend";
    cfg.palette_name = "rainbow";
    cfg.speed = 1.5f;

    auto layout = std::make_shared<K556MatrixLayoutProvider>();
    RandomBlendEngine engine(cfg, layout);

    EXPECT_EQ(engine.get_active_flower_count(), 132);

    auto frame = engine.tick(0.033f);
    EXPECT_EQ(frame.led_count, 132);

    // Verify 100% of keys have non-zero illumination in random blend mode
    int illuminated_count = 0;
    for (int i = 0; i < frame.led_count; ++i) {
        if (frame.data()[i].r > 0 || frame.data()[i].g > 0 || frame.data()[i].b > 0) {
            ++illuminated_count;
        }
    }
    EXPECT_EQ(illuminated_count, frame.led_count);
}

TEST_CASE(Engines, FactoryCreation) {
    EffectConfig cfg1;
    cfg1.effect_type = "blooming";
    auto layout = std::make_shared<K556MatrixLayoutProvider>();

    auto eng1 = EffectEngineFactory::create_engine("blooming", cfg1, layout);
    EXPECT_TRUE(eng1 != nullptr);

    auto eng2 = EffectEngineFactory::create_engine("random_blend", cfg1, layout);
    EXPECT_TRUE(eng2 != nullptr);
}

TEST_CASE(Engines, BloomingEngineLifecycleAndPruning) {
    EffectConfig cfg;
    cfg.fps = 30.0f;
    cfg.speed = 10.0f; // High speed so lifecycle completes quickly
    cfg.max_flowers = 2;
    cfg.spawn_rate = 0.5f;

    auto layout = std::make_shared<K556MatrixLayoutProvider>();
    BloomingEngine engine(cfg, layout);

    // Initial tick spawns first flower
    engine.tick(0.033f);
    EXPECT_GE(engine.get_active_flower_count(), 1);

    // Advance 5 seconds worth of sim time in steps
    for (int i = 0; i < 150; ++i) {
        auto frame = engine.tick(0.033f);
        EXPECT_EQ(frame.led_count, 132);
        EXPECT_LE(engine.get_active_flower_count(), cfg.max_flowers);
    }
}

TEST_CASE(Engines, BloomingEngineEmptyPetalsGracefulFallback) {
    EffectConfig cfg;
    cfg.petal_options.clear(); // Empty petal options
    auto layout = std::make_shared<K556MatrixLayoutProvider>();
    BloomingEngine engine(cfg, layout);

    // Ticking should not crash or throw out-of-bounds error
    auto frame = engine.tick(0.033f);
    EXPECT_EQ(frame.led_count, 132);
    EXPECT_GE(engine.get_active_flower_count(), 1);
}

