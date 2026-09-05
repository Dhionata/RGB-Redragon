"""High-performance direct USB HID transmitter for Redragon K556RGB-M."""
from __future__ import annotations
import logging
from typing import Any, List, Optional
import numpy as np

from openrgb_flowers.core.interfaces.i_frame_transmitter import IFrameTransmitter
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.core.exceptions.hardware_connection_error import HardwareConnectionError

logger = logging.getLogger("openrgb_flowers.transmitter.redragon")


class RedragonK556Transmitter(IFrameTransmitter):
    """Direct USB HID frame transmitter for Redragon K556RGB-M mechanical keyboard.

    Communicates directly with the keyboard's proprietary USB HID Interface (VID: 0x2E3C, PID: 0xC365,
    Interface: 2) using pre-allocated zero-copy packets at up to 500+ FPS, eliminating dependency
    on third-party software while preserving complete backward compatibility with the project architecture.
    """

    VID = 0x2E3C
    PID = 0xC365
    TARGET_INTERFACE = 2

    CHUNK_SIZE = 18
    TOTAL_KEYS = 132
    NUM_CHUNKS = 8

    # Command codes discovered from Redragon WebHID protocol reverse-engineering
    CMD_KEYBOARD_LIGHT = 0x07
    CMD_CUSTOM_CHUNK = 0x09
    MODE_CUSTOM = 10

    def __init__(self, target_path: Optional[bytes] = None) -> None:
        self._target_path = target_path
        self._device: Any = None
        self._connected = False

        # Pre-allocate 8 contiguous 65-byte packets for zero-allocation per frame transmission
        # Header layout (bytes 0-5) matching Redragon K556 WebHID firmware protocol:
        # byte 0: 0x01 (Report ID)
        # byte 1: 0x09 (Command: Custom Light Chunk)
        # byte 2: 0x00 (Custom Lighting Profile Index 0)
        # byte 3: (chunk_index >> 8) & 0xFF
        # byte 4: chunk_index & 0xFF (0..7)
        # byte 5: Byte count (54 bytes for chunks 0-6, 18 bytes for chunk 7)
        # bytes 6..60: Contiguous RGB triplets (18 keys x 3 bytes)
        self._packets: List[bytearray] = []
        for c in range(self.NUM_CHUNKS):
            n_keys = self.CHUNK_SIZE if c < 7 else 6
            n_bytes = n_keys * 3
            pkt = bytearray(65)
            pkt[0] = 0x01
            pkt[1] = self.CMD_CUSTOM_CHUNK
            pkt[2] = 0x00
            pkt[3] = (c >> 8) & 0xFF
            pkt[4] = c & 0xFF
            pkt[5] = n_bytes
            self._packets.append(pkt)

    def is_connected(self) -> bool:
        return self._connected and self._device is not None

    def connect(self) -> bool:
        """Locates and opens the Redragon K556RGB-M HID Interface 2."""
        try:
            import hid
        except ImportError as e:
            raise HardwareConnectionError("hidapi is not installed. Install with 'pip install hidapi'") from e

        try:
            logger.info(f"Scanning for Redragon K556RGB-M (VID: 0x{self.VID:04X}, PID: 0x{self.PID:04X})...")
            devs = hid.enumerate(self.VID, self.PID)
            targets = [d for d in devs if d.get("interface_number") == self.TARGET_INTERFACE]

            if not targets:
                logger.warning(
                    f"Redragon K556RGB-M Interface {self.TARGET_INTERFACE} not found. "
                    "Ensure keyboard is connected via USB."
                )
                self._connected = False
                return False

            chosen = targets[0]
            path = self._target_path or chosen["path"]
            logger.info(f"Connecting to Redragon K556RGB-M at {path}...")

            h = hid.device()
            h.open_path(path)
            h.set_nonblocking(1)

            # Drain any pending residual responses
            while h.read(64):
                pass

            # Switch keyboard microcontroller to Mode 10 (Custom LED Mode)
            # Discovered via Redragon WebHID agreement protocol (Command 0x07)
            mode_pkt = bytearray(65)
            mode_pkt[0] = 0x01  # Report ID
            mode_pkt[1] = self.CMD_KEYBOARD_LIGHT  # 0x07
            mode_pkt[5] = 0x0E  # Payload length (14 bytes)
            mode_pkt[6] = self.MODE_CUSTOM  # Mode 10: Custom LED
            mode_pkt[7] = 5     # Brightness: 5 (Maximum)
            mode_pkt[8] = 3     # Speed: 3
            mode_pkt[9] = 255   # Foreground Red
            mode_pkt[16] = 1    # FullColor: 1 (RGB)
            mode_pkt[17] = 0    # Power: 0 (Light ON)
            h.write(mode_pkt)

            # Send Custom Lighting activation packet (0x09 0x20)
            init_pkt = bytearray(65)
            init_pkt[0] = 0x01
            init_pkt[1] = self.CMD_CUSTOM_CHUNK  # 0x09
            init_pkt[2] = 0x20
            h.write(init_pkt)

            self._device = h
            self._connected = True
            logger.info("Successfully connected to Redragon K556RGB-M direct USB HID interface.")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Redragon K556RGB-M: {e}")
            self._connected = False
            self._device = None
            return False

    def disconnect(self) -> None:
        """Closes HID device connection gracefully."""
        if self._device is not None:
            try:
                self._device.close()
            except Exception:
                pass
        self._device = None
        self._connected = False
        logger.info("Disconnected from Redragon K556RGB-M.")

    def send_frame(self, frame: RenderFrame) -> bool:
        """Transmits rendered RGB frame directly to the keyboard matrix."""
        if not self.is_connected():
            return False

        try:
            # Flatten colors directly into 1D contiguous uint8 array via memoryview (zero copy)
            flat_colors = frame.colors.ravel()
            color_mv = memoryview(flat_colors)
            total_bytes = len(color_mv)

            # Drain any pending read buffers non-blockingly
            try:
                while self._device.read(64):
                    pass
            except Exception:
                pass

            # Update and transmit each chunk
            for c in range(self.NUM_CHUNKS):
                pkt = self._packets[c]
                start_byte = c * self.CHUNK_SIZE * 3
                n_keys = self.CHUNK_SIZE if c < 7 else 6
                n_bytes = n_keys * 3

                # Copy RGB data directly into pre-allocated packet
                if start_byte + n_bytes <= total_bytes:
                    pkt[6 : 6 + n_bytes] = color_mv[start_byte : start_byte + n_bytes]
                else:
                    available = max(0, total_bytes - start_byte)
                    if available > 0:
                        pkt[6 : 6 + available] = color_mv[start_byte : start_byte + available]
                    # Fill remaining with zero
                    for b in range(6 + available, 6 + n_bytes):
                        pkt[b] = 0

                res = self._device.write(pkt)
                if res < 0:
                    logger.warning(f"Error writing chunk {c} to Redragon K556RGB-M.")
                    return False

            return True

        except Exception as e:
            logger.warning(f"Failed to transmit frame to Redragon K556RGB-M: {e}")
            self._connected = False
            return False
