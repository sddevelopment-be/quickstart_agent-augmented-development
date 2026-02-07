# Tactic: Review.IntentAndRiskFirst

**Related tactics:**
- `adversarial-testing.tactic.md` — uses identified risks for structured adversarial analysis
- `analysis-extract-before-interpret.tactic.md` — extraction before interpretation in review context
- `code-review-incremental.tactic.md` — applies intent-first principle to code changes

**Complements:**
- Directive 024 (Self-Observation Protocol) — self-review using same intent-first pattern
- Approach: Decision-First Development — reviews validate decision rationale

---

## Intent
Review work by first understanding intent and surfacing risks before suggesting changes or solutions.

Use this tactic to provide high-value, low-noise feedback that respects the author's context and goals.

---

## Preconditions

**Required inputs:**
- A change set, document, or proposal exists
- The reviewer is not responsible for implementing changes
- The goal is evaluation, not execution

**Assumed context:**
- Review is requested or expected
- The author is open to feedback
- Time exists for thoughtful review (not emergency triage)

**Exclusions (when NOT to use):**
- When immediate fixes are required (emergency response mode)
- When the reviewer is also the implementer (use self-observation instead)
- When review is purely mechanical (automated checks, linting)

---

## Execution Steps

1. Read the **entire change** without commenting.
2. Summarize the **apparent intent** in one paragraph.
3. Identify **potential risks and unknowns**.
4. Categorize risks by type:
   - **Correctness** — functional defects, logic errors
   - **Maintainability** — complexity, clarity, testability
   - **Impact** — performance, security, scalability
   - **Misuse** — API design, error handling, edge cases
5. Stop without proposing fixes unless explicitly requested.

---

## Checks / Exit Criteria
- Intent summary is written and confirmed (or corrected by author).
- Risks are identified and categorized.
- No solutions are proposed prematurely.
- Feedback is actionable and specific.

---

## Failure Modes
- Suggesting fixes before understanding intent.
- Treating preferences or style choices as defects.
- Turning review into redesign or re-implementation.
- Focusing on trivial issues while missing significant risks.

---

## Outputs
- Intent summary (one paragraph)
- Risk list (categorized)
- Optional: Questions for clarification

---

## Notes on Use

**Why intent first?**
- Prevents misaligned feedback
- Respects the author's context and constraints
- Surfaces disagreements about goals early

**Why risk before solutions?**
- Allows author to choose mitigation strategy
- Avoids prescriptive, low-context suggestions
- Focuses review energy on high-impact issues

**High-value feedback is:**
- **Specific** — cites exact locations or examples
- **Categorized** — distinguishes severity and type
- **Respectful** — assumes good intent, offers perspective

**Low-value feedback:**
- Nitpicking style or formatting (use automated tools)
- Proposing alternative implementations without explaining risk
- Commenting on every minor detail

**Escalation indicators:**
- Critical correctness risks require immediate discussion
- Fundamental intent misalignment requires re-planning
- Security or safety issues require prioritization

---
