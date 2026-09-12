#include "openrgb_flowers/effects/random_blend_engine.hpp"
#include "openrgb_flowers/effects/palettes/palette_registry.hpp"
#include "openrgb_flowers/math/fast_color.hpp"

#include <algorithm>

namespace openrgb_flowers::effects {

RandomBlendEngine::RandomBlendEngine(
    core::models::EffectConfig config,
    std::shared_ptr<core::interfaces::ILayoutProvider> layout,
    std::shared_ptr<core::interfaces::IColorPalette> palette
) : config_(std::move(config)),
    layout_(std::move(layout)),
    palette_(palette ? std::move(palette) : palettes::PaletteRegistry::get(config_.palette_name)),
    led_count_(layout_->get_key_count()),
    rng_(std::random_device{}()) {
    initialize_keys();
}

const core::models::EffectConfig& RandomBlendEngine::get_config() const {
    return config_;
}

int RandomBlendEngine::get_active_flower_count() const {
    return static_cast<int>(led_count_);
}

void RandomBlendEngine::update_layout(std::shared_ptr<core::interfaces::ILayoutProvider> layout) {
    layout_ = std::move(layout);
    led_count_ = layout_->get_key_count();
    initialize_keys();
}

void RandomBlendEngine::update_config(const core::models::EffectConfig& config) {
    bool palette_changed = config.palette_name != config_.palette_name;
    config_ = config;
    if (palette_changed) {
        palette_ = palettes::PaletteRegistry::get(config_.palette_name);
        for (size_t i = 0; i < led_count_; ++i) {
            target_rgb_[i] = sample_palette_random();
        }
    }
}

void RandomBlendEngine::reset() {
    sim_time_ = 0.0f;
    frame_count_ = 0;
    initialize_keys();
}

core::models::ColorRGB RandomBlendEngine::sample_palette_random() {
    std::uniform_real_distribution<float> dist(0.0f, 1.0f);
    return palette_->sample(dist(rng_));
}

void RandomBlendEngine::initialize_keys() {
    current_rgb_.resize(led_count_);
    target_rgb_.resize(led_count_);
    progress_.resize(led_count_);
    transition_speeds_.resize(led_count_);
    blended_buffer_.resize(led_count_);
    output_buffer_.resize(led_count_);

    std::uniform_real_distribution<float> prog_dist(0.0f, 1.0f);
    std::uniform_real_distribution<float> speed_dist(0.6f, 2.2f);

    for (size_t i = 0; i < led_count_; ++i) {
        current_rgb_[i] = sample_palette_random();
        target_rgb_[i] = sample_palette_random();
        progress_[i] = prog_dist(rng_);
        transition_speeds_[i] = speed_dist(rng_);
    }
}

core::models::RenderFrame RandomBlendEngine::tick(float dt) {
    sim_time_ += dt;
    ++frame_count_;

    float speed_mult = std::max(0.05f, config_.speed);
    std::uniform_real_distribution<float> speed_dist(0.6f, 2.2f);

    for (size_t i = 0; i < led_count_; ++i) {
        progress_[i] += dt * transition_speeds_[i] * speed_mult;
        if (progress_[i] >= 1.0f) {
            current_rgb_[i] = target_rgb_[i];
            progress_[i] = std::max(0.0f, progress_[i] - 1.0f);
            target_rgb_[i] = sample_palette_random();
            transition_speeds_[i] = speed_dist(rng_);
        }

        // Hermite smoothstep cubic interpolation
        float t = std::clamp(progress_[i], 0.0f, 1.0f);
        float smooth_t = t * t * (3.0f - 2.0f * t);
        blended_buffer_[i] = math::FastColorMath::lerp(current_rgb_[i], target_rgb_[i], smooth_t);
    }

    // Apply brightness, gamma, and saturation
    math::FastColorMath::apply_brightness_gamma_buffer(
        blended_buffer_.data(),
        output_buffer_.data(),
        led_count_,
        config_.brightness,
        config_.gamma,
        config_.saturation
    );

    return core::models::RenderFrame(sim_time_, frame_count_, output_buffer_);
}

} // namespace openrgb_flowers::effects
