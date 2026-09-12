#include "openrgb_flowers/math/easing.hpp"

#include <algorithm>
#include <cmath>

namespace openrgb_flowers::math {

float EasingFunctions::smoothstep(float edge0, float edge1, float x) {
    float diff = edge1 - edge0;
    if (std::fabs(diff) < 1e-9f) {
        return (x >= edge1) ? 1.0f : 0.0f;
    }
    float t = std::clamp((x - edge0) / diff, 0.0f, 1.0f);
    return t * t * (3.0f - 2.0f * t);
}

float EasingFunctions::ease_out_cubic(float t) {
    float inv = 1.0f - std::clamp(t, 0.0f, 1.0f);
    return 1.0f - inv * inv * inv;
}

float EasingFunctions::ease_in_out_cubic(float t) {
    float clamped = std::clamp(t, 0.0f, 1.0f);
    if (clamped < 0.5f) {
        return 4.0f * clamped * clamped * clamped;
    }
    float f = -2.0f * clamped + 2.0f;
    return 1.0f - (f * f * f) / 2.0f;
}

float EasingFunctions::petal_harmonic(float angle, int lobes, float depth, float rotation) {
    return 1.0f + depth * std::cos(static_cast<float>(lobes) * angle + rotation);
}

} // namespace openrgb_flowers::math
