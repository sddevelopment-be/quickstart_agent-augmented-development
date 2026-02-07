# Tactic: Analysis.AdversarialTesting

**Invoked by:**
- Directive 018 (Traceable Decisions) — ADR preparation and proposal stress-testing

**Related tactics:**
- [`premortem-risk-identification.tactic.md`](./premortem-risk-identification.tactic.md) — project-specific failure scenario discovery
- [`ammerse-analysis.tactic.md`](./ammerse-analysis.tactic.md) — trade-off analysis after adversarial exploration

**Complements:**
- Approach: Decision-First Development

---

## Intent
Actively surface weaknesses, blind spots, and failure modes in a proposal, design, or decision by deliberately attempting to make it fail.

This tactic is used to **stress-test ideas before commitment**, not to criticize people or block progress.

---

## Preconditions

**Required inputs:**
- The subject under evaluation is clearly defined (proposal, design, plan, practice)
- The intended context of use is known (organization, team, constraints)
- Willingness to critically assess ideas without defensiveness

**Assumed context:**
- Psychological safety exists: this tactic targets the *idea*, not its author
- Environment values thorough risk assessment
- Goal is learning and risk reduction, not winning an argument

**Exclusions (when NOT to use):**
- Time-critical decisions requiring immediate action
- Trivial or easily reversible decisions
- Contexts where excessive criticism stifles necessary innovation
- When ideas are too preliminary for structured adversarial analysis

---

## Core Principle

This tactic is based on a simple inversion:

> Instead of asking “Why will this work?”, ask  
> **“How could this fail?”**

By explicitly adopting an adversarial stance, hidden assumptions and fragile reasoning become visible.

---

## Execution Steps

1. Restate the subject of analysis in one sentence.
2. Restate the **intended success outcome** in concrete terms.
3. Explicitly switch perspective:
   - Assume the subject has **failed in production**.
   - Assume the failure is real, not hypothetical.
4. Generate a list of failure scenarios by asking:
   - What assumptions turned out to be wrong?
   - What did people misunderstand or misuse?
   - What scaled poorly?
   - What human or organizational factors undermined it?
   - What external changes made it irrelevant or harmful?
5. For each failure scenario:
   1. Describe *how* the failure manifests.
   2. Identify the underlying cause (technical, human, organizational, environmental).
6. Group failure scenarios into themes.
7. Identify which failures are:
   - catastrophic,
   - likely,
   - or both.
8. Reflect on mitigations:
   - Which failures can be reduced?
   - Which must be explicitly accepted?
9. Stop.

---

## Checks / Exit Criteria
- Multiple failure scenarios have been identified.
- At least one human or organizational failure mode is included.
- Failure scenarios are concrete, not abstract.
- Risks are acknowledged without immediately defending against them.

---

## Failure Modes
- Treating this tactic as pessimism or obstruction.
- Rushing to solutions instead of fully exploring failure.
- Only listing technical failures and ignoring human factors.
- Softening language to avoid discomfort.

---

## Outputs
- List of concrete failure scenarios
- Thematic grouping of risks
- Explicitly acknowledged assumptions
- Optional mitigation notes

---

## Notes on Use

This tactic pairs well with:
- **AMMERSE analysis** (to contextualize risks)
- **Decision reviews** (before irreversible commitments)
- **Architecture or process changes** (with long-term impact)

Adversarial testing is not about negativity.  
It is about **intellectual honesty under uncertainty**.
