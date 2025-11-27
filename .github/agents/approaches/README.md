# Approaches

This directory contains an overview of agentic approaches. These are descriptions of step-by-step guides, to be used as a reference by agents to simplify their task execution.

**Goal:** Reduce reasoning complexity and search-space by collecting task-specific operational approaches here.

## Available Approaches

| Approach | Description | Agent(s) | Version |
|----------|-------------|----------|---------|
| [work-directory-orchestration.md](work-directory-orchestration.md) | Canonical guide to the file-based orchestration workflow that powers `work/` | All agents | 1.1.0 |
| [decision-first-development.md](decision-first-development.md) | Step-by-step workflow for capturing architectural decisions during development with flow-aware timing | All agents | 1.0.0 |
| [tooling-setup-best-practices.md](tooling-setup-best-practices.md) | Best practices for tool selection, configuration, and maintenance in agent-augmented development environments | All agents | 1.0.0 |
| [target-audience-fit.md](target-audience-fit.md) | Workflow for applying persona-driven communication (“Target Audience Personas”) to any artifact | Writing-focused agents | 1.0.0 |
| [locality-of-change.md](locality-of-change.md) | Comprehensive guide to avoiding premature optimization through problem measurement and severity assessment | All agents | 1.0.0 |

## Usage

Agents should reference approaches when:
- Executing tasks that match a documented pattern
- Learning operational workflows
- Needing step-by-step guidance for complex coordination

Load approach content as context when applicable to reduce reasoning overhead and ensure consistency.
