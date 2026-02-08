#!/usr/bin/env python3
"""
Release Artifact Builder for Quickstart Agent-Augmented Development Framework

This script builds the release artifact as specified in ADR-013 and ADR-014.
It creates a zip package containing framework_core/, scripts/, and META/
directories with proper checksums, manifests, and Guardian metadata.

Usage:
    python build_release_artifact.py --version 1.0.0 [--output-dir ./output] [--dry-run]
    python build_release_artifact.py --version 1.0.0 --profile minimal
    python build_release_artifact.py --version 1.0.0 --config ops/release/distribution-config.yaml

Reference:
    - ADR-013: Zip-Based Framework Distribution
    - ADR-014: Framework Guardian Agent
    - docs/architecture/design/distribution_of_releases_technical_design.md
    - ops/release/distribution-config.yaml: Distribution configuration
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


# Default configuration (used if config file not found)
# Configuration: Directories to include in framework_core/
CORE_DIRECTORIES = [
    ".github/agents",
    "docs/templates",
    "docs/styleguides",
    "docs/architecture/patterns",
    "validation",
    "work/templates",
    "framework",
]

# Export directories (agent definitions for various platforms)
EXPORT_DIRECTORIES = [
    ".claude",
    ".opencode",
]

# Configuration: Files to include in root of framework_core/
CORE_ROOT_FILES = [
    "README.md",
    "AGENTS.md",
    "pyproject.toml",
    "requirements.txt",
]

# Configuration: Scripts to include
SCRIPTS_TO_INCLUDE = [
    "ops/release/framework_install.sh",
    "ops/release/framework_upgrade.sh",
]

# Configuration: Exclusion patterns
EXCLUDE_PATTERNS = [
    # Version control
    ".git",
    ".gitignore",
    # Python cache
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".coverage",
    ".mutmut-cache",
    # Work outputs
    "work/logs",
    "work/reports",
    "work/collaboration",
    "work/notes",
    "work/analysis",
    "work/articles",
    "work/planning",
    # Local overrides
    "local",
    # Temporary files
    "tmp",
    "output",
    # IDE
    ".vscode",
    ".idea",
    # Node modules (if any)
    "node_modules",
    # Build artifacts
    "dist",
    "build",
    "*.egg-info",
]


class ReleaseArtifactBuilder:
    """Build release artifacts for the framework."""

    def __init__(
        self,
        version: str,
        output_dir: Path,
        repo_root: Path,
        dry_run: bool = False,
        config_file: Optional[Path] = None,
        profile: str = "full",
    ):
        """
        Initialize the builder.

        Args:
            version: Version string (e.g., "1.0.0")
            output_dir: Directory where artifacts will be created
            repo_root: Root of the repository
            dry_run: If True, validate but don't create artifacts
            config_file: Path to distribution configuration YAML file
            profile: Distribution profile to use (full, minimal, etc.)
        """
        self.version = version
        self.output_dir = Path(output_dir)
        self.repo_root = Path(repo_root)
        self.dry_run = dry_run
        self.build_dir = self.output_dir / f"quickstart-framework-{version}"
        self.profile = profile
        self.stats = {
            "files_copied": 0,
            "files_skipped": 0,
            "total_size": 0,
        }
        
        # Load distribution configuration
        self.config = self._load_config(config_file)
        
        # Apply profile to get actual directories/files to include
        self.core_dirs = self._get_core_directories()
        self.export_dirs = self._get_export_directories()
        self.root_files = self._get_root_files()
        self.scripts = self._get_scripts()
        self.exclusions = self._get_exclusions()

    def _load_config(self, config_file: Optional[Path]) -> Dict:
        """Load distribution configuration from YAML file."""
        # Default config file location
        if config_file is None:
            config_file = self.repo_root / "ops/release/distribution-config.yaml"
        
        if config_file.exists():
            print(f"📋 Loading distribution config from {config_file}")
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
                print(f"   Config version: {config.get('version', 'unknown')}")
                return config
        else:
            print(f"⚠️  Config file not found: {config_file}")
            print("   Using default configuration")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration if config file doesn't exist."""
        return {
            "core_directories": [{"path": d, "required": True} for d in CORE_DIRECTORIES],
            "export_directories": [{"path": d, "required": False} for d in EXPORT_DIRECTORIES],
            "root_files": [{"path": f, "required": True} for f in CORE_ROOT_FILES],
            "scripts": [{"path": s, "required": True} for s in SCRIPTS_TO_INCLUDE],
            "exclusions": EXCLUDE_PATTERNS,
            "default_profile": "full",
        }
    
    def _get_core_directories(self) -> List[str]:
        """Get list of core directories to include based on profile."""
        if self.profile == "full":
            return [d["path"] for d in self.config.get("core_directories", [])]
        elif self.profile in self.config.get("profiles", {}):
            profile_config = self.config["profiles"][self.profile]
            include = profile_config.get("include", {}).get("core_directories", [])
            if include == "all":
                return [d["path"] for d in self.config.get("core_directories", [])]
            return include
        return [d["path"] for d in self.config.get("core_directories", []) if d.get("required", True)]
    
    def _get_export_directories(self) -> List[str]:
        """Get list of export directories to include based on profile."""
        if self.profile == "full":
            return [d["path"] for d in self.config.get("export_directories", [])]
        elif self.profile in self.config.get("profiles", {}):
            profile_config = self.config["profiles"][self.profile]
            include = profile_config.get("include", {}).get("export_directories", [])
            if include == "all":
                return [d["path"] for d in self.config.get("export_directories", [])]
            return include
        return []
    
    def _get_root_files(self) -> List[str]:
        """Get list of root files to include based on profile."""
        if self.profile == "full":
            return [f["path"] for f in self.config.get("root_files", [])]
        elif self.profile in self.config.get("profiles", {}):
            profile_config = self.config["profiles"][self.profile]
            include = profile_config.get("include", {}).get("root_files", [])
            if include == "all":
                return [f["path"] for f in self.config.get("root_files", [])]
            return include
        return [f["path"] for f in self.config.get("root_files", []) if f.get("required", True)]
    
    def _get_scripts(self) -> List[str]:
        """Get list of scripts to include based on profile."""
        if self.profile == "full":
            return [s["path"] for s in self.config.get("scripts", [])]
        elif self.profile in self.config.get("profiles", {}):
            profile_config = self.config["profiles"][self.profile]
            include = profile_config.get("include", {}).get("scripts", [])
            if include == "all":
                return [s["path"] for s in self.config.get("scripts", [])]
            return include
        return [s["path"] for s in self.config.get("scripts", []) if s.get("required", True)]
    
    def _get_exclusions(self) -> List[str]:
        """Get flattened list of exclusion patterns."""
        exclusions_dict = self.config.get("exclusions", {})
        if isinstance(exclusions_dict, dict):
            # Flatten nested exclusions
            exclusions = []
            for category, patterns in exclusions_dict.items():
                if isinstance(patterns, list):
                    exclusions.extend(patterns)
            return exclusions
        elif isinstance(exclusions_dict, list):
            return exclusions_dict
        return EXCLUDE_PATTERNS

    def validate_version(self) -> bool:
        """
        Validate version string follows semantic versioning.

        Returns:
            True if valid, False otherwise
        """
        # Semantic versioning pattern: major.minor.patch[-prerelease][+build]
        # Allow hyphens in prerelease identifiers for test versions like "integration-test"
        pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.+-]+)?$"
        if not re.match(pattern, self.version):
            print(f"❌ Invalid version format: {self.version}")
            print("   Expected: X.Y.Z[-prerelease][+build] (e.g., 1.0.0, 1.0.0-rc.1)")
            return False
        return True

    def validate_repository(self) -> bool:
        """
        Validate that we're in a valid repository structure.

        Returns:
            True if valid, False otherwise
        """
        # Check for key directories
        required_dirs = [".github/agents", "validation", "framework"]
        missing_dirs = []

        for dir_path in required_dirs:
            full_path = self.repo_root / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)

        if missing_dirs:
            print(f"❌ Invalid repository structure. Missing directories:")
            for dir_path in missing_dirs:
                print(f"   - {dir_path}")
            return False

        return True

    def should_exclude(self, path: Path) -> bool:
        """
        Check if a path should be excluded from the artifact.

        Args:
            path: Path to check (relative to repo root)

        Returns:
            True if should be excluded, False otherwise
        """
        path_str = str(path)

        for pattern in self.exclusions:
            # Handle directory patterns
            if pattern.endswith("/"):
                if path_str.startswith(pattern.rstrip("/")):
                    return True
            # Handle wildcard patterns
            elif "*" in pattern:
                import fnmatch
                if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern):
                    return True
            # Handle exact matches
            else:
                if pattern in path.parts or path.name == pattern:
                    return True

        return False

    def calculate_sha256(self, file_path: Path) -> str:
        """
        Calculate SHA256 checksum for a file.

        Args:
            file_path: Path to the file

        Returns:
            Hex string of SHA256 hash
        """
        sha256_hash = hashlib.sha256()
        
        # Read in chunks to handle large files
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()

    def generate_file_entry(self, file_path: Path, relative_path: Path) -> Dict:
        """
        Generate a manifest entry for a file.

        Args:
            file_path: Absolute path to the file
            relative_path: Path relative to framework_core/

        Returns:
            Dictionary with file metadata
        """
        checksum = self.calculate_sha256(file_path)
        file_stat = file_path.stat()
        
        # Determine scope based on path
        scope = "template" if "templates" in relative_path.parts else "core"
        
        return {
            "path": str(relative_path),
            "sha256": checksum,
            "mode": oct(file_stat.st_mode)[-3:],  # Get last 3 octal digits
            "scope": scope,
            "size": file_stat.st_size,
        }

    def copy_directory(self, src: Path, dst: Path, base_path: Path) -> List[Dict]:
        """
        Copy a directory tree, excluding patterns.

        Args:
            src: Source directory
            dst: Destination directory
            base_path: Base path for relative path calculation

        Returns:
            List of file entries for manifest
        """
        manifest_entries = []

        if not src.exists():
            print(f"⚠️  Source directory does not exist: {src}")
            return manifest_entries

        # Create destination directory
        if not self.dry_run:
            dst.mkdir(parents=True, exist_ok=True)

        # Walk the directory tree
        for root, dirs, files in os.walk(src):
            root_path = Path(root)
            rel_path = root_path.relative_to(src)

            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude(root_path / d)]

            for file_name in files:
                src_file = root_path / file_name
                rel_file_path = rel_path / file_name

                # Skip excluded files
                if self.should_exclude(src_file):
                    self.stats["files_skipped"] += 1
                    continue

                dst_file = dst / rel_file_path

                # Copy file
                if not self.dry_run:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)

                # Generate manifest entry
                manifest_entry = self.generate_file_entry(src_file, rel_file_path)
                manifest_entries.append(manifest_entry)

                self.stats["files_copied"] += 1
                self.stats["total_size"] += src_file.stat().st_size

        return manifest_entries

    def build_manifest(self, entries: List[Dict]) -> Dict:
        """
        Build the complete manifest structure.

        Args:
            entries: List of file entries

        Returns:
            Complete manifest dictionary
        """
        return {
            "version": self.version,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "files": sorted(entries, key=lambda x: x["path"]),
            "total_files": len(entries),
            "total_size": self.stats["total_size"],
        }

    def generate_metadata(self) -> Dict:
        """
        Generate metadata.json content.

        Returns:
            Metadata dictionary
        """
        metadata = {
            "version": self.version,
            "build_date": datetime.now(timezone.utc).isoformat(),
            "framework_name": "quickstart-agent-augmented-development",
        }

        # Try to get git commit
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True,
            )
            metadata["git_commit"] = result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Git not available or not a git repo
            metadata["git_commit"] = "unknown"

        # Try to get git branch
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True,
            )
            metadata["git_branch"] = result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            metadata["git_branch"] = "unknown"

        metadata["release_notes_path"] = "META/RELEASE_NOTES.md"
        metadata["manifest_path"] = "META/MANIFEST.yml"

        return metadata

    def generate_release_notes(self) -> str:
        """
        Generate release notes content.

        Returns:
            Markdown string
        """
        return f"""# Release Notes: Framework v{self.version}

**Release Date:** {datetime.now(timezone.utc).strftime("%Y-%m-%d")}

## Overview

This release package contains the Quickstart Agent-Augmented Development Framework
version {self.version}, as specified in ADR-013 (Zip-Based Framework Distribution).

## Package Contents

- `framework_core/` - Core framework files (agents, directives, guidelines, templates)
- `scripts/` - Installation and upgrade scripts
- `META/` - Manifest, metadata, and release documentation

## Installation

1. Extract this package to a temporary location
2. Review `META/MANIFEST.yml` to understand included files
3. Run installation scripts (see scripts/README.md)

## Upgrade Notes

If upgrading from a previous version:
- Review `UPGRADE_NOTES.md` for breaking changes
- Run `framework_upgrade.sh` with --dry-run first
- Framework Guardian agent can help resolve conflicts

## Documentation

- Architecture: `framework_core/docs/architecture/`
- Directives: `framework_core/docs/directives/`
- Guidelines: `framework_core/docs/guidelines/`

## Support

For issues and questions:
- Repository: https://github.com/sddevelopment-be/quickstart_agent-augmented-development
- Documentation: See README.md in framework_core/

## Checksums

Verify package integrity using the checksums.txt file alongside this package.
"""

    def assemble_framework_core(self) -> List[Dict]:
        """
        Assemble the framework_core/ directory.

        Returns:
            List of manifest entries
        """
        print("📦 Assembling framework_core/...")
        
        core_dir = self.build_dir / "framework_core"
        all_entries = []

        # Copy core directories
        print(f"   📦 Including {len(self.core_dirs)} core directories")
        for dir_name in self.core_dirs:
            src_dir = self.repo_root / dir_name
            dst_dir = core_dir / dir_name
            
            if src_dir.exists():
                print(f"   📁 Copying {dir_name}...")
                entries = self.copy_directory(src_dir, dst_dir, core_dir)
                all_entries.extend(entries)
            else:
                print(f"   ⚠️  Skipping {dir_name} (not found)")
        
        # Copy export directories (agent definitions for various platforms)
        if self.export_dirs:
            print(f"   📦 Including {len(self.export_dirs)} export directories")
            for dir_name in self.export_dirs:
                src_dir = self.repo_root / dir_name
                dst_dir = core_dir / dir_name
                
                if src_dir.exists():
                    print(f"   📁 Copying {dir_name}...")
                    entries = self.copy_directory(src_dir, dst_dir, core_dir)
                    all_entries.extend(entries)
                else:
                    print(f"   ⚠️  Skipping {dir_name} (not found)")

        # Copy root files
        print(f"   📦 Including {len(self.root_files)} root files")
        for file_name in self.root_files:
            src_file = self.repo_root / file_name
            dst_file = core_dir / file_name
            
            if src_file.exists():
                print(f"   📄 Copying {file_name}...")
                if not self.dry_run:
                    shutil.copy2(src_file, dst_file)
                
                entry = self.generate_file_entry(src_file, Path(file_name))
                all_entries.append(entry)
                
                self.stats["files_copied"] += 1
                self.stats["total_size"] += src_file.stat().st_size
            else:
                print(f"   ⚠️  Skipping {file_name} (not found)")

        print(f"   ✅ Copied {len(all_entries)} files")
        return all_entries

    def assemble_scripts(self) -> None:
        """
        Assemble the scripts/ directory.
        """
        print("📜 Assembling scripts/...")
        
        scripts_dir = self.build_dir / "scripts"
        
        if not self.dry_run:
            scripts_dir.mkdir(parents=True, exist_ok=True)

        # Copy scripts from configuration
        scripts_copied = 0
        for script_path in self.scripts:
            src_script = self.repo_root / script_path
            dst_script = scripts_dir / Path(script_path).name
            
            if src_script.exists():
                print(f"   📜 Copying {script_path}...")
                if not self.dry_run:
                    shutil.copy2(src_script, dst_script)
                    # Ensure scripts are executable
                    dst_script.chmod(dst_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                scripts_copied += 1
            else:
                print(f"   ⚠️  Script not found: {script_path}")
        
        # Create README for scripts directory
        readme_content = """# Framework Scripts

This directory contains helper scripts for installing and upgrading the framework.

## Scripts

### framework_install.sh

Installs the framework into a target repository for the first time.

Usage:
```bash
./framework_install.sh /path/to/target/repo [--dry-run] [--verbose]
```

### framework_upgrade.sh

Upgrades an existing framework installation while preserving local customizations.

Usage:
```bash
./framework_upgrade.sh /path/to/target/repo [--dry-run] [--plan] [--verbose]
```

## Documentation

See `docs/HOW_TO_USE/framework_install.md` for detailed usage instructions.
See `docs/architecture/design/distribution_of_releases_technical_design.md`
for technical specifications.
"""
        
        if not self.dry_run:
            readme_path = scripts_dir / "README.md"
            readme_path.write_text(readme_content)
        
        print("   ✅ Scripts directory prepared")

    def assemble_meta(self, manifest_entries: List[Dict]) -> None:
        """
        Assemble the META/ directory.

        Args:
            manifest_entries: List of file entries for manifest
        """
        print("📋 Assembling META/...")
        
        meta_dir = self.build_dir / "META"
        
        if not self.dry_run:
            meta_dir.mkdir(parents=True, exist_ok=True)

        # Generate manifest
        manifest = self.build_manifest(manifest_entries)
        if not self.dry_run:
            manifest_path = meta_dir / "MANIFEST.yml"
            with open(manifest_path, "w") as f:
                yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
            print(f"   ✅ Created MANIFEST.yml ({len(manifest_entries)} files)")

        # Generate metadata
        metadata = self.generate_metadata()
        if not self.dry_run:
            metadata_path = meta_dir / "metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            print(f"   ✅ Created metadata.json")

        # Generate release notes
        release_notes = self.generate_release_notes()
        if not self.dry_run:
            notes_path = meta_dir / "RELEASE_NOTES.md"
            notes_path.write_text(release_notes)
            print(f"   ✅ Created RELEASE_NOTES.md")

    def create_zip_artifact(self) -> Path:
        """
        Create the zip artifact from the build directory.

        Returns:
            Path to the created zip file
        """
        zip_name = f"quickstart-framework-{self.version}.zip"
        zip_path = self.output_dir / zip_name

        if self.dry_run:
            print(f"🎁 Would create: {zip_path}")
            return zip_path

        print(f"🎁 Creating zip artifact: {zip_name}...")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(self.build_dir):
                for file_name in files:
                    file_path = Path(root) / file_name
                    arcname = file_path.relative_to(self.build_dir)
                    
                    # Preserve file permissions in zip
                    file_stat = file_path.stat()
                    zip_info = zipfile.ZipInfo.from_file(file_path, arcname)
                    zip_info.external_attr = file_stat.st_mode << 16
                    
                    with open(file_path, "rb") as f:
                        zf.writestr(zip_info, f.read())

        zip_size = zip_path.stat().st_size
        print(f"   ✅ Created {zip_name} ({zip_size:,} bytes)")

        return zip_path

    def generate_checksums_file(self, zip_path: Path) -> None:
        """
        Generate checksums.txt for the zip artifact.

        Args:
            zip_path: Path to the zip file
        """
        if self.dry_run:
            print("📝 Would generate checksums.txt")
            return

        print("📝 Generating checksums...")

        checksum = self.calculate_sha256(zip_path)
        checksums_path = self.output_dir / "checksums.txt"

        with open(checksums_path, "w") as f:
            f.write(f"{checksum}  {zip_path.name}\n")

        print(f"   ✅ Created checksums.txt")
        print(f"   SHA256: {checksum}")

    def build(self) -> bool:
        """
        Execute the complete build process.

        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*70}")
        print(f"🚀 Building Release Artifact: v{self.version}")
        print(f"{'='*70}\n")

        # Validation
        print("🔍 Validating...")
        if not self.validate_version():
            return False
        if not self.validate_repository():
            return False
        print("   ✅ Validation passed\n")

        # Create output directory
        if not self.dry_run:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
            self.build_dir.mkdir(parents=True)

        # Assemble components
        manifest_entries = self.assemble_framework_core()
        print()
        
        self.assemble_scripts()
        print()
        
        self.assemble_meta(manifest_entries)
        print()

        # Create zip
        zip_path = self.create_zip_artifact()
        print()

        # Generate checksums
        self.generate_checksums_file(zip_path)
        print()

        # Summary
        print(f"{'='*70}")
        print("✨ Build Summary")
        print(f"{'='*70}")
        print(f"   Version: {self.version}")
        print(f"   Files copied: {self.stats['files_copied']}")
        print(f"   Files skipped: {self.stats['files_skipped']}")
        print(f"   Total size: {self.stats['total_size']:,} bytes")
        if not self.dry_run:
            print(f"   Output: {zip_path}")
            print(f"   Checksums: {self.output_dir / 'checksums.txt'}")
        else:
            print(f"   Mode: DRY RUN (no files created)")
        print(f"{'='*70}\n")

        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build release artifact for Quickstart Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build release v1.0.0 with full profile (default)
  python build_release_artifact.py --version 1.0.0

  # Build with minimal profile (no exports, minimal docs)
  python build_release_artifact.py --version 1.0.0 --profile minimal

  # Build with custom configuration file
  python build_release_artifact.py --version 1.0.0 --config custom-config.yaml

  # Build with custom output directory
  python build_release_artifact.py --version 1.0.0 --output-dir ./releases

  # Dry run to validate without creating files
  python build_release_artifact.py --version 1.0.0 --dry-run

Reference:
  ADR-013: Zip-Based Framework Distribution
  ADR-014: Framework Guardian Agent
  ops/release/distribution-config.yaml: Configuration file
""",
    )

    parser.add_argument(
        "--version",
        required=True,
        help="Version string (e.g., 1.0.0, 1.0.0-rc.1)",
    )

    parser.add_argument(
        "--output-dir",
        default="./output/releases",
        help="Output directory for artifacts (default: ./output/releases)",
    )

    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root directory (default: current directory)",
    )
    
    parser.add_argument(
        "--config",
        help="Path to distribution configuration YAML file (default: ops/release/distribution-config.yaml)",
    )
    
    parser.add_argument(
        "--profile",
        default="full",
        choices=["full", "minimal", "documentation", "platform_exports"],
        help="Distribution profile to use (default: full)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate structure without creating artifacts",
    )

    args = parser.parse_args()

    # Build artifact
    builder = ReleaseArtifactBuilder(
        version=args.version,
        output_dir=Path(args.output_dir),
        repo_root=Path(args.repo_root),
        dry_run=args.dry_run,
        config_file=Path(args.config) if args.config else None,
        profile=args.profile,
    )

    success = builder.build()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
