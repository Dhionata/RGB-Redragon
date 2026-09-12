import sys
from pathlib import Path

# Ensure src directory is available in sys.path when running directly from source
_SRC_DIR = Path(__file__).resolve().parent / "src"
if _SRC_DIR.is_dir() and str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from openrgb_flowers.cli.main import main
from openrgb_flowers.core.crash_handler import CrashHandler


def _entrypoint() -> int:
    """Configures default CLI parameters and runs the main application."""
    if len(sys.argv) == 1:
        sys.argv.append("--gui")
    return main()


if __name__ == "__main__":
    sys.exit(CrashHandler.run_safely(_entrypoint))
