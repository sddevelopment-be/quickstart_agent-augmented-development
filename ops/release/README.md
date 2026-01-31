# Release Packaging System

This directory contains tools for building release artifacts of the Quickstart Agent-Augmented Development Framework.

## Overview

The release packaging system implements the distribution strategy defined in:
- **ADR-013**: Zip-Based Framework Distribution
- **ADR-014**: Framework Guardian Agent
- **Technical Design**: `docs/architecture/design/distribution_of_releases_technical_design.md`

## Components

### build_release_artifact.py

Python script that assembles and packages framework releases.

**Features:**
- ✅ Validates repository structure
- ✅ Assembles `framework_core/` with curated directories
- ✅ Generates manifest with checksums (SHA256)
- ✅ Creates metadata.json with version and git info
- ✅ Produces zip artifact with preserved permissions
- ✅ Generates checksums.txt for artifact verification
- ✅ Supports dry-run mode for validation

**Usage:**

```bash
# Build a release
python ops/release/build_release_artifact.py --version 1.0.0

# Custom output directory
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --output-dir ./releases

# Dry run (validate without creating files)
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --dry-run

# From different repo location
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --repo-root /path/to/repo
```

**Version Format:**

Follows semantic versioning:
- Release: `1.0.0`
- Pre-release: `1.0.0-rc.1`, `1.0.0-alpha.1`, `1.0.0-beta.2`
- Build metadata: `1.0.0+20260131`

## Artifact Structure

```
quickstart-framework-<version>.zip
├── framework_core/
│   ├── .github/
│   │   └── agents/           # Agent profiles and directives
│   ├── docs/
│   │   ├── templates/        # Document templates
│   │   └── architecture/     # Architecture docs and ADRs
│   ├── framework/            # Core Python framework
│   ├── validation/           # Validation scripts and tests
│   ├── work/
│   │   └── templates/        # Work item templates
│   ├── AGENTS.md             # Agent coordination protocol
│   ├── README.md             # Framework documentation
│   ├── pyproject.toml        # Python project config
│   └── requirements.txt      # Python dependencies
├── scripts/
│   └── README.md             # Installation/upgrade script docs
└── META/
    ├── MANIFEST.yml          # File inventory with checksums
    ├── metadata.json         # Build metadata
    └── RELEASE_NOTES.md      # Release documentation
```

## Manifest Format

The `META/MANIFEST.yml` file lists every managed file:

```yaml
version: 1.0.0
generated_at: '2026-01-31T12:00:00+00:00'
files:
  - path: AGENTS.md
    sha256: abc123...
    mode: '664'
    scope: core
    size: 9266
  - path: framework/core.py
    sha256: def456...
    mode: '664'
    scope: core
    size: 6707
total_files: 329
total_size: 2953434
```

**Fields:**
- `path`: Relative path within framework_core/
- `sha256`: SHA256 checksum for integrity verification
- `mode`: Unix file permissions (octal)
- `scope`: `core` or `template` (for Guardian classification)
- `size`: File size in bytes

## Metadata Format

The `META/metadata.json` file contains build information:

```json
{
  "version": "1.0.0",
  "build_date": "2026-01-31T12:00:00+00:00",
  "framework_name": "quickstart-agent-augmented-development",
  "git_commit": "abc123...",
  "git_branch": "main",
  "release_notes_path": "META/RELEASE_NOTES.md",
  "manifest_path": "META/MANIFEST.yml"
}
```

## Exclusion Rules

The following are **excluded** from releases:

### Version Control
- `.git/`, `.gitignore`

### Python Cache
- `__pycache__/`, `*.pyc`, `*.pyo`, `.pytest_cache/`

### Work Outputs
- `work/logs/`, `work/reports/`, `work/collaboration/`

### Local Overrides
- `local/` (project-specific customizations)

### Temporary Files
- `tmp/`, `output/`

### IDE Files
- `.vscode/`, `.idea/`, `.claude/`, `.opencode/`

### Build Artifacts
- `dist/`, `build/`, `*.egg-info/`

## Integration with CI/CD

### GitHub Actions Workflow

See `.github/workflows/release-packaging.yml` for automated builds on:
- Tagged releases (e.g., `v1.0.0`)
- Manual workflow dispatch

### Local Development

```bash
# Quick test
python ops/release/build_release_artifact.py --version 0.0.1-dev --dry-run

# Build test artifact
python ops/release/build_release_artifact.py --version 0.0.1-dev

# Verify artifact
cd output/releases
unzip -l quickstart-framework-0.0.1-dev.zip
sha256sum -c checksums.txt
```

## Verification

### Checksum Verification

```bash
# Verify artifact integrity
sha256sum -c checksums.txt
```

### Manifest Verification

```bash
# Extract and verify
unzip quickstart-framework-1.0.0.zip
cd quickstart-framework-1.0.0

# Check manifest
cat META/MANIFEST.yml | grep "total_files:"

# Verify a specific file
sha256sum framework_core/AGENTS.md
# Compare with value in MANIFEST.yml
```

## Troubleshooting

### Issue: Invalid repository structure

**Symptom:**
```
❌ Invalid repository structure. Missing directories:
   - .github/agents
```

**Solution:**
- Ensure you're running from the repository root
- Use `--repo-root` to specify correct location
- Verify required directories exist

### Issue: Invalid version format

**Symptom:**
```
❌ Invalid version format: v1.0.0
```

**Solution:**
- Don't include 'v' prefix: use `1.0.0` not `v1.0.0`
- Follow semantic versioning: `X.Y.Z[-prerelease][+build]`

### Issue: Permission denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
- Check output directory permissions
- Ensure script is executable: `chmod +x build_release_artifact.py`
- Use `--output-dir` to specify writable location

### Issue: Files missing in artifact

**Symptom:**
Some expected files are not in the zip.

**Solution:**
- Check if files match exclusion patterns (see Exclusion Rules)
- Verify files exist in source repository
- Use `--dry-run` to see what will be included

## Development

### Testing

```bash
# Run acceptance tests
pytest validation/release/test_release_packaging_acceptance.py -v

# Run unit tests
pytest validation/release/test_build_release_artifact.py -v

# Run all release tests
pytest validation/release/ -v
```

### Adding New Directories

To include additional directories in releases:

1. Edit `CORE_DIRECTORIES` in `build_release_artifact.py`
2. Update acceptance tests
3. Document in this README
4. Update manifest schema if needed

### Modifying Exclusion Patterns

To change what's excluded:

1. Edit `EXCLUDE_PATTERNS` in `build_release_artifact.py`
2. Test with `--dry-run`
3. Verify manifest and artifact size
4. Document changes

## References

- [ADR-013: Zip-Based Framework Distribution](../../docs/architecture/adrs/ADR-013-zip-distribution.md)
- [ADR-014: Framework Guardian Agent](../../docs/architecture/adrs/ADR-014-framework-guardian-agent.md)
- [Distribution Architecture](../../docs/architecture/design/distribution_of_releases_architecture.md)
- [Technical Design](../../docs/architecture/design/distribution_of_releases_technical_design.md)

## Support

For issues or questions:
- Check troubleshooting section above
- Review referenced ADRs and design docs
- Create an issue in the repository
- Consult Framework Guardian agent for upgrade conflicts
