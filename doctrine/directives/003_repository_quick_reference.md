<!-- The following information is to be interpreted literally -->

# 003 Repository Quick Reference Directive

Key Directories:

- `.github/agents/` — Agent profiles, directives, approaches, guidelines
- `work/` — Orchestration workspace (see work/README.md for structure)
    - `work/collaboration/` — Task orchestration (inbox, new, assigned, in_progress, done, archive)
    - `work/reports/` — Agent outputs (logs, metrics, benchmarks)
        - `work/reports/logs/<agent-name>/` — Work logs per Directive 014
    - `work/external_memory/` — Inter-agent context sharing
    - `work/notes/` — Temporary notes and ideation
    - `work/articles/` — Public-facing articles and documentation experiments
- `docs/` — Documentation (templates, architecture, HOW_TO_USE guides)
    - `docs/templates/LEX/` — Lexical guidelines and terminology
    - `docs/templates/structure/` — Structural templates and patterns
    - `docs/architecture/adrs/` — Architecture Decision Records
- `validation/` — Validation scripts and test artifacts
- `ops/` — Operational scripts and utilities
    - `ops/framework-core/` — Core framework utilities
    - `ops/orchestration/` — Orchestration and agent utilities
- Generated (do not edit): `.git/`, `__pycache__/`, `.pytest_cache/`
- Templates: `docs/templates/`, org-wide: `sddevelopment-be/templates/` (requires access / local clone)

Dependencies: `requirements.txt` (Python packages)

## Standard Path Conventions

**Task Orchestration:**
- Task files: `work/collaboration/<state>/<agent-name>/<task-id>.yaml`
  - States: `inbox`, `new`, `assigned`, `in_progress`, `done`, `archive`
  - Agent subdirectories required for: `assigned`, `in_progress`, `done`
  - Example: `work/collaboration/done/architect/2025-11-30T1200-task.yaml`

**Work Logs (Directive 014):**
- Format: `work/reports/logs/<agent-name>/YYYY-MM-DDTHHMM-<description>.md`
- Example: `work/reports/logs/curator/2025-11-23T0811-orchestration-guide.md`

**Architecture Decision Records:**
- Format: `docs/architecture/adrs/ADR-NNN-<title>.md`
- Example: `docs/architecture/adrs/ADR-015-follow-up-task-lookup-pattern.md`

**Issue Templates:**
- Location: `.github/ISSUE_TEMPLATE/`
- Format: `<type>-<name>.md` or `<number>-<name>.yml`

**Scripts:**
- Core utilities: `ops/framework-core/`
- Orchestration: `ops/orchestration/`
- Validation: `validation/`

---

_Version: 1.1.0_  
_Last Updated: 2025-11-30_

