# Manager Mike Orchestration - Quick Reference

## When to Use Orchestration

Use Manager Mike's orchestration when you need to coordinate a **multi-phase spec-driven development cycle** from initial specification through deployment.

### Typical Triggers
- "Coordinate spec-to-deployment cycle for [initiative]"
- "Orchestrate feature development for [requirement]"
- "Manage full lifecycle for [specification]"
- "Track implementation cycle for [ADR]"

---

## The 6-Phase Cycle

```
[1] SPECIFICATION     → Analyst Annie creates functional spec
[2] ARCHITECTURE      → Architect Alphonso reviews design
[3] PLANNING          → Planning Petra breaks down tasks
[4] IMPLEMENTATION    → Backend/Frontend build feature
[5] CODE REVIEW       → Code Reviewer Cindy approves changes
[6] INTEGRATION       → Backend/DevOps deploy to production
```

---

## How to Request Orchestration

**Simple format:**
```
@manager-mike: Orchestrate [initiative name]
- Initiative: [brief description]
- Priority: [high/medium/low]
- Constraints: [timeline, dependencies, etc.]
```

**Example:**
```
@manager-mike: Orchestrate user authentication feature
- Initiative: Add OAuth 2.0 authentication to API
- Priority: High
- Constraints: Must integrate with existing session management
```

---

## What Mike Does (Delegation)

✅ **Mike WILL:**
- Create specification task for Analyst Annie
- Route approved spec to Architect Alphonso
- Coordinate planning with Planning Petra
- Track implementation progress
- Trigger code review with Code Reviewer Cindy
- Manage integration handoff
- Update AGENT_STATUS.md at phase transitions
- Surface blockers immediately

❌ **Mike WILL NOT:**
- Write specifications (Annie's job)
- Make architecture decisions (Alphonso's job)
- Create implementation plans (Petra's job)
- Write code (Backend/Frontend's job)
- Review code (Cindy's job)
- Resolve technical blockers (specialists' job)

---

## Status Tracking

### Where to Check Progress

**AGENT_STATUS.md** shows current cycle state:
```yaml
current_cycle:
  id: "2026-02-11-oauth-authentication"
  phase: "Phase 4: Implementation"
  progress: "60%"
  blockers: []
  next_milestone: "Code review by 2026-02-15"
  assigned_agents:
    - "Backend Benny (active)"
    - "Code Reviewer Cindy (queued)"
```

**WORKFLOW_LOG.md** shows chronological history:
```
2026-02-11 09:00 - [Mike] Created specification task for Analyst Annie
2026-02-11 10:30 - [Annie] Specification approved, handed to Alphonso
2026-02-11 14:00 - [Alphonso] Architecture review complete, no blockers
2026-02-12 08:00 - [Petra] Implementation tasks created in inbox/
2026-02-12 16:00 - [Benny] Started implementation (3 tasks assigned)
```

---

## Phase Transitions

Each phase has a **handoff trigger** Mike validates before proceeding:

| Phase | Trigger | Mike Validates |
|-------|---------|----------------|
| 1→2   | Spec approved | Meets Directive 035 standards |
| 2→3   | Architecture approved | No architectural blockers |
| 3→4   | Tasks created | Clear acceptance criteria |
| 4→5   | Tasks in done/ | All tests passing |
| 5→6   | Approval granted | No critical issues |
| 6→✅  | Deployed | Feature live, metrics tracked |

---

## Blocker Handling

When Mike detects a blocker:

1. **Documents** in AGENT_STATUS.md immediately
2. **Notifies** human via status update
3. **Proposes** mitigation if within scope
4. **Does NOT** attempt to resolve technical blockers

**Example blocker notification:**
```markdown
**BLOCKER DETECTED** (Phase 5: Code Review)
- **Issue:** Circular dependency in src/domain/auth/
- **Assigned:** Backend Benny to investigate
- **Human decision needed:** Approve refactoring or rollback?
- **Impact:** Blocks Phase 6 integration
```

---

## Tactical vs Strategic Boundary

| Coordination Type | Owner |
|-------------------|-------|
| Execute THIS cycle | **Manager Mike** (tactical) |
| Track THIS batch | **Manager Mike** |
| Coordinate THIS handoff | **Manager Mike** |
| Plan roadmap | **Planning Petra** (strategic) |
| Prioritize milestones | **Planning Petra** |
| Forecast capacity | **Planning Petra** |

**Rule of thumb:** If it's about the current cycle-in-flight, ask Mike. If it's about future planning or cross-cycle strategy, ask Petra.

---

## Common Questions

**Q: Can Mike skip phases?**  
A: Only with explicit human approval. All 6 phases are normally required for full traceability.

**Q: Can multiple cycles run in parallel?**  
A: Yes, but Mike tracks each cycle separately in AGENT_STATUS.md.

**Q: What if a specialist agent is unavailable?**  
A: Mike documents blocker and escalates to human for mitigation.

**Q: Can I request status mid-cycle?**  
A: Yes, Mike provides current state from AGENT_STATUS.md on request.

**Q: How do I know when orchestration is complete?**  
A: Mike updates AGENT_STATUS with "Phase 6: Complete" and final deployment confirmation.

---

## Quick Commands

```bash
# Request orchestration
@manager-mike: Orchestrate [initiative]

# Check status
@manager-mike: Status for cycle [id]

# View phase history
cat work/coordination/WORKFLOW_LOG.md

# See current assignments
cat work/coordination/AGENT_STATUS.md

# Check handoff readiness
cat work/coordination/HANDOFFS.md
```

---

## Artifacts Location

- **Profile:** `doctrine/agents/manager.agent.md`
- **Status:** `work/coordination/AGENT_STATUS.md`
- **Log:** `work/coordination/WORKFLOW_LOG.md`
- **Handoffs:** `work/coordination/HANDOFFS.md`

---

**Last Updated:** 2026-02-11  
**Profile Version:** 1.1 (Orchestration Enhanced)
