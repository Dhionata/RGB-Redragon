#pragma once

#include "openrgb_flowers/core/interfaces/i_effect_engine.hpp"
#include "openrgb_flowers/core/interfaces/i_frame_transmitter.hpp"
#include "openrgb_flowers/core/interfaces/i_layout_provider.hpp"
#include "openrgb_flowers/core/models/effect_config.hpp"

#include <atomic>
#include <cstdint>
#include <memory>
#include <mutex>
#include <optional>

namespace openrgb_flowers::service {

/**
 * @brief High-precision loop runner coordinating effect simulation and hardware transmission.
 */
class RunnerService {
public:
    RunnerService(
        std::shared_ptr<core::interfaces::IEffectEngine> engine,
        std::shared_ptr<core::interfaces::IFrameTransmitter> transmitter,
        std::shared_ptr<core::interfaces::ILayoutProvider> layout,
        core::models::EffectConfig config
    );

    void run(std::optional<uint64_t> max_frames = std::nullopt);
    void stop();
    [[nodiscard]] bool is_running() const;

    void set_engine(std::shared_ptr<core::interfaces::IEffectEngine> engine);
    void set_palette(const std::string& palette_name);
    void set_effect(const std::string& effect_name);
    void update_config(const core::models::EffectConfig& config);

private:
    std::shared_ptr<core::interfaces::IEffectEngine> engine_;
    std::shared_ptr<core::interfaces::IFrameTransmitter> transmitter_;
    std::shared_ptr<core::interfaces::ILayoutProvider> layout_;
    core::models::EffectConfig config_;

    std::atomic<bool> running_{false};
    mutable std::mutex mutex_;
};

} // namespace openrgb_flowers::service
