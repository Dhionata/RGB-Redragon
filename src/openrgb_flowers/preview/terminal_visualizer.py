"""Terminal live preview visualizer with 24-bit TrueColor ANSI escape codes."""
from __future__ import annotations
import os
import sys
from typing import List
from openrgb_flowers.core.interfaces.i_visualizer import IVisualizer
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.core.models.key_coordinate import KeyCoordinate

ESC = chr(27)


class TerminalVisualizer(IVisualizer):
    """Visualizes keyboard keys and blooming flowers directly inside the user terminal.

    Uses 24-bit TrueColor ANSI escape codes to render a 2D matrix of the keyboard
    layout with vibrant organic colors in real-time.
    """

    def __init__(self, key_symbol: str = "■") -> None:
        self._key_symbol = key_symbol
        self._grid_rows: List[List[KeyCoordinate]] = []
        self._initialized = False

    def _setup_grid(self, layout: ILayoutProvider) -> None:
        if os.name == "nt":
            try:
                os.system("")
            except Exception:
                pass

        keys = layout.get_coordinates()
        rows_dict: dict[int, list[KeyCoordinate]] = {}
        for k in keys:
            rows_dict.setdefault(k.row, []).append(k)

        sorted_rows = sorted(rows_dict.keys())
        self._grid_rows = [sorted(rows_dict[r], key=lambda k: k.x) for r in sorted_rows]
        self._initialized = True
        sys.stdout.write(f"{ESC}[2J{ESC}[H")
        sys.stdout.flush()

    def render(self, frame: RenderFrame, layout: ILayoutProvider, active_blooms: int, fps: float) -> None:
        if not self._initialized:
            self._setup_grid(layout)

        colors = frame.colors
        lines: List[str] = []

        header = f"{ESC}[1;32m🌸 OpenRGB Flowers Blooming Preview{ESC}[0m | Frame: {frame.frame_index} | Blooms: {active_blooms} | Target FPS: {fps:.1f}"
        lines.append(header)
        lines.append("-" * 74)

        for row_keys in self._grid_rows:
            row_str = ""
            last_x = 0.0
            for k in row_keys:
                gap = k.x - last_x
                if gap > 0.05:
                    spaces = int(round(gap * 28))
                    row_str += " " * max(1, spaces)

                idx = k.index
                if idx < colors.shape[0]:
                    r = colors[idx, 0]
                    g = colors[idx, 1]
                    b = colors[idx, 2]
                else:
                    r, g, b = 0, 0, 0

                row_str += f"{ESC}[38;2;{r};{g};{b}m{self._key_symbol} {ESC}[0m"
                last_x = k.x

            lines.append(row_str)

        lines.append("-" * 74)
        lines.append("Press Ctrl+C to stop simulation.")

        output = f"{ESC}[H" + "\n".join(lines) + "\n"
        sys.stdout.write(output)
        sys.stdout.flush()

    def close(self) -> None:
        sys.stdout.write(f"{ESC}[0m\n")
        sys.stdout.flush()
