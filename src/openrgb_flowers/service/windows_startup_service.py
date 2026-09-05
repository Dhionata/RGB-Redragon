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

    def enable(self, extra_args: Optional[str] = "--autostart") -> bool:
        """Registers the application to execute on logon."""
        if not self._is_windows:
            logger.warning("Autostart registration is only supported on Windows.")
            return False

        cmd = self._resolve_launch_command(extra_args or "--autostart")
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
        """Constructs an invisible/silent startup command line."""
        if getattr(sys, "frozen", False):
            # Running as a compiled PyInstaller standalone .exe
            exe_path = Path(sys.executable).resolve()
            return f'"{exe_path}" {extra_args}'

        # Running via Python interpreter: prefer pythonw.exe to prevent terminal window
        py_exe = Path(sys.executable).resolve()
        pyw_exe = py_exe.parent / "pythonw.exe"
        chosen_python = pyw_exe if pyw_exe.exists() else py_exe

        # Point to package working directory or module
        return f'"{chosen_python}" -m openrgb_flowers {extra_args}'
