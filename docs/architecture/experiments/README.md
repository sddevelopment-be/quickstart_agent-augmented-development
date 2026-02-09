# Architectural Experiments

**Purpose:** Active architectural experiments conducted before formalization into ADRs and design documents.

**Status:** Living directory for in-progress research and validation work.

---

## What Belongs Here

Structured architectural experiments that:
- Have explicit hypothesis and success criteria
- Follow defined research/validation phases
- Produce artifacts that inform architectural decisions
- May succeed, fail, or pivot based on evidence

**Examples:**
- New architectural approaches requiring validation
- Linguistic or semantic analysis experiments
- Novel patterns or practices needing proof-of-concept
- Tooling or process experiments with architectural impact

---

## What Does Not Belong Here

- Casual brainstorming (use `tmp/ideas/` or `work/notes/`)
- Finalized architectural decisions (move to `docs/architecture/adrs/`)
- Production designs (move to `docs/architecture/design/`)
- Implementation details (move to `docs/architecture/implementation/`)

---

## Experiment Lifecycle

```
tmp/ideas/          → Rough ideation (transient)
    ↓
experiments/        → Structured research (active, documented)
    ↓
adrs/              → Formalized decisions (accepted/rejected)
    ↓
design/            → Technical designs (if accepted)
    ↓
implementation/    → Implementation artifacts (if built)
```

---

## Experiment Structure (Recommended)

Each experiment should contain:

```
experiment-name/
├── README.md                    # Hypothesis, scope, success criteria
├── concept.md                   # Conceptual exploration and rationale
├── research-guidance.md         # Instructions for research phase (if applicable)
├── phase-X-name/                # Phase-specific artifacts
│   ├── deliverables/
│   └── work-logs/
└── outcomes/                    # Final reports and ADR drafts
    ├── outcome-report.md
    └── draft-adr-NNN.md
```

---

## Quality Gates

Every experiment must define:

1. **Hypothesis** — What are we testing?
2. **Success Criteria** — What outcomes indicate success?
3. **Failure Criteria** — What outcomes indicate we should stop?
4. **Decision Point** — When do we decide to formalize, iterate, or abandon?

**Gate Question:**
> What concrete architectural decisions will this experiment inform?

---

## Archive Policy

**Failed experiments are not deleted.** They are:
- Moved to `outcomes/` with outcome report explaining why
- Documented in `experiments/README.md` archive section below
- Referenced in future work to avoid repeating failed approaches

**Successful experiments:**
- Produce ADRs in `docs/architecture/adrs/`
- May produce design docs in `docs/architecture/design/`
- Outcomes summary captured in `experiments/README.md` archive section

---

## Active Experiments

### Ubiquitous Language & Linguistic Drift Detection

**Status:** Phase 0 - Research Planning  
**Started:** 2026-02-09  
**Hypothesis:** Language drift is a leading indicator of architectural drift; agentic systems can make this observable at low cost.  
**Location:** `ubiquitous-language/`

---

## Archived Experiments

_None yet._

---

## Related Documentation

- **ADRs:** `docs/architecture/adrs/` — Formalized architectural decisions
- **Design:** `docs/architecture/design/` — Technical design documents
- **Patterns:** `docs/architecture/patterns/` — Reusable architectural patterns
- **Assessments:** `docs/architecture/assessments/` — Architecture quality assessments
