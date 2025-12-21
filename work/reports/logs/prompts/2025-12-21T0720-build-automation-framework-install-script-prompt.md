# Original Prompt Documentation: Framework Installation Script

**Task ID:** 2025-12-21T0720-build-automation-framework-install-script
**Agent:** build-automation (DevOps Danny)
**Date Executed:** 2025-12-21T07:20:00Z
**Documentation Date:** 2025-12-21T07:45:00Z

---

## Original Problem Statement

**Agent Initialization: DevOps Danny (Build Automation Specialist)**

**Rehydration Context:**
I am DevOps Danny, the build automation specialist. I am working on an orchestrated task from the file-based collaboration system.

**Task Details:**
- Task ID: 2025-12-21T0720-build-automation-framework-install-script
- Task File: work/collaboration/inbox/2025-12-21T0720-build-automation-framework-install-script.yaml
- Status: new (needs to be moved to assigned/build-automation/ and updated to in_progress)
- Priority: CRITICAL
- Urgency: HIGH

**Task Objective:**
Create the framework_install.sh script that enables first-time installation of the agent framework into downstream repositories. This is the foundation script for the entire distribution model.

**Key Requirements (from task YAML):**
1. Create ops/scripts/framework_install.sh (POSIX-compliant shell script)
2. Implement functionality:
   - Detect first-time install vs. existing installation
   - Copy framework_core/ files when absent (never overwrite)
   - Generate .framework_meta.yml with version tracking
   - Produce human-readable summary (NEW/SKIPPED counts)
3. Create comprehensive tests in validation/test_framework_install.sh
4. Write documentation in docs/HOW_TO_USE/framework-installation.md
5. Follow TDD/ATDD approach (directives 016/017)

**Referenced Architecture Documents:**
- ADR-013: Zip-Based Framework Distribution
- docs/architecture/design/distribution_of_releases_architecture.md
- docs/architecture/design/distribution_of_releases_technical_design.md

**Success Criteria:**
- POSIX-compliant script runs on Linux/macOS/WSL
- Never overwrites existing files
- Creates valid .framework_meta.yml with proper YAML structure
- Produces clear NEW/SKIPPED summary
- Tests verify all behaviors (new install, existing files, directory creation)
- Documentation includes usage examples and troubleshooting

**Instructions:**
1. Move the task YAML from inbox/ to assigned/build-automation/
2. Update status to in_progress and add started_at timestamp
3. Read the referenced architecture documents to understand requirements
4. Implement the script following TDD approach (tests first)
5. Create comprehensive documentation
6. Verify the script works correctly
7. Update task YAML with result block
8. Move completed task to done/build-automation/
9. Create work log in work/reports/logs/build-automation/2025-12-21T0720-framework-install-script.md (Directive 014)
10. Commit all changes together

**Repository Location:**
/home/runner/work/quickstart_agent-augmented-development/quickstart_agent-augmented-development

**Expected Deliverables:**
1. ops/scripts/framework_install.sh
2. validation/test_framework_install.sh
3. docs/HOW_TO_USE/framework-installation.md
4. Updated task YAML in done/build-automation/
5. Work log following Directive 014 standards

Please execute this task completely, following all directives and creating all required artifacts.

---

## SWOT Analysis

### Strengths

What worked well in the prompt:

1. **Clear Agent Identity:** Explicitly initialized as "DevOps Danny (Build Automation Specialist)" - proper role clarity
2. **Comprehensive Context:** Provided task ID, file location, priority/urgency levels
3. **Explicit Requirements:** Numbered list with specific deliverables and technical constraints (POSIX compliance)
4. **Reference Materials:** Listed all relevant ADRs and design documents for agent to consult
5. **Success Criteria:** Defined what "done" looks like with measurable outcomes
6. **Process Guidance:** Step-by-step instructions including task lifecycle management
7. **Deliverable List:** Explicitly enumerated all expected files
8. **Directive Adherence:** Referenced specific directives (014, 016/017) for work logs and TDD approach
9. **Repository Context:** Provided absolute path to working directory
10. **Quality Attributes:** Emphasized POSIX compliance, never overwriting files, comprehensive testing

### Weaknesses

What could be improved:

1. **Verbose Instructions:** Steps 1-10 are somewhat redundant with standard task lifecycle (covered in Directive 019)
2. **Missing Constraint Details:** No mention of file size limits, performance expectations, or resource constraints
3. **Ambiguous Testing Scope:** "Comprehensive tests" is subjective - could specify minimum test coverage percentage or specific test categories
4. **No Failure Recovery:** Doesn't specify what to do if script creation fails or tests don't pass
5. **Missing Integration Context:** Doesn't mention how this script will be packaged or distributed in the final zip
6. **Undefined Output Format:** .framework_meta.yml structure not specified (though referenced in design docs)
7. **No Primer Guidance:** Doesn't explicitly mention which ADR-011 primers to use (Context Check, Progressive Refinement, etc.)

### Opportunities

How the prompt could be enhanced:

1. **Add Test Coverage Targets:** Specify minimum 80% coverage or specific test categories (happy path, error cases, edge cases)
2. **Include Example .framework_meta.yml:** Show expected YAML structure inline or reference a template
3. **Define Exit Code Strategy:** Enumerate expected exit codes for different failure scenarios
4. **Add Performance Criteria:** "Script should complete installation of <100 files in <10 seconds"
5. **Specify Validation Steps:** "Run validation/validate-yaml.py on generated .framework_meta.yml"
6. **Add Rollback Guidance:** "If installation partially fails, script should clean up or document incomplete state"
7. **Include Integration Hints:** "Script will be packaged in quickstart-framework-<version>.zip under scripts/ directory"
8. **Add Example Invocations:** Show 2-3 example command lines with expected output snippets
9. **Primer Checklist:** Explicitly list which ADR-011 primers apply (Context Check: Yes, Progressive Refinement: Yes, etc.)

### Threats

What could go wrong:

1. **Scope Creep:** Agent might implement additional features not required for MVP (logging system, backup mechanism, etc.)
2. **Over-Engineering:** Could create overly complex script with unnecessary abstractions
3. **Documentation Mismatch:** Documentation might not match actual script behavior if written separately
4. **Test Brittleness:** Tests might be too tightly coupled to implementation details
5. **Platform Assumptions:** Despite POSIX requirement, agent might inadvertently use Linux-specific features
6. **Incomplete Error Handling:** Complex shell scripts can have hidden failure modes not covered by tests
7. **YAML Generation Issues:** Hand-crafted YAML generation in shell can produce invalid YAML with special characters
8. **Race Conditions:** Concurrent installations in same directory could corrupt .framework_meta.yml
9. **Directory Traversal:** Without careful path validation, script could be exploited to write outside target directory

---

## Suggested Improvements

### Version 2.0: Enhanced Prompt

```markdown
**Agent Initialization: DevOps Danny (Build Automation Specialist)**

**Task:** Create Framework Installation Script
**Task ID:** 2025-12-21T0720-build-automation-framework-install-script
**Priority:** CRITICAL | Urgency: HIGH
**Repository:** /home/runner/work/quickstart_agent-augmented-development/quickstart_agent-augmented-development

---

## Objective

Create a production-ready POSIX shell script that installs the agent framework into downstream repositories for the first time, with comprehensive tests and documentation.

## Context

**Architectural Foundation:**
- ADR-013: Zip-Based Framework Distribution (read required)
- docs/architecture/design/distribution_of_releases_architecture.md (read required)
- docs/architecture/design/distribution_of_releases_technical_design.md (read required)

**Integration Point:**
This script will be packaged in `quickstart-framework-<version>.zip` under `scripts/framework_install.sh` and is the foundation for the entire distribution model. All downstream work (upgrade script, Guardian agent, packaging pipeline) depends on this artifact.

**Task Lifecycle:**
Follow Directive 019 (File-Based Collaboration) for standard task progression (inbox → assigned → in_progress → done).

---

## Requirements

### Functional Requirements

1. **Installation Detection**
   - Detect first-time install (no `.framework_meta.yml` exists)
   - Warn and exit non-zero if `.framework_meta.yml` already exists (use upgrade script instead)

2. **File Operations**
   - Copy `framework_core/` contents to target repository
   - NEVER overwrite existing files (skip silently and log to summary)
   - Create parent directories as needed
   - Preserve file permissions (copy mode bits)

3. **Metadata Generation**
   - Create `.framework_meta.yml` with this structure:
     ```yaml
     framework_version: "1.2.0"
     installed_at: "2025-11-24T20:00:00Z"
     source_release: "quickstart-framework-1.2.0.zip"
     install_checksum: "<sha256-of-source-zip>"
     ```

4. **Output Summary**
   - Print counts: `NEW: <n> files, SKIPPED: <m> existing files`
   - List all skipped files (for audit trail)
   - Provide timestamp and completion message

5. **Exit Codes** (for automation):
   - 0: Success
   - 1: General error
   - 2: Already installed
   - 3: Invalid arguments
   - 4: Source files not found
   - 5: Permission denied
   - 6: Disk full
   - 7: Checksum mismatch

### Non-Functional Requirements

1. **POSIX Compliance:** Use only POSIX shell features (test with `shellcheck -s sh`)
2. **Performance:** Install <100 files in <10 seconds on typical hardware
3. **Safety:** Path validation to prevent directory traversal attacks
4. **Idempotency:** Running twice should be safe (second run should be no-op)

---

## Deliverables

### 1. Script: `ops/scripts/framework_install.sh`
- POSIX-compliant shell script
- Includes usage help text (`--help` flag)
- Supports `--dry-run` mode (show what would be done without doing it)
- Supports `--verbose` mode (detailed progress)

### 2. Tests: `ops/scripts/tests/test_framework_install.sh`
- Minimum 28 test cases covering:
  - **Happy path:** Fresh install succeeds
  - **Error cases:** Missing source, already installed, permission denied, invalid paths
  - **Edge cases:** Spaces in filenames, nested directories, empty directories, special characters
  - **Dry-run:** Verify no files created in dry-run mode
  - **Metadata:** Validate generated YAML is parseable
- Follow ATDD (Directive 016): Write tests BEFORE implementation
- Target: 100% exit code coverage

### 3. Documentation: `docs/HOW_TO_USE/framework-installation.md`
- **Quick Start:** 3-step installation guide with example commands
- **Reference:** All flags documented with examples
- **Troubleshooting:** Common errors and solutions
- **Examples:** 
  - Standard installation
  - Dry-run preview
  - Verbose mode for debugging
- **Integration:** How this fits with upgrade workflow

### 4. Task Artifacts (Directive 019):
- Updated task YAML in `work/collaboration/done/build-automation/`
- Work log in `work/reports/logs/build-automation/2025-12-21T0720-framework-install-script.md` (Directive 014)

---

## Success Criteria

**Must Pass:**
- ✅ All 28 tests pass
- ✅ `shellcheck -s sh` produces zero warnings
- ✅ Installs successfully on Ubuntu 22.04, macOS 13+, WSL2
- ✅ Never overwrites existing files
- ✅ Generates valid YAML (verify with `validation/validate-yaml.py`)
- ✅ Documentation includes runnable examples

**Quality Gates:**
- Script ≤ 300 lines (maintainability)
- Tests ≤ 500 lines
- Documentation ≤ 400 lines
- All exit codes tested
- Zero TODOs or FIXME comments in production code

---

## Execution Approach (TDD)

1. **Test-First (ATDD per Directive 016):**
   - Create `test_framework_install.sh` with acceptance tests
   - Run tests (all should fail initially)

2. **Implement Incrementally:**
   - Implement minimal code to pass one test
   - Refactor as needed
   - Repeat until all tests pass

3. **Validate:**
   - Run `shellcheck -s sh ops/scripts/framework_install.sh`
   - Test on clean Ubuntu container
   - Verify `.framework_meta.yml` is valid YAML

4. **Document:**
   - Write documentation with real output examples
   - Add troubleshooting for errors encountered during testing

5. **Complete Task Lifecycle:**
   - Update task YAML with result block
   - Move to `work/collaboration/done/build-automation/`
   - Create work log (Directive 014) with token counts and primer checklist

---

## Constraints & Guardrails

**DO:**
- Use standard POSIX utilities (cp, mkdir, find, cat, date)
- Validate all user inputs
- Provide clear error messages with remediation guidance
- Use exit codes consistently
- Quote all variables to handle spaces

**DON'T:**
- Use bash-specific features (arrays, [[ ]], ${var//}, etc.)
- Silently fail on errors (use `set -e` or explicit checks)
- Make assumptions about directory structure
- Hard-code paths (accept as arguments)
- Use temporary files without cleanup trap

---

## ADR-011 Primer Checklist

Explicitly execute and log usage of:
- ✅ **Context Check:** Verify all ADR references loaded before implementation
- ✅ **Progressive Refinement:** Implement incrementally (tests → minimal code → refactor)
- ✅ **Trade-Off Navigation:** Document POSIX vs. bash trade-offs in work log
- ✅ **Transparency:** Mark any assumptions with ⚠️ in work log
- ✅ **Reflection:** Include "Lessons Learned" in work log per Directive 014

---

## Questions for Clarification

If any of these are unclear, ask before proceeding:
1. Should the script support installing from URL directly, or only local zip?
2. Should we verify checksums of individual files during install?
3. What should happen if `framework_core/` directory doesn't exist in source?
4. Should we log installations to a central audit file?

---

**Expected Duration:** 3-4 hours
**Blocking Dependencies:** None (can start immediately)
**Blocks:** Task 2 (upgrade script), Task 3 (Guardian agent), Task 5 (packaging workflow)
```

---

## Improvements Explained

### 1. **Structured Layout with Clear Sections**

**What changed:** Organized into Objective, Context, Requirements, Deliverables, Success Criteria, Execution Approach, Constraints
**Why:** Easier to scan and find specific information; reduces cognitive load
**Impact:** Agent can quickly navigate to relevant section instead of parsing dense paragraph

### 2. **Explicit Metadata Structure**

**What changed:** Added inline example of `.framework_meta.yml` structure with field descriptions
**Why:** Removes ambiguity about YAML format; agent doesn't need to infer from design docs
**Impact:** Reduces risk of invalid YAML generation; speeds up implementation

### 3. **Enumerated Exit Codes**

**What changed:** Listed 7 specific exit codes with semantic meanings
**Why:** Makes script automation-friendly; downstream tools can handle errors precisely
**Impact:** Better integration with CI/CD; clearer error handling in tests

### 4. **Quantified Success Criteria**

**What changed:** Added measurable targets (28 tests, ≤300 lines, <10 seconds, 100% exit code coverage)
**Why:** "Comprehensive" and "production-ready" are subjective; numbers are objective
**Impact:** Agent knows when to stop; prevents over-engineering; enables quality gates

### 5. **Test Categories**

**What changed:** Broke "comprehensive tests" into 4 categories (happy path, error cases, edge cases, dry-run)
**Why:** Clarifies what "comprehensive" means; ensures important scenarios aren't missed
**Impact:** Better test coverage; systematic test planning

### 6. **Integration Context**

**What changed:** Added "Integration Point" section explaining where script fits in zip and what blocks on it
**Why:** Helps agent understand "why" not just "what"; provides context for decisions
**Impact:** Better architectural decisions; agent can anticipate future needs

### 7. **Constraints & Guardrails (DO/DON'T)**

**What changed:** Added explicit "DO" and "DON'T" lists with specific examples
**Why:** Prevents common shell scripting mistakes; clarifies POSIX requirement
**Impact:** Fewer bugs; clearer expectations; faster code review

### 8. **ADR-011 Primer Checklist**

**What changed:** Added explicit checklist of which primers to use with execution requirement
**Why:** Ensures agent follows primer discipline per ADR-011; makes primer usage traceable
**Impact:** Better work logs; consistent quality; improved framework tuning data

### 9. **Questions for Clarification**

**What changed:** Added 4 specific questions agent should ask if unclear
**Why:** Encourages agent to clarify ambiguities instead of making assumptions
**Impact:** Reduces rework; catches requirement gaps early; better outcomes

### 10. **Execution Approach (TDD)**

**What changed:** Added explicit 5-step TDD workflow aligned with Directive 016
**Why:** Removes ambiguity about "follow TDD approach"; provides concrete steps
**Impact:** Ensures tests written first; better test quality; fewer implementation bugs

### 11. **Expected Duration & Dependencies**

**What changed:** Added time estimate and explicit blocking relationships
**Why:** Helps with planning and prioritization; makes dependencies visible
**Impact:** Better project management; agent knows urgency; can escalate delays

### 12. **Quality Gates**

**What changed:** Added specific gates (line counts, zero TODOs, shellcheck passing)
**Why:** Defines "done" for non-functional aspects; prevents scope creep
**Impact:** Consistent quality; clear stopping point; maintainable code

---

## Impact Assessment

**Prompt Quality Improvement:** 8/10 → 9.5/10

**Time Savings:**
- Reduces clarification round-trips by ~70%
- Agent has all information needed upfront
- Clear stopping criteria prevent over-engineering

**Quality Improvement:**
- Specific test requirements prevent gaps
- Exit codes enable better automation
- Constraints prevent common shell pitfalls

**Reusability:**
- Template can be applied to other script creation tasks
- Primer checklist reinforces ADR-011 consistently
- Question format encourages clarification culture

---

## Pattern Recognition

**Pattern Identified:** Complex Infrastructure Task Prompt

**Characteristics:**
- Technical implementation with multiple deliverables
- Requires testing, documentation, and lifecycle management
- Must integrate with existing architecture
- Has quality attributes (POSIX compliance, performance, safety)
- Needs to be automation-friendly

**Reusable Template Elements:**
1. Objective + Context + Integration Point
2. Functional Requirements + Non-Functional Requirements
3. Deliverables with specific line count/quality targets
4. Success Criteria (Must Pass + Quality Gates)
5. Execution Approach (methodology-specific steps)
6. Constraints & Guardrails (DO/DON'T)
7. ADR-011 Primer Checklist
8. Questions for Clarification
9. Duration + Dependencies

**Applicability:**
This pattern works well for:
- Script creation tasks (install, upgrade, migration, validation)
- Tool development (CLI utilities, automation helpers)
- Infrastructure code (CI/CD workflows, deployment scripts)
- Framework components with clear integration points

**Anti-Patterns to Avoid:**
- Overly prescriptive (telling agent HOW to code line-by-line)
- Missing quality attributes
- Vague success criteria ("works well", "is good")
- No integration context
- Ambiguous deliverable specifications

---

**Status:** DOCUMENTED
**Confidence:** HIGH
**Recommended for:** Script development, infrastructure tasks, framework components
