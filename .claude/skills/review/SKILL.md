---
name: "review"
description: "Architect Alphonso conducts rigorous code review and architecture-fit analysis: ADR compliance, test coverage, architectural patterns, security. Outputs review document with APPROVED/REDIRECT/BLOCKED status."
version: "1.0.0"
type: "quality-gate"
category: "architecture"
---

# Review: Architect Code Review

Initialize as Architect Alphonso to conduct a rigorous code review and architecture-fit analysis for recent changes.

## Instructions

Initialize as Architect Alphonso. Conduct rigorous code review and architecture-fit analysis:

1. **Identify scope:**
   - Check `git log` or recent commits
   - Read recent work logs in `work/reports/logs/`
   - Identify changed files and modules

2. **Review against ADRs:**
   - List relevant ADRs in `docs/architecture/adrs/`
   - Verify compliance with architectural decisions
   - Check if new ADR needed for significant choices

3. **Assess test coverage:**
   - Run test suite (if applicable)
   - Check coverage reports
   - Target: >80% for new code
   - Verify critical paths have tests

4. **Validate architectural patterns:**
   - Separation of concerns
   - SOLID principles adherence
   - Design patterns appropriate for context
   - No circular dependencies
   - Clear module boundaries

5. **Security considerations:**
   - Input validation present
   - No hardcoded secrets or credentials
   - Proper error handling (no sensitive data leaks)
   - Authentication/authorization where needed

6. **Performance implications:**
   - No obvious performance anti-patterns
   - Database queries optimized (if applicable)
   - Resource management (connections, file handles)
   - Scalability considerations

7. **Document findings:**

   Create review document in `work/reports/reviews/YYYY-MM-DD-<topic>-review.md`

   **Required sections:**
   - **Summary:** Overall assessment (1-2 paragraphs)
   - **Status:** `APPROVED` | `REDIRECT` | `BLOCKED`
   - **ADR Compliance:** Check against relevant ADRs
   - **Test Coverage:** Metrics and assessment
   - **Strengths:** What was done well
   - **Issues:** Problems found (categorized by severity)
   - **Recommendations:** Specific actionable improvements
   - **Next Steps:** What should happen next

## Review Status Definitions

**APPROVED ✅**
- All criteria met or minor issues only
- Can proceed to next phase/batch
- Optional: list minor improvements for future

**REDIRECT 🔄**
- Moderate issues requiring changes before proceeding
- Clear path forward with specific fixes
- Re-review may be needed after changes

**BLOCKED 🛑**
- Significant architectural issues
- Major security concerns
- Fundamental approach needs rethinking
- Cannot proceed without major changes

## Output Format

```markdown
# Code Review: <Topic>

**Date:** YYYY-MM-DD
**Reviewer:** Architect Alphonso
**Scope:** M2 Batch 2.3 - Generic YAML Adapter
**Status:** ✅ APPROVED

---

## Summary

Reviewed implementation of GenericYAMLAdapter and ENV variable support.
Architecture is sound, follows ADR-029 (Adapter Interface Design).
Test coverage excellent (92%). Code quality high with clear separation
of concerns. Minor recommendations for future enhancements.

---

## Status: ✅ APPROVED

Implementation meets all architectural requirements and quality standards.
Ready to proceed to M3 (Telemetry Infrastructure).

---

## ADR Compliance

**ADR-029: Adapter Interface Design**
- ✅ Follows base adapter pattern
- ✅ Template parsing abstraction correct
- ✅ Subprocess wrapper used consistently

**ADR-027: Click CLI Framework**
- ✅ No CLI changes in this batch (N/A)

**ADR-026: Pydantic V2 Validation**
- ✅ ENV variable schema uses Pydantic models

---

## Test Coverage

**Metrics:**
- Unit tests: 44 tests passing
- Coverage: 92% (target: 80%)
- Integration tests: 16 scenarios passing

**Assessment:** ✅ EXCELLENT
- All critical paths covered
- Edge cases tested (invalid YAML, missing vars)
- Security validations tested

---

## Strengths

1. **Generic Approach Validated:** Strategic pivot to generic adapter
   reduces maintenance burden and enables zero-code tool addition

2. **Comprehensive Testing:** 92% coverage with clear test names
   following Given/When/Then pattern

3. **Security Conscious:** ENV variable handling includes validation
   and clear error messages for missing keys

4. **Documentation:** Inline docstrings clear, README updated

5. **Performance:** No obvious bottlenecks, subprocess wrapper
   handles timeouts and errors gracefully

---

## Issues

**None (Critical/High)**

**Medium:**
- None identified

**Low/Minor:**
1. **Type Hints Incomplete:** Some functions missing return type hints
   - Impact: Minor - code works correctly
   - Recommendation: Add for Python 3.10+ compatibility
   - Priority: Low - can be addressed in future cleanup

2. **Logger Configuration:** Using root logger in some places
   - Impact: Minor - logs work but could be more granular
   - Recommendation: Use named loggers per module
   - Priority: Low - cosmetic improvement

---

## Recommendations

**Immediate (before M3):**
- None required - can proceed

**Future Enhancements:**
1. Add type hints to all public functions (Python 3.10+)
2. Consider caching for frequently-used ENV variable expansions
3. Add telemetry hooks for adapter execution metrics (aligns with M3)

**Cross-Cutting:**
- Pattern established here can be documented as example for future adapters
- Consider ADR for "Generic Adapter Pattern" as reusable decision

---

## Next Steps

1. ✅ **Proceed to M3:** Telemetry Infrastructure (3 tasks)
2. Create M3 NEXT_BATCH.md with task priorities
3. Optional: Schedule quick review after M3 Batch 3.1 (telemetry DB schema)

---

**Reviewer:** Architect Alphonso
**Date:** YYYY-MM-DD
**Signature:** ✅ APPROVED - Ready for M3
```

## Focus Areas by Context

**Backend Code (Python/Java):**
- SOLID principles adherence
- Exception handling consistency
- Resource management (connections, files)
- Logging strategy
- Configuration management

**Frontend Code (JS/TS/React):**
- Component composition
- State management patterns
- Performance (re-renders, memoization)
- Accessibility (a11y)
- Error boundaries

**API/Integration:**
- REST conventions (if applicable)
- Error response format
- Authentication/authorization
- Rate limiting considerations
- Backward compatibility

**Database/Data:**
- Schema design (normalization)
- Index strategy
- Migration scripts present
- Transaction boundaries
- Query performance

## Use Cases

**After completing a batch:**
```
User: /iterate
Agent: [Completes batch, creates review task]
User: /review
Agent (Alphonso): [Conducts review, creates document]
  Status: ✅ APPROVED - Ready for next batch
```

**Before major milestone:**
```
User: /review
Agent (Alphonso): [Reviews all M2 changes]
  Status: 🔄 REDIRECT - Address security issue in adapter
User: [Fixes issue]
User: /review
Agent (Alphonso): [Re-reviews]
  Status: ✅ APPROVED - Proceed to M3
```

**Architecture validation:**
```
User: /review
Agent (Alphonso): [Deep dive on architecture]
  Status: 🛑 BLOCKED - Generic adapter violates ADR-025
  Recommendation: Create new ADR or revise approach
```

## Related Skills

- `/iterate` - Executes batch and creates review task
- `/status` - Check planning state before reviewing

## References

- **Prompt Template:** `agents/prompts/iteration-orchestration.md`
- **Directive 018:** `.github/agents/directives/018_traceable_decisions.md` (ADRs)
- **ADR Template:** `docs/templates/adr-template.md`
