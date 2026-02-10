# Automated Glossary Maintenance Workflows

**Created by:** DevOps Danny  
**Date:** 2026-02-10  
**Purpose:** Continuous terminology synchronization via agent-triggered automation

---

## Overview

This system implements automated Living Glossary maintenance through two GitHub Actions workflows that trigger agent sessions (Lexical Larry + Curator Claire) when doctrine directory changes are detected.

### Workflows

1. **`doctrine-glossary-maintenance.yml`** - Detects changes and creates agent tasks
2. **`glossary-update-pr.yml`** - Creates automated PRs for glossary updates

---

## Workflow 1: Doctrine Glossary Maintenance

**Trigger:** PR to `main` branch with changes to `doctrine/**/*.md`

### Process Flow

```
PR with doctrine changes
    ↓
[Detect Changes] ← workflow scans for modified files
    ↓
[Create Task File] ← generates YAML task for Lexical Larry
    ↓
[Notify PR] ← comments on PR with task details
    ↓
[Human/Agent Invocation] ← trigger agent execution
    ↓
[Lexical Larry] ← extracts terminology from changes
    ↓
[Handoff to Curator Claire] ← via work/collaboration/HANDOFFS.md
    ↓
[Curator Claire] ← integrates terms into GLOSSARY.md
    ↓
[Auto-PR Creation] ← workflow 2 creates PR with updates
```

### Key Features

✅ **Delta Extraction**: Only processes changed/added files  
✅ **Agent-Triggered**: Creates task files for human/AI agent execution  
✅ **PR Integration**: Comments on source PR with task details  
✅ **Handoff Protocol**: Follows multi-agent orchestration patterns  
✅ **Human in Charge**: Requires explicit agent invocation

---

## Agent Invocation Methods

### Method 1: GitHub Copilot / Claude Code (Recommended)

```bash
# In VS Code with GitHub Copilot or Claude Code extension

# Option A: Direct task execution
# Open: work/collaboration/inbox/<task-id>.yaml
# Say to Copilot: "Execute this task as Lexical Larry, then hand off to Curator Claire"

# Option B: Agent-specific invocation (Claude Code)
@lexical execute task work/collaboration/inbox/<task-id>.yaml
# Then after completion:
@curator integrate glossary candidates from previous extraction
```

### Method 2: Scheduled Orchestration

```yaml
# Hourly orchestration workflow picks up tasks automatically
# Location: .github/workflows/orchestration.yml
# Runs: Every hour (cron: '0 * * * *')
# Processes: Tasks in work/collaboration/inbox/
```

### Method 3: Manual Execution (Testing/Fallback)

```bash
# Review task file
cat work/collaboration/inbox/<task-id>.yaml

# Execute steps manually following task instructions
```

---

## Living Glossary Practice Integration

These workflows implement the **Living Glossary Practice** approach:

- **Continuous Capture:** Workflow triggers on every doctrine PR
- **Delta-based:** Only processes changed files
- **Agent-driven:** Lexical Larry + Curator Claire collaboration
- **Human-approved:** Final merge requires human review

---

## References

- **[Living Glossary Practice](../../doctrine/approaches/living-glossary-practice.md)**
- **[Terminology Extraction Tactic](../../doctrine/tactics/terminology-extraction-mapping.tactic.md)**
- **[Lexical Larry Profile](../../doctrine/agents/lexical.agent.md)**
- **[Curator Claire Profile](../../doctrine/agents/curator.agent.md)**

---

**Version:** 1.0.0  
**Maintained by:** DevOps Danny
