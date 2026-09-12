"""Encapsulates Nuitka C++ compilation configuration and execution."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from build_tools.process_manager import ProcessManager


class NuitkaBuilder:
    """Configures and runs Nuitka native C++ compilation generating a single executable."""

    def __init__(
        self,
        entry_point: str = "launcher.py",
        output_name: str = "FlowersBlooming.exe",
        output_dir: str = "dist",
        onefile: bool = False,
    ) -> None:
        self.entry_point = entry_point
        self.output_name = output_name
        self.output_dir = Path(output_dir)
        self.onefile = onefile

    def build_command(self) -> List[str]:
        """Constructs the Nuitka compilation command line arguments."""
        runner_script = Path(__file__).resolve().parent / "nuitka_runner.py"
        cmd = [
            sys.executable,
            str(runner_script),
            "--assume-yes-for-downloads",
            "--mingw64",
            "--lto=yes",
            "--disable-cache=ccache",
            "--windows-console-mode=attach",
            "--enable-plugin=tk-inter",
            "--include-package=openrgb_flowers",
            "--include-package=pystray",
            "--include-package=PIL",
            "--include-package=openrgb",
            "--include-module=hid",
            "--company-name=OpenRGB Community",
            "--product-name=OpenRGB Flowers Blooming",
            "--file-version=1.0.0.0",
            "--product-version=1.0.0.0",
            "--file-description=OpenRGB Flowers Blooming & Redragon RGB Controller (C++ Native)",
            "--copyright=Copyright (C) 2026 OpenRGB Community Contributors",
            f"--output-dir={self.output_dir}",
            f"--output-filename={self.output_name}",
        ]

        if self.onefile:
            cmd.append("--onefile")
        else:
            cmd.append("--standalone")

        cmd.append(self.entry_point)
        return cmd

    def _cleanup_unwanted_files(self, target_dir: Path) -> None:
        """Removes any obsolete duplicate executables to strictly enforce a single binary."""
        unwanted = [
            target_dir / "RedragonFlowers.exe",
            target_dir / "RedragonRGB.exe",
            target_dir / "OpenRGBFlowers.exe",
        ]
        for item in unwanted:
            if item.exists() and item.name != self.output_name:
                try:
                    item.unlink()
                except Exception:
                    pass

    def cleanup_mode_conflicts(self) -> None:
        """Removes stale artifacts from opposing compilation modes to ensure exactly one binary."""
        if self.onefile:
            # When compiling onefile, remove any conflicting standalone portable folder and zip
            portable_dir = self.output_dir / "FlowersBlooming_Portable"
            portable_zip = self.output_dir / "FlowersBlooming_Portable.zip"
            if portable_dir.exists():
                shutil.rmtree(portable_dir, ignore_errors=True)
            if portable_zip.exists():
                try:
                    portable_zip.unlink()
                except Exception:
                    pass
        else:
            # When compiling standalone, remove any conflicting root onefile executable in dist
            root_exe = self.output_dir / self.output_name
            if root_exe.exists():
                try:
                    root_exe.unlink()
                except Exception:
                    pass

    def prepare_build_target(self) -> None:
        """Prepares dist directory and removes stale target before compilation starts."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        ProcessManager.terminate_processes([self.output_name, "RedragonFlowers.exe", "OpenRGBFlowers.exe"])
        self.cleanup_mode_conflicts()
        if self.onefile:
            old_target = self.output_dir / self.output_name
            if old_target.exists():
                try:
                    old_target.unlink()
                except Exception:
                    pass

    def run(self) -> int:
        """Executes compilation, organizes artifacts, and ensures a single executable is produced."""
        print(f"[Nuitka] Iniciando compilacao nativa C++ para {self.output_name}...")
        self.prepare_build_target()

        cmd = self.build_command()
        print("[Nuitka] Executando comando de compilacao com GCC / MinGW-w64...")
        result = subprocess.run(cmd)

        if result.returncode != 0:
            print(f"[Nuitka ERROR] Falha na compilacao com codigo {result.returncode}")
            return result.returncode

        if self.onefile:
            output_file = self.output_dir / self.output_name
            if output_file.exists():
                self._cleanup_unwanted_files(self.output_dir)
                self.cleanup_mode_conflicts()

                entry_stem = Path(self.entry_point).stem
                # Cleanup temporary build directories
                for temp_dir in [
                    self.output_dir / f"{entry_stem}.build",
                    self.output_dir / f"{entry_stem}.dist",
                    self.output_dir / f"{entry_stem}.onefile-build",
                    self.output_dir / "launcher.build",
                    self.output_dir / "launcher.dist",
                    self.output_dir / "launcher.onefile-build",
                ]:
                    if temp_dir.exists():
                        shutil.rmtree(temp_dir, ignore_errors=True)

                print(f"[Nuitka SUCCESS] Executavel unico C++ Onefile gerado: {output_file.resolve()}")
                return 0
        else:
            entry_stem = Path(self.entry_point).stem
            raw_dist = self.output_dir / f"{entry_stem}.dist"
            if not raw_dist.exists() and (self.output_dir / "launcher.dist").exists():
                raw_dist = self.output_dir / "launcher.dist"

            portable_dir = self.output_dir / "FlowersBlooming_Portable"

            if raw_dist.exists():
                if portable_dir.exists():
                    shutil.rmtree(portable_dir, ignore_errors=True)
                raw_dist.rename(portable_dir)

            if portable_dir.exists():
                portable_exe = portable_dir / self.output_name
                self._cleanup_unwanted_files(portable_dir)
                self._cleanup_unwanted_files(self.output_dir)
                self.cleanup_mode_conflicts()

                # Clean up build cache directory
                for build_cache in [
                    self.output_dir / f"{entry_stem}.build",
                    self.output_dir / "launcher.build",
                ]:
                    if build_cache.exists():
                        shutil.rmtree(build_cache, ignore_errors=True)

                # Generate clean ZIP archive
                zip_path = shutil.make_archive(
                    str(self.output_dir / "FlowersBlooming_Portable"),
                    "zip",
                    root_dir=str(self.output_dir),
                    base_dir="FlowersBlooming_Portable",
                )

                print("[Nuitka SUCCESS] Pasta Portatil Standalone gerada com sucesso:")
                print(f"  -> Diretorio: {portable_dir.resolve()}")
                print(f"  -> Executavel unico principal: {portable_exe.resolve()}")
                print(f"  -> Arquivo zip para distribuicao: {Path(zip_path).resolve()}")
                return 0

        print("[Nuitka ERROR] Executavel nao encontrado apos compilacao.")
        return 1
