# Executive Summary: Doctrine Code Representations

**Status:** APPROVED ✅  
**Date:** 2026-02-11  
**Approver:** @stijn-dejongh  
**Architect:** Alphonso  
**Impact:** HIGH - Enables UI inspection, vendor tool distribution, type-safe domain modeling

---

## The Big Picture

We're creating **Python code representations** for doctrine concepts (Agent, Directive, Tactic, Approach, StyleGuide, Template) to:

1. ✅ **Enable UI inspection** - Dashboard and CLI can show "What agents exist? What directives apply?"
2. ✅ **Support vendor tool export** - Transform doctrine configs → OpenCode/Cursor/Cody formats
3. ✅ **Improve maintainability** - Type-safe domain objects with validation
4. ✅ **Clarify architecture** - Refactor `src/common/` → `src/domain/{collaboration,doctrine,specifications}`

**Approval Rationale:** Clean architectural boundaries, no circular dependencies, aligns with existing patterns (ADR-042, ADR-044).

---

## What's Changing?

### Before
```
src/common/                    # Mixed utilities + domain concepts
  ├── agent_loader.py          # Scattered parsing logic
  ├── task_schema.py
  └── types.py

doctrine/                      # Pure YAML/Markdown (no code)
  ├── agents/*.agent.md
  ├── directives/*.md
  └── tactics/*.md
```

### After
```
src/domain/                    # NEW: Domain layer
  ├── collaboration/           # Agents, tasks, batches, iterations
  ├── doctrine/                # Directives, tactics, approaches
  ├── specifications/          # Specs, features
  └── common/                  # Shared types/exceptions

src/adapters/                  # NEW: Vendor tool export
  ├── opencode.py
  └── cursor.py

CLI Commands:                  # NEW: Inspection tools
  $ kitty show agents
  $ kitty inspect stack
  $ kitty validate doctrine
```

---

## Key Decisions

| Decision | Why? | Trade-off |
|----------|------|-----------|
| **Python dataclasses** | Simple, built-in, sufficient | Could use Pydantic later if needed |
| **3 domain submodules** | Clear boundaries | More directories to navigate |
| **ACL/adapter layer** | Support multiple vendor tools | Extra abstraction layer |
| **Phased implementation** | Risk mitigation, 7 weeks | Longer to full completion |
| **CLI inspection** | Developer experience | More code to maintain |

---

## Timeline

**Immediate Actions (16 hours):**
- Backend Benny: Create ADR-045, ADR-046 (4 hours)
- Alphonso: Update architecture docs (1 hour)
- Claire: Check doctrine→ADR dependencies (2 hours)
- Mike: Assess orchestration role (2 hours)
- Petra: Create initiative + 46 tasks (5 hours)

**Implementation (120 hours over 7 weeks):**
- Phase 1: Core domain objects (16 hours)
- Phase 2: Collaboration domain (20 hours)
- Phase 3: File loaders/parsers (24 hours)
- Phase 4: Validation logic (16 hours)
- Phase 5: UI/export integrations (32 hours)
- Phase 6: Migration & cleanup (12 hours)

**Total:** 136 hours

---

## Success Metrics

| Metric | Before | After |
|--------|--------|-------|
| Domain objects | 0 | 15+ |
| Type coverage | 60% | 85% |
| Test coverage | 70% | 80% (domain: 90%) |
| CLI commands | 0 | 5+ |
| Vendor adapters | 0 | 2+ |

---

## What This Unlocks

**For Dashboard Users:**
- View agent profiles, capabilities, directive compliance
- Inspect doctrine stack: "What's configured?"
- Validate consistency: "Are there missing references?"

**For CLI Users:**
```bash
$ kitty show agents
$ kitty inspect stack
$ kitty check compliance --agent=backend-benny
$ kitty validate doctrine
```

**For Vendor Tool Distribution:**
```bash
$ kitty export --format=opencode --output=.opencode/
✅ Wrote .opencode/agents.json (15 agents)
✅ Wrote .opencode/directives.json (34 directives)
```

**For Developers:**
- IDE autocomplete for agent profiles
- Type checking catches errors at compile time
- Single source of truth for domain concepts

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Breaking changes (import paths) | Comprehensive test suite, phased rollout |
| Scope creep | Strict phase boundaries, defer non-critical features |
| Performance regression | Caching layer (Phase 3), benchmarking |
| Incomplete migration | Phase 6 dedicated to cleanup, checklist validation |

---

## Dependencies

**Blocks:**
- SPEC-DIST-001 (vendor tool distribution) - Needs adapter layer
- SPEC-DASH-008 (dashboard doctrine UI) - Needs domain objects

**Depends On:**
- ADR-042 (Shared Task Domain Model) - Pattern established ✅
- ADR-044 (Agent Identity Type Safety) - Pattern established ✅

---

## Next Steps (Immediate)

1. **Backend Benny:** Create ADR-045 and ADR-046 drafts (4 hours)
2. **Architect Alphonso:** Review ADRs, update docs (2 hours)
3. **Curator Claire:** Check doctrine for ADR dependencies (2 hours)
4. **Manager Mike:** Decide on orchestration role ownership (2 hours)
5. **Planning Petra:** Create initiative + 46 tasks (5 hours)

**First Review:** After ADR-045/046 completion  
**Implementation Start:** After all immediate actions complete

---

## Questions?

**Technical:** Ask Architect Alphonso  
**Timeline/Resources:** Ask Manager Mike  
**Scope/Priorities:** Ask Planning Petra  
**Compliance:** Ask Curator Claire

---

## Full Documentation

**Start Here:** `doctrine-code-representations-index.md` (navigation hub)

**Core Documents:**
1. **Architectural Analysis** (47 KB, 1,340 lines) - Full technical spec
2. **Next Steps Guide** (16 KB, 650 lines) - Action items & timeline
3. **Visual Overview** (25 KB, 550 lines) - Diagrams & examples

**Location:** `work/reports/architecture/`

---

**Status:** APPROVED ✅  
**Confidence:** HIGH (clean architecture, proven patterns)  
**Go/No-Go:** ✅ GO - Proceed to ADR creation and implementation
