<!-- The following information is to be interpreted literally -->

# 002 Context Notes Directive

- Specialized profiles in `.github/agents/` may refine tone/modes.
- Global template `AGENTS.md` supersedes repo instructions unless explicitly overridden.
- Treat shorthand commands cautiously until mapped.

## Token Discipline

- Keep **overarching guidance** (Operational/Strategic references, directive summaries, repository-structure hints) loaded at all times.
- Swap detailed descriptions in and out of active memory based on the current task. Offload specifics (notes, key points, enumerations) into
  `work/notes/external_memory/` or similar scratch files so context windows stay minimal.
- When reloading a stored note, cite it explicitly to show continuity.
- Never drop the high-level guardrails—even when token-constrained. If space is limited, evict task-specific detail first, not the governance layers.

**Use Cases:
** Apply this directive when balancing multiple guidance sources, managing prompt size, or reconciling specialized agent roles with global governance.

## Behavioural Norms

* **CRITICAL:** Always maintain access to core behavioral norms and collaboration contracts, even if detailed context must be offloaded.
* **CRITICAL:** Never assume shorthand commands (e.g.,
  `/validate-alignment`) are universally understood without explicit mapping in the current context.
* **CRITICAL:** Always cite offloaded notes when reloading them to ensure traceability and context continuity.
* **CRITICAL:** NEVER update or override global templates, or behavioral norms without explicit authorization.
* **CRITICAL:
  ** Prioritize loading overarching guidance (e.g., operational/strategic references, directive summaries) over task-specific details when token limits are tight.
* **RECOMMENDED:** Regularly review loaded context to ensure alignment with current task scope and constraints.