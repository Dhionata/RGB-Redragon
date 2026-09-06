"""Unit tests for CrashHandler error interception and logging."""
from pathlib import Path
from openrgb_flowers.core.crash_handler import CrashHandler


def test_crash_handler_log_exception(tmp_path: Path):
    log_file = tmp_path / "test_crash.log"
    try:
        raise ValueError("Simulated failure for testing")
    except ValueError as exc:
        recorded_path = CrashHandler.log_exception(exc, log_path=log_file)
        assert recorded_path == log_file

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "ValueError: Simulated failure for testing" in content
    assert "CRASH REPORT" in content


def test_crash_handler_run_safely_success():
    def dummy_success():
        return 42

    code = CrashHandler.run_safely(dummy_success)
    assert code == 42


def test_crash_handler_run_safely_system_exit():
    def dummy_exit():
        raise SystemExit(0)

    code = CrashHandler.run_safely(dummy_exit)
    assert code == 0


def test_crash_handler_run_safely_exception(monkeypatch, tmp_path: Path):
    dummy_log = tmp_path / "safe_crash.log"
    monkeypatch.setattr(CrashHandler, "get_default_log_path", staticmethod(lambda: dummy_log))
    monkeypatch.setattr(CrashHandler, "show_error_dialog", staticmethod(lambda title, msg: None))

    def dummy_failing():
        raise RuntimeError("Fatal startup problem")

    code = CrashHandler.run_safely(dummy_failing)
    assert code == 1
    assert dummy_log.exists()
    assert "RuntimeError: Fatal startup problem" in dummy_log.read_text(encoding="utf-8")
