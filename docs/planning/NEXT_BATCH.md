# Next Batch: M4 Week 1 - Rich CLI + Template Generation

**Batch:** M4 Batch 4.1 - Foundation UX Enhancements  
**Milestone:** Milestone 4 - User Experience Enhancements  
**Status:** 🟢 READY TO START (After M3 Completion)  
**Target Start:** After M3 (Telemetry & Cost Optimization) completes  
**Estimated Duration:** 6-9 hours  
**Priority:** ⭐⭐⭐⭐⭐ HIGH (Human-in-Charge approved)

---

## Strategic Context

This batch implements the first wave of spec-kitty inspired UX enhancements, focusing on professional CLI experience and rapid onboarding. These improvements address key user pain points identified in the [comparative analysis](../architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md).

**Human-in-Charge Priorities:**
- ⭐⭐⭐⭐⭐ Rich Terminal UI (ADR-030)
- ⭐⭐⭐⭐⭐ Template-Based Config (ADR-031)
- ⭐⭐⭐⭐⭐ Dashboard Interface (ADR-032) - Week 2

**Target Outcomes:**
- Professional CLI output (panels, progress bars, colors)
- Onboarding time: 30 minutes → 2 minutes
- Zero manual YAML editing for basic setup

---

## Batch Tasks

### Task 1: Rich Terminal UI Implementation

**File:** `work/collaboration/inbox/2026-02-05T1400-backend-dev-rich-terminal-ui.yaml`  
**Agent:** Backend-dev Benny  
**Estimated:** 2-3 hours  
**Priority:** HIGH  
**Status:** Ready for assignment

**Description:**
Integrate the `rich` Python library to provide structured, colorful CLI output across all llm-service commands.

**Key Deliverables:**
1. Add `rich>=13.0.0` dependency
2. Create console wrapper module (`src/llm_service/ui/console.py`)
3. Update CLI commands to use rich output:
   - Panels for execution summaries
   - Progress bars for operations >2 seconds
   - Tables for structured data (models, tools, metrics)
   - Syntax highlighting for YAML/JSON output
   - Status indicators (✅ ✗ ⚠️)
4. Implement automatic fallback for non-TTY environments
5. Add `--no-color` flag for color disable

**Acceptance Criteria:**
- ✅ All CLI commands use rich output
- ✅ Progress bars for long operations (>2s)
- ✅ Automatic fallback to plain text in CI/CD
- ✅ Unit tests for console output
- ✅ Manual visual tests (TTY and non-TTY modes)

**Reference:** [ADR-030: Rich Terminal UI](../architecture/adrs/ADR-030-rich-terminal-ui-cli-feedback.md)

**Dependencies:**
- None (foundational)

---

### Task 2: Template-Based Configuration Generation

**File:** `work/collaboration/inbox/2026-02-05T1401-backend-dev-template-config-generation.yaml`  
**Agent:** Backend-dev Benny  
**Estimated:** 4-6 hours  
**Priority:** HIGH  
**Status:** Ready for assignment

**Description:**
Implement template-based configuration generation system to reduce onboarding friction from 30 minutes to 2 minutes.

**Key Deliverables:**
1. Template system:
   - Create 4 templates (quick-start, claude-only, cost-optimized, development)
   - Variable substitution (`${VAR}` syntax)
   - Platform-specific path resolution
   - Template validation in CI/CD

2. CLI commands:
   - `llm-service config init [--template NAME]`
   - `llm-service config templates` (list available)
   - `llm-service config show` (display current)

3. Tool management:
   - `llm-service tool add <name> --binary PATH --models LIST`
   - `llm-service tool remove <name>`
   - `llm-service tool list` (show configured tools)

4. Environment scanning:
   - Detect API keys (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.)
   - Find tool binaries in PATH
   - Platform detection (Darwin/Linux/Windows)
   - Validation and helpful next-steps messages

**Acceptance Criteria:**
- ✅ All 4 templates validate successfully
- ✅ `config init` generates working configuration in <30 seconds
- ✅ Environment scanning detects API keys and binaries
- ✅ Tool add/remove commands work atomically (rollback on error)
- ✅ Generated config passes schema validation
- ✅ Unit tests for template substitution and tool management
- ✅ Integration tests for full init workflow

**Reference:** [ADR-031: Template-Based Configuration Generation](../architecture/adrs/ADR-031-template-based-config-generation.md)

**Dependencies:**
- Task 1 (Rich Terminal UI) - for output formatting

---

### Task 3: Spec-Driven Development PRIMER

**File:** `work/collaboration/inbox/2026-02-05T1400-writer-editor-spec-driven-primer.yaml`  
**Agent:** Writer-Editor Sam  
**Estimated:** 2 hours  
**Priority:** MEDIUM  
**Status:** Ready for assignment

**Description:**
Create PRIMER document translating spec-kitty's specification-driven methodology into our approach directory.

**Key Deliverables:**
1. PRIMER document at `.github/agents/approaches/spec-driven-development.md`
2. Content sections:
   - Purpose and core principles
   - SDD vs. ATDD vs. ADRs differentiation
   - When to use guidance
   - Example prompts for agents
   - Integration with file-based orchestration
3. Cross-references to:
   - Directive 016 (ATDD)
   - Directive 034 (Spec-Driven Development)
   - spec-kitty comparative analysis

**Acceptance Criteria:**
- ✅ Document follows PRIMER template
- ✅ Clear distinction between specs/tests/ADRs
- ✅ Practical examples for agent usage
- ✅ Proper metadata and cross-references
- ✅ Reviewed by Architect Alphonso (technical accuracy)

**Reference:** 
- [spec-kitty Comparative Analysis](../architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md)
- [Directive 034: Spec-Driven Development](../.github/agents/directives/034_spec_driven_development.md)

**Dependencies:**
- None (can run in parallel with Tasks 1-2)

---

## Batch Success Criteria

This batch is complete when:

✅ **Rich CLI Output**
- All `llm-service` commands use rich formatting
- Professional appearance (panels, colors, progress bars)
- Automatic fallback for CI/CD environments

✅ **Template-Based Onboarding**
- `llm-service config init` generates working config in <30 seconds
- Time to first execution: 30 minutes → 2 minutes
- Environment scanning provides helpful feedback

✅ **Spec-Driven PRIMER**
- PRIMER document available in approaches directory
- Agents understand when to create specifications
- Integration with existing workflow documented

✅ **Code Quality**
- Test coverage maintained at >90%
- All tests passing
- No regressions in existing functionality

✅ **Documentation**
- CLI commands documented
- Template system explained
- User guide updated with new onboarding flow

---

## Integration Points

### With M3 (Telemetry)
- Rich CLI will display telemetry stats (tokens, costs)
- Template generation includes telemetry configuration
- No blocking dependencies (can start after M3 or in parallel)

### With M4 Week 2 (Dashboard)
- Dashboard backend will use same event system
- Rich CLI provides progress updates that dashboard can display
- Template generation creates dashboard configuration

### With M5 (Integration Testing)
- Rich CLI tested in cross-platform environments
- Template generation tested on Linux/macOS/Windows
- End-to-end onboarding flow validated

---

## Risk Mitigation

**Risk 1: Rich Library Integration Issues**
- *Probability:* Low
- *Impact:* Medium
- *Mitigation:* Rich is battle-tested; fallback to plain text automatic
- *Contingency:* Can continue with basic output if rich fails

**Risk 2: Template Complexity**
- *Probability:* Medium
- *Impact:* Medium  
- *Mitigation:* Start with simple templates, iterate based on feedback
- *Contingency:* Provide manual configuration guide as backup

**Risk 3: Environment Scanning Edge Cases**
- *Probability:* Medium
- *Impact:* Low
- *Mitigation:* Graceful degradation if scanning fails
- *Contingency:* Manual environment variable setup instructions

---

## Next Batch Preview

**M4 Batch 4.2: Dashboard MVP (Week 2)**
- Flask + Flask-SocketIO backend
- File watcher for YAML task tracking
- Single-page web dashboard
- Real-time execution visibility
- **Estimated:** 12-16 hours
- **Priority:** ⭐⭐⭐⭐⭐ HUMAN PRIORITY

---

## References

**ADRs:**
- [ADR-030: Rich Terminal UI](../architecture/adrs/ADR-030-rich-terminal-ui-cli-feedback.md)
- [ADR-031: Template-Based Configuration](../architecture/adrs/ADR-031-template-based-config-generation.md)
- [ADR-032: Real-Time Dashboard](../architecture/adrs/ADR-032-real-time-execution-dashboard.md) - Next batch
- [ADR-033: Step Tracker Pattern](../architecture/adrs/ADR-033-step-tracker-pattern.md) - Week 3

**Planning Documents:**
- [Implementation Roadmap](llm-service-layer-implementation-plan.md)
- [spec-kitty Comparative Analysis](../architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md)
- [spec-kitty Inspired Enhancements](../architecture/design/spec-kitty-inspired-enhancements.md)

**Directives:**
- [Directive 016: ATDD](../.github/agents/directives/016_acceptance_test_driven_dev.md)
- [Directive 034: Spec-Driven Development](../.github/agents/directives/034_spec_driven_development.md)

---

**Batch Owner:** Planning Petra  
**Last Updated:** 2026-02-05 14:00:00 UTC  
**Status:** 🟢 READY FOR ASSIGNMENT
