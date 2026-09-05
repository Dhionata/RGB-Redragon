"""Mock transmitter for unit testing and offline terminal visualization."""
from __future__ import annotations
from typing import List, Optional
from openrgb_flowers.core.interfaces.i_frame_transmitter import IFrameTransmitter
from openrgb_flowers.core.models.render_frame import RenderFrame


class MockTransmitter(IFrameTransmitter):
    """In-memory mock transmitter for tests, headless CI, or offline visualizer runs."""

    def __init__(self) -> None:
        self._connected = False
        self._sent_frames: List[RenderFrame] = []
        self._last_frame: Optional[RenderFrame] = None

    @property
    def sent_frames(self) -> List[RenderFrame]:
        return self._sent_frames

    @property
    def last_frame(self) -> Optional[RenderFrame]:
        return self._last_frame

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def send_frame(self, frame: RenderFrame) -> bool:
        if not self._connected:
            return False
        self._last_frame = frame
        self._sent_frames.append(frame)
        # Limit buffer to prevent memory growth during long test runs
        if len(self._sent_frames) > 500:
            self._sent_frames.pop(0)
        return True
