"""Tests for CLI argument parser and execution."""
from openrgb_flowers.cli.argument_parser import ArgumentParserBuilder
from openrgb_flowers.cli.main import main


def test_argument_parser_defaults():
    parser = ArgumentParserBuilder.build()
    args = parser.parse_args([])
    assert args.palette == "sakura"
    assert args.fps == 30.0
    assert args.speed == 1.0
    assert args.blend == "weighted"


def test_argument_parser_custom():
    parser = ArgumentParserBuilder.build()
    args = parser.parse_args(["--palette", "lotus", "--fps", "60", "--speed", "2.5", "--mock"])
    assert args.palette == "lotus"
    assert args.fps == 60.0
    assert args.speed == 2.5
    assert args.mock is True


def test_cli_main_mock_run(monkeypatch):
    from openrgb_flowers.service.runner_service import RunnerService

    orig_run = RunnerService.run
    def fast_run(self, max_frames=None):
        orig_run(self, max_frames=5)

    monkeypatch.setattr(RunnerService, "run", fast_run)
    exit_code = main(["--mock", "--palette", "rose"])
    assert exit_code == 0
