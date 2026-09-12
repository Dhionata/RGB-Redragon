#include "openrgb_flowers/effects/palettes/base_palette.hpp"
#include "openrgb_flowers/math/fast_color.hpp"

#include <algorithm>

namespace openrgb_flowers::effects::palettes {

BaseColorPalette::BaseColorPalette(std::string name, std::vector<std::pair<float, core::models::ColorRGB>> stops)
    : name_(std::move(name)), stops_(std::move(stops)) {
    std::sort(stops_.begin(), stops_.end(), [](const auto& a, const auto& b) {
        return a.first < b.first;
    });
}

std::string BaseColorPalette::get_name() const {
    return name_;
}

core::models::ColorRGB BaseColorPalette::sample(float t) const {
    if (stops_.empty()) {
        return core::models::ColorRGB(0, 0, 0);
    }
    float t_clamped = std::clamp(t, 0.0f, 1.0f);
    if (t_clamped <= stops_.front().first) {
        return stops_.front().second;
    }
    if (t_clamped >= stops_.back().first) {
        return stops_.back().second;
    }

    // Binary search for interval
    for (size_t i = 1; i < stops_.size(); ++i) {
        if (t_clamped <= stops_[i].first) {
            float p0 = stops_[i - 1].first;
            float p1 = stops_[i].first;
            float factor = (t_clamped - p0) / (p1 - p0 + 1e-7f);
            return math::FastColorMath::lerp(stops_[i - 1].second, stops_[i].second, factor);
        }
    }

    return stops_.back().second;
}

void BaseColorPalette::sample_vector(const float* t_array, core::models::ColorRGB* out_colors, size_t count) const {
    for (size_t i = 0; i < count; ++i) {
        out_colors[i] = sample(t_array[i]);
    }
}

core::models::ColorRGB BaseColorPalette::get_center_color() const {
    return stops_.empty() ? core::models::ColorRGB(0, 0, 0) : stops_.front().second;
}

core::models::ColorRGB BaseColorPalette::get_petal_color() const {
    if (stops_.empty()) return core::models::ColorRGB(0, 0, 0);
    size_t mid = stops_.size() / 2;
    return stops_[mid].second;
}

core::models::ColorRGB BaseColorPalette::get_tip_color() const {
    return stops_.empty() ? core::models::ColorRGB(0, 0, 0) : stops_.back().second;
}

} // namespace openrgb_flowers::effects::palettes
