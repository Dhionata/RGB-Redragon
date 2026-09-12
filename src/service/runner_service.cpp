#include "openrgb_flowers/service/runner_service.hpp"
#include "openrgb_flowers/effects/effect_engine_factory.hpp"

#include <algorithm>
#include <chrono>
#include <csignal>
#include <iostream>
#include <thread>

namespace openrgb_flowers::service {

namespace {

static std::atomic<RunnerService*> s_active_instance{nullptr};

void signal_handler(int sig) {
    (void)sig;
    if (auto* inst = s_active_instance.load()) {
        inst->stop();
    }
}

} // anonymous namespace

RunnerService::RunnerService(
    std::shared_ptr<core::interfaces::IEffectEngine> engine,
    std::shared_ptr<core::interfaces::IFrameTransmitter> transmitter,
    std::shared_ptr<core::interfaces::ILayoutProvider> layout,
    core::models::EffectConfig config
) : engine_(std::move(engine)),
    transmitter_(std::move(transmitter)),
    layout_(std::move(layout)),
    config_(std::move(config)) {}

void RunnerService::stop() {
    running_ = false;
}

bool RunnerService::is_running() const {
    return running_;
}

void RunnerService::set_engine(std::shared_ptr<core::interfaces::IEffectEngine> engine) {
    std::lock_guard<std::mutex> lock(mutex_);
    engine_ = std::move(engine);
}

void RunnerService::set_palette(const std::string& palette_name) {
    std::lock_guard<std::mutex> lock(mutex_);
    config_.palette_name = palette_name;
    if (engine_) {
        engine_->update_config(config_);
    }
}

void RunnerService::set_effect(const std::string& effect_name) {
    std::lock_guard<std::mutex> lock(mutex_);
    config_.effect_type = effect_name;
    engine_ = effects::EffectEngineFactory::create_engine(effect_name, config_, layout_);
}

void RunnerService::update_config(const core::models::EffectConfig& config) {
    std::lock_guard<std::mutex> lock(mutex_);
    bool effect_changed = (config.effect_type != config_.effect_type);
    config_ = config;
    if (effect_changed) {
        engine_ = effects::EffectEngineFactory::create_engine(config_.effect_type, config_, layout_);
    } else if (engine_) {
        engine_->update_config(config_);
    }
}

void RunnerService::run(std::optional<uint64_t> max_frames) {
    running_ = true;
    s_active_instance.store(this);
    std::signal(SIGINT, signal_handler);
    std::signal(SIGTERM, signal_handler);

    if (!transmitter_->is_connected()) {
        transmitter_->connect();
    }

    auto prev_time = std::chrono::steady_clock::now();
    uint64_t frames_rendered = 0;

    while (running_) {
        auto loop_start = std::chrono::steady_clock::now();
        std::chrono::duration<float> dt_duration = loop_start - prev_time;
        prev_time = loop_start;

        float dt = dt_duration.count();
        float dt_clamped = std::clamp(dt, 0.001f, 0.1f);

        core::models::RenderFrame frame;
        float current_fps = 30.0f;
        {
            std::lock_guard<std::mutex> lock(mutex_);
            if (engine_) {
                frame = engine_->tick(dt_clamped);
            }
            current_fps = config_.fps;
        }

        if (frame.led_count > 0) {
            transmitter_->send_frame(frame);
        }

        ++frames_rendered;
        if (max_frames.has_value() && frames_rendered >= max_frames.value()) {
            break;
        }

        auto frame_duration = std::chrono::duration<double>(1.0 / std::max(1.0f, current_fps));
        auto elapsed = std::chrono::steady_clock::now() - loop_start;
        auto sleep_time = frame_duration - elapsed;
        if (sleep_time > std::chrono::duration<double>::zero()) {
            std::this_thread::sleep_for(sleep_time);
        }
    }

    transmitter_->disconnect();
    s_active_instance.store(nullptr);
}

} // namespace openrgb_flowers::service
