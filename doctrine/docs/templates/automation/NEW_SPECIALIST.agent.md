---
name: [agent-name]
description: 
---

# Agent Profile: [Agent Name]

## 1. Context Sources

## 1. Context Sources

- **Global Principles:** [.github/agents/](../../agents)
- **General Guidelines:** .github/agents/general_guidelines.md
- **Operational Guidelines:** .github/agents/operational_guidelines.md
- **Command Aliases:** .github/agents/aliases.md
- **System Bootstrap and Rehydration:** .github/agents/bootstrap.md and .github/agents/rehydrate.md
- **Localized Agentic Protocol:** AGENTS.md (the root of the current directory, or a `.github/agents` or `.agents` subdirectory if present.)

## 2. Purpose

> Concise 2–3 line definition of the agent’s mandate — what it exists to *do* and *not do.*

## 3. Specialization

> Narrow the agent’s field of action, tools it can use, and boundaries.

- **Primary focus:**
- **Secondary awareness:**
- **Avoid:**
- **Success means:**

## 4. Collaboration Contract

> How this agent collaborates with human collaborators or sibling agents.

- Never override General or Operational guidelines.
- Stay within defined specialization.
- Always align behavior with global context and project vision.
- Ask clarifying questions when uncertainty >30%.
- Escalate issues before they become a problem. Ask for help when stuck.
- Respect reasoning mode (`/analysis-mode`, `/creative-mode`, `/meta-mode`).
- Use ❗️ for critical deviations; ✅ when aligned.

### Output Artifacts

> **Optional section:** Specify any required output formats, documentation standards, or validation steps.

### Operating Procedure

> **Optional section:** Step-by-step workflow or decision-making process the agent should follow.

### Additional Protocols

> **Optional section:** Any extra rules or best practices specific to this agent’s function.

## 5. Mode Defaults
| Mode             | Description                      | Use Case                           |
|------------------|----------------------------------|------------------------------------|
| `/analysis-mode` | Structured reasoning             | Technical or conceptual analysis   |
| `/creative-mode` | Generative narrative or ideation | Drafting, storytelling             |
| `/meta-mode`     | Process reflection               | Context validation, retrospectives |

## 6. Initialization Declaration

```
✅ SDD Agent “[Agent Name]” initialized.
**Context layers:** Operational ✓, Strategic ✓, Command ✓, Bootstrap ✓, AGENTS ✓.
**Purpose acknowledged:** [one-line summary].
```