"""Interactive real-time visualizer canvas displaying RGB keyboard keys."""
from __future__ import annotations
import tkinter as tk
from typing import List, Optional
import numpy as np

from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.models.render_frame import RenderFrame


class KeyboardCanvas(tk.Frame):
    """Tkinter Canvas component rendering physical keyboard layout with real-time RGB key illumination."""

    BG_COLOR = "#121418"
    KEY_DEFAULT_COLOR = "#1e222b"
    KEY_BORDER_COLOR = "#2a303c"

    def __init__(
        self,
        parent: tk.Widget,
        layout_provider: ILayoutProvider,
        width: int = 860,
        height: int = 240,
        **kwargs,
    ) -> None:
        super().__init__(parent, bg=self.BG_COLOR, **kwargs)
        self._layout = layout_provider
        self._width = width
        self._height = height

        self._canvas = tk.Canvas(
            self,
            width=self._width,
            height=self._height,
            bg=self.BG_COLOR,
            highlightthickness=1,
            highlightbackground="#232834",
        )
        self._canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self._rect_ids: List[int] = []
        self._text_ids: List[Optional[int]] = []
        self._build_keys()

    def update_layout(self, layout_provider: ILayoutProvider) -> None:
        """Rebuilds keyboard canvas when device layout changes."""
        self._layout = layout_provider
        self._build_keys()

    def _build_keys(self) -> None:
        """Draws keycap rectangles matching physical layout coordinates."""
        self._canvas.delete("all")
        self._rect_ids.clear()
        self._text_ids.clear()

        keys = self._layout.get_coordinates()
        if not keys:
            return

        pad_x = 24
        pad_y = 20
        usable_w = self._width - (pad_x * 2)
        usable_h = self._height - (pad_y * 2)

        # Base keycap dimensions
        key_w = max(18.0, usable_w / 23.5)
        key_h = max(18.0, usable_h / 6.5)

        for key in keys:
            px = pad_x + (key.x * (usable_w - key_w))
            py = pad_y + (key.y * (usable_h - key_h))

            # Keycap body
            rect_id = self._canvas.create_rectangle(
                px,
                py,
                px + key_w,
                py + key_h,
                fill=self.KEY_DEFAULT_COLOR,
                outline=self.KEY_BORDER_COLOR,
                width=1,
            )
            self._rect_ids.append(rect_id)

            # Short key label if available
            label = self._short_label(key.name)
            if label and key_w >= 20:
                t_id = self._canvas.create_text(
                    px + (key_w / 2.0),
                    py + (key_h / 2.0),
                    text=label,
                    fill="#626c7e",
                    font=("Segoe UI", 7, "bold"),
                )
                self._text_ids.append(t_id)
            else:
                self._text_ids.append(None)

    @staticmethod
    def _short_label(name: str) -> str:
        """Returns concise key abbreviation for canvas display."""
        if not name or name.startswith("Key_"):
            return ""
        name_lower = name.lower()
        abbrevs = {
            "escape": "ESC",
            "backspace": "BKSP",
            "capslock": "CAPS",
            "enter": "RET",
            "leftshift": "SHF",
            "rightshift": "SHF",
            "leftcontrol": "CTRL",
            "rightcontrol": "CTRL",
            "leftwindows": "WIN",
            "leftalt": "ALT",
            "rightalt": "ALT",
            "space": "____",
            "numlock": "NUM",
            "printscreen": "PRT",
            "scrolllock": "SCR",
            "pause": "PAU",
            "insert": "INS",
            "delete": "DEL",
            "pageup": "PGU",
            "pagedown": "PGD",
        }
        return abbrevs.get(name_lower, name[:3].upper())

    def update_frame(self, frame: RenderFrame) -> None:
        """Thread-safe update of keycap fill colors on the canvas."""
        colors = frame.colors
        num_keys = min(len(self._rect_ids), colors.shape[0])

        for i in range(num_keys):
            r = int(colors[i, 0])
            g = int(colors[i, 1])
            b = int(colors[i, 2])
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self._canvas.itemconfig(self._rect_ids[i], fill=hex_color)
