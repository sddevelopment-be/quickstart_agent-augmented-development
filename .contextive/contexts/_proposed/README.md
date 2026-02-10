# Proposed Glossary Additions

**Status:** DRAFT  
**Created:** 2026-02-10  
**Source:** Strategic Linguistic Assessment  
**Approval Required:** Yes (Curator Claire + Architecture Team)

---

## Purpose

This directory contains **proposed additions** to the living glossary, generated from the Strategic Linguistic Assessment (2026-02-10). These glossaries document vocabulary that is **already in use** in the codebase but not yet formally defined in the glossary infrastructure.

---

## Files in This Directory

### `orchestration.yml`

**Context:** Orchestration Domain  
**Terms:** 24 operational vocabulary terms  
**Status:** Proposed  
**Priority:** HIGH

**Scope:**
- File-based coordination patterns (TaskDescriptor, Work Directory, Agent Queue)
- Task lifecycle states (Inbox, Assigned, Done, Error, Blocked)
- Anti-Corruption Layer vocabulary (Parser, Serializer)
- Orchestration operations (Persist, Load, Assignment, Completion)

**Rationale:**
The Strategic Linguistic Assessment identified that operational vocabulary (how tasks are persisted, coordinated, and executed) is **absent from the current glossary**, despite being extensively used in code. This glossary documents that vocabulary to:

1. ✅ Support IDE integration (Contextive plugin)
2. ✅ Clarify bounded context boundaries
3. ✅ Enable onboarding and knowledge transfer
4. ✅ Provide translation layer semantics

---

## Approval Process

Per `doctrine/approaches/living-glossary-practice.md`:

### 1. Review Phase (Week 1)

**Owners:** Curator Claire, Architect Alphonso

**Checklist:**
- [ ] Verify all terms are already in use in codebase
- [ ] Check for conflicts with existing glossary entries
- [ ] Validate context boundaries are clear
- [ ] Ensure definitions are precise and actionable

---

### 2. Team Review (Week 2)

**Reviewers:** Python Pedro, Backend Benny, Frontend Freddy

**Feedback Required:**
- Are definitions clear and accurate?
- Any missing terms that should be included?
- Any terminology conflicts with current usage?
- Implementation references correct?

---

### 3. Approval (Week 3)

**Decision Maker:** Architect Alphonso (context owner)

**Approval Criteria:**
- [ ] No unresolved conflicts with existing glossary
- [ ] Definitions align with current code usage
- [ ] Context boundaries clearly documented
- [ ] Team consensus on terminology choices

---

### 4. Integration (Week 3-4)

**Actions:**
1. Move approved glossary from `_proposed/` to `contexts/`
2. Update `.contextive/definitions.yml` with new context
3. Configure IDE plugin to load new glossary
4. Update related ADRs with glossary references
5. Announce to team via collaboration channels

---

## Enhancement Requests

If you'd like to **add**, **modify**, or **remove** terms from proposed glossaries:

1. Open PR with changes to the file in `_proposed/`
2. Tag `@curator-claire` and `@architect-alphonso` for review
3. Explain rationale in PR description
4. Reference code locations where term is used

---

## Related Documents

- **Strategic Linguistic Assessment:** `docs/architecture/assessments/strategic-linguistic-assessment-2026-02-10.md`
- **Living Glossary Practice:** `doctrine/approaches/living-glossary-practice.md`
- **Language-First Architecture:** `doctrine/approaches/language-first-architecture.md`
- **Draft ADR:** `docs/architecture/adrs/_drafts/ADR-XXX-task-context-boundary-definition.md`

---

## Future Proposed Glossaries

Based on Strategic Linguistic Assessment recommendations:

### `task-domain.yml` (Priority: HIGH)
- TaskAggregate, Lifecycle, Transition, Invariant
- Domain-specific state machine vocabulary
- Business rule enforcement terms

### `collaboration.yml` (Priority: MEDIUM)
- WorkItem, Handoff, Delegation, Coordination Event
- Agent assignment patterns
- Multi-agent synchronization vocabulary

### `dashboard.yml` (Priority: LOW)
- UI/presentation layer vocabulary
- Telemetry and observability terms
- Initiative and specification tracking

---

## Status Tracking

| Glossary | Status | Approval Date | Reviewer Comments |
|----------|--------|---------------|-------------------|
| `orchestration.yml` | 📝 Draft | Pending | Awaiting review |
| `task-domain.yml` | ⏳ Not Started | - | - |
| `collaboration.yml` | ⏳ Not Started | - | - |
| `dashboard.yml` | ⏳ Not Started | - | - |

---

## Questions?

Contact:
- **Curator Claire** - Glossary maintenance and curation
- **Architect Alphonso** - Bounded context and vocabulary decisions
- **Lexical Larry** - Terminology consistency validation

---

_This directory structure follows living-glossary-practice.md governance model with human-in-charge decision authority._
