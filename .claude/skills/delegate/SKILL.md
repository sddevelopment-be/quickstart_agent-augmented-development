---
name: "delegate"
description: "Delegate task to specialist agent when expertise required: Initialize as specialist (Planning Petra, Backend Benny, Architect Alphonso, etc.) OR spawn sub-agent if available. Use when task requires specialized knowledge in agent's core focus area."
version: "1.0.0"
type: "coordination"
category: "agent-handoff"
---

# Delegate: Specialist Agent Handoff

Recognize when a task requires specialist expertise and delegate by initializing as the appropriate specialist agent OR spawning a sub-agent (if Task tool available).

## Instructions

### Step 1: Recognize Delegation Trigger

**Delegate when task requires:**
- Specialized domain knowledge (architecture, planning, backend, frontend, etc.)
- Agent-specific workflows or methodologies
- Access to agent-specific context or tools
- Expertise beyond generalist capabilities

**Do NOT delegate when:**
- Task is simple and within current capability
- Overhead of delegation exceeds task complexity
- Current agent can complete efficiently

---

### Step 2: Identify Specialist Agent

| Agent | Alias | Core Focus | When to Delegate |
|-------|-------|------------|------------------|
| **Planning Petra** | `planning-petra` | Coordination, roadmaps, status tracking | Planning, batch creation, progress assessment, executive summaries |
| **Architect Alphonso** | `architect` | Architecture, ADRs, design review | Code review, architectural decisions, ADR creation, design validation |
| **Backend Benny** | `backend-dev` | Backend implementation | Python/Java code, APIs, services, database, backend tests |
| **Frontend Freddy** | `frontend-dev` | Frontend implementation | UI code, JavaScript/TypeScript, React/Vue, styling, frontend tests |
| **Scribe Sally** | `scribe` | Specification writing | Feature specs, requirements, acceptance criteria, traceability |
| **Analyst Annie** | `analyst` | Research, analysis | Investigations, comparative studies, data analysis, retrospectives |
| **Writer-Editor** | `writer-editor` | Documentation | User guides, API docs, technical writing, content editing |
| **DevOps Danny** | `devops` | Automation, CI/CD | Build scripts, deployment, infrastructure, pipeline configuration |
| **Framework Guardian** | `framework-guardian` | Testing infrastructure | Test frameworks, CI setup, quality gates, test architecture |
| **Lexical Larry** | `lexical` | Style, tone, editing | Lexical analysis, style consistency, minimal edits |
| **Curator Claire** | `curator` | Artifact maintenance | Directory curation, normalization, consistency checks |
| **Editor Eddy** | `editor` | Content revision | Document revision, tone refinement, clarity improvements |

---

### Step 3: Choose Delegation Method

#### Option A: Spawn Sub-Agent (Preferred if available)

**Use Task tool to spawn specialist:**

```
Use Task tool with appropriate subagent_type:

Examples:
- subagent_type="Plan" for architecture planning
- subagent_type="Explore" for codebase research
- subagent_type="backend-benny" for backend implementation
- subagent_type="architect-alphonso" for review

Benefits:
- Parallel execution possible
- Preserves main context
- Clean separation of concerns
```

**Example:**
```
User: "Create an ADR for the dashboard architecture"

Agent: [Recognizes: Architect expertise needed]

Action: Spawn sub-agent
  - Task tool: subagent_type="architect-alphonso"
  - Prompt: "Create ADR-032 for Real-Time Execution Dashboard"
  - Run in background if desired

Result: Architect Alphonso creates ADR in parallel
```

#### Option B: Initialize as Specialist (Fallback)

**When Task tool not available or synchronous execution needed:**

```markdown
## Agent Initialization

**Transitioning to:** [Specialist Agent Name]
**Reason:** [Why delegation needed]
**Original Context:** [Brief summary to preserve]

---

[Continue as specialist agent with their perspective and expertise]
```

**Example:**
```
User: "Review the GenericYAMLAdapter implementation"

Agent: This requires architecture expertise and code review skills.
  Delegating to Architect Alphonso...

## Agent Initialization

**Transitioning to:** Architect Alphonso
**Reason:** Code review requires architectural validation against ADR-029
**Original Context:** GenericYAMLAdapter implementation complete (M2 Batch 2.3)

---

[Now operating as Architect Alphonso]

Reviewing GenericYAMLAdapter against ADR-029 (Adapter Interface Design)...

✅ ADR Compliance: Follows base adapter pattern correctly
✅ Test Coverage: 92% (excellent)
✅ Security: ENV variable validation present
...
```

---

## Delegation Patterns

### Pattern 1: Planning Request

**Trigger:** "What's our current status?" or "What should we work on next?"

**Delegate to:** Planning Petra

**Example:**
```
User: What's our current progress on the LLM-service layer?

Agent: This requires Planning Petra's coordination expertise.

## Agent Initialization

**Transitioning to:** Planning Petra
**Reason:** Status assessment and progress tracking

---

[Now as Planning Petra]

Assessing LLM-service layer progress:
- Current: M2 Tool Integration - 100% complete ✅
- Next: M3 Telemetry Infrastructure - 0/3 tasks
- Overall: 45% complete (M1-M2 done, M3-M4 remaining)
- Health: 🟢 ON TRACK
...
```

### Pattern 2: Architecture Review

**Trigger:** "Review this code" or "Is this architecture sound?"

**Delegate to:** Architect Alphonso

**Example:**
```
User: Review the dashboard implementation

Agent: Code review requires Architect Alphonso's expertise.

[Spawn sub-agent with Task tool OR initialize as Alphonso]

Result: Comprehensive review with ADR compliance, test coverage,
        security analysis, recommendations
```

### Pattern 3: Implementation Request

**Trigger:** "Implement feature X" or "Fix this bug"

**Delegate to:** Backend Benny / Frontend Freddy

**Example:**
```
User: Implement the GenericYAMLAdapter with ENV support

Agent: Backend implementation task detected.
  Delegating to Backend Benny...

## Agent Initialization

**Transitioning to:** Backend-dev Benny
**Reason:** Python implementation with TDD

---

[Now as Backend Benny]

Starting M2 Batch 2.3: GenericYAMLAdapter

Phase 1: Write failing tests (TDD RED phase)...
```

### Pattern 4: Specification Creation

**Trigger:** "Create a spec for feature X" or "Define requirements"

**Delegate to:** Scribe Sally or Analyst Annie

**Example:**
```
User: Create specification for real-time dashboard

Agent: Specification writing requires Scribe Sally's expertise.

[Initialize as Scribe Sally]

Creating specification: Real-Time Execution Dashboard
- User story: As a Software Engineer, I want real-time visibility...
- Requirements: 21 total (8 MUST, 5 SHOULD, 4 COULD, 4 WON'T)
- Scenarios: 6 (Given/When/Then format)
- Location: specifications/llm-dashboard/real-time-execution-dashboard.md
```

### Pattern 5: Research & Analysis

**Trigger:** "Investigate X" or "Analyze Y" or "Compare options"

**Delegate to:** Analyst Annie or Researcher Ralph

**Example:**
```
User: Compare our dashboard approach to spec-kitty

Agent: Comparative analysis requires Analyst Annie's research skills.

[Spawn Explore sub-agent OR initialize as Analyst Annie]

Result: 51KB comparative analysis document with:
- Feature comparison table
- Architectural patterns
- Top 5 learnings with ROI
- Integration opportunities
```

---

## Delegation Decision Tree

```
User Request
    |
    ├─ Planning/Status/Coordination?
    |  └─> Delegate to Planning Petra
    |
    ├─ Architecture/Review/ADR?
    |  └─> Delegate to Architect Alphonso
    |
    ├─ Implementation (Backend)?
    |  └─> Delegate to Backend Benny
    |
    ├─ Implementation (Frontend)?
    |  └─> Delegate to Frontend Freddy
    |
    ├─ Specification/Requirements?
    |  └─> Delegate to Scribe Sally
    |
    ├─ Research/Analysis/Investigation?
    |  └─> Delegate to Analyst Annie
    |
    ├─ Documentation/Writing?
    |  └─> Delegate to Writer-Editor
    |
    ├─ CI/CD/Automation?
    |  └─> Delegate to DevOps Danny
    |
    ├─ Style/Editing?
    |  └─> Delegate to Lexical Larry
    |
    └─ Simple/General?
       └─> Handle directly (no delegation)
```

---

## Best Practices

### When to Delegate ✅

- **Specialized Knowledge Required:** Architecture, planning, testing frameworks
- **Domain Expertise Needed:** Backend vs. frontend, infrastructure vs. application
- **Methodology-Specific Work:** TDD (Backend Benny), ADRs (Architect), specs (Scribe)
- **Agent-Specific Context:** Access to agent's work history, patterns, decisions

### When NOT to Delegate ❌

- **Simple Tasks:** Reading a file, answering basic questions
- **Current Agent Capable:** Task within generalist capabilities
- **Excessive Overhead:** Delegation takes longer than doing task
- **No Clear Specialist:** Task doesn't map to any agent's core focus

### Delegation Hygiene

1. **Clear Handoff:**
   - Explain WHY delegating
   - Summarize relevant context
   - State expected outcome

2. **Preserve Context:**
   - Document original request
   - Note key constraints or preferences
   - Link related artifacts

3. **Return to Original:**
   - After specialist work complete
   - Summarize what was done
   - Continue original conversation flow

---

## Anti-Patterns

❌ **Delegation Ping-Pong:**
- Bouncing between agents without progress
- Solution: Identify correct agent upfront

❌ **Over-Delegation:**
- Delegating trivial tasks
- Solution: Handle simple work directly

❌ **Under-Delegation:**
- Attempting work beyond expertise
- Solution: Recognize when specialist needed

❌ **Context Loss:**
- Delegating without preserving context
- Solution: Include relevant background in handoff

---

## Integration with Skills

**Use with:**
- `/iterate` - Delegates to specialists during batch execution
- `/review` - Delegates to Architect Alphonso
- `/status` - Delegates to Planning Petra
- `/fix-bug` - Delegates to Backend/Frontend dev
- `/spec-create` - Delegates to Scribe Sally

**Example Combined Usage:**
```
User: /iterate

[Planning Petra]: Assesses state, identifies next batch
[Backend Benny]: Executes implementation tasks with TDD
[Planning Petra]: Updates artifacts, provides summary
[Architect Alphonso]: Reviews code (delegated)
```

---

## References

- **Approach:** `.github/agents/approaches/agent-profile-handoff-patterns.md`
- **Agent Profiles:** `.github/agents/directives/005_agent_profiles.md`
- **Role Capabilities:** `.github/agents/directives/009_role_capabilities.md`
- **Prompt Template:** `agents/prompts/iteration-orchestration.md` (Agent Profiles section)
