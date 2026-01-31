# Framework Installation and Upgrade Guide

## Overview

This guide explains how to install and upgrade the Quickstart Agent-Augmented Development Framework in your repository.

The framework distribution follows **ADR-013** (Zip-Based Framework Distribution) and **ADR-014** (Framework Guardian Agent) to provide safe, reproducible installations and upgrades without overwriting local customizations.

## Table of Contents

- [Installation](#installation)
- [Upgrade](#upgrade)
- [Conflict Resolution](#conflict-resolution)
- [Framework Guardian Integration](#framework-guardian-integration)
- [Troubleshooting](#troubleshooting)
- [Reference](#reference)

## Installation

### Prerequisites

- POSIX-compliant shell (bash, sh, zsh, etc.)
- Standard Unix utilities: `find`, `cp`, `sha256sum` or `shasum`, `date`
- Framework release artifact (`.zip` file)

### Installation Steps

#### 1. Download and Extract Release

```bash
# Download the release artifact (example)
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.0.0/quickstart-framework-1.0.0.zip

# Extract the archive
unzip quickstart-framework-1.0.0.zip
cd quickstart-framework-1.0.0
```

#### 2. Run Installation Script

**Basic Installation:**

```bash
# Install into current directory
./scripts/framework_install.sh . /path/to/your/repo

# Or install into specific directory
./scripts/framework_install.sh . ~/projects/my-agent-repo
```

**Dry Run (Preview Installation):**

```bash
# See what would be installed without making changes
./scripts/framework_install.sh --dry-run . /path/to/your/repo
```

**Verbose Output:**

```bash
# Get detailed output about each file
./scripts/framework_install.sh --verbose . /path/to/your/repo
```

#### 3. Verify Installation

After installation, verify the framework metadata file was created:

```bash
cat .framework_meta.yml
```

Expected output:

```yaml
framework_version: 1.0.0
installed_at: 2026-01-31T12:00:00Z
source_release: quickstart-framework-1.0.0
installer_version: 1.0.0
```

### What Gets Installed

The installation script copies files from `framework_core/` to your repository:

```
.github/
  agents/          # Agent profiles and directives
docs/
  templates/       # Document templates
  architecture/    # Architecture docs and ADRs
framework/         # Core Python framework
validation/        # Validation scripts and tests
work/
  templates/       # Work item templates
AGENTS.md          # Agent coordination protocol
README.md          # Framework documentation
pyproject.toml     # Python project config
requirements.txt   # Python dependencies
```

### Installation Behavior

- **NEW Files**: Files that don't exist in the target are copied
- **EXISTING Files**: Files that already exist are **NEVER overwritten**
- **Metadata**: Creates `.framework_meta.yml` to track installation

The installation script will report:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework Installation Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results:
  NEW:      250 files
  SKIPPED:  15 files (already exist)

✓ Installation completed successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Upgrade

### Prerequisites

- Existing framework installation (`.framework_meta.yml` must exist)
- New release artifact (`.zip` file)

### Upgrade Steps

#### 1. Extract New Release

```bash
# Download and extract new version
unzip quickstart-framework-1.1.0.zip
cd quickstart-framework-1.1.0
```

#### 2. Run Upgrade Script

**Preview Upgrade (Dry Run):**

```bash
# See what would change without making modifications
./scripts/framework_upgrade.sh --dry-run . /path/to/your/repo
```

**Perform Upgrade:**

```bash
# Execute the upgrade
./scripts/framework_upgrade.sh . /path/to/your/repo
```

**Generate Plan for Framework Guardian:**

```bash
# Create upgrade plan for automated conflict analysis
./scripts/framework_upgrade.sh --plan . /path/to/your/repo
```

**Additional Options:**

```bash
# Verbose mode for detailed output
./scripts/framework_upgrade.sh --verbose . /path/to/your/repo

# Skip backup file creation (not recommended)
./scripts/framework_upgrade.sh --no-backup . /path/to/your/repo
```

#### 3. Review Upgrade Report

The upgrade script generates `upgrade-report.txt`:

```bash
cat upgrade-report.txt
```

### Upgrade Behavior

The upgrade script intelligently handles different file states:

| Status | Description | Action |
|--------|-------------|--------|
| **NEW** | File missing in target | Copied from release |
| **UNCHANGED** | Checksum matches release | No action (skip) |
| **CONFLICT** | File differs from release | Creates `.framework-new` file |
| **PROTECTED** | File in `local/` directory | Never modified |

### Example Upgrade Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework Upgrade Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results:
  NEW:        12 files
  UNCHANGED:  230 files
  CONFLICT:   8 files
  PROTECTED:  3 files

⚡ Manual conflict resolution required for 8 files
   Review .framework-new files and merge changes manually
   See upgrade-report.txt for details

✓ Upgrade completed successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Conflict Resolution

When the upgrade script detects a file conflict (your version differs from the new release), it:

1. **Preserves your original file** (no modifications)
2. **Creates a `.framework-new` file** with the new version
3. **Creates a `.bak.TIMESTAMP` backup** (unless `--no-backup` used)

### Finding Conflicts

```bash
# List all conflict files
find . -name "*.framework-new" -type f

# Count conflicts
find . -name "*.framework-new" -type f | wc -l
```

### Manual Conflict Resolution

For each `.framework-new` file:

1. **Review the conflict:**
   ```bash
   # Compare versions
   diff .github/agents/devops-danny.agent.md \
        .github/agents/devops-danny.agent.md.framework-new
   ```

2. **Choose resolution strategy:**

   **Option A: Accept new version (replace)**
   ```bash
   mv .github/agents/devops-danny.agent.md.framework-new \
      .github/agents/devops-danny.agent.md
   ```

   **Option B: Keep current version (discard new)**
   ```bash
   rm .github/agents/devops-danny.agent.md.framework-new
   ```

   **Option C: Manual merge**
   ```bash
   # Use your preferred merge tool
   vimdiff .github/agents/devops-danny.agent.md \
           .github/agents/devops-danny.agent.md.framework-new
   
   # After merging, remove .framework-new
   rm .github/agents/devops-danny.agent.md.framework-new
   ```

3. **Verify resolution:**
   ```bash
   # Ensure no .framework-new files remain
   find . -name "*.framework-new" -type f
   ```

### Backup Files

If backups were created (`.bak.TIMESTAMP`), you can:

```bash
# List all backups
find . -name "*.bak.*" -type f

# Restore from backup if needed
cp .github/agents/devops-danny.agent.md.bak.20260131_120000 \
   .github/agents/devops-danny.agent.md

# Clean up old backups (after verification)
find . -name "*.bak.*" -type f -delete
```

## Framework Guardian Integration

The **Framework Guardian** agent (ADR-014) provides automated conflict analysis and merge recommendations.

### Using Framework Guardian

#### Audit Mode

Analyze your installation for drift and inconsistencies:

```bash
# Run Guardian in audit mode (future implementation)
# This will generate validation/FRAMEWORK_AUDIT_REPORT.md
```

The audit report will show:
- Files missing from framework
- Files with unexpected modifications
- Recommended actions

#### Upgrade Mode

Get automated merge recommendations after an upgrade:

```bash
# Run Guardian in upgrade mode (future implementation)
# This will generate validation/FRAMEWORK_UPGRADE_PLAN.md
```

The upgrade plan will provide:
- Per-file conflict analysis
- Auto-merge candidates
- Manual merge guidance
- Recommendations for moving customizations to `local/`

### Guardian Outputs

**Audit Report** (`validation/FRAMEWORK_AUDIT_REPORT.md`):
- Installation status
- File inventory comparison
- Drift analysis
- Compliance recommendations

**Upgrade Plan** (`validation/FRAMEWORK_UPGRADE_PLAN.md`):
- Conflict classification
- Merge strategies
- Step-by-step resolution guide
- TODO items for humans

## Troubleshooting

### Installation Issues

#### Error: "No existing framework installation found"

**Problem:** Running upgrade script on a repository without framework installed.

**Solution:** Use `framework_install.sh` for first-time installation:
```bash
./scripts/framework_install.sh . /path/to/repo
```

#### Error: "Invalid release artifact structure"

**Problem:** Missing required directories or files in release artifact.

**Solution:** Verify the extracted release contains:
- `framework_core/`
- `scripts/`
- `META/MANIFEST.yml`

Re-extract the zip file or download a fresh copy.

#### Warning: "Framework appears to be already installed"

**Problem:** `.framework_meta.yml` already exists during installation.

**Solution:** Use upgrade script instead:
```bash
./scripts/framework_upgrade.sh . /path/to/repo
```

### Upgrade Issues

#### Error: "Neither sha256sum nor shasum found"

**Problem:** Missing checksum utility.

**Solution:**
- **Linux:** Install `coreutils`: `sudo apt install coreutils`
- **macOS:** Should have `shasum` by default
- **Windows/WSL:** Install `coreutils` in WSL

#### Files in `local/` Were Modified

**Problem:** Upgrade script should never modify `local/` but changes detected.

**Solution:**
- Verify you're using the latest version of upgrade script
- Check `upgrade-report.txt` for PROTECTED entries
- File a bug report if `local/` files were actually modified

#### Too Many Conflicts

**Problem:** Large number of conflicts after upgrade.

**Solution:**
1. Review conflicts in `upgrade-report.txt`
2. Use Framework Guardian for automated analysis
3. Consider if customizations should move to `local/` directory
4. Merge common conflicts first (e.g., config files)
5. Use `diff` or merge tools to understand changes

### Permission Issues

#### Error: "Permission denied"

**Problem:** Insufficient permissions to write files.

**Solution:**
```bash
# Ensure you have write permissions
ls -la /path/to/repo

# Run with appropriate permissions
sudo ./scripts/framework_install.sh . /path/to/repo
```

### Recovery

#### Rollback Installation

If installation fails or causes issues:

```bash
# Remove installed files (carefully!)
# Review what was installed first
./scripts/framework_install.sh --dry-run . /path/to/repo

# Remove .framework_meta.yml
rm .framework_meta.yml

# Manually remove installed files or restore from backup
git restore .  # if using Git
```

#### Rollback Upgrade

If upgrade causes issues:

```bash
# 1. Restore from backups
find . -name "*.bak.*" -type f | while read backup; do
    original="${backup%.bak.*}"
    cp "$backup" "$original"
done

# 2. Remove .framework-new files
find . -name "*.framework-new" -type f -delete

# 3. Restore old .framework_meta.yml
if [ -f .framework_meta.yml.backup ]; then
    mv .framework_meta.yml.backup .framework_meta.yml
fi

# 4. Verify state
cat .framework_meta.yml
```

## Reference

### Script Options

#### framework_install.sh

```
Usage: framework_install.sh [OPTIONS] RELEASE_DIR TARGET_DIR

Options:
  --dry-run      Preview installation without changes
  --verbose      Detailed output for each file
  --help         Display help message
  --version      Display script version
```

#### framework_upgrade.sh

```
Usage: framework_upgrade.sh [OPTIONS] RELEASE_DIR TARGET_DIR

Options:
  --dry-run      Preview upgrade without changes
  --plan         Generate upgrade plan for Guardian
  --verbose      Detailed output for each file
  --no-backup    Skip backup file creation
  --help         Display help message
  --version      Display script version
```

### File Status Definitions

| Status | Install | Upgrade | Description |
|--------|---------|---------|-------------|
| **NEW** | ✓ | ✓ | File copied to target |
| **SKIPPED** | ✓ | - | File already exists (install) |
| **UNCHANGED** | - | ✓ | Checksum matches (upgrade) |
| **CONFLICT** | - | ✓ | File differs, .framework-new created |
| **PROTECTED** | - | ✓ | File in local/, never touched |
| **ERROR** | ✓ | ✓ | Operation failed |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid arguments or missing directories |
| 2 | Invalid artifact structure or missing installation |
| 3 | Operation failed |

### Related Documentation

- **ADR-013**: [Zip-Based Framework Distribution](../architecture/adrs/ADR-013-zip-distribution.md)
- **ADR-014**: [Framework Guardian Agent](../architecture/adrs/ADR-014-framework-guardian-agent.md)
- **Technical Design**: [Distribution Technical Design](../architecture/design/distribution_of_releases_technical_design.md)
- **Release Packaging**: [ops/release/README.md](../../ops/release/README.md)
- **Framework Guardian**: `.github/agents/framework-guardian.agent.md` *(future)*

### Best Practices

1. **Always dry-run first**: Use `--dry-run` to preview changes
2. **Keep backups enabled**: Don't use `--no-backup` unless necessary
3. **Review upgrade reports**: Read `upgrade-report.txt` carefully
4. **Use Framework Guardian**: Let automation help with conflicts
5. **Protect customizations**: Put project-specific files in `local/`
6. **Test after upgrade**: Verify framework functions correctly
7. **Version control**: Commit before and after upgrades
8. **Document local changes**: Note customizations for future reference

### Support

For issues or questions:

1. Check this documentation and troubleshooting section
2. Review referenced ADRs and technical design documents
3. Consult Framework Guardian agent for upgrade conflicts
4. Search existing issues in the repository
5. Create a new issue with:
   - Script version (use `--version`)
   - Operating system and shell
   - Complete error messages
   - Relevant portions of upgrade-report.txt
   - Steps to reproduce

## Examples

### Example 1: Fresh Installation

```bash
# Extract release
unzip quickstart-framework-1.0.0.zip
cd quickstart-framework-1.0.0

# Preview installation
./scripts/framework_install.sh --dry-run . ~/my-project

# If preview looks good, install
./scripts/framework_install.sh . ~/my-project

# Verify
cat ~/my-project/.framework_meta.yml
```

### Example 2: Standard Upgrade

```bash
# Extract new release
unzip quickstart-framework-1.1.0.zip
cd quickstart-framework-1.1.0

# Preview upgrade
./scripts/framework_upgrade.sh --dry-run . ~/my-project

# Perform upgrade
./scripts/framework_upgrade.sh --verbose . ~/my-project

# Review results
cat ~/my-project/upgrade-report.txt

# Resolve conflicts
find ~/my-project -name "*.framework-new" -type f
```

### Example 3: Automated Upgrade with Guardian

```bash
# 1. Upgrade with plan generation
./scripts/framework_upgrade.sh --plan . ~/my-project

# 2. Run Framework Guardian (future)
# This will analyze conflicts and generate recommendations

# 3. Review Guardian outputs
# cat ~/my-project/validation/FRAMEWORK_UPGRADE_PLAN.md

# 4. Apply recommended merges
# Follow Guardian's step-by-step instructions

# 5. Verify completion
find ~/my-project -name "*.framework-new" -type f  # Should be empty
```

---

**Last Updated:** 2026-01-31  
**Document Version:** 1.0.0  
**Framework Version:** 1.0.0+
