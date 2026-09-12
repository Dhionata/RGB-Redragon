#pragma once

#include <atomic>
#include <functional>
#include <memory>
#include <string>
#include <thread>

namespace openrgb_flowers::gui {

/**
 * @brief Native Windows notification area (System Tray) manager.
 */
class SystemTray {
public:
    using PaletteCallback = std::function<void(const std::string&)>;
    using EffectCallback = std::function<void(const std::string&)>;
    using QuitCallback = std::function<void()>;

    SystemTray(
        std::string tooltip = "OpenRGB Flowers Blooming",
        PaletteCallback on_palette = nullptr,
        EffectCallback on_effect = nullptr,
        QuitCallback on_quit = nullptr
    );
    ~SystemTray();

    bool start();
    void stop();
    [[nodiscard]] bool is_running() const;

private:
    void message_loop();

    std::string tooltip_;
    PaletteCallback on_palette_;
    EffectCallback on_effect_;
    QuitCallback on_quit_;

    std::thread worker_thread_;
    std::atomic<bool> running_{false};
    void* hwnd_{nullptr};
};

} // namespace openrgb_flowers::gui
