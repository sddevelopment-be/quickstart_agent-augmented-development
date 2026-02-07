# Tactic: Reflection.PostActionLearningLoop

**Related tactics:**
- `premortem-risk-identification.tactic.md` — proactive learning before action
- `adversarial-testing.tactic.md` — critical analysis that feeds learning

**Complements:**
- [Directive 024 (Self-Observation Protocol)](../directives/024_self_observation_protocol.md) — captures learning during execution
- Approach: Decision-First Development — lessons inform future decisions

---

## Intent
Capture learning after completing a task in order to improve future decisions, tactics, or constraints.

Use this tactic to externalize knowledge gained through experience and encode it for future use.

---

## Preconditions

**Required inputs:**
- A task or action has been completed
- Outcomes are observable and can be evaluated
- Reflection is intended to inform future work

**Assumed context:**
- Learning is valued and will be acted upon
- Time for reflection is available
- A mechanism exists to encode and surface lessons

**Exclusions (when NOT to use):**
- When immediate follow-up action is required (defer reflection briefly)
- When outcomes are still unfolding or unclear
- For trivial tasks with no reusable lessons

---

## Execution Steps

1. Restate the **original intent** of the task.
2. Describe **what actually happened** (outcomes, process, challenges).
3. Identify what **worked as expected**.
4. Identify what **did not work or caused friction**.
5. Extract **1–3 concrete lessons** from the experience.
6. Suggest **where these lessons should be encoded** (guideline, tactic, template, directive, approach).
7. Stop.

---

## Checks / Exit Criteria
- At least one lesson is extracted.
- Lessons are concrete and actionable (not vague or generic).
- A target location for encoding is identified.
- Lessons are documented for future reference.

---

## Failure Modes
- Vague or generic lessons ("we should communicate better").
- Retrospective justification (defending decisions instead of learning).
- Failing to externalize learning (keeping it implicit or personal).
- Extracting too many lessons (reduces focus and actionability).

---

## Outputs
- Short reflection document
- List of extracted lessons
- Recommendations for encoding lessons

---

## Notes on Use

**Good lessons are:**
- **Concrete** — specific to a situation, but generalizable
- **Actionable** — suggest a change in behavior or approach
- **Encoded** — written down and made discoverable

**Poor example:**
- "We should have been more careful."

**Good example:**
- "Context-Establish-And-Freeze tactic prevented scope drift when applied before implementation. Recommend invoking it for all tasks with ambiguous requirements."

**Integration points:**
- **Tactics** — when a repeatable pattern emerges
- **Directives** — when a principle needs elevation
- **Templates** — when structure improves outcomes
- **Guidelines** — when guidance clarifies ambiguity

**Frequency:** Use this tactic after:
- Completing significant work (features, refactorings, analyses)
- Encountering unexpected challenges or surprises
- Discovering gaps in existing guidance
- Quarterly or milestone reviews

---
