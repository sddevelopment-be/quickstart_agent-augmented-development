# Framework Upgrade Guide

This guide explains how to safely upgrade your framework installation to a new version.

## Prerequisites

- Existing framework installation (see [Installation Guide](framework-installation.md))
- Framework release package for the new version
- Backup of your project (recommended)
- Basic command-line knowledge

## Overview

The upgrade process:
1. **Download** new framework version
2. **Dry-run** to preview changes
3. **Review** upgrade report
4. **Apply** upgrade
5. **Resolve** conflicts (if any)
6. **Validate** with Framework Guardian
7. **Test** your project
8. **Commit** changes

## Quick Start

```bash
# Download and extract new version
unzip quickstart-framework-1.1.0.zip
cd quickstart-framework-1.1.0

# Dry-run to preview
./scripts/framework_upgrade.sh --dry-run /path/to/your/project

# Review report
cat /path/to/your/project/framework-upgrade-report.txt

# Apply upgrade
./scripts/framework_upgrade.sh /path/to/your/project

# Resolve conflicts (if any)
# Review .framework-new files and decide

# Validate
cd /path/to/your/project
python3 work/scripts/framework_guardian.py --mode audit --target .

# Commit
git add .
git commit -m "Upgrade framework to v1.1.0"
```

## Detailed Steps

### 1. Backup Your Project

**Always backup before upgrading:**

```bash
# Option 1: Git branch
cd /path/to/your/project
git checkout -b backup-before-upgrade-v1.1.0
git commit -am "Backup before framework upgrade"
git checkout main  # or your working branch

# Option 2: Directory copy
cp -r /path/to/your/project /path/to/your/project.backup
```

### 2. Download New Version

```bash
# Download from GitHub Releases
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.1.0/quickstart-framework-1.1.0.zip

# Extract
unzip quickstart-framework-1.1.0.zip
cd quickstart-framework-1.1.0

# Verify contents
ls -la
# Should see: framework_core/, scripts/, META/
```

### 3. Dry-Run Preview

**Always run dry-run first:**

```bash
# Preview changes without modifying files
./scripts/framework_upgrade.sh --dry-run /path/to/your/project
```

**What dry-run does:**
- Analyzes all files
- Reports what would change
- Classifies: NEW, UNCHANGED, CONFLICT
- Does NOT modify any files
- Does NOT create .framework-new files
- Does NOT update metadata

**Review the output:**
```
📦 Analyzing upgrade...
  🆕 NEW: docs/templates/new-template.md
  ✅ UNCHANGED: .github/agents/architect.agent.md
  ⚠️  CONFLICT: .github/agents/custom-agent.agent.md
```

### 4. Review Upgrade Report

```bash
# Read detailed report
cat /path/to/your/project/framework-upgrade-report.txt
```

**Report shows:**
- Current vs new version
- Files added (NEW)
- Files unchanged (UNCHANGED)
- Files with conflicts (CONFLICT)
- Statistics summary

**Example report:**
```
Framework Upgrade Report
Generated: 2025-11-24 21:00:00 UTC
Current Version: 1.0.0
New Version: 1.1.0
Mode: DRY-RUN

Status Summary:
NEW: docs/templates/new-template.md
UNCHANGED: .github/agents/architect.agent.md
CONFLICT: .github/agents/custom-agent.agent.md

Upgrade Statistics:
- Files added (NEW): 5
- Files unchanged (UNCHANGED): 87
- Files with conflicts (CONFLICT): 3
```

### 5. Apply Upgrade

**If dry-run looks good, apply:**

```bash
# Run upgrade (without --dry-run)
./scripts/framework_upgrade.sh /path/to/your/project
```

**What this does:**
- Adds NEW files
- Skips UNCHANGED files
- Creates `.framework-new` for CONFLICT files
- Creates `.bak` backups of conflicted files
- Updates `.framework_meta.yml`
- Generates final report

**Output shows real-time progress:**
```
🔄 Framework Upgrade Script
Target: /path/to/your/project
Source: /path/to/package

Current version: 1.0.0
New version: 1.1.0

📦 Analyzing upgrade...
  🆕 NEW: docs/templates/new-template.md
  ✅ UNCHANGED: .github/agents/architect.agent.md
  ⚠️  CONFLICT: .github/agents/custom-agent.agent.md
    Backup: custom-agent.agent.md.bak.20251124210000
    New version: custom-agent.agent.md.framework-new

📝 Updating framework metadata...
✅ Updated: .framework_meta.yml

📊 Upgrade Summary:
  🆕 NEW: 5 files
  ✅ UNCHANGED: 87 files
  ⚠️  CONFLICT: 3 files
```

### 6. Resolve Conflicts

**If conflicts are detected:**

```bash
# Find all .framework-new files
cd /path/to/your/project
find . -name "*.framework-new" -type f
```

**For each conflict:**

1. **Review both versions:**
   ```bash
   # Your current version
   cat .github/agents/custom-agent.agent.md
   
   # Framework's new version
   cat .github/agents/custom-agent.agent.md.framework-new
   
   # See differences
   diff .github/agents/custom-agent.agent.md .github/agents/custom-agent.agent.md.framework-new
   ```

2. **Decide resolution strategy:**

   **Option A: Accept framework version**
   ```bash
   # Replace with framework version
   mv .github/agents/custom-agent.agent.md.framework-new .github/agents/custom-agent.agent.md
   ```

   **Option B: Keep your customization**
   ```bash
   # Keep your version, delete framework version
   rm .github/agents/custom-agent.agent.md.framework-new
   ```

   **Option C: Merge changes manually**
   ```bash
   # Edit to combine both
   vi .github/agents/custom-agent.agent.md
   # Incorporate relevant framework changes
   # Keep your customizations
   rm .github/agents/custom-agent.agent.md.framework-new
   ```

   **Option D: Move customization to local/**
   ```bash
   # Best practice for customizations
   mkdir -p local/agents
   mv .github/agents/custom-agent.agent.md local/agents/
   mv .github/agents/custom-agent.agent.md.framework-new .github/agents/custom-agent.agent.md
   ```

3. **Get assistance from Framework Guardian:**
   ```bash
   python3 work/scripts/framework_guardian.py --mode upgrade --target . --release 1.1.0
   cat validation/FRAMEWORK_UPGRADE_PLAN.md
   ```

### 7. Validate Installation

**Run post-upgrade audit:**

```bash
cd /path/to/your/project

# Run Guardian audit
python3 work/scripts/framework_guardian.py --mode audit --target .

# Review audit report
cat validation/FRAMEWORK_AUDIT_REPORT.md

# Verify no .framework-new files remain
find . -name "*.framework-new" -type f
# Should return nothing
```

### 8. Test Your Project

**Before committing:**

```bash
# Run your project's tests (if applicable)
npm test  # or your test command

# Verify functionality
# Test critical workflows
# Check integrations
```

### 9. Commit Changes

```bash
# Review changes
git status
git diff

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Upgrade framework from v1.0.0 to v1.1.0

- Resolved 3 conflicts
- Moved 2 customizations to local/
- All tests passing
- Guardian audit clean

Ref: framework-upgrade-report.txt"

# Push
git push
```

## Upgrade Scenarios

### Scenario 1: Clean Upgrade (No Conflicts)

**Symptoms:**
- No `.framework-new` files
- All files NEW or UNCHANGED
- Report shows 0 conflicts

**Action:**
```bash
# Just commit and push
git add .
git commit -m "Upgrade framework to v1.1.0 - no conflicts"
git push
```

### Scenario 2: Minor Conflicts

**Symptoms:**
- 1-5 `.framework-new` files
- Known customizations
- Low complexity

**Action:**
```bash
# Resolve each conflict individually
# Accept framework version or keep customization
# Run audit
# Commit
```

### Scenario 3: Major Conflicts

**Symptoms:**
- Many `.framework-new` files
- Complex customizations
- Unsure of correct resolution

**Action:**
```bash
# Use Framework Guardian
python3 work/scripts/framework_guardian.py --mode upgrade --target .

# Review comprehensive upgrade plan
cat validation/FRAMEWORK_UPGRADE_PLAN.md

# Follow step-by-step guidance
# Consider moving customizations to local/
```

## Troubleshooting

### Upgrade Fails - No Existing Installation

**Problem:**
```
❌ Error: No framework installation found
```

**Solution:**
```bash
# Check for .framework_meta.yml
ls -la .framework_meta.yml

# If missing, this is a new installation
# Use framework_install.sh instead
./scripts/framework_install.sh /path/to/project
```

### Too Many Conflicts

**Problem:** Dozens of `.framework-new` files

**Cause:** Extensive local customizations mixed with core files

**Solution:**
```bash
# Adopt local/ directory pattern
mkdir -p local/agents local/guidelines local/directives

# Move customizations
mv .github/agents/my-custom-*.agent.md local/agents/

# Accept framework versions
find . -name "*.framework-new" | while read f; do
  mv "$f" "${f%.framework-new}"
done

# Re-run upgrade from scratch if needed
```

### Backup Files Accumulating

**Problem:** Many `.bak.*` files

**Solution:**
```bash
# After confirming upgrade works
find . -name "*.bak.*" -type f -delete

# Or keep for safety until next successful commit
```

### Can't Find .framework-new Files

**Problem:** Conflicts reported but no `.framework-new` files

**Cause:** Ran in dry-run mode

**Solution:**
```bash
# Run without --dry-run
./scripts/framework_upgrade.sh /path/to/project
```

## Best Practices

1. **Always Backup** - Create git branch or directory copy
2. **Always Dry-Run** - Preview before applying
3. **Read Release Notes** - Check META/RELEASE_NOTES.md
4. **Check Breaking Changes** - Review META/UPGRADE_NOTES.md
5. **Resolve All Conflicts** - Don't leave `.framework-new` files
6. **Use local/ Directory** - Keep customizations separate
7. **Run Guardian** - Get automated conflict analysis
8. **Test Before Commit** - Verify everything works
9. **Audit Post-Upgrade** - Confirm clean installation
10. **Document Decisions** - Note why you kept customizations

## Rollback

**If upgrade causes issues:**

### Option 1: Git Revert

```bash
# Undo the upgrade commit
git revert HEAD

# Or reset to backup branch
git reset --hard backup-before-upgrade-v1.1.0
```

### Option 2: Restore from Backup

```bash
# From directory backup
rm -rf /path/to/your/project
cp -r /path/to/your/project.backup /path/to/your/project
```

### Option 3: Manual Rollback

```bash
# Use .bak files
find . -name "*.bak.*" | while read backup; do
  original="${backup%.bak.*}"
  mv "$backup" "$original"
done

# Restore old metadata
# Edit .framework_meta.yml back to old version
```

## Related Documentation

- [Installation Guide](framework-installation.md) - First-time installation
- [Release Process](release-process.md) - How releases are created
- [Framework Guardian Guide](framework-guardian.md) - Automated assistance
- [ADR-013: Zip-Based Distribution](../architecture/adrs/ADR-013-zip-distribution.md)
- [Technical Design](../architecture/design/distribution_of_releases_technical_design.md)

## Support

For upgrade issues:
1. Check this troubleshooting section
2. Review `framework-upgrade-report.txt`
3. Run Framework Guardian for guidance
4. Check `.framework_meta.yml` for version info
5. Open issue with `upgrade` label
