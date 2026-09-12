#include "openrgb_flowers/service/config_storage_service.hpp"

#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>

namespace openrgb_flowers::service {

namespace fs = std::filesystem;

ConfigStorageService::ConfigStorageService(std::string custom_path) {
    if (!custom_path.empty()) {
        storage_path_ = std::move(custom_path);
    } else {
        const char* user_profile = std::getenv("USERPROFILE");
        if (!user_profile) {
            user_profile = std::getenv("HOME");
        }
        std::string base_dir = user_profile ? user_profile : ".";
        fs::path p = fs::path(base_dir) / ".openrgb_flowers" / "user_config.json";
        storage_path_ = p.string();
    }
}

std::string ConfigStorageService::get_storage_path() const {
    return storage_path_;
}

core::models::EffectConfig ConfigStorageService::load_config() const {
    // 1. Try user persistent path
    if (fs::exists(storage_path_)) {
        try {
            return core::models::EffectConfig::load_json_file(storage_path_);
        } catch (const std::exception& e) {
            std::cerr << "[ConfigStorage] Could not load " << storage_path_ << ": " << e.what() << "\n";
        }
    }

    // 2. Try local fallback config.json
    if (fs::exists("config.json")) {
        try {
            return core::models::EffectConfig::load_json_file("config.json");
        } catch (const std::exception& e) {
            std::cerr << "[ConfigStorage] Could not load local config.json: " << e.what() << "\n";
        }
    }

    // 3. Default fallback
    core::models::EffectConfig cfg;
    cfg.effect_type = "random_blend";
    cfg.palette_name = "rainbow";
    cfg.speed = 1.2f;
    cfg.brightness = 1.0f;
    cfg.saturation = 1.0f;
    cfg.fps = 30.0f;
    return cfg;
}

bool ConfigStorageService::save_config(const core::models::EffectConfig& config) const {
    try {
        fs::path p(storage_path_);
        if (p.has_parent_path()) {
            fs::create_directories(p.parent_path());
        }
        config.save_json_file(storage_path_);
        return true;
    } catch (const std::exception& e) {
        std::cerr << "[ConfigStorage] Error saving config: " << e.what() << "\n";
        return false;
    }
}

} // namespace openrgb_flowers::service
