# Tactic: Change.ApplySmallestViableDiff

**Invoked by:**
- Directive 021 (Locality of Change) — core principle for surgical modifications

**Related tactics:**
- `stopping-conditions.tactic.md` — defines when to stop making changes
- `code-review-incremental.tactic.md` — reviews changes using minimal diff principle

**Complements:**
- Directive 024 (Self-Observation Protocol) — prevents gold-plating and scope creep

---

## Intent
Introduce changes using the smallest possible modification that achieves the stated goal, minimizing unintended side effects.

Use this tactic to make surgical, reviewable changes without introducing unnecessary complexity or risk.

---

## Preconditions

**Required inputs:**
- A concrete change goal has been defined
- Existing code or artifacts are available
- Tests or validation mechanisms exist (or can be created)

**Assumed context:**
- The goal is to modify existing work, not create new functionality from scratch
- Refactoring or rewriting is not the primary intent
- Reviewability and maintainability matter

**Exclusions (when NOT to use):**
- When technical debt makes small changes impossible (consider strangler-fig pattern)
- When the goal explicitly requires architectural changes
- When opportunistic improvements are explicitly requested

---

## Execution Steps

1. Identify the minimal set of files that must change to achieve the goal.
2. Identify the minimal change required within each file.
3. Apply the change without altering unrelated formatting, imports, or structure.
4. Verify the change achieves the stated goal.
5. Stop after the goal is met; do not continue improving.

---

## Checks / Exit Criteria
- The change achieves the stated goal.
- No unrelated files or sections were modified.
- The diff is reviewable without additional explanation.
- Tests pass (or validation succeeds).

---

## Failure Modes
- Expanding scope beyond the stated goal ("while I'm here" syndrome).
- Opportunistic refactoring without explicit approval.
- Mixing functional change with stylistic cleanup.
- Touching files "just to be consistent".

---

## Outputs
- Minimal code or artifact diff
- Verification that goal is met

---

## Notes on Use

This tactic directly implements the **Locality of Change** principle from Directive 021.

Gold-plating indicators:
- Changing formatting in unrelated sections
- Renaming variables beyond the change scope
- Adding "nice to have" improvements
- Reorganizing structure unnecessarily

When in doubt: **Stop and confirm** before expanding scope.

---
