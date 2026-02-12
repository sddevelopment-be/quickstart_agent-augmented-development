---
id: "SPEC-REFACTOR-001"
title: "Refactoring Techniques and Pattern-Informed Tactics Initiative"
status: "draft"
initiative: "Refactoring Techniques"
priority: "HIGH"
epic: "Doctrine Quality and Maintainability Uplift"
target_personas: ["agentic-framework-core-team", "software_engineer", "automation_agent"]
features:
  - id: "FEAT-REFACTOR-001-01"
    title: "Research-backed refactoring techniques corpus"
    status: "draft"
    description: "Curate refactoring and pattern references into actionable evidence matrix"
  - id: "FEAT-REFACTOR-001-02"
    title: "Doctrine refactoring tactics authoring"
    status: "draft"
    description: "Create procedural tactics from selected techniques using tactic template"
  - id: "FEAT-REFACTOR-001-03"
    title: "Directive and discovery integration"
    status: "draft"
    description: "Link tactics in refactoring directives and tactics index for agent discoverability"
  - id: "FEAT-REFACTOR-001-04"
    title: "Pattern reference enrichment"
    status: "draft"
    description: "Add pattern-oriented references under doctrine/docs/references for strategy-level context"
created: "2026-02-12"
updated: "2026-02-12"
author: "analyst-annie"
---

# Initiative Specification: Refactoring Techniques and Pattern-Informed Tactics

**Status:** Draft
**Created:** 2026-02-12
**Last Updated:** 2026-02-12
**Author:** Analyst Annie
**Stakeholders:** Curator Claire, Researcher Ralph, Planning Petra, Manager Mike, Code Reviewer Cindy

## Executive Summary

This initiative converts preferred refactoring approaches into repeatable doctrine tactics so agents produce code that is more maintainable, explicit, and domain-aligned. It uses an evidence-first flow: research and compare techniques, codify selected ones as tactics, wire them into directives, and validate discoverability and compliance.

The source list in `work/tasks/learning_refactoring_plan.md` anchors the initiative to canonical references across low-level refactorings, refactor-to-pattern moves, and architecture-level pattern targets.

## Problem Statement

Current doctrine coverage includes isolated refactoring guidance but lacks a structured, extensible catalog aligned with preferred refactoring moves. This causes inconsistent implementation behavior across agents and increases review overhead.

## User Story

**As a** framework maintainer and multi-agent orchestrator
**I want** preferred refactoring approaches codified as reusable doctrine tactics
**So that** generated code consistently reflects maintainability and design preferences.

## Target Personas

- `docs/audience/agentic-framework-core-team.md` (Primary)
- `docs/audience/software_engineer.md` (Secondary)
- `docs/audience/automation_agent.md` (Secondary)

## Requirements (MoSCoW)

### MUST

- FEAT-REFACTOR-001-01: Research matrix exists in `work/research/` with technique applicability, risks, and failure modes.
- FEAT-REFACTOR-001-02: Selected techniques are encoded as tactics in `doctrine/tactics/` using `doctrine/templates/tactic.md`.
- FEAT-REFACTOR-001-03: Refactoring directives reference tactics (constraints in directives, procedures in tactics).
- FEAT-REFACTOR-001-03: `doctrine/tactics/README.md` includes the new tactics for discovery.

### SHOULD

- FEAT-REFACTOR-001-04: Pattern-level supporting references are added in `doctrine/docs/references/`.
- Work logs capture rationale and traceability for selection decisions.

### COULD

- Introduce taxonomy tags for tactic clustering (e.g., composition, conditionals, object movement).
- Add anti-pattern mapping for tactic selection heuristics.

### WON'T (This Iteration)

- Full ingestion of all listed external techniques into tactics in one batch.
- Automatic tactic generation from source URLs.

## Scenarios

### Scenario 1: Technique-to-Tactic Conversion

Given a curated research matrix, when Curator Claire selects high-fit techniques, then tactic files are created with deterministic execution steps and explicit exit criteria.

### Scenario 2: Directive Integration

Given new tactic files, when directive references are updated, then agents can load constraints via directives and execute procedures via tactics without duplicative policy text.

### Scenario 3: Validation and Assignment

Given created work items, when Manager Mike assigns them, then all tasks appear in `work/collaboration/assigned/<agent>/` with correct status and dependencies.

## Constraints

- Respect doctrine stack precedence.
- Local `.doctrine-config` extensions may enhance behavior but cannot override General or Operational guidelines.
- Tactic references must remain localized to stable doctrine paths.

## Deliverables

- Initiative spec (this document)
- Planning updates in `docs/planning/`
- Assigned orchestration work items for researcher/curator/reviewer
- Work logs and prompt documentation per directives 014/015

## Open Questions

- Which subset of techniques should be in first release (breadth vs depth)?
- Should pattern references be grouped by design goal or source taxonomy?
- Should reviewer policy enforce tactic usage for refactor-heavy changes?

## Related Documentation

- `work/tasks/learning_refactoring_plan.md`
- `doctrine/tactics/refactoring-strangler-fig.tactic.md`
- `doctrine/templates/tactic.md`
- `docs/planning/AGENT_TASKS.md`
