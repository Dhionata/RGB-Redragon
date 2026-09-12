#pragma once

namespace openrgb_flowers::math {

/**
 * @brief Smooth easing and harmonic mathematical functions for organic natural animations.
 */
class EasingFunctions {
public:
    static float smoothstep(float edge0, float edge1, float x);
    static float ease_out_cubic(float t);
    static float ease_in_out_cubic(float t);
    static float petal_harmonic(float angle, int lobes, float depth, float rotation);
};

} // namespace openrgb_flowers::math
