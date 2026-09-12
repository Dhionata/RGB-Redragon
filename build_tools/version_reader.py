"""Version extraction utility respecting SOLID (Single Responsibility) and DRY."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


class VersionReader:
    """Extracts project version from metadata files without importing the whole package."""

    DEFAULT_VERSION = "1.0.0"

    @classmethod
    def get_version(cls, root_dir: Optional[Path] = None) -> str:
        """Retrieves version string from pyproject.toml or falls back to DEFAULT_VERSION."""
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent.parent

        pyproject_file = root_dir / "pyproject.toml"
        if pyproject_file.is_file():
            try:
                content = pyproject_file.read_text(encoding="utf-8")
                # Try tomllib (Python 3.11+) or tomli (Python 3.10)
                try:
                    try:
                        import tomllib  # type: ignore[import-not-found]
                    except ImportError:
                        import tomli as tomllib  # type: ignore[no-redef]
                    data = tomllib.loads(content)
                    ver = data.get("project", {}).get("version")
                    if ver:
                        return str(ver).strip()
                except Exception:
                    pass

                # Fallback: Match version = "x.y.z" specifically inside [project] section
                project_section = re.search(r'\[project\](.*?)(?=\n\[|\Z)', content, re.DOTALL)
                target_text = project_section.group(1) if project_section else content
                match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', target_text)
                if match:
                    return match.group(1).strip()
            except Exception:
                pass

        return cls.DEFAULT_VERSION
