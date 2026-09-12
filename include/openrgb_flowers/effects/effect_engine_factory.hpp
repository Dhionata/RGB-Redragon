#pragma once

#include "openrgb_flowers/core/interfaces/i_effect_engine.hpp"
#include "openrgb_flowers/core/interfaces/i_layout_provider.hpp"
#include "openrgb_flowers/core/interfaces/i_color_palette.hpp"
#include "openrgb_flowers/core/interfaces/i_blend_strategy.hpp"
#include "openrgb_flowers/core/models/effect_config.hpp"

#include <memory>
#include <string>

namespace openrgb_flowers::effects {

/**
 * @brief Factory creating effect engines based on configuration.
 */
class EffectEngineFactory {
public:
    static std::unique_ptr<core::interfaces::IEffectEngine> create_engine(
        const std::string& effect_name,
        core::models::EffectConfig config,
        std::shared_ptr<core::interfaces::ILayoutProvider> layout,
        std::shared_ptr<core::interfaces::IColorPalette> palette = nullptr,
        std::shared_ptr<core::interfaces::IBlendStrategy> blend = nullptr
    );
};

} // namespace openrgb_flowers::effects
