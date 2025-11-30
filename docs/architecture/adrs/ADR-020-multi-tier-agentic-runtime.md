# ADR-020: Multi-Tier Agentic Runtime Architecture

status: Accepted
date: 2025-11-30

## Context

Brainstorming sessions on multi-vendor agentic workflows highlighted a need to clearly separate ergonomics, orchestration, routing, and execution concerns. The repository already defines governance layers (AGENTS.md, directives, profiles), but runtime responsibilities required consolidation to improve portability, traceability, and vendor agility.

## Decision

Adopt a four-tier runtime architecture:

- Layer 0: Human Interface & Utilities
  - IDE workflows (GitHub Copilot), command aliases, local utility scripts.
- Layer 1: Orchestration & Governance
  - Agent specifications (`AGENTS.md`, `.github/agents/**`), YAML task descriptors, Python validators, Titan scripts.
- Layer 2: Model Routing
  - Vendor-neutral routers (OpenRouter and/or OpenCode.ai) for multi-model selection, fallbacks, and cost control.
- Layer 3: Model Execution
  - Direct APIs (OpenAI GPT-5/4.1, Anthropic Claude) and local models (Ollama: Llama3, DeepSeek, Codestral).

## Rationale

- Separation of concerns keeps orchestration portable and auditable.
- Router layer reduces lock-in and provides graceful degradation.
- Direct APIs preserve access to advanced capabilities (long context, structured JSON, explicit tool-calls).
- Local models enable privacy, offline work, and cost-free batch operations.

## Consequences

- Positive:
  - Clear boundaries for responsibilities and evolution.
  - Easier migration across vendors and routers.
  - Improved cost control and fallback strategies.
  - Stronger traceability across ADRs and design docs.
- Negative:
  - Additional configuration surface for routing.
  - Coordination needed between orchestrator and router policies.

## Alternatives Considered

- Single-vendor reliance via IDE only: rejected (limited capabilities, lock-in).
- Heavy agent frameworks (LangChain/LlamaIndex) as orchestrator: rejected for this phase (complexity overhead).
- Routerless direct API usage: feasible but reduces diversity and fallback control.

## References

- `docs/architecture/architectural_vision.md` (updated multi-tier section)
- `work/notes/ideation/full_automatic_agents/brainstorm_part1.md`
- `work/notes/ideation/full_automatic_agents/brainstorm_part2.md`
