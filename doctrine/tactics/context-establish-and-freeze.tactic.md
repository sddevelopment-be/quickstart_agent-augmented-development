# Tactic: Context.EstablishAndFreeze

**Invoked by:**
- [Directive 023 (Clarification Before Execution)](../directives/023_clarification_before_execution.md) — requires explicit context establishment

**Related tactics:**
- `stopping-conditions.tactic.md` — defines when frozen context is satisfied
- `premortem-risk-identification.tactic.md` — uses established context for risk assessment

**Complements:**
- Approach: Decision-First Development — explicit context prevents scope drift

---

## Intent
Establish a shared, explicit understanding of context and constraints before any substantive work begins, and freeze that context for the duration of the task.

Use this tactic to prevent scope creep, misalignment, and wasted effort due to implicit assumptions.

---

## Preconditions

**Required inputs:**
- A task or problem statement has been provided
- The task has non-trivial scope or constraints
- Authority to ask clarifying questions exists

**Assumed context:**
- No work has yet been performed on the task
- Stakeholders are available for clarification
- Explicit alignment is valued over speed

**Exclusions (when NOT to use):**
- Trivial, well-understood tasks (&lt;5 minutes, obvious scope)
- Exploratory work where discovery is the goal
- Time-critical emergencies requiring immediate action

---

## Execution Steps

1. Restate the task in one clear sentence.
2. List explicit **goals** the task is expected to achieve.
3. List explicit **non-goals** and exclusions (what is deliberately out of scope).
4. Identify known **constraints** (technical, organizational, temporal, resource).
5. List **assumptions** being made due to missing information.
6. Ask for confirmation or correction of the above.
7. Freeze the confirmed context and do not revise it during execution without explicit acknowledgment.

---

## Checks / Exit Criteria
- Goals and non-goals are explicitly written.
- Constraints and assumptions are listed.
- Context has been confirmed by stakeholder or explicitly accepted as-is.
- Frozen context is documented for reference during execution.

---

## Failure Modes
- Proceeding with implicit or assumed goals.
- Revising assumptions mid-task without acknowledgment.
- Treating clarification as optional or wasteful.
- Allowing scope drift without re-freezing context.

---

## Outputs
- Written context summary
- Explicit list of assumptions and constraints
- Confirmed goals and non-goals

---

## Notes on Use

This tactic is **front-loaded**: it requires effort before execution begins, but prevents costly rework and misalignment.

If context shifts during execution:
1. Pause work
2. Document the shift
3. Re-establish and re-freeze context
4. Resume with new agreement

Context drift is not failure—**unacknowledged** context drift is.

---
