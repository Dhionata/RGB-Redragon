#pragma once

#include "openrgb_flowers/core/models/effect_config.hpp"
#include <string>

namespace openrgb_flowers::service {

/**
 * @brief Manages persistent configuration loading and saving to disk.
 */
class ConfigStorageService {
public:
    explicit ConfigStorageService(std::string custom_path = "");

    [[nodiscard]] std::string get_storage_path() const;
    [[nodiscard]] core::models::EffectConfig load_config() const;
    bool save_config(const core::models::EffectConfig& config) const;

private:
    std::string storage_path_;
};

} // namespace openrgb_flowers::service
