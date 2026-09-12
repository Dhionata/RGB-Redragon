#include "openrgb_flowers/effects/blooming_engine.hpp"
#include "openrgb_flowers/effects/palettes/palette_registry.hpp"
#include "openrgb_flowers/effects/palettes/rainbow_palette.hpp"
#include "openrgb_flowers/effects/blending/organic_weighted_blend.hpp"
#include "openrgb_flowers/effects/blending/additive_blend.hpp"
#include "openrgb_flowers/effects/blending/screen_blend.hpp"
#include "openrgb_flowers/math/fast_color.hpp"

#include <algorithm>
#include <cmath>
#include <numbers>

namespace openrgb_flowers::effects {

namespace {

std::shared_ptr<core::interfaces::IBlendStrategy> resolve_blend(const std::string& name) {
    if (name == "additive") return std::make_shared<blending::AdditiveBlend>();
    if (name == "screen") return std::make_shared<blending::ScreenBlend>();
    return std::make_shared<blending::OrganicWeightedBlend>();
}

} // anonymous namespace

BloomingEngine::BloomingEngine(
    core::models::EffectConfig config,
    std::shared_ptr<core::interfaces::ILayoutProvider> layout,
    std::shared_ptr<core::interfaces::IColorPalette> palette,
    std::shared_ptr<core::interfaces::IBlendStrategy> blend,
    math::SpatialGrid grid
) : config_(std::move(config)),
    layout_(std::move(layout)),
    palette_(palette ? std::move(palette) : palettes::PaletteRegistry::get(config_.palette_name)),
    blend_strategy_(blend ? std::move(blend) : resolve_blend(config_.blend_mode)),
    grid_(grid),
    rng_(std::random_device{}()) {}

const core::models::EffectConfig& BloomingEngine::get_config() const {
    return config_;
}

int BloomingEngine::get_active_flower_count() const {
    return static_cast<int>(flowers_.size());
}

void BloomingEngine::update_layout(std::shared_ptr<core::interfaces::ILayoutProvider> layout) {
    layout_ = std::move(layout);
}

void BloomingEngine::update_config(const core::models::EffectConfig& config) {
    bool palette_changed = config.palette_name != config_.palette_name;
    bool blend_changed = config.blend_mode != config_.blend_mode;

    config_ = config;

    if (palette_changed) {
        palette_ = palettes::PaletteRegistry::get(config_.palette_name);
    }
    if (blend_changed) {
        blend_strategy_ = resolve_blend(config_.blend_mode);
    }
}

void BloomingEngine::reset() {
    flowers_.clear();
    frame_count_ = 0;
    sim_time_ = 0.0f;
    spawn_accumulator_ = 0.0f;
}

bool BloomingEngine::should_spawn_flower(float dt) {
    if (static_cast<int>(flowers_.size()) >= config_.max_flowers) {
        return false;
    }
    if (flowers_.empty()) {
        return true;
    }
    spawn_accumulator_ += dt * config_.spawn_rate * config_.speed;
    if (spawn_accumulator_ >= 1.0f) {
        spawn_accumulator_ -= 1.0f;
        return true;
    }
    return false;
}

std::pair<float, float> BloomingEngine::generate_flower_position() {
    std::uniform_real_distribution<float> dist_x(0.08f, 0.92f);
    std::uniform_real_distribution<float> dist_y(0.12f, 0.88f);

    float best_x = dist_x(rng_);
    float best_y = dist_y(rng_);

    if (!flowers_.empty()) {
        float max_min_dist = -1.0f;
        for (int i = 0; i < 5; ++i) {
            float cand_x = dist_x(rng_);
            float cand_y = dist_y(rng_);
            float min_d = 1000.0f;
            for (const auto& f : flowers_) {
                auto [cx, cy] = f.get_center();
                float d = std::hypot(cand_x - cx, cand_y - cy);
                if (d < min_d) {
                    min_d = d;
                }
            }
            if (min_d > max_min_dist) {
                max_min_dist = min_d;
                best_x = cand_x;
                best_y = cand_y;
            }
        }
    }
    return {best_x, best_y};
}

void BloomingEngine::spawn_flower() {
    auto [cx, cy] = generate_flower_position();

    int petal_count = 5;
    if (!config_.petal_options.empty()) {
        std::uniform_int_distribution<size_t> petal_dist(0, config_.petal_options.size() - 1);
        petal_count = config_.petal_options[petal_dist(rng_)];
    }

    std::uniform_real_distribution<float> rot_dist(0.0f, 2.0f * std::numbers::pi_v<float>);
    float rotation = rot_dist(rng_);

    std::uniform_real_distribution<float> life_dist(2.8f, 4.4f);
    float lifespan = life_dist(rng_) / config_.speed;

    std::uniform_real_distribution<float> rad_dist(0.35f, 0.52f);
    float max_radius = rad_dist(rng_);

    std::uniform_real_distribution<float> depth_dist(0.18f, 0.28f);
    float petal_depth = depth_dist(rng_);

    std::shared_ptr<core::interfaces::IColorPalette> flower_palette = palette_;
    if (config_.palette_name == "rainbow") {
        std::uniform_real_distribution<float> hue_dist(0.0f, 360.0f);
        flower_palette = std::make_shared<palettes::RainbowPalette>(hue_dist(rng_));
    }

    flowers_.emplace_back(
        cx, cy, flower_palette, petal_count, max_radius, lifespan, rotation, petal_depth, grid_
    );
}

void BloomingEngine::compute_ambient_background(std::vector<core::models::ColorRGB>& out_bg) const {
    size_t key_count = layout_->get_key_count();
    out_bg.resize(key_count);

    if (!config_.ambient_pulse) {
        std::fill(out_bg.begin(), out_bg.end(), config_.background_color);
        return;
    }

    const float* x_coords = layout_->get_x_coords();
    float phase = sim_time_ * 0.8f;
    float bg_r = static_cast<float>(config_.background_color.r);
    float bg_g = static_cast<float>(config_.background_color.g);
    float bg_b = static_cast<float>(config_.background_color.b);

    for (size_t i = 0; i < key_count; ++i) {
        float wave = std::sin(x_coords[i] * 3.0f + phase) * 0.5f + 0.5f;
        float factor = wave * 0.5f;
        uint8_t r = static_cast<uint8_t>(std::clamp(std::round(bg_r + 6.0f * factor), 0.0f, 255.0f));
        uint8_t g = static_cast<uint8_t>(std::clamp(std::round(bg_g + 14.0f * factor), 0.0f, 255.0f));
        uint8_t b = static_cast<uint8_t>(std::clamp(std::round(bg_b + 10.0f * factor), 0.0f, 255.0f));
        out_bg[i] = core::models::ColorRGB(r, g, b);
    }
}

core::models::RenderFrame BloomingEngine::tick(float dt) {
    sim_time_ += dt;
    ++frame_count_;

    // 1. Advance flower lifecycle and purge finished in-place
    std::erase_if(flowers_, [dt_speed = dt * config_.speed](FlowerInstance& f) {
        return !f.update(dt_speed);
    });

    // 2. Spawn new flower if needed
    if (should_spawn_flower(dt)) {
        spawn_flower();
    }

    size_t key_count = layout_->get_key_count();
    const float* x_coords = layout_->get_x_coords();
    const float* y_coords = layout_->get_y_coords();

    // 3. Ambient background
    compute_ambient_background(bg_colors_);

    // 4. Evaluate each active bloom layer
    size_t num_flowers = flowers_.size();
    layer_colors_.resize(num_flowers);
    layer_intensities_.resize(num_flowers);
    for (size_t l = 0; l < num_flowers; ++l) {
        if (layer_colors_[l].size() != key_count) {
            layer_colors_[l].resize(key_count);
            layer_intensities_[l].resize(key_count);
        }
        flowers_[l].evaluate(
            x_coords, y_coords,
            layer_intensities_[l].data(),
            layer_colors_[l].data(),
            key_count
        );
    }

    // 5. Blend layers
    if (blended_.size() != key_count) {
        blended_.resize(key_count);
    }
    blend_strategy_->blend_layers(
        bg_colors_.data(),
        layer_colors_,
        layer_intensities_,
        blended_.data(),
        key_count
    );

    // 6. Post-processing (brightness, saturation, gamma)
    if (final_frame_.size() != key_count) {
        final_frame_.resize(key_count);
    }
    math::FastColorMath::apply_brightness_gamma_buffer(
        blended_.data(),
        final_frame_.data(),
        key_count,
        config_.brightness,
        config_.gamma,
        config_.saturation
    );

    return core::models::RenderFrame(sim_time_, frame_count_, final_frame_);
}

} // namespace openrgb_flowers::effects
