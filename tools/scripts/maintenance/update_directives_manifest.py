#!/usr/bin/env python3
"""
Directives Manifest Maintenance Script

Maintains the directives manifest.json file by scanning the directives directory
and ensuring all directive files are properly registered with correct metadata.

Usage:
    # Validate manifest (report only, exit non-zero if issues found)
    python -m ops.scripts.maintenance.update_directives_manifest

    # Validate with dry-run (explicit report only mode)
    python -m ops.scripts.maintenance.update_directives_manifest --dry-run

    # Auto-fix discrepancies
    python -m ops.scripts.maintenance.update_directives_manifest --fix

    # Specify custom directives directory
    python -m ops.scripts.maintenance.update_directives_manifest --directives-dir /path/to/directives

Features:
    - Scans .github/agents/directives/ for numbered directive files (NNN_slug.md)
    - Validates manifest entries against actual files
    - Detects missing directives (file exists, no manifest entry)
    - Detects orphaned entries (manifest entry, no file)
    - Validates metadata consistency (code, slug, filename match)
    - Provides --dry-run mode (report only)
    - Provides --fix mode (auto-update manifest)
    - Exits non-zero if discrepancies found (CI-ready)

Following:
    - Directive 016: ATDD - Acceptance tests defined first
    - Directive 017: TDD - Unit tests drive implementation
    - Directive 018: Traceable Decisions - Clear documentation
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class ValidationResult:
    """Result of manifest validation."""

    is_valid: bool
    missing_files: List[str] = field(default_factory=list)
    orphaned_entries: List[Dict[str, Any]] = field(default_factory=list)
    metadata_mismatches: List[Dict[str, Any]] = field(default_factory=list)

    def get_report(self) -> str:
        """Generate a human-readable validation report."""
        if self.is_valid:
            return "✅ Manifest is valid - all directives are properly registered."

        lines = ["❌ Manifest validation failed:\n"]

        if self.missing_files:
            lines.append(f"📄 Missing Manifest Entries ({len(self.missing_files)}):")
            for filename in self.missing_files:
                lines.append(f"  - {filename} (file exists but no manifest entry)")
            lines.append("")

        if self.orphaned_entries:
            lines.append(f"👻 Orphaned Manifest Entries ({len(self.orphaned_entries)}):")
            for entry in self.orphaned_entries:
                lines.append(
                    f"  - {entry['file']} (manifest entry exists but file not found)"
                )
            lines.append("")

        if self.metadata_mismatches:
            lines.append(
                f"⚠️  Metadata Inconsistencies ({len(self.metadata_mismatches)}):"
            )
            for mismatch in self.metadata_mismatches:
                lines.append(f"  - {mismatch['file']}:")
                for issue in mismatch["issues"]:
                    lines.append(f"    • {issue}")
            lines.append("")

        lines.append("💡 Resolution:")
        lines.append("  Run with --fix to automatically update the manifest")

        return "\n".join(lines)


# ============================================================================
# File Scanning
# ============================================================================


def extract_directive_code(filename: str) -> str:
    """
    Extract directive code number from filename.

    Args:
        filename: Directive filename (e.g., "001_cli_shell_tooling.md")

    Returns:
        Code number as string (e.g., "001")
    """
    match = re.match(r"^(\d{3})_", filename)
    if not match:
        raise ValueError(f"Invalid directive filename format: {filename}")
    return match.group(1)


def extract_directive_slug(filename: str) -> str:
    """
    Extract directive slug from filename.

    Args:
        filename: Directive filename (e.g., "001_cli_shell_tooling.md")

    Returns:
        Slug (e.g., "cli_shell_tooling")
    """
    match = re.match(r"^\d{3}_(.+)\.md$", filename)
    if not match:
        raise ValueError(f"Invalid directive filename format: {filename}")
    return match.group(1)


def scan_directive_files(directives_dir: Path) -> List[Dict[str, str]]:
    """
    Scan directives directory for numbered directive files.

    Args:
        directives_dir: Path to directives directory

    Returns:
        List of file information dictionaries

    Raises:
        FileNotFoundError: If directives directory doesn't exist
    """
    if not directives_dir.exists():
        raise FileNotFoundError(f"Directives directory not found: {directives_dir}")

    files = []
    pattern = re.compile(r"^\d{3}_.*\.md$")

    for file_path in sorted(directives_dir.glob("*.md")):
        if pattern.match(file_path.name):
            try:
                code = extract_directive_code(file_path.name)
                slug = extract_directive_slug(file_path.name)
                files.append(
                    {"code": code, "slug": slug, "filename": file_path.name}
                )
            except ValueError as e:
                print(f"⚠️  Warning: Skipping invalid file: {e}", file=sys.stderr)

    return files


# ============================================================================
# Manifest Operations
# ============================================================================


def load_manifest(manifest_path: Path) -> Dict[str, Any]:
    """
    Load and parse manifest file.

    Args:
        manifest_path: Path to manifest.json

    Returns:
        Parsed manifest data

    Raises:
        FileNotFoundError: If manifest doesn't exist
        json.JSONDecodeError: If manifest is invalid JSON
    """
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

    with open(manifest_path, "r") as f:
        return json.load(f)


def save_manifest(manifest_path: Path, manifest_data: Dict[str, Any]) -> None:
    """
    Save manifest to file with proper formatting.

    Args:
        manifest_path: Path to manifest.json
        manifest_data: Manifest data to save
    """
    # Update generated_at timestamp
    manifest_data["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=2)
        f.write("\n")  # Add trailing newline


# ============================================================================
# Validation Logic
# ============================================================================


def find_missing_entries(
    files: List[Dict[str, str]], manifest_entries: List[Dict[str, Any]]
) -> List[str]:
    """
    Find files that don't have manifest entries.

    Args:
        files: List of scanned file information
        manifest_entries: List of manifest directive entries

    Returns:
        List of filenames missing from manifest
    """
    manifest_files = {entry["file"] for entry in manifest_entries}
    missing = [f["filename"] for f in files if f["filename"] not in manifest_files]
    return missing


def find_orphaned_entries(
    files: List[Dict[str, str]], manifest_entries: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Find manifest entries for non-existent files.

    Args:
        files: List of scanned file information
        manifest_entries: List of manifest directive entries

    Returns:
        List of orphaned manifest entries
    """
    existing_files = {f["filename"] for f in files}
    orphaned = [
        entry for entry in manifest_entries if entry["file"] not in existing_files
    ]
    return orphaned


def validate_metadata_consistency(
    file_info: Dict[str, str], manifest_entry: Dict[str, Any]
) -> List[str]:
    """
    Validate that manifest metadata matches file information.

    Args:
        file_info: File information from scan
        manifest_entry: Corresponding manifest entry

    Returns:
        List of inconsistency messages (empty if consistent)
    """
    issues = []

    # Check code match
    if file_info["code"] != manifest_entry["code"]:
        issues.append(
            f"Code mismatch: filename has '{file_info['code']}', "
            f"manifest has '{manifest_entry['code']}'"
        )

    # Check slug match
    if file_info["slug"] != manifest_entry["slug"]:
        issues.append(
            f"Slug mismatch: filename has '{file_info['slug']}', "
            f"manifest has '{manifest_entry['slug']}'"
        )

    # Check filename match
    if file_info["filename"] != manifest_entry["file"]:
        issues.append(
            f"Filename mismatch: actual is '{file_info['filename']}', "
            f"manifest has '{manifest_entry['file']}'"
        )

    return issues


# ============================================================================
# Manifest Updating
# ============================================================================


def create_manifest_entry(file_info: Dict[str, str]) -> Dict[str, Any]:
    """
    Create a manifest entry from file information.

    Args:
        file_info: File information from scan

    Returns:
        Manifest entry dictionary with default values
    """
    # Convert slug to title (snake_case to Title Case)
    title = " ".join(word.capitalize() for word in file_info["slug"].split("_"))

    return {
        "code": file_info["code"],
        "slug": file_info["slug"],
        "title": title,
        "file": file_info["filename"],
        "purpose": f"TODO: Add purpose for {file_info['code']}",
        "dependencies": [],
        "requiredInAgents": False,
        "safetyCritical": False,
        "directive_version": "1.0.0",
        "status": "active",
    }


def update_manifest(
    manifest: Dict[str, Any], new_entries: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Add new entries to manifest.

    Args:
        manifest: Existing manifest data
        new_entries: New entries to add

    Returns:
        Updated manifest data
    """
    # Add new entries
    manifest["directives"].extend(new_entries)

    # Sort by code
    manifest["directives"].sort(key=lambda d: d["code"])

    return manifest


def remove_orphaned_entries(
    manifest: Dict[str, Any], orphaned_codes: List[str]
) -> Dict[str, Any]:
    """
    Remove orphaned entries from manifest.

    Args:
        manifest: Existing manifest data
        orphaned_codes: List of codes to remove

    Returns:
        Updated manifest data
    """
    manifest["directives"] = [
        d for d in manifest["directives"] if d["code"] not in orphaned_codes
    ]
    return manifest


# ============================================================================
# Main Validator Class
# ============================================================================


class DirectivesManifestValidator:
    """Main validator for directives manifest."""

    def __init__(self, directives_dir: Path):
        """
        Initialize validator.

        Args:
            directives_dir: Path to directives directory
        """
        self.directives_dir = Path(directives_dir)
        self.manifest_path = self.directives_dir / "manifest.json"

    def validate(self) -> ValidationResult:
        """
        Validate manifest against directive files.

        Returns:
            ValidationResult with details of any discrepancies
        """
        # Scan directive files
        files = scan_directive_files(self.directives_dir)

        # Load manifest
        try:
            manifest = load_manifest(self.manifest_path)
        except FileNotFoundError:
            return ValidationResult(
                is_valid=False,
                missing_files=[f["filename"] for f in files],
                orphaned_entries=[],
                metadata_mismatches=[],
            )

        manifest_entries = manifest.get("directives", [])

        # Find missing entries
        missing_files = find_missing_entries(files, manifest_entries)

        # Find orphaned entries
        orphaned_entries = find_orphaned_entries(files, manifest_entries)

        # Validate metadata consistency
        metadata_mismatches = []
        file_map = {f["filename"]: f for f in files}

        for entry in manifest_entries:
            if entry["file"] in file_map:
                file_info = file_map[entry["file"]]
                issues = validate_metadata_consistency(file_info, entry)
                if issues:
                    metadata_mismatches.append({"file": entry["file"], "issues": issues})

        # Determine if valid
        is_valid = (
            len(missing_files) == 0
            and len(orphaned_entries) == 0
            and len(metadata_mismatches) == 0
        )

        return ValidationResult(
            is_valid=is_valid,
            missing_files=missing_files,
            orphaned_entries=orphaned_entries,
            metadata_mismatches=metadata_mismatches,
        )

    def fix(self) -> ValidationResult:
        """
        Fix manifest discrepancies automatically.

        Returns:
            ValidationResult after fixes applied
        """
        # Scan directive files
        files = scan_directive_files(self.directives_dir)

        # Load or create manifest
        try:
            manifest = load_manifest(self.manifest_path)
        except FileNotFoundError:
            manifest = {
                "version": "1.0.0",
                "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "description": "Manifest of externalized agent directives for agent-augmented development",
                "directives": [],
            }

        manifest_entries = manifest.get("directives", [])

        # Find and add missing entries
        missing_files = find_missing_entries(files, manifest_entries)
        if missing_files:
            print(f"📝 Adding {len(missing_files)} missing entries...")
            file_map = {f["filename"]: f for f in files}
            new_entries = [
                create_manifest_entry(file_map[filename]) for filename in missing_files
            ]
            manifest = update_manifest(manifest, new_entries)

        # Remove orphaned entries
        orphaned_entries = find_orphaned_entries(files, manifest_entries)
        if orphaned_entries:
            print(f"🗑️  Removing {len(orphaned_entries)} orphaned entries...")
            orphaned_codes = [entry["code"] for entry in orphaned_entries]
            manifest = remove_orphaned_entries(manifest, orphaned_codes)

        # Save updated manifest
        save_manifest(self.manifest_path, manifest)
        print(f"✅ Manifest updated: {self.manifest_path}")

        # Validate again
        return self.validate()


# ============================================================================
# CLI Interface
# ============================================================================


def parse_args(args: List[str] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: Arguments to parse (defaults to sys.argv)

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Maintain directives manifest.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate manifest (report only)
  %(prog)s

  # Validate with explicit dry-run mode
  %(prog)s --dry-run

  # Auto-fix discrepancies
  %(prog)s --fix

  # Use custom directives directory
  %(prog)s --directives-dir /path/to/directives
        """,
    )

    parser.add_argument(
        "--directives-dir",
        type=Path,
        default=Path(".github/agents/directives"),
        help="Path to directives directory (default: .github/agents/directives)",
    )

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Report discrepancies without making changes",
    )
    mode_group.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix discrepancies",
    )

    return parser.parse_args(args)


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success, 1 for validation failures)
    """
    args = parse_args()

    validator = DirectivesManifestValidator(args.directives_dir)

    if args.fix:
        print("🔧 Fixing manifest discrepancies...")
        result = validator.fix()
    else:
        print("🔍 Validating manifest...")
        result = validator.validate()

    # Print report
    print()
    print(result.get_report())

    # Return exit code
    return 0 if result.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
