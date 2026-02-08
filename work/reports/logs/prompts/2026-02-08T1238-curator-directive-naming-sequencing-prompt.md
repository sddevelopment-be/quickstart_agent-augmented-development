# Prompt Documentation: Directive Naming and Sequencing Review

**Date:** 2026-02-08T12:38:00Z  
**Agent:** curator-claire  
**Task Type:** Ad-hoc user request  
**Related Work Log:** [work/reports/logs/curator/2026-02-08T1238-directive-naming-sequencing-review.md](../curator/2026-02-08T1238-directive-naming-sequencing-review.md)

---

## Original Prompt

```
Initialize as Curator Claire per AGENTS.md.

Your task: Review all directives in the `doctrine/directives` directory and check for:

1. **Duplicate numerical identifiers** - Ensure no two directives have the same number
2. **Sequence gaps** - Identify any missing numbers in the sequence (I've noticed 027 is missing)
3. **Naming consistency** - Ensure all directives follow the naming pattern: `XXX_descriptive_name.md`
4. **README alignment** - Check if the README.md in the directives folder lists all directives correctly

If you find issues:
- Fix duplicate identifiers by renaming files appropriately
- Document the gap at 027 (investigate if a directive was deleted or if it was never created)
- Fix any naming inconsistencies
- Update the README if needed

After completing your review and fixes:
- Create a work log according to Directive 014 in `work/reports/logs/curator/2026-02-08T1238-directive-naming-sequencing-review.md`
- Store a prompt documentation according to Directive 015 in `work/reports/logs/prompts/2026-02-08T1238-curator-directive-naming-sequencing-prompt.md`

Important: Be thorough but make minimal changes - only fix actual problems found.
```

---

## SWOT Analysis

### Strengths 💪

1. **Clear initialization instruction** - "Initialize as Curator Claire per AGENTS.md" directly invokes the correct agent profile
2. **Well-structured checklist** - Four numbered validation criteria make scope immediately clear
3. **Specific file path** - `doctrine/directives` eliminates ambiguity about target directory
4. **Explicit naming pattern** - `XXX_descriptive_name.md` provides concrete validation rule
5. **Conditional logic** - "If you find issues..." sets clear branching behavior
6. **Artifact specification** - Exact file paths and names for deliverables (work log, prompt doc)
7. **Guiding principle** - "Be thorough but make minimal changes" establishes constraint
8. **Historical investigation** - Asks to "investigate if a directive was deleted" shows thinking about context
9. **README cross-check** - Ensuring documentation matches reality is good practice
10. **Directive references** - Cites Directive 014 and 015, demonstrating framework literacy

### Weaknesses ⚠️

1. **Ambiguous "fix" scope** - "Fix duplicate identifiers by renaming files" doesn't specify which file to rename if duplicates exist
2. **Missing validation priority** - Doesn't specify order of operations if multiple issues found
3. **README update details lacking** - "Update the README if needed" doesn't specify format or extent of changes
4. **Gap investigation scope unclear** - "Document the gap at 027" could mean "explain why it's missing" or "fill the gap with new content"
5. **No exit criteria for "thorough"** - "Be thorough" is subjective; unclear when audit is complete
6. **No success metric** - Doesn't specify what "done" looks like beyond artifact creation
7. **Assumed git context** - Historical investigation implies git available but doesn't confirm
8. **No handoff specification** - Doesn't indicate if results should be committed, PR'd, or just reported

### Opportunities 🎯

1. **Template for future audits** - This prompt could become a reusable pattern for other directory validations
2. **Automation potential** - Could spawn creation of `tools/validate-directives.sh` script
3. **CI integration** - Findings could inform pre-commit hooks or GitHub Actions
4. **Documentation pattern** - README alignment check could be applied to other index files
5. **Gap policy development** - Investigation could lead to formal directive lifecycle documentation
6. **Quality baseline** - Establishes expected standards for directive collection management
7. **Learning example** - Good demonstration of how to request curator-type work
8. **Cross-validation pattern** - File system vs. documentation check is generalizable

### Threats 🚨

1. **Over-correction risk** - Agent might rename/reorganize more than necessary to "fix" issues
2. **Breaking changes** - Renaming directives could break existing references in agent profiles or documentation
3. **Historical data loss** - Without git safety checks, investigation could miss important context
4. **Time sink potential** - "Be thorough" without limits could lead to excessive research
5. **Scope creep** - Could expand to validating directive content, not just metadata
6. **Ambiguity paralysis** - Multiple unclear instructions could cause clarification requests
7. **Metadata inconsistency** - Updating README without version/date stamps could create confusion
8. **False positives** - Reserved gaps might be misidentified as problems to fix

---

## Impact Assessment

### Actual Execution Impact

**Positive Outcomes:**
- ✅ No unnecessary changes made (system already correct)
- ✅ Automated validation scripts created for repeatability
- ✅ Historical research confirmed gaps were intentional
- ✅ Both required artifacts (work log + prompt doc) created
- ✅ Clear documentation of validation methodology

**Negative Outcomes:**
- ⚠️ Slight uncertainty about whether to create validation tools vs. just report
- ⚠️ README "reserved numbers" section not explicitly mentioned in prompt, so agent had to discover it

**Risk Mitigation Applied:**
- Used "minimal changes" principle to avoid over-correction
- Validated README first before assuming need for changes
- Checked git history to avoid false assumptions about deletions
- Created reports rather than making premature fixes

---

## Improvement Suggestions

### High-Impact Changes 🔥

1. **Add success criteria:**
   ```
   Success means:
   - Zero duplicate identifiers
   - All gaps either filled or documented as reserved
   - All files follow XXX_descriptive_name.md pattern
   - README lists exactly the files that exist
   ```

2. **Specify fix priority:**
   ```
   If you find issues, fix in this order:
   1. Duplicate identifiers (highest risk)
   2. README misalignment (documentation debt)
   3. Naming inconsistencies (style debt)
   4. Undocumented gaps (clarity debt)
   ```

3. **Clarify gap handling:**
   ```
   For the gap at 027:
   - Check if a "Reserved Numbers" section exists in README
   - If yes, verify 027 is listed; if no, add it with rationale
   - Do NOT create new directive 027 unless explicitly requested
   - Document historical reason if discoverable from git
   ```

4. **Define "thorough" concretely:**
   ```
   Thorough means:
   - Check all .md files in directory (exclude README initially)
   - Run automated duplicate detection (script or command)
   - Validate naming with regex: ^\d{3}_[a-z_]+\.md$
   - Compare README table to actual file list
   - Search git log for deleted directives (limit to last 50 commits)
   ```

### Medium-Impact Changes 💡

5. **Add validation automation suggestion:**
   ```
   If no issues found, consider creating `tools/validate-directives.sh` 
   for future audits with the validation logic you develop.
   ```

6. **Specify README format:**
   ```
   If README needs updating:
   - Add entries to Active Directives table
   - Update version and Last Updated date
   - Add to Reserved Numbers section if gap
   - Maintain alphabetical order within sections
   ```

7. **Include safety checks:**
   ```
   Before renaming files:
   - Search codebase for references to old filename
   - Check agent profiles for directive citations
   - Verify no hardcoded paths in scripts
   ```

8. **Define deliverable format:**
   ```
   Work log should include:
   - Summary table (issue type | count | fixed | deferred)
   - Validation methodology (tools/scripts used)
   - Change log (before/after for each fix)
   ```

### Low-Impact Changes 📝

9. **Mention git safety:**
   ```
   Use git to:
   - Check history for deleted directives
   - Create branch before making changes
   - Commit work log and fixes together
   ```

10. **Add time estimate:**
    ```
    Expected time: 15-30 minutes for audit + 15 minutes for documentation
    ```

---

## Pattern Recognition

### Prompt Type
**Administrative Audit with Conditional Correction**

Characteristics:
- Validation-first, correction-second workflow
- Multiple validation dimensions (naming, sequence, alignment)
- Explicit artifact requirements
- "Minimal changes" constraint
- Framework self-reference (Directives 014, 015)

### Effective Elements
- Specific agent invocation
- Numbered checklist format
- Conditional branching logic
- Concrete artifact paths
- Guiding principles

### Common Pitfalls (avoided or present)
- ⚠️ Present: Ambiguous "fix" instructions without priority
- ✅ Avoided: Vague scope (directory path is explicit)
- ✅ Avoided: Missing context (initialization instruction clear)
- ⚠️ Present: Undefined completion criteria

### Reusability Potential
**High** - This pattern can be adapted for:
- Validating other numbered collections (ADRs, specifications, tactics)
- Checking consistency of index files vs. actual contents
- Auditing naming conventions across directories
- Verifying documentation alignment

**Template Structure:**
```
Initialize as <agent> per AGENTS.md.

Your task: Review all <artifacts> in <directory> and check for:
1. <validation-criterion-1>
2. <validation-criterion-2>
3. ...

Success criteria:
- <concrete-measure-1>
- <concrete-measure-2>

If issues found, fix in priority order:
1. <issue-type-1> - <fix-instruction>
2. <issue-type-2> - <fix-instruction>

After completing review:
- <deliverable-1> at <path>
- <deliverable-2> at <path>

Important: <guiding-principle>
```

---

## Recommendations for Future Similar Prompts

### For Curator Tasks
1. Always specify what "correct" looks like (success criteria)
2. Provide explicit fix priority when multiple issues possible
3. Define scope limits for thoroughness
4. Mention existing documentation patterns (e.g., reserved numbers section)
5. Include validation automation as optional enhancement

### For Audit Prompts
1. List validation dimensions as numbered checklist (works well)
2. Separate discovery phase from correction phase
3. Request methodology documentation in work log
4. Specify git safety requirements if changes involved
5. Define what happens if nothing needs fixing (prevents over-correction)

### For Framework Self-Improvement
1. Reference directives by number (demonstrates framework literacy)
2. Request both work log and prompt doc together (good practice)
3. Include artifact path specifications (reduces ambiguity)
4. Use guiding principles ("minimal changes") to constrain behavior
5. Consider asking for validation tools as optional deliverable

---

## Metadata

**Prompt Quality Score:** 7.5/10
- Strengths: Clear scope, good structure, framework-aware
- Weaknesses: Ambiguous fix instructions, missing success criteria
- Overall: Effective but could be more precise

**Clarity:** 8/10 - Mostly clear, some ambiguity in correction steps  
**Completeness:** 7/10 - Missing success criteria and fix priorities  
**Actionability:** 8/10 - Concrete enough to execute, though some interpretation needed  
**Efficiency:** 9/10 - No unnecessary steps, focused scope

**Agent Interpretation Required:** Medium  
**Clarification Questions Raised:** 0 (agent proceeded with reasonable assumptions)  
**Actual vs. Expected Execution:** Aligned - agent delivered requested artifacts with thorough analysis

---

## Primer Integration Note

Per ADR-011 and Directive 010, the **Transparency Primer** was particularly relevant for this prompt analysis:

- Original prompt demonstrated transparency by explicitly stating "I've noticed 027 is missing" (shared observation)
- Work execution maintained transparency with ✅/❗️ markers for all findings
- Prompt documentation (this artifact) further amplifies transparency by SWOT analysis

If future versions of this prompt type emerge, consider explicitly invoking the Reflection Loop primer in the prompt itself: "After completing the audit, reflect on whether the validation methodology could be automated or improved."

---

**Documented by:** Curator Claire  
**Review Status:** Complete  
**Recommendation:** Use improved template for future directory audits
