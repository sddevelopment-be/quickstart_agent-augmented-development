# Framework Upgrade Guide

**Complete guide to upgrading your framework installation safely**

This guide explains how to upgrade an existing Quickstart Framework installation to a new version. If you're installing for the first time, see the [Installation Guide](USER_GUIDE_installation.md) instead.

## Table of Contents

- [Overview](#overview)
- [Before You Upgrade](#before-you-upgrade)
- [Upgrade Workflow](#upgrade-workflow)
- [Understanding File States](#understanding-file-states)
- [Conflict Detection](#conflict-detection)
- [Step-by-Step Upgrade](#step-by-step-upgrade)
- [Conflict Resolution](#conflict-resolution)
- [Upgrade Planning](#upgrade-planning)
- [Protected Directories](#protected-directories)
- [Backup and Rollback](#backup-and-rollback)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

### What Happens During an Upgrade

The framework upgrade process is designed to be **safe and transparent**:

1. **Detects** which files have changed since your installation
2. **Preserves** your modifications—never overwrites without asking
3. **Creates** `.framework-new` files for conflicts
4. **Protects** your `local/` directory completely
5. **Reports** exactly what happened

Think of it like a smart merge tool that respects your work while bringing in new framework features.

### Safety Mechanisms

The upgrade script has multiple safety features:

- ✅ **Checksums** - Detects file changes precisely
- ✅ **Conflict markers** - `.framework-new` files for manual review
- ✅ **Backups** - `.bak.TIMESTAMP` files for rollback
- ✅ **Dry-run mode** - Preview before committing
- ✅ **Protected zones** - `local/` never touched
- ✅ **Detailed reporting** - `upgrade-report.txt` documents everything

### Upgrade Philosophy

**You're always in control.** The upgrade script:
- Never overwrites your modifications
- Always gives you the new version (as `.framework-new`)
- Lets you decide how to merge changes
- Tracks everything in a detailed report

## Before You Upgrade

### Check Current Installation

Verify you have an existing framework installation:

```bash
# Check for metadata file
cat .framework_meta.yml
```

**Expected output:**
```yaml
framework_version: 1.0.0
installed_at: 2026-01-31T10:15:30Z
source_release: quickstart-framework-1.0.0
installer_version: 1.0.0
```

If this file doesn't exist, you need to [install](USER_GUIDE_installation.md), not upgrade.

### Review What's New

Before upgrading, check the release notes:

```bash
# Download and extract new release
wget <url>/quickstart-framework-1.1.0.zip
unzip quickstart-framework-1.1.0.zip

# Read release notes
cat quickstart-framework-1.1.0/META/RELEASE_NOTES.md | less
```

Look for:
- **Breaking changes** - Do you need to adapt your workflows?
- **New features** - What capabilities are added?
- **Deprecations** - Is anything being removed?
- **Required actions** - Do you need to do anything post-upgrade?

### Prepare Your Repository

**Clean working state:**

```bash
# Commit or stash pending changes
git status

# Ensure clean state
git stash  # Or commit your work

# Optional but recommended: Create a pre-upgrade tag
git tag pre-upgrade-$(date +%Y%m%d)
```

**Backup your local customizations:**

```bash
# Backup local/ directory
tar czf local-backup-$(date +%Y%m%d).tar.gz local/

# Backup any customized framework files
find .github/agents -name "*.agent.md" -type f -exec tar czf custom-agents-backup.tar.gz {} +
```

### Understand Your Customizations

Know what you've changed:

```bash
# Find files you've modified (if using git)
git status .github/agents docs/templates work/templates

# Compare with known framework files
# (Manual review of what you've customized)
```

Common customizations:
- Agent profiles with team-specific instructions
- Templates adapted to your documentation style
- Workflows modified for your process

**Tip:** Keep notes about your customizations. It'll help during conflict resolution.

## Upgrade Workflow

The upgrade process follows these stages:

```
┌─────────────────┐
│ 1. Download     │  Get new release artifact
│    New Release  │  
└────────┬────────┘
         │
┌────────▼────────┐
│ 2. Dry Run      │  Preview what would change
│                 │  
└────────┬────────┘
         │
┌────────▼────────┐
│ 3. Run Upgrade  │  Execute the upgrade
│                 │  
└────────┬────────┘
         │
┌────────▼────────┐
│ 4. Review       │  Read upgrade-report.txt
│    Report       │  
└────────┬────────┘
         │
┌────────▼────────┐
│ 5. Resolve      │  Handle conflicts manually
│    Conflicts    │  
└────────┬────────┘
         │
┌────────▼────────┐
│ 6. Verify       │  Test that everything works
│                 │  
└────────┬────────┘
         │
┌────────▼────────┐
│ 7. Clean Up     │  Remove .framework-new files
│                 │  
└─────────────────┘
```

**Time required:** 10-60 minutes depending on conflicts

## Understanding File States

During an upgrade, each file falls into one of these categories:

### NEW (New Files)

**What it means:** File exists in new release but not in your installation.

**What happens:** File is copied to your repository.

**Action required:** None—the file is simply added.

**Example:**
```
✓ NEW: .github/agents/new-agent-profile.agent.md
```

### UNCHANGED (Identical Files)

**What it means:** File exists in both versions and checksums match.

**What happens:** Nothing—file is already up to date.

**Action required:** None—file is skipped.

**Example:**
```
ℹ UNCHANGED: .github/agents/devops-danny.agent.md (skip)
```

### CONFLICT (Modified Files)

**What it means:** File exists in both versions but checksums differ.

**What happens:**
1. Your original file stays untouched
2. New version saved as `.framework-new`
3. Backup created as `.bak.TIMESTAMP` (if `--no-backup` not used)

**Action required:** Review and merge manually.

**Example:**
```
⚡ CONFLICT: .github/agents/editor-eddy.agent.md
   → Created: .github/agents/editor-eddy.agent.md.framework-new
   → Backup: .github/agents/editor-eddy.agent.md.bak.20260131_103000
```

### PROTECTED (Files in local/)

**What it means:** File is in the `local/` directory.

**What happens:** Absolutely nothing—file is never touched.

**Action required:** None—your customizations are safe.

**Example:**
```
🛡 PROTECTED: local/agents/custom-agent.agent.md (skipped)
```

### ERROR (Failed Operations)

**What it means:** Something went wrong copying or processing the file.

**What happens:** Error logged, upgrade continues.

**Action required:** Review error, manually copy file if needed.

**Example:**
```
✗ ERROR: docs/templates/special.md (Permission denied)
```

## Conflict Detection

### How It Works

The upgrade script uses **SHA256 checksums** to detect changes:

1. **Calculate checksum** of file in your installation
2. **Compare** with checksum in new release's manifest
3. **If different** → CONFLICT

This is precise—even a single character change is detected.

### Why Conflicts Happen

**Common reasons:**

**1. Intentional customizations**
```markdown
# You added team-specific instructions to an agent profile
# Framework updated that same agent profile with new directives
```

**2. Framework improvements**
```markdown
# Framework fixed a typo or improved wording
# You haven't changed the file, but the checksum differs
```

**3. Local adaptations**
```markdown
# You modified a template to match your documentation style
# Framework enhanced that template with new sections
```

### Conflict Resolution Strategy

For each conflict, you have three options:

| Option | When to Use | Command |
|--------|-------------|---------|
| **Accept new** | Framework change is better; discard your edits | `mv file.framework-new file` |
| **Keep yours** | Your changes are important; skip framework update | `rm file.framework-new` |
| **Merge both** | Both changes are valuable; combine them | Use diff/merge tool |

## Step-by-Step Upgrade

### Step 1: Download New Release

```bash
# Download new version
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.1.0/quickstart-framework-1.1.0.zip

# Verify integrity (recommended)
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/v1.1.0/checksums.txt
sha256sum -c checksums.txt  # Or shasum -a 256 -c checksums.txt on macOS

# Extract
unzip quickstart-framework-1.1.0.zip
cd quickstart-framework-1.1.0
```

### Step 2: Dry Run (Preview)

**Always dry-run first:**

```bash
./scripts/framework_upgrade.sh --dry-run . /path/to/your/repo
```

**What you'll see:**
```
ℹ Running in DRY RUN mode - no changes will be made
ℹ Validating release artifact structure...
✓ Release artifact structure is valid
ℹ Checking existing installation...
✓ Found existing installation (version 1.0.0)
ℹ Analyzing upgrade path: 1.0.0 → 1.1.0
ℹ Scanning files for changes...

Upgrade Analysis:
  NEW:        15 files would be added
  UNCHANGED:  250 files would be skipped (already up to date)
  CONFLICT:   8 files would create .framework-new
  PROTECTED:  3 files in local/ would be skipped

Conflicts requiring manual resolution:
  .github/agents/editor-eddy.agent.md
  .github/agents/devops-danny.agent.md
  docs/templates/ADR_TEMPLATE.md
  work/templates/TASK_TEMPLATE.md
  framework/core.py
  validation/test_structure.py
  AGENTS.md
  README.md

✓ Dry run completed successfully!
ℹ Run without --dry-run to perform upgrade
```

**Review carefully:**
- Are the conflict files expected?
- Do you understand what changed in each?
- Are you ready to handle the conflicts?

### Step 3: Perform the Upgrade

Once satisfied with the dry run:

```bash
./scripts/framework_upgrade.sh . /path/to/your/repo
```

**Progress output:**
```
ℹ Validating release artifact structure...
✓ Release artifact structure is valid
ℹ Checking existing installation...
✓ Found existing installation (version 1.0.0)
ℹ Upgrading: 1.0.0 → 1.1.0
ℹ Processing files...

Files:
  ✓ NEW: .github/agents/framework-guardian.agent.md
  ✓ NEW: .github/agents/directives/023_conflict_resolution.md
  ℹ UNCHANGED: .github/agents/architect-anna.agent.md (skip)
  ⚡ CONFLICT: .github/agents/editor-eddy.agent.md
     → Created: .github/agents/editor-eddy.agent.md.framework-new
     → Backup: .github/agents/editor-eddy.agent.md.bak.20260131_103000
  ⚡ CONFLICT: docs/templates/ADR_TEMPLATE.md
     → Created: docs/templates/ADR_TEMPLATE.md.framework-new
     → Backup: docs/templates/ADR_TEMPLATE.md.bak.20260131_103000
  ... (progress continues)

ℹ Updating framework metadata...
ℹ Generating upgrade report...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework Upgrade Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results:
  NEW:        15 files
  UNCHANGED:  250 files
  CONFLICT:   8 files
  PROTECTED:  3 files
  ERROR:      0 files

⚡ Manual conflict resolution required for 8 files
   Review .framework-new files and merge changes manually
   See upgrade-report.txt for details

✓ Upgrade completed successfully!

Next Steps:
  1. Review: cat upgrade-report.txt
  2. Find conflicts: find . -name "*.framework-new"
  3. Resolve each conflict manually
  4. Clean up: find . -name "*.framework-new" -delete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4: Review Upgrade Report

The upgrade generates a detailed report:

```bash
cat upgrade-report.txt
```

**Report format:**
```
Framework Upgrade Report
========================

Upgrade: 1.0.0 → 1.1.0
Date: 2026-01-31 10:30:00
Target: /path/to/your/repo

Summary
-------
NEW:        15 files
UNCHANGED:  250 files
CONFLICT:   8 files
PROTECTED:  3 files
ERROR:      0 files

New Files (15)
--------------
✓ .github/agents/framework-guardian.agent.md
✓ .github/agents/directives/023_conflict_resolution.md
✓ docs/architecture/adrs/ADR-015-upgrade-safety.md
... (12 more)

Unchanged Files (250)
---------------------
[Listed in full in report]

Conflicts (8)
-------------
⚡ .github/agents/editor-eddy.agent.md
   Your version: a1b2c3d4e5f6... (modified)
   New version:  f6e5d4c3b2a1...
   Files created:
     - .github/agents/editor-eddy.agent.md.framework-new
     - .github/agents/editor-eddy.agent.md.bak.20260131_103000

⚡ docs/templates/ADR_TEMPLATE.md
   Your version: 123abc456def...
   New version:  def456abc123...
   Files created:
     - docs/templates/ADR_TEMPLATE.md.framework-new
     - docs/templates/ADR_TEMPLATE.md.bak.20260131_103000

... (6 more conflicts)

Protected Files (3)
-------------------
🛡 local/agents/custom-agent.agent.md
🛡 local/templates/custom-template.md
🛡 local/workflows/team-workflow.md

Errors (0)
----------
None

Next Actions
------------
1. Review each conflict listed above
2. For each .framework-new file:
   - Compare with your version: diff original .framework-new
   - Accept new: mv .framework-new original
   - Keep yours: rm .framework-new
   - Merge both: manually edit original, then rm .framework-new
3. Verify no .framework-new files remain: find . -name "*.framework-new"
4. Test your installation
5. Commit changes
```

### Step 5: Resolve Conflicts

For each conflict, follow this process:

#### Find All Conflicts

```bash
# List all conflict files
find . -name "*.framework-new" -type f

# Example output:
# ./.github/agents/editor-eddy.agent.md.framework-new
# ./docs/templates/ADR_TEMPLATE.md.framework-new
# ./work/templates/TASK_TEMPLATE.md.framework-new
```

#### Review a Conflict

```bash
# Compare versions
diff .github/agents/editor-eddy.agent.md \
     .github/agents/editor-eddy.agent.md.framework-new
```

**Example diff output:**
```diff
15c15
< - **Primary focus:** Documentation clarity and consistency
---
> - **Primary focus:** Documentation clarity, consistency, and accessibility
20a21,23
> 
> ## Accessibility Requirements
> - Follow WCAG 2.1 AA guidelines for all documentation
```

**Analysis:**
- Framework added "and accessibility" to line 15
- Framework added new "Accessibility Requirements" section

**Decision:** Both changes are valuable—merge them.

#### Merge Strategy 1: Accept Framework Version

**When to use:**
- Framework fixes are clearly better
- Your changes were experimental or temporary
- No important customizations lost

```bash
# Replace your version with the new one
mv .github/agents/editor-eddy.agent.md.framework-new \
   .github/agents/editor-eddy.agent.md

# Backup is still available if needed
# .github/agents/editor-eddy.agent.md.bak.20260131_103000
```

#### Merge Strategy 2: Keep Your Version

**When to use:**
- Your customizations are critical
- Framework changes don't apply to your use case
- You'll integrate framework changes later

```bash
# Discard the framework version
rm .github/agents/editor-eddy.agent.md.framework-new

# Keep your backup for reference
# .github/agents/editor-eddy.agent.md.bak.20260131_103000
```

#### Merge Strategy 3: Manual Merge

**When to use:**
- Both versions have valuable changes
- You need to integrate framework improvements with your customizations

**Using diff3 (three-way merge):**

```bash
# If you have the original framework version (from backup or git)
diff3 -m .github/agents/editor-eddy.agent.md \
         .github/agents/editor-eddy.agent.md.bak.20260131_103000 \
         .github/agents/editor-eddy.agent.md.framework-new \
         > .github/agents/editor-eddy.agent.md.merged

# Review merged result
less .github/agents/editor-eddy.agent.md.merged

# If satisfied, replace
mv .github/agents/editor-eddy.agent.md.merged \
   .github/agents/editor-eddy.agent.md

# Clean up
rm .github/agents/editor-eddy.agent.md.framework-new
```

**Using vimdiff (visual merge):**

```bash
vimdiff .github/agents/editor-eddy.agent.md \
        .github/agents/editor-eddy.agent.md.framework-new

# In vim:
# - Navigate between differences with ]c (next) and [c (previous)
# - Pull from right: :diffget
# - Pull from left: :diffput
# - Save and exit: :wqa

# Clean up
rm .github/agents/editor-eddy.agent.md.framework-new
```

**Manual editing:**

```bash
# Open both files
vim -O .github/agents/editor-eddy.agent.md \
       .github/agents/editor-eddy.agent.md.framework-new

# Or use your favorite editor
code --diff .github/agents/editor-eddy.agent.md \
            .github/agents/editor-eddy.agent.md.framework-new

# Manually integrate changes
# Save your file
# Delete .framework-new when done
rm .github/agents/editor-eddy.agent.md.framework-new
```

### Step 6: Verify Resolution

After resolving all conflicts:

```bash
# Ensure no .framework-new files remain
find . -name "*.framework-new" -type f

# Should output nothing

# Check updated metadata
cat .framework_meta.yml
# Should show new version:
# framework_version: 1.1.0
# installed_at: 2026-01-31T10:30:00Z

# Test key functionality
# (Run your tests, try agent profiles, etc.)
```

### Step 7: Clean Up

```bash
# Review backup files
find . -name "*.bak.*" -type f

# If everything works, you can remove backups
find . -name "*.bak.*" -type f -delete

# Or keep them for a while
# They don't hurt anything
```

### Step 8: Commit Changes

```bash
# Review what changed
git status
git diff .framework_meta.yml

# Commit the upgrade
git add .framework_meta.yml .github/ docs/ work/ framework/ validation/
git commit -m "Upgrade framework from 1.0.0 to 1.1.0"

# Tag the upgrade (optional)
git tag framework-v1.1.0
```

## Upgrade Planning

For complex upgrades with many conflicts, use **plan mode** to generate a detailed upgrade plan:

```bash
./scripts/framework_upgrade.sh --plan . /path/to/your/repo
```

This generates `upgrade-plan.yml` for the Framework Guardian agent to analyze:

```yaml
upgrade_plan:
  version_from: "1.0.0"
  version_to: "1.1.0"
  conflicts:
    - path: ".github/agents/editor-eddy.agent.md"
      your_checksum: "a1b2c3..."
      new_checksum: "f6e5d4..."
      classification: "agent_profile"
      recommendation: "manual_merge"
      priority: "high"
      
    - path: "docs/templates/ADR_TEMPLATE.md"
      your_checksum: "123abc..."
      new_checksum: "def456..."
      classification: "template"
      recommendation: "accept_new"
      priority: "medium"
```

**Use the Framework Guardian agent:**

```
I have an upgrade plan in upgrade-plan.yml. 
Acting as Framework Guardian, analyze the conflicts and provide
step-by-step merge recommendations.
```

The Guardian will:
- Classify each conflict
- Suggest merge strategies
- Generate specific diff commands
- Prioritize conflicts by impact

## Protected Directories

The `local/` directory is **completely protected** during upgrades.

### What's Protected

Any file or directory under `local/`:

```
local/
  agents/              # Your custom agent profiles
  templates/           # Your custom templates
  workflows/           # Your custom workflows
  config/              # Your configuration overrides
  scripts/             # Your custom scripts
```

### Why It's Protected

The `local/` directory is your customization zone. Framework upgrades should never touch it, ensuring:

- Your customizations survive upgrades
- No conflicts for project-specific content
- Clear separation between framework and local

### Using Protected Space

**Example: Custom agent profile**

```bash
# Create custom agent based on framework agent
mkdir -p local/agents
cp .github/agents/devops-danny.agent.md local/agents/devops-danny-team.agent.md

# Customize for your team
vim local/agents/devops-danny-team.agent.md

# Now you can:
# 1. Upgrade framework without losing customizations
# 2. Reference your custom agent: local/agents/devops-danny-team.agent.md
# 3. Keep team-specific practices separate from framework
```

**Example: Organization-specific template**

```bash
mkdir -p local/templates
cp docs/templates/ADR_TEMPLATE.md local/templates/ADR_TEMPLATE_ORG.md

# Adapt to your organization's standards
vim local/templates/ADR_TEMPLATE_ORG.md

# Use it for new ADRs while keeping framework template intact
```

## Backup and Rollback

### Automatic Backups

By default, the upgrade script creates `.bak.TIMESTAMP` backups for conflicted files:

```
.github/agents/editor-eddy.agent.md.bak.20260131_103000
docs/templates/ADR_TEMPLATE.md.bak.20260131_103500
```

**To disable backups** (not recommended):

```bash
./scripts/framework_upgrade.sh --no-backup . /path/to/repo
```

### Manual Backups

Before major upgrades, create comprehensive backups:

```bash
# Backup entire framework installation
tar czf framework-backup-$(date +%Y%m%d).tar.gz \
    .github/agents \
    docs/templates \
    work/templates \
    framework \
    validation \
    AGENTS.md \
    .framework_meta.yml

# Verify backup
tar tzf framework-backup-*.tar.gz | head
```

### Rolling Back an Upgrade

If the upgrade causes problems:

**Option 1: Restore from .bak files**

```bash
# Find all backup files
find . -name "*.bak.*" -type f

# Restore each one
find . -name "*.bak.*" -type f | while read backup; do
    original="${backup%.bak.*}"
    echo "Restoring $original"
    cp "$backup" "$original"
done

# Remove .framework-new files
find . -name "*.framework-new" -type f -delete

# Restore old metadata
if [ -f .framework_meta.yml.bak.* ]; then
    cp .framework_meta.yml.bak.* .framework_meta.yml
fi

# Verify version
cat .framework_meta.yml
```

**Option 2: Git rollback**

```bash
# If you committed pre-upgrade
git log --oneline | head -5

# Find pre-upgrade commit
git show <commit-hash>:.framework_meta.yml

# Rollback
git reset --hard <pre-upgrade-commit>

# Or rollback specific files
git checkout <pre-upgrade-commit> -- .github/ docs/ work/ framework/
```

**Option 3: Restore from manual backup**

```bash
# Extract backup
tar xzf framework-backup-20260131.tar.gz

# Verify contents
cat .framework_meta.yml
```

## Troubleshooting

### Issue: "No existing framework installation found"

**Symptom:**
```
✗ No existing framework installation found
  Missing: .framework_meta.yml
  Run framework_install.sh for first-time installation
```

**Cause:** You're trying to upgrade a repository without an existing installation.

**Solution:**
```bash
# Use install script instead
./scripts/framework_install.sh . /path/to/repo
```

### Issue: "Version downgrade not supported"

**Symptom:**
```
⚠ Warning: Attempting to downgrade
  Current: 1.1.0
  Target:  1.0.0
  Downgrades are not officially supported
```

**Cause:** You're trying to install an older version over a newer one.

**Solution:**

If you really need to downgrade:

```bash
# 1. Remove current installation metadata
mv .framework_meta.yml .framework_meta.yml.backup

# 2. Run install (not upgrade) with older version
./scripts/framework_install.sh . /path/to/repo

# 3. Handle conflicts manually
```

**Better approach:** Use version control to rollback:

```bash
git checkout <commit-with-old-version>
```

### Issue: Too Many Conflicts

**Symptom:**
```
Results:
  CONFLICT:   127 files
```

**Cause:** 
- You've modified many framework files
- Major framework version change
- Missed several incremental upgrades

**Solution:**

**1. Use upgrade planning:**

```bash
./scripts/framework_upgrade.sh --plan . /path/to/repo

# Analyze with Framework Guardian
# Get step-by-step merge recommendations
```

**2. Move customizations to local/:**

```bash
# Identify your customizations
git log --follow .github/agents/

# Move them to local/
mkdir -p local/agents
cp .github/agents/custom*.agent.md local/agents/

# Accept framework versions for standard files
find .github/agents -name "*.framework-new" -type f | while read new; do
    original="${new%.framework-new}"
    mv "$new" "$original"
done
```

**3. Incremental upgrade:**

If you skipped versions 1.0 → 1.5, try:

```bash
# Upgrade one version at a time
# 1.0 → 1.1
# 1.1 → 1.2
# etc.
```

### Issue: Conflicts in Files You Didn't Touch

**Symptom:**
```
⚡ CONFLICT: .github/agents/devops-danny.agent.md
   (But I never edited this file!)
```

**Cause:** Framework improved the file, so checksums differ.

**Solution:**

```bash
# Check what changed
diff .github/agents/devops-danny.agent.md \
     .github/agents/devops-danny.agent.md.framework-new

# If framework changes are clearly improvements, accept them
mv .github/agents/devops-danny.agent.md.framework-new \
   .github/agents/devops-danny.agent.md
```

**To avoid this in future:**
- Don't modify framework files directly
- Put customizations in `local/`

### Issue: Permission Errors

**Symptom:**
```
✗ ERROR: Cannot create file .github/agents/new-agent.agent.md
   Permission denied
```

**Cause:** Insufficient write permissions.

**Solution:**

```bash
# Check permissions
ls -ld .github/agents/

# Fix permissions
chmod -R u+w .github/agents/

# Try upgrade again
./scripts/framework_upgrade.sh . /path/to/repo
```

### Issue: Checksum Utility Missing

**Symptom:**
```
✗ Neither sha256sum nor shasum found
```

**Cause:** System missing checksum utilities (rare).

**Solution:**

```bash
# Linux
sudo apt-get install coreutils

# macOS
# Should be pre-installed, but if not:
brew install coreutils
```

## Best Practices

### 1. Always Dry Run First

```bash
# ✅ Good practice
./scripts/framework_upgrade.sh --dry-run . /path/to/repo
# Review output
./scripts/framework_upgrade.sh . /path/to/repo

# ❌ Risky
./scripts/framework_upgrade.sh . /path/to/repo
# (no preview)
```

### 2. Read Release Notes

```bash
# Before upgrading
cat quickstart-framework-1.1.0/META/RELEASE_NOTES.md | less
```

Understand:
- What's new
- What's changed
- What's deprecated
- Required actions

### 3. Commit Before Upgrading

```bash
# Clean state
git status

# Commit everything
git add .
git commit -m "Pre-upgrade checkpoint"

# Tag it
git tag pre-upgrade-$(date +%Y%m%d)

# Now upgrade
./scripts/framework_upgrade.sh . .
```

### 4. Keep Backups Enabled

```bash
# ✅ Default (keeps backups)
./scripts/framework_upgrade.sh . .

# ❌ Risky
./scripts/framework_upgrade.sh --no-backup . .
```

Backup files don't hurt, and they're lifesavers if something goes wrong.

### 5. Test After Upgrading

```bash
# After upgrade, test functionality
cp work/templates/TASK_TEMPLATE.md /tmp/test_task.md

# Run validation scripts
python validation/validate_structure.py

# Try agent profiles
# (In your AI assistant)
# "Acting as DevOps Danny, help me review this deployment"
```

### 6. Document Your Conflicts

Keep notes about how you resolved conflicts:

```bash
# Create upgrade log
cat > upgrade-log-$(date +%Y%m%d).md << 'EOF'
# Upgrade 1.0.0 → 1.1.0

## Conflicts Resolved

### editor-eddy.agent.md
- **Issue:** Framework added accessibility guidelines
- **Resolution:** Accepted framework version
- **Reason:** Accessibility improvements are valuable

### ADR_TEMPLATE.md
- **Issue:** We added "Business Impact" section, framework added "Security Considerations"
- **Resolution:** Manual merge—included both sections
- **Reason:** Both sections are important

## Testing Done
- Created test task from template ✅
- Ran validation scripts ✅
- Tested agent profiles ✅

## Follow-up Actions
- None

EOF
```

This helps:
- Future upgrades (you'll remember what you did)
- Team members (they'll understand the decisions)
- Onboarding (new people can see the history)

### 7. Upgrade Regularly

Don't skip versions:

```bash
# ✅ Good
1.0.0 → 1.1.0 → 1.2.0 → 1.3.0
# (Small, manageable upgrades)

# ❌ Painful
1.0.0 → 1.5.0
# (Many conflicts, large diff)
```

Regular upgrades = fewer conflicts = less pain.

### 8. Use local/ for Customizations

```bash
# ❌ Don't modify framework files
vim .github/agents/devops-danny.agent.md

# ✅ Create local overrides
mkdir -p local/agents
cp .github/agents/devops-danny.agent.md local/agents/devops-danny-team.agent.md
vim local/agents/devops-danny-team.agent.md
```

Files in `local/` are never touched by upgrades.

## Related Documentation

- **[Installation Guide](USER_GUIDE_installation.md)** - First-time installation
- **[Distribution Guide](USER_GUIDE_distribution.md)** - What's in releases
- **[Getting Started](quickstart/GETTING_STARTED.md)** - Quick start guide
- **[Technical Docs](HOW_TO_USE/framework_install.md)** - Technical details
- **[ADR-013](architecture/adrs/ADR-013-zip-distribution.md)** - Distribution architecture
- **[ADR-014](architecture/adrs/ADR-014-framework-guardian-agent.md)** - Framework Guardian

## Support

Need help with an upgrade?

1. Check this guide's [Troubleshooting](#troubleshooting) section
2. Review `upgrade-report.txt` from your upgrade
3. Use Framework Guardian agent for conflict analysis
4. Read the [technical documentation](HOW_TO_USE/framework_install.md)
5. Search [existing issues](https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues)
6. Create a new issue with:
   - Current version (from `.framework_meta.yml`)
   - Target version
   - Upgrade command used
   - Contents of `upgrade-report.txt`
   - Specific conflicts you're struggling with

---

**Last Updated:** 2026-01-31  
**Document Version:** 1.0.0  
**Framework Version:** 1.0.0+
