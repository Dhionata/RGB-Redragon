"""Unit tests for Inno Setup installer builder and locator (SOLID & DRY)."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from build_tools.inno_builder import InnoSetupBuilder
from build_tools.inno_locator import InnoSetupLocator
from build_tools.version_reader import VersionReader


# ---------------------------------------------------------------------------
# VersionReader Tests
# ---------------------------------------------------------------------------
def test_version_reader_existing_project():
    version = VersionReader.get_version()
    assert version == "1.0.0"


def test_version_reader_custom_dir(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "test-pkg"\nversion = "2.4.1"\n', encoding="utf-8")
    assert VersionReader.get_version(tmp_path) == "2.4.1"


def test_version_reader_fallback_on_missing(tmp_path: Path):
    assert VersionReader.get_version(tmp_path) == "1.0.0"


# ---------------------------------------------------------------------------
# InnoSetupLocator Tests
# ---------------------------------------------------------------------------
def test_inno_locator_candidates_list():
    locator = InnoSetupLocator()
    candidates = locator.get_candidate_paths()
    assert len(candidates) > 0
    assert any("Inno Setup 6" in str(c) for c in candidates)


def test_inno_locator_explicit_path(tmp_path: Path):
    fake_iscc = tmp_path / "ISCC.exe"
    fake_iscc.write_text("dummy binary")

    locator = InnoSetupLocator()
    # Explicit file
    found = locator.find_iscc(explicit_path=fake_iscc)
    assert found == fake_iscc.resolve()

    # Explicit directory
    found_dir = locator.find_iscc(explicit_path=tmp_path)
    assert found_dir == fake_iscc.resolve()


def test_inno_locator_path_lookup(tmp_path: Path):
    fake_iscc = tmp_path / "iscc.exe"
    fake_iscc.write_text("dummy")

    with patch("shutil.which", return_value=str(fake_iscc)):
        locator = InnoSetupLocator()
        found = locator.find_iscc()
        assert found == fake_iscc.resolve()


def test_inno_locator_guidance():
    guidance = InnoSetupLocator.get_installation_guidance()
    assert "winget install JRSoftware.InnoSetup" in guidance
    assert "https://jrsoftware.org/isdl.php" in guidance


# ---------------------------------------------------------------------------
# InnoSetupBuilder Tests
# ---------------------------------------------------------------------------
def test_inno_builder_validate_prerequisites_missing_iss(tmp_path: Path):
    builder = InnoSetupBuilder(
        iss_file=tmp_path / "nonexistent.iss",
        source_dir=tmp_path / "portable",
        output_dir=tmp_path / "dist",
    )
    valid, msg = builder.validate_prerequisites()
    assert not valid
    assert "Arquivo de script Inno Setup nao encontrado" in msg


def test_inno_builder_validate_prerequisites_missing_source_dir(tmp_path: Path):
    iss_file = tmp_path / "installer.iss"
    iss_file.write_text("[Setup]")
    builder = InnoSetupBuilder(
        iss_file=iss_file,
        source_dir=tmp_path / "nonexistent_dir",
        output_dir=tmp_path / "dist",
    )
    valid, msg = builder.validate_prerequisites()
    assert not valid
    assert "Diretorio de origem nao encontrado" in msg


def test_inno_builder_validate_prerequisites_missing_executable(tmp_path: Path):
    iss_file = tmp_path / "installer.iss"
    iss_file.write_text("[Setup]")
    source_dir = tmp_path / "portable"
    source_dir.mkdir()

    builder = InnoSetupBuilder(
        iss_file=iss_file,
        source_dir=source_dir,
        output_dir=tmp_path / "dist",
        main_executable="FlowersBlooming.exe",
    )
    valid, msg = builder.validate_prerequisites()
    assert not valid
    assert "Executavel principal 'FlowersBlooming.exe' nao encontrado" in msg


def test_inno_builder_validate_prerequisites_missing_iscc(tmp_path: Path):
    iss_file = tmp_path / "installer.iss"
    iss_file.write_text("[Setup]")
    source_dir = tmp_path / "portable"
    source_dir.mkdir()
    (source_dir / "FlowersBlooming.exe").write_text("binary")

    mock_locator = MagicMock(spec=InnoSetupLocator)
    mock_locator.find_iscc.return_value = None
    mock_locator.get_installation_guidance.return_value = "Guidance to install"

    builder = InnoSetupBuilder(
        iss_file=iss_file,
        source_dir=source_dir,
        output_dir=tmp_path / "dist",
        locator=mock_locator,
    )
    valid, msg = builder.validate_prerequisites()
    assert not valid
    assert "Guidance to install" in msg


def test_inno_builder_command_generation(tmp_path: Path):
    iss_file = tmp_path / "installer.iss"
    iss_file.write_text("[Setup]")
    source_dir = tmp_path / "portable"
    source_dir.mkdir()
    (source_dir / "FlowersBlooming.exe").write_text("binary")
    fake_iscc = tmp_path / "ISCC.exe"
    fake_iscc.write_text("dummy")

    mock_locator = MagicMock(spec=InnoSetupLocator)
    mock_locator.find_iscc.return_value = fake_iscc

    builder = InnoSetupBuilder(
        iss_file=iss_file,
        source_dir=source_dir,
        output_dir=tmp_path / "dist",
        output_name="FlowersBlooming_Setup",
        app_version="1.2.3",
        locator=mock_locator,
    )

    cmd = builder.build_command()
    assert cmd[0] == str(fake_iscc)
    assert "/DMyAppVersion=1.2.3" in cmd
    assert f"/DSourceDir={source_dir.resolve()}" in cmd
    assert f"/DOutputDir={(tmp_path / 'dist').resolve()}" in cmd
    assert "/DOutputBaseFilename=FlowersBlooming_Setup" in cmd
    assert str(iss_file.resolve()) in cmd


def test_inno_builder_run_success(tmp_path: Path):
    iss_file = tmp_path / "installer.iss"
    iss_file.write_text("[Setup]")
    source_dir = tmp_path / "portable"
    source_dir.mkdir()
    (source_dir / "FlowersBlooming.exe").write_text("binary")
    fake_iscc = tmp_path / "ISCC.exe"
    fake_iscc.write_text("dummy")

    mock_locator = MagicMock(spec=InnoSetupLocator)
    mock_locator.find_iscc.return_value = fake_iscc

    out_dir = tmp_path / "dist"
    builder = InnoSetupBuilder(
        iss_file=iss_file,
        source_dir=source_dir,
        output_dir=out_dir,
        output_name="FlowersBlooming_Setup",
        locator=mock_locator,
    )

    def fake_subprocess_run(cmd):
        # Simulate successful creation of installer binary
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "FlowersBlooming_Setup.exe").write_bytes(b"MZ" + b"\x00" * 1024)
        mock_result = MagicMock()
        mock_result.returncode = 0
        return mock_result

    with patch("subprocess.run", side_effect=fake_subprocess_run):
        ret = builder.run()
        assert ret == 0
        assert (out_dir / "FlowersBlooming_Setup.exe").is_file()


# ---------------------------------------------------------------------------
# installer.iss Verification
# ---------------------------------------------------------------------------
def test_installer_iss_content_integrity():
    iss_path = Path(__file__).resolve().parent.parent / "installer.iss"
    assert iss_path.is_file(), "installer.iss file must exist at project root"

    content = iss_path.read_text(encoding="utf-8")

    # Essential Inno Setup sections
    for section in ["[Setup]", "[Files]", "[Icons]", "[Tasks]", "[Run]", "[UninstallDelete]"]:
        assert section in content, f"Missing section {section} in installer.iss"

    # Crucial configuration directives
    assert "PrivilegesRequired=lowest" in content
    assert "{autopf}\\OpenRGB Flowers" in content
    assert "OutputBaseFilename={#OutputBaseFilename}" in content
    assert "SourceDir" in content
    assert "CloseApplications=yes" in content
    assert "ArchitecturesInstallIn64BitMode=x64" in content
    assert 'WorkingDir: "{app}"' in content


def test_inno_builder_output_name_with_exe_extension(tmp_path: Path):
    iss_file = tmp_path / "installer.iss"
    iss_file.write_text("[Setup]")
    source_dir = tmp_path / "portable"
    source_dir.mkdir()
    (source_dir / "FlowersBlooming.exe").write_text("binary")
    fake_iscc = tmp_path / "ISCC.exe"
    fake_iscc.write_text("dummy")

    mock_locator = MagicMock(spec=InnoSetupLocator)
    mock_locator.find_iscc.return_value = fake_iscc

    builder = InnoSetupBuilder(
        iss_file=iss_file,
        source_dir=source_dir,
        output_dir=tmp_path / "dist",
        output_name="FlowersBlooming_Setup.exe",
        locator=mock_locator,
    )

    cmd = builder.build_command()
    # OutputBaseFilename must NOT have double .exe
    assert "/DOutputBaseFilename=FlowersBlooming_Setup" in cmd
    assert builder.output_name == "FlowersBlooming_Setup"


def test_inno_locator_quoted_explicit_path(tmp_path: Path):
    fake_iscc = tmp_path / "ISCC.exe"
    fake_iscc.write_text("dummy binary")

    locator = InnoSetupLocator()
    quoted_path = f'"{fake_iscc.resolve()}"'
    found = locator.find_iscc(explicit_path=quoted_path)
    assert found == fake_iscc.resolve()


def test_version_reader_multi_section_toml(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[tool.some_dependency]\nversion = "0.1.0"\n'
        '[project]\nname = "flower-app"\nversion = "3.2.1"\n'
        '[tool.other]\nversion = "9.9.9"\n',
        encoding="utf-8"
    )
    assert VersionReader.get_version(tmp_path) == "3.2.1"


# ---------------------------------------------------------------------------
# CI/CD Release Pipeline & Dependency Integrity
# ---------------------------------------------------------------------------
def test_release_pipeline_dependencies_integrity():
    root = Path(__file__).resolve().parent.parent
    req_dev = (root / "requirements-dev.txt").read_text(encoding="utf-8")
    assert "nuitka" in req_dev.lower(), "requirements-dev.txt must include nuitka for CI build"
    assert "pytest" in req_dev.lower(), "requirements-dev.txt must include pytest"

    setup_py = (root / "setup.py").read_text(encoding="utf-8")
    assert "nuitka" in setup_py.lower(), "setup.py extras_require['dev'] must include nuitka"

    workflow_file = root / ".github" / "workflows" / "release.yml"
    assert workflow_file.is_file(), "release.yml workflow must exist"
    wf_text = workflow_file.read_text(encoding="utf-8")
    assert "branches:" in wf_text and "main" in wf_text, "release.yml must trigger on main branch"
    assert "v*" in wf_text, "release.yml must trigger on v* tags"
    assert "pip install -e .[dev]" in wf_text, "release.yml must install dev extras"

