"""Unit tests for build_tools components (SOLID & DRY)."""
from pathlib import Path
from build_tools.process_manager import ProcessManager
from build_tools.nuitka_builder import NuitkaBuilder


def test_process_manager_terminate():
    # Should safely complete without throwing any exception
    ProcessManager.terminate_processes(["non_existent_process_12345.exe"])


def test_nuitka_builder_command_standalone():
    builder = NuitkaBuilder(
        entry_point="launcher.py",
        output_name="FlowersBlooming.exe",
        output_dir="dist",
        onefile=False,
    )
    cmd = builder.build_command()

    assert "--standalone" in cmd
    assert "--onefile" not in cmd
    assert "--mingw64" in cmd
    assert "--lto=yes" in cmd
    assert "--disable-cache=ccache" in cmd
    assert "--windows-console-mode=attach" in cmd
    assert "--output-filename=FlowersBlooming.exe" in cmd
    assert "--enable-plugin=tk-inter" in cmd
    assert "--include-package=openrgb_flowers" in cmd
    assert "--include-package=openrgb" in cmd
    assert "--include-module=hid" in cmd


def test_nuitka_builder_command_onefile():
    builder = NuitkaBuilder(
        entry_point="launcher.py",
        output_name="FlowersBlooming.exe",
        output_dir="dist",
        onefile=True,
    )
    cmd = builder.build_command()

    assert "--onefile" in cmd
    assert "--standalone" not in cmd
    assert "--output-filename=FlowersBlooming.exe" in cmd
    assert "--include-package=openrgb" in cmd


def test_nuitka_builder_cleanup_unwanted_files(tmp_path: Path):
    builder = NuitkaBuilder(output_dir=str(tmp_path))

    valid_file = tmp_path / "FlowersBlooming.exe"
    unwanted_file1 = tmp_path / "RedragonFlowers.exe"
    unwanted_file2 = tmp_path / "RedragonRGB.exe"

    valid_file.write_text("ok")
    unwanted_file1.write_text("bad")
    unwanted_file2.write_text("bad")

    builder._cleanup_unwanted_files(tmp_path)

    assert valid_file.exists()
    assert not unwanted_file1.exists()
    assert not unwanted_file2.exists()


def test_nuitka_builder_cleanup_mode_conflicts_standalone(tmp_path: Path):
    builder = NuitkaBuilder(output_dir=str(tmp_path), onefile=False)

    root_exe = tmp_path / "FlowersBlooming.exe"
    root_exe.write_text("stale onefile exe")

    builder.cleanup_mode_conflicts()
    assert not root_exe.exists()


def test_nuitka_builder_cleanup_mode_conflicts_onefile(tmp_path: Path):
    builder = NuitkaBuilder(output_dir=str(tmp_path), onefile=True)

    portable_dir = tmp_path / "FlowersBlooming_Portable"
    portable_dir.mkdir(parents=True, exist_ok=True)
    (portable_dir / "dummy.txt").write_text("dummy")

    portable_zip = tmp_path / "FlowersBlooming_Portable.zip"
    portable_zip.write_text("dummy zip")

    builder.cleanup_mode_conflicts()
    assert not portable_dir.exists()
    assert not portable_zip.exists()

