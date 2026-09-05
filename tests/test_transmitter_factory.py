"""Unit tests for TransmitterFactory."""
from unittest.mock import patch
import pytest

from openrgb_flowers.hardware.transmitter_factory import TransmitterFactory
from openrgb_flowers.hardware.mock_transmitter import MockTransmitter
from openrgb_flowers.hardware.redragon_k556_transmitter import RedragonK556Transmitter
from openrgb_flowers.hardware.openrgb_transmitter import OpenRGBTransmitter


def test_create_mock_transmitter():
    tx = TransmitterFactory.create_transmitter(driver="mock")
    assert isinstance(tx, MockTransmitter)


def test_create_redragon_transmitter():
    tx = TransmitterFactory.create_transmitter(driver="redragon")
    assert isinstance(tx, RedragonK556Transmitter)


def test_create_openrgb_transmitter():
    tx = TransmitterFactory.create_transmitter(driver="openrgb", host="127.0.0.1", port=6742)
    assert isinstance(tx, OpenRGBTransmitter)
    assert tx._host == "127.0.0.1"
    assert tx._port == 6742


def test_create_auto_transmitter_when_redragon_present():
    with patch.object(TransmitterFactory, "is_redragon_k556_connected", return_value=True):
        tx = TransmitterFactory.create_transmitter(driver="auto")
        assert isinstance(tx, RedragonK556Transmitter)


def test_create_auto_transmitter_when_redragon_not_present():
    with patch.object(TransmitterFactory, "is_redragon_k556_connected", return_value=False):
        tx = TransmitterFactory.create_transmitter(driver="auto")
        assert isinstance(tx, OpenRGBTransmitter)
