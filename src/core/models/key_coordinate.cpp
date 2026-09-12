#include "openrgb_flowers/core/models/key_coordinate.hpp"

#include <algorithm>
#include <utility>

namespace openrgb_flowers::core::models {

KeyCoordinate::KeyCoordinate(std::string key_name, int idx, float posX, float posY, int r, int c)
    : name(std::move(key_name)),
      index(idx),
      x(std::clamp(posX, 0.0f, 1.0f)),
      y(std::clamp(posY, 0.0f, 1.0f)),
      row(r),
      col(c) {}

} // namespace openrgb_flowers::core::models
