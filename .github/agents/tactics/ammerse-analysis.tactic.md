# Tactic: Analysis.AMMERSE

**Invoked by:**
- (Discoverable — architectural trade-off reasoning and decision analysis)

**Related tactics:**
- [`adversarial-testing.tactic.md`](./adversarial-testing.tactic.md) — stress-testing before AMMERSE analysis
- [`premortem-risk-identification.tactic.md`](./premortem-risk-identification.tactic.md) — risk discovery complements trade-off analysis

**Complements:**
- Directive 018 (Traceable Decisions) — ADR rationale documentation
- Approach: Decision-First Development

---

## Intent
Evaluate a practice, proposal, or technique using the AMMERSE decision-making framework in order to surface trade-offs, contextual fit, and second-order effects.

This tactic is used to **reason about decisions**, not to justify them.

---

## Preconditions
- The subject of analysis is clearly defined (practice, proposal, technique, or decision).
- The context of use is known or stated (team, organization, constraints).
- There is no predetermined outcome that this analysis is meant to defend.

---

## AMMERSE Dimensions (Reference)

The AMMERSE framework evaluates impact across seven dimensions:

- **Agile (A)**  
  The ability to adapt to change, incorporate feedback, and adjust decisions or processes without excessive friction.

- **Minimal (Mi)**  
  The degree to which the solution avoids unnecessary complexity, overhead, or cognitive load.

- **Maintainable (Ma)**  
  How easily the solution can be sustained, understood, and kept in working condition over time.

- **Environmental (E)**  
  Fit with the broader environment, including:
  - organizational culture
  - human factors
  - ethical considerations
  - societal or environmental impact
  - standards and norms

- **Reachable (R)**  
  Whether the goals implied by the solution are realistic and achievable within the given constraints (time, skills, resources).

- **Solvable (S)**  
  The extent to which the solution actually addresses the problem and can handle the challenges it introduces.

- **Extensible (Ex)**  
  The ability to evolve, scale, or extend the solution to meet future needs without fundamental redesign.

---

## Execution Steps
1. Restate the subject of analysis in one clear sentence.
2. Describe the context in which the subject would be applied.
3. For each AMMERSE dimension, perform the following:
   1. Describe the **positive impact** of the subject in this dimension.
   2. Describe the **negative impact or risk** in this dimension.
   3. Assign a qualitative weight to the impact  
      (`Low`, `Medium`, or `High`).
4. Identify at least one realistic alternative to the subject.
5. Repeat steps 3.1–3.3 for the alternative.
6. Summarize:
   - where the subject is a strong fit,
   - where it is a poor fit,
   - and which trade-offs are most significant.
7. Stop.

---

## Checks / Exit Criteria
- All seven AMMERSE dimensions are explicitly addressed.
- Both positive and negative impacts are documented for each dimension.
- At least one alternative is analyzed.
- Trade-offs are stated clearly, not implied.

---

## Failure Modes
- Treating AMMERSE as a scoring or ranking system.
- Omitting downsides to support a preferred decision.
- Writing generic statements that ignore context.
- Collapsing multiple dimensions into one argument.

---

## Outputs
- Structured AMMERSE analysis (table or structured prose)
- Contextual fit and trade-off summary
