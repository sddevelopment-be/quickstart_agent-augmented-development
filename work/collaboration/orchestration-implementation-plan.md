# Asynchronous Multi-Agent Orchestration - Implementation Plan

_Created: 2025-11-20_  
_Issue: #8_  
_Status: Proposed_

## Overview

This document outlines the implementation plan for the file-driven, asynchronous multi-agent orchestration system. The work is organized into phases with clear ownership by specialized agents.

## Architecture References

- [Async Multi-Agent Orchestration Architecture](../../docs/architecture/async_multiagent_orchestration.md)
- [Technical Design](../../docs/architecture/async_orchestration_technical_design.md)
- [ADR-002: File-Based Async Coordination](../../docs/architecture/ADR-002-file-based-async-coordination.md)
- [ADR-003: Task Lifecycle and State Management](../../docs/architecture/ADR-003-task-lifecycle-state-management.md)
- [ADR-004: Work Directory Structure](../../docs/architecture/ADR-004-work-directory-structure.md)
- [ADR-005: Coordinator Agent Pattern](../../docs/architecture/ADR-005-coordinator-agent-pattern.md)

## Implementation Phases

### Phase 1: Core Infrastructure (CRITICAL)

**Objective:** Establish foundational directory structure and schemas

**Estimated effort:** 2-3 workdays  
**Priority:** Critical  
**Dependencies:** None

#### Tasks

| Task ID | Description | Agent | Artifacts | Status |
|---------|-------------|-------|-----------|--------|
| ORCH-001 | Create work directory structure script | Build Automation | `work/scripts/init-work-structure.sh` | Not Started |
| ORCH-002 | Define task YAML schema | Architect | `work/schemas/task-schema.yaml` | Not Started |
| ORCH-003 | Create task schema validation script | Build Automation | `work/scripts/validate-task-schema.py` | Not Started |
| ORCH-004 | Create directory structure validation script | Build Automation | `work/scripts/validate-work-structure.sh` | Not Started |
| ORCH-005 | Create task naming validation script | Build Automation | `work/scripts/validate-task-naming.sh` | Not Started |
| ORCH-006 | Initialize work directory with .gitkeep files | Build Automation | `work/**/.gitkeep` | Not Started |
| ORCH-007 | Create work/README.md documentation | Writer-Editor | `work/README.md` | Not Started |

**Acceptance Criteria:**

- [ ] All required directories exist with proper structure
- [ ] Task YAML schema defined and documented
- [ ] Validation scripts detect missing directories
- [ ] Validation scripts detect malformed task files
- [ ] Validation scripts detect incorrect naming conventions
- [ ] README explains directory structure and usage

**Recommended Agent Assignment:**

- **Primary:** Build Automation Agent (setup scripts, validation)
- **Supporting:** Architect (schema design), Writer-Editor (documentation)

---

### Phase 2: Agent Orchestrator Implementation (CRITICAL)

**Objective:** Implement Agent Orchestrator for task routing and monitoring

**Estimated effort:** 3-4 workdays  
**Priority:** Critical  
**Dependencies:** Phase 1

#### Tasks

| Task ID | Description | Agent | Artifacts | Status |
|---------|-------------|-------|-----------|--------|
| ORCH-008 | Implement Agent Orchestrator base script | Build Automation | `work/scripts/agent_orchestrator.py` | Not Started |
| ORCH-009 | Add task assignment logic | Build Automation | `agent_orchestrator.py` (assign_tasks) | Not Started |
| ORCH-010 | Add workflow sequencing logic | Build Automation | `agent_orchestrator.py` (process_completed_tasks) | Not Started |
| ORCH-011 | Add timeout detection | Build Automation | `agent_orchestrator.py` (check_timeouts) | Not Started |
| ORCH-012 | Add conflict detection | Build Automation | `agent_orchestrator.py` (detect_conflicts) | Not Started |
| ORCH-013 | Add status dashboard updates | Build Automation | `agent_orchestrator.py` (update_agent_status) | Not Started |
| ORCH-014 | Add archive logic | Build Automation | `agent_orchestrator.py` (archive_old_tasks) | Not Started |
| ORCH-015 | Create Coordinator agent profile | Architect | `.github/agents/coordinator.agent.md` | Not Started |
| ORCH-016 | Write Agent Orchestrator usage documentation | Writer-Editor | `docs/guides/agent-orchestrator-usage.md` | Not Started |
| ORCH-017 | Test Agent Orchestrator with sample tasks | Build Automation | Test results | Not Started |

**Acceptance Criteria:**

- [ ] Agent Orchestrator assigns tasks from inbox to agents
- [ ] Agent Orchestrator creates follow-up tasks based on next_agent
- [ ] Agent Orchestrator detects tasks stuck in in_progress >2 hours
- [ ] Agent Orchestrator warns on artifact conflicts
- [ ] Agent Orchestrator updates AGENT_STATUS.md
- [ ] Agent Orchestrator logs events to WORKFLOW_LOG.md
- [ ] Agent Orchestrator archives tasks older than 30 days
- [ ] Agent Orchestrator completes cycle in <30 seconds

**Recommended Agent Assignment:**

- **Primary:** Build Automation Agent (implementation, testing)
- **Supporting:** Architect (profile design), Writer-Editor (documentation)

---

### Phase 3: Agent Integration (HIGH)

**Objective:** Update existing agents to work with task-based orchestration

**Estimated effort:** 5-7 workdays  
**Priority:** High  
**Dependencies:** Phase 2

#### Tasks

| Task ID | Description | Agent | Artifacts | Status |
|---------|-------------|-------|-----------|--------|
| ORCH-018 | Create agent execution protocol template | Architect | `docs/templates/agent_execution_template.py` | Not Started |
| ORCH-019 | Update Structural agent for task-based execution | Build Automation | `.github/agents/structural.agent.md` update | Not Started |
| ORCH-020 | Update Lexical agent for task-based execution | Build Automation | `.github/agents/lexical.agent.md` update | Not Started |
| ORCH-021 | Update Curator agent for task-based execution | Curator | `.github/agents/curator.agent.md` update | Not Started |
| ORCH-022 | Update Diagrammer agent for task-based execution | Diagrammer | `.github/agents/diagrammer.agent.md` update | Not Started |
| ORCH-023 | Update Planning agent for task-based execution | Planning | `.github/agents/project-planner.agent.md` update | Not Started |
| ORCH-024 | Update Architect agent for task-based execution | Architect | `.github/agents/architect.agent.md` update | Not Started |
| ORCH-025 | Create sample task files for testing | Planning | `work/inbox/sample-*.yaml` | Not Started |
| ORCH-026 | Test end-to-end workflow: Structural → Lexical | Build Automation | Test results | Not Started |
| ORCH-027 | Test end-to-end workflow: Planning → multiple agents | Planning | Test results | Not Started |
| ORCH-028 | Document agent handoff patterns | Writer-Editor | `docs/guides/agent-handoff-patterns.md` | Not Started |

**Acceptance Criteria:**

- [ ] All agents can read task YAML from their assigned directory
- [ ] All agents update task status appropriately
- [ ] All agents add result blocks on completion
- [ ] All agents move completed tasks to work/done/
- [ ] Multi-step workflows (next_agent) work end-to-end
- [ ] Handoff patterns documented with examples

**Recommended Agent Assignment:**

- **Primary:** Each agent updates its own profile (self-integration)
- **Coordination:** Build Automation Agent (testing, validation)
- **Supporting:** Architect (protocol design), Writer-Editor (documentation)

---

### Phase 4: GitHub Actions Integration (MEDIUM)

**Objective:** Automate Coordinator execution via CI

**Estimated effort:** 2-3 workdays  
**Priority:** Medium  
**Dependencies:** Phase 3

#### Tasks

| Task ID | Description | Agent | Artifacts | Status |
|---------|-------------|-------|-----------|--------|
| ORCH-029 | Create Agent Orchestrator GitHub Actions workflow | Build Automation | `.github/workflows/agent-orchestrator.yml` | Not Started |
| ORCH-030 | Configure workflow permissions and secrets | Build Automation | Workflow config | Not Started |
| ORCH-031 | Create optional per-agent workflows | Build Automation | `.github/workflows/agent-*.yml` | Not Started |
| ORCH-032 | Test Coordinator workflow in CI | Build Automation | CI test results | Not Started |
| ORCH-033 | Document CI setup and troubleshooting | Writer-Editor | `docs/guides/ci-orchestration-setup.md` | Not Started |
| ORCH-034 | Create manual workflow dispatch triggers | Build Automation | Workflow configs | Not Started |

**Acceptance Criteria:**

- [ ] Agent Orchestrator runs every 5 minutes via GitHub Actions
- [ ] Agent Orchestrator can be manually triggered via workflow_dispatch
- [ ] Workflow has proper git permissions to commit results
- [ ] Workflow logs are accessible and debuggable
- [ ] Rate limits are monitored and respected
- [ ] CI setup documented for new repositories

**Recommended Agent Assignment:**

- **Primary:** Build Automation Agent (workflows, CI setup)
- **Supporting:** Writer-Editor (documentation)

---

### Phase 5: Validation and Monitoring (MEDIUM)

**Objective:** Add comprehensive validation and monitoring tools

**Estimated effort:** 2-3 workdays  
**Priority:** Medium  
**Dependencies:** Phase 2

#### Tasks

| Task ID | Description | Agent | Artifacts | Status |
|---------|-------------|-------|-----------|--------|
| ORCH-035 | Enhance schema validation with JSON Schema | Build Automation | `work/schemas/task-schema.json` | Not Started |
| ORCH-036 | Create integrity check script (all validations) | Build Automation | `work/scripts/validate-all.sh` | Not Started |
| ORCH-037 | Create monitoring dashboard generator | Build Automation | `work/scripts/generate-dashboard.py` | Not Started |
| ORCH-038 | Add metrics collection (task counts, durations) | Build Automation | `work/scripts/collect-metrics.py` | Not Started |
| ORCH-039 | Create archive compression script | Build Automation | `work/scripts/compress-archive.sh` | Not Started |
| ORCH-040 | Document validation procedures | Writer-Editor | `docs/guides/orchestration-validation.md` | Not Started |
| ORCH-041 | Document troubleshooting common issues | Writer-Editor | `docs/guides/orchestration-troubleshooting.md` | Not Started |

**Acceptance Criteria:**

- [ ] Schema validation detects all malformed task files
- [ ] Integrity check script runs all validations in one command
- [ ] Dashboard shows real-time system health
- [ ] Metrics track throughput and bottlenecks
- [ ] Archive compression reduces storage usage
- [ ] Validation procedures documented
- [ ] Common issues have documented solutions

**Recommended Agent Assignment:**

- **Primary:** Build Automation Agent (validation, monitoring tools)
- **Supporting:** Writer-Editor (documentation)

---

## Timeline and Dependencies

```
Phase 1 (Core Infrastructure)
  │
  └─→ Phase 2 (Coordinator Implementation)
        │
        ├─→ Phase 3 (Agent Integration)
        │     └─→ Phase 4 (GitHub Actions) [optional]
        │
        └─→ Phase 5 (Validation and Monitoring)
```

**See also:** [Orchestration Phases Timeline Diagram](../../docs/architecture/diagrams/orchestration-phases-timeline.puml)

**Critical Path:** Phase 1 → Phase 2 → Phase 3  
**Optional Enhancements:** Phase 4, Phase 5

**Total Timeline:**

- **Critical Phases (1-3):** 10-14 workdays (2-3 weeks)
- **Optional Phases (4-5):** 4-6 workdays (1 week)
- **Total:** 14-20 workdays (3-4 weeks)

## Success Metrics

### Immediate Success (After Phase 3)

- ✅ Tasks can be created manually and automatically assigned
- ✅ At least one end-to-end workflow tested (e.g., Structural → Lexical)
- ✅ Coordinator operates reliably without manual intervention
- ✅ Status dashboard provides visibility into system state

### Long-term Success (After Phase 5)

- ✅ All agents integrated with task-based orchestration
- ✅ Multi-step workflows execute automatically
- ✅ Conflicts detected and logged
- ✅ Complete audit trail maintained
- ✅ System scales to 100+ tasks without performance issues

## Risk Management

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Coordinator bugs cause task loss | Medium | High | Extensive testing, validation scripts, Git history recovery |
| Agent integration breaks existing workflows | Medium | Medium | Incremental integration, fallback to manual execution |
| GitHub Actions rate limits | Low | Medium | Add delays, use manual execution fallback |
| Task schema evolves incompatibly | Low | High | Version schema, add migration scripts |
| Directory structure corrupted | Low | High | Validation scripts in CI, .gitkeep tracking |

## Next Steps

### Immediate Actions (Week 1)

1. **Architect:** Review and approve architecture artifacts (ADRs, technical design)
2. **Build Automation:** Begin Phase 1 implementation (directory setup, schemas)
3. **Planning Agent:** Create initial task files for Phase 1 work
4. **Agent Orchestrator:** Assign tasks to Build Automation agent (when implemented)

### Short-term Actions (Week 2-3)

1. **Build Automation:** Complete Phase 1 and begin Phase 2 (Agent Orchestrator)
2. **Writer-Editor:** Document directory structure and usage patterns
3. **Architect:** Create Coordinator agent profile
4. **Planning Agent:** Monitor progress, adjust timeline as needed

### Medium-term Actions (Week 4-6)

1. **All Agents:** Update profiles for task-based execution (Phase 3)
2. **Build Automation:** Test end-to-end workflows
3. **Writer-Editor:** Document agent handoff patterns
4. **Coordinator:** Monitor system health and performance

## Approval and Sign-off

This implementation plan requires approval from:

- [ ] **Human Stakeholder:** Overall strategy and priorities
- [ ] **Architect Agent:** Architecture artifacts completeness and correctness
- [ ] **Planning Agent:** Timeline and resource allocation
- [ ] **Build Automation Agent:** Technical feasibility

Once approved, tasks can be created in `work/inbox/` and assigned to respective agents.

---

_Maintained by: Architect Alphonso_  
_Version: 1.0.0_  
_Status: Proposed - Awaiting approval_
