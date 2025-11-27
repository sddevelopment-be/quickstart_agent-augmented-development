 # Planning Scripts Directory

**Purpose:** Orchestration scripts for GitHub issue creation and planning workflows.

**Created by:** DevOps Danny  
**Date:** 2025-11-26

## Directory Structure

```
ops/scripts/planning/
├── README.md                          # This file
├── create-issues-from-definitions.sh  # Main API: Data-driven issue creation engine
├── aggregate-iteration-metrics.py     # Metrics aggregation
├── init-work-structure.sh             # Work directory initialization
├── github-helpers/                    # Tier 3: Issue tracker abstraction layer
│   ├── github-issue-helpers.sh        # GitHub-specific helper functions
│   └── create-github-issue.sh         # GitHub issue creation CLI wrapper
└── agent-scripts/                     # Agent-generated content
    ├── issue-definitions/             # Tier 2: YAML issue definitions (data layer)
    │   ├── architecture-epic.yml      # Architecture epic + issues
    │   ├── architecture-issues.yml
    │   ├── build-cicd-epic.yml        # Build/CI-CD epic + issues
    │   ├── build-cicd-issues.yml
    │   ├── curator-quality-epic.yml   # Curator quality epic + issues
    │   ├── curator-quality-issues.yml
    │   ├── documentation-epic.yml     # Documentation epic + issues
    │   ├── documentation-issues.yml
    │   ├── followup-issues.yml        # Follow-up issues (no epic)
    │   ├── housekeeping-epic.yml      # Housekeeping epic + issues
    │   ├── housekeeping-issues.yml
    │   ├── poc3-epic.yml              # POC3 epic + issues
    │   └── poc3-issues.yml
    ├── legacy/                        # Deprecated bash scripts (reference only)
    │   ├── README.md                  # Deprecation notice
    │   ├── create_housekeeping_issues.sh
    │   └── create_all_task_issues.sh
    ├── IMPLEMENTATION_SUMMARY.md      # Technical implementation guide
    ├── MIGRATION_COMPLETE.md          # Migration completion report
    └── README-housekeeping-issues.md  # Legacy documentation
```

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
ops/scripts/planning/create-issues-from-definitions.sh

# Create only housekeeping issues
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping

# Create multiple tasksets
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping,documentation

# Dry run to preview
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping --dry-run

# List available tasksets
ops/scripts/planning/create-issues-from-definitions.sh --list-tasksets
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

### Via GitHub Workflow (Recommended for Humans)

1. Go to repository Actions tab
2. Select "Create GitHub Issues from Agent Plans"
3. Click "Run workflow"
4. Choose mode:
   - **all**: Create all issues from all scripts
   - **housekeeping**: Create housekeeping epic only
   - **tasks**: Create task-tracking issues only
5. Optionally enable dry-run to preview
6. Click "Run workflow"

**Permissions:** Only repository owners/admins can execute

### Command Line Usage

```bash
# Set GitHub token
export GH_TOKEN="your_github_token"

# List available tasksets
ops/scripts/planning/create-issues-from-definitions.sh --list-tasksets

# Preview issues (dry run)
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping --dry-run

# Create issues for a specific taskset
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping

# Create multiple tasksets
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping,poc3

# Create all issues
ops/scripts/planning/create-issues-from-definitions.sh
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

**Location:** `ops/scripts/planning/github-helpers/github-issue-helpers.sh`

Core abstraction providing functions for issue management:
- `_github_issue::create` - Create issue with labels, assignees, etc.
- `_github_issue::log` - Logging function
- `_github_issue::body_from_file` - Read body from file
- `_github_issue::body_from_source` - Use file or fallback text
- Error handling and validation
- CSV parsing for labels and assignees
- Missing label detection and warnings

### create-github-issue.sh

**Location:** `ops/scripts/planning/github-helpers/create-github-issue.sh`

CLI wrapper for the helper functions. This is the primary interface used by Tier 2 scripts.

**Usage:**
```bash
# From a local file
ops/scripts/planning/github-helpers/create-github-issue.sh \
  --repo owner/repo \
  --title "Issue title" \
  --body-file path/to/body.md \
  --label label1 --label label2 \
  --assignee username

# From STDIN
echo "Issue body" | ops/scripts/planning/github-helpers/create-github-issue.sh \
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

## GitHub Workflow

**File:** `.github/workflows/create-github-issues.yml`

**Trigger:** Manual (workflow_dispatch)  
**Permissions:** Repository owners/admins only

**Workflow Steps:**
1. Checkout repository
2. Validate user permissions (admin/write required)
3. Display execution plan
4. List available agent scripts
5. Execute scaffolding script with selected mode
6. Generate workflow summary

**Inputs:**
- `mode`: all | housekeeping | tasks
- `dry_run`: boolean (preview without creating)

**Security:**
- Validates user has admin or write permission
- Uses GITHUB_TOKEN for authentication
- Only runs on manual trigger
- Permission check prevents unauthorized execution

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

### Updating Agent Scripts

When Petra or other agents create new planning scripts:
1. Scripts are automatically placed in `agent-scripts/` by agents
2. Scaffolding script auto-discovers them
3. No workflow changes needed

### Workflow Updates

The workflow is designed to be stable. Updates needed only for:
- Permission model changes
- New execution modes
- Enhanced validation requirements

### Testing

```bash
# Test scaffolding script
ops/scripts/planning/create-github-issues.sh --list
ops/scripts/planning/create-github-issues.sh --all --dry-run

# Test specific agent script
ops/scripts/planning/create-github-issues.sh --script create_housekeeping_issues.sh --dry-run

# Validate workflow (requires act or GitHub Actions)
gh workflow run create-github-issues.yml -f mode=housekeeping -f dry_run=true
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
ops/scripts/planning/create-issues-from-definitions.sh --list-tasksets
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
