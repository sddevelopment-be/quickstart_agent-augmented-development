# Prompt Template: Test Readability and Clarity Check

**Template Type:** Quality Validation  
**Version:** 1.0.0  
**Last Updated:** 2025-11-29  
**Approach Reference:** `.github/agents/approaches/test-readability-clarity-check.md`

---

## Purpose

This prompt template guides LLM agents through a dual-agent validation process to assess whether tests effectively document system behavior and identify documentation gaps.

---

## Template Structure

### Part 1: Initial Request (User to Agent)

```markdown
As an experiment, let's validate the quality of the test suite by means of a qualitative study.

**Phase 1: Initialize as Researcher Ralph (non-coding agent)**

Ralph is to describe what the various systems and modules do by looking ONLY at the acceptance and unit tests. He is not to take into account any descriptions of system behavior found in markdown files.

**Constraints:**
- Tests ONLY (no .md files, no source code comments)
- Analyze: [SPECIFY TEST FILES, e.g., validation/test_*.py]
- Time Budget: 30 minutes

**Deliverable:**
Ralph is to describe the system in a markdown file in the 'work/notes/' directory:
- File name: `ralph_system_analysis_from_tests.md`
- Content: System understanding purely from test evidence
- Include confidence levels (high/medium/low) per category

**Phase 2: Initialize as Architect Alphonso**

When Ralph is done, initialize as Architect Alphonso and review Ralph's interpretations.

**Input:**
- Ralph's analysis document
- Actual source code
- Architecture documentation (ADRs)

**Deliverable:**
Alphonso is to create `alphonso_architecture_review.md` in 'work/notes/' that:
- Validates accuracy category-by-category
- Highlights discrepancies to actual system and architecture
- Identifies blind spots (what tests don't show)
- Provides test quality verdict and recommendations

**Phase 3: Documentation**

Create work log per Directive 014 and prompt storage per Directive 015.
```

---

## Customization Variables

Replace these placeholders with project-specific values:

| Variable | Description | Example |
|----------|-------------|---------|
| `[TEST_FILES]` | Test files to analyze | `validation/test_*.py` |
| `[MODULE_SCOPE]` | Specific modules to focus on | `task_utils, agent_orchestrator` |
| `[TIME_BUDGET]` | Analysis time limit | `30 minutes` |
| `[OUTPUT_DIR]` | Output directory | `work/notes/` |
| `[DIRECTIVES]` | Applicable directives | `014, 015` |

---

## Example Usage

### Scenario 1: Full Repository Analysis

```markdown
@agent As an experiment, validate the quality of the entire test suite.

Initialize as Researcher Ralph (non-coding agent) and describe what all systems do by looking ONLY at tests in validation/ directory. No markdown files allowed.

Output: `work/notes/ralph_system_analysis_from_tests.md`

Then initialize as Architect Alphonso, review Ralph's analysis against actual source code and ADRs, and create `work/notes/alphonso_architecture_review.md` highlighting discrepancies.

Follow Directives 014 and 015 for work log and prompt storage.
```

### Scenario 2: Specific Module Focus

```markdown
@agent Validate test quality for the orchestration module only.

**Researcher Ralph:** Analyze ONLY:
- validation/test_task_utils.py
- validation/test_agent_orchestrator.py
- validation/test_orchestration_e2e.py

Describe task_utils and agent_orchestrator modules from tests alone.
Output: `work/notes/ralph_orchestration_analysis.md`

**Architect Alphonso:** Review against:
- ops/scripts/orchestration/task_utils.py
- ops/scripts/orchestration/agent_orchestrator.py
- docs/architecture/adrs/ADR-008-file-based-async-coordination.md

Output: `work/notes/alphonso_orchestration_review.md`
```

### Scenario 3: New Feature Validation

```markdown
@agent Validate tests for the new [FEATURE_NAME] feature.

Scope: Tests in validation/test_[feature].py only

**Researcher Ralph:**
- Analyze test_[feature].py ONLY
- Time budget: 15 minutes
- Output: work/notes/ralph_[feature]_analysis.md

**Architect Alphonso:**
- Compare to src/[feature].py and relevant ADRs
- Output: work/notes/alphonso_[feature]_review.md

Document per Directives 014 and 015.
```

---

## Prompt Variations

### Lightweight (20 minutes)
```markdown
@agent Quick test quality check for [MODULE].

Single-pass analysis:
1. Read tests in validation/test_[module].py
2. Generate system understanding
3. Compare to source code
4. Report accuracy percentage and top 3 gaps

Output: Brief report in work/notes/
```

### Deep-Dive (120 minutes)
```markdown
@agent Comprehensive test suite audit.

**Phase 1:** Researcher Ralph (45 min)
- All test files in validation/
- Include performance and security aspects
- Detailed confidence assessment

**Phase 2:** Architect Alphonso (45 min)
- Review against all source code
- Validate against all ADRs
- Security and operational assessment

**Phase 3:** Recommendations (30 min)
- Prioritized improvement backlog
- Cost/benefit analysis
- Implementation examples

Full documentation suite per Directives 014, 015.
```

### Automated (Future)
```markdown
@agent Run automated test readability analysis.

# This is a future enhancement
# Would use specialized tooling to:
# - Parse tests automatically
# - Compare to source AST
# - Generate accuracy scores
# - Flag documentation gaps

For now: Use manual dual-agent approach
```

---

## Success Indicators

### Process Indicators
✅ Ralph analysis created in `work/notes/`  
✅ Alphonso review created in `work/notes/`  
✅ Work log created per Directive 014  
✅ Prompt stored per Directive 015  
✅ Quantitative accuracy scores calculated

### Quality Indicators
✅ Accuracy percentage calculated (e.g., "92%")  
✅ Category-by-category breakdown provided  
✅ Blind spots identified with examples  
✅ Actionable recommendations generated  
✅ Test quality verdict assigned (⭐ rating)

### Outcome Indicators
✅ System understanding validated  
✅ Documentation gaps discovered  
✅ Test improvements prioritized  
✅ Methodology documented for reuse

---

## Failure Modes and Recovery

### Problem: Researcher reads documentation
**Detection:** Analysis includes information not in tests  
**Recovery:** Restart with stricter constraints, audit sources used

### Problem: Analysis too superficial
**Detection:** No quantitative metrics, vague findings  
**Recovery:** Require line-by-line test reading, fixture extraction

### Problem: No actionable recommendations
**Detection:** Alphonso says "tests are good" without specifics  
**Recovery:** Require prioritized improvement backlog with examples

### Problem: Time overrun
**Detection:** Analysis exceeds time budget significantly  
**Recovery:** Reduce scope (fewer test files) or increase budget

### Problem: Cannot repeat
**Detection:** Methodology unclear, results not reproducible  
**Recovery:** Enhance work log with step-by-step commands used

---

## Integration Patterns

### Pre-Release Quality Gate
```yaml
# Run before major releases
trigger: version tag created
agent: DevOps Danny (Build Automation)
output: Quality assessment report
decision: Block release if accuracy <80%
```

### Quarterly Review
```yaml
# Track test quality trends
trigger: First day of quarter
agent: Researcher Ralph + Architect Alphonso
output: Trend report comparing to previous quarter
decision: Adjust test strategy if degrading
```

### Onboarding
```yaml
# New team member introduction
trigger: New contributor joins
agent: Generate fresh analysis
output: System overview from tests
decision: Required reading before first PR
```

### CI/CD Integration
```yaml
# Automated checks (future)
trigger: PR to main with test changes
agent: Automated analyzer
output: Test documentation quality score
decision: Block if score decreases
```

---

## Output Artifacts

### Primary Artifacts

**1. Ralph's System Analysis**
- Location: `work/notes/ralph_system_analysis_from_tests.md`
- Size: 10-20K characters typical
- Sections: Executive summary, components, workflows, confidence

**2. Alphonso's Architecture Review**
- Location: `work/notes/alphonso_architecture_review.md`  
- Size: 15-25K characters typical
- Sections: Accuracy assessment, blind spots, recommendations, verdict

### Supporting Artifacts

**3. Work Log**
- Location: `work/reports/logs/[agent]/[timestamp]-test-readability-study.md`
- Content: Execution metrics, findings, token counts

**4. Prompt Storage**
- Location: `work/reports/prompts/[timestamp]-test-readability-prompt.md`
- Content: Original prompt, SWOT analysis, reusability notes

---

## Quality Checklist

Before considering analysis complete, verify:

- [ ] Ralph analysis covers all test files in scope
- [ ] Quantitative accuracy scores calculated
- [ ] Category-by-category validation performed
- [ ] Blind spots identified with specific examples
- [ ] Recommendations prioritized (high/medium/low)
- [ ] Test quality verdict assigned (⭐ rating)
- [ ] Work log created with token metrics
- [ ] Prompt stored with SWOT analysis
- [ ] All artifacts in correct directories
- [ ] Methodology documented for repeatability

---

## Troubleshooting

### Issue: Low Accuracy (<70%)
**Possible Causes:**
- Tests lack descriptive names
- Few or no integration tests
- Missing edge case coverage
- No fixtures documenting data models

**Solutions:**
- Improve test naming conventions
- Add E2E workflow tests
- Document expected data structures in fixtures

### Issue: High Accuracy (>95%)
**Interpretation:** Excellent! Tests are effective documentation

**Next Steps:**
- Share approach as best practice
- Use as onboarding material
- Consider automating analysis

### Issue: Missing Architecture Context
**Expected:** Tests naturally don't document "why"

**Solutions:**
- Add ADR links to test docstrings
- Include architecture notes in comments
- Reference design decisions in test names

---

## References

**Related Documents:**
- Approach: `.github/agents/approaches/test-readability-clarity-check.md`
- Directive 014: Work log standards
- Directive 015: Prompt storage standards
- ADR-012: Test-driven development defaults

**Example Analysis:**
- Ralph's Analysis: `work/notes/ralph_system_analysis_from_tests.md`
- Alphonso's Review: `work/notes/alphonso_architecture_review.md`
- Work Log: `work/reports/logs/build-automation/2025-11-29T0652-qualitative-test-study.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-29 | Initial template based on successful pilot study |

---

**Template Maintained by:** Build Automation Team  
**Review Cycle:** After each usage, refine based on learnings  
**Status:** Active and proven effective (92% accuracy achieved in pilot)
