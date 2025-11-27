# Locality of Change / Avoiding Gold Plating - Comprehensive Approach

**Purpose:** Guide agents to avoid premature optimization and unnecessary complexity by measuring problem severity before designing solutions, favoring simple alternatives, and maintaining architectural discipline.

**Quick Reference:** For condensed guidance, see [Directive 020](../directives/020_locality_of_change.md)

---

## 1. Core Principle

**Don't add complexity to solve problems that don't exist.**

Before introducing new patterns, abstractions, or architectural enhancements:
1. Verify the problem exists in practice (not just theory)
2. Measure its actual impact or frequency
3. Consider whether current approaches already handle it adequately

## 2. Problem Assessment Protocol

When proposing new solutions or enhancements:

### Required Analysis Steps
1. **Evidence Collection:** Gather data showing the problem manifests in practice
   - Review actual task logs, work patterns, or system behavior
   - Count occurrences, measure frequency, assess impact
   - Distinguish between hypothetical concerns and observed pain points

2. **Severity Measurement:** Quantify the problem's impact
   - How often does it occur?
   - What is the cost of the current workaround?
   - What is the risk if left unaddressed?

3. **Baseline Option:** Always include "do nothing" in trade-off analysis
   - Current state may be acceptable
   - Organic emergence may solve the issue naturally
   - Premature solutions can create maintenance burden

4. **Simple Alternatives First:** Explore lightweight approaches
   - Can documentation/guidelines address it?
   - Can existing patterns be adapted?
   - What achieves 80% of benefits at 20% of cost?

## 3. Architectural Preservation

**Preserve core principles even when solutions seem beneficial.**

Before introducing changes that affect system architecture:
- Cross-check against established ADRs and design principles
- Verify alignment with strategic vision (simplicity, emergence, file-based clarity)
- Consider whether the change would create drift from foundational decisions
- If principles conflict with proposed solution, revisit the problem framing

## 4. Pattern Discipline

**Pattern analysis must always precede pattern prescription.**

When identifying workflows that could benefit from standardization:
- Observe actual practice across multiple instances
- Document what currently works
- Identify genuine pain points (not theoretical inefficiencies)
- Design patterns based on real usage, not anticipated usage
- Let patterns emerge organically before codifying them

## 5. Cost-Benefit Calibration

**Simple alternatives often achieve 80% of benefits at 20% of cost.**

Evaluate solutions across multiple dimensions:
- **Complexity Cost:** Maintenance burden, cognitive overhead, integration surface
- **Flexibility Cost:** Does it constrain future evolution?
- **Alignment Cost:** Does it drift from core principles?
- **Value Delivery:** What % of the problem does it actually solve?

Prefer solutions that:
- Require minimal new abstractions
- Leverage existing mechanisms
- Remain optional or low-touch
- Can be reversed easily if ineffective

## 6. Decision Framework

Use this checklist before proposing architectural changes:

- [ ] **Problem Evidence:** Can I point to 3+ real instances where current approach failed?
- [ ] **Severity Measured:** Have I quantified the impact (frequency, cost, risk)?
- [ ] **Baseline Considered:** Have I evaluated "do nothing" as an option?
- [ ] **Simple Alternatives:** Have I explored documentation/guideline solutions first?
- [ ] **Principle Alignment:** Does this preserve or enhance core architectural values?
- [ ] **Emergence Respected:** Am I prescribing too early instead of letting patterns emerge?
- [ ] **Cost/Benefit Ratio:** Does this achieve significant value at proportional cost?

If 5+ boxes cannot be checked, pause and reassess the problem framing.

## 7. Anti-Patterns to Avoid

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

## 8. Application Guidance

### For Architects
- Use this directive during ADR creation and design reviews
- Validate that proposed solutions address measured problems
- Check alignment with strategic principles before committing

### For Build-Automation Specialists
- Apply before adding new CI steps, tooling layers, or automation
- Ensure tooling solves real friction, not theoretical optimization
- Prefer extending existing tools over introducing new ones

### For Curators
- Reference when auditing consistency across artifacts
- Flag proposals that violate locality of change principles
- Suggest simpler alternatives during review cycles

### For All Agents
- Question requirements that add significant complexity
- Request evidence of problem severity before implementation
- Advocate for "do nothing" when current state is adequate
- Favor organic emergence over premature prescription

## 9. Examples

**✅ Good Practice:**
- Observing 20+ tasks to validate handoff patterns before proposing lookup table
- Measuring 4 handoffs across 20 tasks (20% frequency) before concluding system works well
- Rejecting complex solution when simple agent profile enhancement achieves goal
- Including "do nothing" baseline in trade-off analysis

**❗️ Anti-Pattern:**
- Proposing centralized lookup table without measuring handoff frequency
- Assuming inefficiency exists without reviewing actual task completion data
- Designing comprehensive solution before validating problem severity
- Optimizing coordination that already has 100% success rate

## 10. Integration with Existing Directives

- **Directive 011 (Risk & Escalation):** Use ⚠️ when uncertainty about problem severity; flag ❗️ if proposed solution violates core principles
- **Directive 012 (Operating Procedures):** "Ask clarifying questions when uncertainty >30%" applies to problem assessment
- **Directive 014 (Work Logs):** Document problem evidence, severity analysis, and alternative evaluation in logs
- **ADRs:** Cross-reference architectural decisions to ensure new proposals align with established direction

## 11. Success Indicators

When this directive is applied effectively:
- Rejected proposals cite specific evidence gaps
- Accepted proposals include clear problem quantification
- Simple alternatives are documented even when more complex solution chosen
- Trade-off analyses consistently include "do nothing" baseline
- System simplicity is preserved or enhanced over time

---

**Assigned To:** architect, build-automation, curator  
**Last Updated:** 2025-11-24  
**Version:** 1.0.0  
**Status:** Active
