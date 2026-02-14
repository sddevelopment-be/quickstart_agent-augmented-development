# Domain 03: Agent and Mission Orchestration

## Conceptual Focus
Vocabulary for agent integration, mission selection, context shaping, and command interoperability.

## Canonical Terms
- `supported agents`
- `agent context`
- `workflow commands`
- `slash commands`
- `mission`
- `active mission`
- `config-driven agent management`

## Domain Semantics
- Agent support is treated as a first-class compatibility surface.
- Mission language expresses domain-specific behavior profiles for generated instructions.
- Configuration and context terms mediate what command templates and behaviors agents receive.

## Evidence Anchors
- `AGENTS.md`
- `docs/explanation/mission-system.md`
- `docs/reference/supported-agents.md`
- `src/specify_cli/core/agent_context.py`
- `architecture/adrs/2026-01-23-6-config-driven-agent-management.md`
