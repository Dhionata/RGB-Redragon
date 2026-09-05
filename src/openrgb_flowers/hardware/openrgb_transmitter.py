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

    @property
    def device(self) -> Any:
        return self._device

    def is_connected(self) -> bool:
        return self._connected and self._client is not None

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
            self._client = OpenRGBClient(name=self._client_name, host=self._host, port=self._port)
            self._device = self._find_target_device()
            self._configure_device_mode(self._device)
            self._connected = True
            logger.info(f"Successfully connected to OpenRGB device: {self._device.name} ({len(self._device.leds)} LEDs)")
            return True
        except Exception as e:
            self._connected = False
            self._client = None
            self._device = None
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
        self._connected = False

    def _find_target_device(self) -> Any:
        """Finds target keyboard device (K556, Redragon, or first available keyboard)."""
        devices = self._client.devices
        if not devices:
            raise DeviceNotFoundError("No devices found connected to OpenRGB.")

        # Explicit device index
        if self._target_index is not None and 0 <= self._target_index < len(devices):
            return devices[self._target_index]

        # Explicit device name match
        if self._target_name:
            target_lower = self._target_name.lower()
            for dev in devices:
                if target_lower in dev.name.lower():
                    return dev

        # Auto-detect: Look for Redragon or K556
        for dev in devices:
            name_lower = dev.name.lower()
            if "k556" in name_lower or "redragon" in name_lower:
                return dev

        # Fallback: Look for any Keyboard device type
        try:
            from openrgb.utils import DeviceType
            keyboards = [d for d in devices if getattr(d, "type", None) == DeviceType.KEYBOARD]
            if keyboards:
                return keyboards[0]
        except Exception:
            pass

        # Final fallback: return first device
        return devices[0]

    def _configure_device_mode(self, device: Any) -> None:
        """Sets device mode to Direct to prevent flash memory writes and enable high FPS."""
        try:
            for idx, mode in enumerate(device.modes):
                if mode.name.lower() == "direct":
                    device.set_mode(idx)
                    logger.info(f"Device '{device.name}' set to Direct mode.")
                    return
            logger.info(f"Device '{device.name}' does not have a mode named 'Direct'. Active mode remains: {device.active_mode}")
        except Exception as e:
            logger.warning(f"Could not switch mode to Direct: {e}")

    def send_frame(self, frame: RenderFrame) -> bool:
        """Sends frame to OpenRGB device using fast=True for high framerate."""
        if not self.is_connected():
            return False

        try:
            dev_led_count = len(self._device.leds)
            frame_colors = frame.colors

            # Convert numpy uint8 array to list of RGBColor objects
            # Pre-allocating RGBColor instances efficiently
            n_colors = min(frame_colors.shape[0], dev_led_count)
            rgb_cls = self._rgb_color_cls

            color_list = [
                rgb_cls(int(frame_colors[i, 0]), int(frame_colors[i, 1]), int(frame_colors[i, 2]))
                for i in range(n_colors)
            ]

            # Pad with black if frame has fewer LEDs than device
            if len(color_list) < dev_led_count:
                black = rgb_cls(0, 0, 0)
                color_list.extend([black] * (dev_led_count - len(color_list)))

            # fast=True avoids synchronous round-trip controller update packet, achieving 60+ FPS
            self._device.set_colors(color_list, fast=True)
            return True
        except Exception as e:
            logger.warning(f"Error transmitting frame to OpenRGB: {e}. Attempting reconnect...")
            self._connected = False
            return False
