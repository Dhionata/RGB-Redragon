#include "openrgb_flowers/core/models/effect_config.hpp"
#include "openrgb_flowers/core/json_helper.hpp"

#include <fstream>
#include <sstream>
#include <stdexcept>

namespace openrgb_flowers::core::models {

void EffectConfig::validate() const {
    if (fps < 1.0f || fps > 120.0f) {
        throw std::invalid_argument("fps must be between 1.0 and 120.0");
    }
    if (speed < 0.1f || speed > 10.0f) {
        throw std::invalid_argument("speed must be between 0.1 and 10.0");
    }
    if (max_flowers < 1 || max_flowers > 50) {
        throw std::invalid_argument("max_flowers must be between 1 and 50");
    }
    if (spawn_rate < 0.1f || spawn_rate > 20.0f) {
        throw std::invalid_argument("spawn_rate must be between 0.1 and 20.0");
    }
    if (brightness < 0.0f || brightness > 1.0f) {
        throw std::invalid_argument("brightness must be between 0.0 and 1.0");
    }
    if (saturation < 0.0f || saturation > 3.0f) {
        throw std::invalid_argument("saturation must be between 0.0 and 3.0");
    }
    if (gamma < 0.5f || gamma > 3.5f) {
        throw std::invalid_argument("gamma must be between 0.5 and 3.5");
    }
    if (petal_options.empty()) {
        throw std::invalid_argument("petal_options must not be empty");
    }
    for (int p : petal_options) {
        if (p < 3) {
            throw std::invalid_argument("petal_options must contain integers >= 3");
        }
    }
    if (effect_type != "blooming" && effect_type != "random_blend") {
        throw std::invalid_argument("effect_type must be 'blooming' or 'random_blend'");
    }
    if (blend_mode != "weighted" && blend_mode != "additive" && blend_mode != "screen") {
        throw std::invalid_argument("blend_mode must be 'weighted', 'additive', or 'screen'");
    }
    if (palette_name.empty()) {
        throw std::invalid_argument("palette_name must not be empty");
    }
}

std::string EffectConfig::to_json(int indent) const {
    JsonObject obj;
    obj["effect_type"] = JsonValue(effect_type);
    obj["fps"] = JsonValue(fps);
    obj["speed"] = JsonValue(speed);
    obj["max_flowers"] = JsonValue(max_flowers);
    obj["spawn_rate"] = JsonValue(spawn_rate);

    JsonArray petals;
    for (int p : petal_options) {
        petals.push_back(JsonValue(p));
    }
    obj["petal_options"] = JsonValue(petals);

    obj["palette_name"] = JsonValue(palette_name);
    obj["blend_mode"] = JsonValue(blend_mode);
    obj["background_color"] = JsonValue(background_color.to_hex());
    obj["ambient_pulse"] = JsonValue(ambient_pulse);
    obj["brightness"] = JsonValue(brightness);
    obj["saturation"] = JsonValue(saturation);
    obj["gamma"] = JsonValue(gamma);
    obj["host"] = JsonValue(host);
    obj["port"] = JsonValue(port);
    obj["device_name"] = JsonValue(device_name);
    obj["device_index"] = JsonValue(device_index);

    return JsonValue(obj).serialize(indent);
}

EffectConfig EffectConfig::from_json(const std::string& json_str) {
    JsonValue root = JsonValue::parse(json_str);
    if (!root.is_object()) {
        throw std::invalid_argument("JSON root must be an object");
    }

    EffectConfig cfg;
    if (root.has_key("effect_type")) cfg.effect_type = root.get("effect_type").as_string("blooming");
    if (root.has_key("fps")) cfg.fps = static_cast<float>(root.get("fps").as_double(30.0));
    if (root.has_key("speed")) cfg.speed = static_cast<float>(root.get("speed").as_double(1.0));
    if (root.has_key("max_flowers")) cfg.max_flowers = root.get("max_flowers").as_int(7);
    if (root.has_key("spawn_rate")) cfg.spawn_rate = static_cast<float>(root.get("spawn_rate").as_double(1.4));

    if (root.has_key("petal_options") && root.get("petal_options").is_array()) {
        cfg.petal_options.clear();
        for (const auto& item : root.get("petal_options").as_array()) {
            cfg.petal_options.push_back(item.as_int(5));
        }
    }

    if (root.has_key("palette_name")) cfg.palette_name = root.get("palette_name").as_string("sakura");
    else if (root.has_key("palette")) cfg.palette_name = root.get("palette").as_string("sakura");

    if (root.has_key("blend_mode")) cfg.blend_mode = root.get("blend_mode").as_string("weighted");

    if (root.has_key("background_color")) {
        const auto& bg_val = root.get("background_color");
        if (bg_val.is_string()) {
            cfg.background_color = ColorRGB::from_hex(bg_val.as_string());
        } else if (bg_val.is_array() && bg_val.as_array().size() >= 3) {
            const auto& arr = bg_val.as_array();
            cfg.background_color = ColorRGB(
                static_cast<uint8_t>(arr[0].as_int()),
                static_cast<uint8_t>(arr[1].as_int()),
                static_cast<uint8_t>(arr[2].as_int())
            );
        }
    }

    if (root.has_key("ambient_pulse")) cfg.ambient_pulse = root.get("ambient_pulse").as_bool(true);
    if (root.has_key("brightness")) cfg.brightness = static_cast<float>(root.get("brightness").as_double(1.0));
    if (root.has_key("saturation")) cfg.saturation = static_cast<float>(root.get("saturation").as_double(1.0));
    if (root.has_key("gamma")) cfg.gamma = static_cast<float>(root.get("gamma").as_double(1.0));
    if (root.has_key("host")) cfg.host = root.get("host").as_string("127.0.0.1");
    if (root.has_key("port")) cfg.port = root.get("port").as_int(6742);
    if (root.has_key("device_name")) cfg.device_name = root.get("device_name").as_string("");
    if (root.has_key("device_index")) cfg.device_index = root.get("device_index").as_int(-1);

    cfg.validate();
    return cfg;
}

EffectConfig EffectConfig::load_json_file(const std::string& file_path) {
    std::ifstream file(file_path);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open config file: " + file_path);
    }
    std::stringstream buffer;
    buffer << file.rdbuf();
    return from_json(buffer.str());
}

void EffectConfig::save_json_file(const std::string& file_path) const {
    std::ofstream file(file_path);
    if (!file.is_open()) {
        throw std::runtime_error("Could not write config file: " + file_path);
    }
    file << to_json(2);
}

} // namespace openrgb_flowers::core::models
