"""CLI entrypoint for running the Flowers Blooming effect."""
from __future__ import annotations
import logging
import sys
from typing import Optional

from openrgb_flowers.cli.argument_parser import ArgumentParserBuilder
from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.effects.blooming_engine import BloomingEngine
from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider
from openrgb_flowers.hardware.k556_matrix_layout_provider import K556MatrixLayoutProvider
from openrgb_flowers.hardware.redragon_k556_transmitter import RedragonK556Transmitter
from openrgb_flowers.hardware.transmitter_factory import TransmitterFactory
from openrgb_flowers.core.exceptions import OpenRGBConnectionError, HardwareConnectionError
from openrgb_flowers.preview.terminal_visualizer import TerminalVisualizer
from openrgb_flowers.service.runner_service import RunnerService


def main(args: Optional[list[str]] = None) -> int:
    """CLI main function."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Auto-default to GUI if running as a standalone frozen executable without CLI arguments
    if args is None and len(sys.argv) == 1 and getattr(sys, "frozen", False):
        args = ["--gui"]

    parser = ArgumentParserBuilder.build()
    parsed_args = parser.parse_args(args)

    # Check startup install/uninstall actions
    if getattr(parsed_args, "install_startup", False):
        from openrgb_flowers.service.windows_startup_service import WindowsStartupService
        svc = WindowsStartupService()
        if svc.enable():
            logging.info("✓ Aplicação configurada com sucesso para iniciar com o Windows!")
            return 0
        logging.error("✗ Falha ao registrar inicialização automática no Windows.")
        return 1

    if getattr(parsed_args, "uninstall_startup", False):
        from openrgb_flowers.service.windows_startup_service import WindowsStartupService
        svc = WindowsStartupService()
        if svc.disable():
            logging.info("✓ Inicialização com o Windows removida com sucesso.")
            return 0
        logging.error("✗ Falha ao remover registro de inicialização.")
        return 1

    # 0. Check if GUI mode requested
    if getattr(parsed_args, "gui", False):
        from openrgb_flowers.gui.app_window import launch_gui
        return launch_gui()

    # 1. Load or build config
    if getattr(parsed_args, "autostart", False):
        from openrgb_flowers.service.config_storage_service import ConfigStorageService
        config = ConfigStorageService().load_config()
        logging.info("Iniciando em segundo plano via autostart do Windows...")
    elif parsed_args.config:
        config = EffectConfig.load_json(parsed_args.config)
    else:
        config = EffectConfig(
            effect_type=getattr(parsed_args, "effect", "blooming"),
            fps=parsed_args.fps,
            speed=parsed_args.speed,
            max_flowers=parsed_args.max_flowers,
            spawn_rate=parsed_args.spawn_rate,
            palette_name=parsed_args.palette,
            blend_mode=parsed_args.blend,
            brightness=parsed_args.brightness,
            saturation=getattr(parsed_args, "saturation", 1.0),
            host=parsed_args.host,
            port=parsed_args.port,
            device_name=parsed_args.device,
        )

    config.validate()

    # 2. Resolve Driver & Transmitter
    driver = "mock" if parsed_args.mock else getattr(parsed_args, "driver", "auto")
    transmitter = TransmitterFactory.create_transmitter(
        driver=driver,
        host=config.host,
        port=config.port,
        device_name=config.device_name,
    )

    # 3. Hardware Layout: Hardware matrix for Redragon HID, ANSI layout for OpenRGB/Mock
    if isinstance(transmitter, RedragonK556Transmitter):
        layout = K556MatrixLayoutProvider()
    else:
        layout = K556LayoutProvider()

    # 4. Palette & Engine via EffectEngineFactory
    from openrgb_flowers.effects.effect_engine_factory import EffectEngineFactory
    palette = PaletteRegistry.get(config.palette_name)
    engine = EffectEngineFactory.create_engine(
        effect_name=config.effect_type,
        config=config,
        layout_provider=layout,
        palette=palette,
    )

    # 5. Visualizer
    visualizer = TerminalVisualizer() if parsed_args.preview else None

    # 6. Service & Run
    service = RunnerService(
        engine=engine,
        transmitter=transmitter,
        layout_provider=layout,
        config=config,
        visualizer=visualizer,
    )

    try:
        service.run(max_frames=parsed_args.max_frames)
        return 0
    except KeyboardInterrupt:
        return 0
    except (OpenRGBConnectionError, HardwareConnectionError) as e:
        logging.error("%s", e)
        logging.info("Tip: Run with '--preview' or '--mock' to test the effect in terminal simulation.")
        return 1
    except Exception as e:
        logging.error(f"Fatal error running Flowers Blooming effect: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
