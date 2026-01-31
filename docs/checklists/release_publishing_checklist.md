# Release Publishing Checklist

## Target Audience

**Primary:** Release managers and framework core team members  
**Secondary:** DevOps engineers handling framework distribution

**Purpose:** Ensure consistent, error-free releases with complete validation and communication.

---

## Overview

This checklist guides you through the complete release publishing process from build to post-release validation. Follow each section sequentially and mark items as completed.

**Estimated Time:**
- First-time release: 45-60 minutes
- Experienced release manager: 20-30 minutes

**Related Documents:**
- [Release and Upgrade Workflow Guide](../HOW_TO_USE/release_and_upgrade.md) - Detailed procedures
- [Framework Installation Guide](../HOW_TO_USE/framework_install.md) - Installation reference
- [Release Packaging README](../../ops/release/README.md) - Build script docs

---

## Pre-Release Preparation

### Version Planning

- [ ] **Determine version number** following semantic versioning:
  - `X.Y.Z` for releases (e.g., `1.2.0`)
  - `X.Y.Z-rc.N` for release candidates (e.g., `1.2.0-rc.1`)
  - `X.Y.Z-alpha.N` or `-beta.N` for pre-releases
  
- [ ] **Review CHANGELOG.md** for version completeness:
  - All features documented
  - Breaking changes highlighted
  - Bug fixes listed
  - Contributors acknowledged

- [ ] **Update version references** across documentation:
  - [ ] `README.md` - version badge/reference
  - [ ] `AGENTS.md` - framework version section
  - [ ] `docs/VISION.md` - roadmap version markers
  - [ ] Any other version-specific docs

- [ ] **Create release branch** (recommended for major/minor releases):
  ```bash
  git checkout -b release/v1.2.0
  git push -u origin release/v1.2.0
  ```

### Code Freeze

- [ ] **Verify clean working tree:**
  ```bash
  git status
  # Should show: "nothing to commit, working tree clean"
  ```

- [ ] **All CI/CD pipelines passing:**
  - [ ] Unit tests
  - [ ] Integration tests
  - [ ] Acceptance tests
  - [ ] Linting/formatting checks
  - [ ] Security scans (if configured)

- [ ] **No open critical or high-priority bugs** targeting this release

- [ ] **All PRs merged** for planned features/fixes

---

## Build Release Artifact

### Dry-Run Validation

- [ ] **Run build script in dry-run mode:**
  ```bash
  python ops/release/build_release_artifact.py \
      --version 1.2.0 \
      --dry-run
  ```

- [ ] **Verify dry-run output shows expected file count:**
  - Typical range: 300-350 files for standard framework
  - Check for unexpected exclusions or inclusions

- [ ] **Review directories included:**
  - [ ] `.github/agents/` (agent profiles and directives)
  - [ ] `docs/templates/` (document templates)
  - [ ] `docs/architecture/` (ADRs and designs)
  - [ ] `framework/` (Python framework code)
  - [ ] `validation/` (validation scripts)
  - [ ] `work/templates/` (task templates)

- [ ] **Verify exclusions working correctly:**
  - [ ] No `work/logs/` or `work/reports/`
  - [ ] No `local/` directories
  - [ ] No `.git/` or `__pycache__/`
  - [ ] No IDE files (`.vscode/`, `.idea/`)

### Execute Build

- [ ] **Run build script:**
  ```bash
  python ops/release/build_release_artifact.py --version 1.2.0
  ```

- [ ] **Capture build output:**
  ```bash
  python ops/release/build_release_artifact.py --version 1.2.0 \
      2>&1 | tee build-log-v1.2.0.txt
  ```

- [ ] **Verify build success message displayed**

- [ ] **Check output directory:**
  ```bash
  ls -lh output/releases/
  # Should show:
  # quickstart-framework-1.2.0.zip
  # checksums.txt
  ```

---

## Artifact Verification

### Checksum Validation

- [ ] **Verify artifact integrity:**
  ```bash
  cd output/releases
  sha256sum -c checksums.txt
  # Expected: "quickstart-framework-1.2.0.zip: OK"
  ```

- [ ] **Record checksums** for publication (copy from `checksums.txt`)

### Structure Inspection

- [ ] **Inspect archive contents:**
  ```bash
  unzip -l quickstart-framework-1.2.0.zip | less
  ```

- [ ] **Verify critical files present:**
  ```bash
  unzip -l quickstart-framework-1.2.0.zip | grep -E \
      "(META/MANIFEST|META/metadata|scripts/framework_install|framework_core/AGENTS)"
  
  # Expected output should include:
  # META/MANIFEST.yml
  # META/metadata.json
  # META/RELEASE_NOTES.md
  # scripts/framework_install.sh
  # scripts/framework_upgrade.sh
  # framework_core/AGENTS.md
  # framework_core/README.md
  ```

- [ ] **Check artifact size** (typical compressed size: 500KB - 2MB):
  ```bash
  du -h quickstart-framework-1.2.0.zip
  ```

### Metadata Validation

- [ ] **Extract and inspect manifest:**
  ```bash
  unzip -q quickstart-framework-1.2.0.zip
  cd quickstart-framework-1.2.0
  head -30 META/MANIFEST.yml
  ```

- [ ] **Verify manifest metadata:**
  - [ ] `version:` matches intended release version
  - [ ] `generated_at:` is recent timestamp
  - [ ] `total_files:` is reasonable (300-350 for standard framework)
  - [ ] `total_size:` is consistent with file count

- [ ] **Inspect build metadata:**
  ```bash
  cat META/metadata.json
  ```

- [ ] **Verify metadata.json fields:**
  - [ ] `version` matches release version
  - [ ] `git_commit` is correct commit hash
  - [ ] `git_branch` is expected (main or release/vX.Y.Z)
  - [ ] `build_date` is recent

- [ ] **Review release notes:**
  ```bash
  cat META/RELEASE_NOTES.md
  ```

- [ ] **Verify release notes completeness:**
  - [ ] Version and date correct
  - [ ] Changes summarized appropriately
  - [ ] Breaking changes clearly marked
  - [ ] Migration instructions (if applicable)
  - [ ] Guardian metadata included (see template)

### Installation Scripts Validation

- [ ] **Verify scripts are executable:**
  ```bash
  ls -l scripts/framework_install.sh scripts/framework_upgrade.sh
  # Should show: -rwxr-xr-x (executable bit set)
  ```

- [ ] **Check script versions match:**
  ```bash
  grep -E "^VERSION=" scripts/framework_install.sh
  grep -E "^VERSION=" scripts/framework_upgrade.sh
  # Versions should be compatible with release
  ```

---

## Test Installation

### Prepare Test Environment

- [ ] **Create clean test directory:**
  ```bash
  mkdir -p ~/test-framework-install
  cd ~/test-framework-install
  git init  # Or use existing test repo
  ```

- [ ] **Copy artifact to test location:**
  ```bash
  cp output/releases/quickstart-framework-1.2.0.zip ~/test-framework-install/
  cd ~/test-framework-install
  unzip quickstart-framework-1.2.0.zip
  ```

### Test Fresh Installation

- [ ] **Run installation in dry-run mode:**
  ```bash
  cd quickstart-framework-1.2.0
  ./scripts/framework_install.sh --dry-run . ~/test-framework-install/test-repo
  ```

- [ ] **Review dry-run output for sanity:**
  - Expected NEW count matches manifest total_files
  - No unexpected errors or warnings

- [ ] **Execute installation:**
  ```bash
  ./scripts/framework_install.sh --verbose . ~/test-framework-install/test-repo \
      2>&1 | tee install-test.log
  ```

- [ ] **Verify installation success:**
  ```bash
  cd ~/test-framework-install/test-repo
  cat .framework_meta.yml
  # Should show correct version and recent timestamp
  ```

- [ ] **Spot-check installed files:**
  ```bash
  test -f AGENTS.md && echo "✓ AGENTS.md"
  test -d .github/agents && echo "✓ Agent profiles"
  test -d framework && echo "✓ Framework code"
  test -f pyproject.toml && echo "✓ Python config"
  ```

- [ ] **Test framework functionality (if applicable):**
  ```bash
  # If Python framework:
  python -c "import framework.core; print('✓ Framework imports')"
  
  # If includes validation:
  python validation/smoke_test.py
  ```

### Test Upgrade (if existing installation available)

- [ ] **Prepare test upgrade environment** (skip if no prior version):
  ```bash
  # Install previous version first in separate directory
  # Then run upgrade test
  ```

- [ ] **Run upgrade dry-run:**
  ```bash
  ./scripts/framework_upgrade.sh --dry-run . ~/test-upgrade-repo
  ```

- [ ] **Execute upgrade:**
  ```bash
  ./scripts/framework_upgrade.sh --verbose . ~/test-upgrade-repo \
      2>&1 | tee upgrade-test.log
  ```

- [ ] **Review upgrade report:**
  ```bash
  cat ~/test-upgrade-repo/upgrade-report.txt
  # Check for expected NEW, UNCHANGED, CONFLICT counts
  ```

- [ ] **Verify version updated:**
  ```bash
  cat ~/test-upgrade-repo/.framework_meta.yml
  # Should show new version
  ```

---

## Framework Guardian Audit

### Pre-Publication Guardian Check

- [ ] **Run Guardian audit on release artifact** (if available):
  ```bash
  # Create Guardian task in work/inbox/
  # Or invoke Guardian manually if implemented
  ```

- [ ] **Review Guardian audit report:**
  ```bash
  cat validation/FRAMEWORK_AUDIT_REPORT.md
  ```

- [ ] **Verify audit findings:**
  - [ ] Manifest completeness: 100%
  - [ ] No critical integrity issues
  - [ ] No missing required files
  - [ ] Total file count matches expected

- [ ] **Document Guardian metadata** for release notes:
  - Audit date/time
  - Framework version validated
  - Audit status (PASS/WARN/FAIL)
  - Any action items for consumers

### Example Guardian Metadata Block

```yaml
# Include in META/RELEASE_NOTES.md
guardian_metadata:
  audit_date: 2026-01-31T18:00:00Z
  framework_version: 1.2.0
  audit_status: PASS
  manifest_completeness: 100%
  total_files_audited: 329
  issues_found: 0
  notes: "Pre-release audit completed successfully. No integrity issues detected."
```

- [ ] **Add Guardian metadata to release notes** (see above format)

---

## Publish Release

### Create Git Tag

- [ ] **Create annotated tag:**
  ```bash
  git tag -a v1.2.0 -m "Release v1.2.0"
  ```

- [ ] **Verify tag created:**
  ```bash
  git tag -l -n1 v1.2.0
  # Should show tag with message
  ```

- [ ] **Push tag to remote:**
  ```bash
  git push origin v1.2.0
  ```

### GitHub Release (Manual)

If not using automated CI/CD:

- [ ] **Navigate to GitHub Releases page:**
  - Go to repository → Releases → Draft a new release

- [ ] **Configure release:**
  - [ ] Choose tag: `v1.2.0`
  - [ ] Release title: `Framework Release v1.2.0`
  - [ ] Description: Copy from `META/RELEASE_NOTES.md`
  - [ ] Check "This is a pre-release" if applicable

- [ ] **Upload artifacts:**
  - [ ] Upload `quickstart-framework-1.2.0.zip`
  - [ ] Upload `checksums.txt`
  - [ ] Optionally: Upload `build-log-v1.2.0.txt`

- [ ] **Include checksums in release notes:**
  ```
  ## Verification
  
  SHA256 Checksums:
  <paste from checksums.txt>
  ```

- [ ] **Publish release**

### GitHub Release (Automated)

If using CI/CD (`.github/workflows/release-packaging.yml`):

- [ ] **Verify workflow triggered:**
  - Go to Actions tab
  - Check for "Release Packaging" workflow run
  - Status should be running or completed

- [ ] **Monitor workflow execution:**
  - [ ] Build step completed successfully
  - [ ] Tests passed
  - [ ] Artifact uploaded

- [ ] **Verify release created automatically:**
  - Check Releases page for new release
  - Artifacts should be attached

- [ ] **Review and edit release notes if needed:**
  - Automated releases may use auto-generated notes
  - Add Guardian metadata manually if not automated

### Alternative Distribution (Internal Artifacts)

If publishing to internal artifact repository:

- [ ] **Upload to artifact storage:**
  ```bash
  # Example for S3:
  aws s3 cp quickstart-framework-1.2.0.zip \
      s3://company-artifacts/framework/releases/v1.2.0/
  
  # Example for Artifactory:
  curl -u user:token -T quickstart-framework-1.2.0.zip \
      "https://artifactory.company.com/framework/v1.2.0/"
  ```

- [ ] **Update internal release catalog** (if applicable)

- [ ] **Verify download link accessible** from internal network

---

## Documentation Updates

### Update Framework Documentation

- [ ] **Update main README.md** with latest version references

- [ ] **Update CHANGELOG.md:**
  - [ ] Mark released version with date
  - [ ] Start new "Unreleased" section for next development cycle

- [ ] **Update version badges** (if using shields.io or similar):
  - Update version number in badge URLs
  - Verify badges render correctly

- [ ] **Cross-check installation guide:**
  - [ ] Example commands reference correct version
  - [ ] Download URLs are valid
  - [ ] Version numbers in examples updated

- [ ] **Update architectural documentation if needed:**
  - [ ] ADRs reference correct versions
  - [ ] Technical designs match release state

### Commit Documentation Updates

- [ ] **Commit doc updates:**
  ```bash
  git add README.md CHANGELOG.md docs/
  git commit -m "docs: Update documentation for v1.2.0 release"
  git push origin main  # or release branch
  ```

---

## Communication and Notification

### Internal Communication

- [ ] **Notify framework core team:**
  - Slack/Teams channel announcement
  - Include release notes summary
  - Highlight breaking changes

- [ ] **Post release summary in team channel:**
  ```
  🎉 Framework Release v1.2.0 is now available!
  
  📦 Artifact: https://github.com/org/repo/releases/tag/v1.2.0
  📝 Release Notes: [link]
  🛡️ Guardian Audit: PASSED
  
  Key Changes:
  - [Feature 1]
  - [Feature 2]
  - [Bug Fix 1]
  
  ⚠️ Breaking Changes: None (or list them)
  
  📚 Documentation: docs/HOW_TO_USE/release_and_upgrade.md
  ```

### External Communication

- [ ] **Notify downstream teams/consumers:**
  - Email to known adopters
  - Post in community forum/Slack
  - Update project website (if applicable)

- [ ] **Announce on relevant channels:**
  - [ ] GitHub Discussions (if enabled)
  - [ ] Twitter/LinkedIn (for public releases)
  - [ ] Company blog or newsletter

- [ ] **Update adoption tracking:**
  - Record known consumers
  - Note expected upgrade timeline

### Manager Mike Iteration Summary

If release occurred during iteration cycle:

- [ ] **Create iteration summary** per Directive 014:
  ```bash
  # See: .github/ISSUE_TEMPLATE/run-iteration.md
  # Include release tasks in iteration report
  ```

- [ ] **Update AGENT_STATUS.md:**
  ```bash
  # Document release completion
  # Note any issues encountered
  # Record Guardian findings
  ```

- [ ] **Post Manager Mike recap comment** to relevant PR/issue

---

## Post-Release Validation

### Download and Verify

- [ ] **Download published artifact from clean environment:**
  ```bash
  # From GitHub Releases:
  wget https://github.com/org/repo/releases/download/v1.2.0/quickstart-framework-1.2.0.zip
  wget https://github.com/org/repo/releases/download/v1.2.0/checksums.txt
  ```

- [ ] **Verify checksums of downloaded artifact:**
  ```bash
  sha256sum -c checksums.txt
  # Must show: OK
  ```

- [ ] **Test download link in documentation works:**
  - Copy link from installation guide
  - Verify it downloads correct version

### Monitor Early Adoption

- [ ] **Watch for installation issues:**
  - Monitor GitHub issues
  - Check Slack/Teams channels
  - Review support requests

- [ ] **Respond to feedback promptly:**
  - Address critical installation failures immediately
  - Document common issues in FAQ
  - Consider hotfix release if severe bugs found

- [ ] **Track adoption metrics:**
  - Number of downloads (if available)
  - Successful installation reports
  - Upgrade completion rate

---

## Cleanup and Archival

### Clean Up Build Artifacts

- [ ] **Archive build logs:**
  ```bash
  mkdir -p ops/release/build-logs
  mv build-log-v1.2.0.txt ops/release/build-logs/
  mv install-test.log ops/release/build-logs/
  mv upgrade-test.log ops/release/build-logs/
  ```

- [ ] **Clean up test environments:**
  ```bash
  rm -rf ~/test-framework-install
  rm -rf ~/test-upgrade-repo
  ```

- [ ] **Optionally remove local build artifacts** (keep for records if needed):
  ```bash
  # Keep for 30 days, then can remove:
  # rm -rf output/releases/quickstart-framework-1.2.0/
  ```

### Merge Release Branch

- [ ] **Merge release branch to main** (if used):
  ```bash
  git checkout main
  git merge --no-ff release/v1.2.0 -m "Merge release v1.2.0 into main"
  git push origin main
  ```

- [ ] **Delete release branch** (optional):
  ```bash
  git branch -d release/v1.2.0
  git push origin --delete release/v1.2.0
  ```

### Document Lessons Learned

- [ ] **Capture release retrospective notes:**
  - What went well?
  - What could be improved?
  - Any process changes needed?
  - Automation opportunities?

- [ ] **Update this checklist** if improvements identified

- [ ] **File issues for automation enhancements:**
  - Example: "Automate Guardian audit in CI/CD"
  - Example: "Add release checklist validation script"

---

## Sign-Off

### Release Manager Sign-Off

- [ ] **All checklist items completed**

- [ ] **No critical issues outstanding**

- [ ] **Documentation updated and committed**

- [ ] **Communication sent to stakeholders**

**Release Manager:** ___________________________  
**Date:** ___________________________  
**Version Released:** ___________________________  

### Optional: Peer Review

- [ ] **Second reviewer validated artifact**

- [ ] **Installation tested by someone other than release manager**

**Reviewer:** ___________________________  
**Date:** ___________________________  

---

## Quick Reference Card

### Essential Commands

```bash
# Build
python ops/release/build_release_artifact.py --version X.Y.Z --dry-run
python ops/release/build_release_artifact.py --version X.Y.Z

# Verify
cd output/releases && sha256sum -c checksums.txt

# Tag and Push
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z

# Test Install
./scripts/framework_install.sh --dry-run . /path/to/test/repo
./scripts/framework_install.sh . /path/to/test/repo

# Test Upgrade
./scripts/framework_upgrade.sh --dry-run . /path/to/test/repo
./scripts/framework_upgrade.sh . /path/to/test/repo
```

### Typical Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| Pre-Release | 10-15 min | Version planning, doc updates, code freeze check |
| Build | 2-5 min | Run build script, verify output |
| Verification | 5-10 min | Checksums, structure, metadata validation |
| Testing | 10-20 min | Install and upgrade tests |
| Guardian Audit | 5-10 min | Run audit, document findings |
| Publish | 5-10 min | Create tag, upload artifacts, publish release |
| Communication | 5-10 min | Notify teams, post announcements |
| Post-Release | 5-10 min | Validation, cleanup, archival |
| **Total** | **45-90 min** | First-time: 60-90 min; Experienced: 20-30 min |

### Critical Checkpoints

These items **must** pass before proceeding:

1. ✅ Checksum verification passes
2. ✅ Manifest includes all expected files
3. ✅ Test installation completes successfully
4. ✅ Framework Guardian audit passes (or issues documented)
5. ✅ Release notes complete with breaking changes noted

---

## Appendix: Troubleshooting Common Issues

### Build Fails

**Symptom:** `build_release_artifact.py` exits with error.

**Common Causes:**
- Missing Python dependencies → `pip install -r requirements.txt`
- Incorrect working directory → Run from repository root
- Invalid version format → Use `X.Y.Z` format

### Checksum Mismatch

**Symptom:** `sha256sum -c checksums.txt` shows FAILED.

**Common Causes:**
- File corruption during copy
- Using wrong checksums.txt file
- Archive modified after build

**Action:** Re-run build and verify immediately.

### Installation Test Fails

**Symptom:** Install script exits with error or files missing.

**Common Causes:**
- Permissions issue on test directory
- Corrupted archive
- Missing execute permissions on script

**Action:** Check script output for specific error; verify archive integrity.

### Guardian Audit Fails

**Symptom:** Audit report shows critical issues.

**Common Causes:**
- Files missing from manifest
- Checksum mismatches
- Incomplete build

**Action:** Review specific failures; may need to rebuild.

---

## Metadata

| Field | Value |
|-------|-------|
| **Document Version** | 1.0.0 |
| **Last Updated** | 2026-01-31 |
| **Target Audience** | Release managers, framework core team |
| **Estimated Time** | 20-90 minutes (varies by experience) |
| **Related Documents** | [Release and Upgrade Workflow Guide](../HOW_TO_USE/release_and_upgrade.md), [Framework Installation Guide](../HOW_TO_USE/framework_install.md) |

**Maintained by:** Agentic Framework Core Team  
**Feedback:** Submit PR to improve this checklist or report issues
