"""Tests for RunnerService."""
from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.hardware.k556_layout_provider import K556LayoutProvider
from openrgb_flowers.effects.blooming_engine import BloomingEngine
from openrgb_flowers.hardware.mock_transmitter import MockTransmitter
from openrgb_flowers.service.runner_service import RunnerService


def test_runner_service_execution():
    config = EffectConfig(fps=60.0, speed=2.0)
    layout = K556LayoutProvider()
    engine = BloomingEngine(config=config, layout_provider=layout)
    tx = MockTransmitter()

    service = RunnerService(
        engine=engine,
        transmitter=tx,
        layout_provider=layout,
        config=config,
    )

    # Run for 15 frames
    service.run(max_frames=15)
    assert len(tx.sent_frames) == 15
    assert not tx.is_connected()  # Disconnected at shutdown
