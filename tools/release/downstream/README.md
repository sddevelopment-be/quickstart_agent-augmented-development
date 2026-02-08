# Downstream Deployment Tools

This directory contains tools for downstream repositories to pull and deploy the SDD Agent Framework from upstream releases.

## Overview

When you want to use the SDD Agent Framework in your own repository, these tools help you:

1. **Fetch** the latest (or specific) release from the upstream repository
2. **Install** or **upgrade** the framework in your repository
3. **Verify** the installation using the Framework Guardian agent

## Quick Start

### Option 1: Shell Script (Local/Manual)

Copy `deploy_framework.sh` to your repository and run:

```bash
# Fresh installation
./deploy_framework.sh

# Upgrade existing installation
./deploy_framework.sh --upgrade

# Install specific version
./deploy_framework.sh --version 1.0.0

# Preview changes (dry run)
./deploy_framework.sh --upgrade --dry-run
```

### Option 2: GitHub Actions Workflow (Automated)

Copy `framework-update.yml` to your repository's `.github/workflows/` directory:

```bash
cp framework-update.yml /path/to/your-repo/.github/workflows/
```

Then trigger it via GitHub Actions UI, or enable scheduled updates by uncommenting the cron schedule in the workflow.

## Tools

### deploy_framework.sh

A POSIX-compliant shell script for manual framework deployment.

**Features:**
- Fetches releases from GitHub API
- Supports specific version or latest
- Install or upgrade modes
- Dry-run for previewing changes
- Framework Guardian verification reminder

**Requirements:**
- `curl` or `wget`
- `unzip`
- Optional: `GITHUB_TOKEN` env var for private repos

**Usage:**

```bash
./deploy_framework.sh [OPTIONS]

Options:
  --version VERSION    Install specific version (default: latest)
  --upgrade            Upgrade existing installation
  --target DIR         Target directory (default: current)
  --dry-run            Preview changes without applying
  --skip-guardian      Skip Guardian verification reminder
  --help               Show help message
```

**Exit Codes:**
- `0` - Success
- `1` - Invalid arguments
- `2` - Download failed
- `3` - Installation failed

### framework-update.yml

A GitHub Actions workflow template for automated framework updates.

**Features:**
- Manual trigger with version/mode options
- Optional scheduled updates (weekly)
- Creates PRs for review (configurable)
- Conflict detection and reporting
- Framework Guardian reminder in PR description

**Configuration:**

Edit these variables in the workflow file:

```yaml
env:
  UPSTREAM_REPO: sddevelopment-be/quickstart_agent-augmented-development
  TARGET_BRANCH: main
  PR_BRANCH_PREFIX: framework-update
```

**Workflow Inputs:**

| Input | Description | Default |
|-------|-------------|---------|
| `version` | Specific version to install | (latest) |
| `mode` | `install` or `upgrade` | `upgrade` |
| `dry_run` | Preview without applying | `false` |
| `create_pr` | Create PR instead of direct commit | `true` |

## Workflow

### Fresh Installation

```
Your Repo                    Upstream Repo
    │                             │
    │  1. Fetch latest release    │
    │◄────────────────────────────│
    │                             │
    │  2. Download artifact       │
    │◄────────────────────────────│
    │                             │
    ▼
┌─────────────────────────────────────┐
│  3. Run framework_install.sh        │
│     - Copy framework_core/ files    │
│     - Create .framework_meta.yml    │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  4. Framework Guardian (optional)   │
│     - Verify installation           │
│     - Generate audit report         │
└─────────────────────────────────────┘
```

### Upgrade Existing Installation

```
Your Repo                    Upstream Repo
    │                             │
    │  1. Fetch target release    │
    │◄────────────────────────────│
    │                             │
    │  2. Download artifact       │
    │◄────────────────────────────│
    │                             │
    ▼
┌─────────────────────────────────────┐
│  3. Run framework_upgrade.sh        │
│     - Compare checksums             │
│     - Copy NEW files                │
│     - Create .framework-new for     │
│       CONFLICT files                │
│     - Skip PROTECTED (local/)       │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  4. Framework Guardian (recommended)│
│     - Analyze conflicts             │
│     - Generate upgrade plan         │
│     - Recommend resolutions         │
└─────────────────────────────────────┘
```

## Framework Guardian Integration

After deployment, the Framework Guardian agent can:

1. **Audit Mode** - Verify installation integrity
   - Check all files against manifest checksums
   - Identify missing or misplaced files
   - Generate `validation/FRAMEWORK_AUDIT_REPORT.md`

2. **Upgrade Mode** - Resolve conflicts
   - Analyze `.framework-new` files
   - Classify conflict types
   - Generate `validation/FRAMEWORK_UPGRADE_PLAN.md`
   - Recommend minimal patches

**Invoking Guardian:**

In your AI assistant (Claude, etc.):
```
Switch to Framework Guardian agent and run an audit.
```

Or reference the agent profile directly:
```
See .github/agents/framework-guardian.agent.md
```

## File Statuses

During installation/upgrade, files are classified as:

| Status | Description | Action |
|--------|-------------|--------|
| `NEW` | File doesn't exist in target | Copied from release |
| `UNCHANGED` | Checksums match | No action |
| `CONFLICT` | Checksums differ | `.framework-new` created |
| `PROTECTED` | In `local/` directory | Never modified |

## Troubleshooting

### "No releases found"

The upstream repository may not have any releases yet. Check:
- https://github.com/sddevelopment-be/quickstart_agent-augmented-development/releases

### "Download failed"

- Check network connectivity
- Verify the version exists: `gh release list -R sddevelopment-be/quickstart_agent-augmented-development`
- For private repos, ensure `GITHUB_TOKEN` is set

### "Framework already installed"

Use `--upgrade` flag to update an existing installation:
```bash
./deploy_framework.sh --upgrade
```

### "No existing framework installation"

Remove `--upgrade` flag for fresh installation:
```bash
./deploy_framework.sh
```

### Conflicts after upgrade

1. Find conflict files: `find . -name "*.framework-new"`
2. Compare with originals: `diff file.md file.md.framework-new`
3. Use Framework Guardian for automated analysis
4. Manually merge or replace as needed
5. Delete `.framework-new` files after resolution

## Security Considerations

- The deployment script validates release artifacts via GitHub API
- Checksums are verified during installation
- No automatic code execution from downloaded content
- PR-based workflow allows human review before merging

## References

- [ADR-013: Zip-Based Framework Distribution](../../../docs/architecture/adrs/ADR-013-zip-distribution.md)
- [ADR-014: Framework Guardian Agent](../../../docs/architecture/adrs/ADR-014-framework-guardian-agent.md)
- [Framework Installation Guide](../../../docs/HOW_TO_USE/framework_install.md)
- [Release Packaging System](../README.md)
