# Framework Release Process

This document describes how to create and publish framework releases using the automated packaging pipeline.

## Overview

The framework uses a zip-based distribution model (see [ADR-013](../architecture/adrs/ADR-013-zip-distribution.md)) to package releases. Each release contains:

- **framework_core/**: Curated framework files (agents, directives, guidelines, templates, ADRs)
- **scripts/**: Installation and upgrade scripts
- **META/**: Manifest with file checksums, release notes, and upgrade notes

## Creating a Release

### Automated Release (Recommended)

Releases are automatically created when you push a version tag:

```bash
# Tag the release
git tag -a v1.0.0 -m "Release v1.0.0"

# Push the tag to trigger packaging workflow
git push origin v1.0.0
```

The GitHub Actions workflow will:
1. Run `shellcheck` validation on the packaging script
2. Execute `scripts/framework_package.sh` to create the zip
3. Verify package structure and contents
4. Generate SHA256 checksum
5. Create a GitHub Release with the package attached

### Manual Packaging

To create a package locally for testing:

```bash
# Package a specific version
./scripts/framework_package.sh 1.0.0

# Package development version
./scripts/framework_package.sh dev

# Package to specific directory
./scripts/framework_package.sh 1.0.0 /path/to/output
```

This creates `quickstart-framework-<version>.zip` in the output directory.

### Manual Release via GitHub Actions

You can also trigger packaging manually:

1. Go to **Actions** → **Framework Release Packaging**
2. Click **Run workflow**
3. Enter the version (e.g., `1.0.0`)
4. Click **Run workflow**

The package will be uploaded as a workflow artifact (30-day retention).

## Package Contents

Each release package contains:

```
quickstart-framework-1.0.0/
├── framework_core/
│   ├── .github/agents/          # Agent profiles and directives
│   ├── docs/
│   │   ├── directives/          # Externalized directives
│   │   ├── guidelines/          # Operational guidelines
│   │   ├── templates/           # Document and task templates
│   │   └── architecture/adrs/   # Architecture Decision Records
│   ├── validation/              # Validation scripts and schemas
│   └── work/                    # Empty work directory scaffolds
├── scripts/
│   ├── framework_install.sh     # First-time installation
│   └── framework_upgrade.sh     # Upgrade existing installation
└── META/
    ├── MANIFEST.yml             # File inventory with checksums
    ├── RELEASE_NOTES.md         # Release highlights
    └── UPGRADE_NOTES.md         # Migration guidance
```

## Manifest Generation

The `META/MANIFEST.yml` file is automatically generated during packaging and includes:

```yaml
framework_version: 1.0.0
packaged_at: 2025-11-24T20:00:00Z
package_format: zip

core_files:
  - path: .github/agents/architect.agent.md
    sha256: abc123...
    mode: regular
    scope: core
  - path: scripts/framework_install.sh
    sha256: def456...
    mode: executable
    scope: core
  # ... (all files with checksums)
```

This manifest is used by:
- **Installation script**: To verify file integrity
- **Upgrade script**: To detect changes and conflicts
- **Framework Guardian**: To audit installations and detect drift

## Verification

After packaging, verify the release:

```bash
# Check package structure
unzip -l quickstart-framework-1.0.0.zip

# Verify checksum
sha256sum -c quickstart-framework-1.0.0.zip.sha256

# Test extraction
unzip quickstart-framework-1.0.0.zip
cd quickstart-framework-1.0.0

# Verify scripts are executable
ls -l scripts/

# Check manifest
cat META/MANIFEST.yml | head -20
```

## Release Checklist

Before creating a release:

- [ ] All ADRs are up to date and properly indexed
- [ ] Documentation reflects current framework state
- [ ] Agent profiles are consistent and complete
- [ ] Templates are validated and examples work
- [ ] Installation/upgrade scripts are tested
- [ ] CHANGELOG.md is updated with notable changes
- [ ] Version number follows semantic versioning

After release:

- [ ] Verify GitHub Release was created successfully
- [ ] Test installation in a clean repository
- [ ] Test upgrade from previous version
- [ ] Update downstream projects
- [ ] Announce release to stakeholders

## Troubleshooting

### Package Too Large

If the package size is excessive:

1. Check for accidentally included build artifacts
2. Review `.github/agents/` for unnecessary files
3. Consider excluding large optional directories
4. Update `CORE_DIRS` in `scripts/framework_package.sh`

### Missing Files in Package

If expected files are missing:

1. Verify files exist in the repository
2. Check `CORE_DIRS` includes the parent directory
3. Ensure files aren't gitignored
4. Review build logs for warnings

### Shellcheck Failures

If the packaging script fails shellcheck:

1. Review reported issues
2. Fix POSIX compliance problems
3. Test locally: `shellcheck scripts/framework_package.sh`
4. Commit fixes and retry

### Manifest Generation Errors

If `META/MANIFEST.yml` is incomplete:

1. Check for permission issues on files
2. Verify `sha256sum` is available
3. Check for symlinks (not supported)
4. Review script output for warnings

## Related Documentation

- [ADR-013: Zip-Based Framework Distribution](../architecture/adrs/ADR-013-zip-distribution.md)
- [ADR-014: Framework Guardian Agent](../architecture/adrs/ADR-014-framework-guardian-agent.md)
- [Framework Installation Guide](framework-installation.md) *(to be created)*
- [Framework Upgrade Guide](framework-upgrades.md) *(to be created)*
- [Technical Design: Distribution & Guardian Workflow](../architecture/design/distribution_of_releases_technical_design.md)

## Support

For questions or issues with the release process:

1. Check this documentation
2. Review GitHub Actions logs for errors
3. Consult ADR-013 for architectural rationale
4. Open an issue with the `release` label
