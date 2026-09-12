#pragma once

#include "openrgb_flowers/core/interfaces/i_effect_engine.hpp"
#include "openrgb_flowers/core/interfaces/i_color_palette.hpp"
#include "openrgb_flowers/core/interfaces/i_blend_strategy.hpp"
#include "openrgb_flowers/core/interfaces/i_layout_provider.hpp"
#include "openrgb_flowers/effects/flower_instance.hpp"
#include "openrgb_flowers/math/spatial_grid.hpp"

#include <memory>
#include <random>
#include <vector>

namespace openrgb_flowers::effects {

/**
 * @brief High-performance floral blooming simulation engine orchestrating concurrent blooming flowers.
 */
class BloomingEngine : public core::interfaces::IEffectEngine {
public:
    BloomingEngine(
        core::models::EffectConfig config,
        std::shared_ptr<core::interfaces::ILayoutProvider> layout,
        std::shared_ptr<core::interfaces::IColorPalette> palette = nullptr,
        std::shared_ptr<core::interfaces::IBlendStrategy> blend = nullptr,
        math::SpatialGrid grid = math::SpatialGrid()
    );

    core::models::RenderFrame tick(float dt) override;
    void update_config(const core::models::EffectConfig& config) override;
    void update_layout(std::shared_ptr<core::interfaces::ILayoutProvider> layout) override;
    void reset() override;
    [[nodiscard]] int get_active_flower_count() const override;
    [[nodiscard]] const core::models::EffectConfig& get_config() const override;

private:
    [[nodiscard]] bool should_spawn_flower(float dt);
    void spawn_flower();
    std::pair<float, float> generate_flower_position();
    void compute_ambient_background(std::vector<core::models::ColorRGB>& out_bg) const;

    core::models::EffectConfig config_;
    std::shared_ptr<core::interfaces::ILayoutProvider> layout_;
    std::shared_ptr<core::interfaces::IColorPalette> palette_;
    std::shared_ptr<core::interfaces::IBlendStrategy> blend_strategy_;
    math::SpatialGrid grid_;

    std::vector<FlowerInstance> flowers_;
    uint64_t frame_count_{0};
    float sim_time_{0.0f};
    float spawn_accumulator_{0.0f};

    // Pre-allocated scratch buffers for zero-allocation rendering ticks
    std::vector<core::models::ColorRGB> bg_colors_;
    std::vector<core::models::ColorRGB> blended_;
    std::vector<core::models::ColorRGB> final_frame_;
    std::vector<std::vector<core::models::ColorRGB>> layer_colors_;
    std::vector<std::vector<float>> layer_intensities_;

    std::mt19937 rng_{1337};
};

} // namespace openrgb_flowers::effects
