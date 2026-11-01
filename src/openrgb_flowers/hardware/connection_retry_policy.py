"""Resilient connection retry policy for hardware transmitters."""
from __future__ import annotations
import logging
import time
from typing import Callable, Optional

from openrgb_flowers.core.interfaces.i_frame_transmitter import IFrameTransmitter

logger = logging.getLogger("openrgb_flowers.hardware.retry")


class ConnectionRetryPolicy:
    """Manages connection attempts with backoff and cancellation awareness."""

    def __init__(
        self,
        max_attempts: int = 12,
        interval_seconds: float = 1.5,
        on_attempt: Optional[Callable[[int, int], None]] = None,
        is_cancelled: Optional[Callable[[], bool]] = None,
    ) -> None:
        self._max_attempts = max(1, max_attempts)
        self._interval_seconds = max(0.1, interval_seconds)
        self._on_attempt = on_attempt
        self._is_cancelled = is_cancelled or (lambda: False)

    def execute_connect(self, transmitter: IFrameTransmitter) -> bool:
        """Attempts to connect the transmitter, retrying up to max_attempts."""
        for attempt in range(1, self._max_attempts + 1):
            if self._is_cancelled():
                logger.debug("Connection retry cancelled by caller.")
                return False

            if self._on_attempt:
                self._on_attempt(attempt, self._max_attempts)

            try:
                if transmitter.connect():
                    logger.info(
                        f"Transmitter {transmitter.__class__.__name__} connected successfully "
                        f"(attempt {attempt}/{self._max_attempts})."
                    )
                    return True
            except Exception as e:
                logger.debug(f"Connection attempt {attempt} failed: {e}")

            if attempt < self._max_attempts and not self._is_cancelled():
                # Sleep in short increments to respond quickly to cancellation
                sleep_start = time.perf_counter()
                while time.perf_counter() - sleep_start < self._interval_seconds:
                    if self._is_cancelled():
                        return False
                    time.sleep(0.1)

        logger.warning(
            f"Failed to connect transmitter {transmitter.__class__.__name__} after "
            f"{self._max_attempts} attempts."
        )
        return False
