"""Process management utilities for build scripts."""
from __future__ import annotations

import subprocess
from typing import Sequence


class ProcessManager:
    """Responsible for terminating existing running process instances before build."""

    @staticmethod
    def terminate_processes(image_names: Sequence[str]) -> None:
        """Terminates processes by image name safely without throwing exceptions."""
        for name in image_names:
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", name],
                    capture_output=True,
                    check=False,
                )
            except Exception:
                pass
