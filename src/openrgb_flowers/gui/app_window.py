"""Main graphical window for OpenRGB Flowers Blooming application."""
from __future__ import annotations
import logging
import queue
import tkinter as tk
from typing import Dict, Any, Optional

from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.hardware.k556_matrix_layout_provider import K556MatrixLayoutProvider
from openrgb_flowers.gui.keyboard_canvas import KeyboardCanvas
from openrgb_flowers.gui.control_panel import ControlPanel
from openrgb_flowers.gui.gui_runner import GuiRunner

logger = logging.getLogger("openrgb_flowers.gui.app")


class MainWindow(tk.Tk):
    """Modern dark-themed GUI dashboard for Redragon K556RGB-M & OpenRGB lighting effects."""

    THEME_BG = "#0f1115"
    HEADER_BG = "#161920"
    STATUS_BG = "#13161c"
    TEXT_MAIN = "#f8fafc"
    TEXT_MUTED = "#94a3b8"
    ACCENT = "#38bdf8"

    def __init__(self) -> None:
        super().__init__()
        self.title("🌸 OpenRGB & Redragon K556 - Centro de Iluminação RGB")
        self.geometry("900x620")
        self.minsize(860, 580)
        self.configure(bg=self.THEME_BG)

        # Thread-safe frame queue
        self._frame_queue: queue.Queue[RenderFrame] = queue.Queue(maxsize=4)

        # Layout provider (default to K556 physical matrix)
        self._layout_provider = K556MatrixLayoutProvider()

        # Build UI components
        self._build_header()
        self._build_canvas()
        self._build_controls()
        self._build_status_bar()

        # Initialize background runner
        self._runner = GuiRunner(
            on_frame=self._enqueue_frame,
            on_status=self._set_status_threadsafe,
            on_fps_update=self._set_fps_threadsafe,
        )

        # Start periodic GUI pump
        self._poll_frame_queue()

        # Window closing handler
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=self.HEADER_BG, padx=16, pady=10)
        header.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header,
            text="🌸 Flores Desabrochando & Mosaico Cromático",
            bg=self.HEADER_BG,
            fg=self.TEXT_MAIN,
            font=("Segoe UI", 13, "bold"),
        )
        title_lbl.pack(side=tk.LEFT)

        subtitle_lbl = tk.Label(
            header,
            text="Redragon K556RGB-M Direct HID | OpenRGB SDK",
            bg=self.HEADER_BG,
            fg=self.ACCENT,
            font=("Segoe UI", 9),
        )
        subtitle_lbl.pack(side=tk.RIGHT, pady=2)

    def _build_canvas(self) -> None:
        self._canvas_frame = KeyboardCanvas(
            self,
            layout_provider=self._layout_provider,
            width=860,
            height=210,
        )
        self._canvas_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

    def _build_controls(self) -> None:
        self._control_panel = ControlPanel(
            self,
            on_start=self._start_effect,
            on_stop=self._stop_effect,
        )
        self._control_panel.pack(fill=tk.X, side=tk.TOP, padx=6, pady=4)

    def _build_status_bar(self) -> None:
        status_bar = tk.Frame(self, bg=self.STATUS_BG, padx=14, pady=6)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self._status_label = tk.Label(
            status_bar,
            text="● Pronto para iniciar. Selecione o efeito e clique em Iniciar.",
            bg=self.STATUS_BG,
            fg=self.TEXT_MUTED,
            font=("Segoe UI", 8),
        )
        self._status_label.pack(side=tk.LEFT)

        self._fps_label = tk.Label(
            status_bar,
            text="-- FPS",
            bg=self.STATUS_BG,
            fg=self.ACCENT,
            font=("Segoe UI", 8, "bold"),
        )
        self._fps_label.pack(side=tk.RIGHT)

    def _enqueue_frame(self, frame: RenderFrame) -> None:
        """Called from background thread to enqueue new frame."""
        try:
            if self._frame_queue.full():
                try:
                    self._frame_queue.get_nowait()
                except queue.Empty:
                    pass
            self._frame_queue.put_nowait(frame)
        except Exception:
            pass

    def _poll_frame_queue(self) -> None:
        """Polls queue on main GUI thread and updates canvas."""
        try:
            while not self._frame_queue.empty():
                frame = self._frame_queue.get_nowait()
                self._canvas_frame.update_frame(frame)
        except Exception:
            pass
        finally:
            self.after(20, self._poll_frame_queue)

    def _set_status_threadsafe(self, text: str, is_active: bool) -> None:
        def _update():
            color = "#10b981" if is_active else self.TEXT_MUTED
            dot = "● " if is_active else "○ "
            self._status_label.config(text=dot + text, fg=color)
            if not is_active:
                self._control_panel.set_stopped()
                self._fps_label.config(text="-- FPS")
        self.after(0, _update)

    def _set_fps_threadsafe(self, fps: float) -> None:
        def _update():
            self._fps_label.config(text=f"{fps:.1f} FPS")
        self.after(0, _update)

    def _start_effect(self, settings: Dict[str, Any]) -> None:
        """Starts effect execution."""
        config = EffectConfig(
            effect_type=settings["effect_type"],
            palette_name=settings["palette"],
            speed=settings["speed"],
            brightness=settings["brightness"],
            fps=settings["fps"],
            max_flowers=settings["max_flowers"],
        )
        self._runner.start(
            config=config,
            effect_name=settings["effect_type"],
            driver=settings["driver"],
        )

    def _stop_effect(self) -> None:
        """Stops background execution."""
        self._runner.stop()

    def _on_close(self) -> None:
        """Graceful window close."""
        self._runner.stop()
        self.destroy()


def launch_gui() -> int:
    """Entry point to launch the graphical user interface."""
    app = MainWindow()
    app.mainloop()
    return 0
