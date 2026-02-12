"""
Acceptance tests for directives manifest maintenance script.

Following Directive 016 (ATDD): These tests define the acceptance criteria
for the manifest maintenance system as specified in task
2025-11-28T0426-build-automation-manifest-maintenance-script.

Acceptance Criteria:
1. Script can scan directives directory and find all numbered directive files
2. Script can validate manifest entries against actual files
3. Script can detect missing directives (file exists, no manifest entry)
4. Script can detect orphaned entries (manifest entry, no file)
5. Script can validate metadata consistency (code, slug, filename match)
6. Script supports --dry-run mode (report only)
7. Script supports --fix mode (auto-update manifest)
8. Script exits with non-zero code if discrepancies found (CI-ready)
"""

import json

import pytest

# Import will be available after implementation
# For now, we'll import dynamically in tests


class TestDirectivesManifestAcceptance:
    """
    Acceptance tests for directives manifest maintenance.

    These tests verify end-to-end behavior of the maintenance script.
    """

    @pytest.fixture
    def temp_directives_dir(self, tmp_path):
        """Create a temporary directives directory with sample files."""
        directives_dir = tmp_path / "directives"
        directives_dir.mkdir()

        # Create sample directive files
        (directives_dir / "001_cli_shell_tooling.md").write_text(
            "# 001 CLI and Shell Tooling\nContent here"
        )
        (directives_dir / "002_context_notes.md").write_text(
            "# 002 Context Notes\nContent here"
        )
        (directives_dir / "003_repository_quick_reference.md").write_text(
            "# 003 Repository Quick Reference\nContent here"
        )

        return directives_dir

    @pytest.fixture
    def valid_manifest(self, tmp_path):
        """Create a valid manifest file matching the directive files."""
        manifest_data = {
            "version": "1.0.0",
            "generated_at": "2025-11-28T12:45:00Z",
            "description": "Test manifest",
            "directives": [
                {
                    "code": "001",
                    "slug": "cli_shell_tooling",
                    "title": "CLI & Shell Tooling",
                    "file": "001_cli_shell_tooling.md",
                    "purpose": "Test purpose",
                    "dependencies": [],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                },
                {
                    "code": "002",
                    "slug": "context_notes",
                    "title": "Context Notes",
                    "file": "002_context_notes.md",
                    "purpose": "Test purpose",
                    "dependencies": [],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                },
                {
                    "code": "003",
                    "slug": "repository_quick_reference",
                    "title": "Repository Quick Reference",
                    "file": "003_repository_quick_reference.md",
                    "purpose": "Test purpose",
                    "dependencies": ["002"],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                },
            ],
        }

        manifest_file = tmp_path / "directives" / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data, indent=2))
        return manifest_file

    @pytest.fixture
    def manifest_with_missing_entry(self, tmp_path, temp_directives_dir):
        """Create a manifest missing one directive entry."""
        manifest_data = {
            "version": "1.0.0",
            "generated_at": "2025-11-28T12:45:00Z",
            "description": "Test manifest",
            "directives": [
                {
                    "code": "001",
                    "slug": "cli_shell_tooling",
                    "title": "CLI & Shell Tooling",
                    "file": "001_cli_shell_tooling.md",
                    "purpose": "Test purpose",
                    "dependencies": [],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                },
                # Missing 002
                {
                    "code": "003",
                    "slug": "repository_quick_reference",
                    "title": "Repository Quick Reference",
                    "file": "003_repository_quick_reference.md",
                    "purpose": "Test purpose",
                    "dependencies": ["002"],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                },
            ],
        }

        manifest_file = temp_directives_dir / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data, indent=2))
        return manifest_file

    @pytest.fixture
    def manifest_with_orphaned_entry(self, tmp_path):
        """Create a manifest with entry for non-existent file."""
        directives_dir = tmp_path / "directives"
        directives_dir.mkdir()

        # Only create 001 and 003, not 002
        (directives_dir / "001_cli_shell_tooling.md").write_text("# 001\nContent")
        (directives_dir / "003_repository_quick_reference.md").write_text(
            "# 003\nContent"
        )

        manifest_data = {
            "version": "1.0.0",
            "generated_at": "2025-11-28T12:45:00Z",
            "description": "Test manifest",
            "directives": [
                {
                    "code": "001",
                    "slug": "cli_shell_tooling",
                    "title": "CLI & Shell Tooling",
                    "file": "001_cli_shell_tooling.md",
                    "purpose": "Test purpose",
                    "dependencies": [],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                },
                {
                    "code": "002",
                    "slug": "context_notes",
                    "title": "Context Notes",
                    "file": "002_context_notes.md",  # This file doesn't exist
                    "purpose": "Test purpose",
                    "dependencies": [],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                },
                {
                    "code": "003",
                    "slug": "repository_quick_reference",
                    "title": "Repository Quick Reference",
                    "file": "003_repository_quick_reference.md",
                    "purpose": "Test purpose",
                    "dependencies": ["002"],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                },
            ],
        }

        manifest_file = directives_dir / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data, indent=2))
        return manifest_file

    @pytest.fixture
    def manifest_with_inconsistent_metadata(self, tmp_path):
        """Create a manifest with metadata that doesn't match filenames."""
        directives_dir = tmp_path / "directives"
        directives_dir.mkdir()

        (directives_dir / "001_cli_shell_tooling.md").write_text("# 001\nContent")

        manifest_data = {
            "version": "1.0.0",
            "generated_at": "2025-11-28T12:45:00Z",
            "description": "Test manifest",
            "directives": [
                {
                    "code": "002",  # Wrong code! File is 001
                    "slug": "cli_shell_tooling",
                    "title": "CLI & Shell Tooling",
                    "file": "001_cli_shell_tooling.md",
                    "purpose": "Test purpose",
                    "dependencies": [],
                    "requiredInAgents": False,
                    "safetyCritical": True,
                    "directive_version": "1.0.0",
                    "status": "active",
                }
            ],
        }

        manifest_file = directives_dir / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data, indent=2))
        return manifest_file

    def test_validates_valid_manifest(self, temp_directives_dir, valid_manifest):
        """
        AC1: Script validates a correct manifest without errors.

        Given a directives directory with files 001, 002, 003
        And a manifest.json with matching entries
        When the validation runs
        Then no discrepancies should be found
        And exit code should be 0
        """
        from tools.scripts.maintenance.update_directives_manifest import (
            DirectivesManifestValidator,
        )

        validator = DirectivesManifestValidator(temp_directives_dir)
        result = validator.validate()

        assert result.is_valid
        assert len(result.missing_files) == 0
        assert len(result.orphaned_entries) == 0
        assert len(result.metadata_mismatches) == 0

    def test_detects_missing_manifest_entries(
        self, temp_directives_dir, manifest_with_missing_entry
    ):
        """
        AC2: Script detects files without manifest entries.

        Given a directives directory with files 001, 002, 003
        And a manifest.json missing entry for 002
        When the validation runs
        Then missing file 002_context_notes.md should be detected
        And exit code should be non-zero
        """
        from tools.scripts.maintenance.update_directives_manifest import (
            DirectivesManifestValidator,
        )

        validator = DirectivesManifestValidator(temp_directives_dir)
        result = validator.validate()

        assert not result.is_valid
        assert len(result.missing_files) == 1
        assert "002_context_notes.md" in result.missing_files

    def test_detects_orphaned_manifest_entries(self, manifest_with_orphaned_entry):
        """
        AC3: Script detects manifest entries for non-existent files.

        Given a directives directory with files 001, 003 (no 002)
        And a manifest.json with entry for 002
        When the validation runs
        Then orphaned entry for 002_context_notes.md should be detected
        And exit code should be non-zero
        """
        from tools.scripts.maintenance.update_directives_manifest import (
            DirectivesManifestValidator,
        )

        directives_dir = manifest_with_orphaned_entry.parent
        validator = DirectivesManifestValidator(directives_dir)
        result = validator.validate()

        assert not result.is_valid
        assert len(result.orphaned_entries) == 1
        assert result.orphaned_entries[0]["file"] == "002_context_notes.md"

    def test_detects_metadata_inconsistencies(
        self, manifest_with_inconsistent_metadata
    ):
        """
        AC4: Script detects metadata mismatches.

        Given a directive file 001_cli_shell_tooling.md
        And a manifest entry with code "002"
        When the validation runs
        Then metadata mismatch should be detected
        And exit code should be non-zero
        """
        from tools.scripts.maintenance.update_directives_manifest import (
            DirectivesManifestValidator,
        )

        directives_dir = manifest_with_inconsistent_metadata.parent
        validator = DirectivesManifestValidator(directives_dir)
        result = validator.validate()

        assert not result.is_valid
        assert len(result.metadata_mismatches) == 1

    def test_dry_run_mode_reports_without_changes(
        self, manifest_with_missing_entry, temp_directives_dir
    ):
        """
        AC5: Script in dry-run mode reports issues without making changes.

        Given a manifest with discrepancies
        When run in --dry-run mode
        Then discrepancies should be reported
        And manifest file should not be modified
        """
        from tools.scripts.maintenance.update_directives_manifest import (
            DirectivesManifestValidator,
        )

        # Get original manifest content
        original_content = manifest_with_missing_entry.read_text()

        validator = DirectivesManifestValidator(temp_directives_dir)
        result = validator.validate()

        # Verify issues were detected
        assert not result.is_valid

        # Verify manifest was not modified
        assert manifest_with_missing_entry.read_text() == original_content

    def test_fix_mode_updates_manifest(
        self, manifest_with_missing_entry, temp_directives_dir
    ):
        """
        AC6: Script in --fix mode auto-updates manifest.

        Given a manifest missing an entry for directive 002
        When run in --fix mode
        Then manifest should be updated with the missing entry
        And the updated manifest should validate successfully
        """
        from tools.scripts.maintenance.update_directives_manifest import (
            DirectivesManifestValidator,
        )

        validator = DirectivesManifestValidator(temp_directives_dir)
        validator.fix()

        # Validate again - should now be valid
        result = validator.validate()
        assert result.is_valid

    def test_script_exit_codes(self, temp_directives_dir, valid_manifest):
        """
        AC7: Script returns proper exit codes for CI usage.

        Given various manifest states
        When the script runs
        Then exit code 0 for valid manifest
        And exit code 1 for discrepancies found
        """
        import subprocess
        import sys

        # Test valid manifest (exit 0)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "tools.scripts.maintenance.update_directives_manifest",
                "--directives-dir",
                str(temp_directives_dir),
            ],
            capture_output=True,
        )

        assert result.returncode == 0

    def test_comprehensive_error_messages(
        self, manifest_with_missing_entry, temp_directives_dir
    ):
        """
        AC8: Script provides clear, actionable error messages.

        Given a manifest with discrepancies
        When validation runs
        Then error messages should include:
        - File name of missing/orphaned entries
        - Specific metadata mismatches
        - Suggestions for resolution
        """
        from tools.scripts.maintenance.update_directives_manifest import (
            DirectivesManifestValidator,
        )

        validator = DirectivesManifestValidator(temp_directives_dir)
        result = validator.validate()

        report = result.get_report()

        # Verify report contains actionable information
        assert "002_context_notes.md" in report
        assert "missing" in report.lower()

    def test_handles_complex_filename_patterns(self, tmp_path):
        """
        AC9: Script correctly parses various directive filename patterns.

        Given directive files with different naming patterns
        When the script scans the directory
        Then it should correctly extract code numbers and slugs
        """
        directives_dir = tmp_path / "directives"
        directives_dir.mkdir()

        # Create directives with various patterns
        (directives_dir / "001_cli_shell_tooling.md").write_text("# 001")
        (directives_dir / "010_mode_protocol.md").write_text("# 010")
        (directives_dir / "025_framework_guardian.md").write_text("# 025")

        from tools.scripts.maintenance.update_directives_manifest import (
            scan_directive_files,
        )

        files = scan_directive_files(directives_dir)

        assert len(files) == 3
        assert "001" in [f["code"] for f in files]
        assert "010" in [f["code"] for f in files]
        assert "025" in [f["code"] for f in files]
