"""
Integration test for the complete release packaging pipeline.

This test validates the actual implementation against acceptance criteria.
"""

import json
import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

import pytest
import yaml


def test_full_release_pipeline():
    """
    Integration test: Build a complete release artifact and verify all components.
    
    This test validates:
    - Script execution
    - Artifact structure
    - Manifest correctness
    - Metadata completeness
    - Checksum accuracy
    """
    
    # Setup
    test_version = "0.1.0-integration-test"
    test_output_dir = tempfile.mkdtemp()
    
    try:
        # Get repository root
        repo_root = Path(__file__).parent.parent.parent
        
        # Build the artifact
        result = subprocess.run(
            [
                "python",
                str(repo_root / "ops/release/build_release_artifact.py"),
                "--version", test_version,
                "--output-dir", test_output_dir,
                "--repo-root", str(repo_root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        # Verify build succeeded
        assert result.returncode == 0, f"Build failed:\n{result.stdout}\n{result.stderr}"
        
        # Verify artifact was created
        artifact_name = f"quickstart-framework-{test_version}.zip"
        artifact_path = Path(test_output_dir) / artifact_name
        assert artifact_path.exists(), f"Artifact not found: {artifact_path}"
        
        # Verify checksums file was created
        checksums_path = Path(test_output_dir) / "checksums.txt"
        assert checksums_path.exists(), "checksums.txt not found"
        
        # Verify checksum is correct
        import hashlib
        with open(artifact_path, "rb") as f:
            actual_checksum = hashlib.sha256(f.read()).hexdigest()
        
        with open(checksums_path, "r") as f:
            expected_line = f.read().strip()
            expected_checksum = expected_line.split()[0]
        
        assert actual_checksum == expected_checksum, "Checksum mismatch"
        
        # Extract artifact
        extract_dir = Path(test_output_dir) / f"quickstart-framework-{test_version}"
        with zipfile.ZipFile(artifact_path, 'r') as zf:
            zf.extractall(test_output_dir)
        
        # Verify directory structure
        assert extract_dir.exists(), "Extracted directory not found"
        assert (extract_dir / "framework_core").exists(), "framework_core/ missing"
        assert (extract_dir / "scripts").exists(), "scripts/ missing"
        assert (extract_dir / "META").exists(), "META/ missing"
        
        # Verify META files
        manifest_path = extract_dir / "META/MANIFEST.yml"
        assert manifest_path.exists(), "MANIFEST.yml missing"
        
        metadata_path = extract_dir / "META/metadata.json"
        assert metadata_path.exists(), "metadata.json missing"
        
        release_notes_path = extract_dir / "META/RELEASE_NOTES.md"
        assert release_notes_path.exists(), "RELEASE_NOTES.md missing"
        
        # Verify manifest structure
        with open(manifest_path, "r") as f:
            manifest = yaml.safe_load(f)
        
        assert manifest["version"] == test_version, "Version mismatch in manifest"
        assert "generated_at" in manifest, "generated_at missing"
        assert "files" in manifest, "files list missing"
        assert isinstance(manifest["files"], list), "files should be a list"
        assert len(manifest["files"]) > 0, "files list is empty"
        assert "total_files" in manifest, "total_files missing"
        assert "total_size" in manifest, "total_size missing"
        
        # Verify file entry structure
        first_file = manifest["files"][0]
        assert "path" in first_file, "path missing in file entry"
        assert "sha256" in first_file, "sha256 missing in file entry"
        assert "mode" in first_file, "mode missing in file entry"
        assert "scope" in first_file, "scope missing in file entry"
        assert "size" in first_file, "size missing in file entry"
        
        # Verify metadata structure
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        
        assert metadata["version"] == test_version, "Version mismatch in metadata"
        assert "build_date" in metadata, "build_date missing"
        assert "framework_name" in metadata, "framework_name missing"
        assert "git_commit" in metadata, "git_commit missing"
        assert "release_notes_path" in metadata, "release_notes_path missing"
        assert "manifest_path" in metadata, "manifest_path missing"
        
        # Verify core files are included
        assert (extract_dir / "framework_core/AGENTS.md").exists(), "AGENTS.md missing"
        assert (extract_dir / "framework_core/README.md").exists(), "README.md missing"
        assert (extract_dir / "framework_core/.github/agents").exists(), "agents/ missing"
        
        # Verify exclusions worked
        assert not (extract_dir / "framework_core/.git").exists(), ".git should be excluded"
        assert not (extract_dir / "framework_core/tmp").exists(), "tmp should be excluded"
        
        # Verify checksum of a file matches manifest
        test_file = extract_dir / "framework_core/AGENTS.md"
        with open(test_file, "rb") as f:
            file_checksum = hashlib.sha256(f.read()).hexdigest()
        
        # Find the file in manifest
        agents_entry = next(
            (f for f in manifest["files"] if f["path"] == "AGENTS.md"),
            None
        )
        assert agents_entry is not None, "AGENTS.md not in manifest"
        assert agents_entry["sha256"] == file_checksum, "AGENTS.md checksum mismatch"
        
        print("✅ All integration tests passed!")
        
    finally:
        # Cleanup
        shutil.rmtree(test_output_dir, ignore_errors=True)


def test_dry_run_mode():
    """Test that dry-run mode validates without creating files."""
    
    repo_root = Path(__file__).parent.parent.parent
    test_version = "0.1.0-dry-run-test"
    test_output_dir = tempfile.mkdtemp()
    
    try:
        result = subprocess.run(
            [
                "python",
                str(repo_root / "ops/release/build_release_artifact.py"),
                "--version", test_version,
                "--output-dir", test_output_dir,
                "--repo-root", str(repo_root),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        # Should succeed
        assert result.returncode == 0, f"Dry-run failed:\n{result.stdout}\n{result.stderr}"
        
        # Should not create artifact
        artifact_path = Path(test_output_dir) / f"quickstart-framework-{test_version}.zip"
        assert not artifact_path.exists(), "Artifact should not be created in dry-run mode"
        
        # Output should mention dry-run
        assert "DRY RUN" in result.stdout, "Output should mention dry-run mode"
        
        print("✅ Dry-run test passed!")
        
    finally:
        shutil.rmtree(test_output_dir, ignore_errors=True)


def test_invalid_version_format():
    """Test that invalid version formats are rejected."""
    
    repo_root = Path(__file__).parent.parent.parent
    test_output_dir = tempfile.mkdtemp()
    
    try:
        # Try with 'v' prefix (invalid)
        result = subprocess.run(
            [
                "python",
                str(repo_root / "ops/release/build_release_artifact.py"),
                "--version", "v1.0.0",  # Invalid: has 'v' prefix
                "--output-dir", test_output_dir,
                "--repo-root", str(repo_root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        # Should fail
        assert result.returncode != 0, "Should reject version with 'v' prefix"
        assert "Invalid version format" in result.stdout, "Should mention invalid format"
        
        print("✅ Invalid version test passed!")
        
    finally:
        shutil.rmtree(test_output_dir, ignore_errors=True)


if __name__ == "__main__":
    # Run tests
    test_full_release_pipeline()
    test_dry_run_mode()
    test_invalid_version_format()
    print("\n🎉 All integration tests passed!")
