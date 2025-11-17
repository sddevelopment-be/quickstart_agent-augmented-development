# Bootstrap Instructions

_Version: 1.0.0_  
_Last updated: 2025-11-17_
_Format: Markdown protocol for agent initialization and governance_

---

How an agent should start when it has no prior context.

1. Read:
   - `docs/VISION.md`
   - `docs/specific_guidelines.md`
   - `.github/agents/guidelines/general_guidelines.md`
   - `.github/agents/guidelines/operational_guidelines.md`
   - `.github/agents/aliases.md` (command shortcuts & mode discipline)
   - Your own specialist file (`.github/agents/*.agent.md`) if you are acting as a specialist agent.
   - Initialize, according to your agent profile.

2. Create or update a progress log in `work/`:
   - Note the current date.
   - Summarise your understanding of the task.
   - List your next 2–3 steps.
   - Indicate which aliases you expect to use (e.g. `/analysis-mode`, `/summarize-notes`, `/validate-alignment`).

3. Perform the first small step:
   - Prefer analysis or planning over large code changes.
   - Use relevant mode aliases (e.g. `/analysis-mode`) before reasoning.
   - Write any non-final output to `work/`.

4. Stop after a coherent unit of work and summarise:
   - What you did.
   - What you recommend next.
   - Which aliases were invoked and any alignment or risk flags (❗️ / ⚠️ / ✅).
