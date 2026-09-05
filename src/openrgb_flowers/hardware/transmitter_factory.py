"""Factory for instantiating hardware and simulated frame transmitters."""
from __future__ import annotations
import logging
from typing import Optional

from openrgb_flowers.core.interfaces.i_frame_transmitter import IFrameTransmitter
from openrgb_flowers.hardware.mock_transmitter import MockTransmitter
from openrgb_flowers.hardware.openrgb_transmitter import OpenRGBTransmitter
from openrgb_flowers.hardware.redragon_k556_transmitter import RedragonK556Transmitter

logger = logging.getLogger("openrgb_flowers.transmitter.factory")


class TransmitterFactory:
    """Factory responsible for resolving and instantiating frame transmitters."""

    @classmethod
    def is_redragon_k556_connected(cls) -> bool:
        """Probes USB devices to check if Redragon K556RGB-M Interface 2 is physically connected."""
        try:
            import hid
            devs = hid.enumerate(RedragonK556Transmitter.VID, RedragonK556Transmitter.PID)
            return any(d.get("interface_number") == RedragonK556Transmitter.TARGET_INTERFACE for d in devs)
        except Exception:
            return False

    @classmethod
    def create_transmitter(
        cls,
        driver: str = "auto",
        host: str = "127.0.0.1",
        port: int = 6742,
        device_name: Optional[str] = None,
        device_index: Optional[int] = None,
    ) -> IFrameTransmitter:
        """Instantiates appropriate transmitter based on driver type.

        Args:
            driver: 'auto', 'redragon', 'openrgb', or 'mock'.
            host: OpenRGB server host (if using OpenRGB).
            port: OpenRGB server port (if using OpenRGB).
            device_name: Optional device name filter.
            device_index: Optional device index filter.

        Returns:
            Instance conforming to IFrameTransmitter.
        """
        driver_lower = driver.lower().strip()

        if driver_lower == "mock":
            logger.info("Instantiating MockTransmitter (simulation mode).")
            return MockTransmitter()

        if driver_lower == "redragon":
            logger.info("Instantiating RedragonK556Transmitter (direct USB HID mode).")
            return RedragonK556Transmitter()

        if driver_lower == "openrgb":
            logger.info(f"Instantiating OpenRGBTransmitter ({host}:{port}).")
            return OpenRGBTransmitter(
                host=host,
                port=port,
                device_name=device_name,
                device_index=device_index,
            )

        # 'auto' driver resolution: check for physical Redragon K556RGB-M first
        if cls.is_redragon_k556_connected():
            logger.info("Auto-detected Redragon K556RGB-M USB device! Using native Redragon HID transmitter.")
            return RedragonK556Transmitter()

        logger.info("Redragon K556RGB-M not directly detected. Defaulting to OpenRGB transmitter.")
        return OpenRGBTransmitter(
            host=host,
            port=port,
            device_name=device_name,
            device_index=device_index,
        )
