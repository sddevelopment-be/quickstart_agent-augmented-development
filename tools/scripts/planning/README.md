 # Planning Scripts Directory

**Purpose:** Orchestration scripts for GitHub issue creation and planning workflows.

**Created by:** DevOps Danny  
**Date:** 2025-11-26

## Directory Structure

**Organization:** 3-tier architecture (API → Data → Helpers)

```
ops/planning/
├── create-issues-from-definitions.sh  # Main API (Tier 1)
├── github-helpers/                    # Issue tracker abstraction (Tier 3)
├── agent-scripts/
│   ├── issue-definitions/             # YAML issue definitions (Tier 2)
└── [supporting scripts and documentation]
```

**Key Locations:**
- **Main API:** `create-issues-from-definitions.sh`
- **Issue Definitions:** `agent-scripts/issue-definitions/*.yml`
- **Helper Functions:** `github-helpers/`
- **Documentation:** `README.md`, `agent-scripts/IMPLEMENTATION_SUMMARY.md`

> **Note:** See directory listing for complete file inventory. The file system is the source of truth.

## Architecture (3-Tier Design)

```
┌─────────────────────────────────────────────────────────────┐
│ Tier 1: API Layer                                           │
│  - create-issues-from-definitions.sh (main API)             │
│  - Parses YAML, filters by taskset, orchestrates creation   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Tier 2: Data Layer (YAML Definitions)                       │
│  - agent-scripts/issue-definitions/*.yml                    │
│  - Pure data: epics and issues as structured YAML           │
│  - Taskset-based organization for filtering                 │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Tier 3: Helper Layer (Tracker Abstraction)                  │
│  - github-helpers/create-github-issue.sh                    │
│  - github-helpers/github-issue-helpers.sh                   │
│  - GitHub CLI (gh)                                          │
└─────────────────────────────────────────────────────────────┘

**Benefits:**
- Tier 3 can be swapped (GitHub → Jira, GitLab, Linear, etc.)
- Tier 2 is pure data (easy for agents to generate)
- Tier 1 is reusable logic (one engine for all tasksets)
```

## Data-Driven Issue Creation

**New Approach:** Issue definitions are stored as YAML files in `agent-scripts/issue-definitions/`, enabling:
- **Separation of data and logic**: Issue content separate from creation logic
- **Easy iteration**: Add new issues without modifying scripts
- **Taskset filtering**: Create specific subsets of issues (e.g., only housekeeping)
- **Agent-friendly**: Agents generate YAML definitions instead of full scripts

### Issue Definition Format

```yaml
---
type: epic              # "epic" or "issue"
taskset: housekeeping   # Category/grouping for filtering
title: "Issue Title"
labels: label1,label2,label3
assignee: ""            # Optional
priority: high          # Optional: high, normal, low
epic_ref: epic-file     # For issues: reference to parent epic definition file

body: |
  # Issue Body
  
  Markdown content for the issue body.
  Can be multiline.
```

### Creating Issues from Definitions

```bash
# Create all issues
ops/planning/create-issues-from-definitions.sh

# Create only housekeeping issues
ops/planning/create-issues-from-definitions.sh --taskset housekeeping

# Create multiple tasksets
ops/planning/create-issues-from-definitions.sh --taskset housekeeping,documentation

# Dry run to preview
ops/planning/create-issues-from-definitions.sh --taskset housekeeping --dry-run

# List available tasksets
ops/planning/create-issues-from-definitions.sh --list-tasksets
```

### For Agents: Creating New Issue Definitions

Instead of writing bash scripts, agents should create YAML definition files:

1. Create file in `agent-scripts/issue-definitions/`
2. Name format: `{taskset}-{type}.yml` (e.g., `documentation-epic.yml`, `deployment-issues.yml`)
3. Follow the YAML format above
4. Multiple issues can be in one file as an array (use `- type: issue` for each)
5. Reference parent epics using `epic_ref: filename-without-extension`

**Example multi-issue file:**
```yaml
---
- type: issue
  taskset: documentation
  epic_ref: documentation-epic
  title: "Update API docs"
  labels: documentation,api
  body: |
    Update API documentation...

- type: issue
  taskset: documentation
  epic_ref: documentation-epic
  title: "Create user guide"
  labels: documentation,guide
  body: |
    Create comprehensive user guide...
```

## Usage


```bash
# Set GitHub token
export GH_TOKEN="your_github_token"

# List available tasksets
ops/planning/create-issues-from-definitions.sh --list-tasksets

# Preview issues (dry run)
ops/planning/create-issues-from-definitions.sh --taskset housekeeping --dry-run

# Create issues for a specific taskset
ops/planning/create-issues-from-definitions.sh --taskset housekeeping

# Create multiple tasksets
ops/planning/create-issues-from-definitions.sh --taskset housekeeping,poc3

# Create all issues
ops/planning/create-issues-from-definitions.sh
```

## Main API: create-issues-from-definitions.sh

**File:** `create-issues-from-definitions.sh`

**Features:**
- Data-driven: reads YAML definitions instead of bash scripts
- Taskset filtering: create specific subsets of issues
- Dry-run capability: preview before creating
- Epic tracking: automatically links child issues to parent epics
- Color-coded output for readability
- No external dependencies (uses grep/awk for YAML parsing)

**Options:**
```
--taskset <name>    Create issues for specific taskset(s) (comma-separated)
--dry-run           Preview what would be created without creating
--repo <owner/name> Override repository
--list-tasksets     List available tasksets and exit
-h, --help          Show help message
```

## For Agents: Creating Issue Definitions

Instead of writing bash scripts, agents should create YAML definition files in `agent-scripts/issue-definitions/`.

### Creating New Issues

1. Create YAML file in `agent-scripts/issue-definitions/`
2. Name format: `{taskset}-epic.yml` and `{taskset}-issues.yml`
3. Follow the YAML format (see Data-Driven Issue Creation section above)
4. Set proper permissions: `chmod 644 your-file.yml`
5. Test with dry-run: `create-issues-from-definitions.sh --taskset your-taskset --dry-run`

## Tier 3: GitHub Helpers (Tracker Abstraction Layer)

The `github-helpers/` directory contains GitHub-specific implementations that abstract issue tracker operations. This layer can be swapped with alternative implementations for other issue trackers.

### github-issue-helpers.sh

**Location:** `ops/planning/github-helpers/github-issue-helpers.sh`

Core abstraction providing functions for issue management:
- `_github_issue::create` - Create issue with labels, assignees, etc.
- `_github_issue::log` - Logging function
- `_github_issue::body_from_file` - Read body from file
- `_github_issue::body_from_source` - Use file or fallback text
- Error handling and validation
- CSV parsing for labels and assignees
- Missing label detection and warnings

### create-github-issue.sh

**Location:** `ops/planning/github-helpers/create-github-issue.sh`

CLI wrapper for the helper functions. This is the primary interface used by Tier 2 scripts.

**Usage:**
```bash
# From a local file
ops/planning/github-helpers/create-github-issue.sh \
  --repo owner/repo \
  --title "Issue title" \
  --body-file path/to/body.md \
  --label label1 --label label2 \
  --assignee username

# From STDIN
echo "Issue body" | ops/planning/github-helpers/create-github-issue.sh \
  --repo owner/repo \
  --title "Issue title" \
  --label label1
```

### Replacing the Issue Tracker

To use a different issue tracker, replace the `github-helpers/` directory with an equivalent implementation that provides the same function signatures. For example:
- `jira-helpers/` for Jira
- `gitlab-helpers/` for GitLab Issues
- `linear-helpers/` for Linear

Tier 2 scripts would remain unchanged as long as the interface stays consistent.


## Integration with Repository

### Work Directory

Scripts create GitHub issues that reference tasks in:
- `work/collaboration/inbox/` - New tasks awaiting assignment
- `work/collaboration/assigned/` - Tasks assigned to agents
- `work/collaboration/done/` - Completed tasks

### Task Tracking

Each GitHub issue includes:
- Link to originating task YAML file
- Agent assignment
- Priority level
- Acceptance criteria
- Deliverables list
- Epic reference (for child issues)

### Work Logs

Agent execution logs referenced from:
- `work/reports/logs/project-planner/` - Planning Petra logs
- Includes task inventory and planning analysis

## Maintenance

### Adding New Issue Definitions

When agents create new issues:
1. Create YAML files in `agent-scripts/issue-definitions/`
2. Follow naming convention: `{taskset}-epic.yml`, `{taskset}-issues.yml`
3. Use `--list-tasksets` to verify detection
4. Test with `--dry-run` before creating

### Testing

```bash
# List available tasksets
ops/planning/create-issues-from-definitions.sh --list-tasksets

# Dry run (preview without creating)
ops/planning/create-issues-from-definitions.sh --taskset housekeeping --dry-run

# Test all tasksets
ops/planning/create-issues-from-definitions.sh --dry-run

# Validate YAML syntax
for f in agent-scripts/issue-definitions/*.yml; do 
  grep -q "^type:" "$f" && echo "✓ $f" || echo "✗ $f"
done
```

## Troubleshooting

### "GH_TOKEN environment variable is not set"

**Solution:** Set GitHub token before running:
```bash
export GH_TOKEN="your_token_here"
# Or authenticate with:
gh auth login
```

### "User does not have sufficient permissions"

**Solution:** Only repository owners/collaborators with write access can run the workflow. Contact a repository owner.

### "Script not found"

**Solution:** Ensure you're running from repository root or use full path:
```bash
cd /path/to/quickstart_agent-augmented-development
ops/planning/create-issues-from-definitions.sh --list-tasksets
```

### "gh: command not found"

**Solution:** Install GitHub CLI:
```bash
# macOS
brew install gh

# Linux
# See: https://cli.github.com/
```

## Related Documentation

- [GitHub Issues Creation Workflow](/.github/workflows/create-github-issues.yml)
- [Housekeeping Epic Documentation](agent-scripts/README-housekeeping-issues.md)
- [Planning Petra Work Logs](../../../work/reports/logs/project-planner/)
- [File-Based Orchestration](../../../.github/agents/approaches/file_based_collaboration/)

## Version History

- **v2.0.0** (2025-11-27): Data-driven migration by DevOps Danny
  - ✅ Migrated all 27 issues + 6 epics to YAML definitions
  - ✅ Created generic issue creation engine
  - ✅ Deprecated legacy bash scripts
  - ✅ Implemented 3-tier architecture (API → Data → Helpers)
  - ✅ Removed `create-github-issues.sh` and `create-follow-up-issues.sh`
  - See `agent-scripts/MIGRATION_COMPLETE.md` for details

- **v1.0.0** (2025-11-26): Initial implementation by DevOps Danny
  - Created scaffolding architecture
  - Implemented GitHub workflow
  - Organized agent scripts into subdirectory
  - Added comprehensive documentation

---

**Maintained by:** DevOps Danny (Build Automation Specialist)  
**Last Updated:** 2025-11-27
