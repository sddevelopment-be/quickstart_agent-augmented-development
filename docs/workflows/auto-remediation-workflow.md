# Automatic Copilot Remediation Workflow

## Overview

The automatic remediation workflow (`auto-remediate-failures.yml`) monitors PR workflow failures and automatically creates remediation tasks for Copilot agents with appropriate specialist delegation.

## How It Works

### 1. Trigger Mechanism

```yaml
workflow_run:
  workflows: 
    - "Doctrine Dependency Validation"
    - "Work Directory Validation"
    - "PR Quality Gate"
  types:
    - completed
  branches:
    - 'copilot/**'
```

Monitors specific validation workflows and triggers only on failure for Copilot branches.

### 2. Failure Detection

When a workflow fails:
- Extracts workflow name, failure URL, PR number, branch
- Downloads error artifacts if available
- Determines appropriate specialist agent

### 3. Specialist Agent Selection

| Workflow Type | Specialist Agent | Task |
|--------------|------------------|------|
| Dependency Validation | Curator Claire | Fix doctrine dependency violations |
| Quality Gate / Tests | Code Reviewer Cindy | Address code quality issues |
| Work Directory | Project Planner Petra | Fix work directory structure |
| Other | General Purpose | Investigate and fix failures |

### 4. Automated Actions

1. **Creates GitHub Issue** with:
   - Workflow failure details
   - Error summary (if artifacts available)
   - Recommended specialist agent
   - Instructions for Copilot
   - Quick command references

2. **Comments on PR** (if applicable):
   - Notifies about auto-remediation
   - Links to remediation issue
   - Tags @copilot

3. **Provides Context**:
   - Links to workflow logs
   - Error artifacts location
   - Branch and commit info

## For Copilot Agents

When you receive an auto-remediation issue:

### Step 1: Review Context
```bash
# View workflow logs
gh run view RUN_ID --log-failed

# Download error artifacts
gh run download RUN_ID
```

### Step 2: Delegate to Specialist
Based on the recommendation in the issue:

- **Curator Claire**: Dependency violations, framework hygiene
- **Code Reviewer Cindy**: Quality issues, test failures
- **Project Planner Petra**: Work directory structure
- **General Purpose**: Complex or unknown issues

### Step 3: Apply Fixes
Follow Boy Scout Rule (Directive 036):
1. Understand the failure
2. Make minimal fixes
3. Validate changes
4. Document in work log

### Step 4: Update Issue
Report back with:
- What was fixed
- Validation results
- Commit references

## Example Auto-Remediation Flow

```
1. PR workflow fails (e.g., Dependency Validation)
   ↓
2. auto-remediate-failures.yml triggers
   ↓
3. Creates issue: "🔴 Auto-Fix: Doctrine Dependency Validation failed"
   ↓
4. Issue includes:
   - Error details
   - Specialist recommendation: Curator Claire
   - Instructions for @copilot
   ↓
5. Copilot reviews issue
   ↓
6. Delegates to Curator Claire
   ↓
7. Claire fixes violations
   ↓
8. Updates issue with results
   ↓
9. PR workflow re-runs and passes ✅
```

## Configuration

### Add More Monitored Workflows

Edit `.github/workflows/auto-remediate-failures.yml`:

```yaml
workflow_run:
  workflows:
    - "Doctrine Dependency Validation"
    - "Work Directory Validation"
    - "PR Quality Gate"
    - "Your New Workflow"  # Add here
```

### Customize Specialist Selection

In the "Extract failure context" step:

```bash
case "$WORKFLOW_NAME" in
  *"YourKeyword"*)
    SPECIALIST="your-agent"
    TASK="Your specific task"
    ;;
esac
```

## Benefits

### For Development Teams
- ✅ Automatic failure detection
- ✅ Appropriate specialist routing
- ✅ Reduced manual triage time
- ✅ Faster issue resolution

### For Copilot Agents
- ✅ Clear context and instructions
- ✅ Error artifacts readily available
- ✅ Specialist guidance
- ✅ Structured remediation workflow

### For Repository Quality
- ✅ Faster fix turnaround
- ✅ Consistent remediation patterns
- ✅ Full audit trail
- ✅ Knowledge capture in issues

## Troubleshooting

### Issue: Workflow doesn't trigger

**Check:**
- Workflow is monitoring the right workflow names
- Branch matches pattern (`copilot/**`)
- Workflow has appropriate permissions

### Issue: No error artifacts

**Solution:**
- Ensure failing workflows use error-summary action
- Check artifact upload configuration
- Workflow continues even without artifacts

### Issue: Wrong specialist assigned

**Solution:**
- Update specialist selection logic
- Add more specific workflow name patterns
- Consider multiple specialists for complex issues

## Related Documentation

- **Error Reporting System:** `docs/error-reporting-system.md`
- **Boy Scout Rule:** `doctrine/directives/036_boy_scout_rule.md`
- **Agent Profiles:** `doctrine/agents/`
- **Workflow Patterns:** `.github/workflows/`

## Version History

- **1.0.0** (2026-02-11): Initial implementation with Curator, Code Reviewer, Project Planner routing
