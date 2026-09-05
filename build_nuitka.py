"""Build standalone native Windows executable using Nuitka (C++ compilation).

Complies with SOLID & DRY principles, separating build steps and process termination.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Sequence


class ProcessManager:
    """Responsible for ensuring target executable files are not locked by running processes."""

    @staticmethod
    def terminate_processes(image_names: Sequence[str]) -> None:
        for name in image_names:
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", name],
                    capture_output=True,
                    check=False,
                )
            except Exception:
                pass


class NuitkaBuilder:
    """Encapsulates Nuitka C++ compilation configuration and execution."""

    def __init__(
        self,
        entry_point: str = "launcher.py",
        output_name: str = "FlowersBlooming.exe",
        output_dir: str = "dist",
        onefile: bool = True,
    ) -> None:
        self.entry_point = entry_point
        self.output_name = output_name
        self.output_dir = Path(output_dir)
        self.onefile = onefile

    def build_command(self) -> List[str]:
        cmd = [
            sys.executable,
            "-m",
            "nuitka",
            "--assume-yes-for-downloads",
            "--windows-console-mode=disable",
            "--enable-plugin=tk-inter",
            "--include-package=openrgb_flowers",
            "--include-module=hid",
            "--include-module=openrgb",
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

    def run(self) -> int:
        print(f"[Nuitka] Iniciando compilacao nativa em C++ para {self.output_name}...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        ProcessManager.terminate_processes([self.output_name, "RedragonFlowers.exe"])

        cmd = self.build_command()
        print("[Nuitka] Executando comando de compilacao...")
        result = subprocess.run(cmd)

        if result.returncode != 0:
            print(f"[Nuitka ERROR] Falha na compilacao com codigo {result.returncode}")
            return result.returncode

        output_file = self.output_dir / self.output_name
        if output_file.exists():
            alias_file = self.output_dir / "RedragonFlowers.exe"
            try:
                shutil.copyfile(output_file, alias_file)
                print(f"[Nuitka SUCCESS] Criado alias adicional: {alias_file}")
            except Exception:
                pass

            # Cleanup temporary build directories to keep dist/ clean
            for temp_dir in [
                self.output_dir / "launcher.build",
                self.output_dir / "launcher.dist",
                self.output_dir / "launcher.onefile-build",
            ]:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)

            print(f"[Nuitka SUCCESS] Executavel C++ gerado com sucesso: {output_file}")
            return 0

        print("[Nuitka ERROR] Executavel nao encontrado apos compilacao.")
        return 1


def main() -> int:
    builder = NuitkaBuilder()
    return builder.run()


if __name__ == "__main__":
    sys.exit(main())
