# Operational Guidelines

_Version: 1.3.0_
_Last updated: 2025-11-23_
_Format: Markdown protocol for agent initialization and governance_

---

How agents should operate inside this repository.

> For low-risk tasks, prefer the lightweight context from
`guidelines/runtime_sheet.md` + your specialist profile. Use the full contents below when operating in high-stakes or cross-cutting areas.

## Files and directories

- Treat `docs/` as the **source of truth** about intent and constraints.
- Use `work/` for:
    - scratch notes
    - progress logs
    - intermediate drafts
- Use `output/` for:
    - generated artifacts ready for human review
- Prefer small, incremental changes over large rewrites.

### Repository Structure Note

**Important:** The `agents/` directory is a symlink to `.github/agents/`. Any changes made to files or directories under
`agents/` will actually modify `.github/agents/` and vice versa. This means:

- `agents/directives/` → `.github/agents/directives/` (same location)
- `agents/approaches/` → `.github/agents/approaches/` (same location)
- There is only ONE copy of each file, not duplicates
- Edits to either path modify the same underlying file

## Rules

- Do not modify files under `docs/` unless explicitly instructed.
- Prefer creating new files in `work/` or `output/` over rewriting existing ones without context.
- Keep output structured and easy to diff.
- Always reference relevant guidelines before executing tasks.
- When in doubt, ask for clarification rather than making assumptions.
- If you are a specialist agent: NEVER exceed your specific role's scope.

## Token Discipline

- Prefer links and section references over inlining entire guidelines in the prompt.
- Drop non-essential sections when the task scope is narrow.
- Keep transient reasoning in `${WORKSPACE_ROOT}/notes` instead of the prompt transcript.

## Style Guidelines

- Reuse existing templates and patterns (`templates/`) whenever possible.
- Adhere to the writing guidelines in the `${DOC_ROOT}/styleguide/` directory.
- Use clear, concise language. Maintain a calm and professional tone.
- Follow existing style conventions in code and documentation.
- Content over Hype: Avoid buzzwords and jargon unless necessary.
