# Tactic: ATDD.AdversarialAcceptance

**Invoked by:**
- [Directive 016 (ATDD)](../directives/016_acceptance_test_driven_development.md) — acceptance boundary definition with adversarial thinking

**Related tactics:**
- [`adversarial-testing.tactic.md`](./adversarial-testing.tactic.md) — broader ideation pass before ATDD scenarios
- [`test-boundaries-by-responsibility.tactic.md`](./test-boundaries-by-responsibility.tactic.md) — clarifying test scope and responsibility

**Complements:**
- [Directive 016 (ATDD workflow)](../directives/016_acceptance_test_driven_development.md)
- Approach: Test-Driven Development practices

---

## Intent
Strengthen ATDD acceptance criteria by deliberately exploring how a feature, rule, or workflow could fail in real usage, then converting selected failure scenarios into **adversarial acceptance tests**.

This tactic is used to **discover and encode acceptance boundaries** (misuse, edge cases, ambiguity, unsafe defaults), not to replace happy-path acceptance tests.

---

## Preconditions
- A feature/story slice exists with an initial success definition.
- The team has a shared ATDD cadence (three amigos or equivalent).
- The goal is agreement on behavior at the boundaries, not exhaustive testing.
- Psychological safety: critique targets the *behavior contract*, not the author.

---

## Core Principle
Acceptance tests usually describe *when we accept success*.  
Adversarial acceptance tests describe *when we refuse, constrain, or safely degrade*.

The tactic applies the inversion:

> “Assume this feature is rejected in production.  
> What caused that rejection, and what must we assert so it cannot happen silently?”

---

## Output Shape
Adversarial acceptance tests should be expressed in the same style as your ATDD suite (Given/When/Then, examples table, etc.), and should yield one of these outcomes:

- **Explicit rejection** with a clear error message
- **Safe degradation** with observable signaling
- **Constraint enforcement** (prevent invalid state)
- **Ambiguity resolution** (behavior is defined, not guessed)

---

## Execution Steps

### 1) Establish the acceptance baseline
1. Restate the story goal in one sentence.
2. Write (or confirm) 1–3 baseline acceptance examples for the happy path.
3. Identify the primary stakeholder(s) and what “accepted” means for them.

### 2) Generate failure scenarios (adversarial exploration)
4. Switch stance: assume the feature “failed acceptance” after release.
5. Generate failure scenarios by probing these angles:
   - **Misuse**: a reasonable user does the wrong thing
   - **Ambiguity**: inputs that can be interpreted in multiple ways
   - **Boundaries**: empty, max, extreme, malformed, unexpected combinations
   - **State**: partial state, missing prerequisites, wrong ordering
   - **Concurrency / timing**: repeated actions, race-ish sequences, retries
   - **Integration**: upstream sends weird data, downstream rejects output
   - **Human/org**: policy, governance, roles, permissions, approvals
6. Capture each scenario as:
   - *Trigger* (what happens)
   - *Manifestation* (what the user/system observes)
   - *Likely cause* (why it happens)

### 3) Triage: decide which failures become adversarial acceptance tests
7. For each scenario, decide the intended contract outcome:
   - **Prevent** (block it)
   - **Reject** (explicit error)
   - **Degrade** (continue safely with warning/flag)
   - **Tolerate** (allowed; document why)
8. Select candidates for adversarial acceptance tests using these criteria:
   - High business risk if wrong
   - Likely to occur in real use
   - Would be expensive to detect late
   - Would create silent corruption or confusing behavior

### 4) Convert to ATDD scenarios (contract-first)
9. Convert each selected scenario into an acceptance test using:
   - *Given* (context/state)
   - *And* (relevant preconditions)
   - *When* (the adversarial action/input)
   - *Then* (explicit outcome + observable signal)
10. Ensure each test asserts at least one of:
   - error message / code
   - state remains unchanged
   - rejected command is not applied
   - audit/log/metric signal exists (if relevant)
   - user guidance is provided (next step)

### 5) Review for fit and redundancy
11. Check that adversarial tests:
   - do not duplicate unit tests
   - remain stakeholder-meaningful (business-facing)
   - define boundaries clearly (no vague “should handle” language)
12. Stop.

---

## Checks / Exit Criteria
- At least one adversarial scenario was considered for each major input or workflow step.
- Selected adversarial tests assert explicit outcomes and signals.
- Each adversarial test maps to an agreed contract decision:
  prevent / reject / degrade / tolerate.
- Happy path tests remain intact and readable.

---

## Failure Modes
- Converting every edge case into ATDD (suite becomes brittle and slow).
- Writing adversarial tests in adversarial language instead of contract language.
- Creating tests that require internal implementation detail to pass.
- Mixing exploration (analysis) and enforcement (tests) without triage.

---

## Outputs
- A set of adversarial ATDD scenarios (Given/When/Then + examples)
- A short decision log stating which failures were:
  - prevented,
  - rejected,
  - degraded,
  - tolerated (and why)

---

## Notes
- This tactic pairs well with:
## Notes
- This tactic pairs well with:
  - `adversarial-testing.tactic.md` (as a broader ideation pass)
  - `ammerse-analysis.tactic.md` (to prioritize trade-offs and constraints)
- Prefer **few, high-leverage** adversarial acceptance tests over exhaustive coverage.
  The goal is to protect the system's contract at the boundaries where reality meets expectations, not to enumerate every conceivable edge case.
