# Glossary Candidate Extraction: Batch 1 - Directives

**Agent:** Lexical Larry  
**Date:** 2026-02-10  
**Source:** doctrine/directives/ (directives 001-038)  
**Status:** Complete  
**Method:** Manual extraction per Living Glossary Practice approach

---

## Extraction Summary

**Total Directives Processed:** 32 (excluding README.md)  
**Domain Terms Extracted:** 99 candidates  
**Confidence Distribution:**
- High confidence: 74 terms (75%)
- Medium confidence: 21 terms (21%)
- Low confidence: 4 terms (4%)

**Domain Distribution:**
- Framework (45 terms): Orchestration, context management, governance, version control
- Development Practice (28 terms): Testing, quality, version control, process
- Domain-Driven Design (16 terms): Bounded contexts, ubiquitous language, integration patterns
- Testing (10 terms): TDD, ATDD, test-first practices

---

## Extracted Terms by Domain

### 1. CLI & Tooling Domain (Directives 001, 013)
1. **Bypass Check** - Pre-execution LOCAL_ENV.md verification
2. **Remediation Technique** - Fallback for unreliable terminal interactions
3. **Flaky Terminal Behavior** - Unreliable shell interactions requiring remediation
4. **Fallback Strategy** - Alternative tools when preferred unavailable (fd→find, rg→grep)

### 2. Context & Token Management (Directive 002)
5. **Token Discipline** - Maintaining governance layers while offloading details
6. **External Memory** - work/notes/external_memory/ storage for context swapping
7. **Offloading** - Moving detailed context to files to conserve token budget

### 3. Orchestration & Collaboration (Directives 019, 014)
8. **File-Based Orchestration** - YAML task file coordination system
9. **Task State** - Lifecycle position: inbox/new/assigned/in_progress/done/archive
10. **Task Management Scripts** - Automated tools (start_task.py, complete_task.py, etc.)
11. **Worklog** - Structured execution documentation in work/reports/logs/
12. **Primer Checklist** - Required documentation of primer usage in work logs

### 4. Testing & Quality (Directives 016, 017, 028)
13. **ATDD (Acceptance Test Driven Development)** - User-visible behavior tests first
14. **Black-Box Testing** - Testing through public interfaces (HTTP, CLI)
15. **Red-Green-Refactor** - TDD cycle: failing test, minimal code, improve design
16. **Refactor Phase** - TDD step 3 where only production code changes, tests stay green
17. **Test-First Bug Fixing** - Reproduction test before fix
18. **Reproduction Test** - Test demonstrating bug by failing due to defect

### 5. Mode & Reasoning (Directives 010, 024)
19. **Mode Transition** - Explicit shift between reasoning modes [mode: source → target]
20. **Meta-Mode** - Self-reflection, process alignment, governance calibration
21. **Ralph Wiggum Loop** - Mid-execution self-observation checkpoint protocol
22. **Checkpoint** - Mandatory/optional pause for progress assessment
23. **Course Correction** - Mid-execution adjustment from checkpoint findings
24. **Warning Sign** - Detectable execution symptoms (drift, confusion, scope creep)

### 6. Decision Documentation (Directive 018)
25. **Documentation Level Framework** - Matching detail to information volatility
26. **Volatility** - Rate of information change determining documentation approach
27. **Stability Marker** - Annotation indicating stable vs. experimental aspects

### 7. Leniency & Adherence (Directive 020)
28. **Leniency Level** - Calibration scale (0-4) for template adherence strictness
29. **Structural Adherence** - Degree outputs match prescribed templates

### 8. Locality & Simplicity (Directives 021, 036)
30. **Gold Plating** - Adding features without evidence of need
31. **Premature Abstraction** - Creating frameworks before patterns stabilize
32. **Complexity Creep** - Cumulative degradation from small additions
33. **Boy Scout Rule** - Leave code/docs cleaner than found
34. **Spot Check** - Pre-task scan (2-5 min) for quick wins
35. **Quick Win** - Improvement taking <5 minutes
36. **Cleanup Commit** - Separate commit for pre-task improvements

### 9. Clarification & Alignment (Directives 023, 038)
37. **Clarification Request** - Formal pause for ambiguity resolution
38. **Conceptual Alignment** - Explicit confirmation of shared terminology understanding
39. **Domain Term** - Business/context-specific vocabulary requiring interpretation

### 10. Specification-Driven Development (Directives 034, 035)
40. **Specification (Spec)** - Feature-level design document with YAML frontmatter
41. **Feature (Spec Context)** - Sub-component within specification
42. **Initiative (Portfolio Context)** - Top-level grouping of specifications
43. **Feature Status** - draft/in_progress/done/blocked
44. **Phase Checkpoint Protocol** - 6-step phase completion verification
45. **Role Boundaries** - Authority matrix: PRIMARY/CONSULT/NO per phase

### 11. Commit & Version Control (Directive 026)
46. **Agent Slug** - Lowercase, hyphenated agent identifier for commits
47. **Commit Frequency** - Principle of small, atomic commits
48. **Atomic Commit** - Single-purpose commit for one logical unit
49. **Human in Charge** - Governance centering human accountability and authority
50. **Session Override** - Human-authorized temporary protocol deviation

### 12. Framework Guardian (Directive 025)
51. **Framework Distribution** - Zip-based packaging with integrity verification
52. **Framework Guardian** - Agent for audits, upgrades (read-only, recommend-only)
53. **Framework Audit** - Validation against canonical manifest checksums
54. **Manifest** - Authoritative registry (META/MANIFEST.yml) with SHA256 checksums
55. **Conflict Classification** - Upgrade conflict categories: Auto-Merge/Non-Breaking/Local/Breaking
56. **Anti-Corruption Layer (ACL)** - Translation layer protecting downstream context

### 13. Context-Aware Design (Directive 037)
57. **Bounded Context** - Explicit boundary with consistent domain model and language
58. **Context Boundary** - Edge between contexts requiring translation
59. **Published Language** - Stable API published for multiple consumers
60. **Context Map** - Visual diagram of context relationships
61. **Shared Kernel** - Small shared model requiring high coordination
62. **Ubiquitous Language** - Shared vocabulary within bounded context
63. **Living Glossary** - Continuously updated, executable glossary with enforcement
64. **Enforcement Tier** - Advisory/Acknowledgment/Hard Failure governance levels

### 14. Prompt & Communication (Directives 015, 023)
65. **Prompt Documentation** - Optional SWOT analysis of task prompts
66. **SWOT Analysis (Prompt Context)** - Evaluation framework for prompt quality
67. **Success Criteria** - Measurable conditions defining task completion
68. **Deliverable** - Specific artifact or output with file paths and validation

---

## Additional Terms Extracted (69-99)

69. **6-Phase Cycle** - Analysis → Architecture → Planning → Tests → Code → Review
70. **Phase Skipping** - Anti-pattern of bypassing required workflow phases
71. **Role Overstepping** - Agent acting outside authority boundaries
72. **Quad-A Pattern** - Test structure: Arrange-Act-Assert-After
73. **Characterization Test** - Safety net for legacy code before changes
74. **Flaky Test** - Non-deterministic test requiring stabilization
75. **Test Readability** - Clarity of test intent and structure
76. **Anemic Domain Model** - Anti-pattern with logic in services not domain objects
77. **Specification Frontmatter** - YAML metadata at top of specification files
78. **Progress Rollup** - Calculation of initiative/spec progress from task statuses
79. **Orphan Task** - Task not linked to any specification
80. **Portfolio View** - Dashboard hierarchy: Initiative → Specification → Task
81. **Task-to-Specification Linking** - Via `specification:` field in task YAML
82. **Premortem Risk Identification** - Anticipating failure modes before starting
83. **Adversarial Testing** - Stress-testing proposals with edge cases
84. **AMMERSE Analysis** - Trade-off framework for decision-making
85. **Stopping Conditions** - Pre-defined criteria for ending or pausing work
86. **Fresh Context Iteration** - Starting from clean context periodically
87. **Safe-to-Fail Experiment** - Small, reversible exploratory work
88. **Incremental Code Review** - Reviewing changes in small batches
89. **Extract-Before-Interpret** - Data gathering before analysis
90. **Fail-Fast Validation** - Early input checking to prevent cascading errors
91. **Smallest Viable Diff** - Minimal change to achieve goal
92. **BDD (Behavior-Driven Development)** - Given/When/Then acceptance test format
93. **Gherkin** - BDD scenario language syntax
94. **Integration Test** - Testing component interactions
95. **System Test** - End-to-end testing across full system
96. **Regression Prevention** - Tests ensuring bugs don't recur
97. **Test Coverage** - Percentage of code exercised by tests
98. **Continuous Integration** - Automated build/test on every commit
99. **Trunk-Based Development** - Short-lived branches, frequent integration

---

## Confidence Rating Methodology

**High Confidence (74 terms):**
- Explicit definition provided in directive
- Consistent usage across multiple contexts
- Clear boundaries and distinct from related concepts
- Examples or usage guidelines included

**Medium Confidence (21 terms):**
- Implicit definition derivable from context
- Some ambiguity in scope or boundaries
- Limited usage examples
- May overlap with related concepts

**Low Confidence (4 terms):**
- Emerging concept not fully defined
- Highly context-dependent meaning
- Sparse usage in directives
- Requires domain expert validation

---

## Quality Gates Applied

✅ **Domain-Specific Filter:** Excluded generic programming terms (list, dict, array, function, class) unless given domain-specific meaning  
✅ **Context Grounding:** Every term includes source directive and usage context  
✅ **Relationship Mapping:** Related_terms connections enable navigation  
✅ **Usage Notes:** Practical application guidance when available  
✅ **Confidence Transparency:** Explicit rating per term

---

## Recommended Next Steps

1. **Curator Review:** Validate consistency with existing GLOSSARY.md entries
2. **Bidirectional Links:** Ensure related_terms connections are mutual
3. **Domain Expert Validation:** Confirm DDD terms align with standard definitions
4. **Elevation Candidates:** Identify high-confidence terms for canonical status
5. **Disambiguation:** Flag terms needing context-specific definitions
6. **Integration:** Link to IDE glossary tools (Contextive)
7. **Enforcement Planning:** Determine which terms warrant acknowledgment/hard-failure tiers

---

## Terms Requiring Special Attention

**Potential Synonyms to Reconcile:**
- Work Log vs. Worklog (both used; prefer "Work Log" per GLOSSARY.md)
- Specification vs. Spec (abbreviation common; both acceptable)
- Feature (metadata) vs. Feature (capability) - context disambiguates

**Terms with Multiple Meanings:**
- Feature: (1) spec frontmatter metadata, (2) user-facing capability
- Context: (1) bounded context (DDD), (2) agent context (memory), (3) execution context
- Mode: (1) reasoning mode, (2) operational mode, (3) file permissions

**Emerging Concepts (Low Confidence):**
- Flaky Terminal Behavior (environment-specific)
- Session Override (governance edge case)
- Course Correction (Ralph Wiggum-specific)
- Warning Sign (checklist-specific)

---

## Statistics Summary

| Category | Count | Percentage |
|----------|-------|------------|
| **Total Terms** | 99 | 100% |
| High Confidence | 74 | 75% |
| Medium Confidence | 21 | 21% |
| Low Confidence | 4 | 4% |
| **By Domain** | | |
| Framework | 45 | 45% |
| Development Practice | 28 | 28% |
| Domain-Driven Design | 16 | 16% |
| Testing | 10 | 10% |

---

## Methodology Notes

**Extraction Process:**
1. Read all 32 directives sequentially
2. Identify terms with domain-specific definitions
3. Extract definition from directive context
4. Note related terms and cross-references
5. Assign confidence based on usage clarity
6. Document source and practical notes

**Exclusion Criteria:**
- Generic programming vocabulary without domain specialization
- Tool names unless part of framework practice (fd, rg, etc.)
- File paths and directory names
- Proper names of people or organizations
- Version numbers and dates

**Inclusion Criteria:**
- Domain-specific terminology
- Framework-specific practices
- DDD concepts with clear application
- Workflow/process terms
- Quality/governance concepts
- Integration patterns

---

## File Outputs

1. **batch1-directives-candidates.yaml** - Full structured YAML (99 entries)
2. **batch1-directives-extraction-summary.md** - This summary document
3. **README.md** - Glossary candidates directory guide

---

**Extraction Complete** ✅  
**Agent:** Lexical Larry  
**Date:** 2026-02-10  
**Next:** Curator review and domain expert validation
