# GitHub Copilot CLI: Skills & Agent Delegation Guide

## Overview

**Yes!** GitHub Copilot CLI has similar capabilities to Claude Code skills, and they're already integrated in this repository. Here's how to use them effectively.

---

## 🎯 Two Ways to Access Specialist Agents

### Method 1: Direct Skill Invocation (Simple Tasks)

I have access to **7 built-in skills** that you can invoke directly:

| Skill | What It Does | When to Use |
|-------|-------------|-------------|
| `delegate` | Route task to specialist agent | Complex multi-step work requiring expertise |
| `fix-bug` | Test-first bug fixing workflow | When you find a bug (writes test first, then fixes) |
| `iterate` | Execute complete iteration cycle | "Run next batch" / orchestration cycles |
| `review` | Architect code review | Before merging, after major implementation |
| `self-check` | Mid-execution self-monitoring | Long tasks (Ralph Wiggum loop checkpoint) |
| `spec-create` | Create functional specification | Complex features needing formal requirements |
| `status` | Assess implementation state | "Where are we?" / progress checks |

**How to invoke:**
```
Just ask naturally:
- "Run the next iteration" → I'll use `iterate` skill
- "Review the dashboard code" → I'll use `review` skill
- "Check my current progress" → I'll use `self-check` skill
- "What's our status?" → I'll use `status` skill
```

---

### Method 2: Custom Agent Delegation (Complex Work)

For specialized work, I can delegate to **25+ custom agents** using the `task` tool:

#### Available Custom Agents

**Strategy & Planning:**
- `project-planner` (Planning Petra) - Roadmaps, milestones, batch planning
- `architect` (Architect Alphonso) - Architecture, ADRs, design review
- `analyst-annie` - Research, analysis, comparative studies

**Implementation:**
- `backend-dev` (Backend Benny) - Python/backend code with TDD
- `python-pedro` - Python specialist (ATDD + TDD workflow)
- `frontend` - UI/UX implementation
- `java-jenny` - Java development specialist

**Documentation & Content:**
- `writer-editor` (Editor Eddy) - Document revision, content editing
- `scribe` - Specification writing, requirements
- `lexical` (Lexical Larry) - Style analysis, tone consistency
- `curator` (Curator Claire) - Directory structure, metadata consistency

**Operations:**
- `build-automation` (DevOps Danny) - CI/CD, automation scripts
- `framework-guardian` - Testing infrastructure, quality gates

**Specialized:**
- `diagrammer` - Architecture diagrams, visual documentation
- `researcher` - Deep research, grounded insights
- `synthesizer` - Multi-agent output integration
- `translator` - Cross-language translation
- `manager` (Manager Mike) - Multi-agent workflow coordination

**How to delegate:**
```
Just tell me what you need:
- "Have Planning Petra assess our status" → I delegate to project-planner
- "Ask Architect Alphonso to review the code" → I delegate to architect
- "Get Backend Benny to implement M3.1" → I delegate to backend-dev
- "Have Analyst Annie research options" → I delegate to analyst-annie
```

---

## 📖 How I Decide Which Method to Use

I automatically choose based on your request:

```
Your Request → My Decision Process
    |
    ├─ Simple, within my capability?
    |  └─> I handle directly (no delegation)
    |
    ├─ Matches a built-in skill?
    |  └─> I invoke the skill (e.g., iterate, review, status)
    |
    └─ Requires specialist expertise?
       └─> I delegate to custom agent (e.g., backend-dev, architect)
```

**Examples:**

| Your Request | What I Do |
|-------------|-----------|
| "What's next?" | Use `status` skill → Quick assessment |
| "Run the next iteration" | Use `iterate` skill → Full orchestration cycle |
| "Review this code" | Delegate to `architect` → Comprehensive ADR-aligned review |
| "Implement telemetry database" | Delegate to `backend-dev` → TDD implementation |
| "Create spec for dashboard" | Use `spec-create` skill → Specification creation |
| "Research alternatives" | Delegate to `analyst-annie` → Deep research |

---

## 🔄 The Skills Already Exported for Copilot

Your repository already has **24 skills exported** for Copilot CLI:

### Prompt Template Skills (7)
Located in `.claude/skills/` as Copilot-compatible format:

1. **architect-adr** - Architect creates ADR
2. **automation-script** - DevOps generates automation
3. **bootstrap-repo** - Bootstrap Bill scaffolds repo
4. **curate-directory** - Curator audits directory
5. **editor-revision** - Editor revises document
6. **lexical-analysis** - Lexical Larry analyzes style
7. **new-agent** - Create new specialist agent

### Approach Skills (17)
Operational patterns and guides:

1. **delegate** - Route to specialist agent
2. **fix-bug** - Test-first bug fixing
3. **iterate** - Complete iteration cycle
4. **review** - Architect code review
5. **self-check** - Ralph Wiggum loop checkpoint
6. **spec-create** - Create specification
7. **status** - Assess implementation state
8. **decision-first-development** - Decision capture workflow
9. **design-diagramming-incremental-detail** - C4 diagramming
10. **file-based-orchestration** - Multi-agent coordination
11. **locality-of-change** - Avoid gold-plating
12. **ralph-wiggum-loop** - Self-observation pattern
13. **spec-driven-development** - SDD PRIMER
14. **target-audience-fit** - Persona-driven writing
15. **test-readability-clarity-check** - Test documentation quality
16. **tooling-setup-best-practices** - Tool selection rigor
17. **trunk-based-development** - Branching strategy

---

## 💡 Natural Language Commands

**You don't need to memorize skill names!** Just ask naturally:

### Planning & Status
```
❌ Don't say: "Invoke status skill and delegate to project-planner"
✅ Do say: "What's our current status on the LLM service?"
```

### Implementation
```
❌ Don't say: "Use task tool with backend-dev agent type"
✅ Do say: "Implement the telemetry database for M3.1"
```

### Review & Quality
```
❌ Don't say: "Invoke review skill and delegate to architect"
✅ Do say: "Review the dashboard implementation"
```

### Iteration & Orchestration
```
❌ Don't say: "Invoke iterate skill with file-based orchestration"
✅ Do say: "Run the next iteration" or "Execute next batch"
```

---

## 🎯 Recommended Phrases for Common Tasks

### Status & Planning
- "What's our current status?"
- "What should we work on next?"
- "Show me the roadmap"
- "Are we on track?"

### Implementation
- "Implement [feature name]"
- "Build the [component] with tests"
- "Fix the bug in [module]"
- "Add [capability] to [component]"

### Review & Quality
- "Review this code"
- "Check if this follows our architecture"
- "Run a self-check"
- "Is this implementation correct?"

### Documentation & Specs
- "Create a spec for [feature]"
- "Document the [component] architecture"
- "Write requirements for [feature]"
- "Explain how [system] works"

### Research & Analysis
- "Research alternatives for [problem]"
- "Compare [option A] vs [option B]"
- "Investigate why [issue]"
- "Analyze [topic]"

---

## 🚀 Examples: How It Works

### Example 1: Status Check
```
You: "What's our status on the dashboard?"

Me: [I recognize: status request]
    → Use `status` skill
    → Delegate to Planning Petra
    
Response:
✅ Dashboard backend: 100% complete (CORS, file watcher, telemetry)
🚧 Dashboard frontend: Needs telemetry data integration
📋 Next: M3 Batch 3.1 (Telemetry Infrastructure, 8-11 hours)
🟢 Health: ON TRACK
```

### Example 2: Implementation Request
```
You: "Implement the telemetry database for M3.1"

Me: [I recognize: backend implementation with TDD]
    → Delegate to `backend-dev` (Backend Benny)
    → TDD workflow automatically applied
    
Response:
[Backend Benny initializes]
Starting M3 Batch 3.1: Telemetry Infrastructure

Phase 1: Write failing tests (RED)
- test_telemetry_database_schema()
- test_invocation_logging()
...
[Implementation proceeds with test-first approach]
```

### Example 3: Code Review
```
You: "Review the dashboard implementation"

Me: [I recognize: architecture review needed]
    → Use `review` skill
    → Delegate to `architect` (Architect Alphonso)
    
Response:
[Architect Alphonso reviews]
✅ ADR-032 Compliance: Follows real-time dashboard design
✅ Test Coverage: 37/37 tests passing (100%)
✅ Security: Localhost-only default, CORS configured
⚠️ Consideration: Telemetry data integration pending (M3.1)
```

### Example 4: Next Iteration
```
You: "Run the next iteration"

Me: [I recognize: orchestration cycle]
    → Use `iterate` skill
    → Multi-agent coordination:
      1. Planning Petra reads NEXT_BATCH.md
      2. Backend Benny executes tasks
      3. Architect Alphonso reviews
      4. Planning Petra updates roadmap
      5. Manager Mike provides summary
```

---

## 📂 Where Skills Are Stored

**Claude Code Skills:** `.claude/skills/` (exported for cross-tool compatibility)
**Copilot Skills:** Loaded from custom instructions (available automatically)
**Agent Profiles:** `.github/agents/*.agent.md`
**Approaches:** `.github/agents/approaches/*.md`
**Directives:** `.github/agents/directives/*.md`

---

## 🔧 Extending the Skills

Want to add a new skill? Two options:

### Option 1: Add to Custom Instructions
Edit `.github/copilot/custom-instructions.md` and add to the skills list.

### Option 2: Create New Agent Profile
```bash
# Use the new-agent skill
You: "Create a new agent for [domain]"

Me: [Uses new-agent skill]
    → Delegates to Manager Mike
    → Creates .github/agents/[name].agent.md
    → Exports to .claude/skills/ and Copilot format
```

---

## 🎓 Best Practices

### DO ✅
- **Ask naturally** - I understand context and intent
- **Trust delegation** - I'll route to the right specialist
- **Provide context** - "Review dashboard code for M4.2" is better than "review code"
- **Use iteration commands** - "Run next iteration" triggers full orchestration

### DON'T ❌
- **Don't micromanage routing** - I know which agent to use
- **Don't memorize skill names** - Natural language works
- **Don't skip context** - "What's the status?" is vague vs "What's our M3 status?"
- **Don't bypass skills** - "Run iteration" is better than manually coordinating agents

---

## 🆘 Quick Reference Card

| I Want To... | Just Say... |
|--------------|-------------|
| Check progress | "What's our status?" |
| Run next batch | "Run the next iteration" |
| Review code | "Review [component]" |
| Fix a bug | "Fix the bug in [module]" |
| Create spec | "Create spec for [feature]" |
| Research options | "Research alternatives for [problem]" |
| Implement feature | "Implement [feature] with tests" |
| Mid-task check | "Run a self-check" or "Am I on track?" |

---

## 🔗 Related Documentation

- **Skills Export:** `ops/skills-exporter.js` - How skills are generated
- **Agent Profiles:** `.github/agents/directives/005_agent_profiles.md`
- **Delegation Approach:** `.github/agents/approaches/agent-profile-handoff-patterns.md`
- **Custom Instructions:** `.github/copilot/custom-instructions.md`
- **Iterate Command:** `.github/agents/prompts/iteration-orchestration.md`

---

**TL;DR:** Just talk to me naturally. I'll figure out which skill or agent to use based on your request. The framework is already set up—you don't need to know the implementation details! 🚀
