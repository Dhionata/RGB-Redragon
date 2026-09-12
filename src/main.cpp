#include "openrgb_flowers/cli/argument_parser.hpp"
#include "openrgb_flowers/core/models/effect_config.hpp"
#include "openrgb_flowers/effects/effect_engine_factory.hpp"
#include "openrgb_flowers/gui/system_tray.hpp"
#include "openrgb_flowers/hardware/layout_factory.hpp"
#include "openrgb_flowers/hardware/transmitter_factory.hpp"
#include "openrgb_flowers/service/config_storage_service.hpp"
#include "openrgb_flowers/service/runner_service.hpp"
#include "openrgb_flowers/service/windows_startup_service.hpp"

#include <iostream>
#include <memory>

#ifdef _WIN32
#include <windows.h>
#endif

using namespace openrgb_flowers;

int main(int argc, char* argv[]) {
    auto parsed = cli::ArgumentParser::parse(argc, argv);

    if (parsed.show_help) {
        cli::ArgumentParser::print_help();
        return 0;
    }

    if (parsed.install_startup) {
        service::WindowsStartupService svc;
        if (svc.enable()) {
            std::cout << "✓ Aplicacao configurada com sucesso para iniciar com o Windows!\n";
            return 0;
        }
        std::cerr << "✗ Falha ao registrar inicializacao automatica no Windows.\n";
        return 1;
    }

    if (parsed.uninstall_startup) {
        service::WindowsStartupService svc;
        if (svc.disable()) {
            std::cout << "✓ Inicializacao automatica removida com sucesso.\n";
            return 0;
        }
        std::cerr << "✗ Falha ao remover registro de inicializacao automatica.\n";
        return 1;
    }

    // 1. Resolve configuration
    core::models::EffectConfig config;
    service::ConfigStorageService storage_svc;

    if (parsed.autostart) {
#ifdef _WIN32
        HWND console_hwnd = GetConsoleWindow();
        if (console_hwnd) {
            ShowWindow(console_hwnd, SW_HIDE);
        }
#endif
        config = storage_svc.load_config();
        std::cout << "[Init] Iniciando em segundo plano via autostart...\n";
    } else if (!parsed.config_file.empty()) {
        try {
            config = core::models::EffectConfig::load_json_file(parsed.config_file);
        } catch (const std::exception& e) {
            std::cerr << "[Config Error] " << e.what() << "\n";
            return 1;
        }
    } else {
        config = parsed.config;
    }

    try {
        config.validate();
    } catch (const std::exception& e) {
        std::cerr << "[Config Validation Error] " << e.what() << "\n";
        return 1;
    }

    // 2. Hardware transmitter & layout
    auto transmitter = hardware::TransmitterFactory::create_transmitter(
        parsed.driver,
        config.host,
        config.port,
        config.device_name,
        config.device_index
    );

    auto layout = hardware::LayoutFactory::create_layout(transmitter);

    // 3. Engine
    auto engine = effects::EffectEngineFactory::create_engine(
        config.effect_type,
        config,
        layout
    );
    std::shared_ptr<core::interfaces::IEffectEngine> shared_engine = std::move(engine);

    // 4. Runner service
    auto runner = std::make_shared<service::RunnerService>(
        shared_engine,
        transmitter,
        layout,
        config
    );

    // 5. System Tray (optional / autostart)
    std::unique_ptr<gui::SystemTray> tray;
    if (parsed.tray || parsed.autostart) {
        tray = std::make_unique<gui::SystemTray>(
            "OpenRGB Flowers Blooming",
            [runner, &config](const std::string& pal) {
                config.palette_name = pal;
                runner->set_palette(pal);
                std::cout << "[Tray] Paleta alterada para: " << pal << "\n";
            },
            [runner, &config](const std::string& eff) {
                config.effect_type = eff;
                runner->set_effect(eff);
                std::cout << "[Tray] Efeito alterado para: " << eff << "\n";
            },
            [runner]() {
                runner->stop();
            }
        );
        tray->start();
    }

    std::cout << "=============================================================================\n";
    std::cout << "🌸 OpenRGB Flowers Blooming C++ Native Controller Rodando!\n";
    std::cout << "   Efeito: " << config.effect_type << " | Paleta: " << config.palette_name << "\n";
    std::cout << "   Driver: " << layout->get_device_name() << " (" << layout->get_key_count() << " LEDs)\n";
    std::cout << "   Taxa: " << config.fps << " FPS | Brilho: " << static_cast<int>(config.brightness * 100) << "%\n";
    std::cout << "   Pressione Ctrl+C para encerrar com seguranca.\n";
    std::cout << "=============================================================================\n";

    runner->run(parsed.max_frames);

    if (tray) {
        tray->stop();
    }

    std::cout << "\n[Shutdown] Aplicacao encerrada com sucesso.\n";
    return 0;
}
