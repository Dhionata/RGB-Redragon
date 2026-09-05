"""Control panel widget containing interactive sliders, selectors, and action buttons."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any

from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry
from openrgb_flowers.effects.effect_engine_factory import EffectEngineFactory


class ControlPanel(tk.Frame):
    """Modern dark-themed control panel for tuning RGB lighting parameters."""

    BG_COLOR = "#181b22"
    PANEL_BG = "#1e222b"
    TEXT_COLOR = "#e2e8f0"
    ACCENT_COLOR = "#38bdf8"
    START_COLOR = "#10b981"
    STOP_COLOR = "#ef4444"

    def __init__(
        self,
        parent: tk.Widget,
        on_start: Callable[[Dict[str, Any]], None],
        on_stop: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(parent, bg=self.BG_COLOR, **kwargs)
        self._on_start = on_start
        self._on_stop = on_stop

        # Style configuration
        self._setup_styles()
        self._build_widgets()

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground="#252a36",
            background="#2a303e",
            foreground="#ffffff",
            arrowcolor="#38bdf8",
        )
        style.configure("TLabel", background=self.BG_COLOR, foreground=self.TEXT_COLOR)

    def _build_widgets(self) -> None:
        grid_frame = tk.Frame(self, bg=self.BG_COLOR)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # Row 1: Effect, Palette, Driver
        col1 = tk.LabelFrame(
            grid_frame,
            text=" Configurações Principais ",
            bg=self.PANEL_BG,
            fg=self.ACCENT_COLOR,
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=8,
        )
        col1.grid(row=0, column=0, sticky="nsew", padx=6, pady=4)

        # Effect Dropdown
        tk.Label(col1, text="Efeito de Iluminação:", bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Segoe UI", 9)).grid(
            row=0, column=0, sticky="w", pady=2
        )
        self._effect_var = tk.StringVar(value="🌸 Flores Desabrochando (Blooming)")
        self._effect_cb = ttk.Combobox(
            col1,
            textvariable=self._effect_var,
            state="readonly",
            values=[
                "🌸 Flores Desabrochando (Blooming)",
                "✨ Mosaico Aleatório (Random Blend - 100% teclas)",
            ],
            width=38,
        )
        self._effect_cb.grid(row=1, column=0, sticky="w", pady=(0, 6))
        self._effect_cb.bind("<<ComboboxSelected>>", self._on_effect_changed)

        # Palette Dropdown
        tk.Label(col1, text="Paleta de Cores:", bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Segoe UI", 9)).grid(
            row=2, column=0, sticky="w", pady=2
        )
        available_palettes = PaletteRegistry.list_available()
        self._palette_var = tk.StringVar(value="rainbow" if "rainbow" in available_palettes else available_palettes[0])
        self._palette_cb = ttk.Combobox(
            col1,
            textvariable=self._palette_var,
            state="readonly",
            values=[p.capitalize() for p in available_palettes],
            width=38,
        )
        self._palette_cb.grid(row=3, column=0, sticky="w", pady=(0, 6))

        # Hardware Driver
        tk.Label(col1, text="Driver de Hardware:", bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Segoe UI", 9)).grid(
            row=4, column=0, sticky="w", pady=2
        )
        self._driver_var = tk.StringVar(value="Auto (Detecta Redragon K556 / OpenRGB)")
        self._driver_cb = ttk.Combobox(
            col1,
            textvariable=self._driver_var,
            state="readonly",
            values=[
                "Auto (Detecta Redragon K556 / OpenRGB)",
                "Redragon K556 (Nativo USB HID)",
                "OpenRGB SDK Server",
                "Simulação (Mock)",
            ],
            width=38,
        )
        self._driver_cb.grid(row=5, column=0, sticky="w", pady=(0, 6))

        # Row 1 Col 2: Sliders
        col2 = tk.LabelFrame(
            grid_frame,
            text=" Ajustes Dinâmicos ",
            bg=self.PANEL_BG,
            fg=self.ACCENT_COLOR,
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=8,
        )
        col2.grid(row=0, column=1, sticky="nsew", padx=6, pady=4)

        # Speed Slider
        self._speed_label = tk.Label(col2, text="Velocidade: 1.2x", bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Segoe UI", 9))
        self._speed_label.grid(row=0, column=0, sticky="w")
        self._speed_scale = tk.Scale(
            col2,
            from_=0.2,
            to=4.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            showvalue=0,
            bg="#252a36",
            fg=self.TEXT_COLOR,
            troughcolor="#161920",
            highlightthickness=0,
            command=self._update_speed_label,
            length=220,
        )
        self._speed_scale.set(1.2)
        self._speed_scale.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        # Brightness Slider
        self._brightness_label = tk.Label(col2, text="Brilho: 100%", bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Segoe UI", 9))
        self._brightness_label.grid(row=2, column=0, sticky="w")
        self._brightness_scale = tk.Scale(
            col2,
            from_=10,
            to=100,
            resolution=5,
            orient=tk.HORIZONTAL,
            showvalue=0,
            bg="#252a36",
            fg=self.TEXT_COLOR,
            troughcolor="#161920",
            highlightthickness=0,
            command=self._update_brightness_label,
            length=220,
        )
        self._brightness_scale.set(100)
        self._brightness_scale.grid(row=3, column=0, sticky="ew", pady=(0, 4))

        # FPS Slider
        self._fps_label = tk.Label(col2, text="FPS Alvo: 30 FPS", bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Segoe UI", 9))
        self._fps_label.grid(row=4, column=0, sticky="w")
        self._fps_scale = tk.Scale(
            col2,
            from_=15,
            to=60,
            resolution=5,
            orient=tk.HORIZONTAL,
            showvalue=0,
            bg="#252a36",
            fg=self.TEXT_COLOR,
            troughcolor="#161920",
            highlightthickness=0,
            command=self._update_fps_label,
            length=220,
        )
        self._fps_scale.set(30)
        self._fps_scale.grid(row=5, column=0, sticky="ew", pady=(0, 4))

        # Row 1 Col 3: Action Buttons & Advanced Options
        col3 = tk.LabelFrame(
            grid_frame,
            text=" Controle e Ações ",
            bg=self.PANEL_BG,
            fg=self.ACCENT_COLOR,
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=8,
        )
        col3.grid(row=0, column=2, sticky="nsew", padx=6, pady=4)

        # Max Flowers Slider (visible when Blooming)
        self._flowers_label = tk.Label(col3, text="Máx Flores: 7", bg=self.PANEL_BG, fg=self.TEXT_COLOR, font=("Segoe UI", 9))
        self._flowers_label.grid(row=0, column=0, sticky="w")
        self._flowers_scale = tk.Scale(
            col3,
            from_=2,
            to=16,
            resolution=1,
            orient=tk.HORIZONTAL,
            showvalue=0,
            bg="#252a36",
            fg=self.TEXT_COLOR,
            troughcolor="#161920",
            highlightthickness=0,
            command=self._update_flowers_label,
            length=180,
        )
        self._flowers_scale.set(7)
        self._flowers_scale.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        # Start Button
        self._btn_start = tk.Button(
            col3,
            text="▶ INICIAR EFEITO",
            bg=self.START_COLOR,
            fg="#ffffff",
            activebackground="#059669",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=6,
            command=self._trigger_start,
        )
        self._btn_start.grid(row=2, column=0, sticky="ew", pady=4)

        # Stop Button
        self._btn_stop = tk.Button(
            col3,
            text="⏹ PARAR",
            bg="#374151",
            fg="#9ca3af",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            state=tk.DISABLED,
            cursor="hand2",
            padx=12,
            pady=6,
            command=self._trigger_stop,
        )
        self._btn_stop.grid(row=3, column=0, sticky="ew", pady=4)

    def _on_effect_changed(self, event=None) -> None:
        is_blooming = "blooming" in self._effect_var.get().lower()
        if is_blooming:
            self._flowers_label.grid()
            self._flowers_scale.grid()
        else:
            self._flowers_label.grid_remove()
            self._flowers_scale.grid_remove()

    def _update_speed_label(self, val: str) -> None:
        self._speed_label.config(text=f"Velocidade: {float(val):.1f}x")

    def _update_brightness_label(self, val: str) -> None:
        self._brightness_label.config(text=f"Brilho: {int(float(val))}%")

    def _update_fps_label(self, val: str) -> None:
        self._fps_label.config(text=f"FPS Alvo: {int(float(val))} FPS")

    def _update_flowers_label(self, val: str) -> None:
        self._flowers_label.config(text=f"Máx Flores: {int(float(val))}")

    def _trigger_start(self) -> None:
        raw_driver = self._driver_var.get().lower()
        if "redragon" in raw_driver:
            driver = "redragon"
        elif "openrgb" in raw_driver:
            driver = "openrgb"
        elif "mock" in raw_driver:
            driver = "mock"
        else:
            driver = "auto"

        raw_effect = self._effect_var.get().lower()
        effect_type = "random_blend" if "random" in raw_effect or "mosaico" in raw_effect else "blooming"

        settings = {
            "effect_type": effect_type,
            "palette": self._palette_var.get().lower(),
            "driver": driver,
            "speed": float(self._speed_scale.get()),
            "brightness": float(self._brightness_scale.get()) / 100.0,
            "fps": float(self._fps_scale.get()),
            "max_flowers": int(self._flowers_scale.get()),
        }

        self._btn_start.config(state=tk.DISABLED, bg="#374151", fg="#9ca3af")
        self._btn_stop.config(state=tk.NORMAL, bg=self.STOP_COLOR, fg="#ffffff")
        self._on_start(settings)

    def _trigger_stop(self) -> None:
        self._btn_start.config(state=tk.NORMAL, bg=self.START_COLOR, fg="#ffffff")
        self._btn_stop.config(state=tk.DISABLED, bg="#374151", fg="#9ca3af")
        self._on_stop()

    def set_stopped(self) -> None:
        """Resets UI buttons to stopped state."""
        self._btn_start.config(state=tk.NORMAL, bg=self.START_COLOR, fg="#ffffff")
        self._btn_stop.config(state=tk.DISABLED, bg="#374151", fg="#9ca3af")
