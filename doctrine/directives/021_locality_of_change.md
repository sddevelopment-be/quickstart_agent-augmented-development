<!-- The following information is to be interpreted literally -->

# 020 Locality of Change Directive

**Purpose:** Guide agents to avoid premature optimization and unnecessary complexity by measuring problem severity before designing solutions.

**Core Concept:** See [Locality of Change](../GLOSSARY.md#locality-of-change) in the glossary for foundational definition.

**Detailed Guidance:** See `approaches/locality-of-change.md` for comprehensive analysis framework and examples.

## Core Principle

**Don't add complexity to solve problems that don't exist.**

Before introducing new patterns, abstractions, or architectural enhancements:

1. Verify the problem exists in practice (not just theory)
2. Measure its actual impact or frequency
3. Consider whether current approaches already handle it adequately

## Quick Decision Checklist

Use this checklist before proposing architectural changes:

- [ ] **Problem Evidence:** Can I point to 3+ real instances where current approach failed?
- [ ] **Severity Measured:** Have I quantified the impact (frequency, cost, risk)?
- [ ] **Baseline Considered:** Have I evaluated "do nothing" as an option?
- [ ] **Simple Alternatives:** Have I explored documentation/guideline solutions first?
- [ ] **Principle Alignment:** Does this preserve or enhance core architectural values?
- [ ] **Emergence Respected:** Am I prescribing too early instead of letting patterns emerge?
- [ ] **Cost/Benefit Ratio:** Does this achieve significant value at proportional cost?

If 5+ boxes cannot be checked, pause and reassess the problem framing.

## Anti-Patterns to Avoid

### Gold Plating

- Adding features "just in case" or "for completeness"
- Solving hypothetical future problems
- Over-engineering for flexibility never exercised

### Premature Abstraction

- Creating lookup tables before patterns stabilize
- Introducing automation before manual process proves valuable
- Building frameworks before use cases mature

### Complexity Creep

- Each small addition seems reasonable in isolation
- Cumulative effect degrades simplicity principle
- System becomes harder to understand and maintain

## Application Guidance

### For All Agents

- Question requirements that add significant complexity
- Request evidence of problem severity before implementation
- Advocate for "do nothing" when current state is adequate
- Favor organic emergence over premature prescription
- **For exploratory work under uncertainty:** Invoke `tactics/safe-to-fail-experiment-design.tactic.md`
- **When reviewing changes:** Invoke `tactics/code-review-incremental.tactic.md` to prevent scope expansion

### For Architects & Build-Automation

- Use this directive during ADR creation and design reviews
- Apply before adding new CI steps, tooling layers, or automation
- Validate that proposed solutions address measured problems

### For Curators

- Reference when auditing consistency across artifacts
- Flag proposals that violate locality of change principles
- Suggest simpler alternatives during review cycles

## Integration with Directives

- **[Directive 011](./011_risk_escalation.md) (Risk & Escalation):
  ** Use ⚠️ when uncertain about problem severity; flag ❗️ if proposed solution violates core principles
- **[Directive 012](./012_operating_procedures.md) (Operating Procedures):
  ** "Ask clarifying questions when uncertainty >30%" applies to problem assessment
- **[Directive 014](./014_worklog_creation.md) (Work Logs):** Document problem evidence, severity analysis, and alternative evaluation in logs
- **ADRs:** Cross-reference architectural decisions (see `${DOC_ROOT}/architecture/decisions/`) to ensure new proposals align with established direction
