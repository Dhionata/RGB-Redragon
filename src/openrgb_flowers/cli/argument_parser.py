"""Command-line argument parser builder for Flowers Blooming."""
from __future__ import annotations
import argparse
from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry


class ArgumentParserBuilder:
    """Builds user-friendly command-line argument parser with bilingual help."""

    @classmethod
    def build(cls) -> argparse.ArgumentParser:
        available_palettes = PaletteRegistry.list_available()

        parser = argparse.ArgumentParser(
            prog="openrgb-flowers",
            description="🌸 OpenRGB Flowers Blooming - Organic floral lighting effect for Redragon K556RGB-M & OpenRGB keyboards.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(
            "--effect",
            "-e",
            type=str,
            default="blooming",
            choices=["blooming", "random_blend"],
            help="Lighting effect type / Tipo de efeito: 'blooming' (flores desabrochando) or 'random_blend' (todas as teclas iluminadas misturando cores aleatórias).",
        )
        parser.add_argument(
            "--gui",
            action="store_true",
            help="Launch interactive graphical user interface / Abre a interface gráfica interativa.",
        )
        parser.add_argument(
            "--palette",
            "-p",
            type=str,
            default="sakura",
            choices=available_palettes,
            help="Floral color palette theme / Paleta de cores florais.",
        )
        parser.add_argument(
            "--fps",
            type=float,
            default=30.0,
            help="Target frames per second (15-60) / Taxa de quadros por segundo.",
        )
        parser.add_argument(
            "--speed",
            "-s",
            type=float,
            default=1.0,
            help="Bloom expansion speed multiplier / Velocidade de expansão das flores.",
        )
        parser.add_argument(
            "--max-flowers",
            "-m",
            type=int,
            default=7,
            help="Maximum simultaneous blooming flowers / Máximo de flores simultâneas.",
        )
        parser.add_argument(
            "--spawn-rate",
            type=float,
            default=1.4,
            help="Average flowers spawned per second / Média de flores geradas por segundo.",
        )
        parser.add_argument(
            "--brightness",
            "-b",
            type=float,
            default=1.0,
            help="Global brightness factor (0.0 to 1.0) / Brilho global.",
        )
        parser.add_argument(
            "--blend",
            type=str,
            default="weighted",
            choices=["weighted", "screen", "additive"],
            help="Petal color blending strategy / Modo de mesclagem de cores.",
        )
        parser.add_argument(
            "--driver",
            type=str,
            default="auto",
            choices=["auto", "redragon", "openrgb", "mock"],
            help="Hardware driver / Driver de transmissão: 'auto' (detects K556 else OpenRGB), 'redragon' (direct USB HID for K556RGB-M), 'openrgb' (OpenRGB SDK), or 'mock' (simulation).",
        )
        parser.add_argument(
            "--preview",
            action="store_true",
            help="Enable live 24-bit TrueColor terminal preview / Ativa visualização no terminal.",
        )
        parser.add_argument(
            "--mock",
            action="store_true",
            help="Alias for '--driver mock' / Executa em modo simulação sem hardware.",
        )
        parser.add_argument(
            "--host",
            type=str,
            default="127.0.0.1",
            help="OpenRGB SDK server host address / Endereço do servidor OpenRGB.",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=6742,
            help="OpenRGB SDK server port / Porta do servidor OpenRGB.",
        )
        parser.add_argument(
            "--device",
            "-d",
            type=str,
            default=None,
            help="Specific target device name filter (e.g., 'K556') / Nome do dispositivo alvo.",
        )
        parser.add_argument(
            "--config",
            "-c",
            type=str,
            default=None,
            help="Path to JSON configuration file / Caminho para arquivo de configuração JSON.",
        )
        parser.add_argument(
            "--max-frames",
            type=int,
            default=None,
            help="Optional maximum frames to render before exiting / Limite de quadros a renderizar.",
        )

        return parser
