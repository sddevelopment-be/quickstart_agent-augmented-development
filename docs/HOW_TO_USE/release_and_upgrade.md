# Release and Upgrade Workflow Guide

## Target Audience

This guide is for **Agentic Framework Core Team** members and **downstream adopters** managing framework releases and installations. It assumes familiarity with version control, command-line tools, and framework architecture.

> **For quick installation/upgrade instructions only**, see [Framework Installation Guide](framework_install.md).  
> **For packaging automation**, see [Release Packaging README](../../ops/release/README.md).

---

## Overview

This guide walks through the complete release-to-deployment lifecycle of the Quickstart Agent-Augmented Development Framework:

1. **Build** → Package a versioned release artifact
2. **Verify** → Validate artifact integrity and structure
3. **Publish** → Distribute to downstream consumers
4. **Install** → Deploy framework to new repositories
5. **Upgrade** → Update existing installations safely
6. **Validate** → Run Framework Guardian audits

The workflow implements **ADR-013** (Zip-Based Framework Distribution) and **ADR-014** (Framework Guardian Agent).

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quickstart: End-to-End Example](#quickstart-end-to-end-example)
- [Deep Dive: Build Release Artifact](#deep-dive-build-release-artifact)
- [Deep Dive: Verify and Publish](#deep-dive-verify-and-publish)
- [Deep Dive: Install Framework](#deep-dive-install-framework)
- [Deep Dive: Upgrade Framework](#deep-dive-upgrade-framework)
- [Deep Dive: Framework Guardian Validation](#deep-dive-framework-guardian-validation)
- [Integration with Iteration Workflow](#integration-with-iteration-workflow)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [References](#references)

---

## Prerequisites

### For Release Managers (Building Artifacts)

- Python 3.8+ with `pyyaml` installed
- Git repository access with clean working tree
- Write access to release output directory
- Semantic versioning knowledge

### For Downstream Teams (Installing/Upgrading)

- POSIX-compliant shell (bash, sh, zsh)
- Standard Unix utilities: `find`, `cp`, `sha256sum` or `shasum`, `date`
- Write access to target repository
- Basic understanding of conflict resolution (for upgrades)

### For Framework Guardian Operations

- Python 3.8+ with framework dependencies
- Access to `META/MANIFEST.yml` from release artifact
- `.framework_meta.yml` present in target repository (for audits)

---

## Quickstart: End-to-End Example

**Scenario:** You're releasing version 1.2.0 and installing it in a new downstream repository.

```bash
# 1. BUILD: Create release artifact
cd ~/quickstart_agent-augmented-development
python ops/release/build_release_artifact.py --version 1.2.0

# 2. VERIFY: Check artifact integrity
cd output/releases
sha256sum -c checksums.txt
unzip -l quickstart-framework-1.2.0.zip | grep META

# 3. PUBLISH: Upload to GitHub Releases (manual or CI/CD)
# (GitHub Actions workflow handles this automatically for tagged releases)

# 4. INSTALL: Deploy to new repository
cd ~/my-new-project
wget https://github.com/org/repo/releases/download/v1.2.0/quickstart-framework-1.2.0.zip
unzip quickstart-framework-1.2.0.zip
cd quickstart-framework-1.2.0
./scripts/framework_install.sh --dry-run . ~/my-new-project  # Preview first
./scripts/framework_install.sh . ~/my-new-project           # Execute

# 5. VERIFY: Confirm installation
cat ~/my-new-project/.framework_meta.yml

# 6. VALIDATE: Run Framework Guardian audit (optional)
# (Future: Guardian agent invocation for compliance check)
```

**Time estimate:** 15-30 minutes for first-time release managers; 5-10 minutes for experienced teams.

---

## Deep Dive: Build Release Artifact

### Overview

The `build_release_artifact.py` script assembles framework files, generates checksums, and creates a distributable zip package.

### Command Reference

```bash
python ops/release/build_release_artifact.py --version VERSION [OPTIONS]

Options:
  --version VERSION       Semantic version (e.g., 1.0.0, 1.0.0-rc.1)
  --output-dir DIR        Output directory (default: output/releases)
  --repo-root PATH        Repository root (default: current directory)
  --dry-run               Validate without creating files
  --profile PROFILE       Use predefined config profile (minimal, standard, full)
  --config FILE           Custom distribution config YAML
```

### Step-by-Step Process

#### 1. Prepare Repository

```bash
# Ensure clean working tree
git status

# Create a release branch (recommended)
git checkout -b release/v1.2.0

# Update version references if needed
# (e.g., update AGENTS.md, README.md with new version)
```

#### 2. Run Dry-Run Validation

```bash
# Preview what will be included
python ops/release/build_release_artifact.py \
    --version 1.2.0 \
    --dry-run

# Expected output:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DRY RUN - No files will be created
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✓ Repository structure validated
# ✓ Found 329 files in framework_core/
# ✓ Manifest would include 329 files (2.8 MB total)
# ✓ Metadata generated with commit: abc123...
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 3. Build Release Artifact

```bash
# Create the release package
python ops/release/build_release_artifact.py --version 1.2.0

# Output location: output/releases/quickstart-framework-1.2.0.zip
```

#### 4. Review Build Output

```bash
cd output/releases

# Verify files created
ls -lh
# Expected:
# quickstart-framework-1.2.0.zip      (compressed artifact)
# checksums.txt                        (SHA256 checksums)

# Check artifact size (typical: 500KB - 2MB compressed)
du -h quickstart-framework-1.2.0.zip
```

### What Gets Included

The artifact contains:

```
quickstart-framework-1.2.0.zip
├── framework_core/           # Core framework files
│   ├── .github/agents/       # Agent profiles and directives
│   ├── docs/                 # Templates and architecture
│   ├── framework/            # Python framework code
│   ├── validation/           # Validation scripts
│   ├── work/templates/       # Work item templates
│   ├── AGENTS.md             # Coordination protocol
│   ├── README.md             # Framework documentation
│   ├── pyproject.toml        # Python config
│   └── requirements.txt      # Dependencies
├── scripts/                  # Installation scripts
│   ├── framework_install.sh
│   └── framework_upgrade.sh
└── META/                     # Release metadata
    ├── MANIFEST.yml          # File checksums
    ├── metadata.json         # Build info
    └── RELEASE_NOTES.md      # Version notes
```

### What Gets Excluded

Per `build_release_artifact.py` configuration:

- Version control: `.git/`, `.gitignore`
- Python cache: `__pycache__/`, `*.pyc`, `.pytest_cache/`
- Work outputs: `work/logs/`, `work/reports/`, `work/collaboration/`
- Local overrides: `local/` directory
- Temporary files: `tmp/`, `output/`
- IDE files: `.vscode/`, `.idea/`, `.claude/`
- Build artifacts: `dist/`, `*.egg-info/`

### Troubleshooting Build

#### Error: "Invalid repository structure"

**Cause:** Running from wrong directory or missing required directories.

**Fix:**
```bash
# Run from repository root
cd ~/quickstart_agent-augmented-development
python ops/release/build_release_artifact.py --version 1.2.0

# Or specify repo root explicitly
python ops/release/build_release_artifact.py \
    --version 1.2.0 \
    --repo-root /path/to/repo
```

#### Error: "Invalid version format"

**Cause:** Version doesn't follow semantic versioning.

**Fix:**
```bash
# Correct formats:
--version 1.0.0           # Release
--version 1.0.0-rc.1      # Release candidate
--version 1.0.0-alpha.1   # Alpha
--version 1.0.0+20260131  # With build metadata

# Incorrect formats:
--version v1.0.0          # Don't use 'v' prefix
--version 1.0             # Must be X.Y.Z
```

#### Warning: "Uncommitted changes detected"

**Cause:** Git working tree has modifications.

**Effect:** Git commit hash in metadata may not reflect actual content.

**Fix:**
```bash
# Commit or stash changes
git add .
git commit -m "Prepare v1.2.0 release"

# Or continue with warning (not recommended for production releases)
```

---

## Deep Dive: Verify and Publish

### Artifact Verification

#### 1. Checksum Verification

```bash
cd output/releases

# Verify artifact integrity
sha256sum -c checksums.txt

# Expected output:
# quickstart-framework-1.2.0.zip: OK
```

#### 2. Structure Verification

```bash
# Inspect zip contents without extracting
unzip -l quickstart-framework-1.2.0.zip | head -30

# Verify critical components present
unzip -l quickstart-framework-1.2.0.zip | grep -E "(META/MANIFEST|scripts/framework_install|framework_core/AGENTS.md)"

# Expected:
# META/MANIFEST.yml
# scripts/framework_install.sh
# scripts/framework_upgrade.sh
# framework_core/AGENTS.md
```

#### 3. Manifest Inspection

```bash
# Extract and examine manifest
unzip -q quickstart-framework-1.2.0.zip
cd quickstart-framework-1.2.0

# Check manifest metadata
head -20 META/MANIFEST.yml

# Expected:
# version: 1.2.0
# generated_at: '2026-01-31T12:00:00+00:00'
# files:
#   - path: AGENTS.md
#     sha256: abc123...
#     mode: '664'
#     scope: core
# total_files: 329
```

#### 4. Metadata Inspection

```bash
# Review build metadata
cat META/metadata.json

# Verify:
# - version matches intended release
# - git_commit is correct
# - git_branch is expected (main, release/vX.Y.Z)
# - build_date is recent
```

### Publishing Release

#### Manual GitHub Release

```bash
# 1. Create and push tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# 2. Upload artifact to GitHub Releases
# - Go to https://github.com/org/repo/releases/new
# - Select tag v1.2.0
# - Upload quickstart-framework-1.2.0.zip
# - Upload checksums.txt
# - Add release notes from META/RELEASE_NOTES.md
# - Publish release
```

#### Automated CI/CD Publishing

If using GitHub Actions (see `.github/workflows/release-packaging.yml`):

```bash
# Tag triggers automated build and release
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# GitHub Actions will:
# 1. Build artifact
# 2. Run acceptance tests
# 3. Create GitHub Release
# 4. Upload artifact and checksums
# 5. Notify stakeholders
```

#### Internal Distribution

For organizations with internal artifact repositories:

```bash
# Upload to internal storage
aws s3 cp quickstart-framework-1.2.0.zip \
    s3://company-artifacts/framework/releases/

# Or Artifactory/Nexus
curl -u user:token -T quickstart-framework-1.2.0.zip \
    "https://artifactory.company.com/framework/v1.2.0/"
```

### Post-Publication Checklist

- [ ] Artifact uploaded and accessible
- [ ] Checksums verified after upload
- [ ] Release notes published
- [ ] Download link tested from clean environment
- [ ] Internal teams notified (Slack, email, etc.)
- [ ] Documentation updated with new version
- [ ] Installation guide tested with new artifact

---

## Deep Dive: Install Framework

See [Framework Installation Guide](framework_install.md) for comprehensive installation instructions.

### Quick Reference

```bash
# Extract release
unzip quickstart-framework-1.2.0.zip
cd quickstart-framework-1.2.0

# Preview installation
./scripts/framework_install.sh --dry-run . /path/to/target/repo

# Execute installation
./scripts/framework_install.sh . /path/to/target/repo

# Verify
cat /path/to/target/repo/.framework_meta.yml
```

### Expected Outcomes

- **NEW files**: Copied from release to target
- **EXISTING files**: Skipped (never overwritten)
- **Metadata**: `.framework_meta.yml` created with version info
- **Summary**: Report shows NEW and SKIPPED counts

### Installation Verification

```bash
cd /path/to/target/repo

# 1. Check metadata
cat .framework_meta.yml
# framework_version: 1.2.0
# installed_at: 2026-01-31T14:30:00Z

# 2. Verify key files present
test -f AGENTS.md && echo "✓ AGENTS.md"
test -d .github/agents && echo "✓ Agent profiles"
test -d framework && echo "✓ Framework code"

# 3. Test framework initialization (if Python framework)
python -c "import framework.core; print('✓ Framework imports')"
```

---

## Deep Dive: Upgrade Framework

### Overview

Upgrading existing framework installations requires careful conflict management. The `framework_upgrade.sh` script intelligently handles:

- **NEW files**: Missing in target → copied
- **UNCHANGED files**: Checksums match → skipped
- **CONFLICT files**: Content differs → creates `.framework-new`
- **PROTECTED files**: In `local/` → never touched

See [Framework Installation Guide - Upgrade Section](framework_install.md#upgrade) for full details.

### Step-by-Step Upgrade

#### 1. Pre-Upgrade Preparation

```bash
# Backup current state
cd /path/to/target/repo
git add . && git commit -m "Pre-upgrade snapshot for v1.2.0"

# Verify current version
cat .framework_meta.yml
# framework_version: 1.1.0

# Document local customizations
find . -path ./local -prune -o -name "*.local.*" -print
```

#### 2. Preview Upgrade

```bash
# Extract new release
cd ~/downloads
unzip quickstart-framework-1.2.0.zip
cd quickstart-framework-1.2.0

# Dry-run to see what would change
./scripts/framework_upgrade.sh --dry-run . /path/to/target/repo

# Expected output:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DRY RUN - No files will be modified
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Would be:
#   NEW:        15 files
#   UNCHANGED:  305 files
#   CONFLICT:   9 files
#   PROTECTED:  3 files (local/)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 3. Execute Upgrade

```bash
# Run upgrade with verbose output
./scripts/framework_upgrade.sh --verbose . /path/to/target/repo

# Upgrade creates:
# - upgrade-report.txt          (detailed status for each file)
# - .framework-new files        (conflicted content)
# - .bak.TIMESTAMP backups      (originals before conflicts)
```

#### 4. Review Upgrade Report

```bash
cd /path/to/target/repo
cat upgrade-report.txt

# Look for:
# - NEW: Files added in v1.2.0
# - CONFLICT: Files requiring manual review
# - PROTECTED: Your local customizations (untouched)
```

#### 5. Resolve Conflicts

```bash
# Find all conflicts
find . -name "*.framework-new" -type f

# For each conflict:
# a) View differences
diff .github/agents/devops-danny.agent.md \
     .github/agents/devops-danny.agent.md.framework-new

# b) Choose resolution strategy:

# Option A: Accept new version
mv .github/agents/devops-danny.agent.md.framework-new \
   .github/agents/devops-danny.agent.md

# Option B: Keep current version
rm .github/agents/devops-danny.agent.md.framework-new

# Option C: Merge manually
vimdiff .github/agents/devops-danny.agent.md \
        .github/agents/devops-danny.agent.md.framework-new
# After merging, remove .framework-new file
```

#### 6. Verify Upgrade Completion

```bash
# No conflicts remaining
find . -name "*.framework-new" -type f
# (Should return empty)

# Version updated
cat .framework_meta.yml
# framework_version: 1.2.0
# upgraded_at: 2026-01-31T15:45:00Z

# Commit upgrade
git add .
git commit -m "Upgrade framework to v1.2.0"
```

### Conflict Resolution Strategies

#### Strategy 1: Framework Takes Precedence

**Use when:** Core framework files changed for bug fixes or critical updates.

```bash
# Accept all framework updates
find . -name "*.framework-new" -type f | while read new_file; do
    original="${new_file%.framework-new}"
    mv "$new_file" "$original"
done
```

#### Strategy 2: Local Customizations Preserved

**Use when:** Your modifications are intentional and must persist.

```bash
# Reject all framework updates
find . -name "*.framework-new" -type f -delete

# Consider moving customizations to local/
mkdir -p local/agents
cp .github/agents/custom-agent.agent.md local/agents/
```

#### Strategy 3: Selective Merge

**Use when:** Both framework and local changes are valuable.

```bash
# Use three-way merge tool
git merge-file \
    .github/agents/devops-danny.agent.md \
    .github/agents/devops-danny.agent.md.bak.20260131_154500 \
    .github/agents/devops-danny.agent.md.framework-new

# Or interactive merge
meld .github/agents/devops-danny.agent.md \
     .github/agents/devops-danny.agent.md.framework-new
```

### Rollback Procedure

If upgrade causes issues:

```bash
# 1. Revert to pre-upgrade commit
git log --oneline -10
git reset --hard <commit-before-upgrade>

# 2. Or restore from backups
find . -name "*.bak.*" -type f | while read backup; do
    original="${backup%.bak.*}"
    cp "$backup" "$original"
done

# 3. Remove .framework-new files
find . -name "*.framework-new" -type f -delete

# 4. Verify rollback
cat .framework_meta.yml
# Should show previous version
```

---

## Deep Dive: Framework Guardian Validation

### Overview

The **Framework Guardian** agent audits framework installations and guides upgrade conflict resolution. See [Framework Guardian Profile](../../.github/agents/framework-guardian.agent.md) for full specification.

### Audit Mode

**Purpose:** Verify framework installation integrity and detect drift from canonical manifest.

#### Running an Audit

```bash
# Future implementation - Guardian agent invocation
# Expected workflow:

# 1. Create Guardian task
cat > work/inbox/framework-guardian/audit-request.yaml <<EOF
id: 2026-01-31T1600-guardian-audit
agent: framework-guardian
priority: medium
mode: /analysis-mode
title: Audit framework installation integrity
requirements:
  - Compare installed files against META/MANIFEST.yml
  - Detect missing, diverged, and custom files
  - Generate validation/FRAMEWORK_AUDIT_REPORT.md
EOF

# 2. Invoke Guardian (via Manager Mike iteration)
# See: .github/ISSUE_TEMPLATE/run-iteration.md

# 3. Review audit report
cat validation/FRAMEWORK_AUDIT_REPORT.md
```

#### Audit Report Contents

```markdown
# Framework Audit Report

## Summary
- Framework Version: 1.2.0
- Audit Date: 2026-01-31T16:00:00Z
- Total Manifest Files: 329
- Status: ⚠️ 3 files diverged, 2 files missing

## File Status

| Status | Count | Description |
|--------|-------|-------------|
| UNCHANGED | 324 | Match manifest checksum |
| DIVERGED | 3 | Local modifications detected |
| MISSING | 2 | Expected but not found |
| CUSTOM | 15 | Present but not in manifest |

## Diverged Files

1. `.github/agents/devops-danny.agent.md`
   - Expected SHA256: abc123...
   - Actual SHA256: def456...
   - **Recommendation:** Review changes; consider moving to `local/` if intentional

## Missing Files

1. `docs/templates/automation/CI_PIPELINE.md`
   - **Recommendation:** Re-run upgrade or install missing file manually

## Action Items

- [ ] Review diverged files and decide: keep, revert, or relocate to `local/`
- [ ] Install missing files from release artifact
- [ ] Document intentional customizations in `local/README.md`
```

### Upgrade Mode

**Purpose:** Generate conflict resolution plan with minimal, actionable patches.

#### Running Upgrade Guidance

```bash
# 1. Run upgrade with --plan flag
./scripts/framework_upgrade.sh --plan . /path/to/target/repo

# 2. Create Guardian task for conflict analysis
cat > work/inbox/framework-guardian/upgrade-plan-request.yaml <<EOF
id: 2026-01-31T1700-guardian-upgrade
agent: framework-guardian
priority: high
mode: /creative-mode
title: Generate upgrade conflict resolution plan
requirements:
  - Analyze all .framework-new conflicts
  - Classify by merge complexity
  - Propose minimal patches
  - Generate validation/FRAMEWORK_UPGRADE_PLAN.md
context:
  upgrade_from: 1.1.0
  upgrade_to: 1.2.0
  conflicts: 9
EOF

# 3. Review upgrade plan
cat validation/FRAMEWORK_UPGRADE_PLAN.md
```

#### Upgrade Plan Contents

```markdown
# Framework Upgrade Plan: v1.1.0 → v1.2.0

## Summary
- Total Conflicts: 9
- Auto-Merge Candidates: 5
- Manual Review Required: 3
- Breaking Changes: 1

## Conflict Classification

### Auto-Merge (5 files)

Conflicts with trivial differences (whitespace, comments, formatting).

1. **`.github/agents/curator-claire.agent.md`**
   - **Conflict Type:** Whitespace only
   - **Recommendation:** Accept framework version
   - **Command:** `mv .github/agents/curator-claire.agent.md.framework-new .github/agents/curator-claire.agent.md`

### Manual Review (3 files)

2. **`.github/agents/devops-danny.agent.md`**
   - **Conflict Type:** Local customization (custom tool added)
   - **Framework Change:** Updated directive references
   - **Recommendation:** Merge manually or relocate tool to `local/agents/devops-danny.local.md`
   - **Diff Highlights:**
     ```diff
     + tools: [ "read", "write", "bash", "custom-deployment-tool" ]  # Your addition
     - Directive 005  # Framework removed deprecated directive
     + Directive 020  # Framework added new directive
     ```

### Breaking Changes (1 file)

3. **`framework/core.py`**
   - **Change Type:** API signature change
   - **Impact:** Custom scripts using `load_context()` must update
   - **Migration:**
     ```python
     # Old: load_context(repo_path)
     # New: load_context(repo_path, config=None)
     ```
   - **Recommendation:** Review all `import framework.core` usage

## Suggested Workflow

1. Apply auto-merge candidates (low risk)
2. Review manual merge files with domain expert
3. Test breaking changes in isolated environment
4. Update local customizations to use `local/` directory
5. Commit incrementally with clear messages
```

### Guardian Integration Points

#### With Iteration Workflow

Framework Guardian fits into the iteration cycle as a validation step:

```yaml
# .github/ISSUE_TEMPLATE/run-iteration.md snippet
# After upgrade task completion:

- [ ] Run Framework Guardian audit
- [ ] Review Guardian reports
- [ ] Resolve flagged conflicts
- [ ] Update AGENT_STATUS.md with Guardian findings
```

#### With Release Checklist

See [Release Publishing Checklist](../checklists/release_publishing_checklist.md) for Guardian invocation steps during release workflow.

---

## Integration with Iteration Workflow

### Release Tasks in Iteration Cycles

When Manager Mike processes iteration tasks, release-related activities follow this pattern:

#### Task 1: Build Release Artifact

```yaml
# work/inbox/build-automation/build-release-v1-2-0.yaml
id: 2026-01-31T1400-build-release
agent: build-automation
priority: high
title: Build framework release v1.2.0
requirements:
  - Run build_release_artifact.py
  - Verify artifact integrity
  - Generate build report
artefacts:
  - output/releases/quickstart-framework-1.2.0.zip
  - output/releases/checksums.txt
```

**Completion criteria:**
- [ ] Artifact created and checksums verified
- [ ] Build report generated in `work/reports/`
- [ ] Work log created per Directive 014

#### Task 2: Publish Release

```yaml
# work/inbox/build-automation/publish-release-v1-2-0.yaml
id: 2026-01-31T1500-publish-release
agent: build-automation
priority: high
title: Publish framework release v1.2.0 to GitHub
dependencies:
  - 2026-01-31T1400-build-release
requirements:
  - Upload artifact to GitHub Releases
  - Update release notes
  - Notify downstream teams
artefacts:
  - GitHub Release URL
  - Notification log
```

#### Task 3: Framework Guardian Audit

```yaml
# work/inbox/framework-guardian/audit-post-release.yaml
id: 2026-01-31T1600-guardian-audit
agent: framework-guardian
priority: medium
title: Audit release artifact integrity
dependencies:
  - 2026-01-31T1500-publish-release
requirements:
  - Verify MANIFEST.yml completeness
  - Validate metadata consistency
  - Generate audit report
artefacts:
  - validation/FRAMEWORK_AUDIT_REPORT.md
```

### Manager Mike's Release Summary

After completing release tasks, Manager Mike creates an iteration summary:

```markdown
# Iteration Summary: Release v1.2.0

## Tasks Completed
1. ✅ Build release artifact (build-automation)
2. ✅ Publish to GitHub Releases (build-automation)
3. ✅ Guardian audit passed (framework-guardian)

## Metrics
- Build time: 2m 15s
- Artifact size: 1.2 MB (compressed)
- Files packaged: 329
- Checksum verification: ✓ PASS

## Guardian Findings
- Installation integrity: ✓ PASS
- Manifest completeness: ✓ PASS (329/329 files)
- No drift detected in release artifact

## Communication
- [X] Release notes published
- [X] Downstream teams notified (Slack #framework-releases)
- [X] Documentation updated with v1.2.0 links

## Next Steps
- Monitor downstream adoption
- Address upgrade conflicts as reported
- Schedule post-release retrospective
```

### Cross-Linking with run-iteration.md

The iteration template references this guide:

```markdown
## Release-Specific Instructions

When processing release tasks:
1. Follow [Release and Upgrade Workflow Guide](docs/HOW_TO_USE/release_and_upgrade.md)
2. Use [Release Publishing Checklist](docs/checklists/release_publishing_checklist.md)
3. Invoke Framework Guardian for validation
4. Update release notes per template
```

---

## Troubleshooting

### Build Issues

#### Problem: "Python module 'yaml' not found"

**Solution:**
```bash
pip install pyyaml
# Or install framework dependencies
pip install -r requirements.txt
```

#### Problem: Build succeeds but manifest is incomplete

**Symptoms:** Missing expected files in MANIFEST.yml.

**Solution:**
```bash
# Check exclusion patterns
python ops/release/build_release_artifact.py --version 1.2.0 --dry-run | grep "excluded"

# Review EXCLUDE_PATTERNS in build_release_artifact.py
# Ensure your files aren't accidentally excluded
```

### Installation Issues

#### Problem: Installation script fails with "Permission denied"

**Solution:**
```bash
# Ensure script is executable
chmod +x scripts/framework_install.sh

# Check target directory permissions
ls -ld /path/to/target/repo
# Should be writable by current user
```

#### Problem: Files installed but .framework_meta.yml not created

**Symptoms:** Framework files present but no metadata.

**Diagnosis:** Script may have crashed before metadata write.

**Solution:**
```bash
# Check script output for errors
./scripts/framework_install.sh . /path/to/repo 2>&1 | tee install.log

# Manually create metadata if needed (not recommended)
cat > /path/to/repo/.framework_meta.yml <<EOF
framework_version: 1.2.0
installed_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
source_release: quickstart-framework-1.2.0
installer_version: 1.0.0
EOF
```

### Upgrade Issues

#### Problem: Excessive conflicts (50+ files)

**Symptoms:** Nearly every file marked as CONFLICT.

**Diagnosis:** May indicate:
- Wrong release artifact for upgrade
- Major framework refactor
- Corruption or checksum issues

**Solution:**
```bash
# 1. Verify current version
cat .framework_meta.yml

# 2. Check upgrade path compatibility
# e.g., v1.0.0 → v1.2.0 should be compatible
# but v1.0.0 → v2.0.0 may have breaking changes

# 3. Consider fresh installation instead
# Backup local customizations first:
git diff > local-changes.patch
# Then fresh install + reapply local changes
```

#### Problem: "No existing framework installation found" during upgrade

**Cause:** Missing `.framework_meta.yml`.

**Solution:**
```bash
# If framework was manually installed:
# 1. Create metadata file
cat > .framework_meta.yml <<EOF
framework_version: 1.1.0  # Set to current version
installed_at: 2026-01-01T00:00:00Z
source_release: unknown
installer_version: 1.0.0
EOF

# 2. Re-run upgrade
./scripts/framework_upgrade.sh . /path/to/repo
```

### Guardian Issues

#### Problem: Guardian audit reports false positives

**Symptoms:** Files flagged as DIVERGED but changes are intentional.

**Solution:**
```bash
# Move intentional customizations to local/
mkdir -p local/agents
cp .github/agents/custom-agent.agent.md local/agents/

# Update references to use local path
# Guardian won't flag files in local/
```

#### Problem: Guardian upgrade plan not generated

**Cause:** No `.framework-new` files found.

**Solution:**
```bash
# Verify conflicts exist
find . -name "*.framework-new" -type f

# If none found, upgrade had no conflicts:
cat upgrade-report.txt | grep "CONFLICT"
# Should show count

# Guardian only generates plans when conflicts exist
```

---

## Best Practices

### For Release Managers

1. **Version Discipline**
   - Use semantic versioning strictly
   - Tag releases in Git before building
   - Maintain CHANGELOG.md with version notes

2. **Build Hygiene**
   - Always run `--dry-run` before production builds
   - Verify checksums immediately after build
   - Test installation in clean environment before publishing

3. **Communication**
   - Announce releases via changelog and notifications
   - Document breaking changes prominently
   - Provide migration guides for major versions

4. **Automation**
   - Use CI/CD for consistent builds
   - Automate checksum verification
   - Integrate Guardian audits into release pipeline

### For Downstream Teams

1. **Pre-Upgrade Planning**
   - Review release notes before upgrading
   - Backup current state (Git commit)
   - Run dry-run to preview conflicts
   - Schedule dedicated time for conflict resolution

2. **Conflict Management**
   - Use Guardian upgrade plans when available
   - Resolve conflicts incrementally (commit after each file)
   - Document resolution decisions in commit messages
   - Keep backup files until verification complete

3. **Local Customizations**
   - Use `local/` directory for project-specific overrides
   - Document customizations in `local/README.md`
   - Minimize framework file modifications
   - Consider contributing common patterns upstream

4. **Validation**
   - Run Guardian audit after installation/upgrade
   - Test framework functionality before committing
   - Verify version in `.framework_meta.yml`
   - Check for orphaned `.framework-new` or `.bak.*` files

### For Framework Developers

1. **Breaking Change Management**
   - Avoid breaking changes in patch versions (X.Y.Z → X.Y.Z+1)
   - Document breaking changes in RELEASE_NOTES.md
   - Provide migration scripts when possible
   - Consider deprecation warnings before removals

2. **Manifest Integrity**
   - Include all distributed files in MANIFEST.yml
   - Verify checksums during build
   - Mark scope correctly (`core` vs `template`)
   - Keep manifest schema stable

3. **Guardian Integration**
   - Design for Guardian analysis (clear diff boundaries)
   - Use structured formats for configuration files
   - Separate core logic from customization points
   - Document expected customization patterns

---

## References

### Architecture Documents

- [ADR-013: Zip-Based Framework Distribution](../architecture/adrs/ADR-013-zip-distribution.md)
- [ADR-014: Framework Guardian Agent](../architecture/adrs/ADR-014-framework-guardian-agent.md)
- [Distribution Architecture](../architecture/design/distribution_of_releases_architecture.md)
- [Distribution Technical Design](../architecture/design/distribution_of_releases_technical_design.md)

### Operational Documents

- [Framework Installation Guide](framework_install.md) - Detailed install/upgrade instructions
- [Release Packaging README](../../ops/release/README.md) - Build script documentation
- [Release Publishing Checklist](../checklists/release_publishing_checklist.md) - Step-by-step verification
- [Framework Guardian Profile](../../.github/agents/framework-guardian.agent.md) - Agent specification

### Templates and Workflows

- [Run Iteration Template](../../.github/ISSUE_TEMPLATE/run-iteration.md) - Orchestration cycle
- [Release Notes Template](../templates/RELEASE_NOTES.md) - Version documentation
- [Guardian Audit Report Template](../templates/GUARDIAN_AUDIT_REPORT.md)
- [Guardian Upgrade Plan Template](../templates/GUARDIAN_UPGRADE_PLAN.md)

### Scripts

- `ops/release/build_release_artifact.py` - Build script
- `ops/release/framework_install.sh` - Installation script
- `ops/release/framework_upgrade.sh` - Upgrade script
- `work/scripts/agent_orchestrator.py` - Task assignment

### Directives

- Directive 014: Work Log Creation
- Directive 018: Documentation Level Framework
- Directive 020: Lenient Adherence
- Directive 021: Locality of Change
- Directive 022: Audience-Oriented Writing
- Directive 025: Framework Guardian

---

## Appendix: Version History

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.0.0   | 2026-01-31 | Initial release covering full workflow       |

---

**Maintained by:** Agentic Framework Core Team  
**Target Audience:** Release managers, downstream adopters, framework developers  
**Feedback:** Create an issue or submit a PR to improve this guide  
**Related Support:** See [Troubleshooting](#troubleshooting) section above
