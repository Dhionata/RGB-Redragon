"""Threaded runner coordinating background lighting loop and GUI canvas dispatch."""
from __future__ import annotations
import logging
import threading
import time
from typing import Callable, Optional

from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.core.interfaces.i_effect_engine import IEffectEngine
from openrgb_flowers.core.interfaces.i_frame_transmitter import IFrameTransmitter
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.effects.effect_engine_factory import EffectEngineFactory
from openrgb_flowers.hardware.layout_factory import LayoutFactory
from openrgb_flowers.hardware.transmitter_factory import TransmitterFactory
from openrgb_flowers.hardware.redragon_k556_transmitter import RedragonK556Transmitter
from openrgb_flowers.hardware.k556_matrix_layout_provider import K556MatrixLayoutProvider
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider

logger = logging.getLogger("openrgb_flowers.gui.runner")


class GuiRunner:
    """Manages asynchronous rendering thread without blocking the GUI event loop."""

    def __init__(
        self,
        on_frame: Callable[[RenderFrame], None],
        on_status: Callable[[str, bool], None],
        on_fps_update: Callable[[float], None],
    ) -> None:
        self._on_frame = on_frame
        self._on_status = on_status
        self._on_fps_update = on_fps_update

        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._running = False
        self._lock = threading.Lock()
        self._pending_config: Optional[EffectConfig] = None
        self._pending_effect_name: Optional[str] = None

    def is_running(self) -> bool:
        return self._running

    def start(self, config: EffectConfig, effect_name: str, driver: str) -> None:
        """Starts background rendering thread."""
        if self._running:
            return

        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._worker_loop,
            args=(config, effect_name, driver),
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        """Signals background thread to terminate."""
        if not self._running:
            return

        self._running = False
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.5)
        self._thread = None
        self._on_status("Parado / Idle", False)

    def update_config(self, config: EffectConfig, effect_name: Optional[str] = None) -> None:
        """Applies dynamic parameter changes to the running worker without reconnecting hardware."""
        with self._lock:
            self._pending_config = config
            self._pending_effect_name = effect_name

    def _worker_loop(self, config: EffectConfig, effect_name: str, driver: str) -> None:
        """Worker loop executing on background thread."""
        transmitter: Optional[IFrameTransmitter] = None
        try:
            self._on_status("Conectando ao hardware...", True)

            # 1. Resolve transmitter
            transmitter = TransmitterFactory.create_transmitter(
                driver=driver,
                host=config.host,
                port=config.port,
                device_name=config.device_name,
            )
            transmitter.connect()

            # 2. Resolve layout provider
            if isinstance(transmitter, RedragonK556Transmitter):
                layout: ILayoutProvider = K556MatrixLayoutProvider()
            else:
                layout = K556LayoutProvider()

            # 3. Adapt to live device if connected via OpenRGB
            device = getattr(transmitter, "device", None)
            if device is not None:
                layout = LayoutFactory.create_layout(device)

            # 4. Instantiate effect engine via factory
            engine: IEffectEngine = EffectEngineFactory.create_engine(
                effect_name=effect_name,
                config=config,
                layout_provider=layout,
            )

            status_text = (
                f"Transmitindo: {effect_name.upper()} | {transmitter.__class__.__name__} ({layout.get_key_count()} LEDs)"
            )
            self._on_status(status_text, True)

            target_fps = max(10.0, float(config.fps))
            frame_interval = 1.0 / target_fps
            prev_time = time.perf_counter()
            fps_timer = time.perf_counter()
            fps_counter = 0

            while not self._stop_event.is_set():
                # Process any on-the-fly configuration/effect changes
                with self._lock:
                    if self._pending_config is not None:
                        new_cfg = self._pending_config
                        new_eff = self._pending_effect_name or effect_name
                        self._pending_config = None
                        self._pending_effect_name = None

                        if new_eff != effect_name:
                            effect_name = new_eff
                            engine = EffectEngineFactory.create_engine(
                                effect_name=effect_name,
                                config=new_cfg,
                                layout_provider=layout,
                            )
                            self._on_status(
                                f"Transmitindo: {effect_name.upper()} | {transmitter.__class__.__name__} ({layout.get_key_count()} LEDs)",
                                True,
                            )
                        else:
                            engine.update_config(new_cfg)

                        target_fps = max(10.0, float(new_cfg.fps))
                        frame_interval = 1.0 / target_fps

                t_start = time.perf_counter()
                dt = min(0.1, max(0.001, t_start - prev_time))
                prev_time = t_start

                # Tick engine & transmit frame
                frame = engine.tick(dt)
                transmitter.send_frame(frame)

                # Dispatch frame to UI
                self._on_frame(frame)

                fps_counter += 1
                now = time.perf_counter()
                if now - fps_timer >= 0.5:
                    actual_fps = fps_counter / (now - fps_timer)
                    self._on_fps_update(actual_fps)
                    fps_counter = 0
                    fps_timer = now

                # Sleep to maintain FPS
                elapsed = time.perf_counter() - t_start
                sleep_sec = frame_interval - elapsed
                if sleep_sec > 0:
                    time.sleep(sleep_sec)

        except Exception as e:
            logger.error(f"Error in GUI worker loop: {e}", exc_info=True)
            self._on_status(f"Erro: {e}", False)
        finally:
            if transmitter is not None:
                try:
                    transmitter.disconnect()
                except Exception:
                    pass
            self._running = False
            self._on_status("Parado / Pronto", False)
