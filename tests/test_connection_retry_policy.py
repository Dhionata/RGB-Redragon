"""Unit tests for ConnectionRetryPolicy."""
from unittest.mock import MagicMock
import pytest

from openrgb_flowers.hardware.connection_retry_policy import ConnectionRetryPolicy


def test_retry_policy_immediate_success():
    mock_transmitter = MagicMock()
    mock_transmitter.connect.return_value = True

    policy = ConnectionRetryPolicy(max_attempts=3, interval_seconds=0.01)
    result = policy.execute_connect(mock_transmitter)

    assert result is True
    assert mock_transmitter.connect.call_count == 1


def test_retry_policy_eventual_success():
    mock_transmitter = MagicMock()
    # Fails first two times, succeeds on third
    mock_transmitter.connect.side_effect = [False, False, True]

    attempts = []
    policy = ConnectionRetryPolicy(
        max_attempts=5,
        interval_seconds=0.01,
        on_attempt=lambda cur, tot: attempts.append(cur),
    )
    result = policy.execute_connect(mock_transmitter)

    assert result is True
    assert mock_transmitter.connect.call_count == 3
    assert attempts == [1, 2, 3]


def test_retry_policy_exhaustion():
    mock_transmitter = MagicMock()
    mock_transmitter.connect.return_value = False

    policy = ConnectionRetryPolicy(max_attempts=3, interval_seconds=0.01)
    result = policy.execute_connect(mock_transmitter)

    assert result is False
    assert mock_transmitter.connect.call_count == 3


def test_retry_policy_cancellation():
    mock_transmitter = MagicMock()
    mock_transmitter.connect.return_value = False

    cancelled = [False]
    def check_cancelled():
        return cancelled[0]

    policy = ConnectionRetryPolicy(
        max_attempts=5,
        interval_seconds=0.01,
        is_cancelled=check_cancelled,
    )
    cancelled[0] = True
    result = policy.execute_connect(mock_transmitter)

    assert result is False
    assert mock_transmitter.connect.call_count == 0
