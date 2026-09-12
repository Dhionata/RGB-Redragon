"""Inno Setup compiler (ISCC.exe) detection and path resolution.

Complies with SOLID (Single Responsibility Principle):
Responsible solely for locating the Inno Setup executable and providing
troubleshooting / installation guidance when not found.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import List, Optional


class InnoSetupLocator:
    """Detects and resolves the path to the Inno Setup Compiler (ISCC.exe)."""

    EXE_NAME = "ISCC.exe"

    def __init__(self, search_paths: Optional[List[Path]] = None) -> None:
        self._custom_search_paths = search_paths or []

    def get_candidate_paths(self) -> List[Path]:
        """Returns ordered list of candidate filesystem paths where ISCC might be installed."""
        candidates: List[Path] = []

        # Add user-provided custom paths first
        candidates.extend(self._custom_search_paths)

        # Standard Windows environment folders
        env_vars = ["ProgramFiles(x86)", "ProgramFiles", "LocalAppData"]
        subfolders = [
            Path("Inno Setup 6") / self.EXE_NAME,
            Path("Programs") / "Inno Setup 6" / self.EXE_NAME,
            Path("Inno Setup 5") / self.EXE_NAME,
        ]

        for env_var in env_vars:
            base_val = os.environ.get(env_var)
            if base_val:
                base_dir = Path(base_val)
                for sub in subfolders:
                    candidates.append(base_dir / sub)

        # Direct C:\ fallbacks in case env vars differ
        direct_roots = [
            Path(r"C:\Program Files (x86)\Inno Setup 6") / self.EXE_NAME,
            Path(r"C:\Program Files\Inno Setup 6") / self.EXE_NAME,
            Path(r"C:\Program Files (x86)\Inno Setup 5") / self.EXE_NAME,
            Path(r"C:\Program Files\Inno Setup 5") / self.EXE_NAME,
        ]
        for direct in direct_roots:
            if direct not in candidates:
                candidates.append(direct)

        return candidates

    def _check_registry(self) -> Optional[Path]:
        """Checks Windows Registry for Inno Setup installation path."""
        try:
            import winreg  # type: ignore

            # 1. App Paths
            app_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\ISCC.exe"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\ISCC.exe"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\ISCC.exe"),
            ]
            for root, subkey in app_paths:
                try:
                    with winreg.OpenKey(root, subkey) as key:
                        val, _ = winreg.QueryValueEx(key, "")
                        if val:
                            clean_val = str(val).strip('"\'').strip()
                            if clean_val and Path(clean_val).is_file():
                                return Path(clean_val)
                except OSError:
                    continue

            # 2. Uninstall keys
            uninstall_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1"),
            ]
            for root, subkey in uninstall_keys:
                try:
                    with winreg.OpenKey(root, subkey) as key:
                        install_loc, _ = winreg.QueryValueEx(key, "InstallLocation")
                        if install_loc:
                            clean_loc = str(install_loc).strip('"\'').strip()
                            candidate = Path(clean_loc) / self.EXE_NAME
                            if candidate.is_file():
                                return candidate
                except OSError:
                    continue
        except Exception:
            pass

        return None

    def find_iscc(self, explicit_path: Optional[str | Path] = None) -> Optional[Path]:
        """Locates the ISCC executable.

        Search precedence:
        1. Explicit path parameter (if valid file)
        2. System PATH environment variable
        3. Standard Program Files and LocalAppData directories
        4. Windows Registry keys
        """
        # 1. Explicit path
        if explicit_path:
            clean_explicit = str(explicit_path).strip('"\'').strip()
            p = Path(clean_explicit)
            if p.is_file():
                return p.resolve()
            if p.is_dir() and (p / self.EXE_NAME).is_file():
                return (p / self.EXE_NAME).resolve()

        # 2. System PATH
        which_path = shutil.which("iscc") or shutil.which("iscc.exe") or shutil.which("ISCC.exe")
        if which_path:
            return Path(which_path).resolve()

        # 3. Known filesystem candidates
        for candidate in self.get_candidate_paths():
            if candidate.is_file():
                return candidate.resolve()

        # 4. Windows Registry
        reg_path = self._check_registry()
        if reg_path and reg_path.is_file():
            return reg_path.resolve()

        return None

    @staticmethod
    def get_installation_guidance() -> str:
        """Returns clear, user-friendly instructions on how to install Inno Setup."""
        return (
            "========================================================================\n"
            "[AVISO] O compilador do Inno Setup (ISCC.exe) nao foi encontrado no sistema.\n"
            "========================================================================\n"
            "Para gerar o instalador executavel (.exe), instale o Inno Setup 6:\n\n"
            "  Opcao 1 (Recomendada via Terminal / PowerShell):\n"
            "    winget install JRSoftware.InnoSetup\n\n"
            "  Opcao 2 (Chocolatey):\n"
            "    choco install innosetup\n\n"
            "  Opcao 3 (Download direto oficial):\n"
            "    https://jrsoftware.org/isdl.php\n\n"
            "Apos instalar, feche e abra novamente este terminal ou execute gerar_instalador.bat.\n"
            "========================================================================"
        )
