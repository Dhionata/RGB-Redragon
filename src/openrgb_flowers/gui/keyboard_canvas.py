"""Interactive real-time visualizer canvas displaying RGB keyboard keys with responsive layout."""
from __future__ import annotations
import tkinter as tk
from typing import List, Optional
import numpy as np

from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.models.render_frame import RenderFrame


class KeyboardCanvas(tk.Frame):
    """Tkinter Canvas component rendering physical keyboard layout with real-time RGB key illumination.

    Features responsive resizing, aspect-ratio preservation, centered positioning,
    dynamic keycap font scaling, and complete layout key naming.
    """

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

        # Bind window resize / maximize event to dynamically rescale the canvas
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        self._rect_ids: List[int] = []
        self._text_ids: List[Optional[int]] = []
        self._cached_colors: List[str] = []
        self._build_keys()

    def update_layout(self, layout_provider: ILayoutProvider) -> None:
        """Rebuilds keyboard canvas when device layout changes."""
        self._layout = layout_provider
        self._build_keys()

    def _on_canvas_configure(self, event: tk.Event) -> None:
        """Dynamically rescales and recenters keyboard when canvas size changes (e.g. window maximized)."""
        new_w = event.width
        new_h = event.height
        if new_w < 50 or new_h < 50:
            return

        # Avoid redundant rebuilds on micro jitter
        if abs(new_w - self._width) > 6 or abs(new_h - self._height) > 6:
            self._width = new_w
            self._height = new_h
            self._build_keys()

    def _build_keys(self) -> None:
        """Draws keycap rectangles matching physical layout coordinates, dynamically centered and scaled."""
        previous_colors = list(self._cached_colors)
        self._canvas.delete("all")
        self._rect_ids.clear()
        self._text_ids.clear()
        self._cached_colors.clear()

        keys = self._layout.get_coordinates()
        if not keys:
            return

        self._cached_colors = [""] * len(keys)

        pad_x = 20.0
        pad_y = 16.0
        avail_w = max(100.0, float(self._width) - (pad_x * 2.0))
        avail_h = max(60.0, float(self._height) - (pad_y * 2.0))

        # Standard full-size keyboard spans 22 columns by 6 rows.
        # Compute uniform unit size preserving physical aspect ratio without stretching keys into needles.
        unit_w = avail_w / 23.2
        unit_h = avail_h / 6.4
        unit_size = max(16.0, min(unit_w, unit_h))

        key_w = unit_size * 0.90
        key_h = unit_size * 0.90

        # Total keyboard bounding box
        total_kb_w = 21.0 * unit_size + key_w
        total_kb_h = 5.0 * unit_size + key_h

        # Center inside canvas
        offset_x = max(pad_x, (float(self._width) - total_kb_w) / 2.0)
        offset_y = max(pad_y, (float(self._height) - total_kb_h) / 2.0)

        # Scale font size dynamically with key size
        font_size = max(6, min(11, int(key_w / 3.4)))
        font_spec = ("Segoe UI", font_size, "bold")

        for idx, key in enumerate(keys):
            px = offset_x + (key.x * (total_kb_w - key_w))
            py = offset_y + (key.y * (total_kb_h - key_h))

            # Maintain active color across canvas rebuilds to prevent visual flicker
            fill_color = self.KEY_DEFAULT_COLOR
            if idx < len(previous_colors) and previous_colors[idx]:
                fill_color = previous_colors[idx]
                self._cached_colors[idx] = fill_color

            # Keycap body
            rect_id = self._canvas.create_rectangle(
                px,
                py,
                px + key_w,
                py + key_h,
                fill=fill_color,
                outline=self.KEY_BORDER_COLOR,
                width=1,
            )
            self._rect_ids.append(rect_id)

            # Keycap label
            label = self._short_label(key.name)
            if label and key_w >= 16.0:
                t_id = self._canvas.create_text(
                    px + (key_w / 2.0),
                    py + (key_h / 2.0),
                    text=label,
                    fill="#626c7e",
                    font=font_spec,
                )
                self._text_ids.append(t_id)
            else:
                self._text_ids.append(None)

    @staticmethod
    def _short_label(name: str) -> str:
        """Returns concise key abbreviation for canvas display, identifying every numpad key and symbol."""
        if not name:
            return ""

        clean = name[4:] if name.startswith("Key_") else name
        lower = clean.lower()

        explicit_map = {
            "escape": "ESC",
            "backspace": "BKSP",
            "capslock": "CAPS",
            "enter": "ENTER",
            "leftshift": "SHIFT",
            "rightshift": "SHIFT",
            "leftcontrol": "CTRL",
            "rightcontrol": "CTRL",
            "leftwindows": "WIN",
            "rightwindows": "WIN",
            "leftalt": "ALT",
            "rightalt": "ALT",
            "space": "SPACE",
            "printscreen": "PRT",
            "scrolllock": "SCR",
            "pause": "PAU",
            "insert": "INS",
            "delete": "DEL",
            "home": "HOME",
            "end": "END",
            "pageup": "PGUP",
            "pagedown": "PGDN",
            # Numpad specific keys
            "numlock": "NLK",
            "numslash": "/",
            "numdivide": "/",
            "numasterisk": "*",
            "nummultiply": "*",
            "numminus": "-",
            "numsubtract": "-",
            "numplus": "+",
            "numadd": "+",
            "numenter": "ENT",
            "numperiod": ".",
            "numdecimal": ".",
            "num0": "0",
            "num1": "1",
            "num2": "2",
            "num3": "3",
            "num4": "4",
            "num5": "5",
            "num6": "6",
            "num7": "7",
            "num8": "8",
            "num9": "9",
            # Directional Arrows
            "uparrow": "▲",
            "downarrow": "▼",
            "leftarrow": "◄",
            "rightarrow": "►",
            "up": "▲",
            "down": "▼",
            "left": "◄",
            "right": "►",
            # Punctuation & Symbols
            "grave": "`",
            "minus": "-",
            "equal": "=",
            "equals": "=",
            "leftbracket": "[",
            "rightbracket": "]",
            "semicolon": ";",
            "apostrophe": "'",
            "backslash": "\\",
            "intlbackslash": "\\",
            "comma": ",",
            "period": ".",
            "slash": "/",
            "intlro": "/",
            "tab": "TAB",
            "fn": "FN",
            "menu": "MENU",
        }

        if lower in explicit_map:
            return explicit_map[lower]

        # Handle any other "NumX" keys dynamically (e.g. Num8 -> 8)
        if lower.startswith("num") and len(clean) > 3:
            return clean[3:].upper()

        if len(clean) <= 4:
            return clean.upper()

        return clean[:3].upper()

    def update_frame(self, frame: RenderFrame) -> None:
        """Thread-safe update of keycap fill colors on the canvas with zero-work bypass when hidden."""
        if not self.winfo_viewable():
            return

        colors = frame.colors
        num_keys = min(len(self._rect_ids), colors.shape[0])

        for i in range(num_keys):
            r = int(colors[i, 0])
            g = int(colors[i, 1])
            b = int(colors[i, 2])
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            if i >= len(self._cached_colors) or hex_color != self._cached_colors[i]:
                if i < len(self._cached_colors):
                    self._cached_colors[i] = hex_color
                self._canvas.itemconfig(self._rect_ids[i], fill=hex_color)
