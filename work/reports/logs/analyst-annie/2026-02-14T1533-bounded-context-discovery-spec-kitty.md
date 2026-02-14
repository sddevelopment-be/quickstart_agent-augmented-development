# Specialist Report: Analyst Annie

## Scope
Infer bounded contexts from terminology drift and module/documentation clustering.

## Evidence Highlights
- Workflow lifecycle vocabulary in `README.md`, `spec-driven.md`, and `docs/tutorials/your-first-feature.md`.
- Worktree/workspace and dependency semantics in `docs/explanation/workspace-per-wp.md`.
- Agent and mission semantics in `AGENTS.md`, `docs/explanation/mission-system.md`, `src/specify_cli/core/agent_context.py`.
- Operational runtime concepts in `src/specify_cli/dashboard/`, `src/specify_cli/events/`, and `src/specify_cli/orchestrator/`.
- Governance vocabulary from ADR corpus in `architecture/adrs/` and `architecture/README.md`.

## Proposed Domains
1. Specification Lifecycle and Work Package Management
2. Workspace and Branch Topology
3. Agent and Mission Orchestration
4. Dashboard and Runtime Observability
5. Template, Migration, and Upgrade Distribution
6. Quality, Validation, and Adversarial Hardening

## Boundary Signals
- `lane` vs `merge` semantics changed and clarified by ADRs (notably ADR-21 references).
- `workspace` and `worktree` used as operationally distinct terms in workspace-per-WP docs and code.
- `mission` terms cluster around prompt strategy and artifact profiles, not around git topology.
- `dashboard` terms cluster around process lifecycle and scanner diagnostics.
