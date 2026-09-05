"""Standalone application launcher for PyInstaller build and direct execution."""
import sys
from openrgb_flowers.cli.main import main

if __name__ == "__main__":
    # If launched with no CLI arguments (e.g. double-clicked from Explorer/Desktop), default to GUI
    if len(sys.argv) == 1:
        sys.argv.append("--gui")
    sys.exit(main())
