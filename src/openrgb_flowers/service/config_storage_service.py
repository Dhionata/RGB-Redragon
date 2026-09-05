"""Persistent configuration storage service."""
from __future__ import annotations
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from openrgb_flowers.core.interfaces.config_storage_service import IConfigStorageService
from openrgb_flowers.core.models.effect_config import EffectConfig

logger = logging.getLogger("openrgb_flowers.service.config_storage")


class ConfigStorageService(IConfigStorageService):
    """Manages reading and writing application configuration to JSON storage."""

    APP_DIR_NAME = ".openrgb_flowers"
    CONFIG_FILE_NAME = "user_config.json"

    def __init__(self, custom_path: Optional[Path] = None) -> None:
        if custom_path:
            self._storage_path = Path(custom_path).resolve()
        else:
            home = Path.home()
            self._storage_dir = home / self.APP_DIR_NAME
            self._storage_path = self._storage_dir / self.CONFIG_FILE_NAME

    def get_storage_path(self) -> str:
        return str(self._storage_path)

    def load_config(self) -> EffectConfig:
        """Loads persistent configuration, falling back to local config.json or defaults."""
        # 1. Try user storage path
        if self._storage_path.exists():
            try:
                with open(self._storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"Loaded persistent config from {self._storage_path}")
                return self._dict_to_config(data)
            except Exception as e:
                logger.warning(f"Failed to read user config at {self._storage_path}: {e}")

        # 2. Try local repository config.json
        local_cfg = Path("config.json")
        if local_cfg.exists():
            try:
                return EffectConfig.load_json(str(local_cfg))
            except Exception as e:
                logger.warning(f"Failed to load local config.json: {e}")

        # 3. Default fallback
        return EffectConfig(
            effect_type="random_blend",
            palette_name="rainbow",
            speed=1.2,
            brightness=1.0,
            saturation=1.0,
            fps=30.0,
        )

    def save_config(self, config: EffectConfig, extra_settings: Optional[Dict[str, Any]] = None) -> bool:
        """Saves current configuration and metadata to user config file."""
        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            data: Dict[str, Any] = {
                "effect_type": config.effect_type,
                "palette_name": config.palette_name,
                "speed": config.speed,
                "brightness": config.brightness,
                "saturation": config.saturation,
                "fps": config.fps,
                "max_flowers": config.max_flowers,
                "spawn_rate": config.spawn_rate,
                "blend_mode": config.blend_mode,
                "host": config.host,
                "port": config.port,
                "device_name": config.device_name,
            }
            if extra_settings:
                data.update(extra_settings)

            with open(self._storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Configuration successfully saved to {self._storage_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write configuration to {self._storage_path}: {e}")
            return False

    def _dict_to_config(self, data: Dict[str, Any]) -> EffectConfig:
        return EffectConfig(
            effect_type=data.get("effect_type", "random_blend"),
            palette_name=data.get("palette_name", data.get("palette", "rainbow")),
            speed=float(data.get("speed", 1.2)),
            brightness=float(data.get("brightness", 1.0)),
            saturation=float(data.get("saturation", 1.0)),
            fps=float(data.get("fps", 30.0)),
            max_flowers=int(data.get("max_flowers", 7)),
            spawn_rate=float(data.get("spawn_rate", 1.4)),
            blend_mode=str(data.get("blend_mode", "weighted")),
            host=str(data.get("host", "127.0.0.1")),
            port=int(data.get("port", 6742)),
            device_name=data.get("device_name"),
        )
