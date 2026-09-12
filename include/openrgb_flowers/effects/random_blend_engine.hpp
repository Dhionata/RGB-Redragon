#pragma once

#include "openrgb_flowers/core/interfaces/i_effect_engine.hpp"
#include "openrgb_flowers/core/interfaces/i_color_palette.hpp"
#include "openrgb_flowers/core/interfaces/i_layout_provider.hpp"
#include "openrgb_flowers/core/models/effect_config.hpp"

#include <memory>
#include <random>
#include <vector>

namespace openrgb_flowers::effects {

/**
 * @brief High-performance engine where 100% of keys remain brightly illuminated while smoothly
 * and independently transitioning through randomized, organic mixed colors.
 */
class RandomBlendEngine : public core::interfaces::IEffectEngine {
public:
    RandomBlendEngine(
        core::models::EffectConfig config,
        std::shared_ptr<core::interfaces::ILayoutProvider> layout,
        std::shared_ptr<core::interfaces::IColorPalette> palette = nullptr
    );

    core::models::RenderFrame tick(float dt) override;
    void update_config(const core::models::EffectConfig& config) override;
    void update_layout(std::shared_ptr<core::interfaces::ILayoutProvider> layout) override;
    void reset() override;
    [[nodiscard]] int get_active_flower_count() const override;
    [[nodiscard]] const core::models::EffectConfig& get_config() const override;

private:
    void initialize_keys();
    core::models::ColorRGB sample_palette_random();

    core::models::EffectConfig config_;
    std::shared_ptr<core::interfaces::ILayoutProvider> layout_;
    std::shared_ptr<core::interfaces::IColorPalette> palette_;

    size_t led_count_{0};
    uint64_t frame_count_{0};
    float sim_time_{0.0f};

    // Pre-allocated per-key state vectors (zero allocations per tick)
    std::vector<core::models::ColorRGB> current_rgb_;
    std::vector<core::models::ColorRGB> target_rgb_;
    std::vector<float> progress_;
    std::vector<float> transition_speeds_;
    std::vector<core::models::ColorRGB> blended_buffer_;
    std::vector<core::models::ColorRGB> output_buffer_;

    std::mt19937 rng_{42};
};

} // namespace openrgb_flowers::effects
