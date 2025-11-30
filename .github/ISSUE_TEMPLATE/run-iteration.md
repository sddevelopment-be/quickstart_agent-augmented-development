---
name: Run Orchestration Iteration
about: Execute an orchestration cycle to process pending tasks
title: '[Iteration] Run orchestration cycle - YYYY-MM-DD'
labels: orchestration, automation, iteration
assignees: copilot
version: 1.1.0
---

## Configuration Parameters (Optional)

_Customize iteration behavior by setting these parameters:_

- **max_tasks**: Maximum number of tasks to process (default: 3)
- **agent_focus**: Target specific agent(s) (e.g., `build-automation`, `curator`)
- **priority_threshold**: Minimum priority level (e.g., `high`, `medium`)
- **mode**: Execution mode (default: `/analysis-mode`)

**Example:** To process up to 5 high-priority build-automation tasks:
```yaml
max_tasks: 5
agent_focus: build-automation
priority_threshold: high
```

## Objective

Execute an orchestration cycle to process pending tasks in the work queue following the file-based orchestration approach.

## Context

- **Orchestration Framework**: Implemented and production-ready (PR #16)
- **Approach**: File-based orchestration (`.github/agents/approaches/file-based-orchestration.md`)
- **Work Directory**: `work/` (inbox, assigned, done, logs, collaboration)
- **Agent Profiles**: `.github/agents/*.agent.md`
- **Directives**: `.github/agents/directives/`
- **Mode**: `/analysis-mode` for task execution

## Current Status

_To be filled by running `template-status-checker.py`:_
```bash
python ops/framework-core/template-status-checker.py
```

_With validation:_
```bash
python ops/framework-core/template-status-checker.py --validate
```

## Execution Instructions

### 1. Initialize
- Initialize as Manager Mike per `AGENTS.md` guidelines
- Read `work/collaboration/AGENT_STATUS.md` for current context
- Verify orchestration framework operational status

### 2. Task Selection
- Check `work/inbox/` for pending tasks
- Run `python work/scripts/agent_orchestrator.py` to assign tasks
- Identify top 3 priority tasks:
  - Priority order: critical > high > medium > normal
  - Consider dependencies (tasks with satisfied dependencies first)
  - Check POC/chain continuity (advance multi-agent chains)

### 3. Task Execution
- Delegate each task to appropriate custom agent
- Follow file-based orchestration lifecycle:
  1. Update status: assigned → in_progress
  2. Execute task per agent specialization
  3. Create artifacts as specified
  4. Update task YAML with result block
  5. Update status: in_progress → done
  6. Move task from `work/assigned/<agent>/` to `work/done/<agent>/`
     - **Important:** Tasks must be moved to the agent-specific subdirectory, not directly to `work/done/` root
  7. Create work log in `work/reports/logs/<agent>/` per Directive 014

### 4. Documentation & Reporting
- Create work log for each completed task (Directive 014)
- Update `work/collaboration/AGENT_STATUS.md`
- Create iteration summary (Manager Mike)
- Capture metrics: duration, tokens, artifacts, validation results
- Commit changes with `report_progress` after each task
- Update PR description with iteration summary
- Post Manager Mike recap comment to PR

## Success Criteria

_Note: These checkboxes can be auto-populated by orchestrator post-execution using `work/scripts/template-status-checker.sh --validate`_

- [ ] At least 1 task completed (or all remaining if fewer than 3)
- [ ] All work logs created per Directive 014
- [ ] `AGENT_STATUS.md` updated with current iteration state
- [ ] Iteration summary created by Manager Mike
- [ ] Metrics captured and reported
- [ ] Framework health assessed (completion rate, validation success, etc.)
- [ ] Zero validation errors or failures
- [ ] All artifacts committed and pushed

## Deliverables

- **Completed Tasks**: Moved to `work/done/<agent>/` subdirectories
- **Work Logs**: Created in `work/reports/logs/<agent>/`
- **Iteration Summary**: Added to `work/collaboration/`
- **Updated Status**: `AGENT_STATUS.md` reflects current state
- **Manager Recap**: Comment posted to PR
- **Metrics Report**: Duration, tokens, artifacts, success rate

## References

- **File-Based Orchestration**: `.github/agents/approaches/file-based-orchestration.md`
- **AGENTS.md**: Root orchestration protocol
- **Directive 014**: Work Log Creation (`.github/agents/directives/014_worklog_creation.md`)
- **ADR-009**: Orchestration Metrics Standard
- **Agent Profiles**: `.github/agents/*.agent.md`
- **Previous Iterations**: Check `work/collaboration/ITERATION_*_SUMMARY.md`

## Example Prompt

```
Execute an orchestration cycle following file-based orchestration approach:

1. Initialize as Manager Mike per AGENTS.md
2. Read work/collaboration/AGENT_STATUS.md
3. Run agent_orchestrator.py to assign pending tasks
4. Execute top 3 priority tasks by delegating to custom agents
5. Create work logs per Directive 014
6. Update AGENT_STATUS.md and create iteration summary
7. Post Manager Mike recap comment

Ensure:
- Tasks selected by priority (critical > high > medium)
- All work logs Directive 014 compliant
- Metrics captured per ADR-009
- Incremental commits with report_progress
- Framework health assessed
```

---

_This issue template enables repeatable orchestration iterations with consistent execution patterns._

## Template Metadata

- **Version:** 1.1.0
- **Last Updated:** 2025-11-24
- **Changelog:**
  - v1.1.0: Added version tracking, optional parameters, status automation script, validation guidance
  - v1.0.0: Initial template creation
