"""Tests for MockTransmitter and OpenRGBTransmitter."""
import numpy as np
from openrgb_flowers.hardware.mock_transmitter import MockTransmitter
from openrgb_flowers.core.models.render_frame import RenderFrame


def test_mock_transmitter_send_frame():
    tx = MockTransmitter()
    assert not tx.is_connected()

    # Sending before connect should fail
    frame = RenderFrame(timestamp=0.1, frame_index=1, colors=np.zeros((10, 3), dtype=np.uint8), led_count=10)
    assert not tx.send_frame(frame)

    tx.connect()
    assert tx.is_connected()
    assert tx.send_frame(frame)
    assert tx.last_frame == frame
    assert len(tx.sent_frames) == 1

    tx.disconnect()
    assert not tx.is_connected()
