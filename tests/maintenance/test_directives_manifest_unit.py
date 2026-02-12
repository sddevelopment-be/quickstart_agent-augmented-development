"""
Unit tests for directives manifest maintenance script.

Following Directive 017 (TDD): These tests drive the implementation
of individual components and functions.
"""

import json
from pathlib import Path

import pytest


class TestDirectiveFileScanning:
    """Unit tests for directive file scanning functionality."""

    def test_scan_finds_all_numbered_directives(self, tmp_path):
        """Should find all files matching pattern NNN_slug.md."""
        directives_dir = tmp_path / "directives"
        directives_dir.mkdir()

        # Create directive files
        (directives_dir / "001_first.md").write_text("content")
        (directives_dir / "002_second.md").write_text("content")
        (directives_dir / "010_tenth.md").write_text("content")

        # Create files that should be ignored
        (directives_dir / "manifest.json").write_text("{}")
        (directives_dir / "README.md").write_text("readme")
        (directives_dir / "temp.txt").write_text("temp")

        from tools.scripts.maintenance.update_directives_manifest import (
            scan_directive_files,
        )

        files = scan_directive_files(directives_dir)

        assert len(files) == 3
        assert {f["code"] for f in files} == {"001", "002", "010"}

    def test_extract_code_from_filename(self):
        """Should extract code number from filename."""
        from tools.scripts.maintenance.update_directives_manifest import (
            extract_directive_code,
        )

        assert extract_directive_code("001_cli_shell_tooling.md") == "001"
        assert extract_directive_code("010_mode_protocol.md") == "010"
        assert extract_directive_code("025_framework_guardian.md") == "025"

    def test_extract_slug_from_filename(self):
        """Should extract slug from filename."""
        from tools.scripts.maintenance.update_directives_manifest import (
            extract_directive_slug,
        )

        assert extract_directive_slug("001_cli_shell_tooling.md") == "cli_shell_tooling"
        assert extract_directive_slug("010_mode_protocol.md") == "mode_protocol"
        assert (
            extract_directive_slug("025_framework_guardian.md") == "framework_guardian"
        )

    def test_handles_missing_directory(self):
        """Should handle non-existent directives directory gracefully."""
        from tools.scripts.maintenance.update_directives_manifest import (
            scan_directive_files,
        )

        with pytest.raises(FileNotFoundError):
            scan_directive_files(Path("/nonexistent/directory"))


class TestManifestParsing:
    """Unit tests for manifest parsing functionality."""

    def test_load_valid_manifest(self, tmp_path):
        """Should load and parse a valid manifest file."""
        manifest_data = {
            "version": "1.0.0",
            "generated_at": "2025-11-28T12:45:00Z",
            "description": "Test",
            "directives": [
                {
                    "code": "001",
                    "slug": "test",
                    "title": "Test",
                    "file": "001_test.md",
                    "purpose": "Test",
                    "dependencies": [],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                }
            ],
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        from tools.scripts.maintenance.update_directives_manifest import load_manifest

        manifest = load_manifest(manifest_file)

        assert manifest["version"] == "1.0.0"
        assert len(manifest["directives"]) == 1

    def test_handles_missing_manifest(self, tmp_path):
        """Should handle missing manifest file gracefully."""
        from tools.scripts.maintenance.update_directives_manifest import load_manifest

        with pytest.raises(FileNotFoundError):
            load_manifest(tmp_path / "nonexistent.json")

    def test_handles_invalid_json(self, tmp_path):
        """Should handle invalid JSON gracefully."""
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text("{invalid json")

        from tools.scripts.maintenance.update_directives_manifest import load_manifest

        with pytest.raises(json.JSONDecodeError):
            load_manifest(manifest_file)


class TestValidationLogic:
    """Unit tests for validation logic."""

    def test_detect_missing_manifest_entry(self):
        """Should detect when a file exists but has no manifest entry."""
        from tools.scripts.maintenance.update_directives_manifest import (
            find_missing_entries,
        )

        files = [
            {"code": "001", "slug": "first", "filename": "001_first.md"},
            {"code": "002", "slug": "second", "filename": "002_second.md"},
        ]

        manifest_entries = [
            {"code": "001", "file": "001_first.md"},
        ]

        missing = find_missing_entries(files, manifest_entries)

        assert len(missing) == 1
        assert missing[0] == "002_second.md"

    def test_detect_orphaned_manifest_entry(self):
        """Should detect when manifest entry exists but file doesn't."""
        from tools.scripts.maintenance.update_directives_manifest import (
            find_orphaned_entries,
        )

        files = [
            {"code": "001", "slug": "first", "filename": "001_first.md"},
        ]

        manifest_entries = [
            {"code": "001", "file": "001_first.md"},
            {"code": "002", "file": "002_second.md"},
        ]

        orphaned = find_orphaned_entries(files, manifest_entries)

        assert len(orphaned) == 1
        assert orphaned[0]["code"] == "002"

    def test_detect_code_mismatch(self):
        """Should detect when code in filename doesn't match manifest."""
        from tools.scripts.maintenance.update_directives_manifest import (
            validate_metadata_consistency,
        )

        file_info = {"code": "001", "slug": "first", "filename": "001_first.md"}
        manifest_entry = {"code": "002", "slug": "first", "file": "001_first.md"}

        mismatches = validate_metadata_consistency(file_info, manifest_entry)

        assert len(mismatches) > 0
        assert any("code" in m.lower() for m in mismatches)

    def test_detect_slug_mismatch(self):
        """Should detect when slug in filename doesn't match manifest."""
        from tools.scripts.maintenance.update_directives_manifest import (
            validate_metadata_consistency,
        )

        file_info = {"code": "001", "slug": "first", "filename": "001_first.md"}
        manifest_entry = {"code": "001", "slug": "second", "file": "001_first.md"}

        mismatches = validate_metadata_consistency(file_info, manifest_entry)

        assert len(mismatches) > 0
        assert any("slug" in m.lower() for m in mismatches)

    def test_valid_metadata_returns_no_mismatches(self):
        """Should return empty list when metadata is consistent."""
        from tools.scripts.maintenance.update_directives_manifest import (
            validate_metadata_consistency,
        )

        file_info = {"code": "001", "slug": "first", "filename": "001_first.md"}
        manifest_entry = {"code": "001", "slug": "first", "file": "001_first.md"}

        mismatches = validate_metadata_consistency(file_info, manifest_entry)

        assert len(mismatches) == 0


class TestManifestUpdating:
    """Unit tests for manifest update functionality."""

    def test_create_manifest_entry_from_file(self):
        """Should create a properly formatted manifest entry from file info."""
        from tools.scripts.maintenance.update_directives_manifest import (
            create_manifest_entry,
        )

        file_info = {
            "code": "001",
            "slug": "test_directive",
            "filename": "001_test_directive.md",
        }

        entry = create_manifest_entry(file_info)

        assert entry["code"] == "001"
        assert entry["slug"] == "test_directive"
        assert entry["file"] == "001_test_directive.md"
        assert "title" in entry
        assert "purpose" in entry
        assert "dependencies" in entry

    def test_update_manifest_preserves_structure(self, tmp_path):
        """Should preserve manifest structure when updating."""
        from tools.scripts.maintenance.update_directives_manifest import (
            update_manifest,
        )

        original_manifest = {
            "version": "1.0.0",
            "generated_at": "2025-11-28T12:45:00Z",
            "description": "Test manifest",
            "directives": [
                {
                    "code": "001",
                    "slug": "first",
                    "title": "First",
                    "file": "001_first.md",
                    "purpose": "Purpose",
                    "dependencies": [],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                }
            ],
        }

        new_entry = {
            "code": "002",
            "slug": "second",
            "title": "Second",
            "file": "002_second.md",
            "purpose": "Purpose",
            "dependencies": [],
            "requiredInAgents": False,
            "safetyCritical": True,
            "directive_version": "1.0.0",
            "status": "active",
        }

        updated = update_manifest(original_manifest, [new_entry])

        assert updated["version"] == "1.0.0"
        assert updated["description"] == "Test manifest"
        assert len(updated["directives"]) == 2
        assert any(d["code"] == "002" for d in updated["directives"])

    def test_remove_orphaned_entries(self):
        """Should remove entries for non-existent files."""
        from tools.scripts.maintenance.update_directives_manifest import (
            remove_orphaned_entries,
        )

        manifest = {
            "directives": [
                {"code": "001", "file": "001_first.md"},
                {"code": "002", "file": "002_second.md"},
                {"code": "003", "file": "003_third.md"},
            ]
        }

        orphaned_codes = ["002"]

        updated = remove_orphaned_entries(manifest, orphaned_codes)

        assert len(updated["directives"]) == 2
        assert not any(d["code"] == "002" for d in updated["directives"])


class TestReportGeneration:
    """Unit tests for report generation."""

    def test_generate_report_with_issues(self):
        """Should generate a comprehensive report of all issues."""
        from tools.scripts.maintenance.update_directives_manifest import (
            ValidationResult,
        )

        result = ValidationResult(
            is_valid=False,
            missing_files=["002_missing.md"],
            orphaned_entries=[{"code": "003", "file": "003_orphaned.md"}],
            metadata_mismatches=[
                {"file": "004_mismatch.md", "issues": ["Code mismatch"]}
            ],
        )

        report = result.get_report()

        assert "002_missing.md" in report
        assert "003_orphaned.md" in report
        assert "004_mismatch.md" in report
        assert "Code mismatch" in report

    def test_generate_report_no_issues(self):
        """Should generate a success report when no issues found."""
        from tools.scripts.maintenance.update_directives_manifest import (
            ValidationResult,
        )

        result = ValidationResult(
            is_valid=True,
            missing_files=[],
            orphaned_entries=[],
            metadata_mismatches=[],
        )

        report = result.get_report()

        assert "valid" in report.lower() or "success" in report.lower()


class TestCLIInterface:
    """Unit tests for CLI argument parsing and execution."""

    def test_parse_dry_run_argument(self):
        """Should parse --dry-run flag correctly."""
        from tools.scripts.maintenance.update_directives_manifest import parse_args

        args = parse_args(["--dry-run"])

        assert args.dry_run is True
        assert args.fix is False

    def test_parse_fix_argument(self):
        """Should parse --fix flag correctly."""
        from tools.scripts.maintenance.update_directives_manifest import parse_args

        args = parse_args(["--fix"])

        assert args.fix is True
        assert args.dry_run is False

    def test_parse_directives_dir_argument(self):
        """Should parse --directives-dir argument correctly."""
        from tools.scripts.maintenance.update_directives_manifest import parse_args

        args = parse_args(["--directives-dir", "/custom/path"])

        assert str(args.directives_dir) == "/custom/path"

    def test_default_directives_dir(self):
        """Should use default directives directory when not specified."""
        from tools.scripts.maintenance.update_directives_manifest import parse_args

        args = parse_args([])

        assert ".github/agents/directives" in str(args.directives_dir)
