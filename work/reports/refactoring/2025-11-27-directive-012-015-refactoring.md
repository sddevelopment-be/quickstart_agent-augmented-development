# Refactoring Notes: Directives 012 & 015 Token Optimization

**Date:** 2025-11-27  
**Agent:** Curator Claire  
**Task:** Refactor Directive 012 and 015 to improve token efficiency  
**Related Issue:** #[issue-number]  
**Parent Epic:** Housekeeping and Refactoring (#55)

## Summary

Extracted verbose operational procedure content from Directive 012 and 015 into modular approach files following the pattern established by Directive 019 refactoring. Achieved 54.4% token reduction overall while maintaining all behavioral guidance and references.

## Changes Made

### 1. Directive 015: Store Prompts (60.0% reduction)

**Before:** 1,498 words  
**After:** 599 words  
**Reduction:** 899 words (60.0%)

**Extracted Content:**
- Complete prompt documentation structure template → `agents/approaches/prompt_documentation/01_documentation_structure.md`
- SWOT analysis guidelines (Strengths, Weaknesses, Opportunities, Threats) → `agents/approaches/prompt_documentation/02_swot_analysis_guidelines.md`
- Improvement guidelines (version numbering, categories, impact assessment) → `agents/approaches/prompt_documentation/03_improvement_guidelines.md`
- Pattern recognition methodology (effective patterns, anti-patterns) → `agents/approaches/prompt_documentation/04_pattern_recognition.md`

**Retained in Directive:**
- When to store prompts (MAY/SHOULD criteria)
- File location and naming convention
- Quick procedure with approach references
- Integration with work logs
- Benefits and validation criteria

**New Structure:**
```
agents/approaches/prompt_documentation/
├── README.md (overview and approach steps)
├── 01_documentation_structure.md
├── 02_swot_analysis_guidelines.md
├── 03_improvement_guidelines.md
└── 04_pattern_recognition.md
```

### 2. Directive 012: Operating Procedures (36.0% reduction)

**Before:** 456 words  
**After:** 292 words  
**Reduction:** 164 words (36.0%)

**Extracted Content:**
- Redundancy rationale detailed explanation → `agents/approaches/operating_procedures/01_redundancy_rationale.md`
  - Cognitive priming explanation
  - Defense against partial context loss
  - Consistency across agent specializations
  - Validation and audit trail details
  - Recovery and rehydration mechanisms
  - Token cost justification analysis

**Retained in Directive:**
- Core behaviors (canonical list)
- Summary of redundancy rationale key points
- Non-removal clause (30% uncertainty rule)
- Usage guidelines

**New Structure:**
```
agents/approaches/operating_procedures/
├── README.md (overview and design context)
└── 01_redundancy_rationale.md
```

### 3. Supporting Changes

**Manifest Update:**
- Added Directive 019 (file_based_collaboration) to `manifest.json`
- Ensures validation scripts pass with all 19 directives

## Results

### Token Count Metrics

| Directive | Before | After | Reduction | Percentage |
|-----------|--------|-------|-----------|------------|
| 012       | 456    | 292   | 164       | 36.0%      |
| 015       | 1,498  | 599   | 899       | 60.0%      |
| **Total** | **1,954** | **891** | **1,063** | **54.4%** |

**Target Achieved:** 50%+ reduction ✓

### Validation

All validation scripts pass:
- ✅ Directive count matches (19)
- ✅ Directive numbering contiguous
- ✅ All headings correct
- ✅ Manifest entries valid
- ✅ AGENTS.md index complete
- ✅ Clarifying line present in all agent profiles

## Design Pattern Applied

Followed the Directive 019 refactoring pattern:

1. **Directive remains lightweight**: Core purpose, when to use, quick reference
2. **Approach provides depth**: Step-by-step procedures, detailed guidelines
3. **Token discipline**: Load only relevant approach steps as needed
4. **Cross-references**: Clear pointers from directive to approach files

## Benefits

### Token Efficiency
- **Context window savings**: 1,063 fewer words (~1,400 tokens estimated)
- **Selective loading**: Agents load only relevant approach steps
- **Scalability**: Pattern enables future directive refactoring

### Maintainability
- **Modular structure**: Updates isolated to specific approach files
- **Clear separation**: Directive = "what/when", Approach = "how/why"
- **Reusability**: Approach files can be referenced from multiple contexts

### User Experience
- **Faster directive scanning**: Core information immediately visible
- **Deep-dive available**: Detailed guidance accessible when needed
- **Consistent pattern**: Same structure across refactored directives

## Migration Guide

### For Agents Currently Using These Directives

**Directive 012 (Operating Procedures):**
- Core behaviors unchanged
- If you need detailed redundancy rationale, load: `agents/approaches/operating_procedures/01_redundancy_rationale.md`
- 30% uncertainty rule still present in directive

**Directive 015 (Store Prompts):**
- When to document criteria unchanged
- For documentation structure: load `agents/approaches/prompt_documentation/01_documentation_structure.md`
- For SWOT analysis: load `agents/approaches/prompt_documentation/02_swot_analysis_guidelines.md`
- For improvements: load `agents/approaches/prompt_documentation/03_improvement_guidelines.md`
- For patterns: load `agents/approaches/prompt_documentation/04_pattern_recognition.md`

### For Framework Maintainers

**No breaking changes:**
- All behavioral norms preserved
- Cross-references clearly documented
- Validation scripts updated and passing

**Future refactoring:**
- Apply same pattern to other verbose directives
- Target directives with >500 words for similar treatment
- Maintain 50%+ reduction goal

## Files Changed

### Created (9 files)
1. `agents/approaches/operating_procedures/README.md`
2. `agents/approaches/operating_procedures/01_redundancy_rationale.md`
3. `agents/approaches/prompt_documentation/README.md`
4. `agents/approaches/prompt_documentation/01_documentation_structure.md`
5. `agents/approaches/prompt_documentation/02_swot_analysis_guidelines.md`
6. `agents/approaches/prompt_documentation/03_improvement_guidelines.md`
7. `agents/approaches/prompt_documentation/04_pattern_recognition.md`
8. `work/reports/refactoring/2025-11-27-directive-012-015-refactoring.md` (this file)

### Modified (3 files)
1. `.github/agents/directives/012_operating_procedures.md`
2. `.github/agents/directives/015_store_prompts.md`
3. `.github/agents/directives/manifest.json`

## Testing

### Validation Scripts
- ✅ `validation/validate_directives.sh` - All checks pass
- ✅ All 19 directives validated
- ✅ Manifest consistency confirmed

### Manual Verification
- ✅ All cross-references resolve correctly
- ✅ Approach files exist at referenced paths
- ✅ No broken links or missing content
- ✅ Behavioral norms preserved in directives

## Recommendations

### Immediate
1. Update agent initialization to reference new approach structure
2. Communicate pattern to team for consistency
3. Monitor token usage in practice

### Future Refactoring Candidates
Based on word count, consider similar treatment for:
- Directive 001: CLI & Shell Tooling (if verbose)
- Directive 009: Role Capabilities (if verbose)
- Directive 016: Acceptance Test Driven Development (if verbose)
- Directive 017: Test Driven Development (if verbose)

### Pattern Evolution
- Consider creating approach file templates
- Document approach creation guidelines
- Build tooling for semi-automated extraction

## Conclusion

Successfully refactored Directives 012 and 015, achieving 54.4% token reduction while maintaining all behavioral guidance. The modular approach structure improves token efficiency, maintainability, and scalability. Pattern is now validated across three directives (012, 015, 019) and ready for broader application.

---

**Refactoring Completed By:** Curator Claire  
**Date:** 2025-11-27  
**Status:** Complete  
**Validation:** Passed
