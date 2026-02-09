# Ubiquitous Language Experiment: A Primer

**Version:** 1.0.0  
**Date:** 2026-02-09  
**Purpose:** Foundational understanding of the agentic ubiquitous language experiment  
**Audience:** Architects, engineering leads, and agents participating in the experiment  
**Reading Time:** ~15 minutes

---

## Executive Summary

This experiment tests whether agentic systems can make **semantic drift visible early enough to matter** by treating language as a first-class architectural concern. The core insight: many architectural problems are preceded by linguistic problems. The system observes language patterns, surfaces conflicts, and enables human-led decisions about terminology governance—with agents as sensors, not authorities.

**Key Principle:** Human in charge, not human in the loop. Agents detect and evidence; humans interpret and decide.

---

## 1. Hypothesis: Language Drift as Architectural Signal

### The Core Observation

Domain-Driven Design's most powerful corporate effect is not its tactical patterns (aggregates, repositories, entities), but its **linguistic discipline**:

- **Shared terms within a context** - teams speaking the same vocabulary
- **Explicit disagreement across contexts** - acknowledging semantic boundaries
- **Conscious translation at boundaries** - deliberate transformation of terms

When language drifts, architecture follows. Common patterns:

| Linguistic Problem | Architectural Manifestation | Business Impact |
|-------------------|----------------------------|-----------------|
| Same term, multiple meanings | Hidden bounded context boundary | Accidental coupling, unexpected side effects |
| Different terms, same concept | Fragmented understanding | Duplicated logic, misaligned features |
| Vague or ambiguous terminology | Leaky abstractions | Maintenance burden, slow delivery |
| Missing domain vocabulary | Generic technical jargon dominates | Business rules hidden in code |
| Deprecated terms still in use | Legacy coupling | Refactoring paralysis |

### Why This Matters Now

Historically, continuous linguistic monitoring was **economically infeasible**:

- Manual glossary curation required dedicated ownership
- Capturing meeting transcripts and code at scale was labor-intensive
- Detecting drift patterns across multiple sources was prohibitive
- Feedback loops were measured in quarters, not days

**Agentic systems change the economics:**

- Continuous capture becomes tractable
- Multi-source pattern detection is efficient
- Incremental maintenance replaces big-bang efforts
- Feedback can occur at PR-time, not post-release

This is not an incremental improvement—it's a **feasibility shift** that makes previously theoretical practices operational.

---

## 2. Mechanism: Agents as Drift Detectors

### What Agents Do

The system uses LLM-based agents to:

1. **Observe** - ingest organizational artifacts (code, docs, transcripts, meeting notes)
2. **Extract** - identify domain concepts and terminology patterns
3. **Detect** - surface cases where:
   - The same word means different things in different contexts
   - Different words are used for the same concept
   - Terminology clashes across team or system boundaries
4. **Evidence** - present findings with source citations and confidence levels
5. **Propose** - suggest glossary entries, boundary clarifications, translation needs

### What Agents Don't Do

- **Make decisions** - humans own all terminology choices
- **Approve architecture** - agents flag, humans judge
- **Enforce purity** - defaults are advisory, not punitive
- **Centralize authority** - bounded contexts legitimize local differences

### The Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ Input Sources                                                    │
│ • Codebase (names, comments, docs)                             │
│ • Meeting transcripts (anonymized)                              │
│ • Architecture docs, ADRs                                       │
│ • Team communication channels                                   │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Agent Processing                                                 │
│ • Linguistic pattern detection                                  │
│ • Semantic conflict identification                              │
│ • Context boundary inference                                    │
│ • Glossary candidate extraction                                 │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Human Review                                                     │
│ • Accept/reject glossary entries                                │
│ • Assign term ownership per context                             │
│ • Document translation rules                                    │
│ • Classify conflicts (true/false positives)                     │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Continuous Feedback                                              │
│ • PR-level domain review (terminology checks)                   │
│ • Boundary leak detection                                       │
│ • Drift trend monitoring                                        │
│ • Glossary maintenance prompts                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Technical Capabilities

**LLMs are strong at:**
- Pattern detection across large corpora
- Identifying linguistic inconsistencies
- Suggesting semantic relationships
- Operating at scale with low incremental cost

**LLMs are weak at:**
- Determining "correct" terminology (context-dependent)
- Understanding business incentive conflicts
- Judging political implications of naming
- Assessing sociolinguistic register variations

**Design implication:** Use LLMs for observation and evidence; reserve judgment for humans.

---

## 3. Governance: Human in Charge

### Terminology Ownership

Every term in the glossary has:
- **Owner** - individual/team accountable for definition
- **Context** - bounded context where term applies
- **Status** - Canonical | Deprecated | Under Review | Candidate
- **History** - decision rationale and evolution

### Enforcement Tiers

The system supports **asymmetric enforcement** to balance guidance with autonomy:

| Tier | Behavior | Use Case |
|------|----------|----------|
| **Advisory** | Comment on PR, no blocking | New term suggestions, style preferences |
| **Acknowledgment** | Require developer confirmation | Deprecated terms, cross-context usage |
| **Hard Failure** | Block PR merge | Banned terms, critical boundary violations |

**Default:** Advisory. Escalate to acknowledgment/hard failure only with explicit human decision and documentation.

### Decision Rights

- **Local (Team/Context):** Term definitions within bounded context
- **Architectural:** Cross-context translation rules, boundary policies
- **Organizational:** Globally banned terms, compliance requirements

### Review Cadence

- **Continuous:** PR-level terminology feedback
- **Weekly:** Drift trend review, new candidate triage
- **Quarterly:** Glossary health check, deprecated term cleanup
- **Annual:** Governance model retrospective

---

## 4. Where It Fits in Delivery

### The 8-Stage Pipeline

The experiment spans from research to outcome capture:

```
Research & Capture → Prune & Synthesize → Architectural Analysis
    ↓
Specification (Vocabulary + Functional Slices) → Technical Design
    ↓
Execution → Evaluation → Capture Outcomes
```

Each stage has:
- **Purpose** - why this stage exists
- **Inputs** - what materials are needed
- **Outputs** - concrete artifacts produced
- **Quality Gate** - decision criterion to proceed

### Integration Points

**With ADRs (ADR-017 Traceable Decisions):**
- Language decisions reference governing ADRs
- Architectural decisions cite glossary terms
- Decision markers link terminology to rationale

**With Test-Driven Development (ADR-012):**
- Acceptance tests use domain vocabulary from glossary
- Test names follow ubiquitous language conventions
- Failing tests surface terminology ambiguity

**With PR Review:**
- Domain review agent runs on every PR diff
- Flags terminology drift, boundary leaks, deprecated terms
- Provides glossary links for context

**With Agent Orchestration (ADR-008):**
- Agents check relevant glossary before generating code
- Task outputs reference governing terminology decisions
- Work logs document linguistic choices made

---

## 5. Failure Modes and Mitigations

### Failure Mode 1: Linguistic Policing

**Risk:** System becomes a compliance regime where developers write to appease bots instead of achieving shared understanding.

**Symptoms:**
- Defensive reactions to PR feedback
- Performative adherence without comprehension
- Increased anxiety around terminology choices
- Gaming the system (e.g., writing vague generic terms)

**Mitigations:**
- Default to advisory feedback, not blocking
- Make suppression easy with required rationale
- Publish suppression patterns to identify systemic issues
- Measure developer sentiment through retrospectives
- Require human approval for any hard-failure rules

### Failure Mode 2: False Positives and Early Noise

**Risk:** Low-quality output in early stages damages trust and leads to abandonment.

**Symptoms:**
- Casual shorthand misread as semantic conflict
- Legacy code distorts current understanding
- Transcripts capture exploratory language, not decisions
- High suppression rates

**Mitigations:**
- Phase introduction: team-by-team, context-by-context
- Explicit training period with feedback-only mode
- Confidence thresholds for suggestions
- Regular false-positive review and model tuning
- Transparent accuracy metrics published to teams

### Failure Mode 3: Glossary as Power Instrument

**Risk:** Terminology enforcement becomes a tool for organizational control.

**Symptoms:**
- One team's language becomes "official" across contexts
- Cross-team blocks weaponized in political conflicts
- Glossary ownership concentrated in architecture team
- Lack of translation tolerance at boundaries

**Mitigations:**
- Bounded contexts explicitly legitimize local differences
- Translation required at boundaries, not unification
- Ownership distributed to domain teams, not centralized
- Escalation process for conflicts (with mediation)
- Audit log of glossary changes and decision rationale

### Failure Mode 4: Incentive Conflicts Misdiagnosed as Semantic Conflicts

**Risk:** Terms diverge because incentives diverge, not due to misunderstanding. A glossary documents this but cannot resolve it.

**Symptoms:**
- Same term redefined by different product lines
- Persistent conflicts despite clear documentation
- Workarounds that bypass glossary
- Teams agreeing on definitions but not behavior

**Mitigations:**
- Recognize when conflict is organizational, not linguistic
- Escalate to leadership when incentives misalign
- Document conflict explicitly in glossary
- Use bounded contexts to contain, not force resolution

### Failure Mode 5: Canonizing the Wrong Model

**Risk:** System standardizes what is common rather than what is correct or useful.

**Symptoms:**
- Legacy language formalized despite known issues
- Majority usage overrides domain expert judgment
- Generic technical terms replace rich domain vocabulary
- Glossary reflects "as-is" instead of "should-be"

**Mitigations:**
- Distinguish descriptive (observed) vs prescriptive (intended) terms
- Require domain expert review for canonical status
- Support coexistence of "current" and "target" terminology
- Migration plans for terminology evolution

### Failure Mode 6: Maintenance Burden and Glossary Rot

**Risk:** Glossaries decay without ownership, cadence, and tooling.

**Symptoms:**
- Stale definitions
- Deprecated terms not marked
- No clear ownership for updates
- Increasing divergence between glossary and reality

**Mitigations:**
- Mandatory ownership assignment for every term
- Automated staleness detection (terms not referenced)
- Quarterly health reviews
- PR-based glossary updates (treat as code)
- Metrics: term coverage, staleness age, conflict resolution time

---

## 6. Success Criteria

This experiment succeeds if:

1. **Early Detection:** Semantic conflicts surface 2+ weeks earlier than historical baseline
2. **Improved Conversations:** Architecture discussions reference shared vocabulary
3. **Reduced Coupling:** Measurable decrease in cross-context term collisions
4. **Reusable Insight:** Patterns and techniques documented for future application

**Failure is acceptable.** Silent drift is not.

The goal is learning, not perfection. If the experiment reveals that linguistic monitoring is not cost-effective, that knowledge has value. What matters is making the attempt **inspectable and honest**.

---

## 7. Key Concepts the Experiment Depends On

This experiment synthesizes multiple theoretical foundations:

### Domain-Driven Design (Eric Evans, Vaughn Vernon)

**Ubiquitous Language:**
- Shared vocabulary between domain experts and developers
- Reduces translation errors and misunderstandings
- Evolves through continuous collaboration

**Bounded Contexts:**
- Explicit boundaries within which terms have consistent meaning
- Different contexts may use same word with different definitions
- Translation required at context boundaries, not global standardization

**Strategic Design:**
- Context mapping reveals organizational and linguistic boundaries
- Upstream/downstream relationships affect terminology authority
- Anti-corruption layers protect context integrity

### Conway's Law and Team Topologies (Mel Conway, Skelton & Pais)

**Conway's Law:**
- System structure mirrors communication structure
- Team boundaries predict semantic boundaries
- Misaligned topology creates persistent language conflicts

**Team Topologies:**
- Stream-aligned teams own domain vocabulary in their context
- Platform teams provide shared technical vocabulary
- Cognitive load limits terminology complexity

**Architectural Implication:**
- Language drift often signals team boundary issues
- Semantic conflicts reveal hidden coupling
- Vocabulary scope should match team scope

### Concept-Based Design (Rebecca Wirfs-Brock, Daniel Jackson)

**Naming as Design:**
- Names are not cosmetic—they constrain implementation
- Poor naming creates hidden coupling
- Refactoring names is architectural work

**Concepts as Anchors:**
- Stable concepts provide design clarity
- Good concepts balance precision and generality
- Responsibilities (OO) sharpen vocabulary

**Design Implication:**
- Terminology choices have architectural weight
- Name changes should be deliberate and traced
- Ambiguous names indicate design uncertainty

### Evolutionary Architecture (Ford, Parsons, Kua)

**Fitness Functions:**
- Automated checks that verify architectural properties
- Linguistic checks as fitness functions for semantic integrity
- Trade-offs between guidance and rigidity

**Architectural Drift:**
- Small deviations compound over time
- Continuous monitoring more effective than periodic audits
- Feedback loops prevent drift from becoming entrenched

---

## 8. What Makes This Different

### Compared to Traditional Glossary Initiatives

| Traditional Approach | Agentic Approach |
|---------------------|------------------|
| Manual curation | Automated extraction with human review |
| Point-in-time snapshot | Continuous observation |
| Centralized ownership | Distributed, context-specific ownership |
| Published document | Living, PR-integrated feedback |
| Compliance focus | Learning and guidance focus |
| Big-bang rollout | Incremental, context-by-context adoption |

### Compared to Code Review Comments

| Ad-hoc Review | Systematic Linguistic Review |
|---------------|----------------------------|
| Subjective, reviewer-dependent | Evidence-based with glossary reference |
| Lost after merge | Contributes to glossary evolution |
| No trend analysis | Drift patterns visible over time |
| No enforcement consistency | Tiered enforcement with rationale |

---

## 9. Open Questions for Research Phase

The research phase must address:

1. **Feasibility:** What tools/techniques enable continuous capture at acceptable cost?
2. **Boundaries:** How do we detect context boundaries from linguistic evidence alone?
3. **Privacy:** What anonymization techniques preserve semantic value while protecting individuals?
4. **Sociolinguistics:** How do we distinguish normal register variation from problematic drift?
5. **Feedback Timing:** What belongs in PR review vs. periodic retrospectives?
6. **Success Metrics:** What leading indicators predict semantic drift before architectural impact?

---

## 10. Next Steps

### For Research Phase

1. **Curate source materials** - reading notes from DDD, Team Topologies, Conway's Law
2. **Build concept map** - visualize relationships between key ideas
3. **Draft primers** - synthesize core concepts into readable summaries
4. **Identify tools** - evaluate Contextive, semantic analysis libraries, LLM tooling

### For Pilot Phase (If Research Succeeds)

1. **Select bounded context** - start small, well-understood domain
2. **Bootstrap glossary** - extract 20-30 core terms manually
3. **Configure tooling** - set up Contextive, PR review agent
4. **Run first cycle** - observe, refine, iterate
5. **Measure outcomes** - track metrics, gather feedback

---

## Conclusion

This experiment treats language as **infrastructure**—fragile, political, and deeply architectural. Agentic systems do not solve linguistic conflict. They make it **explicit, contextual, and governable** with humans in charge.

The hypothesis: making semantic drift visible enables architectural conversations that would otherwise remain implicit and corrosive.

**The experiment stands or falls on intellectual honesty:** acknowledge that semantic conflict is normal, treat bounded contexts as containment strategy, and keep humans accountable for meaning.

That alone may justify the effort.

---

## References

- **Experiment Structure:** [README.md](./README.md)
- **Conceptual Framing:** [concept.md](./concept.md)
- **Research Guidance:** [research-guidance.md](./research-guidance.md)
- **Related ADRs:** ADR-017 (Traceable Decisions), ADR-012 (Test-Driven Defaults), ADR-008 (File-Based Coordination)
- **Framework Context:** [Doctrine Stack](../../../../doctrine/DOCTRINE_STACK.md), [Agent Glossary](../../../../doctrine/GLOSSARY.md)
