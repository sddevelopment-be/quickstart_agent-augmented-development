# Commit Message Guidelines: Phase Declarations

**Purpose:** Make phase progression visible in git history for spec-driven development workflows.

**Status:** Active | **Version:** 1.0.0 | **Created:** 2026-02-08 | **Author:** Curator Claire

---

## Standard Format

```
<type>(scope): Phase N - <description>

<body explaining what was accomplished>

Phase: N of 6 (<phase name>)
Specification: <spec-id> v<version>
Agent: <agent-name>
```

---

## Phase Names (Per Directive 034)

| Phase | Name | Primary Agent(s) |
|-------|------|------------------|
| 1 | Analysis | Analyst Annie |
| 2 | Architecture/Tech Design | Architect Alphonso |
| 3 | Planning | Planning Petra |
| 4 | Acceptance Test Implementation | Assigned (e.g., DevOps Danny) |
| 5 | Code Implementation | Assigned (e.g., DevOps Danny, Backend-Dev) |
| 6 | Review | Multiple (Alphonso, Gail, Claire) |

---

## Examples

### Phase 1 (Analysis)
```
docs(spec): Phase 1 - create SPEC-DIST-001 stub

Analyst Annie (Phase 1 of 6 - Analysis):

Created specification stub with:
- Problem statement and background
- Stakeholder requirements
- Doctrine→toolstack mapping matrix (137 lines)
- Open questions for architectural review

Phase: 1 of 6 (Analysis)
Specification: SPEC-DIST-001 v1.0.0
Agent: Analyst Annie
Hand-off: Architect Alphonso (Phase 2)
```

### Phase 2 (Architecture)
```
arch(review): Phase 2 - architectural review approved

Architect Alphonso (Phase 2 of 6 - Architecture):

Architectural review completed:
✅ Technical feasibility: HIGH
✅ Risk assessment: LOW-MEDIUM (all mitigated)
✅ Decision: Pure exporter approach (no symlinks)

Recommendation: Proceed to Phase 3 (Planning)

Phase: 2 of 6 (Architecture/Tech Design)
Specification: SPEC-DIST-001 v1.1.0
Agent: Architect Alphonso
Hand-off: Planning Petra (Phase 3)
```

### Phase 3 (Planning)
```
plan: Phase 3 - task breakdown and YAML files

Planning Petra (Phase 3 of 6 - Planning):

Task breakdown complete:
- 7 tasks identified (70min estimated)
- YAML files created for Phases 4-5
- Critical path: exporter updates → tests → validation

Phase: 3 of 6 (Planning)
Specification: SPEC-DIST-001 v1.1.0
Agent: Planning Petra
Hand-off: DevOps Danny (Phase 4 - Acceptance Tests)
```

### Phase 4 (Acceptance Tests)
```
test: Phase 4 - validation tests created (RED phase)

DevOps Danny (Phase 4 of 6 - Acceptance Tests):

Created validation tests:
- tests/integration/exporters/test_doctrine_exports.test.js
- 4 tests total: 2/4 failing (RED phase as expected)
- Tests verify exporters read from doctrine/

Phase: 4 of 6 (Acceptance Test Implementation)
Specification: SPEC-DIST-001 v1.1.0
Agent: DevOps Danny
ATDD: Red phase confirmed ✅
Hand-off: DevOps Danny continues (Phase 5 - Implementation)
```

### Phase 5 (Implementation)
```
feat: Phase 5 - exporters updated, tests passing (GREEN phase)

DevOps Danny (Phase 5 of 6 - Implementation):

Exporter updates:
- 3 files modified (opencode-exporter, deploy-skills, skills-exporter)
- All paths updated: .github/agents → doctrine/agents
- 5 symlinks removed

Test results:
✅ 4/4 tests passing (was 2/4 failing in Phase 4)
✅ ATDD green phase achieved

Phase: 5 of 6 (Code Implementation)
Specification: SPEC-DIST-001 v1.1.0
Agent: DevOps Danny
ATDD: Green phase confirmed ✅
Hand-off: Architect Alphonso + Framework Guardian Gail (Phase 6 - Review)
```

### Phase 6 (Review)
```
review: Phase 6 - all reviews approved

Phase 6 of 6 (Review):

Architecture Review (Architect Alphonso):
✅ Architecture compliance: PASS
✅ Specification conformance: 100% (8/8)

Standards Review (Framework Guardian Gail):
✅ Directive compliance: PASS
✅ Code quality: HIGH

Final Verdict: APPROVED FOR MERGE ✅

Phase: 6 of 6 (Review)
Specification: SPEC-DIST-001 v1.1.0
Agents: Architect Alphonso + Framework Guardian Gail
```

---

## When NOT to Use Phase Declarations

**Skip phase declarations for:**
- Bug fixes (use standard `fix:` type)
- Refactoring (use standard `refactor:` type)
- Documentation updates not part of spec cycle (use `docs:` type)
- Chores and maintenance (use `chore:` type)

**Only use phase declarations for:**
- Work following the 6-phase specification-driven development cycle (Directive 034)
- Multi-phase features requiring coordination between specialized agents

---

## Benefits

1. **Visibility:** Git history shows phase progression clearly
2. **Traceability:** Easy to find all commits related to specific phase
3. **Accountability:** Agent ownership explicit in commit message
4. **Audit Trail:** Hand-offs documented for process review
5. **Debug Aid:** When issues arise, can trace back to specific phase

---

## Related

- **Directive 034:** [Specification-Driven Development](../directives/034_spec_driven_development.md)
- **Phase Checkpoint Protocol:** [In Directive 034](../directives/034_spec_driven_development.md#phase-checkpoint-protocol)
- **Conventional Commits:** https://www.conventionalcommits.org/ (standard types: feat, fix, docs, etc.)

---

**Version:** 1.0.0  
**Status:** Active  
**Next Review:** After 5 full spec-driven cycles completed
