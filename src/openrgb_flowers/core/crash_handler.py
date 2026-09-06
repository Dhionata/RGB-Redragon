"""Crash handling and unexpected error logging for desktop execution."""
from __future__ import annotations

import ctypes
import datetime
import sys
import traceback
from pathlib import Path
from typing import Callable, Optional


class CrashHandler:
    """Provides centralized crash reporting, logging, and visual dialogs for GUI launchers."""

    @staticmethod
    def get_default_log_path() -> Path:
        """Determines the appropriate crash log file path."""
        try:
            cwd_log = Path.cwd() / "crash.log"
            # Test write access
            with open(cwd_log, "a", encoding="utf-8") as _:
                pass
            return cwd_log
        except Exception:
            fallback = Path.home() / ".openrgb_flowers"
            fallback.mkdir(parents=True, exist_ok=True)
            return fallback / "crash.log"

    @staticmethod
    def log_exception(exc: BaseException, log_path: Optional[Path] = None) -> Path:
        """Writes the unhandled exception and traceback to a persistent crash log."""
        target_path = log_path or CrashHandler.get_default_log_path()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tb = traceback.format_exc()

        content = (
            f"\n{'=' * 60}\n"
            f"CRASH REPORT - {timestamp}\n"
            f"Python: {sys.version}\n"
            f"Platform: {sys.platform}\n"
            f"Exception: {type(exc).__name__}: {exc}\n"
            f"{'=' * 60}\n"
            f"{tb}\n"
        )

        try:
            with open(target_path, "a", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass

        return target_path

    @staticmethod
    def show_error_dialog(title: str, message: str) -> None:
        """Displays a native graphical message box on Windows, or logs to stderr."""
        if sys.platform == "win32":
            try:
                # MB_OK (0x0) | MB_ICONERROR (0x10) | MB_SYSTEMMODAL (0x1000)
                flags = 0x00000000 | 0x00000010 | 0x00001000
                ctypes.windll.user32.MessageBoxW(0, message, title, flags)
                return
            except Exception:
                pass

        sys.stderr.write(f"\n[{title}] {message}\n")

    @classmethod
    def run_safely(cls, entrypoint: Callable[[], int]) -> int:
        """Executes the given entrypoint with comprehensive crash catching and reporting."""
        try:
            return entrypoint()
        except SystemExit as se:
            return se.code if isinstance(se.code, int) else 0
        except KeyboardInterrupt:
            return 0
        except BaseException as exc:
            log_file = cls.log_exception(exc)
            dialog_msg = (
                "O aplicativo encontrou um erro inesperado e precisou ser encerrado.\n\n"
                f"Erro: {type(exc).__name__}: {exc}\n\n"
                f"Log de depuração gravado em:\n{log_file.resolve()}\n\n"
                "Dica: Se o antivírus (Avast) bloqueou a inicialização, adicione a pasta "
                "nas exceções de segurança."
            )
            cls.show_error_dialog("Flowers Blooming - Erro de Execução", dialog_msg)
            return 1
