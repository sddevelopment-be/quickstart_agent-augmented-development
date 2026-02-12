# Agent Specialization Hierarchy: Migration Guide

## Overview

Agent Specialization Hierarchy (ASH) enables intelligent routing of tasks to the most appropriate specialist agents based on context (language, frameworks, domain, writing style). Rather than assigning all Python work to a generic backend agent, ASH routes tasks to Python Pedro. Rather than sending all documentation to Editor Eddy, ASH routes user guides to a specialized User Guide Ursula.

This guide helps repository adopters understand how to leverage ASH and add custom specialists.

**Foundation:** See [DDR-011: Agent Specialization Hierarchy](../../doctrine/decisions/DDR-011-agent-specialization-hierarchy.md) for decision rationale and architecture.

---

## Quick Start for Repository Adopters

### Adding a Custom Specialist Agent

The simplest way to extend ASH is to create a custom specialist in your repository's `.doctrine-config/custom-agents/` directory.

#### Example: Creating User Guide Ursula (Editor Eddy Specialist)

Create `.doctrine-config/custom-agents/user-guide-ursula.agent.md`:

```yaml
---
name: user-guide-ursula
description: Specialist for user-facing documentation and guides
tools: ["read", "write", "edit", "Bash", "Grep"]
specializes_from: editor-eddy
routing_priority: 85
max_concurrent_tasks: 3
specialization_context:
  domain_keywords: [user-guide, tutorial, onboarding, getting-started, faq]
  file_patterns: ["**/docs/guides/**", "**/docs/user-guide/**"]
  writing_style: [instructional, accessible, beginner-friendly]
  complexity_preference: [low, medium]
---

# Agent Profile: User Guide Ursula (User Guide Specialist)

## Purpose

Create accessible, step-by-step user guides that enable non-technical users to accomplish tasks.

## Specialization

- **Primary focus:** Clear, instructional writing; user journey mapping; example-driven documentation
- **Secondary awareness:** Accessibility standards; localization considerations; user feedback incorporation
- **Avoid:** Technical deep-dives; API reference material; implementation details
- **Success means:** Users complete tasks independently; minimal support requests; positive feedback

## Collaboration Contract

- Always verify user audience before writing (beginner vs experienced)
- Include concrete examples and screenshots when possible
- Validate step-by-step procedures with actual workflows
- Stay in User Guide Ursula lane; delegate API docs and technical specs to Editor Eddy
```

#### Why This Works

- `specializes_from: editor-eddy` declares Parent Agent
- `routing_priority: 85` (higher than Editor Eddy's default 50) means ASH prefers Ursula for matching tasks
- `domain_keywords: [user-guide, ...]` + `file_patterns` define when Ursula should be selected
- `writing_style: [instructional, ...]` ensures she's used for tutorials, not API references
- Local specialists in `.doctrine-config/custom-agents/` receive automatic +20 priority boost

---

## Agent Profile Frontmatter Schema

### Required Fields

```yaml
---
name: agent-slug                # Unique identifier (kebab-case)
description: Brief description  # 1-2 sentences
tools: [...]                    # Available tools
---
```

### Specialization Fields (Optional)

| Field | Type | Default | Purpose | Example |
|-------|------|---------|---------|---------|
| `specializes_from` | string | (none) | Parent agent slug | `backend-benny` |
| `routing_priority` | int (0-100) | 50 | Specificity score | 80 for specialist |
| `max_concurrent_tasks` | int | 8 | Workload threshold | 5 for focused specialist |
| `specialization_context` | object | {} | Context matching rules | See below |

### Specialization Context Reference

Define when your specialist should be preferred. All keys are optional but recommended:

```yaml
specialization_context:
  language: [python, javascript]        # Programming languages (string[])
  frameworks: [flask, fastapi]          # Frameworks/libraries (string[])
  file_patterns:                        # File glob patterns (string[])
    - "**/*.py"
    - "**/pyproject.toml"
  domain_keywords: [api, backend]       # Domain/task keywords (string[])
  writing_style: [technical, academic]  # For writing agents (string[])
  complexity_preference: [low, medium]  # Task complexity levels (string[])
```

### Field Explanations

**`language`** — Programming languages your specialist prefers
- Examples: `python`, `java`, `javascript`, `go`, `rust`
- Used for routing code tasks
- Match is worth 40% of routing score

**`frameworks`** — Specific libraries/frameworks
- Examples: `flask`, `fastapi`, `spring`, `react`, `pytorch`
- Refines language matching
- Match is worth 20% of routing score

**`file_patterns`** — Glob patterns to match files
- Examples: `**/*.py`, `**/src/**`, `**/docs/guides/**`
- Used to detect task context from file paths
- Match is worth 20% of routing score

**`domain_keywords`** — Task/domain keywords
- Examples: `api`, `database`, `ui`, `user-guide`, `tutorial`
- Extracted from task title/description and matched
- Match is worth 10% of routing score

**`writing_style`** — For writing-focused specialists (Editor Eddy children)
- Examples: `instructional`, `technical`, `marketing`, `academic`
- Used to select appropriate writer for tone/audience
- Match is worth 10% of routing score

**`complexity_preference`** — Complexity levels your specialist prefers
- Valid values: `low`, `medium`, `high`
- Specialists typically prefer `[low, medium]`
- Parents prefer `[medium, high]` (complex tasks need broader context)

---

## Creating a Custom Specialist: Step-by-Step

### 1. Identify the Parent Agent

Determine which agent your specialist will inherit from:

- **Backend specialists** → `specializes_from: backend-benny`
- **Frontend specialists** → `specializes_from: frontend-freddy`
- **Writing specialists** → `specializes_from: editor-eddy`
- **DevOps specialists** → `specializes_from: build-automation`

### 2. Create the Profile File

Create `.doctrine-config/custom-agents/{name}.agent.md`:

```bash
mkdir -p .doctrine-config/custom-agents/
touch .doctrine-config/custom-agents/my-specialist.agent.md
```

### 3. Add Frontmatter with Specialization

```yaml
---
name: my-specialist
description: [Concise purpose]
tools: [...]
specializes_from: [parent-agent]
routing_priority: 80              # 60-90 typical for specialists
max_concurrent_tasks: 5
specialization_context:
  language: [...]                 # If language specialist
  frameworks: [...]               # If framework specialist
  file_patterns: [...]            # If file-pattern specialist
  domain_keywords: [...]          # Domain-specific routing
  writing_style: [...]            # If writing specialist
  complexity_preference: [low, medium]
---
```

### 4. Write Profile Sections

Follow your parent's structure. Include:

- **Purpose** — What problems does this specialist solve?
- **Specialization** — Primary focus, secondary awareness, what to avoid
- **Collaboration Contract** — How others should work with this specialist
- **Directives** — Which doctrine directives apply

Example:

```markdown
# Agent Profile: My Specialist

## Purpose

[1-2 sentences describing why this specialist exists]

## Specialization

- **Primary focus:** [Main responsibilities]
- **Secondary awareness:** [Related but not core]
- **Avoid:** [Out of scope]
- **Success means:** [How to measure success]

## Collaboration Contract

- [Behavioral commitments]
- [Escalation rules]
- [Interaction patterns]
```

### 5. Test with Validation

Validate your new specialist:

```bash
python tools/validators/validate-agent-hierarchy.py
```

Expected output:

```
✅ Validation passed
   - 25 agents loaded
   - 0 circular dependencies
   - 0 missing parents
   - 0 priority conflicts
```

Common errors and fixes:

| Error | Fix |
|-------|-----|
| `Missing parent: backend-benny` | Check `specializes_from` value spelling |
| `Circular dependency detected` | Ensure specialist doesn't declare parent as its child |
| `Priority conflict in context: python` | Two agents with same priority matching same context—adjust one |

---

## Migrating Existing Tasks

### What Happens During Migration

When you add new specialists, existing generic assignments don't automatically update. Manager Mike performs periodic **reassignment passes** to upgrade tasks to more specific agents:

1. **Scan** all `new` and `assigned` tasks
2. **Match** task context against hierarchy (language, frameworks, files)
3. **Select** most appropriate specialist using SELECT_APPROPRIATE_AGENT
4. **Update** task.agent field and log rationale
5. **Respect** pinned tasks (don't reassign if `task.pinned: true`)

### Triggering a Reassignment Pass

For immediate migration:

```bash
python tools/scripts/complete_task.py reassign-pass --dry-run
python tools/scripts/complete_task.py reassign-pass
```

This updates assignments and generates audit report:

```
Reassignment Pass Report
========================
Tasks evaluated: 47
Tasks upgraded: 12
  backend-benny → python-pedro: 8 tasks
  backend-benny → java-jenny: 4 tasks
Tasks unchanged: 35
Tasks pinned: 0
```

### Pinning Tasks (Do Not Reassign)

If a task should NOT be reassigned despite matching specialist context, pin it:

```yaml
task:
  id: task-001
  title: Complex cross-language refactor
  agent: backend-benny
  pinned: true  # Don't reassign to Python Pedro
  reason: Requires multi-language context
```

### Timeline

- **Day 0:** Add new specialist to `.doctrine-config/custom-agents/`
- **Day 1:** Run `validate-agent-hierarchy.py` (no errors)
- **Day 1:** Run reassignment pass (review audit report)
- **Day 2-7:** Monitor if specialist is being used correctly
- **Week 2:** Gather feedback, adjust routing priorities if needed

---

## Validation

### Running Validation Script

```bash
python tools/validators/validate-agent-hierarchy.py
```

**What it checks:**

- ✅ All agents loadable and well-formed
- ✅ No circular parent-child dependencies
- ✅ All `specializes_from` parents exist
- ✅ No priority conflicts (two specialists with same priority matching same context)
- ✅ `.doctrine-config/custom-agents/` specialists valid

### Interpreting Results

**Pass (0 issues):**
```
✅ Validation passed (25 agents, 0 issues)
```

**Fail (with issues):**
```
❌ Validation failed (25 agents, 3 issues):
   1. Circular dependency: python-pedro → backend-benny → python-pedro
   2. Missing parent: java-jenny specializes_from backend-dev (not found)
   3. Priority conflict in context python+pytest (two agents with priority 80)
```

**Fix circular dependencies:**
- Review `specializes_from` declarations
- Ensure: A → B → C (not A → B → A)

**Fix missing parents:**
- Correct spelling: `backend-dev` vs `backend-benny`
- Check parent exists in `doctrine/agents/`

**Fix priority conflicts:**
- Adjust `routing_priority` (one specialist lower, one higher)
- Example: `routing_priority: 80` and `routing_priority: 85`

---

## Frequently Asked Questions

### Q: What if my specialist and parent both match a task context?

**A:** Routing priority determines preference. Specialists typically have higher priority (70-90) than parents (50).

**Example:**
- Task: Python code review
- Matches: `backend-benny` (generic backend) + `python-pedro` (Python specialist)
- Result: python-pedro selected (priority 80 > 50)

To prefer parent in edge cases, set specialist to lower priority:
```yaml
routing_priority: 45  # Lower than parent default of 50
```

### Q: Can I have multiple levels of specialization?

**A:** Yes, but keep it shallow (max 2-3 levels):

```
Backend Benny [priority 50]
├── Python Pedro [priority 80]
│   └── FastAPI Specialist [priority 85]  # OK but rare
└── Java Jenny [priority 80]
```

Deeper nesting makes routing complex and hard to debug.

### Q: What if no specialist matches?

**A:** Task falls back to parent agent.

**Example:**
- Task: Go microservice (no Go specialist in hierarchy)
- Result: assigned to `backend-benny` (parent)

This is intentional—parents are always valid fallback.

### Q: How do I disable a specialist temporarily?

**A:** Remove from `.doctrine-config/custom-agents/`:

```bash
rm .doctrine-config/custom-agents/user-guide-ursula.agent.md
```

Next reassignment pass will revert Ursula tasks back to Editor Eddy. No data loss—tasks are preserved.

To re-enable, restore the file:

```bash
git checkout .doctrine-config/custom-agents/user-guide-ursula.agent.md
```

### Q: Can a specialist have multiple parents?

**A:** No. Each specialist has exactly one parent (`specializes_from: parent`).

If you need hybrid behavior, create separate specialists:
- `python-pedro` → specializes from `backend-benny`
- `python-docs` → specializes from `editor-eddy`

Manager Mike routes based on task context (code vs documentation).

### Q: How does workload affect routing?

**A:** If a specialist is overloaded (5+ active tasks), Manager Mike penalties their score and may prefer parent:

- 0-2 active tasks: No penalty
- 3-4 active tasks: 15% penalty
- 5+ active tasks: 30% penalty

This prevents specialist bottlenecks. If Python Pedro is busy, work routes to Backend Benny temporarily.

### Q: Can I adjust complexity preferences?

**A:** Yes. Adjust `complexity_preference` in frontmatter:

```yaml
# Specialist comfortable with complex work
complexity_preference: [low, medium, high]

# Specialist prefers narrow scope
complexity_preference: [low]
```

Higher complexity +10% boost for parents, -10% for specialists (because complex tasks need broader context).

---

## Related Documentation

- **Decision:** [DDR-011: Agent Specialization Hierarchy](../../doctrine/decisions/DDR-011-agent-specialization-hierarchy.md)
- **Tactic:** [SELECT_APPROPRIATE_AGENT](../../doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md) (routing algorithm)
- **Validation:** `tools/validators/validate-agent-hierarchy.py`
- **Existing Specialists:** `doctrine/agents/python-pedro.agent.md`, `doctrine/agents/java-jenny.agent.md`

---

**Status:** Ready for adoption
**Version:** 1.0
**Last Updated:** 2026-02-12
