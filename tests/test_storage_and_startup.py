"""Unit tests for ConfigStorageService and WindowsStartupService."""
import platform
import sys
from pathlib import Path
import pytest

from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.service.config_storage_service import ConfigStorageService
from openrgb_flowers.service.windows_startup_service import WindowsStartupService


def test_config_storage_save_and_load(tmp_path: Path):
    custom_cfg_path = tmp_path / "test_user_config.json"
    storage = ConfigStorageService(custom_path=custom_cfg_path)

    cfg = EffectConfig(
        effect_type="random_blend",
        palette_name="cyberpunk",
        speed=2.5,
        brightness=0.8,
        saturation=1.5,
        fps=45.0,
        max_flowers=10,
    )

    success = storage.save_config(cfg, {"driver": "redragon"})
    assert success is True
    assert custom_cfg_path.exists()

    loaded = storage.load_config()
    assert loaded.effect_type == "random_blend"
    assert loaded.palette_name == "cyberpunk"
    assert loaded.speed == 2.5
    assert loaded.brightness == 0.8
    assert loaded.saturation == 1.5
    assert loaded.fps == 45.0
    assert loaded.max_flowers == 10


def test_config_storage_default_fallback(tmp_path: Path):
    non_existent = tmp_path / "does_not_exist.json"
    storage = ConfigStorageService(custom_path=non_existent)
    loaded = storage.load_config()
    assert loaded.effect_type in ["random_blend", "blooming"]
    assert loaded.speed > 0


def test_windows_startup_resolve_command():
    service = WindowsStartupService(app_name="OpenRGBFlowersTest")
    cmd = service._resolve_launch_command("--autostart")
    assert "--autostart" in cmd
    if platform.system().lower() == "windows":
        assert "python" in cmd.lower() or ".exe" in cmd.lower()


def test_windows_startup_enable_and_disable():
    if platform.system().lower() != "windows":
        pytest.skip("Windows only test")

    test_app_name = "OpenRGBFlowers_UnitTest_Temp"
    service = WindowsStartupService(app_name=test_app_name)

    try:
        # Enable
        enabled = service.enable("--autostart")
        assert enabled is True
        assert service.is_enabled() is True

        # Disable
        disabled = service.disable()
        assert disabled is True
        assert service.is_enabled() is False
    finally:
        service.disable()
