"""PyInstaller build script to generate standalone Windows executable."""
import os
import shutil
import sys
from pathlib import Path


def _patch_pyinstaller_winutils() -> None:
    """Safely monkey-patches PyInstaller winutils on Windows to prevent pefile lock crashes."""
    try:
        from PyInstaller.utils.win32 import winutils

        orig_timestamp = getattr(winutils, "set_exe_build_timestamp", None)
        if orig_timestamp:
            def safe_set_timestamp(exe_path, timestamp):
                try:
                    return orig_timestamp(exe_path, timestamp)
                except Exception:
                    pass
            winutils.set_exe_build_timestamp = safe_set_timestamp

        orig_checksum = getattr(winutils, "update_exe_pe_checksum", None)
        if orig_checksum:
            def safe_update_checksum(exe_path):
                try:
                    return orig_checksum(exe_path)
                except Exception:
                    pass
            winutils.update_exe_pe_checksum = safe_update_checksum
    except Exception:
        pass


def build() -> int:
    print("Iniciando compilação do executável standalone OpenRGBFlowers.exe...")
    _patch_pyinstaller_winutils()

    try:
        import subprocess
        subprocess.run(["taskkill", "/F", "/IM", "OpenRGBFlowers.exe", "/IM", "RedragonRGB.exe"], capture_output=True)
    except Exception:
        pass

    import PyInstaller.__main__

    args = [
        "--noconsole",
        "--onefile",
        "--name",
        "OpenRGBFlowers",
        "--paths",
        "src",
        "--collect-all",
        "openrgb_flowers",
        "--hidden-import",
        "hid",
        "--hidden-import",
        "openrgb",
        "--clean",
        "-y",
    ]

    version_file = Path("file_version_info.txt")
    if version_file.exists():
        args.extend(["--version-file", str(version_file)])

    args.append("launcher.py")

    try:
        PyInstaller.__main__.run(args)
    except SystemExit as e:
        if e.code != 0:
            print(f"\n[ERROR] Falha na compilação com código: {e.code}")
            return int(e.code)
    except Exception as e:
        print(f"\n[ERROR] Exceção durante compilação: {e}")
        return 1

    dist_dir = Path("dist")
    primary_exe = dist_dir / "OpenRGBFlowers.exe"
    alias_exe = dist_dir / "RedragonRGB.exe"

    if primary_exe.exists():
        try:
            shutil.copyfile(primary_exe, alias_exe)
        except Exception:
            pass

        print(f"\n[SUCCESS] Executáveis gerados com sucesso:")
        print(f"  -> {primary_exe.resolve()}")
        print(f"  -> {alias_exe.resolve()}")
        return 0

    print("\n[ERROR] Arquivo executável não encontrado após compilação.")
    return 1


if __name__ == "__main__":
    sys.exit(build())

