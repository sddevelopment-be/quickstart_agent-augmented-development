# Dependency Direction Audit - Executive Summary

**Date:** 2026-02-11  
**Agent:** Curator Claire  
**Requester:** @stijn-dejongh  

---

## Quick Answer

✅ **YES** - Doctrine artifacts are pointing to local ADRs, violating dependency direction constraints.

---

## By The Numbers

| Category | Count |
|----------|-------|
| **Total Violations** | 114 |
| 🔴 Critical (Direct Dependencies) | 6 |
| 🟠 Moderate-High | 1 |
| 🟡 Moderate | 16 |
| 🟢 Low/Informational | 91 |

---

## Critical Violations (Immediate Action Required)

1. **Directive 023** - References ADR-023 as implementation basis (4 occurrences)
2. **Directive 034** - Uses ADR-028, ADR-032 as authoritative examples
3. **GLOSSARY.md** - Defines "Primer" relative to ADR-011
4. **Directive 019** - Cites ADR-002, ADR-003 in references section
5. **Directive 025 (Guardian)** - Circular dependency: references ADR-013, ADR-014 which define Guardian itself
6. **Directive 018** - Self-references ADR-017

---

## Additional Findings

- **23 Agent Profiles** - All reference "ADR-011 Primer Matrix" in boilerplate text
- **16 Directives** - Moderate violations in exception handling and context references
- **89 Templates/Approaches** - Use `${DOC_ROOT}/architecture/adrs/` pattern (intentional for portability)

---

## Deliverables

1. ✅ **Full Report:** `work/curator/2026-02-11-doctrine-dependency-violations-report.md`
2. ✅ **Validation Script:** `work/curator/validate-dependencies.sh` (functional, tested)
3. ⏳ **Remediation Plan:** Phased approach with 4 priorities
4. ⏳ **Prevention Strategy:** CI validation, pre-commit hooks, documentation

---

## Recommended Next Steps

### Immediate (Priority 1)
1. Review full report: `work/curator/2026-02-11-doctrine-dependency-violations-report.md`
2. Decide on remediation approach for 6 critical violations
3. Consider "Framework Decision" directory proposal (`doctrine/decisions/` with FD-NNN prefix)

### Short-term (Priority 2)
4. Fix moderate violations (exception handling, primer references)
5. Update all agent profile boilerplate

### Medium-term (Priority 3)
6. Implement validation script in CI pipeline
7. Add pre-commit hooks
8. Create dependency direction guide

---

## Key Insight: Bootstrap Problem

Several violations stem from **framework-level decisions** (ADR-011 Primers, ADR-013 Distribution, ADR-014 Guardian) that are currently treated as "local ADRs" but logically belong WITH the framework.

**Proposed Solution:** Create `doctrine/decisions/` for framework-level ADRs using "FD-NNN" prefix to distinguish from repository-local "ADR-NNN" decisions.

---

## Validation

Run the validation script:
```bash
bash work/curator/validate-dependencies.sh
```

Currently detects **60+ direct violations** (excluding templates/approaches with `${DOC_ROOT}`).

---

## Effort Estimate

| Phase | Priority | Hours |
|-------|----------|-------|
| Phase 1: Critical fixes | 1 | 4-6h |
| Phase 2: Moderate fixes | 2 | 2-3h |
| Phase 3: Prevention | 3 | 2-3h |
| Phase 4: Framework Decisions | 4 | 4-6h |
| **Total** | | **12-18h** |

---

## Questions for @stijn-dejongh

1. **Severity agreement:** Do you concur with the Critical/Moderate/Low classification?
2. **Framework Decisions:** Should we create `doctrine/decisions/` with FD-NNN prefix for framework-level ADRs?
3. **Remediation timing:** Immediate fix or schedule for next sprint?
4. **Validation enforcement:** Add to CI pipeline now or after remediation?

---

**Status:** ✅ Audit Complete  
**Next Owner:** @stijn-dejongh for review and prioritization  

---

*See full report for detailed analysis, violation-by-violation breakdown, and complete remediation strategy.*
