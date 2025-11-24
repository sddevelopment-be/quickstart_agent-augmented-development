# Architecture Decision Records (ADRs)

Architecture Decision Records (ADRs) are concise documents that capture important architectural decisions made throughout the lifecycle of this project. Each ADR provides context, rationale, and consequences for a specific decision, ensuring traceability and clarity for current and future contributors.

## ADR Index (Canonical)

| ADR Number                                                      | Title                                         | Date       | Status             | Description                                                                                    |
|-----------------------------------------------------------------|-----------------------------------------------|------------|--------------------|------------------------------------------------------------------------------------------------|
| [ADR-001](ADR-001-modular-agent-directive-system.md)            | Modular Agent Directive System                | 2025-11-17 | Accepted           | Adopted a modular, directive-based system for agent governance, replacing the monolithic spec. |
| [ADR-003](ADR-003-task-lifecycle-state-management.md)           | Task Lifecycle and State Management           | 2025-11-20 | Accepted           | Establishes explicit task lifecycle states and transition rules for multi-agent orchestration. |
| [ADR-004](ADR-004-work-directory-structure.md)                  | Work Directory Structure and Conventions      | 2025-11-20 | Accepted           | Defines hierarchical `work/` directory layout for tasks, ownership, and retention.             |
| [ADR-005](ADR-005-coordinator-agent-pattern.md)                 | Coordinator Agent Pattern                     | 2025-11-20 | Accepted           | Introduces a meta-agent for assignment, sequencing, monitoring, and error escalation.          |
| [ADR-006](ADR-006-adopt-three-layer-governance-model.md)        | Adopt Three-Layer Governance Model            | 2025-11-22 | Accepted           | Introduces strategic, operational, and execution governance layers via metadata tagging.       |
| [ADR-007](ADR-007-repository-restructuring-layer-separation.md) | Repository Restructuring for Layer Separation | 2025-11-22 | Rejected / Adapted | Rejects physical layer separation; adopts logical metadata classification strategy.            |
| [ADR-008](ADR-008-file-based-async-coordination.md)             | File-Based Asynchronous Agent Coordination    | 2025-11-20 | Proposed           | Introduces file-based task coordination using repository directories and YAML task files.      |
| [ADR-009](ADR-009-orchestration-metrics-standard.md)            | Orchestration Metrics and Quality Standards   | 2025-11-23 | Accepted           | Establishes mandatory metrics capture and quality standards for orchestrated agent tasks.      |
| [ADR-010](ADR-010-github-copilot-tooling-setup.md)              | GitHub Copilot Tooling Setup                  | 2025-11-23 | Accepted           | Defines environment setup and tooling installation for GitHub Copilot Workspace agents.        |
| [ADR-011](ADR-011-follow-up-task-lookup-pattern.md)             | Follow-Up Task Lookup Pattern                 | 2025-11-24 | Rejected           | Rejects centralized lookup table for handoffs; recommends agent profile enhancement instead.   |


> Uniqueness Guarantee: Each ADR number in the table above maps to exactly one canonical ADR file. Historical superseded ADRs MUST NOT be edited except to archive them (recommended future path:
`adrs/_historical/`).
