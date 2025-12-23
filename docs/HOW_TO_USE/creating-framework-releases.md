# Creating Framework Releases

## Overview

This guide explains how to create and publish releases of the quickstart-agent-augmented-development framework. The release process packages the framework core into a distributable zip file and publishes it as a GitHub Release.

**Related Documentation:**
- ADR-013: Zip-Based Framework Distribution
- `docs/architecture/design/distribution_of_releases_technical_design.md`
- `docs/architecture/design/distribution_of_releases_architecture.md`

## Release Package Structure

Each release produces `quickstart-framework-<version>.zip` containing:

```
quickstart-framework-<version>.zip
├── framework_core/
│   ├── .github/agents/          # Core agent profiles, directives, guidelines
│   ├── docs/templates/          # Architecture, documentation templates
│   ├── validation/              # Schema validation and testing
│   ├── work/                    # Work directory structure scaffold
│   ├── AGENTS.md                # Agent Specification Document
│   └── REPO_MAP.md              # Repository structure overview
├── scripts/
│   ├── framework_install.sh     # Installation script
│   └── framework_upgrade.sh     # Upgrade script
└── META/
    ├── MANIFEST.yml             # File inventory with checksums
    └── RELEASE_NOTES.md         # Release notes
```

## Prerequisites

Before creating a release, ensure:

1. **All tests pass**: Run validation workflows locally or in CI
2. **Documentation is current**: Update relevant docs for any changes
3. **MANIFEST.yml is up-to-date**: Run `ops/scripts/generate_manifest.sh` if needed
4. **ADRs are documented**: Significant decisions should have ADRs
5. **Version number decided**: Follow semantic versioning (MAJOR.MINOR.PATCH)

## Local Testing

### Test Package Assembly

Before triggering the CI release, test the packaging script locally:

```bash
# Test with dry-run to see what would be packaged
./ops/scripts/assemble_framework_package.sh --dry-run 1.0.0

# Actually create the package
./ops/scripts/assemble_framework_package.sh 1.0.0

# Verify package contents
cd build
unzip -l quickstart-framework-1.0.0.zip

# Extract and test installation
unzip quickstart-framework-1.0.0.zip
cd quickstart-framework-1.0.0

# Test installation script (dry-run)
./scripts/framework_install.sh --dry-run /tmp/test-project

# Test upgrade script (dry-run)
./scripts/framework_upgrade.sh --dry-run /tmp/existing-project
```

### Test Release Notes Generation

```bash
# Generate release notes for review
./ops/scripts/generate_release_notes.sh 1.0.0

# Generate with previous version comparison
./ops/scripts/generate_release_notes.sh --previous 0.9.0 1.0.0

# Save to file
./ops/scripts/generate_release_notes.sh --output RELEASE_NOTES.md 1.0.0
```

### Validate Package Structure

```bash
# After creating package, validate structure
cd build
mkdir validate-test
cd validate-test
unzip ../quickstart-framework-1.0.0.zip

# Check required directories exist
ls -la framework_core scripts META

# Verify MANIFEST.yml is valid YAML
python3 -c "import yaml; yaml.safe_load(open('META/MANIFEST.yml'))"

# Check scripts are executable
ls -l scripts/*.sh

# Verify checksum
sha256sum -c ../SHA256SUMS
```

## Creating a Release

### Option 1: Tag-Triggered Release (Recommended)

The automated way to create releases using Git tags:

```bash
# 1. Ensure you're on main branch and up-to-date
git checkout main
git pull origin main

# 2. Create and push version tag
VERSION="1.0.0"
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin "v$VERSION"

# 3. Monitor workflow
# Go to GitHub Actions → Framework Release workflow
# The workflow will automatically:
#   - Assemble the package
#   - Generate release notes
#   - Validate package structure
#   - Create GitHub Release
#   - Attach zip and checksum
```

**Tag Format:**
- Production release: `v1.0.0`
- Pre-release: `v1.0.0-beta.1`, `v1.0.0-rc.1`
- Tags with `-` suffix are automatically marked as pre-release

### Option 2: Manual Dispatch

For testing or special cases, trigger manually:

```bash
# Go to GitHub → Actions → Framework Release → Run workflow
# Inputs:
#   - version: 1.0.0 (without 'v' prefix)
#   - prerelease: true/false
```

This is useful for:
- Testing the release process
- Creating releases without creating tags
- Rebuilding a release if needed

## Release Workflow Steps

The GitHub Actions workflow performs these steps:

1. **Version Determination**
   - Extract version from tag or manual input
   - Validate semver format

2. **Package Assembly** (`assemble_framework_package.sh`)
   - Create clean build directory
   - Copy framework_core directories
   - Copy installation scripts
   - Generate/update META files
   - Validate no sensitive data included

3. **Release Notes Generation** (`generate_release_notes.sh`)
   - Extract relevant changelog entries
   - List new/modified ADRs
   - Format installation instructions

4. **Package Validation**
   - Verify directory structure
   - Check required files present
   - Validate MANIFEST.yml
   - Ensure scripts are executable

5. **Zip Creation**
   - Create deterministic zip archive
   - Calculate SHA256 checksum
   - Store in SHA256SUMS file

6. **GitHub Release**
   - Create release with generated notes
   - Attach quickstart-framework-<version>.zip
   - Attach SHA256SUMS
   - Mark as pre-release if applicable

7. **Artifact Upload**
   - Store build artifacts for 90 days
   - Available for download/review

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

**Format:** MAJOR.MINOR.PATCH

- **MAJOR**: Incompatible changes (breaking changes)
  - Example: `1.0.0` → `2.0.0`
  - Requires migration guide
  - May need manual conflict resolution

- **MINOR**: New features, backward-compatible
  - Example: `1.0.0` → `1.1.0`
  - Safe upgrades with `framework_upgrade.sh`
  - May add new files

- **PATCH**: Bug fixes, backward-compatible
  - Example: `1.0.0` → `1.0.1`
  - Safe upgrades
  - No new features

**Pre-release Versions:**
- Alpha: `1.0.0-alpha.1`
- Beta: `1.0.0-beta.1`
- Release Candidate: `1.0.0-rc.1`

## Post-Release Checklist

After a successful release:

- [ ] Verify release appears on GitHub Releases page
- [ ] Download and test the zip package
- [ ] Verify checksum matches
- [ ] Test installation on a clean project
- [ ] Test upgrade on an existing project
- [ ] Update documentation if needed
- [ ] Announce release (if public)
- [ ] Monitor for issues in first 24 hours

## Troubleshooting

### Package Assembly Fails

**Problem:** Script errors during assembly

**Solutions:**
```bash
# Check source files exist
ls -la .github/agents/ docs/templates/ validation/

# Verify MANIFEST.yml is valid
python3 -c "import yaml; yaml.safe_load(open('META/MANIFEST.yml'))"

# Run with verbose output
bash -x ops/scripts/assemble_framework_package.sh 1.0.0
```

### Release Already Exists

**Problem:** Tag or release already exists

**Solutions:**
```bash
# Delete tag locally and remotely (careful!)
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# Or delete release via GitHub UI and re-run workflow

# Or update version number
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

### Zip Validation Fails

**Problem:** Package structure doesn't match spec

**Solutions:**
```bash
# Check what's actually in the package
unzip -l build/quickstart-framework-1.0.0.zip

# Review assembly script logic
cat ops/scripts/assemble_framework_package.sh

# Verify source paths exist
find .github/agents docs/templates validation -type f | wc -l
```

### GitHub Actions Workflow Fails

**Problem:** Workflow errors in CI

**Solutions:**
1. Check workflow run logs in GitHub Actions
2. Look for specific step failures
3. Test scripts locally first
4. Verify permissions (workflow needs `contents: write`)
5. Check if secrets/tokens are valid

### Checksum Mismatch

**Problem:** SHA256 doesn't match after download

**Solutions:**
```bash
# Recalculate locally
sha256sum quickstart-framework-1.0.0.zip

# Compare with GitHub Release SHA256SUMS
# If different, package may be corrupted
# Re-run release workflow or re-upload manually
```

## Manual Release (Fallback)

If automation fails, create release manually:

```bash
# 1. Create package locally
./ops/scripts/assemble_framework_package.sh 1.0.0

# 2. Generate release notes
./ops/scripts/generate_release_notes.sh --output NOTES.md 1.0.0

# 3. Create release via GitHub CLI
gh release create v1.0.0 \
  build/quickstart-framework-1.0.0.zip \
  build/SHA256SUMS \
  --title "Framework Release 1.0.0" \
  --notes-file NOTES.md

# Or use GitHub web UI:
# - Go to Releases → Draft a new release
# - Choose tag or create new: v1.0.0
# - Upload zip and SHA256SUMS
# - Paste release notes
# - Publish release
```

## Security Considerations

### Before Release

- [ ] Review changes for sensitive data exposure
- [ ] Ensure no API keys, tokens, or passwords in files
- [ ] Validate all included files are intended for distribution
- [ ] Review new scripts for security issues
- [ ] Check dependencies for known vulnerabilities

### Package Validation

The assembly script performs basic checks:
```bash
# Searches for common sensitive patterns
grep -r "password\|secret\|token\|api.key" build/
```

**Manual review recommended for:**
- Configuration files
- Environment templates
- Example files
- Test fixtures

### Distribution

- Always provide SHA256 checksum
- Sign releases with GPG (optional but recommended)
- Publish release notes explaining changes
- Document known issues or breaking changes
- Monitor for security reports after release

## Advanced: Customizing Release Process

### Custom Package Contents

Edit `ops/scripts/assemble_framework_package.sh`:

```bash
# Modify core_paths variable to include/exclude directories
core_paths=".github/agents docs/templates validation work/README.md AGENTS.md"
```

### Custom Release Notes

Edit `ops/scripts/generate_release_notes.sh`:

```bash
# Add custom sections
generate_custom_section() {
    output "## Custom Section"
    output ""
    # Your custom logic here
}
```

### Workflow Customization

Edit `.github/workflows/framework-release.yml`:

```yaml
# Add custom validation steps
- name: Custom Validation
  run: |
    # Your validation logic
    ./custom-checks.sh
```

## Related Scripts

- **`ops/scripts/assemble_framework_package.sh`**: Package assembly
- **`ops/scripts/generate_release_notes.sh`**: Release notes generation
- **`ops/scripts/framework_install.sh`**: Installation (included in package)
- **`ops/scripts/framework_upgrade.sh`**: Upgrade (included in package)
- **`ops/scripts/generate_manifest.sh`**: MANIFEST.yml generation

## Support

For questions or issues with the release process:

1. Check this documentation
2. Review ADR-013 and technical design docs
3. Examine workflow logs in GitHub Actions
4. Test scripts locally with `--dry-run`
5. Open an issue on the repository

## Release History

Releases are available at:
https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases

Download format:
```bash
# Latest release
curl -LO https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/latest/download/quickstart-framework-VERSION.zip

# Specific version
curl -LO https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.0.0/quickstart-framework-1.0.0.zip
```
