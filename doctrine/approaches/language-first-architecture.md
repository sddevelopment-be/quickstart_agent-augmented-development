# Approach: Language-First Architecture

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Source:** Ubiquitous Language Experiment Research

---

## Purpose

Treat **language drift as an architectural signal** by recognizing that many architectural problems are preceded by linguistic problems. This approach makes semantic conflicts visible early enough to enable proactive architectural decisions.

---

## Core Principle

**Language Fragmentation Predicts System Problems**

When terminology becomes inconsistent or ambiguous, it signals deeper architectural issues:

| Linguistic Problem | Architectural Manifestation | Business Impact |
|-------------------|----------------------------|-----------------|
| Same term, multiple meanings | Hidden bounded context boundary | Accidental coupling, unexpected side effects |
| Different terms, same concept | Fragmented understanding | Duplicated logic, misaligned features |
| Vague or ambiguous terminology | Leaky abstractions | Maintenance burden, slow delivery |
| Missing domain vocabulary | Generic technical jargon dominates | Business rules hidden in code |
| Deprecated terms still in use | Legacy coupling | Refactoring paralysis |

---

## Why This Matters Now

### Historical Context

Continuous linguistic monitoring was **economically infeasible**:
- Manual glossary curation required dedicated ownership
- Capturing meeting transcripts and code at scale was labor-intensive
- Detecting drift patterns across multiple sources was prohibitive
- Feedback loops were measured in quarters, not days

### Agentic Feasibility Shift

Agentic systems change the economics:
- **Continuous capture** becomes tractable
- **Multi-source pattern detection** is efficient
- **Incremental maintenance** replaces big-bang efforts
- **PR-time feedback** replaces post-release discovery

This is not an incremental improvement—it's a **feasibility shift** that makes previously theoretical practices operational.

---

## Core Practices

### 1. Early Detection via Linguistic Signals

**Hypothesis:** Language conflicts precede architectural problems by 2-4 weeks (historical baseline).

**Evidence Chain:**
- Same term, different meanings → hidden bounded context boundary
- Different terms, same concept → fragmented understanding
- Vague terminology → leaky abstractions
- Deprecated terms persist → legacy coupling

**Target Metric:** Detect conflicts <2 weeks before architectural impact (50% improvement over baseline).

### 2. Treat Terminology as First-Class Architectural Concern

**Not just documentation hygiene:**
- Terminology decisions are architectural decisions
- Glossary ownership reflects system ownership
- Naming standards enforce boundaries
- Translation layers protect context integrity

**Integration Points:**
- Architecture Decision Records reference terminology choices
- Code reviews validate domain language usage
- PR checks enforce glossary compliance
- Refactoring plans include terminology alignment

### 3. Human-Led, Agent-Assisted Observation

**What Agents Do:**
1. **Observe** - ingest organizational artifacts (code, docs, transcripts)
2. **Extract** - identify domain concepts and terminology patterns
3. **Detect** - surface linguistic conflicts and drift
4. **Evidence** - present findings with source citations and confidence levels
5. **Propose** - suggest glossary entries, boundary clarifications

**What Agents Don't Do:**
- Make terminology decisions (humans own choices)
- Approve architecture (agents flag, humans judge)
- Enforce purity (defaults advisory, not punitive)
- Centralize authority (bounded contexts legitimize differences)

### 4. Continuous Feedback Loops

**Short Cycles:**
- **PR-time:** Terminology validation during code review
- **Weekly:** Glossary candidate triage
- **Quarterly:** Context boundary health check
- **Annual:** Governance retrospective

**Long Cycles:**
- Strategic architecture reviews informed by linguistic trends
- Organizational structure alignment with semantic boundaries
- Technology selection influenced by vocabulary complexity

---

## When to Use

✅ **Use Language-First Architecture when:**
- System complexity is growing (multiple teams, contexts)
- Cross-team misalignment signals appear
- Domain vocabulary conflicts arise frequently
- Architectural decisions feel unclear or contentious
- Legacy terminology constrains evolution

⚠️ **Exercise Caution when:**
- Team is too small to justify overhead (<5 people)
- Domain is well-understood and stable
- Organization resists linguistic discipline
- Tooling infrastructure unavailable

❌ **Do Not Use when:**
- Simple CRUD applications with minimal domain logic
- Prototyping phase (premature formalization)
- Team lacks DDD/architecture maturity
- Political environment weaponizes standards

---

## Integration with Doctrine Stack

### Related Approaches
- **[Bounded Context Linguistic Discovery](bounded-context-linguistic-discovery.md)** - Technique for inferring context boundaries
- **[Living Glossary Practice](living-glossary-practice.md)** - Maintenance workflow for terminology
- **[Decision-First Development](decision-first-development.md)** - ADR integration patterns

### Related Directives
- **[Directive 018: Traceable Decisions](../directives/018_traceable_decisions.md)** - Document terminology choices in ADRs
- **[Directive 034: Specification-Driven Development](../directives/034_spec_driven_development.md)** - Ubiquitous language in specs

### Related Tactics
- **[Terminology Extraction and Mapping](../tactics/terminology-extraction-mapping.tactic.md)** - How to build glossary
- **[Context Boundary Inference](../tactics/context-boundary-inference.tactic.md)** - Detect hidden boundaries

---

## Success Metrics

### Leading Indicators
- **Conflict Lead Time:** Time from linguistic conflict detection to architectural issue (target: <2 weeks)
- **Vocabulary Convergence:** Glossary term usage in docs/code (target: >80% adoption)
- **Cross-Context Collisions:** Same term, different meaning count (target: <5 per quarter)

### Lagging Indicators
- **Defect Rate:** Bugs traced to terminology ambiguity (target: <5% of total)
- **Integration Issues:** Failed handoffs between contexts (target: <2 per quarter)
- **Team Velocity:** Delivery speed stability (target: ±10% variance)

### Sentiment Indicators
- **Developer Survey:** "Can domain experts understand your code?" (target: >75% yes)
- **Suppression Patterns:** Glossary check override frequency (target: <10% PRs)
- **Contribution Rate:** Team-initiated glossary updates (target: >5 per quarter)

---

## Failure Modes and Mitigations

### Failure Mode 1: Linguistic Policing
**Symptom:** Compliance regime instead of shared understanding  
**Cause:** Punitive enforcement, centralized authority  
**Mitigation:** Default advisory-only, bounded context autonomy, tiered enforcement

### Failure Mode 2: False Positives
**Symptom:** Low-quality output damages trust  
**Cause:** Overaggressive detection, poor context awareness  
**Mitigation:** Confidence thresholds, register variation awareness, human review loops

### Failure Mode 3: Glossary as Power Tool
**Symptom:** Weaponized in organizational politics  
**Cause:** Centralized control, lack of ownership clarity  
**Mitigation:** Bounded context authority, transparent decision history, escalation to leadership

### Failure Mode 4: Maintenance Burden
**Symptom:** Glossary becomes stale, diverges from reality  
**Cause:** No ownership, big-bang updates, manual processes  
**Mitigation:** Mandatory ownership per context, continuous capture, incremental updates

---

## Agent Relevance

**Primary Agents:**
- **Architect Alphonso:** Strategic design using linguistic signals
- **Analyst Annie:** Requirements elicitation with domain vocabulary
- **Code Reviewer Cindy:** Terminology validation in PRs

**Supporting Agents:**
- **Lexical Larry:** Style and terminology consistency
- **Bootstrap Bill:** Initial glossary infrastructure setup
- **Curator Claire:** Ongoing glossary maintenance
- **Manager Mike:** Organizational alignment with Conway's Law

---

## References

### Research Sources
- **Experiment Primer:** `docs/architecture/experiments/ubiquitous-language/experiment-primer.md`
- **Concept Map:** `docs/architecture/experiments/ubiquitous-language/concept-map.md`
- **Research Findings:** `docs/architecture/experiments/ubiquitous-language/research-findings-summary.md`

### Theoretical Foundation
- **Domain-Driven Design:** Eric Evans (2003) - Ubiquitous Language, Strategic Design
- **Conway's Law:** Organizational structure predicts system architecture
- **Concept-Based Design:** Daniel Jackson (2021) - Software concepts and clarity

### Related Documentation
- **[DDD Core Concepts Reference](../docs/ddd-core-concepts-reference.md)** - Terminology primer
- **[Linguistic Anti-Patterns Catalog](../docs/linguistic-anti-patterns.md)** - Common failure modes
- **[Contextive Integration Guide](../docs/contextive-integration-guide.md)** - Tooling setup

---

## Version History

- **1.0.0** (2026-02-10): Initial version extracted from ubiquitous language experiment research

---

**Curation Status:** ✅ Claire Approved (Doctrine Stack Compliant)
