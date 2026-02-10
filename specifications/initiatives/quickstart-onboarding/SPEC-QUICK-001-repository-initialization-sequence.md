---
id: SPEC-QUICK-001
title: Enhanced Repository Initialization Sequence
status: draft
version: 1.0.0
author: Analyst Annie
created: 2026-02-10
updated: 2026-02-10
initiative: Quickstart & Onboarding
priority: high
type: functional
tags: [initialization, bootstrap, multi-agent, setup]
---

# SPEC-QUICK-001: Enhanced Repository Initialization Sequence

## Executive Summary

Define a multi-step repository initialization sequence that creates framework-ready repositories with best practices by default. Supports both automated (scripted) and guided (interactive) modes with multi-agent collaboration patterns.

**Goal:** Reduce repository initialization time from hours to <15 minutes while ensuring quality and completeness.

---

## Problem Statement

### Current State

**Manual Setup Required:**
- Read multiple documentation files
- Manually create directory structure
- Copy templates individually
- Write vision document from scratch
- Create glossary structure manually
- Configure local doctrine overrides
- No validation of completeness

**Pain Points:**
- 2-4 hours typical initialization time
- Easy to miss critical steps
- Inconsistent setups across teams
- No guidance on best practices
- Difficult to validate setup correctness

### Desired State

**Automated Initialization:**
- Single command execution: `./scripts/init-repository.sh`
- Or interactive wizard: `./scripts/setup-wizard.sh`
- Intelligent defaults with customization options
- Automated directory creation
- Template-based document generation
- Built-in validation and verification
- Multi-agent collaboration examples

**Benefits:**
- 10-15 minute initialization (85% time reduction)
- Consistent, high-quality setups
- Best practices by default
- Reduced support burden
- Lower barrier to adoption

---

## Requirements

### Functional Requirements

#### FR-1: Directory Structure Creation
**Priority:** MUST

The initialization sequence MUST create the following directory structure:

```
repository-root/
├── .contextive/
│   └── contexts/
│       ├── doctrine.yml
│       ├── ddd.yml
│       ├── organizational.yml
│       └── software-design.yml
├── .doctrine-config/
│   └── config.yaml
├── doctrine/              # Optional: local overrides
│   ├── guidelines/
│   └── approaches/
├── docs/
│   ├── architecture/
│   │   ├── adrs/
│   │   └── design/
│   ├── audience/          # Target personas
│   └── vision.md
├── specifications/
│   └── initiatives/
├── work/
│   ├── collaboration/
│   │   ├── assigned/
│   │   ├── pending/
│   │   └── fridge/
│   ├── planning/
│   ├── reports/
│   └── notes/
└── src/                   # If code repository
```

**Acceptance Criteria:**
- ✅ All directories created with correct permissions
- ✅ README files placed in key directories explaining purpose
- ✅ .gitkeep files in empty directories to preserve structure

---

#### FR-2: Vision Document Generation
**Priority:** MUST

The initialization sequence MUST create a project vision document.

**Template Source:** `doctrine/templates/architecture/design_vision.md`

**Customization:** Interactive prompts OR CLI flags for:
- Project name
- Problem statement (1-2 sentences)
- Target users/audience
- Key objectives (3-5 items)
- Success criteria

**Acceptance Criteria:**
- ✅ `docs/vision.md` created with customized content
- ✅ Follows template structure
- ✅ All placeholder sections filled or marked as TODO
- ✅ Links to audience personas (if defined)

---

#### FR-3: Glossary Infrastructure Setup
**Priority:** MUST

The initialization sequence MUST create Contextive glossary structure.

**Components:**
1. **Base glossaries** in `.contextive/contexts/`:
   - `doctrine.yml` (framework terms)
   - `ddd.yml` (domain-driven design concepts)
   - `organizational.yml` (Conway's Law, team patterns)
   - `software-design.yml` (architecture patterns)

2. **Project-specific glossary** (empty template):
   - `.contextive/contexts/project.yml`
   - Pre-populated with 5-10 placeholder terms based on vision

3. **Contextive configuration**:
   - `.contextive/definitions.yml` with directory references

**Acceptance Criteria:**
- ✅ All base glossary files created
- ✅ Project glossary template created
- ✅ Contextive config references all glossary files
- ✅ README in `.contextive/` explaining structure

---

#### FR-4: Local Doctrine Configuration
**Priority:** SHOULD

The initialization sequence SHOULD configure local doctrine overrides.

**Configuration File:** `.doctrine-config/config.yaml`

**Content:**
```yaml
# Doctrine Framework Configuration
version: "1.0.0"
source: "git-subtree"  # or "local", "remote"

paths:
  doctrine_root: "doctrine"
  local_overrides: "doctrine/local"
  
customization:
  local_guidelines: false
  local_approaches: false
  local_directives: false
  
distribution:
  enabled: true
  targets: ["github-copilot", "claude-desktop"]
  
validation:
  strict_mode: false
  check_cross_references: true
```

**Acceptance Criteria:**
- ✅ Config file created with sensible defaults
- ✅ Comments explain each section
- ✅ Documented in `.doctrine-config/README.md`

---

#### FR-5: Multi-Agent Collaboration Templates
**Priority:** SHOULD

The initialization sequence SHOULD create example collaboration workflows.

**Location:** `work/collaboration/examples/`

**Templates:**
1. **Multi-agent task example:**
   - Shows task delegation pattern
   - References directive 019 (file-based collaboration)
   
2. **Specification-driven workflow:**
   - Annie creates spec → Petra plans → Agents execute
   
3. **Review and iteration:**
   - Code review → feedback → iteration cycle

**Acceptance Criteria:**
- ✅ At least 2 example YAML task files
- ✅ README explaining collaboration patterns
- ✅ References to relevant directives

---

#### FR-6: Validation and Verification
**Priority:** MUST

The initialization sequence MUST validate setup completeness.

**Validation Checks:**
1. ✅ All required directories exist
2. ✅ Vision document created and not empty
3. ✅ Glossary files present and valid YAML
4. ✅ Configuration file valid YAML
5. ✅ No duplicate directory creation (idempotent)

**Output:**
- Success message with checklist of what was created
- Warning messages for any optional items skipped
- Error messages for validation failures
- Rollback on critical errors

**Acceptance Criteria:**
- ✅ Validation runs automatically after setup
- ✅ Clear success/failure messaging
- ✅ Exit code 0 for success, non-zero for failure

---

### Non-Functional Requirements

#### NFR-1: Performance
- Initialization completes in <30 seconds (excluding user input time)
- No external network calls required (all templates local)

#### NFR-2: Idempotency
- Running initialization twice does NOT break existing setup
- Existing files preserved (not overwritten) unless --force flag
- Clear warnings when skipping existing items

#### NFR-3: Cross-Platform
- Works on Linux, macOS, Windows (with Git Bash)
- No platform-specific dependencies
- Uses portable shell scripting (POSIX-compliant)

#### NFR-4: Maintainability
- Script references doctrine templates (no duplication)
- Comments explain each step
- Easy to extend with new steps
- Automated tests validate script functionality

---

## Implementation Design

### Execution Modes

#### Mode 1: Automated (Non-Interactive)

**Command:** `./scripts/init-repository.sh --auto`

**Behavior:**
- Uses default values for all prompts
- Creates minimal required structure
- Vision document has generic placeholder text
- Glossaries use base templates only
- Fast execution (<10 seconds)

**Use Case:** CI/CD, automated testing, quick prototypes

---

#### Mode 2: Guided (Interactive)

**Command:** `./scripts/init-repository.sh`

**Behavior:**
- Prompts for key information:
  - Project name
  - Problem statement
  - Target audience
  - Initial glossary terms (optional)
- Generates customized documents
- Offers to create example tasks
- Shows progress indicators

**Use Case:** New project setup, team onboarding

---

#### Mode 3: Wizard (Fully Interactive)

**Command:** `./scripts/setup-wizard.sh`

**Behavior:**
- Step-by-step guided experience
- Explanations at each step
- Preview before commit
- Rollback option
- Post-setup validation and next steps

**Use Case:** First-time users, complex setups

**Note:** See SPEC-QUICK-002 for detailed wizard specification

---

### Script Structure

```bash
#!/bin/bash
# init-repository.sh - Enhanced Repository Initialization

set -e  # Exit on error

# 1. Parse arguments (--auto, --force, --help)
parse_arguments "$@"

# 2. Validate environment (git, required tools)
validate_environment

# 3. Check if already initialized
check_existing_setup

# 4. Create directory structure
create_directory_structure

# 5. Generate vision document
generate_vision_document

# 6. Setup glossary infrastructure
setup_glossary_infrastructure

# 7. Configure local doctrine
configure_doctrine

# 8. Create collaboration examples
create_collaboration_examples

# 9. Validate setup
validate_setup

# 10. Display summary
display_summary
```

---

### Multi-Agent Collaboration Patterns

#### Pattern 1: Bootstrap Bill Leads
**Scenario:** Initial repository setup

**Flow:**
1. Human invokes: "Bootstrap Bill, initialize repository for project X"
2. Bill executes init-repository.sh with prompts
3. Bill creates vision document
4. Bill invokes Curator Claire to validate structure
5. Bill creates initial task for Planning Petra (roadmap)

**Outcome:** Fully initialized repository with first planning task queued

---

#### Pattern 2: Annie Specifies, Bill Executes
**Scenario:** Complex custom setup

**Flow:**
1. Human provides requirements to Annie
2. Annie creates initialization specification
3. Annie delegates to Bootstrap Bill
4. Bill executes per spec, reports back
5. Annie validates against requirements

**Outcome:** Custom initialization meeting specific requirements

---

#### Pattern 3: Wizard with Multi-Agent Support
**Scenario:** Interactive setup with agent assistance

**Flow:**
1. Human runs setup wizard
2. Wizard prompts for vision (optionally delegates to Writer-Editor)
3. Wizard prompts for glossary terms (optionally delegates to Lexical Larry)
4. Wizard prompts for architecture decisions (optionally delegates to Alphonso)
5. Bill executes initialization with collected inputs

**Outcome:** High-quality setup with expert agent input

---

## Testing Strategy

### Unit Tests

**Script Functions:**
- ✅ Directory creation (test in temp directory)
- ✅ YAML generation (validate structure)
- ✅ Template rendering (check placeholders replaced)
- ✅ Validation checks (simulate failures)

**Location:** `tests/unit/test_init_repository.py`

---

### Integration Tests

**End-to-End:**
- ✅ Full automated initialization in temp repo
- ✅ Guided mode with simulated inputs
- ✅ Idempotency (run twice, no errors)
- ✅ Validation failures trigger rollback

**Location:** `tests/integration/test_repository_init.py`

---

### Acceptance Tests

**User Scenarios:**
- ✅ New user can initialize repository in <15 minutes
- ✅ Initialized repository passes validation
- ✅ All templates render correctly
- ✅ Documentation explains next steps

**Location:** Manual test checklist + automated where possible

---

## Dependencies

**Upstream (Required):**
- ✅ Doctrine framework in `doctrine/` directory
- ✅ Templates in `doctrine/templates/`
- ✅ Bootstrap Bill agent profile defined

**Downstream (Enables):**
- SPEC-QUICK-002: Repository Setup Wizard (builds on this)
- Dashboard integration (uses initialized structure)
- Getting-started guide agent (references this process)

---

## Risks & Mitigations

### Risk 1: Template Staleness
**Symptom:** Init script uses outdated templates  
**Likelihood:** High (as framework evolves)  
**Impact:** High (poor user experience)  
**Mitigation:** 
- Script references doctrine templates directly (no copies)
- Automated tests validate template compatibility
- CI/CD runs init script on every commit

### Risk 2: Platform Incompatibility
**Symptom:** Script fails on Windows  
**Likelihood:** Medium  
**Impact:** Medium (excludes Windows users)  
**Mitigation:**
- Use POSIX-compliant shell commands
- Test on Windows Git Bash in CI
- Document platform requirements

### Risk 3: Over-Complexity
**Symptom:** Script too complex to maintain  
**Likelihood:** Low (with discipline)  
**Impact:** High (maintenance burden)  
**Mitigation:**
- Keep core script simple (<500 lines)
- Modular functions for each step
- Extensive comments and documentation

---

## Success Criteria

**Specification is successful when:**
- ✅ Script exists and is executable
- ✅ Automated mode completes in <30 seconds
- ✅ Guided mode completes in <15 minutes (with user input)
- ✅ 90% of initialized repositories validate successfully
- ✅ User feedback: "Easy to use" (>80% satisfaction)
- ✅ Adoption: >50% of new repos use initialization script

---

## Future Enhancements

### Phase 2 (Post-Launch):
1. **Git Integration:**
   - Automatic git init + first commit
   - Pre-commit hooks for validation
   
2. **CI/CD Templates:**
   - GitHub Actions workflow templates
   - GitLab CI configuration
   
3. **Language-Specific Setups:**
   - Python project structure
   - Node.js project structure
   - Java project structure

4. **Remote Repository Integration:**
   - Clone from quickstart template repo
   - Fork and customize pattern

---

## Related Documentation

**Directives:**
- Directive 037: Context-Aware Design
- Directive 038: Ensure Conceptual Alignment
- Directive 019: File-Based Collaboration

**Approaches:**
- Living Glossary Practice
- Language-First Architecture

**Templates:**
- `doctrine/templates/structure/` - Directory structure
- `doctrine/templates/architecture/design_vision.md` - Vision template
- `doctrine/templates/documentation/` - Documentation templates

**Agent Profiles:**
- Bootstrap Bill (primary implementer)
- Curator Claire (validation)
- Analyst Annie (requirements)

---

## Version History

- **1.0.0** (2026-02-10): Initial specification created by Analyst Annie

---

**Specification Status:** ✅ Ready for Review
**Next Steps:** 
1. Architect review (Alphonso)
2. Implementation planning (Petra)
3. Development (Bootstrap Bill)
