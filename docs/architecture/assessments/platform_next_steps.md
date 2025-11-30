# Platform Next Steps: Multi-Tier Agentic Framework

Version: 1.0.0  
Date: 2025-11-30  
Owner: Planning Petra

## Context Overview

We have refined our architecture into a four-tier runtime framework that separates developer ergonomics, orchestration/governance, model routing, and model execution.

- Architectural Vision updated: see [architectural_vision.md](../architectural_vision.md)
- New ADRs:
  - [ADR-020: Multi-Tier Agentic Runtime Architecture](../adrs/ADR-020-multi-tier-agentic-runtime.md)
  - [ADR-021: Model Routing Strategy (OpenRouter + OpenCode.ai)](../adrs/ADR-021-model-routing-strategy.md)
- Prior related ADRs:
  - [ADR-002: Adopt OpenCode Specification for Agent Portability](../adrs/ADR-002-portability-enhancement-opencode.md)
  - [ADR-009: Orchestration Metrics Standard](../adrs/ADR-009-orchestration-metrics-standard.md)
- Brainstorm references:
  - [Brainstorm Part 1](../../../work/notes/ideation/full_automatic_agents/brainstorm_part1.md)
  - [Brainstorm Part 2](../../../work/notes/ideation/full_automatic_agents/brainstorm_part2.md)

This plan prioritizes portable orchestration and vendor agility, leveraging routers (OpenRouter/OpenCode.ai), direct APIs (OpenAI/Anthropic) for advanced capabilities, and local models (Ollama) for private worker tasks.

## Objectives

- Formalize router configurations and model catalogs for deterministic selection and fallbacks.
- Establish minimal orchestration interfaces isolating router specifics from agent contracts.
- Extend task descriptors to include model selection hints and execution constraints.
- Operationalize local worker nodes (Ollama) for offline/private batch tasks.
- Strengthen validation and CI to enforce consistency and traceability.

## Work Breakdown (Specialist Agent Tasks)

- Manager Mike
  - Define iteration using the template: [Run Orchestration Iteration](../../../.github/ISSUE_TEMPLATE/run-iteration.md)
  - Create and track an iteration issue titled `Run orchestration cycle - <YYYY-MM-DD>`
  - Ensure outcomes recorded in `work/collaboration/AGENT_STATUS.md`

- Devops Danny
  - Create router config: `ops/config/model_router.yaml` with primary=OpenRouter, secondary=OpenCode.ai.
  - Include model aliases and raw IDs for GPT-5/4.1, Claude Sonnet/Opus, Codestral, DeepSeek, Llama3 variants.
  - Add fallback policy and pricing ceilings.
  - Implement loader/validator: `ops/scripts/validate-model-router.py` to verify IDs, context windows, and fallbacks.

- Diagram Daisy
  - Produce diagrams-as-code for Layer 0–3 flows: `docs/architecture/diagrams/multi_tier_runtime.mmd` in PlantUML, using a C4 Context/Container/Component diagram (or combination thereof) .
  - Cross-link diagrams from [architectural_vision.md](../architectural_vision.md) and ADR-020/ADR-021.

- Spec Scribe Sally
  - Extend agent task descriptor template: `docs/templates/agent-tasks/model-selection.yaml` with fields:
    - `task_type`, `preferred_models`, `hard_constraints` (context window, tool-calls), `cost_ceiling`, `privacy_requirements`.
  - Update `.github/agents/directives/` with an addendum requiring explicit model selection hints.

- Devops Danny
  - Update validator: `validation/validate-task-schema.py` to enforce model selection hints and router constraints.
  - Add CI hook to check ADR links and diagram consistency with [architectural_vision.md](../architectural_vision.md).

- Devops Danny
  - Create `ops/config/ollama_models.yaml` listing supported local models and use-cases.
  - Implement `ops/scripts/run-local-worker.py` to execute batch tasks with structured outputs and local validators.

- Devops Danny
  - Integrate router/model selection metrics with ADR-009 via `ops/dashboards/generate-dashboard.py`.
  - Track token usage, duration, artifacts, fallbacks, and success rates.

## Milestones & Deliverables

- M1: Router config + validator
  - Files: `ops/config/model_router.yaml`, `ops/scripts/validate-model-router.py`
  - Validation report attached to CI and iteration issues.

- M2: Orchestrator interface
  - Files: `ops/orchestration/model_client.py`
  - Functions: `select_model(task_type, constraints)`, `invoke(model_id, prompt, tools)`, `fallback_chain(model_id, error)`

- M3: Task descriptor and directives update
  - Files: `docs/templates/agent-tasks/model-selection.yaml`, `.github/agents/directives/` addendum
  - Updated examples in `work/` tasks.

- M4: Local worker operationalization
  - Files: `ops/config/ollama_models.yaml`, `ops/scripts/run-local-worker.py`
  - Demo task executed and validated.

- M5: Diagrams and docs sync
  - Files: `docs/architecture/diagrams/multi_tier_runtime.mmd`
  - Links embedded in [architectural_vision.md](../architectural_vision.md), ADR-020, ADR-021.

- M6: Metrics and CI
  - Updated dashboards and CI validation for new configs and descriptors.

## Risks & Mitigations

- Router availability or terms changes
  - Mitigation: dual-router config + direct API paths retained.
- Inconsistent model IDs/context windows across routers
  - Mitigation: central validator + explicit catalog.
- Complexity creep in orchestrator code
  - Mitigation: minimal interface, strict separation from router specifics.
- Local model quality variance
  - Mitigation: usage scoped to batch/offline tasks; evaluate models quarterly.

## Execution Notes

- Use `/analysis-mode` for planning and orchestration edits per [AGENTS.md](/AGENTS.md).
- Validate changes using scripts under `validation/` and `ops/` before merging.
- Record decisions in ADR updates; attach iteration summaries under `work/collaboration/`.

## Next Actions (Immediate)

1. Create `ops/config/model_router.yaml` and `ops/scripts/validate-model-router.py`.  
2. Draft `ops/orchestration/model_client.py` with stubbed methods and docstrings.  
3. Author `docs/templates/agent-tasks/model-selection.yaml` and reference it in `.github/agents/directives/` addendum.  
4. Prepare `ops/config/ollama_models.yaml` and `ops/scripts/run-local-worker.py`.  
5. Generate `docs/architecture/diagrams/multi_tier_runtime.mmd` and link it.  
6. Update CI to run router and task-schema validators.

---

Prepared by: Architect Alphonso  
Mode: `/analysis-mode`
