# Proposal: Plug Doctrine into Spec Kitty (Enhance, Do Not Fork)

- Date: 2026-02-14
- Owner: architect-alphonso
- Status: Proposed
- Scope: Integrate Doctrine as a governance plugin layer for Spec Kitty while preserving Spec Kitty as the primary product/workflow engine.

## Executive Intent
This proposal formalizes a **Spec Kitty-first integration** model:
- Spec Kitty remains authoritative for mission flow, spec lifecycle, orchestration, and routing.
- Doctrine is plugged in as a governance enhancement layer.
- Local doctrine overrides (`.doctrine-config/`) are supported as project policy customization.

This is explicitly **not** a proposal to extract parts of Spec Kitty into a separate framework.

## Strategic Position
1. Keep Spec Kitty as the main platform:
- spec lifecycle (`spec -> plan -> tasks -> implement -> review -> accept -> merge`)
- mission adaptation
- WP orchestration and worktree lifecycle
- routing and execution extensions

2. Attach Doctrine as policy/governance plugin:
- `doctrine/` stack reused as-is
- `.doctrine-config/` used for local override policy
- governance checks executed via extension hooks

3. Map, do not replace:
- generic specifications-domain abstractions map to Spec Kitty mission/spec semantics
- no takeover of Spec Kitty schema, lanes, or command contract

## Architecture Contract
### Ownership by Layer
1. Layer 1 - Governance Plugin: Doctrine + `.doctrine-config`
2. Layer 2 - Specification Domain: Spec Kitty `kitty-specs/*` + missions
3. Layer 3 - Orchestration: Spec Kitty workflow engine + dependency/worktree orchestration
4. Layer 4 - Routing: Spec Kitty provider-based task-to-model/tool routing
5. Layer 5 - Execution: Spec Kitty execution runtime + LLM vendor adapter framework

### Precedence (when Doctrine is enabled)
1. Constitution (project-local top policy)
2. Doctrine Guidelines
3. Doctrine Directives
4. Spec Kitty mission-level workflow guidance
5. Doctrine Tactics/Templates

Constraint: Spec Kitty lane and merge semantics remain authoritative for lifecycle progression.

## Extension Design
### `governance-doctrine` extension
Purpose:
- load doctrine core + local overrides
- run lifecycle policy checks
- expose normalized pass/warn/block results

Lifecycle hook targets:
- `pre_plan`, `pre_tasks`, `pre_implement`, `pre_review`, `pre_accept`

Output contract:
- `status: pass|warn|block`
- `reasons: []`
- `directive_refs: []`

### `routing-provider` extension interface
Purpose:
- plug model/tool/agent routing into Spec Kitty without hard-coding vendors

Conceptual interface:
- `route_task(task_context) -> RoutingDecision`
- `RoutingDecision = {agent_key, tool, model, fallback_chain, rationale}`

Doctrine policy provider:
- optional provider that reads doctrine policy files and returns routing hints
- routing authority stays in Spec Kitty extension contract

### Event bridge
Purpose:
- emit normalized events from lane transitions and command lifecycle
- feed governance checks and telemetry without mutating WP schema

## Implementation Roadmap
1. Phase 1 - Governance plugin bootstrap
- optional doctrine install/sync
- constitution precedence block injection

2. Phase 2 - Governance lifecycle hooks
- advisory mode first, block mode later

3. Phase 3 - Routing provider support
- default provider + doctrine policy provider

4. Phase 4 - Execution telemetry and query surfaces
- normalized event emission
- execution metadata capture via adapter framework

## Risks and Controls
1. Dual-authority confusion
- control: explicit precedence + command-time policy trace output

2. Over-coupling to doctrine internals
- control: extension consumes stable outputs, not parser internals

3. Vendor lock-in in routing
- control: provider interface, fallback chain, adapter boundary

4. Workflow regressions
- control: advisory rollout and feature flags

## Acceptance Criteria
1. Doctrine is optional and backward compatible when disabled.
2. Enabling doctrine does not alter core WP frontmatter schema.
3. Governance checks execute at lifecycle hooks with deterministic outcomes.
4. Routing provider can be swapped without core command rewrites.
5. Spec Kitty remains the single orchestrator and workflow authority.

## Linked Artifacts
- `work/kitty/proposal/README.md`
- `work/kitty/proposal/VISION.md`
- `work/kitty/proposal/OVERVIEW_llm_service.md`
- `work/kitty/proposal/OVERVIEW_spec_kitty.md`
- `work/kitty/proposal/EXECUTIVE_SUMMARY.md`
- `work/kitty/proposal/spec-kitty-doctrine-layered-target-architecture.puml`
