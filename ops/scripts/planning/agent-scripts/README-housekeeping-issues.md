# Temporary Scripts Directory

This directory contains helper scripts for various repository operations.

## GitHub Issues Creation

### Script: `create_housekeeping_issues.sh`

**Purpose:** Automate creation of the "Housekeeping and Refactoring" epic and related child issues.

**Created by:** Planning Petra  
**Date:** 2025-11-26  
**Context:** Work directory restructuring PR follow-up tasks

### Prerequisites

1. **GitHub CLI installed** (should already be available)
   ```bash
   gh --version
   ```

2. **GitHub token with repo access**
   ```bash
   export GH_TOKEN="your_github_token_here"
   ```
   
   Or authenticate with:
   ```bash
   gh auth login
   ```

### Usage

```bash
# From repository root
bash tmp/create_housekeeping_issues.sh
```

### What It Does

1. Creates epic issue: "Epic: Housekeeping and Refactoring"
2. Creates 6 child issues:
   - Review Directive 009 and create shared glossary
   - Extract Directive 013 to approaches
   - Extract Directive 015 to templates
   - Refactor Directive 018 for token efficiency
   - Create metric capture scripts and dashboards
   - Assess dynamic dashboard feasibility
3. Links all child issues to the epic
4. Applies appropriate labels (epic, housekeeping, priority levels, etc.)

### Expected Output

```
🏗️  Creating Housekeeping and Refactoring Epic and related issues...

📋 Creating Epic: Housekeeping and Refactoring...
✅ Epic created: #XXX

📝 Creating: Review Directive 009 and consider shared glossary creation
📝 Creating: Extract verbose content from Directive 013 to approaches directory
📝 Creating: Extract verbose content from Directive 015 to docs/templates
📝 Creating: Refactor Directive 018 to reduce verbosity and extract sub-directives
📝 Creating: Create metric capture scripts and recreate collaboration dashboard files
📝 Creating: Assess creating dynamic dashboard via stateless webservice

✅ All issues created successfully!

Epic: #XXX

Next steps:
1. Review created issues at https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues
2. Agents can process tasks from work/collaboration/inbox/
3. Link GitHub issues to task completions
```

### Troubleshooting

**Error: "Failed to create epic issue. Please check GH_TOKEN is set."**
- Ensure GH_TOKEN environment variable is set
- Verify token has `repo` scope permissions
- Try authenticating: `gh auth login`

**Error: "gh: command not found"**
- Install GitHub CLI: https://cli.github.com/

**Warning: "labels missing in repository"**
- Script will still create issues but labels won't be applied
- Manually add labels in GitHub UI, or sync labels first

### Related Files

- Task files: `work/collaboration/inbox/2025-11-26T06*.yaml`
- Work log: `work/reports/logs/project-planner/2025-11-26T0645-github-issues-planning.md`
- Ops script: `ops/scripts/create-github-issue.sh` (used by this script)

### Cleanup

After successful execution, you can optionally remove this script:
```bash
rm tmp/create_housekeeping_issues.sh
```

However, keeping it provides documentation of how issues were created.

---

**Note:** This script uses the repository's existing `ops/scripts/create-github-issue.sh` infrastructure, ensuring consistency with other automated issue creation workflows.
