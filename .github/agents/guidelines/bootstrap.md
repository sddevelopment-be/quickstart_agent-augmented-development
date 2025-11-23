# Bootstrap Instructions

_Version: 1.1.0_
_Last updated: 2025-11-23_
_Format: Markdown protocol for agent initialization and governance_

---

How an agent should start when it has no prior context.

## Choose the Path First
- **Small-footprint (default for low-risk edits):** load `guidelines/runtime_sheet.md` + the relevant specialist profile. Pull extra directives only when needed.
- **Full governance pack (high-stakes):** append general + operational guidelines, risk/escalation directives, and the specialist profile.
- Use `ops/scripts/assemble-agent-context.sh --agent <profile> --mode minimal|full` to emit the needed bundle instead of manual copy/paste.

## Core Steps (applies to both modes)
1. Read the task and the minimal required references (see runtime sheet links). Avoid front-loading the entire repo.
2. Create or update a progress log in `work/`:
   - Date, task understanding, next 2–3 steps.
   - Aliases you expect to use (e.g. `/analysis-mode`, `/summarize-notes`, `/validate-alignment`).
3. Perform the first small step:
   - Prefer analysis or planning over large code changes.
   - Use relevant mode aliases before reasoning; keep scratch in `work/`.
4. Stop after a coherent unit of work and summarise:
   - What you did and recommend next.
   - Which aliases were invoked and any alignment or risk flags (❗️ / ⚠️ / ✅).
