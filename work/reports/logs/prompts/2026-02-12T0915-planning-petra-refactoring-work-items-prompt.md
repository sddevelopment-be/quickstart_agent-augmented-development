# Original Prompt Documentation: Refactoring Planning and Work Item Creation

**Task ID:** n/a
**Agent:** planning-petra
**Date Executed:** 2026-02-12T09:15:00Z
**Documentation Date:** 2026-02-12T09:15:00Z

---

## Original Problem Statement

> "...as Petra: add it to the roadmap/planning artefacts in the `docs` directory and create the required work items..."

---

## SWOT Analysis

### Strengths

- Role responsibility is explicit.
- Required output categories are clear (planning artifacts + work items).

### Weaknesses

- No exact file list provided for planning artifacts.
- "Required work items" lacks quantity and explicit scope boundaries.

### Opportunities

- Standardize planning updates to `FEATURES_OVERVIEW.md`, `NEXT_BATCH.md`, `AGENT_TASKS.md`.
- Define default minimum work-item bundle for initiative kickoff.

### Threats

- Inconsistent planning updates across runs.
- Drift in task granularity from different planners.

---

## Suggested Improvements

### Version 2.0: Enhanced Prompt Segment

```text
As Petra, update exactly:
1) docs/planning/FEATURES_OVERVIEW.md
2) docs/planning/NEXT_BATCH.md
3) docs/planning/AGENT_TASKS.md

Then create 5 task files in work/collaboration/inbox with IDs and dependencies:
- researcher matrix
- curator tactics
- curator references
- curator directive integration
- reviewer validation
```

---

## Pattern Recognition

### Effective Prompt Elements

1. Role segmentation enables clean phase commits.
2. Directive references increase quality controls.

### Anti-Patterns to Avoid

1. Ambiguous artifact scope in planning updates.
2. Missing explicit dependency chain for new tasks.

---

**Documented by:** planning-petra
**Date:** 2026-02-12T09:15:00Z
**Purpose:** Improve repeatability of planning prompts
