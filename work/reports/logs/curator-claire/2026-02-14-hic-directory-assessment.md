# HiC Directory Structure - Initial Assessment

**Agent:** Curator Claire  
**Date:** 2026-02-14  
**Status:** Assessment Complete ✅

---

## Executive Summary

The proposed `work/human-in-charge/` directory structure is **strongly aligned** with existing doctrine patterns and addresses a critical gap in async agent-human coordination. I recommend **proceeding with implementation** with minor enhancements.

**Recommendation:** ✅ Approve with enhancements

---

## Proposal Analysis

### Original Proposal
```
work/human-in-charge/
├── executive_summary/    # High-level summaries for HiC
├── decision_request/     # Files requiring HiC decisions  
└── problems/             # Issues blocking progress
```

### Alignment with Existing Patterns

#### ✅ Strong Alignment Points

1. **Work Directory Orchestration Approach**
   - Current: `work/collaboration/` for agent-to-agent coordination
   - Gap: No dedicated human-agent escalation path
   - HiC directory fills this gap perfectly

2. **AFK Mode (doctrine/shorthands/afk-mode.md)**
   - Line 142-148: "Create checkpoint file" for pauses
   - Current: Scattered in agent-specific logs
   - HiC directory provides structured collection point

3. **File-Based Collaboration (Directive 019)**
   - Principle: All coordination through files in `work/`
   - HiC directory extends this principle to human escalations

4. **Existing Report Structures**
   - `work/reports/exec_summaries/` exists (singular "summary")
   - `work/reports/executive-summaries/` also exists (hyphenated)
   - HiC consolidates executive-level human outputs

5. **Manager Mike Coordination Role**
   - Current: Routes agent-to-agent work
   - Gap: No clear escalation protocol for human decisions
   - HiC directory provides this pathway

#### ⚠️ Considerations & Enhancements

1. **Subdirectory Naming**
   - Proposed: `executive_summary` (singular)
   - Existing: `exec_summaries/` and `executive-summaries/` (plural)
   - **Recommendation:** Use plural `executive_summaries` for consistency

2. **Subdirectory Scope**
   - `problems/` is accurate but could be broader
   - **Recommendation:** Add `blockers/` subdirectory (distinct from problems)
   - **Rationale:** Blockers are external (waiting), problems are internal (needs fixing)

3. **Cross-Directory Redundancy**
   - `work/reports/exec_summaries/` overlaps with proposed HiC directory
   - **Recommendation:** Clarify distinction in documentation
   - **Distinction:** Reports = completed work summaries, HiC = pending human review

4. **Integration with Task System**
   - `work/collaboration/` uses YAML task files with `status: error` for blockers
   - **Recommendation:** HiC directory complements (not replaces) task system
   - **Use Case:** HiC is for "needs human decision", tasks are "needs agent action"

---

## Proposed Final Structure

```
work/human-in-charge/
├── README.md                  # Usage guide and conventions
├── executive_summaries/       # High-level summaries requiring review
├── decision_requests/         # Explicit decisions needed (plural for consistency)
├── blockers/                  # External blockers (waiting on humans/systems)
└── problems/                  # Internal problems requiring human judgment
```

### Directory Definitions

**executive_summaries/**
- **Purpose:** Consolidated summaries of complex work for HiC review
- **When to use:** Multi-phase initiatives, architecture changes, major refactorings
- **Format:** Markdown with frontmatter (status, agent, date, summary, details)
- **Example:** `2026-02-14-doctrine-stack-audit-summary.md`

**decision_requests/**
- **Purpose:** Explicit decisions that agents cannot make autonomously
- **When to use:** Architectural choices, breaking changes, trade-off decisions
- **Format:** Markdown with options, pros/cons, recommendation
- **Example:** `2026-02-14-test-strategy-decision.md`
- **Related:** AFK mode "critical decisions" (afk-mode.md line 95-111)

**blockers/**
- **Purpose:** External blockers preventing progress (awaiting humans/systems)
- **When to use:** Missing credentials, awaiting PR reviews, external dependencies
- **Format:** Markdown with blocker description, impact, workaround attempts
- **Example:** `2026-02-14-missing-api-key.md`

**problems/**
- **Purpose:** Internal problems requiring human judgment
- **When to use:** Unexpected results, ambiguous requirements, design conflicts
- **Format:** Markdown with problem description, context, attempted solutions
- **Example:** `2026-02-14-test-suite-contradictions.md`

---

## Use Case Scenarios

### Scenario 1: AFK Mode with Critical Decision
**Context:** Agent working autonomously, encounters architectural decision  
**Action:**
1. Agent pauses work per AFK protocol
2. Creates decision request: `work/human-in-charge/decision_requests/[timestamp]-[topic].md`
3. Documents options with pros/cons
4. Adds recommendation if possible
5. Waits for HiC guidance

### Scenario 2: Async Coordination (GitHub Copilot Web)
**Context:** Human in GitHub web interface, agent completed complex work  
**Action:**
1. Agent creates executive summary in `work/human-in-charge/executive_summaries/`
2. HiC reviews at convenience
3. HiC leaves feedback in summary file or creates decision request
4. Agent picks up feedback asynchronously

### Scenario 3: Blocker During Task Execution
**Context:** Agent needs API key to proceed with integration test  
**Action:**
1. Agent creates blocker file: `work/human-in-charge/blockers/[timestamp]-api-key-needed.md`
2. Agent moves task to `frozen` status with reference to blocker
3. Agent continues with other tasks
4. HiC provides credentials when available
5. Agent resumes task

### Scenario 4: Problem Discovery
**Context:** Agent finds contradictory requirements in specifications  
**Action:**
1. Agent creates problem file: `work/human-in-charge/problems/[timestamp]-spec-contradiction.md`
2. Documents conflicting requirements with evidence
3. Proposes resolution options
4. Awaits HiC clarification before proceeding

---

## Integration Points

### With Existing Systems

**1. Work Directory Orchestration**
- HiC directory is a peer to `collaboration/`, `reports/`, `planning/`
- Follows same file-based async pattern
- Complements (not replaces) task lifecycle

**2. AFK Mode**
- AFK pause protocol references HiC directory
- Critical decisions → `decision_requests/`
- Blockers → `blockers/`
- Current line 142 updated to reference HiC directory

**3. Manager Mike Coordination**
- When agent escalates, Manager Mike routes to HiC directory
- Mike can consolidate multiple agent escalations into executive summaries
- Mike monitors HiC directory for resolved decisions/blockers

**4. Directive 024 (Self-Observation Protocol)**
- Checkpoint files can reference HiC directory items
- "Awaiting decision [link to decision_request]"

**5. Directive 019 (File-Based Collaboration)**
- Extends collaboration principle to human-agent boundary
- Same patterns: markdown, frontmatter, traceability

---

## Benefits Assessment

### ✅ Pros

1. **Async-Friendly:** Humans review at convenience, no real-time needed
2. **Structured Escalation:** Clear paths for different escalation types
3. **Traceability:** All escalations in Git history
4. **Pattern Consistency:** Extends existing work directory patterns
5. **AFK Enhancement:** Makes AFK mode more practical for long sessions
6. **Reduced Noise:** Executive summaries consolidate complex work
7. **Decision Context:** Decision requests preserve full context for HiC

### ⚠️ Potential Challenges

1. **Directory Proliferation:** Another top-level directory in `work/`
   - **Mitigation:** Clear documentation on when to use
2. **Overlap with Reports:** Some overlap with `work/reports/exec_summaries/`
   - **Mitigation:** Clarify distinction (reports = done, HiC = pending)
3. **Agent Training:** All agents need to know when/how to use
   - **Mitigation:** Directive + update all agent profiles
4. **Human Monitoring:** Requires HiC to check directory regularly
   - **Mitigation:** Document checking cadence expectations

### 🎯 Overall Assessment

**Score: 9/10** - Excellent alignment, minor enhancements needed

---

## Recommended Next Steps

1. ✅ **Create DDR** (ADR-047)
   - Document decision to add HiC directory
   - Explain rationale and alternatives
   - Reference related ADRs (ADR-004, ADR-008)

2. ✅ **Create Directive** (040)
   - When to use HiC directory
   - Subdirectory usage guide
   - File naming conventions
   - Frontmatter standards

3. ✅ **Implement Structure**
   - Create `work/human-in-charge/` with subdirectories
   - Add comprehensive README.md
   - Add .gitkeep files
   - Add template files for each subdirectory

4. ✅ **Update Agent Profiles**
   - Manager Mike: Add HiC escalation protocol
   - All agents: Reference Directive 040
   - Analyst Annie, Architect Alphonso: Heavy users of decision_requests

5. ✅ **Update Related Documentation**
   - `work/README.md`: Add HiC directory description
   - `doctrine/shorthands/afk-mode.md`: Reference HiC directory
   - `doctrine/directives/019_file_based_collaboration.md`: Mention HiC escalation

6. 📋 **Future Enhancements** (not in scope)
   - Automation script to notify HiC of new items
   - Dashboard integration for HiC directory monitoring
   - Metrics on escalation frequency by type

---

## Conclusion

The `work/human-in-charge/` directory structure is a well-conceived addition that:
- Addresses real gaps in async agent-human coordination
- Aligns perfectly with existing doctrine patterns
- Enhances AFK mode practicality
- Provides structured escalation paths
- Maintains file-based async collaboration principles

**Proceeding with implementation with recommended enhancements.**

---

**Next Action:** Create DDR-047 and Directive 040

**Estimated Effort:** 2-3 hours for complete implementation

**Risk Level:** Low (additive change, no breaking modifications)
