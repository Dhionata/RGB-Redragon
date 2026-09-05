"""Unit tests for SystemTrayManager and tray icon integration."""
from unittest.mock import MagicMock
from openrgb_flowers.gui.system_tray import SystemTrayManager, ISystemTray


def test_system_tray_manager_lifecycle():
    mock_restore = MagicMock()
    mock_quit = MagicMock()

    tray = SystemTrayManager(
        on_restore=mock_restore,
        on_quit=mock_quit,
        tooltip="Test Tray Tooltip",
    )

    # Verify protocol compliance
    assert isinstance(tray, ISystemTray)
    assert not tray.is_running()

    # Verify image generation
    img = tray.create_tray_image(size=32)
    assert img.size == (32, 32)
    assert img.mode == "RGBA"

    # Test handlers invocation
    tray._handle_restore()
    mock_restore.assert_called_once()

    tray._handle_quit()
    mock_quit.assert_called_once()
