# Glossary Curation Plan: Batch 1-4 Integration

**Date:** 2026-02-10  
**Agent:** Curator Claire  
**Task:** Integrate 475 candidate terms into doctrine/GLOSSARY.md  
**Mode:** /analysis-mode (structural validation and consistency)

---

## Situation Analysis

### Current State
- **Existing glossary:** 64 terms in doctrine/GLOSSARY.md (416 lines)
- **Candidate terms:** 475 terms across 4 batches
  - Batch 1 (Directives): 99 terms, 75% high-confidence
  - Batch 2 (Approaches): 129 terms, 69% high-confidence
  - Batch 3 (Tactics): 127 terms, 75% high-confidence
  - Batch 4 (Agents): 120 terms, 100% high-confidence
- **Total after integration:** ~440-445 terms (accounting for duplicates)

### Source Files
- **Batch summaries:** work/glossary-candidates/batch{1,2,3,4}-*-extraction-summary.md
- **YAML candidates:** work/glossary-candidates/batch{1,2,3,4}-*-candidates.yaml
- **Integration plan:** work/glossary-candidates/batch1-4-complete-integration-plan.md
- **Living Glossary Practice:** doctrine/approaches/living-glossary-practice.md

---

## Approach

Given the scale (475 terms), I will work systematically:

### Phase 1: Load and Parse All Candidate Terms
1. Extract all terms from batch summary markdown files
2. Load YAML candidate files for structured data
3. Create master term list with batch provenance

### Phase 2: Deduplication Analysis
1. Check existing 64 terms against candidates
2. Identify overlaps across batches (estimated 30-40 terms)
3. Create merge strategy for duplicates
4. Priority: preserve existing terms, enhance with new context

### Phase 3: Term Consolidation
1. Merge duplicate definitions (combine context from all sources)
2. Resolve conflicts (select canonical definition + usage notes)
3. Enhance cross-references
4. Add source citations

### Phase 4: Quality Assurance
1. Verify all terms have clear definitions
2. Check context specification
3. Validate related_terms bidirectional links
4. Ensure alphabetical ordering

### Phase 5: Integration
1. Create new GLOSSARY.md with all terms
2. Maintain existing structure (## Terms section)
3. Preserve metadata and usage guidelines
4. Update version and last updated date

### Phase 6: Documentation
1. Create curation summary report
2. Document decisions made
3. List terms added, merged, preserved
4. Provide recommendations

---

## Execution Strategy

Given the volume, I'll work in stages:

1. **Stage 1:** Parse all source files, create master term database
2. **Stage 2:** Identify and resolve duplicates (scripted analysis)
3. **Stage 3:** Generate consolidated GLOSSARY.md (automated with review)
4. **Stage 4:** Manual quality pass (structure, links, tone)
5. **Stage 5:** Generate final report

**Commit frequency:** After each major stage completion

---

## Risk Mitigation

**Risk:** File size may become unwieldy  
**Mitigation:** Keep definitions concise, use Related: for cross-refs

**Risk:** Alphabetical insertion errors  
**Mitigation:** Script-based alphabetization, validation pass

**Risk:** Tone/style drift with 475 new entries  
**Mitigation:** Apply existing glossary patterns, consistency review

**Risk:** Missing bidirectional links  
**Mitigation:** Automated cross-reference validation

---

## Next Steps

1. Create Python script to parse all batches
2. Build master term database with provenance
3. Run deduplication analysis
4. Generate initial consolidated glossary
5. Quality review and refinement
6. Final report generation

**Time Estimate:** 2-3 hours (systematic, scripted approach)

---

**Status:** ✅ Plan Complete - Ready to Execute
