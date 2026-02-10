# Architecture Assessments

This directory contains strategic architecture assessments that evaluate system health from various perspectives.

---

## Active Assessments

### Strategic Linguistic Assessment (2026-02-10)

**Assessor:** Architect Alphonso  
**Approach:** Language-First Architecture  
**Status:** Complete  
**Health Score:** 65/100 (MODERATE)

**Purpose:**  
Analyze linguistic patterns in the codebase to identify hidden architectural concerns, bounded context boundaries, and vocabulary drift.

**Key Findings:**
- 🔴 Task polysemy across 3 contexts (HIGH risk - coupling concern)
- 🟡 Agent identity as technical jargon (MEDIUM - domain clarity issue)
- 🟡 Workflow vocabulary gap (MEDIUM - collaboration friction)
- 🟢 DDD theory-practice gap (LOW - documentation vs practice)

**Deliverables:**
- [Full Assessment](./strategic-linguistic-assessment-2026-02-10.md) (~36KB detailed analysis)
- [Executive Summary](./strategic-linguistic-assessment-EXECUTIVE-SUMMARY.md) (~6KB quick reference)
- [Draft ADR: Task Context Boundaries](../adrs/_drafts/ADR-XXX-task-context-boundary-definition.md)
- [Proposed Orchestration Glossary](../../.contextive/contexts/_proposed/orchestration.yml)

**Recommended Actions:**
- Week 1: ADR for Task boundaries, glossary additions (7 hours)
- Month 1: Context map, translation layer POC (24 hours)
- Quarter 1: Module refactoring, strategic alignment (52 hours)

**Next Review:** 2026-05-10 (quarterly cadence)

---

## Assessment Types

### 1. Linguistic Assessment

**Focus:** Terminology patterns, vocabulary consistency, ubiquitous language  
**Signals:** Polysemy, terminology gaps, fragmented understanding, deprecated terms  
**Approach:** Language-First Architecture  
**Frequency:** Quarterly or on-demand

**When to Run:**
- After major feature additions
- When onboarding friction increases
- Before architectural refactoring
- When cross-team misalignment appears

---

### 2. Structural Assessment

**Focus:** Module boundaries, dependency graphs, coupling metrics  
**Signals:** Circular dependencies, high coupling, unclear responsibilities  
**Approach:** Dependency analysis, Conway's Law evaluation  
**Frequency:** Semi-annually or pre-refactoring

**Status:** Not yet performed

---

### 3. Technical Debt Assessment

**Focus:** Code quality, duplication, anti-patterns, maintenance burden  
**Signals:** Bug clusters, slow delivery, refactoring paralysis  
**Approach:** Static analysis, defect correlation, developer surveys  
**Frequency:** Quarterly

**Status:** Partial (ADR-042 addresses task I/O duplication)

---

### 4. Performance Assessment

**Focus:** Latency, throughput, resource usage, scalability bottlenecks  
**Signals:** Slow endpoints, memory leaks, database N+1 queries  
**Approach:** Profiling, load testing, telemetry analysis  
**Frequency:** As needed (performance issues arise)

**Status:** Not yet performed

---

## Assessment Request Process

### When to Request an Assessment

✅ **Request assessment when:**
- Significant architectural decisions pending
- System behavior is unclear or unpredictable
- Team velocity decreasing
- Onboarding taking longer than expected
- Cross-team conflicts arising

⚠️ **Consider deferring when:**
- System is stable and team is productive
- Immediate fires requiring attention
- Assessment results unlikely to change decisions
- Team bandwidth is severely constrained

---

### How to Request

1. **Create task in work/inbox/**
   ```yaml
   id: YYYY-MM-DDThhmm-architect-assessment-type
   title: "<Assessment Type> Assessment"
   agent: architect-alphonso
   priority: medium
   description: |
     Perform <assessment type> to evaluate <specific concern>.
     Context: <why now, what decisions depend on this>
   ```

2. **Specify scope:**
   - What areas to focus on?
   - What decisions are pending?
   - What's the urgency/priority?
   - Who needs the results?

3. **Define deliverables:**
   - Full assessment document?
   - Executive summary?
   - Draft ADRs?
   - Recommendations with effort estimates?

---

## Reading an Assessment

### For Leadership (Executive Summary)

**Read:**
- Health Score and Key Findings
- Investment Summary (time/effort)
- Recommended Actions (prioritized)
- Risk Assessment (if not addressed)

**Skip:**
- Detailed linguistic analysis
- Technical implementation details
- Methodology sections

**Time:** 10-15 minutes

---

### For Architects (Full Assessment)

**Read:**
- All sections
- Architectural insights
- Cross-context analysis
- Detailed recommendations
- Implementation strategies

**Skip:**
- Nothing (comprehensive review recommended)

**Time:** 45-60 minutes

---

### For Developers (Relevant Sections)

**Read:**
- Executive Summary (context)
- Sections relevant to your work area
- Specific recommendations for your domain
- Proposed glossary entries

**Skip:**
- Strategic/organizational analysis
- Other domain-specific sections

**Time:** 15-30 minutes

---

## Assessment Artifacts

Each assessment produces:

1. **Main Assessment Document**
   - Comprehensive analysis
   - Detailed findings
   - Architectural insights
   - Full recommendations

2. **Executive Summary**
   - Quick overview
   - Key findings
   - Investment summary
   - Action items

3. **Supporting Artifacts** (as needed)
   - Draft ADRs
   - Glossary proposals
   - Context maps
   - Diagrams

4. **Work Log**
   - Methodology details
   - Time tracking
   - Handoff notes

---

## Integration with Doctrine

**Related Approaches:**
- [Language-First Architecture](../../../doctrine/approaches/language-first-architecture.md)
- [Living Glossary Practice](../../../doctrine/approaches/living-glossary-practice.md)
- [Bounded Context Linguistic Discovery](../../../doctrine/approaches/bounded-context-linguistic-discovery.md)

**Related Directives:**
- Directive 018: Traceable Decisions
- Directive 022: Audience-Oriented Writing
- Directive 001: CLI Shell Tooling

**Related Tactics:**
- Terminology Extraction and Mapping
- Context Boundary Inference
- Documentation Curation Audit

---

## Assessment Schedule

| Assessment Type | Frequency | Last Run | Next Run | Owner |
|-----------------|-----------|----------|----------|-------|
| Linguistic | Quarterly | 2026-02-10 | 2026-05-10 | Architect Alphonso |
| Structural | Semi-annual | Not yet | TBD | Architect Alphonso |
| Technical Debt | Quarterly | Partial | 2026-04-01 | Python Pedro |
| Performance | As-needed | Not yet | As-needed | Backend Benny |

---

## Questions?

Contact:
- **Architect Alphonso** - Strategic assessments, bounded contexts
- **Python Pedro** - Technical debt, code quality
- **Backend Benny** - Performance, scalability
- **Manager Mike** - Assessment prioritization, resource allocation

---

_This directory follows assessment best practices from language-first-architecture.md and traceable-decisions.md._
