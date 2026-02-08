#!/usr/bin/env python3
"""
Acceptance and Unit Tests for load_directives.py

Tests directive loading functionality that replaces load_directives.sh
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add framework-core directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "ops" / "framework-core"))

# Import will be available after we create the module
# from load_directives import DirectiveLoader


@pytest.fixture
def temp_directives_dir(tmp_path: Path) -> Path:
    """Create a temporary directives directory with sample files."""
    directives_dir = tmp_path / "directives"
    directives_dir.mkdir()

    # Create sample directive files
    (directives_dir / "001_cli_shell_tooling.md").write_text(
        "# Directive 001: CLI Tooling\n\nSample content for directive 001.",
        encoding="utf-8",
    )
    (directives_dir / "006_version_governance.md").write_text(
        "# Directive 006: Version Governance\n\nSample content for directive 006.",
        encoding="utf-8",
    )
    (directives_dir / "014_worklog_creation.md").write_text(
        "# Directive 014: Work Log Creation\n\nSample content for directive 014.",
        encoding="utf-8",
    )

    return directives_dir


# ============================================================================
# Acceptance Tests
# ============================================================================


def test_list_available_directives(temp_directives_dir: Path) -> None:
    """
    Acceptance Test: List all available directives.

    Given a directives directory with multiple files
    When requesting a list of directives
    Then all directive codes and filenames should be returned.
    """
    # Arrange
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(temp_directives_dir)

    # Assumption Check
    assert (
        temp_directives_dir.exists()
    ), "Test precondition: directives dir should exist"
    assert (
        len(list(temp_directives_dir.glob("*.md"))) == 3
    ), "Test precondition: should have 3 directives"

    # Act
    directives = loader.list_directives()

    # Assert
    assert len(directives) == 3, "Should list 3 directives"
    assert any(d["code"] == "001" for d in directives), "Should include directive 001"
    assert any(d["code"] == "006" for d in directives), "Should include directive 006"
    assert any(d["code"] == "014" for d in directives), "Should include directive 014"


def test_load_single_directive(temp_directives_dir: Path) -> None:
    """
    Acceptance Test: Load a single directive by code.

    Given a directive code
    When loading the directive
    Then the directive content should be returned with markers.
    """
    # Arrange
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(temp_directives_dir)

    # Assumption Check
    assert (temp_directives_dir / "001_cli_shell_tooling.md").exists()

    # Act
    content = loader.load_directives(["001"])

    # Assert
    assert "<!-- Directive 001 Begin -->" in content
    assert "# Directive 001: CLI Tooling" in content
    assert "Sample content for directive 001" in content
    assert "<!-- Directive 001 End -->" in content


def test_load_multiple_directives(temp_directives_dir: Path) -> None:
    """
    Acceptance Test: Load multiple directives by codes.

    Given multiple directive codes
    When loading the directives
    Then all directive contents should be concatenated.
    """
    # Arrange
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(temp_directives_dir)

    # Act
    content = loader.load_directives(["001", "006"])

    # Assert
    assert "<!-- Directive 001 Begin -->" in content
    assert "# Directive 001: CLI Tooling" in content
    assert "<!-- Directive 006 Begin -->" in content
    assert "# Directive 006: Version Governance" in content


def test_load_nonexistent_directive(temp_directives_dir: Path, capsys) -> None:
    """
    Acceptance Test: Handle nonexistent directive gracefully.

    Given a nonexistent directive code
    When loading the directive
    Then a warning should be issued but execution continues.
    """
    # Arrange
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(temp_directives_dir)

    # Act
    content = loader.load_directives(["999"])
    captured = capsys.readouterr()

    # Assert
    # Should not raise exception, just skip the missing directive
    assert "[WARN]" in captured.err or content == ""


# ============================================================================
# Unit Tests
# ============================================================================


def test_directive_loader_initialization(temp_directives_dir: Path) -> None:
    """Test DirectiveLoader initializes with correct directory."""
    # Arrange & Act
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(temp_directives_dir)

    # Assert
    assert loader.directives_dir == temp_directives_dir
    assert loader.directives_dir.exists()


def test_find_directive_file(temp_directives_dir: Path) -> None:
    """Test finding a directive file by code."""
    # Arrange
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(temp_directives_dir)

    # Act
    file_path = loader._find_directive_file("001")

    # Assert
    assert file_path is not None
    assert file_path.name == "001_cli_shell_tooling.md"


def test_find_directive_file_not_found(temp_directives_dir: Path) -> None:
    """Test finding a nonexistent directive file."""
    # Arrange
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(temp_directives_dir)

    # Act
    file_path = loader._find_directive_file("999")

    # Assert
    assert file_path is None


def test_extract_directive_code_from_filename() -> None:
    """Test extracting directive code from filename."""
    # Arrange
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(Path("."))

    # Act & Assert
    assert loader._extract_code("001_cli_shell_tooling.md") == "001"
    assert loader._extract_code("014_worklog_creation.md") == "014"
    assert loader._extract_code("invalid_name.md") is None


def test_format_directive_output(temp_directives_dir: Path) -> None:
    """Test formatting directive content with markers."""
    # Arrange
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(temp_directives_dir)
    content = "# Test Content\n\nTest body."

    # Act
    formatted = loader._format_directive("001", content)

    # Assert
    assert formatted.startswith("\n<!-- Directive 001 Begin -->")
    assert "# Test Content" in formatted
    assert formatted.endswith("<!-- Directive 001 End -->\n")


def test_empty_directives_directory(tmp_path: Path) -> None:
    """Test behavior with empty directives directory."""
    # Arrange
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    from load_directives import DirectiveLoader

    loader = DirectiveLoader(empty_dir)

    # Act
    directives = loader.list_directives()

    # Assert
    assert len(directives) == 0, "Empty directory should return no directives"
