# OVERVIEW: SDDevelopment LLM Service + Doctrine Stack

- Author: lexical
- Date: 2026-02-14
- References: `work/kitty/sddev_stack_reference/*`

## Main Ideas
1. Layered governance via Doctrine stack
- Guidelines -> Approaches -> Directives -> Tactics -> Templates.
- Purpose: predictable agent behavior, reasoning discipline, output contracts.

2. Control-plane architecture
- Command/query separation with service/distributor/execution/storage/query layers.
- Designed for operational observability and policy enforcement.

3. Routing and policy model
- Task-aware model/tool selection via routing engine/provider concepts.
- Policy enforcement for constraints and cost/budget behavior.

4. Execution adapter abstraction
- CLI/SDK/tool adapters isolate vendor/tool differences.

5. Telemetry and query surfaces
- Event logging and queryable read models for diagnostics/governance insight.

## Core Terminology
- `Doctrine Stack`: layered governance system for agent behavior.
- `Guideline`: durable value/preference constraints.
- `Directive`: explicit mandatory instruction/constraint.
- `Tactic`: procedural execution playbook.
- `Template`: output shape contract.
- `Coordination Service`: command-side orchestration service.
- `Distributor`: strategy for dispatching work.
- `Execution Adapter`: provider/tool-specific invocation boundary.
- `Telemetry Store`: event/usage/cost tracking persistence.
- `Query Service`: read-model facade for dashboards/console.

## Architectural Position
LLM service and doctrine concepts provide governance + infrastructure depth. In this proposal they are integrated as enhancement layers around Spec Kitty, not as a replacement runtime.
