 # Planning Scripts Directory

**Purpose:** Orchestration scripts for GitHub issue creation and planning workflows.

**Created by:** DevOps Danny  
**Date:** 2025-11-26

## Directory Structure

```
ops/scripts/planning/
├── README.md                          # This file
├── create-github-issues.sh            # Main orchestration (API layer)
├── create-issues-from-definitions.sh  # Data-driven issue creation engine
├── create-follow-up-issues.sh         # Follow-up task creation (specific logic)
├── aggregate-iteration-metrics.py     # Metrics aggregation
├── init-work-structure.sh             # Work directory initialization
├── github-helpers/                    # Shared helper layer (abstraction for issue tracker)
│   ├── github-issue-helpers.sh        # GitHub-specific helper functions
│   └── create-github-issue.sh         # GitHub issue creation CLI wrapper
└── agent-scripts/                     # Agent-generated content
    ├── issue-definitions/             # YAML issue definitions (data-driven)
    │   ├── housekeeping-epic.yml      # Housekeeping epic definition
    │   ├── housekeeping-issues.yml    # Housekeeping child issues
    │   └── ...                        # Additional taskset definitions
    ├── README-housekeeping-issues.md  # Legacy documentation
    ├── create_housekeeping_issues.sh  # Legacy script (to be deprecated)
    └── create_all_task_issues.sh      # Legacy script (to be deprecated)
```

## Workflow Architecture (3-Tier Design)

```
┌─────────────────────────────────────────────────────────────┐
│ Tier 1: API Layer (Orchestration)                           │
│  - GitHub Workflow (create-github-issues.yml)               │
│  - create-github-issues.sh (main orchestration)             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Tier 2: Specific Logic (Planning Scripts)                   │
│  - create-follow-up-issues.sh                               │
│  - agent-scripts/create_housekeeping_issues.sh              │
│  - agent-scripts/create_all_task_issues.sh                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Tier 3: Shared Helpers (Tracker Abstraction)                │
│  - github-helpers/github-issue-helpers.sh                   │
│  - github-helpers/create-github-issue.sh                    │
│  - GitHub CLI (gh)                                          │
└─────────────────────────────────────────────────────────────┘

This design allows easy swapping of issue trackers by replacing Tier 3
with alternative implementations (e.g., Jira, GitLab, Linear helpers).
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

### Via Command Line (Local Execution)

```bash
# Set GitHub token
export GH_TOKEN="your_github_token"

# Create all issues
bash ops/scripts/planning/create-github-issues.sh --all

# Create only housekeeping issues
bash ops/scripts/planning/create-github-issues.sh --housekeeping

# Create only task issues
bash ops/scripts/planning/create-github-issues.sh --tasks

# Dry run to preview
bash ops/scripts/planning/create-github-issues.sh --all --dry-run

# List available agent scripts
bash ops/scripts/planning/create-github-issues.sh --list

# Run a specific agent script
bash ops/scripts/planning/create-github-issues.sh --script create_housekeeping_issues.sh
```

## Scaffolding Script Features

**File:** `create-github-issues.sh`

**Features:**
- Orchestrates multiple agent-generated scripts
- Validates prerequisites (GH_TOKEN, GitHub CLI)
- Provides dry-run capability
- Color-coded output for readability
- Error handling and logging
- Lists available agent scripts
- Flexible execution modes

**Options:**
```
--all               Create all issues from all agent scripts
--housekeeping      Create housekeeping and refactoring issues only
--tasks             Create issues for all open/assigned tasks
--script <name>     Run a specific agent script by name
--list              List available agent scripts
--dry-run           Show what would be executed without running
-h, --help          Show help message
```

## Agent Scripts

### Subdirectory: `agent-scripts/`

Agent-generated planning scripts are stored here for easy discovery and organization.

**Current Scripts:**

1. **create_housekeeping_issues.sh** (by Planning Petra)
   - Creates: 1 epic + 6 child issues
   - Focus: Directive refactoring, token efficiency, infrastructure
   - Priority: 3 high, 2 normal, 1 low
   - Timeline: 2-3 weeks

2. **create_all_task_issues.sh** (by Planning Petra)
   - Creates: 5 epics + 20+ child issues
   - Coverage: All open/assigned repository tasks
   - Includes: POC3, Documentation, Build/CI-CD, Architecture, Quality
   - Timeline: 3-4 weeks total

### Adding New Agent Scripts

When agents create new planning scripts:

1. Place script in `agent-scripts/` directory
2. Make it executable: `chmod +x agent-scripts/your-script.sh`
3. Add description comment at top of script
4. Script should call issue creation via `$REPO_ROOT/ops/scripts/planning/github-helpers/create-github-issue.sh`
5. Test with scaffolding script: `./create-github-issues.sh --script your-script.sh`
6. Document in this README if it's a permanent addition

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
bash ops/scripts/planning/create-github-issues.sh --all
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

- **v1.0.0** (2025-11-26): Initial implementation by DevOps Danny
  - Created scaffolding architecture
  - Implemented GitHub workflow
  - Organized agent scripts into subdirectory
  - Added comprehensive documentation

---

**Maintained by:** DevOps Danny (Build Automation Specialist)  
**Last Updated:** 2025-11-26
