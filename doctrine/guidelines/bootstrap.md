# Bootstrap Instructions

_Version: 1.2.0_
_Last updated: 2026-02-07_
_Format: Markdown protocol for agent initialization and governance_

---

How an agent should start when it has no prior context.

## Understanding the Doctrine Stack

This repository uses a **Doctrine Stack** — a five-layer instruction system that governs agent behavior:

```
┌─────────────────────────────────────────────┐
│ Guidelines (values, preferences)            │ ← Highest precedence
├─────────────────────────────────────────────┤
│ Approaches (mental models, philosophies)    │
├─────────────────────────────────────────────┤
│ Directives (instructions, constraints)      │ ← Select tactics
├─────────────────────────────────────────────┤
│ Tactics (procedural execution guides)       │ ← Execute work
├─────────────────────────────────────────────┤
│ Templates (output structure contracts)      │ ← Lowest precedence
└─────────────────────────────────────────────┘
```

**Key references:**
- Full doctrine stack documentation: `DOCTRINE_STACK.md`
- Tactics catalog: `tactics/README.md`
- Extended directives: `directives/`
- Shorthand commands: `shorthands/README.md`

**Tactics usage:** Directives explicitly invoke tactics at workflow steps. Agents may also discover and propose tactics from the catalog.

**Shorthands usage:** Quick-access commands for common workflows (e.g., `/architect-adr`, `/afk-mode`, `/curate-directory`). Load from `shorthands/` directory for task shortcuts.

## Choose the Path First

- **Small-footprint (default for low-risk edits):** load
  `guidelines/runtime_sheet.md` + the relevant specialist profile. Pull extra directives only when needed.
- **Full governance pack (high-stakes):** append general + operational guidelines, risk/escalation directives, and the specialist profile.
- Use `ops/scripts/assemble-agent-context.sh --agent <profile> --mode minimal|full` to emit the needed bundle instead of manual copy/paste.

## Load Local Doctrine Overrides (After Core Stack)

After loading the core doctrine stack from `doctrine/`, agents should load repository-local overrides from `.doctrine-config/` when present.

- Expected local guideline file: `.doctrine-config/specific_guidelines.md`
- Additional optional local extensions:
  - `.doctrine-config/custom-agents/`
  - `.doctrine-config/approaches/`
  - `.doctrine-config/directives/` (or local instruction files)
  - `.doctrine-config/tactics/`
- Local overrides may tweak, enhance, or extend execution behavior.
- Local overrides MUST NOT override `doctrine/guidelines/general_guidelines.md` or `doctrine/guidelines/operational_guidelines.md`.

## Core Steps (applies to both modes)

1. Read the task and the minimal required references (see runtime sheet links). Avoid front-loading the entire repo.
2. Load `.doctrine-config/` overrides after core doctrine loading, if present, and validate non-conflict with General/Operational guidelines.
3. Create or update a progress log in `work/`:
    - Date, task understanding, next 2–3 steps.
    - Aliases you expect to use (e.g. `/analysis-mode`, `/summarize-notes`, `/validate-alignment`).
4. Perform the first small step:
    - Prefer analysis or planning over large code changes.
    - Use relevant mode aliases before reasoning; keep scratch in `work/`.
5. Stop after a coherent unit of work and summarise:
    - What you did and recommend next.
    - Which aliases were invoked and any alignment or risk flags (❗️ / ⚠️ / ✅).
