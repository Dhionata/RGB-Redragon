"""Abstract interface for operating system autostart / background service registration."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class IAutoStartService(ABC):
    """Contract for configuring application autostart on system boot."""

    @abstractmethod
    def is_enabled(self) -> bool:
        """Checks if autostart is currently configured for the application."""
        pass

    @abstractmethod
    def enable(self, extra_args: Optional[str] = "--autostart") -> bool:
        """Registers the application to launch automatically on system login."""
        pass

    @abstractmethod
    def disable(self) -> bool:
        """Unregisters the application from system autostart."""
        pass
