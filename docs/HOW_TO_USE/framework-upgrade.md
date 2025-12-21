# Framework Upgrade Guide

## Overview

The `framework_upgrade.sh` script enables safe upgrades of the agent framework in downstream repositories without destroying local customizations. It intelligently compares files using SHA256 checksums and creates `.framework-new` files for manual review when conflicts occur.

## Prerequisites

- Framework must already be installed (`.framework_meta.yml` exists)
- POSIX-compliant shell (sh, bash, dash, ash)
- SHA256 checksum tool (`sha256sum` or `shasum`)
- Framework distribution package (zip) extracted

## Usage

### Basic Upgrade

```bash
# From the extracted framework distribution directory
./ops/scripts/framework_upgrade.sh /path/to/your/project
```

### Dry-Run Mode (Preview Changes)

```bash
# See what would change without making modifications
./ops/scripts/framework_upgrade.sh --dry-run /path/to/your/project
```

### Help

```bash
./ops/scripts/framework_upgrade.sh --help
```

## File Status Categories

The upgrade script classifies each framework file into one of three categories:

### NEW
- **Meaning**: File exists in new framework but not in your project
- **Action**: File is copied to your project
- **Impact**: Low risk - adds new framework functionality

### UNCHANGED
- **Meaning**: File exists in both versions with identical SHA256 checksums
- **Action**: No changes made (file skipped)
- **Impact**: No risk - file already up to date

### CONFLICT
- **Meaning**: File exists in both versions but with different content
- **Action**: Creates `<filename>.framework-new` for manual review
- **Impact**: Requires manual resolution
- **Note**: Original file is **never** modified

## Upgrade Workflow

### Step 1: Pre-Upgrade Preparation

1. **Backup your project** (recommended):
   ```bash
   git add -A
   git commit -m "Pre-framework-upgrade snapshot"
   # OR create a backup copy
   cp -r /path/to/project /path/to/project.backup
   ```

2. **Check current framework version**:
   ```bash
   grep framework_version: /path/to/project/.framework_meta.yml
   ```

3. **Download and extract** the new framework distribution:
   ```bash
   unzip quickstart-framework-1.2.0.zip
   cd quickstart-framework-1.2.0
   ```

### Step 2: Preview Changes (Recommended)

Run a dry-run to understand what will change:

```bash
./ops/scripts/framework_upgrade.sh --dry-run /path/to/project
```

Review the output:
- Check the NEW count (new features being added)
- Check the CONFLICT count (files requiring manual review)
- Read the summary carefully

### Step 3: Execute Upgrade

Run the actual upgrade:

```bash
./ops/scripts/framework_upgrade.sh /path/to/project
```

The script will:
- Copy new files
- Skip unchanged files
- Create `.framework-new` files for conflicts
- Generate `upgrade-report.txt` in your project root
- Update `.framework_meta.yml` with new version

### Step 4: Review Upgrade Report

Examine the generated report:

```bash
cat /path/to/project/upgrade-report.txt
```

The report contains:
- Summary counts (NEW, UNCHANGED, CONFLICT)
- Complete list of files by status
- Timestamp and version information

### Step 5: Resolve Conflicts

For each CONFLICT, you'll find a `.framework-new` file:

```bash
# Find all conflicts
find /path/to/project -name "*.framework-new"
```

#### Conflict Resolution Options

For each conflicting file, you have three options:

**Option 1: Accept Framework Version (Discard Local Changes)**

```bash
# Replace your version with the framework version
mv /path/to/file.framework-new /path/to/file
```

Use when:
- You want the latest framework behavior
- Your local changes are outdated or experimental

**Option 2: Keep Local Version (Reject Framework Changes)**

```bash
# Delete the framework-new file
rm /path/to/file.framework-new
```

Use when:
- Your customizations are intentional and valuable
- Framework changes would break your workflow
- You've made strategic deviations from framework defaults

**Option 3: Merge Manually (Combine Both)**

```bash
# Compare files to understand differences
diff /path/to/file /path/to/file.framework-new

# OR use a visual diff tool
vimdiff /path/to/file /path/to/file.framework-new
# git diff --no-index /path/to/file /path/to/file.framework-new
# meld /path/to/file /path/to/file.framework-new

# Manually edit to combine best of both
vim /path/to/file

# Remove .framework-new after merging
rm /path/to/file.framework-new
```

Use when:
- Both versions have valuable changes
- You need specific framework updates plus your customizations
- The changes affect different sections of the file

#### Moving Customizations to local/

If you find yourself repeatedly having conflicts in core framework files, consider moving your customizations to the `local/` directory (which is never touched by upgrades):

```bash
# Example: Move custom agent to local directory
mkdir -p /path/to/project/local/agents
mv /path/to/project/.github/agents/my-custom-agent.md \
   /path/to/project/local/agents/

# Update references in your project to point to local/
```

### Step 6: Verify and Test

After resolving conflicts:

1. **Verify no .framework-new files remain**:
   ```bash
   find /path/to/project -name "*.framework-new" | wc -l
   # Should return 0
   ```

2. **Check framework version updated**:
   ```bash
   grep framework_version: /path/to/project/.framework_meta.yml
   ```

3. **Test your workflows**:
   - Run validation scripts
   - Test your agents
   - Verify documentation renders correctly

4. **Commit changes**:
   ```bash
   git add -A
   git commit -m "Upgrade framework to version 1.2.0"
   ```

## Advanced Usage

### Custom Framework Location

```bash
# Override framework_core directory location
export FRAMEWORK_SOURCE=/custom/path/to/framework_core
./ops/scripts/framework_upgrade.sh /path/to/project
```

### Custom Manifest Location

```bash
# Override MANIFEST.yml location
export MANIFEST_PATH=/custom/path/to/MANIFEST.yml
./ops/scripts/framework_upgrade.sh /path/to/project
```

### Automated Conflict Detection

Use with CI/CD pipelines:

```bash
#!/bin/bash
# ci-upgrade-check.sh

./ops/scripts/framework_upgrade.sh --dry-run /project/path > upgrade-preview.txt

CONFLICTS=$(grep "CONFLICT:" upgrade-preview.txt | grep -o '[0-9]*' | head -1)

if [ "$CONFLICTS" -gt 0 ]; then
    echo "⚠️  Upgrade would create $CONFLICTS conflicts"
    echo "Manual review required before upgrade"
    exit 1
else
    echo "✅ Upgrade can proceed safely (no conflicts)"
    exit 0
fi
```

## Protected Directories

The upgrade script **never modifies** files under:
- `local/**` - All local customizations are protected

This design allows you to maintain project-specific customizations without fear of upgrades overwriting them.

## Exit Codes

| Code | Meaning | Action Required |
|------|---------|----------------|
| 0 | Success | Review conflicts if any |
| 1 | Framework not installed | Run framework_install.sh first |
| 2 | Invalid parameters | Check command syntax |
| 3 | framework_core/ not found | Run from distribution directory |
| 4 | META/MANIFEST.yml not found | Verify distribution package |
| 5 | Failed to create directories | Check filesystem permissions |
| 6 | Failed to copy files | Check disk space and permissions |
| 7 | Failed to update metadata | Check write permissions |

## Troubleshooting

### Issue: "Framework not installed"

**Solution**: Run `framework_install.sh` first for initial installation:
```bash
./ops/scripts/framework_install.sh /path/to/project
```

### Issue: "No SHA256 checksum tool available"

**Solution**: Install sha256sum or shasum:
```bash
# Ubuntu/Debian
sudo apt-get install coreutils

# macOS (shasum is usually pre-installed)
# Check with: which shasum

# Alpine
apk add coreutils
```

### Issue: Many conflicts after upgrade

**Causes**:
- Heavy local customization of core files
- Skipped multiple framework versions

**Solutions**:
1. **Review conflicts methodically**: Use the upgrade-report.txt to prioritize
2. **Move to local/**: Migrate custom agents/guidelines to local/ directory
3. **Incremental upgrades**: Upgrade one version at a time when possible

### Issue: Upgrade report not readable

**Solution**: The report is plain text:
```bash
cat /path/to/project/upgrade-report.txt | less
```

### Issue: Need to undo upgrade

**Solution** (if you made a backup):
```bash
# If using git
git reset --hard HEAD^

# If using filesystem backup
rm -rf /path/to/project
mv /path/to/project.backup /path/to/project
```

## Framework Guardian Integration

After upgrade, the Framework Guardian agent can assist with conflict resolution:

```bash
# Launch Framework Guardian in audit mode
# (Requires Framework Guardian agent - see ADR-014)

# Guardian will:
# - Analyze all .framework-new files
# - Classify conflicts (auto-merge vs manual review)
# - Generate FRAMEWORK_UPGRADE_PLAN.md with recommendations
```

## Best Practices

### DO:
✅ Run `--dry-run` before actual upgrade  
✅ Backup your project before upgrading  
✅ Read the CHANGELOG for the new framework version  
✅ Resolve conflicts promptly after upgrade  
✅ Test your workflows after upgrade  
✅ Move custom agents to `local/` directory  
✅ Commit framework upgrades as discrete changes  

### DON'T:
❌ Skip dry-run for major version upgrades  
❌ Leave `.framework-new` files unresolved  
❌ Modify `.framework_meta.yml` manually  
❌ Run upgrade without backup  
❌ Customize core framework files (use local/ instead)  
❌ Force upgrades in CI without manual approval  

## File Comparison Strategy

The script uses **SHA256 checksums** for file comparison:
- **Fast**: Only computes checksums when files differ in size/timestamp
- **Reliable**: Same approach as Git (detects even single-byte changes)
- **Cross-platform**: Works on Linux, macOS, and WSL

## Upgrade Report Format

Example `upgrade-report.txt`:

```
=== Framework Upgrade Report ===
Date: 2025-12-21T08:00:00Z
From version: 1.0.0
To version: 1.2.0

=== Summary ===
NEW: 5 files
UNCHANGED: 23 files
CONFLICT: 2 files

=== File Details ===
NEW: docs/templates/new-template.md
NEW: .github/agents/framework-guardian.md
NEW: docs/guidelines/conflict-resolution.md
NEW: validation/framework-checks.sh
NEW: docs/HOW_TO_USE/framework-upgrade.md
CONFLICT: .github/agents/general-guidelines.md
CONFLICT: docs/templates/agent-template.md
UNCHANGED: AGENTS.md
UNCHANGED: .github/agents/bootstrap.md
...
```

## Security Considerations

- **No remote access**: Script operates entirely on local files
- **No destructive operations**: Original files never modified on conflict
- **Transparent operations**: All actions logged to upgrade-report.txt
- **Auditable**: All file changes traceable via checksums

## Related Documentation

- [Framework Installation Guide](./framework-installation.md) - Initial setup
- [Framework Distribution Architecture](../architecture/design/distribution_of_releases_architecture.md)
- [ADR-013: Zip-Based Framework Distribution](../architecture/adrs/ADR-013-zip-distribution.md)
- [ADR-014: Framework Guardian Agent](../architecture/adrs/ADR-014-framework-guardian.md)

## Version History

- **1.0.0** (2025-12-21): Initial release
  - SHA256-based conflict detection
  - Dry-run mode support
  - Upgrade report generation
  - Protected local/ directory

## Support

For issues or questions:
1. Review this documentation
2. Check the upgrade-report.txt for details
3. Consult the Framework Guardian agent
4. Review framework CHANGELOG for breaking changes
5. Open an issue in the framework repository
