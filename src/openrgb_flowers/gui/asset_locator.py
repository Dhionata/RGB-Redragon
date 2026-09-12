"""Asset locator service for resolving application icons and resources.

Complies with SOLID & DRY principles:
- Single Responsibility: Provides a single source of truth for resolving asset paths.
- Resilient: Searches frozen application directories, source trees, and working directories.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional


class AssetLocator:
    """Resolves filesystem paths for application assets across execution modes."""

    _cached_paths: dict[str, Optional[Path]] = {}

    @classmethod
    def get_asset_path(cls, filename: str) -> Optional[Path]:
        """Resolves the absolute path to an asset file, or returns None if not found."""
        if filename in cls._cached_paths:
            return cls._cached_paths[filename]

        search_locations = []

        # 1. PyInstaller extraction directory
        if hasattr(sys, "_MEIPASS"):
            search_locations.append(Path(sys._MEIPASS) / "assets" / filename)
            search_locations.append(Path(sys._MEIPASS) / filename)

        # 2. Executable parent directory (Nuitka standalone / Inno Setup install dir)
        exe_dir = Path(sys.executable).resolve().parent
        search_locations.append(exe_dir / "assets" / filename)
        search_locations.append(exe_dir / filename)

        # 3. Source repository root (openrgb_flowers/gui/../../assets/filename)
        source_root = Path(__file__).resolve().parent.parent.parent
        search_locations.append(source_root / "assets" / filename)

        # 4. Current working directory
        search_locations.append(Path.cwd() / "assets" / filename)
        search_locations.append(Path.cwd() / filename)

        for candidate in search_locations:
            if candidate.is_file():
                cls._cached_paths[filename] = candidate.resolve()
                return cls._cached_paths[filename]

        cls._cached_paths[filename] = None
        return None

    @classmethod
    def get_icon_ico_path(cls) -> Optional[Path]:
        """Returns the resolved Path to the official icon.ico, or None."""
        return cls.get_asset_path("icon.ico")

    @classmethod
    def get_icon_png_path(cls) -> Optional[Path]:
        """Returns the resolved Path to the official icon.png, or None."""
        return cls.get_asset_path("icon.png")
