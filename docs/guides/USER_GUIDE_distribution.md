# Framework Distribution Guide

**Understanding what gets distributed and how to build releases**

This guide explains the distribution model for the Quickstart Agent-Augmented Development Framework—what's included in releases, how different profiles work, and how to build your own distributions.

## Table of Contents

- [Overview](#overview)
- [What Gets Distributed](#what-gets-distributed)
- [Distribution Profiles](#distribution-profiles)
- [Export Directories](#export-directories)
- [Building Releases](#building-releases)
- [Artifact Structure](#artifact-structure)
- [Exclusion Rules](#exclusion-rules)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

The framework follows a **zip-based distribution model** (ADR-013) that packages everything you need into a single, versioned artifact. This approach gives you:

- **Reproducible installations** - Same artifact = same result
- **Version tracking** - Know exactly what version you have installed
- **Integrity verification** - Checksums ensure nothing got corrupted
- **Safe upgrades** - Clear conflict detection and resolution

Think of it like a well-behaved software package: predictable, verifiable, and respectful of your customizations.

## What Gets Distributed

Each framework release includes several categories of content:

### Core Directories

These form the heart of the framework:

| Directory | Contents | Required |
|-----------|----------|----------|
| `.github/agents/` | Agent profiles and directives | ✅ Yes |
| `docs/templates/` | Document templates | ✅ Yes |
| `docs/architecture/` | Architecture docs and ADRs | ⚪ Optional |
| `framework/` | Python framework modules | ✅ Yes |
| `validation/` | Validation scripts and tests | ⚪ Optional |
| `work/templates/` | Work item templates | ✅ Yes |

**Why these?** These directories contain the framework's operational intelligence—the profiles that define agent behavior, the templates that structure work, and the validation that ensures quality.

### Root Files

Essential configuration and documentation:

```
README.md              # Framework documentation
AGENTS.md              # Agent coordination protocol  
pyproject.toml         # Python project configuration
requirements.txt       # Python dependencies
LICENSE                # Software license
```

### Installation Scripts

Located in `scripts/` within the release:

- `framework_install.sh` - First-time installation
- `framework_upgrade.sh` - Upgrade existing installation
- `README.md` - Script documentation

### Metadata

The `META/` directory contains release information:

- `MANIFEST.yml` - Complete file inventory with checksums
- `metadata.json` - Build information (version, git commit, date)
- `RELEASE_NOTES.md` - What's new in this version
- `checksums.txt` - Artifact integrity verification

## Distribution Profiles

Different use cases need different content. We provide four preconfigured profiles:

### Full Profile (Default)

**Use when:** You want everything.

**Includes:**
- All core directories
- All export directories (.claude, .opencode)
- All root files
- All scripts
- Complete documentation

**Best for:**
- Adopting the framework for the first time
- Setting up a template repository
- Building a downstream distribution
- Having all options available

**Size:** ~3-5 MB (largest distribution)

### Minimal Profile

**Use when:** You want just the essentials.

**Includes:**
- `.github/agents/` (agent profiles)
- `work/templates/` (work templates)
- `framework/` (core Python modules)
- `README.md` and `AGENTS.md`
- Installation scripts

**Excludes:**
- Documentation and architecture
- Platform-specific exports
- Optional components

**Best for:**
- Resource-constrained environments
- CI/CD integration where you only need core functionality
- Quick prototyping
- Minimal attack surface

**Size:** ~1-2 MB (smallest distribution)

### Documentation Profile

**Use when:** You're focused on documentation and architecture.

**Includes:**
- `.github/agents/` (for documentation agents)
- `docs/templates/` (document templates)
- `docs/architecture/` (ADRs and design docs)
- `README.md` and `AGENTS.md`

**Excludes:**
- Python framework modules
- Validation infrastructure
- Installation scripts
- Platform exports

**Best for:**
- Documentation-only teams
- Architecture repositories
- Knowledge management systems
- Teaching and training materials

**Size:** ~500 KB - 1 MB

### Platform Exports Profile

**Use when:** You only need agent definitions for specific platforms.

**Includes:**
- `.claude/` (Claude Desktop exports)
- `.opencode/` (OpenCode.ai exports)
- `README.md` and `AGENTS.md`

**Excludes:**
- Core framework directories
- Python modules
- Installation scripts
- Templates

**Best for:**
- Platform-specific deployments
- Distributing agent profiles to end users
- Integration with specific AI platforms
- Lightweight agent deployment

**Size:** ~200-500 KB (very small)

### Choosing a Profile

```bash
# When building, specify profile with --profile flag
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --profile minimal

# Default is 'full' if not specified
python ops/release/build_release_artifact.py --version 1.0.0
# ↑ Same as --profile full
```

> **Tip:** Start with the **full** profile. You can always build a minimal distribution later if you need it.

## Export Directories

Export directories contain platform-specific agent definitions generated from the framework's canonical profiles.

### .claude Directory

**Purpose:** Agent definitions for Claude Desktop and Anthropic API.

**Structure:**
```
.claude/
├── agents/           # Agent profile exports
│   ├── devops-danny.json
│   ├── editor-eddy.json
│   └── ...
├── prompts/          # System prompts
│   ├── analysis.txt
│   ├── technical-writing.txt
│   └── ...
└── skills/           # Reusable skills/functions
    ├── code-review.json
    └── ...
```

**Use when:**
- Deploying to Claude Desktop
- Using Claude API with custom profiles
- Integrating with Anthropic's MCP (Model Context Protocol)

### .opencode Directory

**Purpose:** Agent definitions for OpenCode.ai platform.

**Structure:**
```
.opencode/
├── agents/           # Agent profile exports
│   ├── devops-danny.yaml
│   ├── editor-eddy.yaml
│   └── ...
└── skills/           # Reusable skills
    ├── code-review.yaml
    └── ...
```

**Use when:**
- Deploying to OpenCode.ai
- Using OpenCode's agent orchestration
- Platform-specific integrations

### Export Generation

Exports are generated during the release build process:

```bash
# Exports are automatically included in 'full' and 'platform_exports' profiles
python ops/release/build_release_artifact.py --version 1.0.0

# To rebuild exports manually (future capability):
# python ops/export/generate_platform_exports.py
```

> **Note:** Export directories are optional. If you're not using Claude Desktop or OpenCode.ai, you can use profiles that exclude them.

## Building Releases

### Prerequisites

Before building a release, ensure you have:

- Python 3.8+ installed
- All framework files present in repository
- Git repository (for metadata extraction)
- Write permissions in output directory

### Basic Release Build

```bash
# Navigate to repository root
cd /path/to/quickstart_agent-augmented-development

# Build a release
python ops/release/build_release_artifact.py --version 1.0.0
```

**Output:**
```
🔨 Building release artifact
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository: /path/to/quickstart_agent-augmented-development
Version: 1.0.0
Profile: full
Output directory: output/releases

✓ Repository structure validated
✓ Framework core assembled (287 files)
✓ Manifest generated (META/MANIFEST.yml)
✓ Metadata created (META/metadata.json)
✓ Release artifact created: quickstart-framework-1.0.0.zip
✓ Checksums generated: checksums.txt

📦 Release ready: output/releases/quickstart-framework-1.0.0.zip

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Advanced Build Options

```bash
# Specify output directory
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --output-dir /path/to/releases

# Use different profile
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --profile minimal

# Dry run (validate without creating files)
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --dry-run

# Build from different repository location
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --repo-root /path/to/other/repo
```

### Version Format

The `--version` parameter follows semantic versioning (semver):

**Release versions:**
```bash
--version 1.0.0        # Major.Minor.Patch
--version 2.5.13       # Standard release
```

**Pre-release versions:**
```bash
--version 1.0.0-alpha.1    # Alpha release
--version 1.0.0-beta.2     # Beta release
--version 1.0.0-rc.1       # Release candidate
```

**Build metadata:**
```bash
--version 1.0.0+20260131   # With build date
--version 1.0.0+abc123     # With git commit
```

> **Note:** Don't include a 'v' prefix—use `1.0.0`, not `v1.0.0`.

### CI/CD Integration

The framework includes a GitHub Actions workflow for automated releases:

**.github/workflows/release-packaging.yml**

**Triggers:**
- Git tags matching `v*` (e.g., `v1.0.0`)
- Manual workflow dispatch
- Pull requests (dry-run validation)

**To create a release via CI/CD:**

```bash
# Tag the release
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will:
# 1. Build the release artifact
# 2. Run validation tests
# 3. Create a GitHub Release
# 4. Upload the .zip artifact
# 5. Generate release notes
```

**To trigger manually:**

1. Go to GitHub Actions tab
2. Select "Release Packaging" workflow
3. Click "Run workflow"
4. Enter version and options
5. Click "Run workflow"

## Artifact Structure

Understanding what's inside a release artifact helps with troubleshooting and customization.

### Zip File Layout

```
quickstart-framework-1.0.0.zip
├── framework_core/              # ← This is what gets installed
│   ├── .github/
│   │   └── agents/
│   │       ├── devops-danny.agent.md
│   │       ├── editor-eddy.agent.md
│   │       ├── directives/
│   │       └── ...
│   ├── docs/
│   │   ├── templates/
│   │   │   ├── ADR_TEMPLATE.md
│   │   │   └── ...
│   │   └── architecture/
│   │       ├── adrs/
│   │       └── design/
│   ├── framework/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   └── ...
│   ├── validation/
│   ├── work/
│   │   └── templates/
│   ├── AGENTS.md
│   ├── README.md
│   └── ...
├── scripts/                     # ← Installation scripts
│   ├── framework_install.sh
│   ├── framework_upgrade.sh
│   └── README.md
└── META/                        # ← Release metadata
    ├── MANIFEST.yml
    ├── metadata.json
    ├── RELEASE_NOTES.md
    └── checksums.txt
```

### framework_core/

This directory contains everything that will be copied to your project during installation. It's the actual framework content.

**Why separate?** So the installation script can cleanly copy `framework_core/*` to your target directory without including the scripts or metadata.

### scripts/

Standalone installation and upgrade scripts. These are not installed into your project—they're used to perform the installation.

### META/

Release metadata for verification, auditing, and Framework Guardian integration.

## Exclusion Rules

Certain files and directories are **never** included in releases. This keeps artifacts clean and secure.

### Version Control
```
.git/
.gitignore
.gitattributes
```
**Why:** Git history and configuration are specific to the source repository, not relevant to downstream installations.

### Python Cache
```
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.coverage
*.egg-info/
```
**Why:** Generated files that should be rebuilt in the target environment.

### Work Artifacts
```
work/logs/
work/reports/
work/collaboration/
work/notes/
work/analysis/
work/articles/
work/planning/
```
**Why:** These are outputs from using the framework, not part of the framework itself. Each installation creates its own work artifacts.

### Local Overrides
```
local/
local/**
```
**Why:** The `local/` directory is for project-specific customizations. It's never distributed—each project maintains its own local overrides.

### Temporary Files
```
tmp/
output/
*.tmp
*.bak
*.swp
.framework-new
```
**Why:** Temporary and backup files are transient artifacts that shouldn't be distributed.

### IDE Files
```
.vscode/
.idea/
*.iml
```
**Why:** Editor configurations are personal preferences, not framework content.

### Build Artifacts
```
dist/
build/
node_modules/
```
**Why:** Generated outputs that should be rebuilt as needed.

### Custom Exclusions

If you're building a custom distribution, you can modify exclusion patterns:

1. Edit `ops/release/distribution-config.yaml`
2. Add patterns to the `exclusions` section
3. Rebuild the release

```yaml
exclusions:
  custom:
    - "my-secret-files/*"
    - "*.private"
```

## Verification

After building or downloading a release, verify its integrity.

### Checksum Verification

Every release includes a `checksums.txt` file:

```bash
# Verify the zip file integrity
sha256sum -c checksums.txt

# Expected output:
# quickstart-framework-1.0.0.zip: OK
```

On macOS:
```bash
shasum -a 256 -c checksums.txt
```

### Manifest Inspection

The manifest lists every file with its checksum:

```bash
# Extract the artifact
unzip quickstart-framework-1.0.0.zip

# View the manifest
cat quickstart-framework-1.0.0/META/MANIFEST.yml
```

**Manifest structure:**
```yaml
version: 1.0.0
generated_at: '2026-01-31T12:00:00Z'
files:
  - path: AGENTS.md
    sha256: abc123...
    mode: '644'
    scope: core
    size: 9266
  # ... more files ...
total_files: 287
total_size: 2953434
```

**Verify a specific file:**
```bash
# Calculate checksum
sha256sum framework_core/AGENTS.md

# Compare with manifest value
grep "AGENTS.md" META/MANIFEST.yml
```

### Metadata Review

Check build metadata:

```bash
cat quickstart-framework-1.0.0/META/metadata.json
```

```json
{
  "version": "1.0.0",
  "build_date": "2026-01-31T12:00:00Z",
  "framework_name": "quickstart-agent-augmented-development",
  "git_commit": "abc123...",
  "git_branch": "main",
  "release_notes_path": "META/RELEASE_NOTES.md"
}
```

This tells you:
- Exact version
- When it was built
- Source git commit (traceability)
- Where to find release notes

## Troubleshooting

### Issue: Invalid repository structure

**Symptom:**
```
❌ Invalid repository structure. Missing directories:
   - .github/agents
   - framework
```

**Causes:**
- Running build script from wrong directory
- Incomplete framework checkout
- Required directories deleted or renamed

**Solutions:**

```bash
# 1. Verify you're in the repository root
pwd
ls -la .github/agents framework

# 2. If not, specify correct location
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --repo-root /correct/path

# 3. Ensure required directories exist
mkdir -p .github/agents framework work/templates
```

### Issue: Invalid version format

**Symptom:**
```
❌ Invalid version format: v1.0.0
```

**Cause:** Including 'v' prefix in version.

**Solution:**
```bash
# ❌ Wrong
python ops/release/build_release_artifact.py --version v1.0.0

# ✅ Correct
python ops/release/build_release_artifact.py --version 1.0.0
```

### Issue: Permission denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: 'output/releases'
```

**Causes:**
- Output directory not writable
- Parent directory doesn't exist
- Insufficient permissions

**Solutions:**

```bash
# 1. Check output directory permissions
ls -ld output/releases

# 2. Create output directory if missing
mkdir -p output/releases

# 3. Use a different output directory
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --output-dir ~/releases

# 4. Fix permissions
chmod 755 output/releases
```

### Issue: Files missing from artifact

**Symptom:** Expected files not in the zip.

**Causes:**
- Files match exclusion patterns
- Files don't exist in source
- Wrong profile selected

**Solutions:**

```bash
# 1. Dry run to see what will be included
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --dry-run

# 2. Check if files exist in source
ls -la path/to/expected/file

# 3. Verify profile selection
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --profile full

# 4. Check exclusion patterns
cat ops/release/distribution-config.yaml | grep -A 20 "exclusions:"
```

### Issue: Artifact too large

**Symptom:** Generated .zip file is unexpectedly large.

**Causes:**
- Including work artifacts
- Python cache files not excluded
- Large binary files in framework

**Solutions:**

```bash
# 1. Check artifact contents
unzip -l quickstart-framework-1.0.0.zip | head -50

# 2. Look for large files
unzip -l quickstart-framework-1.0.0.zip | sort -k4 -n | tail -20

# 3. Verify exclusions are working
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --dry-run | grep -i cache

# 4. Clean repository before building
rm -rf __pycache__ .pytest_cache work/logs work/collaboration
```

## Best Practices

### For Framework Maintainers

**1. Consistent Versioning**

Follow semantic versioning strictly:
- **Major** (1.0.0 → 2.0.0): Breaking changes
- **Minor** (1.0.0 → 1.1.0): New features, backward compatible
- **Patch** (1.0.0 → 1.0.1): Bug fixes

**2. Meaningful Release Notes**

Update `META/RELEASE_NOTES.md` for each release:
```markdown
# Version 1.1.0 - 2026-02-15

## New Features
- Added Framework Guardian agent profile
- New conflict resolution commands

## Improvements
- Faster checksum calculation
- Better error messages

## Bug Fixes
- Fixed path handling on Windows

## Breaking Changes
None
```

**3. Test Before Release**

```bash
# Run acceptance tests
pytest validation/release/ -v

# Build and test installation
python ops/release/build_release_artifact.py --version 0.0.1-test
cd output/releases
unzip quickstart-framework-0.0.1-test.zip
cd quickstart-framework-0.0.1-test
./scripts/framework_install.sh --dry-run . /tmp/test-install
```

**4. Tag Consistently**

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag to trigger CI/CD
git push origin v1.0.0
```

### For Downstream Distributors

**1. Fork with Purpose**

If you're creating a downstream distribution:
- Keep the framework's core intact
- Add your customizations in `local/`
- Document what you've changed
- Maintain upgrade path to upstream

**2. Custom Profiles**

Create organization-specific profiles:

```yaml
# ops/release/distribution-config-custom.yaml
profiles:
  corporate:
    description: "Corporate standard framework"
    include:
      core_directories: all
      export_directories: [".claude"]  # Only Claude
      root_files: all
      scripts: all
```

```bash
# Build with custom config
python ops/release/build_release_artifact.py \
    --version 1.0.0-corp \
    --config ops/release/distribution-config-custom.yaml \
    --profile corporate
```

**3. Internal Distribution**

For internal distribution within an organization:

```bash
# Build release
python ops/release/build_release_artifact.py --version 1.0.0-internal

# Host on internal artifact server
aws s3 cp output/releases/quickstart-framework-1.0.0-internal.zip \
    s3://our-artifacts/framework/

# Or use internal package registry
# ... organization-specific distribution ...
```

### For End Users

**1. Verify Before Installing**

Always verify checksums:
```bash
sha256sum -c checksums.txt
```

**2. Read Release Notes**

Before upgrading, review what's changed:
```bash
unzip -p quickstart-framework-1.1.0.zip \
    META/RELEASE_NOTES.md | less
```

**3. Keep Distribution Artifacts**

Save the .zip files you install from:
```bash
mkdir -p ~/framework-releases
cp quickstart-framework-*.zip ~/framework-releases/
```

This helps with rollbacks and troubleshooting.

## Related Documentation

- **[Installation Guide](USER_GUIDE_installation.md)** - How to install the framework
- **[Upgrade Guide](USER_GUIDE_upgrade.md)** - How to upgrade existing installations
- **[Getting Started](quickstart/GETTING_STARTED.md)** - Quick start guide
- **[ADR-013](architecture/adrs/ADR-013-zip-distribution.md)** - Distribution architecture decision
- **[Release README](../ops/release/README.md)** - Technical build documentation

## Support

Questions about distribution?

1. Check this guide and troubleshooting section
2. Review release packaging README: `ops/release/README.md`
3. Examine distribution configuration: `ops/release/distribution-config.yaml`
4. Search existing issues in repository
5. Create a new issue with:
   - Build command used
   - Error messages
   - Output of `--dry-run`
   - Profile selected

---

**Last Updated:** 2026-01-31  
**Document Version:** 1.0.0  
**Framework Version:** 1.0.0+
