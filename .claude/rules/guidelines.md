<!-- Source: general_guidelines.md, operational_guidelines.md -->
# Guidelines

These guidelines apply to all agents in this repository.


## Behaviour

- Act as a careful, cooperative assistant.
- Prefer clarity over cleverness.
- Be explicit about assumptions.
- Keep changes small and reviewable.

## Communication

- Explain what you’re doing and why when it matters.
- Use clear, concise language.
- When something is ambiguous, propose options and trade-offs.

## Collaboration

- Respect repo-specific rules from `${DOC_ROOT}/specific_guidelines.md`.
- When you create or modify files, summarise the change in a short note.
- Use `work/` for intermediate notes and coordination.





How agents should operate inside this repository.


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

**Important:** The `agents/` directory is a symlink to `doctrine/` in consuming repositories. Any changes made to files or directories under
`agents/` will actually modify `doctrine/` in consuming repositories and vice versa. This means:

- `agents/directives/` → `directives/` (same location)
- `agents/approaches/` → `approaches/` (same location)
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
