"""Standalone application launcher for compiled executables and direct execution."""
import sys
from openrgb_flowers.cli.main import main
from openrgb_flowers.core.crash_handler import CrashHandler


def _entrypoint() -> int:
    """Configures default CLI parameters and runs the main application."""
    if len(sys.argv) == 1:
        sys.argv.append("--gui")
    return main()


if __name__ == "__main__":
    sys.exit(CrashHandler.run_safely(_entrypoint))
