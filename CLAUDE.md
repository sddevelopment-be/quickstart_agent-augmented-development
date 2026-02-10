<!-- Generated from doctrine/ — do not edit manually -->
# Project Instructions

## Purpose

This repository serves as a **quickstart template and reference implementation** for agent-augmented development workflows, providing a structured, portable, and maintainable foundation for teams integrating AI agents into their software development processes.

## Repository Structure

- `doctrine/` in consuming repositories — Agent profiles, directives, approaches, guidelines
- `work/` — Orchestration workspace (see work/README.md for structure)
- `docs/` — Documentation (templates, architecture, HOW_TO_USE guides)
- `validation/` — Validation scripts and test artifacts
- `ops/` — Operational scripts and utilities

## Coding Conventions

- Line length (88 characters default)
- Consistent spacing around operators
- String quote normalization (prefer double quotes)
- Trailing commas in multi-line structures
- Blank line management
- Unused imports
- Undefined variables
- Code quality issues

## Common Commands

```bash
python -m pytest                    # Run all tests
python -m pytest tests/unit/        # Run unit tests
npm run deploy:claude               # Deploy Claude Code artifacts
npm run export:all                  # Export all distributions
npm test                            # Run JS tests
```

## Further Reference

- `doctrine/` — Full governance stack (guidelines, directives, approaches)
- `.claude/rules/` — Auto-loaded coding and collaboration rules
- `.claude/agents/` — Specialist agent definitions
- `.claude/skills/` — On-demand skill prompts
- `docs/` — Architecture decisions, templates, vision
