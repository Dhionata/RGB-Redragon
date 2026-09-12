#pragma once

#include "openrgb_flowers/core/models/effect_config.hpp"
#include "openrgb_flowers/core/models/render_frame.hpp"
#include "openrgb_flowers/core/interfaces/i_layout_provider.hpp"
#include <memory>

namespace openrgb_flowers::core::interfaces {

/**
 * @brief Interface contract for real-time floral lighting simulation engines.
 */
class IEffectEngine {
public:
    virtual ~IEffectEngine() = default;

    virtual models::RenderFrame tick(float dt) = 0;
    virtual void update_config(const models::EffectConfig& config) = 0;
    virtual void update_layout(std::shared_ptr<ILayoutProvider> layout) = 0;
    virtual void reset() = 0;
    [[nodiscard]] virtual int get_active_flower_count() const = 0;
    [[nodiscard]] virtual const models::EffectConfig& get_config() const = 0;
};

} // namespace openrgb_flowers::core::interfaces
