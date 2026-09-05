"""Unit tests for GUI components, preview engine, and ControlPanel."""
import tkinter as tk
import pytest

from openrgb_flowers.gui.control_panel import ControlPanel
from openrgb_flowers.gui.gui_runner import GuiRunner
from openrgb_flowers.core.models.effect_config import EffectConfig


@pytest.fixture
def tk_root():
    root = tk.Tk()
    root.withdraw()
    yield root
    try:
        root.destroy()
    except Exception:
        pass


def test_control_panel_initialization(tk_root):
    started_settings = []
    panel = ControlPanel(
        tk_root,
        on_start=lambda s: started_settings.append(s),
        on_stop=lambda: None,
    )
    settings = panel.get_current_settings()
    assert "effect_type" in settings
    assert "palette" in settings
    assert "speed" in settings
    assert "brightness" in settings
    assert "saturation" in settings
    assert "fps" in settings
    assert settings["saturation"] == 1.0
    assert settings["brightness"] == 1.0


def test_control_panel_apply_and_undo(tk_root):
    applied = []
    undone = []
    panel = ControlPanel(
        tk_root,
        on_start=lambda s: None,
        on_stop=lambda: None,
        on_apply=lambda s: applied.append(s),
        on_undo=lambda: undone.append(True),
    )

    # Start effect
    panel._trigger_start()
    assert panel._is_running

    # Modify speed and saturation
    panel._speed_scale.set(3.0)
    panel._saturation_scale.set(180)
    panel._on_control_changed()

    # Buttons should now be enabled
    assert str(panel._btn_apply['state']) == 'normal'
    assert str(panel._btn_undo['state']) == 'normal'

    # Apply changes
    panel._trigger_apply()
    assert len(applied) == 1
    assert applied[0]['speed'] == 3.0
    assert applied[0]['saturation'] == 1.8
    assert str(panel._btn_apply['state']) == 'disabled'

    # Change again and undo
    panel._speed_scale.set(0.5)
    panel._on_control_changed()
    assert str(panel._btn_undo['state']) == 'normal'

    panel._trigger_undo()
    assert len(undone) == 1
    assert panel._speed_scale.get() == 3.0
    assert str(panel._btn_undo['state']) == 'disabled'


def test_gui_runner_update_config():
    frames = []
    runner = GuiRunner(
        on_frame=lambda f: frames.append(f),
        on_status=lambda s, a: None,
        on_fps_update=lambda fps: None,
    )
    cfg = EffectConfig(effect_type="random_blend", speed=1.0)
    runner.update_config(cfg, "random_blend")

    with runner._lock:
        assert runner._pending_config == cfg
        assert runner._pending_effect_name == "random_blend"
