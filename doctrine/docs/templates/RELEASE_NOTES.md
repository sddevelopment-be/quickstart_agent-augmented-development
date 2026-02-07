# Release Notes: Framework vX.Y.Z

**Release Date:** YYYY-MM-DD  
**Release Manager:** [Name]  
**Release Type:** [Major | Minor | Patch | Pre-release]

---

## Overview

[Brief description of this release - 2-3 sentences summarizing key changes]

**Target Audience:** [Framework core team | Downstream adopters | Both]

---

## Version Information

| Field | Value |
|-------|-------|
| **Version** | X.Y.Z |
| **Previous Version** | X.Y.Z-1 |
| **Release Branch** | release/vX.Y.Z or main |
| **Git Commit** | [commit hash] |
| **Build Date** | YYYY-MM-DDTHH:MM:SSZ |
| **Distribution Artifact** | quickstart-framework-X.Y.Z.zip |

---

## What's New

### ✨ New Features

- **[Feature Name]**: [Brief description of feature and value]
  - [Additional detail if needed]
  - [Usage example or reference to docs]

- **[Feature Name]**: [Brief description]

### 🔧 Improvements

- **[Component/Area]**: [Description of improvement]
- **[Component/Area]**: [Description of improvement]

### 🐛 Bug Fixes

- **[Issue #]**: [Description of fix]
- **[Issue #]**: [Description of fix]

### 📚 Documentation

- [Documentation update description]
- [Documentation update description]

### 🔨 Internal Changes

[Changes relevant to framework developers but not end users]

- [Internal change]
- [Internal change]

---

## Breaking Changes

> ⚠️ **IMPORTANT:** This section lists changes that may require action from downstream teams.

### [Breaking Change Title]

**Impact:** [What is broken and who is affected]

**Migration Path:**

```bash
# Before (old approach):
[old code/config example]

# After (new approach):
[new code/config example]
```

**Documentation:** [Link to migration guide or detailed docs]

---

## Upgrade Instructions

### Prerequisites

- Existing framework installation with `.framework_meta.yml`
- Framework version X.Y.Z-1 or later recommended
- [Any specific prerequisites for this release]

### Standard Upgrade

```bash
# 1. Download release artifact
wget https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/download/vX.Y.Z/quickstart-framework-X.Y.Z.zip

# 2. Extract archive
unzip quickstart-framework-X.Y.Z.zip
cd quickstart-framework-X.Y.Z

# 3. Preview upgrade (recommended)
./scripts/framework_upgrade.sh --dry-run . /path/to/your/repo

# 4. Execute upgrade
./scripts/framework_upgrade.sh . /path/to/your/repo

# 5. Review upgrade report
cat /path/to/your/repo/upgrade-report.txt

# 6. Resolve conflicts (if any)
find /path/to/your/repo -name "*.framework-new" -type f
# Follow conflict resolution guide in upgrade-report.txt
```

### First-Time Installation

```bash
# 1. Download and extract (as above)

# 2. Run installation script
./scripts/framework_install.sh . /path/to/your/repo

# 3. Verify installation
cat /path/to/your/repo/.framework_meta.yml
```

**Detailed Instructions:** See [Release and Upgrade Workflow Guide](docs/HOW_TO_USE/release_and_upgrade.md)

---

## Framework Guardian Metadata

> 🛡️ This release has been validated by Framework Guardian per ADR-014.

```yaml
guardian_metadata:
  audit_date: "YYYY-MM-DDTHH:MM:SSZ"
  framework_version: "X.Y.Z"
  audit_status: "[PASS | WARN | FAIL]"
  manifest_completeness: "100%"
  total_files_audited: [number]
  issues_found: [number]
  notes: "[Any relevant audit notes or findings]"
```

### Audit Summary

- **Status**: [✅ PASS | ⚠️ WARN | ❌ FAIL]
- **Files Audited**: [number] files
- **Manifest Integrity**: [100% | describe any issues]
- **Known Issues**: [None | list issues]

**Full Audit Report:** [Link to validation/FRAMEWORK_AUDIT_REPORT.md if included]

---

## Distribution Metadata

### Artifact Information

| Property | Value |
|----------|-------|
| **Artifact Name** | quickstart-framework-X.Y.Z.zip |
| **Compressed Size** | [X.X MB] |
| **Uncompressed Size** | [X.X MB] |
| **Total Files** | [number] |
| **SHA256 Checksum** | [checksum] |

### Included Components

**Core Directories:**
- `.github/agents/` - [N files] - Agent profiles and directives
- `${DOC_ROOT}/templates/` - [N files] - Document templates
- `${DOC_ROOT}/architecture/` - [N files] - ADRs and design docs
- `framework/` - [N files] - Python framework code
- `validation/` - [N files] - Validation scripts
- `work/templates/` - [N files] - Task templates

**Root Files:**
- `AGENTS.md` - Agent coordination protocol
- `README.md` - Framework documentation
- `pyproject.toml` - Python project configuration
- `requirements.txt` - Python dependencies

**Scripts:**
- `framework_install.sh` - Installation script (v[version])
- `framework_upgrade.sh` - Upgrade script (v[version])

**Metadata:**
- `META/MANIFEST.yml` - File checksums and inventory
- `META/metadata.json` - Build metadata
- `META/RELEASE_NOTES.md` - This file

### Verification

```bash
# Verify artifact integrity
sha256sum -c checksums.txt

# Expected output:
# quickstart-framework-X.Y.Z.zip: OK
```

---

## Known Issues

### Critical

[None | List critical issues with workarounds]

### High Priority

[None | List high-priority issues]

### Medium Priority

[None | List medium-priority issues]

### Workarounds

[Document any necessary workarounds for known issues]

---

## Deprecations

> ⚠️ Features or APIs marked for removal in future releases.

### Deprecated in This Release

- **[Feature/API Name]**: [Reason for deprecation]
  - **Deprecation Date**: YYYY-MM-DD
  - **Planned Removal**: vX.Y.Z (release date)
  - **Alternative**: [Recommended replacement]

### Previously Deprecated (Removal Warning)

- **[Feature/API Name]**: Will be removed in vX.Y.Z

---

## Dependencies

### Python Dependencies

[If Python dependencies changed]

```
# Updated requirements.txt
[list key dependency changes]
```

### System Requirements

- **Python**: 3.8+ (unchanged | updated from X.Y)
- **Shell**: POSIX-compliant (bash, sh, zsh)
- **Utilities**: Standard Unix tools (find, cp, sha256sum/shasum, date)

### Framework Compatibility

- **Compatible with**: Framework vX.Y.Z and later
- **Breaking changes from**: vX.Y.Z (requires migration)

---

## Testing and Validation

### Test Coverage

- **Unit Tests**: [pass rate or N/N passed]
- **Integration Tests**: [pass rate or N/N passed]
- **Acceptance Tests**: [pass rate or N/N passed]
- **Installation Tests**: [✅ PASS | details]
- **Upgrade Tests**: [✅ PASS | details]

### Validation Checklist

- [✅ | ❌] Build artifact checksum verified
- [✅ | ❌] Manifest completeness validated
- [✅ | ❌] Installation tested in clean environment
- [✅ | ❌] Upgrade tested from previous version
- [✅ | ❌] Framework Guardian audit passed
- [✅ | ❌] Documentation reviewed and updated
- [✅ | ❌] Release notes approved

---

## Communication and Rollout

### Release Announcement

- **Internal Announcement**: [Date] via [Slack/Teams/Email]
- **External Announcement**: [Date] via [GitHub Discussions/Blog/Social]
- **Downstream Notification**: [Date] to known adopters

### Rollout Plan

1. **Phase 1**: Internal testing (framework core team)
2. **Phase 2**: Early adopter validation (select downstream teams)
3. **Phase 3**: General availability

**Current Phase**: [Phase number and status]

### Support

For issues or questions:

1. **Documentation**: 
   - [Release and Upgrade Workflow Guide](docs/HOW_TO_USE/release_and_upgrade.md)
   - [Framework Installation Guide](docs/HOW_TO_USE/framework_install.md)
   - [Troubleshooting Section](#troubleshooting)

2. **Issue Tracking**:
   - Create an issue: https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues
   - Use label: `release/vX.Y.Z`

3. **Community**:
   - [GitHub Discussions]
   - [Slack Channel]
   - [Team Contact]

---

## Contributors

[Thank contributors who made this release possible]

### Core Team

- [Name] - [Role/Contribution]
- [Name] - [Role/Contribution]

### Community Contributors

- [Name] - [Contribution]
- [Name] - [Contribution]

**Thank you to everyone who contributed to this release!**

---

## Troubleshooting

### Common Upgrade Issues

**Issue:** "No existing framework installation found"

**Solution:**
```bash
# This is a fresh installation, use install script instead:
./scripts/framework_install.sh . /path/to/repo
```

**Issue:** Excessive conflicts during upgrade

**Solution:**
1. Review upgrade-report.txt for conflict details
2. Use Framework Guardian for conflict analysis (if available)
3. Consider selective merge or fresh installation with manual customization reapply

**Issue:** [Other common issue specific to this release]

**Solution:** [Resolution steps]

### Getting Help

If you encounter issues not covered here:

1. Check [Framework Installation Guide - Troubleshooting](docs/HOW_TO_USE/framework_install.md#troubleshooting)
2. Review [Release and Upgrade Workflow Guide](docs/HOW_TO_USE/release_and_upgrade.md#troubleshooting)
3. Search existing issues for similar problems
4. Create a new issue with:
   - Release version (vX.Y.Z)
   - Operating system and shell
   - Complete error messages
   - Steps to reproduce
   - Relevant portions of upgrade-report.txt (if applicable)

---

## References

### Architecture Documents

- [ADR-013: Zip-Based Framework Distribution](${DOC_ROOT}/architecture/adrs/ADR-013-zip-distribution.md)
- [ADR-014: Framework Guardian Agent](${DOC_ROOT}/architecture/adrs/ADR-014-framework-guardian-agent.md)

### Operational Guides

- [Release and Upgrade Workflow Guide](docs/HOW_TO_USE/release_and_upgrade.md)
- [Framework Installation Guide](docs/HOW_TO_USE/framework_install.md)
- [Release Publishing Checklist](docs/checklists/release_publishing_checklist.md)

### Source Repository

- **GitHub**: https://github.com/sddevelopment-be/quickstart_agent-augmented-development
- **Release Tag**: vX.Y.Z
- **Release Assets**: https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases/tag/vX.Y.Z

---

## Changelog Entry

[Copy this section to CHANGELOG.md]

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- [Feature description]
- [Feature description]

### Changed
- [Change description]
- [Change description]

### Fixed
- [Fix description]
- [Fix description]

### Deprecated
- [Deprecation notice]

### Removed
- [Removal notice]

### Security
- [Security update]
```

---

## Metadata

| Field | Value |
|-------|-------|
| **Template Version** | 2.0.0 |
| **Last Updated** | 2026-01-31 |
| **Maintained By** | Agentic Framework Core Team |
| **Template Purpose** | Standardized release documentation with Guardian integration |
| **Related Templates** | CHANGELOG.md, FRAMEWORK_AUDIT_REPORT.md, FRAMEWORK_UPGRADE_PLAN.md |

---

**End of Release Notes**

---

## Template Usage Instructions

> **Note:** This section should be removed from actual release notes.

### How to Use This Template

1. **Copy this template** to `META/RELEASE_NOTES.md` in your release artifact
2. **Replace all placeholders**:
   - `X.Y.Z` → actual version number
   - `YYYY-MM-DD` → actual dates
   - `[Name]` → actual names
   - `[Description]` → actual descriptions
   - `[number]` → actual counts
   - `[checksum]` → actual SHA256 checksums
3. **Remove sections** that don't apply (e.g., "Breaking Changes" for patch releases)
4. **Add content** specific to your release
5. **Run Guardian audit** and populate Guardian Metadata section
6. **Review completeness** using [Release Publishing Checklist](docs/checklists/release_publishing_checklist.md)
7. **Remove this "Template Usage Instructions" section**

### Key Sections Explained

- **Overview**: High-level summary for skimmers
- **What's New**: User-facing changes organized by category
- **Breaking Changes**: CRITICAL for downstream teams
- **Upgrade Instructions**: Practical step-by-step commands
- **Framework Guardian Metadata**: NEW in v2.0.0 - ADR-014 compliance
- **Distribution Metadata**: NEW in v2.0.0 - Packaging details
- **Troubleshooting**: Common issues specific to this release

### Guardian Metadata (NEW in v2.0.0)

The Guardian Metadata section is a key addition per ADR-014. It provides:

- Audit status and completeness
- File integrity verification
- Known issues from automated analysis
- Confidence level for upgrade safety

**To populate:**
1. Run Framework Guardian audit after build
2. Copy output from `validation/FRAMEWORK_AUDIT_REPORT.md`
3. Include audit summary in release notes
4. Mark audit_status as PASS/WARN/FAIL

### Distribution Metadata (NEW in v2.0.0)

The Distribution Metadata section provides transparency about:

- Artifact size and file count
- Included components and directory structure
- Script versions included
- Verification procedures

**To populate:**
1. Extract information from `META/MANIFEST.yml`
2. Get checksums from `checksums.txt`
3. Use `du -h` for size information
4. Count files with `find` or manifest `total_files`

### Template Evolution

- **v1.0.0**: Basic release notes structure
- **v2.0.0**: Added Guardian Metadata and Distribution Metadata sections per ADR-013/014

**Feedback:** Submit improvements to this template via PR or issue.
