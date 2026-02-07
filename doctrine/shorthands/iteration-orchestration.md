# Iteration Orchestration Prompt Template

**Version:** 1.0.0
**Created:** 2026-02-06
**Purpose:** Streamline multi-agent iteration cycles following the file-based orchestration approach

---

## Quick Reference

### Standard Iteration Command

```
/iterate
```

**Expands to:**

> Acting as the orchestrator in the file-based agent collaboration approach, execute a batch of work by:
> 1. Initialize as Planning Petra and assess current work/collaboration/ state
> 2. Identify next batch from work/collaboration/inbox/ (priority order)
> 3. For each task: initialize as specialist agent, execute with TDD/ATDD
> 4. Adhere to directives 014 (work logs), 016 (ATDD), 017 (TDD)
> 5. When complete, initialize as Petra and update planning artifacts
> 6. Provide executive summary with metrics
> 7. Create task for Architect Alphonso to conduct review (if significant changes)

---

## Command Aliases

### `/iterate` - Full Iteration Cycle

Executes one complete batch: planning → execution → documentation → review setup.

**Full Prompt:**
```markdown
Acting as orchestrator in file-based agent collaboration, execute a batch:

1. Planning Petra: Assess current state
   - Read work/collaboration/inbox/ for pending tasks
   - Identify next batch (check NEXT_BATCH.md if exists)
   - Priority order: critical > high > medium > low

2. Execute batch (specialist agents):
   For each task in batch (priority descending):
   a. Initialize as assigned agent (backend-dev, architect, etc.)
   b. Follow TDD/ATDD: RED → GREEN → REFACTOR
   c. Run tests: ensure all passing before proceeding
   d. Move completed task from inbox/ to done/<agent>/
   e. Create work log (directive 014)

3. Planning Petra: Update artifacts
   - Update roadmap if exists (docs/architecture/roadmap-*.md)
   - Update NEXT_BATCH.md with next priorities
   - Document any blockers or decisions

4. Provide executive summary:
   - Tasks completed (with time estimates vs actual)
   - Tests passing (coverage %)
   - Decisions made or deferred
   - Blockers identified
   - Next recommended batch

5. Review gate (conditional):
   - If significant architectural changes: create Alphonso review task
   - If routine implementation: proceed to next batch
```

### `/iterate-reviewed` - Iteration with Immediate Review

Same as `/iterate` but Alphonso review executes immediately after batch completion.

**Full Prompt:**
```markdown
Acting as orchestrator, execute batch with immediate review:

1. Planning Petra: Assess state and identify batch
2. Execute batch as specialist agents (TDD/ATDD)
3. Planning Petra: Update artifacts + executive summary
4. Architect Alphonso: Execute code review immediately
   - Check ADR alignment
   - Verify test coverage (>80% target)
   - Validate architectural fit
   - Document in work/reports/reviews/
5. Planning Petra: If approved, prepare next batch recommendation

Quality gates:
- All tests passing
- Coverage >80%
- Architecture tests passing (if applicable)
- No blocking issues identified
```

### `/review` - Architect Review Only

**Full Prompt:**
```markdown
Initialize as Architect Alphonso. Conduct rigorous code review and architecture-fit analysis:

1. Review recent changes (check git log or work logs)
2. Validate against relevant ADRs (docs/architecture/adrs/)
3. Check test coverage and quality
4. Verify architectural patterns and best practices
5. Document findings in work/reports/reviews/<date>-<topic>-review.md

Focus areas:
- ADR compliance
- Test coverage (target >80%)
- Separation of concerns
- Security considerations
- Performance implications

Output: Review document with APPROVED/REDIRECT/BLOCKED status and recommendations
```

### `/status` - Planning Status Check

**Full Prompt:**
```markdown
Initialize as Planning Petra. Assess current implementation state:

1. Check active branch and git status
2. List work/collaboration/inbox/ (pending tasks)
3. List work/collaboration/assigned/ (in-progress tasks)
4. Read planning documents if present:
   - docs/architecture/roadmap-*.md
   - work/collaboration/NEXT_BATCH.md
   - work/planning/*.md
5. Review recent work logs (work/reports/logs/)

Provide executive summary:
- Current milestone/phase progress (% complete)
- Active tasks (agent, priority, estimate)
- Completed tasks (this session)
- Blockers or decisions needed
- Next recommended batch
- Overall project health: ON TRACK / AT RISK / BLOCKED
```

---

## Full Iteration Workflow

### Complete Cycle Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ START: /iterate                                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ Planning Petra: Status Assessment                           │
│ - Read work/collaboration/inbox/                            │
│ - Identify next batch (priority order)                      │
│ - Check NEXT_BATCH.md if exists                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ For Each Task in Batch (Priority Descending):               │
│                                                              │
│ 1. Initialize as Specialist Agent                           │
│    (backend-dev, architect, frontend, writer, etc.)         │
│                                                              │
│ 2. TDD/ATDD Cycle:                                          │
│    RED: Write failing test                                  │
│    GREEN: Implement minimum code to pass                    │
│    REFACTOR: Improve code quality                           │
│                                                              │
│ 3. Validation:                                              │
│    - Run all tests (must pass)                              │
│    - Check coverage (target >80%)                           │
│    - Verify linting/formatting                              │
│                                                              │
│ 4. Documentation:                                           │
│    - Create work log (directive 014)                        │
│    - Update relevant docs                                   │
│    - Move task: inbox/ → done/<agent>/                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ Planning Petra: Update Planning Artifacts                   │
│ - Update roadmap progress                                   │
│ - Update NEXT_BATCH.md with next priorities                 │
│ - Document decisions/blockers                               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ Executive Summary (Petra)                                   │
│ - Batch completion metrics                                  │
│ - Time: estimated vs actual                                 │
│ - Quality: test coverage, passing rate                      │
│ - Blockers: identified issues                               │
│ - Next: recommended batch                                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌──────────────┐   ┌──────────────────┐
│ Significant  │   │ Routine          │
│ Changes?     │   │ Implementation?  │
└──────┬───────┘   └────────┬─────────┘
       │ YES                │ NO
       ▼                    │
┌──────────────────┐        │
│ Create Review    │        │
│ Task for Alphonso│        │
└──────────────────┘        │
                            │
┌───────────────────────────┴────────┐
│ COMPLETE: Ready for next /iterate  │
└────────────────────────────────────┘
```

---

## Agent Profiles Reference

| Agent | Directory Alias | Specialty | Typical Tasks |
|-------|----------------|-----------|---------------|
| Planning Petra | `planning-petra` | Coordination, roadmaps, status | Batch planning, progress tracking, executive summaries |
| Backend Benny | `backend-dev` | Backend implementation | Python/Java code, APIs, services, tests |
| Architect Alphonso | `architect` | Design, review, ADRs | Code review, architecture decisions, ADR authoring |
| Frontend Freddy | `frontend-dev` | Frontend implementation | UI, JavaScript/TypeScript, React/Vue, styling |
| Writer-Editor | `writer-editor` | Documentation | User guides, API docs, technical writing |
| Scribe Sally | `scribe` | Specification docs | Requirements, acceptance criteria, traceability |
| DevOps Danny | `devops` | Automation, CI/CD | Build scripts, deployment, infrastructure |
| Framework Guardian | `framework-guardian` | Testing, quality | Test frameworks, CI setup, quality gates |

---

## Directory Structure

### Standard Layout

```
project-root/
├── agents/
│   ├── prompts/               # Reusable prompt templates (THIS FILE)
│   └── GLOSSARY.md            # Agent terminology reference
│
├── .github/
│   └── agents/
│       ├── directives/        # Operational directives
│       └── approaches/        # Methodology documentation
│
├── docs/
│   ├── architecture/
│   │   ├── adrs/              # Architecture Decision Records
│   │   ├── design/            # Design documents
│   │   └── roadmap-*.md       # Feature roadmaps
│   └── planning/
│       ├── PLAN_OVERVIEW.md   # Strategic overview (optional)
│       └── NEXT_BATCH.md      # Current/next batch (optional)
│
├── work/
│   ├── collaboration/
│   │   ├── inbox/             # Pending tasks (YAML)
│   │   ├── assigned/<agent>/  # In-progress tasks
│   │   └── done/<agent>/      # Completed tasks
│   │
│   ├── reports/
│   │   ├── logs/<agent>/      # Work logs (directive 014)
│   │   └── reviews/           # Code review documents
│   │
│   └── analysis/              # Research, investigations
│
└── tests/                     # Test suite
    ├── unit/
    ├── integration/
    └── acceptance/
```

---

## Task YAML Format

### Standard Task File

```yaml
# work/collaboration/inbox/2026-02-06T1000-backend-dev-feature-name.yaml

id: "2026-02-06T1000-backend-dev-feature-name"
title: "Implement feature X"
agent: "backend-dev"
priority: "high"  # critical | high | medium | low
status: "new"     # new | assigned | in_progress | done | blocked
estimated_hours: 3
tags: ["feature", "m2-batch-2.1"]

description: |
  Detailed description of the task, including context,
  requirements, and acceptance criteria.

acceptance_criteria:
  - "Test coverage >80%"
  - "All unit tests passing"
  - "Integration tests passing"
  - "Work log created"

dependencies: []  # List of task IDs that must complete first

notes: |
  Additional context, references, or clarifications.
```

---

## Directives Reference

### Key Directives for Iterations

**Directive 014: Work Log Creation**
- Create timestamped work log after task completion
- Location: `work/reports/logs/<agent>/YYYY-MM-DD-<topic>.md`
- Include: decisions, challenges, time metrics, references

**Directive 016: Acceptance Test-Driven Development (ATDD)**
- Write acceptance tests FIRST (Given/When/Then)
- Tests define "done" criteria
- Implement to satisfy acceptance tests

**Directive 017: Test-Driven Development (TDD)**
- Write unit tests FIRST (RED phase)
- Implement minimum code to pass (GREEN phase)
- Refactor for quality (REFACTOR phase)
- Never skip tests

**Directive 018: Traceable Decisions (ADRs)**
- Document significant architectural decisions
- ADR format: Context → Decision → Consequences
- Location: `docs/architecture/adrs/ADR-NNN-title.md`

**Directive 019: File-Based Collaboration**
- Tasks as YAML files in `work/collaboration/`
- Lifecycle: inbox → assigned → done
- Git audit trail preserved

---

## Quality Gates

### Test Coverage Targets

| Component | Minimum | Target | Excellent |
|-----------|---------|--------|-----------|
| Unit Tests | 70% | 80% | 90%+ |
| Integration Tests | 60% | 70% | 80%+ |
| Critical Paths | 90% | 95% | 100% |

### Test Commands (Common)

**Python:**
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

**Java (Maven):**
```bash
mvn test                                  # Full test suite
mvn test -Dtest="ArchitectureTest"        # Architecture rules
mvn test -Pmutation                       # Mutation testing (slow)
```

**JavaScript (npm):**
```bash
npm test -- --coverage
```

---

## Example Usage Session

### Typical Iteration Flow

```
User: /status
Agent (Petra):
  Current: M2 Tool Integration - 75% complete
  Inbox: 3 tasks (2 high, 1 medium)
  Next batch: M2 Batch 2.3 - Generic YAML Adapter (2 tasks)
  Health: ON TRACK

User: /iterate
Agent (Petra): Starting M2 Batch 2.3...
Agent (Backend-Dev): [Implements GenericYAMLAdapter with TDD]
Agent (Backend-Dev): [Creates tests, implements, refactors]
Agent (Petra):
  ✅ Batch complete (2/2 tasks, 3.5h actual vs 5h estimated)
  ✅ 24 tests passing, 82% coverage
  ✅ Work logs created
  📊 M2 Tool Integration now 100% complete
  🎯 Next: M3 Telemetry Infrastructure

User: /review
Agent (Alphonso):
  ✅ APPROVED - Architecture aligned with ADR-029
  ✅ Test coverage excellent (82%)
  ✅ Generic approach validated
  📝 Minor: Consider adding type hints for Python 3.10+
  🟢 Proceed to M3

User: /iterate
Agent (Petra): Starting M3 Batch 3.1...
[Next iteration begins...]
```

---

## Tips for Effective Iterations

### Best Practices

1. **Start with `/status`** - Always understand current state before iterating
2. **One batch at a time** - Don't combine multiple phases
3. **TDD is non-negotiable** - Write tests first, always
4. **Review gates are checkpoints** - Don't skip architectural reviews
5. **Work logs preserve context** - Essential for long-term projects
6. **Keep batches small** - 2-4 tasks max per iteration
7. **Document decisions** - Create ADRs for significant choices

### Anti-Patterns to Avoid

❌ **Skipping tests** - "I'll add tests later" never works
❌ **Large batches** - More than 4 tasks becomes unmanageable
❌ **Ignoring blockers** - Address issues immediately, don't defer
❌ **No work logs** - Context loss is expensive
❌ **Skipping reviews** - Architecture drift compounds over time
❌ **Ad-hoc changes** - Follow the file-based orchestration flow

---

## SWOT Analysis

### Strengths ✅
- **Structured:** Clear agent roles, lifecycle, handoffs
- **Traceable:** Work logs, ADRs, Git history
- **Quality-focused:** TDD + ATDD + architecture tests
- **Flexible:** Stop/resume at batch boundaries
- **Visible:** All work in Git, no external tools required

### Weaknesses ⚠️
- **Overhead:** Planning updates per iteration
- **Context-dependent:** Requires reading planning docs
- **Manual coordination:** No automation of task assignment

### Opportunities 💡
- **Command aliases:** Reduce prompt length (this file!)
- **Automation:** Script common validation sequences
- **Templates:** Standardize task YAML generation
- **Metrics:** Track velocity, quality trends over time

### Threats 🔴
- **Context loss:** Long sessions may lose state
- **Scope creep:** Batches expand without bounds
- **Review bottleneck:** Architect review blocks progress
- **Test debt:** Skipping TDD creates technical debt

---

## Troubleshooting

### Common Issues

**Issue:** "No tasks in inbox/"
- **Solution:** Run `/status` to check if tasks are in `assigned/` or create new tasks

**Issue:** "Tests failing after implementation"
- **Solution:** Follow TDD - tests should pass incrementally, not all at end

**Issue:** "Batch taking longer than estimated"
- **Solution:** Break into smaller batches (2-3 tasks max), re-estimate

**Issue:** "Don't know which agent to use"
- **Solution:** Check Agent Profiles Reference table above

**Issue:** "Architecture review blocking progress"
- **Solution:** Address review feedback first, don't proceed with unresolved issues

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-02-06 | Initial creation from external template and project needs | Claude Sonnet 4.5 |

---

_Template created for: quickstart_agent-augmented-development_
_Based on:_
- _External reference: iteration-orchestration.md (Regnology helpertools)_
- _SDD Agentic Framework_
- _Directive 019: File-Based Orchestration_
- _AGENTS.md specification_
