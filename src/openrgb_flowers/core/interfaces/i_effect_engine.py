"""Interface for effect generation engine."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.core.models.effect_config import EffectConfig


class IEffectEngine(ABC):
    """Contract for the floral blooming effect calculation engine."""

    @abstractmethod
    def tick(self, dt: float) -> RenderFrame:
        """Advances simulation by dt seconds and renders the next frame."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Resets engine state, clearing active flowers."""
        pass

    @abstractmethod
    def get_config(self) -> EffectConfig:
        """Returns current effect configuration."""
        pass

    @abstractmethod
    def get_active_flower_count(self) -> int:
        """Returns number of currently blooming flowers."""
        pass

    @abstractmethod
    def update_layout(self, layout_provider: Any) -> None:
        """Updates the physical layout provider and recomputes coordinate buffers."""
        pass

    @abstractmethod
    def update_config(self, config: EffectConfig) -> None:
        """Updates active runtime parameters (speed, brightness, saturation, palette, etc.) on the fly."""
        pass
