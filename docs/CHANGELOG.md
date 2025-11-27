# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

> Scope / plan for upcoming release

### Added

- Modular agent directive system with 13 core directives (001-013)
- Agent profiles for specialized roles (architect, curator, developer, writer)
- Directive manifest with enhanced metadata (directive_version, status)
- Directive validation tooling (`validation/validate_directives.sh`)
- Agent bootstrapping and rehydration protocols
- Command aliases for efficient agent interaction
- Issue templates (epics, features, tasks, bugs, agent creation)
- Work collaboration space (`work/collaboration/`, `work/curator/`)
- Architecture documentation templates (ADR, design vision, technical design, roadmap)
- Structure mapping templates (REPO_MAP, SURFACES, WORKFLOWS, CONTEXT_LINKS)
- LEX templates for style consistency
- OpenCode configuration mapping and validation
- Automation agent audience documentation (`docs/audience/automation_agent.md`)
- Architecture documentation (`docs/architecture/`)
- ADR-001: Modular Agent Directive System
- ADR-001: Portability Enhancement via OpenCode Specification
- Architectural Vision document
- Agent Specialization Patterns guide
- Directive System Architecture documentation
- Architecture README with navigation
- Directive 013: Tooling Setup & Fallbacks
- Redundancy rationale in Directive 012
- Meta-version tracking in `AGENTS.md` (core_version, directive_set_version)
- Work inbox task index (`work/inbox/INDEX.md`) for 10 orchestration tasks
- Manager agent work logs directory (`work/logs/manager/`)
- Orchestration coordination tasks (synthesizer assessments, architect reviews, CI/CD integration)
- Manager Mike coordination log (`work/logs/manager/2025-11-23T1845-inbox-review-coordination.md`)
- 3-tier GitHub issue automation (`ops/scripts/planning/github-helpers/`)
- ADR-011: Solutioning Primer workflow and command alias mapping
- ADR-012: ATDD + TDD as default coding approach
- Directives 016 (ATDD) and 017 (TDD) for test-first development
- Architecture synthesis notes (primers, gold plating, batch scripting, test boundaries)

### Changed

- Refactored `AGENTS.md` to lean core (12 sections) with external directive references
- Externalized operational guidance into modular directives
- Improved token efficiency via lazy directive loading
- Enhanced agent initialization with validation checkpoints
- Standardized integrity markers (✅ ⚠️ ❗️) across agent communications
- Updated `work/collaboration/AGENT_STATUS.md` with 4-phase plan and dependency graph
- Split CI/CD integration task (1744) into 3 parallel subtasks
- Disabled auto-run for orchestration workflow on `main` branch (manual dispatch required)
- Consolidated root changelog entries into `docs/CHANGELOG.md` as single source of truth
- Codified primer execution matrices per ADR-011 in directives (010/011/014/015)
- Added test-first requirements to specialist agent definitions (link to directives 016/017)
- Simplified `agents/aliases.md` to command-shorthand only; moved primer guidance to directives 010, 016, 017

### Removed

> Deprecated features and functionalities

### Fixed

- Task naming validation now accepts orchestrator-generated filenames with embedded timestamps (39 task files validated)

### Security

> Vulnerabilities addressed and security improvements

## [Iteration 3] - 2025-11-23

**Status:** ✅ **PRODUCTION READY** — Framework approved for production deployment

This iteration delivered a production-grade orchestration framework with full architectural validation, health scoring, and documentation coverage across five specialized agents.

**Key Metrics**
- Architectural alignment: 98.9% (267/270 points)
- Framework health score: 92/100 (Excellent)
- Task completion rate: 100% (5/5 tasks)
- Production readiness: Approved

### Added
- POC3 Metrics Synthesis with ADR-009 validation and cross-artifact traceability (`docs/architecture/synthesis/poc3-orchestration-metrics-synthesis.md`)
- Architecture assessment reports with ADR-by-ADR scoring (`docs/architecture/assessments/`, `docs/architecture/recommendations/`)
- Repository mapping suite (73KB): `REPO_MAP.md`, `SURFACES.md`, `WORKFLOWS.md`, `DEPENDENCIES.md`
- Work log analysis synthesis: 41 logs, 23 improvements, 4-phase roadmap (`work/synthesizer/worklog-analysis-synthesis.md`)
- Iteration 3 executive summary with consolidated metrics (`work/collaboration/ITERATION_3_SUMMARY.md`)

### Changed
- `work/collaboration/AGENT_STATUS.md` updated to reflect active agents and assignments for the iteration.

### Fixed
- Directive 003: Replaced Hugo assumptions with actual repo structure; added version metadata
- Directive 007: Removed stale §18 reference; clarified requirements; added version metadata
- Directive review audit resolved remaining medium/high findings (`work/logs/curator/2025-11-23T2246-directives-approaches-review-report.md`)
- Removed 5 duplicate task files for accurate orchestration tracking

### Framework Milestones
- ADR-002, ADR-003, ADR-004, ADR-005, ADR-009 all scored 10/10.
- Performance target exceeded (orchestrator cycles <10s vs <30s goal).
- Observability, maintainability, and security standards met with 95%+ documentation coverage.

**Recommendation:** Deploy to production; future improvements enhance rather than fix.

## Previous Iterations

### [Iteration 2] - 2025-11-22
- Multi-agent orchestration demonstrations
- POC2 execution and validation
- Initial agent coordination patterns

### [Iteration 1] - 2025-11-21
- File-based orchestration framework foundation
- Initial agent profiles and directives
- POC1 single-agent validation
