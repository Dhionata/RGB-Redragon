#pragma once

#include <map>
#include <memory>
#include <string>
#include <variant>
#include <vector>

namespace openrgb_flowers::core {

enum class JsonType {
    Null,
    Boolean,
    Number,
    String,
    Array,
    Object
};

class JsonValue;
using JsonArray = std::vector<JsonValue>;
using JsonObject = std::map<std::string, JsonValue>;

class JsonValue {
public:
    JsonType type{JsonType::Null};
    std::variant<std::monostate, bool, double, std::string, JsonArray, JsonObject> data;

    JsonValue() : type(JsonType::Null), data(std::monostate{}) {}
    JsonValue(bool b) : type(JsonType::Boolean), data(b) {}
    JsonValue(double num) : type(JsonType::Number), data(num) {}
    JsonValue(int num) : type(JsonType::Number), data(static_cast<double>(num)) {}
    JsonValue(const char* str) : type(JsonType::String), data(std::string(str)) {}
    JsonValue(std::string str) : type(JsonType::String), data(std::move(str)) {}
    JsonValue(JsonArray arr) : type(JsonType::Array), data(std::move(arr)) {}
    JsonValue(JsonObject obj) : type(JsonType::Object), data(std::move(obj)) {}

    [[nodiscard]] bool is_null() const { return type == JsonType::Null; }
    [[nodiscard]] bool is_bool() const { return type == JsonType::Boolean; }
    [[nodiscard]] bool is_number() const { return type == JsonType::Number; }
    [[nodiscard]] bool is_string() const { return type == JsonType::String; }
    [[nodiscard]] bool is_array() const { return type == JsonType::Array; }
    [[nodiscard]] bool is_object() const { return type == JsonType::Object; }

    [[nodiscard]] bool as_bool(bool default_val = false) const;
    [[nodiscard]] double as_double(double default_val = 0.0) const;
    [[nodiscard]] int as_int(int default_val = 0) const;
    [[nodiscard]] std::string as_string(const std::string& default_val = "") const;
    [[nodiscard]] const JsonArray& as_array() const;
    [[nodiscard]] const JsonObject& as_object() const;

    [[nodiscard]] bool has_key(const std::string& key) const;
    [[nodiscard]] const JsonValue& get(const std::string& key) const;

    static JsonValue parse(const std::string& json_str);
    [[nodiscard]] std::string serialize(int indent = 2) const;
};

} // namespace openrgb_flowers::core
