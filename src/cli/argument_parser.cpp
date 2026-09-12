#include "openrgb_flowers/cli/argument_parser.hpp"

#include <iostream>

namespace openrgb_flowers::cli {

ParsedArguments ArgumentParser::parse(int argc, char* argv[]) {
    std::vector<std::string> args;
    for (int i = 1; i < argc; ++i) {
        args.emplace_back(argv[i]);
    }
    return parse(args);
}

ParsedArguments ArgumentParser::parse(const std::vector<std::string>& args) {
    ParsedArguments result;

    for (size_t i = 0; i < args.size(); ++i) {
        const auto& arg = args[i];

        if (arg == "-h" || arg == "--help") {
            result.show_help = true;
            return result;
        } else if ((arg == "-e" || arg == "--effect") && i + 1 < args.size()) {
            result.config.effect_type = args[++i];
        } else if ((arg == "-p" || arg == "--palette") && i + 1 < args.size()) {
            result.config.palette_name = args[++i];
        } else if (arg == "--fps" && i + 1 < args.size()) {
            result.config.fps = std::stof(args[++i]);
        } else if ((arg == "-s" || arg == "--speed") && i + 1 < args.size()) {
            result.config.speed = std::stof(args[++i]);
        } else if ((arg == "-m" || arg == "--max-flowers") && i + 1 < args.size()) {
            result.config.max_flowers = std::stoi(args[++i]);
        } else if (arg == "--spawn-rate" && i + 1 < args.size()) {
            result.config.spawn_rate = std::stof(args[++i]);
        } else if ((arg == "-b" || arg == "--brightness") && i + 1 < args.size()) {
            result.config.brightness = std::stof(args[++i]);
        } else if (arg == "--saturation" && i + 1 < args.size()) {
            result.config.saturation = std::stof(args[++i]);
        } else if (arg == "--blend" && i + 1 < args.size()) {
            result.config.blend_mode = args[++i];
        } else if (arg == "--driver" && i + 1 < args.size()) {
            result.driver = args[++i];
        } else if (arg == "--mock") {
            result.mock = true;
            result.driver = "mock";
        } else if (arg == "--host" && i + 1 < args.size()) {
            result.config.host = args[++i];
        } else if (arg == "--port" && i + 1 < args.size()) {
            result.config.port = std::stoi(args[++i]);
        } else if ((arg == "-d" || arg == "--device") && i + 1 < args.size()) {
            result.config.device_name = args[++i];
        } else if ((arg == "-c" || arg == "--config") && i + 1 < args.size()) {
            result.config_file = args[++i];
        } else if (arg == "--max-frames" && i + 1 < args.size()) {
            result.max_frames = std::stoull(args[++i]);
        } else if (arg == "--tray") {
            result.tray = true;
        } else if (arg == "--autostart") {
            result.autostart = true;
            result.tray = true;
        } else if (arg == "--install-startup") {
            result.install_startup = true;
        } else if (arg == "--uninstall-startup") {
            result.uninstall_startup = true;
        }
    }

    return result;
}

void ArgumentParser::print_help() {
    std::cout << R"(
=============================================================================
🌸 OpenRGB & Redragon Flowers Blooming (C++ Native Controller)
=============================================================================

Uso / Usage:
  FlowersBlooming.exe [opções / options]

Opções / Options:
  -e, --effect <tipo>        'blooming' (flores) ou 'random_blend' (mosaico cromático).
  -p, --palette <tema>       sakura, rose, lotus, sunflower, lavender, rainbow, cyberpunk, aurora.
  -s, --speed <multiplicador>Velocidade da propagação/transição (padrão: 1.0).
  -b, --brightness <fator>   Brilho global (0.0 a 1.0, padrão: 1.0).
      --saturation <fator>   Saturação das cores (padrão: 1.0).
      --fps <taxa>           Taxa de quadros (padrão: 30.0).
  -m, --max-flowers <num>    Máximo de flores simultâneas (padrão: 7).
      --spawn-rate <taxa>    Taxa de surgimento de novas flores por segundo.
      --blend <modo>         weighted, screen, additive (padrão: weighted).
      --driver <driver>      auto, redragon, openrgb, mock (padrão: auto).
      --mock                 Executa em modo simulação (sem hardware).
      --host <ip>            Endereço do servidor OpenRGB (padrão: 127.0.0.1).
      --port <porta>         Porta TCP do OpenRGB SDK (padrão: 6742).
  -d, --device <nome>        Filtro de nome do dispositivo OpenRGB (ex: 'K556').
  -c, --config <arquivo>     Carrega parâmetros de arquivo JSON.
      --tray                 Inicia com ícone na bandeja do sistema (system tray).
      --autostart            Modo silencioso em segundo plano para inicialização.
      --install-startup      Registra execução automática no login do Windows.
      --uninstall-startup    Remove registro de execução automática no Windows.
  -h, --help                 Exibe esta ajuda.
)";
}

} // namespace openrgb_flowers::cli
