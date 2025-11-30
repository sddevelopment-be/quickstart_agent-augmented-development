# ADR-021: Model Routing Strategy (OpenRouter + OpenCode.ai)

status: Accepted
date: 2025-11-30

## Context

The agentic stack requires access to multiple LLM vendors and local models with predictable behavior, pricing transparency, and fallback paths. Brainstorm outcomes indicate OpenRouter and OpenCode.ai both meet the routing need with complementary strengths.

## Decision

Use a router-first approach for programmatic calls:

- Prefer OpenRouter for breadth of models and mature ecosystem.
- Use OpenCode.ai where local model integration and cleaner interfaces are desired.
- Maintain direct vendor API integrations (OpenAI, Anthropic) for capabilities not exposed via routers.

## Rationale

- Vendor diversity and easy swapping between models.
- Centralized retry/fallback and cost-aware routing.
- Transparent exposure of raw model names and limits for agent determinism.
- Migration resilience if one router changes terms or availability.

## Implementation Notes

- Keep orchestrator contracts independent of router specifics; store router configuration separately.
- Document raw model identifiers and context windows used by agents.
- Validate tool-calls and structured outputs locally using Python validators.

## Consequences

- Positive:
  - Cost control and resilience via fallback models.
  - Faster adoption of new models without orchestrator changes.
  - Cleaner separation between governance and execution concerns.
- Negative:
  - Additional coordination and configuration to keep routers consistent.
  - Potential small latency overhead due to routing.

## Alternatives Considered

- Direct APIs only: simpler but less flexible, harder cost control.
- Single router dependency: increases risk; lesser migration resilience.

## References

- `work/notes/ideation/full_automatic_agents/brainstorm_part1.md`
- `work/notes/ideation/full_automatic_agents/brainstorm_part2.md`
- `docs/architecture/architectural_vision.md`
