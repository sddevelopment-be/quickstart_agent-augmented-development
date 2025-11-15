# Operational Guidelines

How agents should operate inside this repository.

## Files and directories

# Agent Guidelines

- Treat `docs/` as the **source of truth** about intent and constraints.
- Use `work/` for:
  - scratch notes
  - progress logs
  - intermediate drafts
- Use `output/` for:
  - generated artifacts ready for human review
- Prefer small, incremental changes over large rewrites.

## Rules

- Do not modify files under `docs/` unless explicitly instructed.
- Prefer creating new files in `work/` or `output/` over rewriting existing ones without context.
- Keep output structured and easy to diff.
