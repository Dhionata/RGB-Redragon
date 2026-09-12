"""System tray icon integration for OpenRGB Flowers Blooming.

Observes SOLID and DRY principles:
- Single Responsibility: SystemTrayManager manages only tray icon lifecycle and OS events.
- Interface Segregation: ISystemTray defines a clean contract for tray operations.
- Dependency Inversion: Coordinates with MainWindow through injected callbacks.
"""
from __future__ import annotations

import logging
import math
import threading
from typing import Callable, Optional, Protocol, runtime_checkable

try:
    from PIL import Image, ImageDraw
    import pystray
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False

logger = logging.getLogger("openrgb_flowers.gui.tray")


@runtime_checkable
class ISystemTray(Protocol):
    """Interface contract for system tray managers."""

    def start(self) -> None:
        """Start and display the system tray icon."""
        ...

    def stop(self) -> None:
        """Stop and remove the system tray icon."""
        ...

    def is_running(self) -> bool:
        """Check if tray icon is currently active."""
        ...


class SystemTrayManager:
    """Manages the Windows notification area (system tray) icon and context menu."""

    def __init__(
        self,
        on_restore: Callable[[], None],
        on_quit: Callable[[], None],
        tooltip: str = "OpenRGB Flowers Blooming",
    ) -> None:
        self._on_restore = on_restore
        self._on_quit = on_quit
        self._tooltip = tooltip
        self._icon: Optional[pystray.Icon] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False

    @staticmethod
    def create_tray_image(size: int = 64) -> Image.Image:
        """Generates a vibrant multi-colored flower icon programmatically."""
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = size // 2, size // 2
        r_petal = size * 0.28
        dist = size * 0.22

        colors = [
            (244, 114, 182, 240),  # Pink
            (192, 132, 252, 240),  # Purple
            (56, 189, 248, 240),   # Cyan
            (251, 146, 60, 240),   # Orange
            (250, 204, 21, 240),   # Gold
        ]
        for i in range(5):
            angle = i * (2 * math.pi / 5) - math.pi / 2
            px = cx + dist * math.cos(angle)
            py = cy + dist * math.sin(angle)
            draw.ellipse(
                [px - r_petal, py - r_petal, px + r_petal, py + r_petal],
                fill=colors[i],
            )

        # Core
        r_core = size * 0.16
        draw.ellipse(
            [cx - r_core, cy - r_core, cx + r_core, cy + r_core],
            fill=(255, 255, 255, 255),
        )
        return img

    @classmethod
    def get_tray_image(cls, size: int = 64) -> Image.Image:
        """Loads the official project icon if available, with graceful procedural fallback."""
        from openrgb_flowers.gui.asset_locator import AssetLocator
        png_path = AssetLocator.get_icon_png_path()
        if png_path and png_path.is_file():
            try:
                img = Image.open(png_path)
                return img.resize((size, size), Image.Resampling.LANCZOS)
            except Exception as e:
                logger.debug(f"Failed to load icon from {png_path}: {e}")

        ico_path = AssetLocator.get_icon_ico_path()
        if ico_path and ico_path.is_file():
            try:
                img = Image.open(ico_path)
                return img.resize((size, size), Image.Resampling.LANCZOS)
            except Exception as e:
                logger.debug(f"Failed to load icon from {ico_path}: {e}")

        return cls.create_tray_image(size=size)

    def start(self) -> None:
        """Starts the tray icon in a dedicated daemon thread."""
        if not PYSTRAY_AVAILABLE:
            logger.warning("pystray not installed, system tray disabled.")
            return

        if self._running and self._icon is not None:
            return

        try:
            image = self.get_tray_image()
            menu = pystray.Menu(
                pystray.MenuItem("🌸 Abrir Painel", self._handle_restore, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("✕ Encerrar", self._handle_quit),
            )

            self._icon = pystray.Icon(
                name="openrgb_flowers_tray",
                icon=image,
                title=self._tooltip,
                menu=menu,
            )

            self._running = True
            self._thread = threading.Thread(target=self._run_icon, daemon=True)
            self._thread.start()
            logger.info("System tray icon started successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize system tray icon: {e}")
            self._running = False

    def _run_icon(self) -> None:
        """Thread worker executing pystray event loop."""
        try:
            if self._icon:
                self._icon.run()
        except Exception as e:
            logger.debug(f"Tray icon loop ended: {e}")
        finally:
            self._running = False

    def _handle_restore(self, icon: Optional[pystray.Icon] = None, item: Optional[pystray.MenuItem] = None) -> None:
        """Invoked when user clicks or double-clicks 'Abrir Painel'."""
        try:
            self._on_restore()
        except Exception as e:
            logger.error(f"Error restoring window from tray: {e}")

    def _handle_quit(self, icon: Optional[pystray.Icon] = None, item: Optional[pystray.MenuItem] = None) -> None:
        """Invoked when user selects 'Encerrar'."""
        try:
            self.stop()
            self._on_quit()
        except Exception as e:
            logger.error(f"Error shutting down from tray: {e}")

    def stop(self) -> None:
        """Stops and cleans up the tray icon."""
        if not self._running:
            return
        self._running = False
        try:
            if self._icon is not None:
                self._icon.stop()
                self._icon = None
        except Exception as e:
            logger.debug(f"Error stopping tray icon: {e}")

    def is_running(self) -> bool:
        """Returns True if tray icon is active."""
        return self._running
