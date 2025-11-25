# Approaches

This directory contains an overview of agentic approaches. These are descriptions of step-by-step guides, to be used as a reference by agents to simplify their task execution.

**Goal:** Reduce reasoning complexity and search-space by collecting task-specific operational approaches here.

## Available Approaches

| Approach | Description | Agent(s) | Version |
|----------|-------------|----------|---------|
| [file-based-orchestration.md](file-based-orchestration.md) | File-based asynchronous agent coordination pattern using YAML tasks and directory state machines | All agents | 1.0.0 |
| [decision-first-development.md](decision-first-development.md) | Step-by-step workflow for capturing architectural decisions during development with flow-aware timing | All agents | 1.0.0 |

## Usage

Agents should reference approaches when:
- Executing tasks that match a documented pattern
- Learning operational workflows
- Needing step-by-step guidance for complex coordination

Load approach content as context when applicable to reduce reasoning overhead and ensure consistency.