#include "openrgb_flowers/core/json_helper.hpp"

#include <cctype>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <stdexcept>

namespace openrgb_flowers::core {

namespace {

class JsonParser {
    const std::string& src;
    size_t pos{0};

    void skip_whitespace() {
        while (pos < src.size() && (src[pos] == ' ' || src[pos] == '\t' || src[pos] == '\r' || src[pos] == '\n')) {
            ++pos;
        }
    }

    char peek() {
        skip_whitespace();
        return pos < src.size() ? src[pos] : '\0';
    }

    char get() {
        skip_whitespace();
        return pos < src.size() ? src[pos++] : '\0';
    }

public:
    explicit JsonParser(const std::string& input) : src(input) {}

    JsonValue parse_value() {
        skip_whitespace();
        char c = peek();
        if (c == '\0') {
            return JsonValue();
        }
        if (c == 'n') {
            return parse_null();
        }
        if (c == 't' || c == 'f') {
            return parse_bool();
        }
        if (c == '"') {
            return parse_string();
        }
        if (c == '[') {
            return parse_array();
        }
        if (c == '{') {
            return parse_object();
        }
        if (c == '-' || std::isdigit(static_cast<unsigned char>(c))) {
            return parse_number();
        }
        throw std::runtime_error(std::string("Unexpected character in JSON: ") + c);
    }

    JsonValue parse_null() {
        if (src.compare(pos, 4, "null") == 0) {
            pos += 4;
            return JsonValue();
        }
        throw std::runtime_error("Invalid null literal");
    }

    JsonValue parse_bool() {
        if (src.compare(pos, 4, "true") == 0) {
            pos += 4;
            return JsonValue(true);
        }
        if (src.compare(pos, 5, "false") == 0) {
            pos += 5;
            return JsonValue(false);
        }
        throw std::runtime_error("Invalid boolean literal");
    }

    std::string parse_raw_string() {
        get(); // consume opening quote
        std::string result;
        while (pos < src.size()) {
            char c = src[pos++];
            if (c == '"') {
                return result;
            }
            if (c == '\\' && pos < src.size()) {
                char esc = src[pos++];
                switch (esc) {
                    case '"': result += '"'; break;
                    case '\\': result += '\\'; break;
                    case '/': result += '/'; break;
                    case 'b': result += '\b'; break;
                    case 'f': result += '\f'; break;
                    case 'n': result += '\n'; break;
                    case 'r': result += '\r'; break;
                    case 't': result += '\t'; break;
                    case 'u': {
                        if (pos + 4 <= src.size()) {
                            std::string hex_str = src.substr(pos, 4);
                            pos += 4;
                            try {
                                unsigned long code = std::stoul(hex_str, nullptr, 16);
                                if (code <= 0x7F) {
                                    result += static_cast<char>(code);
                                } else if (code <= 0x7FF) {
                                    result += static_cast<char>(0xC0 | ((code >> 6) & 0x1F));
                                    result += static_cast<char>(0x80 | (code & 0x3F));
                                } else {
                                    result += static_cast<char>(0xE0 | ((code >> 12) & 0x0F));
                                    result += static_cast<char>(0x80 | ((code >> 6) & 0x3F));
                                    result += static_cast<char>(0x80 | (code & 0x3F));
                                }
                            } catch (...) {
                                result += "\\u" + hex_str;
                            }
                        } else {
                            result += 'u';
                        }
                        break;
                    }
                    default: result += esc; break;
                }
            } else {
                result += c;
            }
        }
        throw std::runtime_error("Unterminated string in JSON");
    }

    JsonValue parse_string() {
        return JsonValue(parse_raw_string());
    }

    JsonValue parse_number() {
        size_t start = pos;
        if (src[pos] == '-') {
            ++pos;
        }
        while (pos < src.size() && (std::isdigit(static_cast<unsigned char>(src[pos])) || src[pos] == '.' || src[pos] == 'e' || src[pos] == 'E' || src[pos] == '+' || src[pos] == '-')) {
            ++pos;
        }
        std::string num_str = src.substr(start, pos - start);
        try {
            double val = std::stod(num_str);
            return JsonValue(val);
        } catch (...) {
            throw std::runtime_error("Invalid number literal in JSON: " + num_str);
        }
    }

    JsonValue parse_array() {
        get(); // consume '['
        JsonArray arr;
        skip_whitespace();
        if (peek() == ']') {
            get();
            return JsonValue(arr);
        }
        while (true) {
            arr.push_back(parse_value());
            skip_whitespace();
            char c = get();
            if (c == ']') {
                break;
            }
            if (c != ',') {
                throw std::runtime_error("Expected ',' or ']' in array");
            }
        }
        return JsonValue(arr);
    }

    JsonValue parse_object() {
        get(); // consume '{'
        JsonObject obj;
        skip_whitespace();
        if (peek() == '}') {
            get();
            return JsonValue(obj);
        }
        while (true) {
            skip_whitespace();
            if (peek() != '"') {
                throw std::runtime_error("Expected string key in object");
            }
            std::string key = parse_raw_string();
            skip_whitespace();
            if (get() != ':') {
                throw std::runtime_error("Expected ':' after key in object");
            }
            JsonValue val = parse_value();
            obj[key] = std::move(val);
            skip_whitespace();
            char c = get();
            if (c == '}') {
                break;
            }
            if (c != ',') {
                throw std::runtime_error("Expected ',' or '}' in object");
            }
        }
        return JsonValue(obj);
    }
};

static const JsonValue NULL_VALUE;
static const JsonArray EMPTY_ARRAY;
static const JsonObject EMPTY_OBJECT;

} // anonymous namespace

bool JsonValue::as_bool(bool default_val) const {
    if (type == JsonType::Boolean) {
        return std::get<bool>(data);
    }
    return default_val;
}

double JsonValue::as_double(double default_val) const {
    if (type == JsonType::Number) {
        return std::get<double>(data);
    }
    return default_val;
}

int JsonValue::as_int(int default_val) const {
    if (type == JsonType::Number) {
        return static_cast<int>(std::get<double>(data));
    }
    return default_val;
}

std::string JsonValue::as_string(const std::string& default_val) const {
    if (type == JsonType::String) {
        return std::get<std::string>(data);
    }
    return default_val;
}

const JsonArray& JsonValue::as_array() const {
    if (type == JsonType::Array) {
        return std::get<JsonArray>(data);
    }
    return EMPTY_ARRAY;
}

const JsonObject& JsonValue::as_object() const {
    if (type == JsonType::Object) {
        return std::get<JsonObject>(data);
    }
    return EMPTY_OBJECT;
}

bool JsonValue::has_key(const std::string& key) const {
    if (type != JsonType::Object) {
        return false;
    }
    const auto& obj = std::get<JsonObject>(data);
    return obj.find(key) != obj.end();
}

const JsonValue& JsonValue::get(const std::string& key) const {
    if (type != JsonType::Object) {
        return NULL_VALUE;
    }
    const auto& obj = std::get<JsonObject>(data);
    auto it = obj.find(key);
    if (it != obj.end()) {
        return it->second;
    }
    return NULL_VALUE;
}

JsonValue JsonValue::parse(const std::string& json_str) {
    JsonParser parser(json_str);
    return parser.parse_value();
}

std::string JsonValue::serialize(int indent) const {
    std::ostringstream ss;

    auto indent_str = [indent](int depth) -> std::string {
        if (indent <= 0) return "";
        return std::string(static_cast<size_t>(depth * indent), ' ');
    };

    auto escape_json_string = [](const std::string& s) -> std::string {
        std::string out;
        out.reserve(s.size() + 8);
        for (char c : s) {
            switch (c) {
                case '"': out += "\\\""; break;
                case '\\': out += "\\\\"; break;
                case '\b': out += "\\b"; break;
                case '\f': out += "\\f"; break;
                case '\n': out += "\\n"; break;
                case '\r': out += "\\r"; break;
                case '\t': out += "\\t"; break;
                default:
                    if (static_cast<unsigned char>(c) < 0x20) {
                        char buf[8];
                        std::snprintf(buf, sizeof(buf), "\\u%04x", static_cast<unsigned int>(static_cast<unsigned char>(c)));
                        out += buf;
                    } else {
                        out += c;
                    }
                    break;
            }
        }
        return out;
    };

    auto do_serialize = [&](auto& self, const JsonValue& val, int depth) -> void {
        switch (val.type) {
            case JsonType::Null:
                ss << "null";
                break;
            case JsonType::Boolean:
                ss << (std::get<bool>(val.data) ? "true" : "false");
                break;
            case JsonType::Number: {
                double num = std::get<double>(val.data);
                if (std::floor(num) == num && std::fabs(num) < 1e15) {
                    ss << static_cast<long long>(num);
                } else {
                    ss << num;
                }
                break;
            }
            case JsonType::String:
                ss << '"' << escape_json_string(std::get<std::string>(val.data)) << '"';
                break;
            case JsonType::Array: {
                const auto& arr = std::get<JsonArray>(val.data);
                if (arr.empty()) {
                    ss << "[]";
                    break;
                }
                ss << '[';
                if (indent > 0) ss << '\n';
                for (size_t i = 0; i < arr.size(); ++i) {
                    if (indent > 0) ss << indent_str(depth + 1);
                    self(self, arr[i], depth + 1);
                    if (i + 1 < arr.size()) ss << ',';
                    if (indent > 0) ss << '\n';
                }
                if (indent > 0) ss << indent_str(depth);
                ss << ']';
                break;
            }
            case JsonType::Object: {
                const auto& obj = std::get<JsonObject>(val.data);
                if (obj.empty()) {
                    ss << "{}";
                    break;
                }
                ss << '{';
                if (indent > 0) ss << '\n';
                size_t i = 0;
                for (const auto& [k, v] : obj) {
                    if (indent > 0) ss << indent_str(depth + 1);
                    ss << '"' << escape_json_string(k) << "\": ";
                    self(self, v, depth + 1);
                    if (i + 1 < obj.size()) ss << ',';
                    if (indent > 0) ss << '\n';
                    ++i;
                }
                if (indent > 0) ss << indent_str(depth);
                ss << '}';
                break;
            }
        }
    };

    do_serialize(do_serialize, *this, 0);
    return ss.str();
}

} // namespace openrgb_flowers::core
