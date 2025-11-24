# Framework Installation Guide

This guide explains how to install the agent-augmented development framework in your repository.

## Prerequisites

- Framework release package (`quickstart-framework-<version>.zip`)
- Target repository (Git repository recommended)
- POSIX-compliant shell (bash, sh, zsh)
- Basic command-line tools: `cp`, `find`, `mkdir`

## Installation Steps

### 1. Download and Extract Package

Download the framework release package from GitHub Releases:

```bash
# Download release
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.0.0/quickstart-framework-1.0.0.zip

# Extract package
unzip quickstart-framework-1.0.0.zip

# Navigate to extracted directory
cd quickstart-framework-1.0.0
```

###  2. Verify Package Contents

Before installation, verify the package structure:

```bash
# List package contents
ls -la

# Expected structure:
# framework_core/  - Core framework files
# scripts/         - Installation and upgrade scripts  
# META/            - Manifest and release notes
```

### 3. Run Installation Script

Install the framework in your target repository:

```bash
# Basic installation (current directory)
./scripts/framework_install.sh .

# Install in specific directory
./scripts/framework_install.sh /path/to/your/repository

# Example
./scripts/framework_install.sh ~/projects/my-app
```

### 4. Review Installation Results

The installer provides immediate feedback:

```
🚀 Framework Installation Script
Target: /path/to/your/repository
Source: /path/to/package

📦 Installing framework files...
  ✅ NEW: .github/agents/architect.agent.md
  ✅ NEW: .github/agents/build-automation.agent.md
  ...
  
📝 Creating framework metadata...
✅ Created: .framework_meta.yml

📊 Installation Summary:
  ✅ NEW: 95 files
  ⏭️  SKIP: 0 files

📄 Report saved: framework-install-report.txt
📄 Metadata saved: .framework_meta.yml

✅ Installation complete!
```

### 5. Review Installed Files

Check what was installed:

```bash
# View metadata
cat .framework_meta.yml

# Review installation report
cat framework-install-report.txt

# List installed agent profiles
ls -l .github/agents/

# Check templates
ls -l docs/templates/
```

### 6. Commit to Version Control

Add the framework files to your repository:

```bash
# Stage framework files
git add .github/agents/
git add docs/directives/
git add docs/guidelines/
git add docs/templates/
git add validation/
git add work/
git add .framework_meta.yml

# Commit
git commit -m "Install agent-augmented development framework v1.0.0"

# Push
git push
```

## Installation Behavior

### Safe Installation

The installation script is designed to be safe:

- **Never overwrites existing files** - If a file already exists, it's skipped
- **Creates parent directories** - Missing directories are created automatically
- **Preserves permissions** - File permissions are maintained
- **Generates reports** - Complete installation log saved to `framework-install-report.txt`
- **Tracks metadata** - Version and installation details in `.framework_meta.yml`

### What Gets Installed

The framework installs:

```
your-repository/
├── .github/agents/              # Agent profiles and directives
├── docs/
│   ├── directives/              # Externalized directives
│   ├── guidelines/              # Operational guidelines
│   ├── templates/               # Document and task templates
│   └── architecture/adrs/       # Architecture Decision Records
├── validation/                  # Validation scripts and schemas
├── work/                        # Work directory scaffolds
│   ├── inbox/                   # Task inbox
│   ├── assigned/                # Assigned tasks
│   ├── done/                    # Completed tasks
│   ├── archive/                 # Archived tasks
│   ├── logs/                    # Agent logs
│   └── collaboration/           # Cross-agent artifacts
├── .framework_meta.yml          # Installation metadata
└── framework-install-report.txt # Installation report
```

### What's NOT Installed

The installer respects local customizations:

- **Existing files** - Never overwritten
- **local/** directories - Not included in framework core
- **Project-specific content** - Your code, configs, docs remain untouched
- **Git history** - Installation adds files, doesn't modify history

## Installation Metadata

The `.framework_meta.yml` file tracks installation details:

```yaml
framework_version: 1.0.0
installed_at: 2025-11-24T20:00:00Z
source_package: quickstart-framework-1.0.0
installation_method: framework_install.sh
target_directory: /path/to/repository

files_installed: 95
files_skipped: 0
files_errored: 0
```

This file is used by:
- **Upgrade script** - To detect version and plan upgrades
- **Framework Guardian** - To audit installation integrity
- **Version tracking** - To know which version is installed

## Troubleshooting

### Already Installed Error

**Problem:** Script reports framework already installed

```
⚠️  Warning: Framework already installed
Meta file found: .framework_meta.yml
To upgrade, use framework_upgrade.sh instead
```

**Solution:** Use the upgrade script instead:
```bash
./scripts/framework_upgrade.sh /path/to/repository
```

### Permission Denied

**Problem:** Permission errors during installation

**Solution:** Ensure write permissions:
```bash
# Check permissions
ls -ld /path/to/repository

# Fix if needed
chmod u+w /path/to/repository
```

### Missing framework_core

**Problem:** `framework_core/ not found in package`

**Solution:** Verify you're running from extracted package:
```bash
# Check current directory
pwd
ls -la

# Should see framework_core/, scripts/, META/
# If not, cd to correct directory
```

### Partial Installation

**Problem:** Some files installed, some skipped

This is normal behavior when files already exist. Check the report:

```bash
cat framework-install-report.txt
```

Files marked `SKIPPED` already existed and were not overwritten.

### Installation Failed with Errors

**Problem:** `ERROR` entries in report

**Solution:**
1. Check `framework-install-report.txt` for specific errors
2. Verify disk space: `df -h`
3. Check file permissions on target directory
4. Ensure no conflicting processes are accessing files
5. Run again - installation is idempotent

## Verification

After installation, verify the framework:

```bash
# Check version
grep "framework_version:" .framework_meta.yml

# Verify agent profiles
ls .github/agents/*.agent.md | wc -l

# Check directives
ls docs/directives/*.md | wc -l

# Validate installation
# (if Framework Guardian is available)
python3 work/scripts/framework_guardian.py --mode audit --target .
```

## Next Steps

After successful installation:

1. **Review Documentation**
   - Read `AGENTS.md` for framework overview
   - Check `docs/guidelines/` for operational guidelines
   - Review agent profiles in `.github/agents/`

2. **Configure for Your Project**
   - Customize agent profiles if needed (in `local/agents/`)
   - Add project-specific templates
   - Configure work directory structure

3. **Start Using the Framework**
   - Create tasks in `work/inbox/`
   - Run orchestrator: `python3 work/scripts/agent_orchestrator.py`
   - See `docs/HOW_TO_USE/` for usage guides

4. **Track Changes**
   - Commit installed framework to version control
   - Document framework adoption in project README
   - Set up CI/CD integration if needed

## Upgrading

When a new framework version is released:

```bash
# Download new version
wget https://github.com/.../quickstart-framework-1.1.0.zip
unzip quickstart-framework-1.1.0.zip
cd quickstart-framework-1.1.0

# Run upgrade script (dry-run first)
./scripts/framework_upgrade.sh --dry-run /path/to/repository

# Review upgrade report
cat /path/to/repository/framework-upgrade-report.txt

# Apply upgrade
./scripts/framework_upgrade.sh /path/to/repository
```

See [Framework Upgrade Guide](framework-upgrades.md) for details.

## Related Documentation

- [Release Process](release-process.md) - How releases are created
- [Framework Upgrade Guide](framework-upgrades.md) - Upgrading existing installations
- [ADR-013: Zip-Based Distribution](../architecture/adrs/ADR-013-zip-distribution.md)
- [Technical Design: Distribution Workflow](../architecture/design/distribution_of_releases_technical_design.md)

## Support

For issues or questions:

1. Check this documentation and troubleshooting section
2. Review `framework-install-report.txt` for details
3. Check `.framework_meta.yml` for installation metadata
4. Open an issue with the `installation` label
