#include "openrgb_flowers/effects/effect_engine_factory.hpp"
#include "openrgb_flowers/effects/blooming_engine.hpp"
#include "openrgb_flowers/effects/random_blend_engine.hpp"

#include <algorithm>
#include <cctype>

namespace openrgb_flowers::effects {

namespace {

std::string to_lower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c) {
        return static_cast<char>(std::tolower(c));
    });
    return s;
}

} // anonymous namespace

std::unique_ptr<core::interfaces::IEffectEngine> EffectEngineFactory::create_engine(
    const std::string& effect_name,
    core::models::EffectConfig config,
    std::shared_ptr<core::interfaces::ILayoutProvider> layout,
    std::shared_ptr<core::interfaces::IColorPalette> palette,
    std::shared_ptr<core::interfaces::IBlendStrategy> blend
) {
    std::string key = to_lower(effect_name);
    if (key == "random_blend" || key == "random" || key == "blend" || key == "mosaic") {
        return std::make_unique<RandomBlendEngine>(std::move(config), std::move(layout), std::move(palette));
    }
    return std::make_unique<BloomingEngine>(
        std::move(config), std::move(layout), std::move(palette), std::move(blend)
    );
}

} // namespace openrgb_flowers::effects
