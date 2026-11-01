"""Windows startup registration service using HKCU Run registry key."""
from __future__ import annotations
import logging
import os
import platform
import sys
from pathlib import Path
from typing import Optional

from openrgb_flowers.core.interfaces.autostart_service import IAutoStartService

logger = logging.getLogger("openrgb_flowers.service.windows_startup")


class WindowsStartupService(IAutoStartService):
    """Manages Windows auto-start on user logon without requiring administrator privileges."""

    REG_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "OpenRGBFlowers"
    DEFAULT_ARGS = "--autostart --tray"

    def __init__(self, app_name: Optional[str] = None) -> None:
        self._app_name = app_name or self.APP_NAME
        self._is_windows = platform.system().lower() == "windows"

    def is_enabled(self) -> bool:
        """Checks if the registry key exists in HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run."""
        if not self._is_windows:
            return False

        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_KEY_PATH, 0, winreg.KEY_READ) as key:
                try:
                    val, _ = winreg.QueryValueEx(key, self._app_name)
                    return bool(val)
                except FileNotFoundError:
                    return False
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.warning(f"Failed to check autostart registry key: {e}")
            return False

    def enable(self, extra_args: Optional[str] = None) -> bool:
        """Registers the application to execute on logon."""
        if not self._is_windows:
            logger.warning("Autostart registration is only supported on Windows.")
            return False

        args_to_use = extra_args if extra_args is not None else self.DEFAULT_ARGS
        cmd = self._resolve_launch_command(args_to_use)
        try:
            import winreg
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, self.REG_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self._app_name, 0, winreg.REG_SZ, cmd)
            logger.info(f"Registered Windows autostart: '{self._app_name}' -> '{cmd}'")
            return True
        except Exception as e:
            logger.error(f"Failed to enable autostart registry key: {e}")
            return False

    def disable(self) -> bool:
        """Removes the application from HKCU Run registry key."""
        if not self._is_windows:
            return False

        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:
                try:
                    winreg.DeleteValue(key, self._app_name)
                    logger.info(f"Removed Windows autostart: '{self._app_name}'")
                    return True
                except FileNotFoundError:
                    return True
        except FileNotFoundError:
            return True
        except Exception as e:
            logger.error(f"Failed to disable autostart registry key: {e}")
            return False

    def _resolve_launch_command(self, extra_args: str) -> str:
        """Constructs an invisible/silent startup command line with absolute paths."""
        if getattr(sys, "frozen", False):
            # Running as a compiled PyInstaller / Nuitka standalone .exe
            exe_path = Path(sys.executable).resolve()
            return f'"{exe_path}" {extra_args}'

        # If compiled standalone executable exists in dist, prefer it
        root_dir = Path(__file__).resolve().parent.parent.parent.parent
        portable_exe = root_dir / "dist" / "FlowersBlooming_Portable" / "FlowersBlooming.exe"
        if portable_exe.is_file():
            return f'"{portable_exe.resolve()}" {extra_args}'
        dist_exe = root_dir / "dist" / "FlowersBlooming.exe"
        if dist_exe.is_file():
            return f'"{dist_exe.resolve()}" {extra_args}'

        # Running via Python interpreter: prefer pythonw.exe to prevent terminal window
        py_exe = Path(sys.executable).resolve()
        pyw_exe = py_exe.parent / "pythonw.exe"
        chosen_python = pyw_exe if pyw_exe.exists() else py_exe

        # Point directly to launcher.py with absolute path so sys.path is guaranteed
        launcher_file = root_dir / "launcher.py"
        if launcher_file.is_file():
            return f'"{chosen_python}" "{launcher_file.resolve()}" {extra_args}'

        # Fallback to module
        return f'"{chosen_python}" -m openrgb_flowers {extra_args}'
