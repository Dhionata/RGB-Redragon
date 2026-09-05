"""OpenRGB frame transmitter communicating via the OpenRGB SDK."""
from __future__ import annotations
import logging
import time
from typing import Any, Optional
from openrgb_flowers.core.interfaces.i_frame_transmitter import IFrameTransmitter
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.core.exceptions import OpenRGBConnectionError, DeviceNotFoundError

logger = logging.getLogger("openrgb_flowers.transmitter")


class OpenRGBTransmitter(IFrameTransmitter):
    """High-speed frame transmitter interfacing with OpenRGB SDK via openrgb-python."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6742,
        device_name: Optional[str] = None,
        device_index: Optional[int] = None,
        client_name: str = "Flowers Blooming",
    ) -> None:
        self._host = host
        self._port = int(port)
        self._target_name = device_name
        self._target_index = device_index
        self._client_name = client_name

        self._client: Any = None
        self._device: Any = None
        self._connected = False
        self._rgb_color_cls: Any = None
        self._color_buffer: list[Any] = []

    @property
    def device(self) -> Any:
        return self._device

    def is_connected(self) -> bool:
        return self._connected and self._client is not None and self._device is not None

    def connect(self) -> bool:
        """Connects to OpenRGB SDK server, detects keyboard, and configures Direct mode."""
        try:
            from openrgb import OpenRGBClient
            from openrgb.utils import DeviceType, RGBColor
            self._rgb_color_cls = RGBColor
        except ImportError as e:
            raise OpenRGBConnectionError("openrgb-python is not installed. Install with 'pip install openrgb-python'") from e

        try:
            logger.info(f"Connecting to OpenRGB server at {self._host}:{self._port}...")
            self._client = OpenRGBClient(address=self._host, port=self._port, name=self._client_name)
            self._device = self._find_target_device()
            self._configure_device_mode(self._device)

            # Pre-allocate contiguous color buffer for zero-allocation high FPS transmission
            dev_led_count = len(getattr(self._device, "leds", []))
            self._color_buffer = [self._rgb_color_cls(0, 0, 0) for _ in range(dev_led_count)]

            self._connected = True
            logger.info(f"Successfully connected to OpenRGB device: {self._device.name} ({dev_led_count} LEDs)")
            return True
        except Exception as e:
            self._connected = False
            self._client = None
            self._device = None
            self._color_buffer = []
            logger.warning(f"Failed to connect to OpenRGB: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnects cleanly from the OpenRGB SDK server."""
        if self._client:
            try:
                self._client.disconnect()
            except Exception:
                pass
        self._client = None
        self._device = None
        self._color_buffer = []
        self._connected = False

    def _find_target_device(self) -> Any:
        """Finds target keyboard device (K556, Redragon, or first available keyboard)."""
        devices = getattr(self._client, "devices", [])
        if not devices:
            raise DeviceNotFoundError("No devices found connected to OpenRGB.")

        # Explicit device index
        if self._target_index is not None and 0 <= self._target_index < len(devices):
            return devices[self._target_index]

        # Explicit device name match
        if self._target_name:
            target_lower = self._target_name.lower()
            for dev in devices:
                if target_lower in getattr(dev, "name", "").lower():
                    return dev

        # Auto-detect: Look for Redragon or K556
        for dev in devices:
            name_lower = getattr(dev, "name", "").lower()
            if "k556" in name_lower or "redragon" in name_lower:
                return dev

        # Fallback: Look for any Keyboard device type
        try:
            from openrgb.utils import DeviceType
            for dev in devices:
                dev_type = getattr(dev, "type", None)
                if dev_type == DeviceType.KEYBOARD or getattr(dev_type, "value", None) == DeviceType.KEYBOARD.value:
                    return dev
        except Exception:
            pass

        # Final fallback: return first device
        return devices[0]

    def _configure_device_mode(self, device: Any) -> None:
        """Sets device mode to Direct / Custom / Per-LED to prevent flash memory writes and enable high FPS."""
        try:
            from openrgb.utils import ModeColors
            modes = getattr(device, "modes", [])

            # 1. Prefer mode explicitly named 'direct'
            for idx, mode in enumerate(modes):
                if getattr(mode, "name", "").lower() == "direct":
                    device.set_mode(idx)
                    logger.info(f"Device '{device.name}' set to Direct mode (index {idx}).")
                    return

            # 2. Check for modes commonly enabling per-key lighting on Redragon / EVision
            for idx, mode in enumerate(modes):
                mname = getattr(mode, "name", "").lower()
                if any(target in mname for target in ("custom", "per led", "per-led", "per-key", "per key")):
                    device.set_mode(idx)
                    logger.info(f"Device '{device.name}' set to '{mode.name}' mode (index {idx}).")
                    return

            # 3. Check for any mode marked with ModeColors.PER_LED
            for idx, mode in enumerate(modes):
                if getattr(mode, "color_mode", None) == ModeColors.PER_LED:
                    device.set_mode(idx)
                    logger.info(f"Device '{device.name}' set to PER_LED mode '{mode.name}' (index {idx}).")
                    return

            # 4. Fallback: try set_custom_mode if supported
            if hasattr(device, "set_custom_mode"):
                device.set_custom_mode()
                logger.info(f"Device '{device.name}' configured via set_custom_mode().")
                return

            logger.info(f"Device '{getattr(device, 'name', '')}' active mode remains: {getattr(device, 'active_mode', None)}")
        except Exception as e:
            logger.warning(f"Could not configure device mode: {e}")

    def send_frame(self, frame: RenderFrame) -> bool:
        """Sends frame to OpenRGB device using fast=True for high framerate."""
        if not self.is_connected():
            return False

        try:
            dev_led_count = len(self._device.leds)
            frame_colors = frame.colors

            # Ensure buffer matches LED count if device LEDs changed
            if len(self._color_buffer) != dev_led_count:
                self._color_buffer = [self._rgb_color_cls(0, 0, 0) for _ in range(dev_led_count)]

            # High-performance in-place mutation of pre-allocated RGBColor buffer
            # Zero memory allocation per frame
            n_colors = min(frame_colors.shape[0], dev_led_count)
            buffer = self._color_buffer
            for i in range(n_colors):
                c = buffer[i]
                c.red = int(frame_colors[i, 0])
                c.green = int(frame_colors[i, 1])
                c.blue = int(frame_colors[i, 2])

            # Pad remaining LEDs with black if frame has fewer colors
            for i in range(n_colors, dev_led_count):
                c = buffer[i]
                c.red = 0
                c.green = 0
                c.blue = 0

            # fast=True avoids synchronous round-trip controller update packet, achieving 60+ FPS
            self._device.set_colors(buffer, fast=True)
            return True
        except Exception as e:
            logger.warning(f"Error transmitting frame to OpenRGB: {e}. Marking disconnected...")
            self._connected = False
            return False
