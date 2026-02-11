# Changelog - SDD Agentic Framework Repository

All notable changes to this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Note:** Framework doctrine updates are documented separately in [`doctrine/CHANGELOG.md`](doctrine/CHANGELOG.md).

---

## [Unreleased]

### Added - Agent-Friendly Error Reporting System (2025-02-11)

**Implemented by:** DevOps Danny

#### Added
- **Error Aggregation Infrastructure**
  - `tools/scripts/generate-error-summary.py` - Python script for structured error reporting
  - `tools/scripts/generate-error-summary.sh` - Shell wrapper with GitHub Actions integration
  - Structured error data model with location tracking, severity levels, and fix suggestions
  - JSON output for programmatic agent access
  - Markdown output for human-readable summaries
  - GitHub Actions annotations for inline PR feedback

- **Reusable GitHub Action**
  - `.github/actions/error-summary/action.yml` - Composite action for easy workflow integration
  - Automatic artifact upload with configurable retention
  - Output variables for downstream workflow steps
  - Integrated step summary generation

- **Enhanced Validation Workflow**
  - `.github/workflows/validation-enhanced.yml` - Demonstration workflow with full error reporting
  - Multi-validator integration (structure, schema, naming, E2E tests)
  - Automated PR comments with structured error reports
  - Agent-friendly instructions and artifact links

- **Comprehensive Documentation**
  - `docs/error-reporting-system.md` - Complete system documentation (522 lines)
  - `docs/error-reporting-quick-reference.md` - Quick start guide (365 lines)
  - `docs/IMPLEMENTATION_ERROR_REPORTING.md` - Implementation summary
  - Updated `tools/scripts/README.md` with error reporting section

- **Examples & Testing**
  - `examples/error-reports/` - Example JSON and Markdown error reports
  - `tests/test_error_reporting_integration.sh` - Integration test suite (7/7 passing)
  - Sample error scenarios for agent training

#### Benefits
- **For Agents:** Machine-readable JSON with precise locations and actionable suggestions
- **For Humans:** Clear Markdown summaries, inline annotations, and PR comments
- **For Repository:** Reproducible error reporting, improved CI/CD reliability

#### Alignment
- Follows Directive 001 (CLI & Shell Tooling), Directive 018 (Documentation Framework)
- Implements test-first approach per Directive 028 (Bug Fixing Techniques)
- Aligned with ADR-011 (Primer Execution Matrix) and ADR-028

---

### Major Refactoring - Code Artifact Consolidation (2026-02-08)

#### Changed
- **BREAKING:** Reorganized entire codebase into four clear directories:
  - `src/` - Production code (framework runtime, services)
  - `tools/` - Development utilities (exporters, validators, scripts, release automation)
  - `tests/` - All test code (framework, orchestration, integration)
  - `fixtures/` - Test data and example files
- **Eliminated directories:** `ops/`, `validation/`, `examples/`
- **146 files relocated** across new structure
- Updated all import paths in Python, JavaScript, and shell scripts
- Updated configuration: `package.json` (28 scripts), `pyproject.toml` (test paths, mutation config)

#### Added
- `src/README.md` - Production code guidelines and principles
- `tools/README.md` - Development utilities documentation
- Clear separation between production code and development tooling
- Comprehensive refactoring completion report in session artifacts

#### Details
Production code moved to `src/framework/`:
- `orchestration/` ← `ops/orchestration/` (runtime agent dispatch)
- `context/` ← `ops/framework-core/` (context assembly, directive loading)
- `config/` ← `ops/config/` (model routing configuration)
- `schemas/` ← `validation/schemas/` (production JSON schemas)

Development tooling moved to `tools/`:
- `exporters/` ← `ops/exporters/` (Copilot/Claude/OpenCode exporters)
- `validators/` ← `ops/validation/` + `validation/validate_*` (CI validation)
- `scripts/` ← `ops/scripts/` (utilities, planning automation)
- `dashboards/` ← `ops/dashboards/` (development dashboards)
- `release/` ← `ops/release/` (release automation)

Tests consolidated to `tests/`:
- `framework/` ← `validation/framework/`
- `orchestration/` ← `validation/test_orchestration*.py`
- `maintenance/` ← `validation/maintenance/`
- `integration/exporters/` ← `validation/agent_exports/`

Fixtures consolidated to `fixtures/`:
- `prompts/` ← `examples/prompts/` (ADR-023 test fixtures)
- `copilot/`, `opencode/`, `ir/`, `schemas/` ← `validation/fixtures/`
- `agents/` ← `validation/fixtures/agents/`

**Commits:** 0a1e15c, 268a41d, f78349a, 750df53, 0774676

---

### Doctrine Migration - Phase 1 Complete (2026-02-08)

See [`doctrine/CHANGELOG.md`](doctrine/CHANGELOG.md) for full details.

**Summary:**
- Extracted SDD Agentic Framework from `.github/agents/` to standalone `doctrine/` directory
- 201 files migrated with zero external dependencies
- All paths parameterized for portability (`${WORKSPACE_ROOT}`, `${DOC_ROOT}`, etc.)
- Framework ready for distribution via git subtree

**Key Changes:**
- Created `docs/architecture/design/DOCTRINE_MAP.md` - Complete framework navigation guide (moved from doctrine/)
- Moved templates to canonical location: `doctrine/templates/`
- Updated all 20 agent profiles to reference `doctrine/` paths
- Bootstrap Bill configured to create `.doctrine/config.yaml` during repo setup
- Removed deprecated `agents` symlink (pointed to old `.github/agents/`)

**Commits:** 22b17ee + 26 prior commits in Phase 1

---

## Template History

This repository was created from the SDD Agentic Framework template. For template-specific changes, see the upstream template repository.

---

## Versioning Notes

- **Repository version:** Tracks changes to this specific repository instance
- **Doctrine version:** Tracked separately in `doctrine/CHANGELOG.md`
- **Template version:** Inherited from `sddevelopment-be/templates`

Version numbering follows SemVer:
- **Major:** Breaking changes to API or structure
- **Minor:** New features, backward-compatible changes
- **Patch:** Bug fixes, documentation updates
