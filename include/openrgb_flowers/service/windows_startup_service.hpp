#pragma once

#include <string>

namespace openrgb_flowers::service {

/**
 * @brief Manages Windows auto-start on user logon without requiring administrator privileges.
 */
class WindowsStartupService {
public:
    explicit WindowsStartupService(std::string app_name = "OpenRGBFlowers");

    [[nodiscard]] bool is_enabled() const;
    bool enable(const std::string& extra_args = "--autostart") const;
    bool disable() const;

private:
    std::string app_name_{"OpenRGBFlowers"};
};

} // namespace openrgb_flowers::service
