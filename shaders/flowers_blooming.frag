/*
 * OpenRGB Effects Plugin - Flowers Blooming Shader
 *
 * An organic floral blooming effect for RGB keyboards and devices.
 * Multiple flowers sprout, open harmonic petal lobes, radiate vivid botanical
 * gradients, and dissolve smoothly into a gentle meadow breeze.
 *
 * Compatible with OpenRGB Effects Plugin -> Shaders.
 */

#ifdef GL_ES
precision mediump float;
#endif

uniform float time;
uniform vec2 resolution;

// Organic pseudo-random hash
vec2 hash2(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
    return fract(sin(p) * 43758.5453123);
}

// Cubic smoothstep
float smoothCurve(float edge0, float edge1, float x) {
    float t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
    return t * t * (3.0 - 2.0 * t);
}

// Single flower bloom evaluation
vec4 evaluateBloom(vec2 uv, vec2 center, float seed, float globalTime) {
    // Spatial distance with aspect-ratio correction
    vec2 delta = uv - center;
    float dist = length(delta);
    float angle = atan(delta.y, delta.x);

    // Staggered bloom lifecycle (4.0 second cycle per flower seed)
    float cyclePeriod = 4.0;
    float localTime = mod(globalTime + seed * 5.731, cyclePeriod);
    float progress = localTime / cyclePeriod;

    // Petal harmonics: 4, 5, 6, or 8 petals based on seed
    float petalCount = 4.0 + floor(fract(seed * 17.31) * 4.0);
    float rotation = seed * 6.28318;
    float petalDepth = 0.22 + fract(seed * 3.14) * 0.1;

    // Radius expansion with cubic ease-out
    float growthT = min(1.0, progress / 0.65);
    float maxRadius = 0.35 + fract(seed * 7.19) * 0.15;
    float currentRadius = maxRadius * (1.0 - pow(1.0 - growthT, 3.0));

    // Petal boundary: R(theta) = R_0 * (1 + alpha * cos(k * theta + phi))
    float boundary = currentRadius * (1.0 + petalDepth * cos(petalCount * angle + rotation));

    // Edge falloff
    float falloff = 1.0 - smoothCurve(boundary * 0.75, boundary * 1.1, dist);

    // Temporal lifecycle intensity envelope
    float envelope = 0.0;
    if (progress < 0.2) {
        envelope = smoothCurve(0.0, 0.2, progress);
    } else if (progress < 0.65) {
        envelope = 1.0;
    } else {
        envelope = 1.0 - smoothCurve(0.65, 1.0, progress);
    }

    float intensity = falloff * envelope;
    if (intensity <= 0.001) {
        return vec4(0.0);
    }

    // Floral gradient: Stamen Gold -> Vibrant Sakura Pink -> Ivory Rim
    float gradPos = clamp(dist / max(0.001, boundary), 0.0, 1.0);
    vec3 stamenColor = vec3(1.0, 0.84, 0.25);
    vec3 petalColor  = vec3(1.0, 0.35, 0.65);
    vec3 tipColor    = vec3(0.98, 0.95, 1.0);

    vec3 bloomColor;
    if (gradPos < 0.25) {
        bloomColor = mix(stamenColor, petalColor, gradPos / 0.25);
    } else {
        bloomColor = mix(petalColor, tipColor, (gradPos - 0.25) / 0.75);
    }

    return vec4(bloomColor, intensity);
}

void main() {
    // Normalize coordinates in [0.0, 1.0] with keyboard aspect ratio (approx 3.7:1)
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    vec2 correctedUV = vec2(uv.x * (resolution.x / resolution.y), uv.y);

    // Ambient background meadow: gentle emerald dark slate breeze
    float breeze = sin(uv.x * 4.0 + time * 0.7) * 0.5 + 0.5;
    vec3 baseColor = mix(vec3(0.02, 0.03, 0.05), vec3(0.03, 0.07, 0.05), breeze);

    // Accumulate concurrent blooming flowers
    vec3 accumColor = vec3(0.0);
    float totalWeight = 0.0;
    float maxAlpha = 0.0;

    // 5 active flower bloom seeds positioned across keyboard
    for (int i = 0; i < 5; i++) {
        float seed = float(i) * 1.371 + 0.5;
        vec2 rawCenter = hash2(vec2(seed, seed * 2.31));
        vec2 normCenter = vec2(0.1 + rawCenter.x * 0.8, 0.15 + rawCenter.y * 0.7);
        vec2 correctedCenter = vec2(normCenter.x * (resolution.x / resolution.y), normCenter.y);

        vec4 flower = evaluateBloom(correctedUV, correctedCenter, seed, time * 0.85);
        if (flower.a > 0.0) {
            accumColor += flower.rgb * flower.a;
            totalWeight += flower.a;
            maxAlpha = max(maxAlpha, flower.a);
        }
    }

    vec3 finalColor = baseColor;
    if (totalWeight > 0.001) {
        vec3 floralMix = accumColor / totalWeight;
        finalColor = mix(baseColor, floralMix, clamp(maxAlpha, 0.0, 1.0));
    }

    gl_FragColor = vec4(finalColor, 1.0);
}
