"""Abstract interface for persisting and restoring effect and user preferences."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from openrgb_flowers.core.models.effect_config import EffectConfig


class IConfigStorageService(ABC):
    """Contract for persisting application configuration and user preferences."""

    @abstractmethod
    def load_config(self) -> EffectConfig:
        """Loads persistent configuration, falling back to default values if absent."""
        pass

    @abstractmethod
    def save_config(self, config: EffectConfig, extra_settings: Optional[Dict[str, Any]] = None) -> bool:
        """Saves current configuration and optional extra preferences to persistent storage."""
        pass

    @abstractmethod
    def get_storage_path(self) -> str:
        """Returns the canonical filesystem path where the configuration is stored."""
        pass
