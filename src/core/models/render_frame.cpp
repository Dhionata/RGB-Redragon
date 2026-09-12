#include "openrgb_flowers/core/models/render_frame.hpp"
#include <utility>

namespace openrgb_flowers::core::models {

RenderFrame::RenderFrame(double ts, uint64_t idx, std::vector<ColorRGB> cols)
    : timestamp(ts),
      frame_index(idx),
      colors(std::move(cols)),
      led_count(static_cast<int>(colors.size())) {}

const ColorRGB* RenderFrame::data() const {
    return colors.data();
}

const uint8_t* RenderFrame::raw_bytes() const {
    return reinterpret_cast<const uint8_t*>(colors.data());
}

size_t RenderFrame::raw_size() const {
    return colors.size() * sizeof(ColorRGB);
}

} // namespace openrgb_flowers::core::models
