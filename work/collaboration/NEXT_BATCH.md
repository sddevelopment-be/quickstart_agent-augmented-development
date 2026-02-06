# Next Batch Recommendation

**Updated:** 2026-02-06 11:45:00 UTC
**Prepared By:** Planning Petra
**Status:** 🟢 **READY FOR ASSIGNMENT**

---

## Recent Completions ✅

### Batch 1: M2 Batch 2.3 - Generic YAML Adapter (Historical - 2026-02-05)
- **Status:** ✅ Already complete
- **Completed:** 2026-02-05 by Backend-dev
- **Duration:** ~6 hours (all 3 tasks)
- **Achievements:**
  - Generic YAML adapter (455 lines, 82% coverage)
  - ENV variable support (env_utils.py, 340 tests)
  - Routing integration (routing.py, 111 lines)
  - 367/369 tests passing (99.5%)

### Batch 2: Dashboard Integration Wiring (2026-02-06)
- **Status:** ✅ Complete
- **Completed:** 2026-02-06 (today) by Backend-dev
- **Duration:** 1.5h actual vs 2.0h estimated
- **Achievements:**
  - File watcher integration
  - Telemetry integration
  - 17/17 dashboard tests passing
  - Dashboard production-ready

---

## Current Project State

### Completed Milestones
- ✅ **M1: Foundation** (100%) - Config, CLI, Routing engine
- ✅ **M2: Tool Integration** (100%) - Generic YAML adapter, ENV support
- ✅ **M4 Batch 4.1: Rich CLI + Templates** (100%) - Rich terminal UI, config generation
- ✅ **Dashboard Integration** (100%) - WebSocket server, file watcher, telemetry

### In-Progress Milestones
- 🚀 **M3: Cost Optimization & Telemetry** (0%) - Ready to start
- 🚀 **M4: User Experience** (50%) - Batch 4.1 done, Batch 4.2 pending

---

## Next Batch Options

### Option 1: M3 Batch 3.1 - Telemetry Infrastructure (HIGH) ⭐⭐⭐⭐⭐

**Strategic Importance:** CRITICAL - Enables cost tracking and optimization

**Tasks (3-4 Total):**
1. SQLite database schema for invocation logs (HIGH, 2-3h)
2. Telemetry logger with token/cost/latency tracking (HIGH, 3-4h)
3. Database initialization and migration support (MEDIUM, 2h)
4. Privacy controls (metadata-only vs. full logging) (MEDIUM, 1-2h)

**Estimated Duration:** 2-3 days (8-11 hours)
**Strategic Value:** ⭐⭐⭐⭐⭐ Critical path for cost optimization
**Dependencies:** All met ✅ (Dashboard telemetry API already integrated)

**Why This Batch:**
- Completes M3 Telemetry Infrastructure milestone
- Unblocks M3 Batch 3.2 (Policy Engine) and 3.3 (Stats & Reporting)
- Dashboard telemetry API already wired (today's work)
- Natural progression: Dashboard ready → Feed it real data
- High business value: Cost tracking = $3K-$6K annual savings

**Recommendation:** **EXECUTE NEXT** - Critical for cost optimization goals

---

### Option 2: M4 Batch 4.2 - Dashboard MVP (MEDIUM) ⭐⭐⭐⭐

**Tasks (4-5 Total):**
1. Real-time WebSocket event emission (MEDIUM, 2-3h)
2. Dashboard frontend components (HIGH, 4-5h)
3. Task visualization and metrics (MEDIUM, 2-3h)
4. End-to-end dashboard testing (MEDIUM, 2h)

**Estimated Duration:** 2-3 days (10-13 hours)
**Strategic Value:** ⭐⭐⭐⭐ High user experience value
**Dependencies:** Mostly met (backend wiring done, needs frontend work)

**Why This Batch:**
- Dashboard backend complete (today's work)
- Natural next step: Add frontend and real-time features
- User-facing value: Real-time task monitoring
- Completes M4 User Experience milestone

**Recommendation:** DEFER - Complete M3 first (telemetry enables richer dashboard data)

---

### Option 3: Additional Dashboard Features (LOW) ⭐⭐

**Tasks in Inbox:**
- Rich terminal UI enhancement (MEDIUM)
- Template config generation enhancement (MEDIUM)
- Spec-driven primer (documentation) (MEDIUM)

**Recommendation:** DEFER - Optional enhancements, not critical path

---

## Planning Petra's Recommendation

**Execute Next:** **Option 1 - M3 Batch 3.1 (Telemetry Infrastructure)**

**Rationale:**
1. **Critical Path:** M3 Telemetry enables cost optimization (core project goal)
2. **Dependencies Met:** Dashboard telemetry API wired today, ready for real implementation
3. **Business Value:** Cost tracking = $3K-$6K annual savings per team
4. **Natural Flow:** Dashboard backend ready → Feed it real telemetry data
5. **Unblocks Future:** M3.2 Policy Engine, M3.3 Stats require M3.1 telemetry

**Alternative:** If frontend skills available, M4 Batch 4.2 (Dashboard MVP) is also valuable

**Next Command:** `/iterate` (will execute M3 Batch 3.1)

---

## Overall Project Health: 🟢 ON TRACK

### LLM-Service Layer
- **Completed:** M1 Foundation, M2 Tool Integration
- **Next:** M3 Telemetry Infrastructure (Batch 3.1)
- **After That:** M3 Batch 3.2 (Policy Engine), M3 Batch 3.3 (Stats)

### Dashboard
- **Status:** ✅ Production ready (backend complete)
- **Next:** Real-time features + frontend (M4 Batch 4.2)

### Overall
- **Blockers:** None
- **Decisions Needed:** None
- **Timeline:** On track for milestone targets
- **Risk Level:** LOW
- **Code Quality:** 367/369 tests passing (99.5%)

---

## Task Queue Summary

**Inbox (3 tasks - all LOW/MEDIUM):**
- Rich terminal UI enhancement (deferred)
- Template config generation (deferred)
- Spec-driven primer (deferred)

**Active:** None (batch just completed)

**Done (recent):**
- M2 Batch 2.3: Generic YAML adapter (3 tasks) - 2026-02-05
- Dashboard integration wiring (3 tasks) - 2026-02-06

---

## M3 Batch 3.1 - Telemetry Infrastructure (Detailed Plan)

**Batch ID:** `2026-02-06-llm-service-m3-batch-3.1`
**Estimated Duration:** 2-3 days (8-11 hours)
**Strategic Importance:** ⭐⭐⭐⭐⭐ CRITICAL

### Strategic Context

**Goal:** Implement telemetry infrastructure for cost tracking and optimization

**Success Criteria:**
- SQLite database schema for invocation logs
- Telemetry logger tracks token/cost/latency per invocation
- Database initialization and migration support
- Privacy controls (metadata-only vs. full logging)
- Integration with dashboard telemetry API
- Unit tests with >80% coverage

### Tasks

**Task 1: SQLite Database Schema** (HIGH, 2-3h)
- Design schema for invocation logs (tool, model, tokens, cost, duration)
- Create database initialization script
- Add migration support for schema evolution
- Write unit tests for schema operations

**Task 2: Telemetry Logger** (HIGH, 3-4h)
- Implement TelemetryLogger class
- Track: tool_name, model, prompt_tokens, completion_tokens, cost, duration
- Support sync and async logging
- Calculate costs based on model pricing
- Write comprehensive unit tests

**Task 3: Database Initialization** (MEDIUM, 2h)
- Auto-create database on first run
- Migration support for schema changes
- Database backup/restore utilities
- Configuration for database path

**Task 4: Privacy Controls** (MEDIUM, 1-2h)
- Metadata-only mode (no prompt/response content)
- Full logging mode (includes prompts/responses)
- Configurable via YAML (privacy level)
- Clear documentation of privacy implications

### Dependencies

- ✅ Dashboard telemetry API (integrated today)
- ✅ M2 Tool Integration (Generic adapter complete)
- ✅ M1 Configuration system

### Deliverables

- `src/llm_service/telemetry/database.py` - SQLite schema and operations
- `src/llm_service/telemetry/logger.py` - TelemetryLogger class
- `src/llm_service/telemetry/models.py` - Data models for logs
- `tests/unit/telemetry/` - Comprehensive test suite
- `docs/architecture/adrs/ADR-0XX-telemetry-privacy.md` - Privacy ADR

---

**Prepared By:** Planning Petra
**Date:** 2026-02-06 11:45:00 UTC
**Status:** 🟢 **READY FOR ASSIGNMENT**
**Recommended Start:** Immediate
**Expected Completion:** 2-3 days (8-11 hours with buffer)

**Next Steps:**
1. Create M3 Batch 3.1 task YAML files in inbox/
2. Use `/iterate` to execute M3 Batch 3.1
3. Backend-dev implements telemetry infrastructure with TDD
4. Integrate with dashboard telemetry API
5. Move to M3 Batch 3.2 (Policy Engine) after completion
