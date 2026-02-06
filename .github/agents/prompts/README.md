# Agent Prompts Directory

**Purpose:** Reusable prompt templates for multi-agent orchestration workflows.

---

## Overview

This directory contains comprehensive prompt templates that support file-based orchestration with multi-agent coordination. These templates are referenced by skills in `.claude/skills/` to provide consistent, repeatable workflows.

## Available Prompts

### `iteration-orchestration.md`

**Purpose:** Multi-agent iteration cycle orchestration
**Skills Using This:** `/iterate`, `/status`, `/review`
**Version:** 1.0.0

**Provides:**
- Complete iteration workflow (planning → execution → review)
- Agent handoff patterns
- TDD/ATDD cycle templates
- Quality gate definitions
- Work log templates
- SWOT analysis of the approach

**Key Workflows:**
- **Standard Iteration** (`/iterate`): Planning Petra → Specialist Agents → Review Setup
- **Status Check** (`/status`): Current state assessment, blockers, next batch recommendation
- **Architect Review** (`/review`): Code review with ADR compliance, coverage analysis, recommendations

---

## Usage Patterns

### Starting a New Session

```
User: /status
Agent (Petra): [Assesses current state, identifies next batch]

User: /iterate
Agent (Petra → Specialists → Petra): [Executes batch with TDD/ATDD]
```

### Full Cycle with Review

```
User: /iterate
Agent: [Completes batch, creates review task]

User: /review
Agent (Alphonso): [Reviews, outputs APPROVED/REDIRECT/BLOCKED]

User: /iterate
Agent: [Next batch...]
```

### Quick Status Check

```
User: /status
Agent (Petra):
  Current: M2 Tool Integration - 75%
  Inbox: 3 tasks (2 high, 1 medium)
  Next: M2 Batch 2.3 (2 tasks, ~5h)
  Health: ON TRACK
```

---

## Integration with Project Structure

### Skills Reference Prompts

Skills in `.claude/skills/` reference these templates:

```
.claude/skills/iterate/SKILL.md
  ↓ (uses workflow from)
agents/prompts/iteration-orchestration.md
```

### Directives Applied

These prompts implement several framework directives:

- **Directive 014:** Work Log Creation
- **Directive 016:** Acceptance Test-Driven Development (ATDD)
- **Directive 017:** Test-Driven Development (TDD)
- **Directive 018:** Traceable Decisions (ADRs)
- **Directive 019:** File-Based Orchestration

### Directory Integration

```
project-root/
├── agents/
│   └── prompts/              ← THIS DIRECTORY
│       ├── README.md         ← You are here
│       └── iteration-orchestration.md
│
├── .claude/skills/           ← Skills reference prompts
│   ├── iterate/
│   ├── status/
│   └── review/
│
├── work/collaboration/       ← Task files (YAML)
│   ├── inbox/
│   ├── assigned/<agent>/
│   └── done/<agent>/
│
└── work/reports/            ← Outputs from workflows
    ├── logs/<agent>/        ← Work logs (Directive 014)
    └── reviews/             ← Code reviews (Architect)
```

---

## Agent Roles

### Coordinator Agents

**Planning Petra** (`/status`, `/iterate`)
- Assesses current state
- Identifies next batch
- Updates planning artifacts
- Provides executive summaries

**Architect Alphonso** (`/review`)
- Code review and architecture-fit analysis
- ADR compliance verification
- Quality gate enforcement

### Specialist Agents

**Backend Benny** (`backend-dev`)
- Python/Java implementation
- APIs, services, backend logic
- Database integration

**Frontend Freddy** (`frontend-dev`)
- UI implementation
- JavaScript/TypeScript
- React/Vue components

**DevOps Danny** (`devops`)
- Build automation
- CI/CD pipelines
- Infrastructure scripts

**Writer-Editor** (`writer-editor`)
- Documentation
- User guides
- API documentation

**Scribe Sally** (`scribe`)
- Specifications
- Requirements
- Acceptance criteria

---

## Quality Standards

### Test Coverage Targets

| Component | Minimum | Target | Excellent |
|-----------|---------|--------|-----------|
| Unit Tests | 70% | 80% | 90%+ |
| Integration Tests | 60% | 70% | 80%+ |
| Critical Paths | 90% | 95% | 100% |

### TDD Cycle (Non-Negotiable)

1. **RED:** Write failing test first
2. **GREEN:** Implement minimum code to pass
3. **REFACTOR:** Improve code quality

**Never skip tests.** Tests define "done."

### Work Log Requirements (Directive 014)

Every completed task requires a work log:

- **Location:** `work/reports/logs/<agent>/YYYY-MM-DD-<topic>.md`
- **Content:** Decisions, challenges, time metrics, references
- **Purpose:** Context preservation for future sessions

---

## Customization

### Adding New Workflows

To add a new orchestration workflow:

1. Create template in `agents/prompts/<workflow-name>.md`
2. Document workflow steps, agent handoffs, quality gates
3. Create skill in `.claude/skills/<skill-name>/SKILL.md`
4. Reference template in skill's "References" section
5. Update this README with workflow description

### Adapting for Different Tech Stacks

**Python Projects:**
- Test command: `pytest tests/ --cov=src --cov-report=term-missing`
- Coverage tool: pytest-cov

**Java Projects:**
- Test command: `mvn test`
- Architecture tests: `mvn test -Dtest="ArchitectureTest"`
- Mutation testing: `mvn test -Pmutation`

**JavaScript Projects:**
- Test command: `npm test -- --coverage`
- Coverage tool: Jest or Vitest

---

## Best Practices

### Do ✅

- Start sessions with `/status` to understand current state
- Keep batches small (2-4 tasks max)
- Follow TDD religiously (RED → GREEN → REFACTOR)
- Create work logs for every completed task
- Run quality gates after each batch
- Request architect review for significant changes

### Don't ❌

- Skip tests ("I'll add them later" never works)
- Create large batches (>4 tasks becomes unmanageable)
- Ignore blockers (address immediately)
- Skip work logs (context loss is expensive)
- Proceed without reviews on architectural changes
- Make ad-hoc changes outside orchestration flow

---

## Troubleshooting

### "No tasks in inbox/"

**Solution:** Check if tasks are in `assigned/` or create new tasks manually.

### "Tests failing after implementation"

**Solution:** Follow TDD - tests should pass incrementally during GREEN phase, not all at the end.

### "Batch taking longer than estimated"

**Solution:** Break into smaller batches (2-3 tasks max), re-estimate remaining work.

### "Don't know which agent to use"

**Solution:** Check Agent Roles section above, or use `/status` to see task assignments.

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-02-06 | Initial creation with iteration orchestration template | Claude Sonnet 4.5 |

---

## References

**Framework Documentation:**
- AGENTS.md specification
- Directive 019: File-Based Orchestration (`.github/agents/directives/019_file_based_collaboration.md`)
- Work Directory Orchestration Approach (`.github/agents/approaches/work-directory-orchestration.md`)

**External Inspiration:**
- Regnology helpertools: `quality_check/agents/prompts/iteration-orchestration.md`
- SDD Agentic Framework patterns

---

_Maintained by: Multi-agent coordination team_
_Framework: SDD Agentic Framework + File-Based Orchestration_
