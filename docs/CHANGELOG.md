# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

> Scope / plan for upcoming release

### Added

- Modular agent directive system with 13 core directives (001-013)
- Comprehensive agent profiles for specialized roles (architect, curator, developer, writer, etc.)
- Directive manifest with enhanced metadata (directive_version, status fields)
- Validation tooling (`validation/validate_directives.sh`) for directive integrity checks
- Agent bootstrapping and rehydration protocols
- Command aliases system for efficient agent interaction
- Issue templates for epics, features, tasks, bugs, and agent creation
- Work collaboration space structure (`work/collaboration/`, `work/curator/`)
- Documentation templates for architecture (ADR, design vision, technical design, roadmap)
- Documentation templates for structure mapping (REPO_MAP, SURFACES, WORKFLOWS, CONTEXT_LINKS)
- LEX (Lexical Excellence) templates for style consistency
- OpenCode configuration mapping and validation scripts
- Portability enhancement documentation
- Audience documentation for automation agents (`docs/audience/automation_agent.md`)
- Architecture documentation directory (`docs/architecture/`)
  - ADR-001: Modular Agent Directive System
  - ADR-001: Portability Enhancement – OpenCode Specification (standardized agent configuration using OpenCode JSON for portability, validation, and CI/CD)
  - Architectural Vision document
  - Agent Specialization Patterns guide
  - Directive System Architecture technical documentation
  - Architecture README with navigation and guidelines
- Directive 013: Tooling Setup & Fallbacks (install commands, version requirements, fallback strategies)
- Redundancy rationale documentation in directive 012
- Meta-version tracking in `AGENTS.md` (core_version, directive_set_version)
- Work inbox task index (`work/inbox/INDEX.md`) tracking 10 open orchestration tasks
- Manager agent work logs directory (`work/logs/manager/`)
- Orchestration coordination tasks:
  - Synthesizer done-work assessment task for efficiency analysis
  - Architect synthesizer assessment review task for solution fitness evaluation
  - Architect follow-up task lookup pattern assessment
  - Build-automation CI/CD integration tasks (orchestration, validation, diagram workflows)
- Manager Mike inbox review and coordination log (`work/logs/manager/2025-11-23T1845-inbox-review-coordination.md`)
3-- GitHub Issue Automation with 3-tier architecture (`ops/scripts/planning/github-helpers/`) enabling easy issue tracker swapping.
- ADR-011 formalizing the Solutioning Primer → command alias mapping plus curator/architect review workflow.
- ADR-012 establishing ATDD + TDD as the default coding approach (with throw-away script exceptions).
- Directives 016 (ATDD) and 017 (TDD) describing acceptance-test-first and red/green/refactor cadences.
- Architecture synthesis notes for primer references, gold plating, batch scripting, test boundaries, and fail-fast alignment.

### Changed

- Refactored `AGENTS.md` to lean core specification (12 sections) with external directive references
- Externalized detailed operational guidance into modular directives
- Improved token efficiency through lazy directive loading
- Enhanced agent initialization protocol with validation checkpoints
- Standardized integrity markers (✅ ⚠️ ❗️) across all agent communications
- Updated `work/collaboration/AGENT_STATUS.md` with 4-phase execution plan and dependency graph
- Split CI/CD integration task (1744) into 3 parallel subtasks for orchestration, validation, and diagram workflows
- Orchestration workflow no longer auto-runs on `main`; manual dispatch is required to respect branch protection rules (added `if: github.ref != 'refs/heads/main'`).
- Consolidated duplicate root changelog entries into `docs/CHANGELOG.md` to keep one canonical history source.
- Agents/aliases and directives (010/011/014/015) now codify primer execution matrices per ADR-011, and all specialist profiles reference both the primer requirements and directives 016/017.
- Specialist agent definitions now include test-first requirements and links back to directives 016/017 for any executable work.
- Simplified `agents/aliases.md` back to a command-shorthand catalogue; all primer/test-driven guidance now lives exclusively inside directives 010, 016, and 017.

### Removed

> Deprecated features and functionalities

### Fixed

- Task naming validation script now accepts orchestrator-generated follow-up filenames with embedded timestamps, eliminating false positives and keeping all 39 task files valid.

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
- POC3 Metrics Synthesis (`docs/architecture/synthesis/poc3-orchestration-metrics-synthesis.md`) with comprehensive ADR-009 validation, accessibility audit, and cross-artifact traceability.
- Architecture assessment reports (`docs/architecture/assessments/implementation-progress-review.md`, `docs/architecture/recommendations/architecture-alignment-report.md`) capturing ADR-by-ADR scoring and recommendations.
- Repository mapping suite (`REPO_MAP.md`, `docs/SURFACES.md`, `docs/WORKFLOWS.md`, `docs/DEPENDENCIES.md`) totaling 73KB of structure documentation.
- Work log analysis synthesis (`work/synthesizer/worklog-analysis-synthesis.md`) covering 41 work logs, 23 improvements, and a 4-phase roadmap.
- Iteration 3 executive summary (`work/collaboration/ITERATION_3_SUMMARY.md`) with consolidated metrics and recommendations.

### Changed
- `work/collaboration/AGENT_STATUS.md` updated to reflect active agents and assignments for the iteration.

### Fixed
- Directive 003 replaced Hugo assumptions with the actual repo structure and added version metadata.
- Directive 007 removed a stale §18 reference, clarified requirements, and added version metadata.
- Directive review audit (`work/logs/curator/2025-11-23T2246-directives-approaches-review-report.md`) resolved the remaining medium/high findings.
- Removed five duplicate task files to keep orchestration tracking accurate.

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
