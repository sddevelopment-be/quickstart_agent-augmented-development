# Core Terminology Index

| Term | Definition (in Spec Kitty context) | Primary Domain |
|---|---|---|
| Spec-Driven Development (SDD) | Workflow model where specification artifacts drive implementation phases. | Specification Lifecycle |
| Feature Spec | Top-level feature intent artifact under `kitty-specs/<feature>/spec.md`. | Specification Lifecycle |
| Plan | Implementation approach artifact (`plan.md`) generated after specification. | Specification Lifecycle |
| Work Package (WP) | Independently deliverable implementation slice (`WPxx`). | Specification Lifecycle |
| Lane | Workflow status field in WP frontmatter (`planned`, `doing`, `for_review`, `done`). | Specification Lifecycle |
| Finalize Tasks | Step that validates and operationalizes task/work package structure before implementation. | Specification Lifecycle |
| Review | Workflow stage moving a WP toward acceptance readiness. | Specification Lifecycle |
| Accept | Validation gate confirming feature readiness before merge. | Specification Lifecycle |
| Worktree | Git worktree instance used to isolate implementation context. | Workspace/Branch Topology |
| Workspace | Operational working context for a WP, including persisted context metadata. | Workspace/Branch Topology |
| Base Workspace | Parent workspace used when implementing dependent work packages. | Workspace/Branch Topology |
| Target Branch | Intended integration branch for status/merge routing. | Workspace/Branch Topology |
| Dependency Graph | Directed WP dependency model used for ordering and merge logic. | Workspace/Branch Topology |
| Merge Preflight | Checks executed before merge execution. | Workspace/Branch Topology |
| Status Resolver | Logic for lane/conflict/status interpretation during merge/review flows. | Workspace/Branch Topology |
| Agent Context | Runtime instructions/config controlling agent behavior for a project/feature. | Agent/Mission Orchestration |
| Supported Agents | AI tools/platforms with template + command integration in Spec Kitty. | Agent/Mission Orchestration |
| Mission | Domain-specific workflow profile defining prompts, rules, and outputs. | Agent/Mission Orchestration |
| Active Mission | Currently selected mission configuration for a feature/project. | Agent/Mission Orchestration |
| Slash Commands | Agent-facing command vocabulary (for example `/spec-kitty.plan`). | Agent/Mission Orchestration |
| Workflow Commands | CLI commands that advance lifecycle steps while maintaining lane integrity. | Agent/Mission Orchestration |
| Dashboard Lifecycle | Start/health/stop runtime lifecycle for dashboard service. | Dashboard/Observability |
| Health Check | Runtime availability probe used by dashboard diagnostics and startup logic. | Dashboard/Observability |
| Diagnostics | CLI/runtime checks for environment and dashboard correctness. | Dashboard/Observability |
| Scanner | Component that reads feature/task state for dashboard views. | Dashboard/Observability |
| Event Log | Structured runtime event stream used for status/telemetry synchronization. | Dashboard/Observability |
| Template Source | Canonical location where command templates originate. | Template/Migration/Upgrade |
| Command Template | Prompt or command artifact generated per agent/mission configuration. | Template/Migration/Upgrade |
| Migration Registry | Ordered catalog of migrations and their metadata. | Template/Migration/Upgrade |
| Upgrade Runner | Execution path applying template/schema/version migrations. | Template/Migration/Upgrade |
| Manifest | Project-level metadata describing runtime/tooling/template configuration. | Template/Migration/Upgrade |
| Context Validation | Checks that execution context is coherent before command progression. | Quality/Validation |
| Metadata Validation | Checks that frontmatter/file state match expected workflow structure. | Quality/Validation |
| Plan Validation | Guardrail preventing lifecycle progression with invalid/incomplete plans. | Quality/Validation |
| Encoding Validation | Guardrail for text encoding issues that can break dashboard/workflows. | Quality/Validation |
| Path Validation | Security guardrail against invalid/malicious paths. | Quality/Validation |
| Adversarial Suite | Tests that probe security and robustness failures by attack pattern. | Quality/Validation |
| CSV Schema Enforcement | Deterministic schema validation for research outputs. | Quality/Validation |
