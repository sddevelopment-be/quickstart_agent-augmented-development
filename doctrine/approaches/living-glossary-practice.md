# Approach: Living Glossary Practice

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Source:** Ubiquitous Language Experiment Research

---

## Purpose

Maintain a **continuously updated, executable glossary** as infrastructure rather than static documentation. This approach treats terminology as a living artifact that evolves with code and domain understanding.

---

## Core Principle

**Glossary as Executable Artifact, Not Static Document**

Traditional glossaries fail because they:
- Become stale instantly (point-in-time snapshots)
- Lack ownership (no one maintains them)
- Are ignored (not integrated into workflow)
- Provide no enforcement (advisory only, easily bypassed)

Living glossaries succeed because they:
- Update continuously (agentic capture + human review)
- Have clear ownership (per bounded context)
- Integrate into workflow (PR checks, IDE plugins)
- Provide tiered enforcement (advisory → acknowledgment → hard failure)

---

## Economic Feasibility Shift

### Historical Infeasibility

**Manual Approach Barriers:**
- Point-in-time glossaries became stale
- Continuous capture was labor-intensive
- Multi-source analysis was prohibitive
- Feedback loops measured in quarters

**Outcome:** "Dictionary DDD" anti-pattern—create glossary document, consider DDD "done," never update it.

### Agentic Enablement

**What Changed:**
- **Continuous capture:** Agents observe code, docs, meetings automatically
- **Pattern detection:** LLMs identify terminology conflicts at scale
- **Incremental maintenance:** Small updates replace big-bang efforts
- **PR-time feedback:** Validation during development, not post-release

**New Feasibility:** Living glossaries are now operationally viable, not just aspirational.

---

## Governance Model: Human in Charge

### Not "Human in the Loop"

**Human in the Loop (Wrong):**
- Agents propose, humans approve (reactive)
- Oversight role (after the fact)
- Compliance checkpoints (bureaucratic)

**Human in Charge (Correct):**
- Humans own terminology decisions (proactive)
- Accountability and authority (decision rights)
- Veto power over automation (override anytime)

### Ownership Model

**Per Bounded Context:**
- Each context has an **owner** (team lead, domain expert, or architect)
- Owner approves glossary entries for their context
- Owner defines enforcement tier (advisory, acknowledgment, hard failure)
- Owner maintains decision history (why terms chosen, alternatives considered)

**Cross-Context:**
- **Shared terms** require negotiation between context owners
- **Translation rules** defined at boundaries (explicit mapping)
- **Conflict resolution** escalates to architectural decision (ADR required)

---

## Enforcement Tiers

### Tier 1: Advisory (Default)

**When:** New terms, style preferences, emerging patterns  
**Behavior:** Comment on PR, no blocking  
**Override:** No acknowledgment required  
**Use Case:** Suggestions, experimentation, learning

**Example:** "Consider using 'Customer' instead of 'User' per glossary. (Advisory)"

---

### Tier 2: Acknowledgment Required

**When:** Deprecated terms, cross-context usage, known conflicts  
**Behavior:** PR requires explicit acknowledgment to merge  
**Override:** Developer must confirm they've reviewed and accept risk  
**Use Case:** Warnings, drift detection, boundary violations

**Example:** "Term 'Order' has different meanings in Sales and Fulfillment contexts. Acknowledge cross-context usage. (Acknowledgment Required)"

---

### Tier 3: Hard Failure (Rare)

**When:** Banned terms, critical violations, security risks  
**Behavior:** PR blocked until fixed  
**Override:** Requires owner approval and written justification  
**Use Case:** Regulatory compliance, security, explicit policy

**Example:** "Term 'password' banned in logs per security policy. Use 'credential hash'. (Hard Failure)"

**Caution:** Overuse creates resentment. Reserve for critical cases only.

---

## Glossary Structure

### Term Entry Format

```yaml
term: "Bounded Context"
definition: "Explicit boundary within which a domain model and its ubiquitous language have clear, consistent meaning."
context: "DDD Core"
source: "Domain-Driven Design, Eric Evans (2003)"
related_terms:
  - "Ubiquitous Language"
  - "Context Map"
  - "Semantic Boundary"
status: "canonical"
owner: "architect-alphonso"
enforcement_tier: "advisory"
decision_history:
  - date: "2026-02-10"
    rationale: "Core DDD term, widely adopted"
    alternatives_considered: ["Domain Boundary", "Semantic Context"]
```

### Status Lifecycle

1. **Candidate** - Proposed, under review
2. **Canonical** - Approved, active use
3. **Deprecated** - Being phased out, avoid in new code
4. **Under Review** - Existing term being re-evaluated
5. **Superseded** - Replaced by new term (historical reference only)

---

## Integration Points

### 1. IDE Integration (Contextive)

**What:** IDE plugin showing glossary terms inline during development

**Benefits:**
- Developers see definitions while coding
- Context-aware (shows terms for current module's context)
- Reduces cognitive load (no context switching)

**Setup:** See [Contextive Integration Guide](../docs/contextive-integration-guide.md)

---

### 2. PR-Level Validation

**What:** Automated glossary checks during code review

**Checks:**
- ✅ New terminology documented?
- ⚠️ Using deprecated terms?
- ❌ Cross-context violations?
- ℹ️ Glossary candidates suggested?

**Implementation:** GitHub Actions, GitLab CI, or LLM-based agent review

---

### 3. Specification Alignment

**What:** Specs reference glossary terms with hyperlinks

**Format:**
```markdown
The [Customer](#customer) places an [Order](#order) which triggers [Fulfillment](#fulfillment).
```

**Validation:** Check that all domain terms in specs exist in glossary.

---

### 4. Architecture Decision Records

**What:** ADRs document terminology choices

**Template Addition:**
```markdown
## Terminology Decisions

| Term | Definition | Rationale |
|------|------------|-----------|
| "Customer" | Person who purchases | Preferred over "User" (too generic) |
| "Order" | Purchase intent | Distinct from "Fulfillment Order" (warehouse) |
```

**Traceability:** Link ADRs ↔ glossary entries bidirectionally.

---

## Maintenance Workflow

### Continuous Capture

**Frequency:** Ongoing, automated observation

**Process:**
1. **Agents observe:** Code, docs, meetings, PRs
2. **Pattern detection:** Identify new terms, conflicts, drift
3. **Candidate generation:** Propose glossary entries
4. **Human review:** Owner approves/rejects/modifies

**Output:** Glossary candidates queue for weekly triage

---

### Weekly Triage

**Frequency:** Weekly 30-minute session

**Process:**
1. **Review candidates:** Agent-generated proposals
2. **Make decisions:** Approve, reject, defer
3. **Assign enforcement tiers:** Advisory, acknowledgment, hard failure
4. **Update glossary:** Commit changes with rationale

**Participants:** Context owners, architects, domain experts

---

### Quarterly Health Check

**Frequency:** Quarterly 2-hour workshop

**Activities:**
1. **Staleness audit:** Identify outdated definitions
2. **Coverage assessment:** Missing domain terms?
3. **Conflict resolution:** Address ambiguities
4. **Enforcement review:** Are tiers appropriate?

**Outcome:** Glossary refinement plan, enforcement adjustments

---

### Annual Governance Retrospective

**Frequency:** Annual half-day session

**Activities:**
1. **Hard failure justification review:** Were blocks necessary?
2. **False positive analysis:** Agent accuracy assessment
3. **Organizational alignment:** Conway's Law validation
4. **Tooling evolution:** What worked? What didn't?

**Outcome:** Governance policy updates, process improvements

---

## When to Use

✅ **Use Living Glossary when:**
- Multiple teams share domain vocabulary
- Terminology conflicts arise regularly
- Domain complexity requires precision
- Onboarding new team members
- Long-lived systems with evolving domain

⚠️ **Exercise Caution when:**
- Team is small (<5 people, informal glossary sufficient)
- Domain is simple and well-understood
- Organization resists process discipline
- Tooling overhead exceeds benefit

❌ **Do Not Use when:**
- Prototyping phase (premature formalization)
- Throwaway code or experiments
- Domain vocabulary is trivial
- Team communication already excellent

---

## Success Metrics

### Adoption Metrics
- **Glossary term usage in code/docs:** Target >80%
- **IDE plugin active users:** Target >75% of team
- **Glossary update frequency:** Target >5 per quarter

### Quality Metrics
- **Staleness rate:** % of outdated definitions (Target <10%)
- **Coverage:** % of domain terms documented (Target >90%)
- **Conflict resolution time:** Days to resolve ambiguity (Target <7 days)

### Sentiment Metrics
- **Developer survey:** "Glossary is helpful" (Target >75% agree)
- **Suppression patterns:** % PRs overriding checks (Target <10%)
- **Contribution rate:** Team-initiated entries (Target >50%)

---

## Failure Modes and Mitigations

### Failure Mode 1: Maintenance Burden
**Symptom:** Glossary becomes stale, diverges from reality  
**Cause:** No ownership, big-bang updates, manual processes  
**Mitigation:** Mandatory ownership per context, continuous capture, incremental updates

### Failure Mode 2: Linguistic Policing
**Symptom:** Compliance regime instead of shared understanding  
**Cause:** Punitive enforcement, centralized authority  
**Mitigation:** Default advisory-only, bounded context autonomy, tiered enforcement

### Failure Mode 3: False Positives
**Symptom:** Low-quality output damages trust  
**Cause:** Overaggressive detection, poor context awareness  
**Mitigation:** Confidence thresholds, register variation awareness, human review loops

### Failure Mode 4: Glossary as Power Tool
**Symptom:** Weaponized in organizational politics  
**Cause:** Centralized control, lack of ownership clarity  
**Mitigation:** Bounded context authority, transparent decision history, escalation protocols

---

## Agent Relevance

**Primary Agents:**
- **Lexical Larry:** Terminology consistency validation
- **Curator Claire:** Ongoing glossary maintenance
- **Bootstrap Bill:** Initial glossary infrastructure setup

**Supporting Agents:**
- **Architect Alphonso:** Strategic term definitions
- **Analyst Annie:** Requirements terminology alignment
- **Code Reviewer Cindy:** PR-level enforcement

---

## References

### Research Sources
- **Experiment Primer:** `docs/architecture/experiments/ubiquitous-language/experiment-primer.md` (Section 2: Governance)
- **Terminology Map:** `docs/architecture/experiments/ubiquitous-language/terminology-map.md`

### Theoretical Foundation
- **Domain-Driven Design:** Eric Evans (2003) - Living Documentation
- **Evolutionary Architecture:** Ford, Parsons, Kua (2017) - Fitness Functions

### Related Documentation
- **[DDD Core Concepts Reference](../docs/ddd-core-concepts-reference.md)** - Core terminology
- **[Contextive Integration Guide](../docs/contextive-integration-guide.md)** - Tooling setup
- **[Linguistic Anti-Patterns Catalog](../docs/linguistic-anti-patterns.md)** - Common failures

---

## Version History

- **1.0.0** (2026-02-10): Initial version extracted from ubiquitous language experiment research

---

**Curation Status:** ✅ Claire Approved (Doctrine Stack Compliant)
