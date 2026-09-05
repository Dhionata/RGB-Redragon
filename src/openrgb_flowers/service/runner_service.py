"""Execution service coordinating the main loop, frame pacing, and signals."""
from __future__ import annotations
import logging
import signal
import sys
import time
from typing import Optional

from openrgb_flowers.core.interfaces.i_effect_engine import IEffectEngine
from openrgb_flowers.core.interfaces.i_frame_transmitter import IFrameTransmitter
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.interfaces.i_visualizer import IVisualizer
from openrgb_flowers.core.models.effect_config import EffectConfig

logger = logging.getLogger("openrgb_flowers.service")


class RunnerService:
    """Coordinates high-performance main loop with precise frame pacing and clean shutdown."""

    def __init__(
        self,
        engine: IEffectEngine,
        transmitter: IFrameTransmitter,
        layout_provider: ILayoutProvider,
        config: EffectConfig,
        visualizer: Optional[IVisualizer] = None,
    ) -> None:
        self._engine = engine
        self._transmitter = transmitter
        self._layout = layout_provider
        self._config = config
        self._visualizer = visualizer
        self._running = False

    def stop(self) -> None:
        """Signals the main loop to stop."""
        self._running = False

    def run(self, max_frames: Optional[int] = None) -> None:
        """Runs the main effect rendering loop.

        Args:
            max_frames: Optional limit of frames to render (useful for tests/benchmarks).
        """
        self._running = True

        # Signal handlers for clean shutdown
        def _sig_handler(sig, frame):
            self.stop()

        try:
            signal.signal(signal.SIGINT, _sig_handler)
            signal.signal(signal.SIGTERM, _sig_handler)
        except (ValueError, AttributeError):
            # Signal handling may differ on some environments/threads
            pass

        # Connect transmitter
        self._transmitter.connect()

        target_fps = self._config.fps
        frame_time = 1.0 / target_fps
        prev_time = time.perf_counter()
        frames_rendered = 0

        logger.info(f"Starting Flowers Blooming effect loop @ {target_fps:.1f} FPS...")

        try:
            while self._running:
                loop_start = time.perf_counter()
                dt = loop_start - prev_time
                prev_time = loop_start

                # Clamp dt to avoid huge leap on lag spike
                dt_clamped = min(0.1, max(0.001, dt))

                # Advance simulation and render frame
                frame = self._engine.tick(dt_clamped)

                # Transmit frame to hardware
                self._transmitter.send_frame(frame)

                # Optional live visualizer
                if self._visualizer:
                    active_blooms = self._engine.get_active_flower_count()
                    self._visualizer.render(frame, self._layout, active_blooms, target_fps)

                frames_rendered += 1
                if max_frames and frames_rendered >= max_frames:
                    break

                # Precise frame throttling
                elapsed = time.perf_counter() - loop_start
                sleep_time = frame_time - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

        finally:
            logger.info("Shutting down Flowers Blooming effect...")
            if self._visualizer:
                self._visualizer.close()
            self._transmitter.disconnect()
