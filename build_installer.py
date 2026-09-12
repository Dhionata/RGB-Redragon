"""Build Windows Installer (Inno Setup) for OpenRGB Flowers Blooming.

Complies with SOLID & DRY principles, delegating build steps and Inno Setup
detection to dedicated build_tools modules.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure project root is in sys.path for build_tools import
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from build_tools.inno_builder import InnoSetupBuilder
from build_tools.inno_locator import InnoSetupLocator
from build_tools.nuitka_builder import NuitkaBuilder
from build_tools.version_reader import VersionReader


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OpenRGB Flowers Blooming - Inno Setup Installer Builder"
    )
    parser.add_argument(
        "--compile-nuitka",
        action="store_true",
        help="Force Nuitka standalone C++ compilation before running Inno Setup",
    )
    parser.add_argument(
        "--skip-nuitka",
        action="store_true",
        help="Skip Nuitka compilation and use existing dist/FlowersBlooming_Portable directory",
    )
    parser.add_argument(
        "--iss-path",
        type=str,
        default=str(PROJECT_ROOT / "installer.iss"),
        help="Path to Inno Setup script (.iss)",
    )
    parser.add_argument(
        "--iscc-path",
        type=str,
        default=None,
        help="Explicit path to Inno Setup Compiler (ISCC.exe)",
    )
    parser.add_argument(
        "--version",
        type=str,
        default=None,
        help="Application version string (defaults to version from pyproject.toml)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="dist",
        help="Directory to save the generated installer",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default="FlowersBlooming_Setup",
        help="Base filename of the generated installer without extension",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    version = args.version or VersionReader.get_version(PROJECT_ROOT)
    source_dir = PROJECT_ROOT / "dist" / "FlowersBlooming_Portable"
    portable_exe = source_dir / "FlowersBlooming.exe"

    should_compile_nuitka = False
    if args.compile_nuitka:
        should_compile_nuitka = True
    elif not args.skip_nuitka:
        # If user didn't specify, compile if portable folder or executable is missing
        if not portable_exe.is_file():
            print(f"[Build] Executavel portatil nao encontrado em {portable_exe}.")
            print("[Build] Compilando automaticamente com Nuitka (--standalone)...")
            should_compile_nuitka = True
        else:
            print(f"[Build] Usando pasta portatil existente: {source_dir}")

    if should_compile_nuitka:
        print("[Build] Executando NuitkaBuilder (standalone)...")
        nuitka_builder = NuitkaBuilder(
            entry_point=str(PROJECT_ROOT / "launcher.py"),
            output_name="FlowersBlooming.exe",
            output_dir=str(PROJECT_ROOT / "dist"),
            onefile=False,
        )
        ret = nuitka_builder.run()
        if ret != 0:
            print(f"[Build ERROR] Compilacao Nuitka falhou com codigo {ret}.")
            return ret

    locator = InnoSetupLocator()
    builder = InnoSetupBuilder(
        iss_file=args.iss_path,
        source_dir=source_dir,
        output_dir=PROJECT_ROOT / args.output_dir,
        output_name=args.output_name,
        app_version=version,
        locator=locator,
        custom_iscc_path=args.iscc_path,
    )

    return builder.run()


if __name__ == "__main__":
    sys.exit(main())
