"""Configuration model for the Flowers Blooming effect."""
from __future__ import annotations
from dataclasses import dataclass, field
import json
from typing import Any, Dict, List, Optional
from openrgb_flowers.core.models.color_rgb import ColorRGB
from openrgb_flowers.core.exceptions import ConfigurationError


@dataclass
class EffectConfig:
    """Strongly-typed configuration for the Flowers Blooming effect."""

    effect_type: str = "blooming"
    fps: float = 30.0
    speed: float = 1.0
    max_flowers: int = 7
    spawn_rate: float = 1.4
    petal_options: List[int] = field(default_factory=lambda: [4, 5, 6, 8])
    palette_name: str = "sakura"
    blend_mode: str = "weighted"
    background_color: ColorRGB = field(default_factory=lambda: ColorRGB(4, 8, 12))
    ambient_pulse: bool = True
    brightness: float = 1.0
    gamma: float = 2.2
    host: str = "127.0.0.1"
    port: int = 6742
    device_name: Optional[str] = None
    device_index: Optional[int] = None

    def validate(self) -> None:
        """Validates configuration parameters."""
        if not (1.0 <= self.fps <= 120.0):
            raise ConfigurationError(f"fps must be between 1.0 and 120.0, got {self.fps}")
        if not (0.1 <= self.speed <= 10.0):
            raise ConfigurationError(f"speed must be between 0.1 and 10.0, got {self.speed}")
        if not (1 <= self.max_flowers <= 50):
            raise ConfigurationError(f"max_flowers must be between 1 and 50, got {self.max_flowers}")
        if not (0.1 <= self.spawn_rate <= 20.0):
            raise ConfigurationError(f"spawn_rate must be between 0.1 and 20.0, got {self.spawn_rate}")
        if not (0.0 <= self.brightness <= 1.0):
            raise ConfigurationError(f"brightness must be between 0.0 and 1.0, got {self.brightness}")
        if not (0.5 <= self.gamma <= 3.5):
            raise ConfigurationError(f"gamma must be between 0.5 and 3.5, got {self.gamma}")
        if not self.petal_options or any(p < 3 for p in self.petal_options):
            raise ConfigurationError("petal_options must contain integers >= 3")

    def to_dict(self) -> Dict[str, Any]:
        """Serializes config to dictionary."""
        return {
            "effect_type": self.effect_type,
            "fps": self.fps,
            "speed": self.speed,
            "max_flowers": self.max_flowers,
            "spawn_rate": self.spawn_rate,
            "petal_options": self.petal_options,
            "palette_name": self.palette_name,
            "blend_mode": self.blend_mode,
            "background_color": self.background_color.to_hex(),
            "ambient_pulse": self.ambient_pulse,
            "brightness": self.brightness,
            "gamma": self.gamma,
            "host": self.host,
            "port": self.port,
            "device_name": self.device_name,
            "device_index": self.device_index,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EffectConfig:
        """Loads config from dictionary."""
        bg_val = data.get("background_color", "#04080C")
        bg_rgb = ColorRGB.from_hex(bg_val) if isinstance(bg_val, str) else ColorRGB(*bg_val)
        cfg = cls(
            effect_type=str(data.get("effect_type", "blooming")),
            fps=float(data.get("fps", 30.0)),
            speed=float(data.get("speed", 1.0)),
            max_flowers=int(data.get("max_flowers", 7)),
            spawn_rate=float(data.get("spawn_rate", 1.4)),
            petal_options=list(data.get("petal_options", [4, 5, 6, 8])),
            palette_name=str(data.get("palette_name", "sakura")),
            blend_mode=str(data.get("blend_mode", "weighted")),
            background_color=bg_rgb,
            ambient_pulse=bool(data.get("ambient_pulse", True)),
            brightness=float(data.get("brightness", 1.0)),
            gamma=float(data.get("gamma", 2.2)),
            host=str(data.get("host", "127.0.0.1")),
            port=int(data.get("port", 6742)),
            device_name=data.get("device_name"),
            device_index=data.get("device_index"),
        )
        cfg.validate()
        return cfg

    @classmethod
    def load_json(cls, file_path: str) -> EffectConfig:
        """Loads configuration from JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))
