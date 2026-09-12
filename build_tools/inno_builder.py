"""Encapsulates Inno Setup Compiler configuration and execution.

Complies with SOLID (SRP, OCP, DIP) and DRY principles.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

from build_tools.inno_locator import InnoSetupLocator
from build_tools.process_manager import ProcessManager


class InnoSetupBuilder:
    """Configures and runs Inno Setup Compiler to create a Windows installer executable."""

    def __init__(
        self,
        iss_file: str | Path = "installer.iss",
        source_dir: str | Path = "dist/FlowersBlooming_Portable",
        output_dir: str | Path = "dist",
        output_name: str = "FlowersBlooming_Setup",
        app_version: str = "1.0.0",
        main_executable: str = "FlowersBlooming.exe",
        locator: Optional[InnoSetupLocator] = None,
        custom_iscc_path: Optional[str | Path] = None,
    ) -> None:
        self.iss_file = Path(iss_file)
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        clean_output_name = str(output_name)
        if clean_output_name.lower().endswith(".exe"):
            clean_output_name = clean_output_name[:-4]
        self.output_name = clean_output_name
        self.app_version = app_version
        self.main_executable = main_executable
        self.locator = locator or InnoSetupLocator()
        self.custom_iscc_path = custom_iscc_path

    def get_iscc_path(self) -> Optional[Path]:
        """Resolves the ISCC executable path via the configured locator."""
        return self.locator.find_iscc(self.custom_iscc_path)

    def validate_prerequisites(self) -> Tuple[bool, str]:
        """Validates all required inputs before invoking the compiler."""
        if not self.iss_file.is_file():
            return False, f"Arquivo de script Inno Setup nao encontrado: {self.iss_file.resolve()}"

        if not self.source_dir.is_dir():
            return False, (
                f"Diretorio de origem nao encontrado: {self.source_dir.resolve()}.\n"
                "Execute primeiro a compilacao Nuitka standalone ('--standalone') para gerar este diretorio."
            )

        exe_path = self.source_dir / self.main_executable
        if not exe_path.is_file():
            return False, (
                f"Executavel principal '{self.main_executable}' nao encontrado em {self.source_dir.resolve()}.\n"
                "Verifique a compilacao Nuitka."
            )

        iscc = self.get_iscc_path()
        if not iscc:
            return False, self.locator.get_installation_guidance()

        return True, ""

    def build_command(self) -> List[str]:
        """Constructs the ISCC command line invocation with preprocessor definitions."""
        iscc = self.get_iscc_path()
        if not iscc:
            raise FileNotFoundError("ISCC.exe nao foi localizado no sistema.")

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        return [
            str(iscc),
            f"/DMyAppVersion={self.app_version}",
            f"/DSourceDir={self.source_dir.resolve()}",
            f"/DOutputDir={self.output_dir.resolve()}",
            f"/DOutputBaseFilename={self.output_name}",
            str(self.iss_file.resolve()),
        ]

    def run(self) -> int:
        """Executes installer compilation and verifies output artifact."""
        print(f"[Inno Setup] Iniciando geracao do instalador para versao {self.app_version}...")

        # Terminate any running installer or application instances to prevent file locking
        target_exe_name = f"{self.output_name}.exe"
        ProcessManager.terminate_processes([target_exe_name, self.main_executable])

        # Validate prerequisites
        valid, msg = self.validate_prerequisites()
        if not valid:
            print(f"[Inno Setup ERROR] {msg}")
            return 1

        cmd = self.build_command()
        print(f"[Inno Setup] Executando ISCC: {' '.join(cmd)}")
        result = subprocess.run(cmd)

        if result.returncode != 0:
            print(f"[Inno Setup ERROR] Falha no Inno Setup com codigo {result.returncode}")
            return result.returncode

        expected_installer = self.output_dir / target_exe_name
        if expected_installer.is_file():
            print("\n========================================================")
            print(" [Inno Setup SUCCESS] Instalador gerado com sucesso!")
            print(f" -> Arquivo: {expected_installer.resolve()}")
            print(f" -> Tamanho: {expected_installer.stat().st_size / (1024 * 1024):.2f} MB")
            print("========================================================\n")
            return 0

        print(f"[Inno Setup ERROR] Arquivo de instalador esperado nao foi encontrado: {expected_installer}")
        return 1
