#pragma once

#include "openrgb_flowers/core/models/effect_config.hpp"
#include <optional>
#include <string>
#include <vector>

namespace openrgb_flowers::cli {

/**
 * @brief Parsed command-line arguments and configuration options.
 */
struct ParsedArguments {
    core::models::EffectConfig config;
    std::string driver{"auto"};
    std::string config_file;
    bool mock{false};
    bool tray{false};
    bool autostart{false};
    bool install_startup{false};
    bool uninstall_startup{false};
    bool show_help{false};
    std::optional<uint64_t> max_frames;
};

/**
 * @brief Command-line argument parser with bilingual help.
 */
class ArgumentParser {
public:
    static ParsedArguments parse(int argc, char* argv[]);
    static ParsedArguments parse(const std::vector<std::string>& args);
    static void print_help();
};

} // namespace openrgb_flowers::cli
