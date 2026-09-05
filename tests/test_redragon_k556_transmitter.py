"""Unit tests for RedragonK556Transmitter."""
from unittest.mock import MagicMock
import numpy as np
import pytest

from openrgb_flowers.hardware.redragon_k556_transmitter import RedragonK556Transmitter
from openrgb_flowers.core.models.render_frame import RenderFrame


def test_packet_structure_and_headers():
    tx = RedragonK556Transmitter()
    assert len(tx._packets) == 8

    for c, pkt in enumerate(tx._packets):
        assert len(pkt) == 65
        assert pkt[0] == 0x01  # Report ID
        assert pkt[1] == 0x09  # CMD_CUSTOM_CHUNK (Command 0x09)
        assert pkt[2] == 0x00  # Custom index 0
        assert pkt[3] == (c >> 8) & 0xFF
        assert pkt[4] == c & 0xFF
        expected_bytes = 54 if c < 7 else 18
        assert pkt[5] == expected_bytes


def test_send_frame_when_not_connected():
    tx = RedragonK556Transmitter()
    dummy_colors = np.zeros((132, 3), dtype=np.uint8)
    frame = RenderFrame(timestamp=0.0, frame_index=1, colors=dummy_colors, led_count=132)
    assert not tx.send_frame(frame)


def test_send_frame_with_mock_device():
    tx = RedragonK556Transmitter()
    mock_dev = MagicMock()
    mock_dev.write.return_value = 64
    mock_dev.read.return_value = []

    tx._device = mock_dev
    tx._connected = True

    # 132 colors with vibrant distinct test values
    colors = np.ones((132, 3), dtype=np.uint8) * 128
    colors[0] = [255, 10, 20]  # First key in chunk 0
    colors[131] = [50, 60, 70] # Last key in chunk 7

    frame = RenderFrame(timestamp=1.5, frame_index=42, colors=colors, led_count=132)
    success = tx.send_frame(frame)

    assert success
    assert mock_dev.write.call_count == 8

    # Verify first chunk RGB payload
    first_pkt = tx._packets[0]
    assert first_pkt[6] == 255
    assert first_pkt[7] == 10
    assert first_pkt[8] == 20

    # Verify last chunk RGB payload (last key is 6th key in chunk 7)
    last_pkt = tx._packets[7]
    # Key 5 in chunk 7 offset: 6 + 5*3 = 21
    assert last_pkt[21] == 50
    assert last_pkt[22] == 60
    assert last_pkt[23] == 70


def test_connect_initializes_mode_10(monkeypatch):
    tx = RedragonK556Transmitter()
    mock_hid = MagicMock()
    mock_dev_instance = MagicMock()
    mock_dev_instance.read.side_effect = [b"", b""]
    mock_hid.device.return_value = mock_dev_instance
    mock_hid.enumerate.return_value = [{"interface_number": 2, "path": b"test_path"}]

    monkeypatch.setattr("hid.enumerate", mock_hid.enumerate)
    monkeypatch.setattr("hid.device", mock_hid.device)

    connected = tx.connect()
    assert connected
    assert tx.is_connected()
    # connect() should have written 2 packets: mode 10 (cmd 0x07) and init (cmd 0x09 0x20)
    assert mock_dev_instance.write.call_count == 2
    calls = mock_dev_instance.write.call_args_list

    mode_pkt = calls[0][0][0]
    assert mode_pkt[0] == 0x01
    assert mode_pkt[1] == 0x07
    assert mode_pkt[6] == 10  # Mode 10

    init_pkt = calls[1][0][0]
    assert init_pkt[0] == 0x01
    assert init_pkt[1] == 0x09
    assert init_pkt[2] == 0x20
