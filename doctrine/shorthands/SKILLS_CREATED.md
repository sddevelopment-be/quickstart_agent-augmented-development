# Skills Created: Session Summary

**Date:** 2026-02-06
**Session:** Iteration Orchestration & Framework Skills
**Total Skills Created:** 6 new skills + 1 comprehensive prompt template

---

## Overview

Created a complete iteration orchestration system with skills for multi-agent coordination, bug fixing, specification creation, and self-monitoring. All skills reference comprehensive prompt templates and framework directives.

---

## New Skills

### 1. `/iterate` - Iteration Orchestration ⭐⭐⭐⭐⭐

**Command:** `/iterate`
**Location:** `.claude/skills/iterate/SKILL.md`
**Purpose:** Execute complete iteration cycle with multi-agent coordination

**Workflow:**
1. Planning Petra: Assess state, identify next batch
2. Specialist agents: Execute tasks with TDD/ATDD
3. Planning Petra: Update artifacts, executive summary
4. Conditional: Create Architect review task if needed

**Key Features:**
- File-based orchestration (${WORKSPACE_ROOT}/collaboration/)
- TDD/ATDD enforcement (RED → GREEN → REFACTOR)
- Work log creation (Directive 014)
- Quality gates (>80% test coverage target)
- Agent handoff patterns

**Example Usage:**
```
User: /iterate

Agent (Petra): Starting M2 Batch 2.3 (2 tasks)...
Agent (Backend-Dev): [Implements with TDD, 44 tests pass, 92% coverage]
Agent (Petra): ✅ Batch complete, 5h actual vs 7h estimated
  Next: M3 Batch 3.1 - Telemetry Infrastructure
```

---

### 2. `/status` - Planning State Assessment ⭐⭐⭐⭐⭐

**Command:** `/status`
**Location:** `.claude/skills/status/SKILL.md`
**Purpose:** Planning Petra's executive view of current state

**Provides:**
- Current milestone progress (% complete)
- Task queue overview (inbox/assigned/done by priority)
- Blockers or decisions needed
- Next recommended batch (2-4 tasks, estimated time)
- Overall project health: ON TRACK | AT RISK | BLOCKED

**Best Practice:** Start every session with `/status` before `/iterate`

**Example Usage:**
```
User: /status

Agent (Petra):
  Current: M2 Tool Integration - 75% complete
  Inbox: 3 tasks (2 high, 1 medium)
  Next batch: M2 Batch 2.3 (2 tasks, ~5h)
  Health: 🟢 ON TRACK
```

---

### 3. `/review` - Architect Code Review ⭐⭐⭐⭐

**Command:** `/review`
**Location:** `.claude/skills/review/SKILL.md`
**Purpose:** Architect Alphonso conducts rigorous code review

**Review Areas:**
- ADR compliance verification
- Test coverage assessment (>80% target)
- Architectural patterns validation
- Security considerations
- Performance implications

**Output Status:**
- ✅ APPROVED - Ready to proceed
- 🔄 REDIRECT - Changes needed, then re-review
- 🛑 BLOCKED - Major issues, fundamental rethink

**Documents Review:** `${WORKSPACE_ROOT}/reports/reviews/YYYY-MM-DD-<topic>-review.md`

**Example Usage:**
```
User: /review

Agent (Alphonso):
  Reviewed: M2 Batch 2.3 - Generic YAML Adapter
  Status: ✅ APPROVED
  - ADR-NNN (architecture pattern) compliance: ✅
  - Test coverage: 92% (excellent)
  - Security: ✅ ENV validation present
  Minor: Add type hints (low priority)
  Next: Proceed to M3
```

---

### 4. `/fix-bug` - Test-First Bug Fixing ⭐⭐⭐⭐⭐

**Command:** `/fix-bug`
**Location:** `.claude/skills/fix-bug/SKILL.md`
**Purpose:** Systematic bug resolution with proof of fix

**Golden Rule:**
> Before you change production code, write a test that fails because of the bug.

**Process:**
1. **Phase 1: Write failing test** (DO THIS FIRST)
   - Choose test level (unit/integration/acceptance)
   - Reproduce bug in test
   - Verify test FAILS for right reason
   - Commit failing test

2. **Phase 2: Fix the code**
   - Minimal change to pass test
   - Test transitions RED → GREEN
   - Run ALL tests (no regressions)

3. **Phase 3: Commit fix**
   - Document root cause
   - Link to test file

**Benefits:**
- ✅ Proof bug existed
- ✅ Proof bug is fixed
- ✅ Regression prevention
- ✅ Fast feedback (no deployment)
- ✅ Documents the issue

**Example Usage:**
```
User: Bug - API returns 500 for special characters

Agent (Backend-Dev):
  Phase 1: Reproduce bug
  - Created test: tests/test_api_special_chars.py
  - Test FAILS ❌ (assert 500 == 200)
  - Committed failing test

  Phase 2: Fix code
  - Root cause: Missing input sanitization
  - Fixed: Added html.escape() in processor
  - Test PASSES ✅

  Phase 3: Commit fix
  - All tests: 127/127 PASSED ✅
  - Committed with test reference
```

---

### 5. `/spec-create` - Specification Creation ⭐⭐⭐⭐

**Command:** `/spec-create`
**Location:** `.claude/skills/spec-create/SKILL.md`
**Purpose:** Create comprehensive functional specifications

**When to Use:**
- ✅ Complex features spanning multiple components
- ✅ Features requiring cross-team coordination
- ✅ API contracts needing stakeholder agreement
- ✅ Features with security/performance constraints

**Skip For:**
- ❌ Simple CRUD operations
- ❌ Bug fixes (use /fix-bug)
- ❌ Architectural decisions (use ADRs)

**Spec Structure:**
- User story (As a/I want/So that)
- Functional requirements (MoSCoW: MUST/SHOULD/COULD/WON'T)
- Scenarios (Given/When/Then format)
- Constraints and business rules
- Non-functional requirements
- Open questions and decisions
- Acceptance criteria summary
- Traceability (strategic → tactical)

**Lifecycle:**
1. Draft → Review → Approved → Implemented

**Location:** `${SPEC_ROOT}/[domain]/[feature-name].md`

**Example Usage:**
```
User: We need a real-time execution dashboard

Agent (Scribe Sally):
  Creating specification...
  - Feature: Real-Time Execution Dashboard
  - Personas: Software Engineer (primary)
  - Requirements: 8 MUST, 5 SHOULD, 4 COULD, 4 WON'T
  - Scenarios: 6 (4 happy path, 2 error cases)
  - Constraints: <100ms latency, localhost-only
  - Location: ${SPEC_ROOT}/llm-dashboard/real-time-execution-dashboard.md
  Status: DRAFT → Ready for stakeholder review
```

---

### 6. `/self-check` - Self-Observation Protocol ⭐⭐⭐⭐

**Command:** `/self-check`
**Location:** `.claude/skills/self-check/SKILL.md`
**Purpose:** Mid-execution checkpoint to detect drift and course-correct

**Mandatory Checkpoints:**
- 25% task completion (early warning)
- Before delegating tasks to other agents
- After loading 5+ directives or large documents
- When 3+ ⚠️ symbols appear within 10 minutes
- Before marking task complete

**Checkpoint Protocol:**
1. Enter meta-mode
2. Document checkpoint header
3. Run self-observation checklist
4. Pattern recognition (drift/confusion/gold-plating)
5. Course correction
6. Exit meta-mode

**Warning Patterns Detected:**
- Goal drift (scope creep)
- Confusion (uncertainty accumulating)
- Gold-plating (over-engineering)
- Repetition (same approach multiple times)
- Speculation (guessing without validation)
- Mode misuse (wrong reasoning mode)

**Results:**
- ✅ Aligned - Continue
- ⚠️ Corrected - Adjustments made
- ❗️ Blocked - Stop, request guidance

**Example Usage:**
```
Agent: [At 25% completion]

🔄 Self-Check Checkpoint
  Task: Implement GenericYAMLAdapter
  Progress: 3/12 steps (25%)
  Warning: [x] Scope creep (added caching not in requirements)
  Pattern: Gold-plating
  Correction: Removed 45 lines of caching code
  Result: ⚠️ Corrected - Refocused on core requirements
  Resuming: Step 4 - ENV variable expansion
```

---

## Supporting Documentation

### Comprehensive Prompt Template

**`agents/prompts/iteration-orchestration.md`** (1,100+ lines)
- Complete iteration workflow documentation
- Agent handoff patterns
- TDD/ATDD cycle templates
- Quality gates and standards
- Task YAML format specifications
- Troubleshooting guide
- Directory structure reference
- Agent profiles reference
- Best practices and anti-patterns

**`agents/prompts/README.md`**
- Overview of orchestration system
- Usage patterns
- Integration with project structure
- Quality standards
- Customization guide

---

## Skill Relationships

### Typical Workflow

```
1. /status          → Assess current state
2. /iterate         → Execute batch
   ├─ /self-check   → Mid-execution checkpoint (25%, 50%, 75%)
   ├─ /fix-bug      → If bugs encountered
   └─ /spec-create  → If complex feature needs spec first
3. /review          → Architect approval
4. /status          → Check next batch
5. /iterate         → Continue...
```

### Complementary Skills

- **Planning:** `/status` before `/iterate`
- **Quality:** `/self-check` during `/iterate`, `/review` after
- **Problem-Solving:** `/fix-bug` for defects, `/spec-create` for complex features
- **Documentation:** All skills create work logs (Directive 014)

---

## Framework Integration

### Directives Applied

| Skill | Primary Directives |
|-------|-------------------|
| `/iterate` | 014 (Work Logs), 016 (ATDD), 017 (TDD), 019 (File-Based) |
| `/status` | 019 (File-Based Orchestration) |
| `/review` | 018 (Traceable Decisions / ADRs) |
| `/fix-bug` | 017 (TDD), 028 (Bug Fixing Techniques) |
| `/spec-create` | 034 (Spec-Driven Development), 016 (ATDD), 022 (Audience-Oriented) |
| `/self-check` | 024 (Self-Observation Protocol), 020 (Locality of Change) |

### Approaches Referenced

- File-Based Orchestration (${WORKSPACE_ROOT}/collaboration/)
- Test-First Bug Fixing
- Spec-Driven Development
- Ralph Wiggum Loop (Self-Observation)
- Decision-First Development (ADRs)

---

## Usage Statistics (This Session)

**Skills Created:** 6
**Prompt Templates Created:** 1 comprehensive template
**Documentation Created:** 2 README files
**Total Lines Written:** ~3,500 lines
**Time Investment:** ~3 hours
**Value Delivered:** Complete iteration orchestration system

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│ ITERATION ORCHESTRATION SKILLS                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  /status          Check current state, next batch      │
│  /iterate         Execute batch with TDD/ATDD          │
│  /review          Architect code review                │
│  /fix-bug         Test-first bug fixing                │
│  /spec-create     Create feature specification         │
│  /self-check      Mid-execution checkpoint             │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ TYPICAL SESSION:                                        │
│                                                         │
│  1. /status      → "M2 75% complete, 3 tasks in inbox" │
│  2. /iterate     → Execute M2 Batch 2.3                │
│  3. /self-check  → [At 25%, 50%, before completion]    │
│  4. /review      → Alphonso: "✅ APPROVED"             │
│  5. /status      → "M2 100%, ready for M3"             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Next Steps

### Immediate Use

1. Try `/status` to see current project state
2. Use `/iterate` to execute next batch
3. Invoke `/self-check` at 25% completion milestone

### Future Enhancements

Consider creating skills for:
- `/commit` - Structured git commit workflow
- `/pr-create` - Pull request creation with checklist
- `/refactor` - Safe refactoring workflow
- `/deploy` - Deployment checklist and validation

---

**Created By:** Claude Sonnet 4.5
**Date:** 2026-02-06
**Framework:** SDD Agentic Framework + File-Based Orchestration
**Status:** ✅ COMPLETE - All skills operational
