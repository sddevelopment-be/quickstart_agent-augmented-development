Goal: Execute orchestration cycle for task management using file-based approach.

Context: 
- Follow file-based orchestration as per `.github/agents/approaches/file-based-orchestration.md`
- work/collaboration/orchestration-implementation-plan.md
- work/collaboration/AGENT_STATUS.md
- work/collaboration/WORK_LOG.md
- Ensure compliance with general guidelines, operational guidelines, and Directive 014 (Work Log Creation).
- Leverage agent profile `[agent-profile]` and reasoning mode `/analysis-mode` for task execution.

Task:
- Initialize as per AGENTS.md guidelines
- Read Manager Mike's work/collaboration/AGENT_STATUS.md
- Ensure AGENT_STATUS.md is up to date as per relevant `work` directories 
- Following agents/approaches/file-based-orchestration.md:
    - Check work/inbox for task
    - Move to work/assigned/[agent], update status
    - Execute task (see subtask handling below)
    - Update task YAML with result, timestamps
    - Move to work/done/
    - Create follow-up tasks in `work/inbox` for other agents if needed

Subtask Handling:
- Check parent task YAML for subtask references
- Locate subtasks in work/inbox (same timestamp prefix)
- Process sequentially or in parallel as dependencies allow
- Follow same file-based orchestration for each

Documentation Strategy:
- during execution
- single feature, multi-task initiative

Ensure:
- Tasks are selected based on priority and dependencies
- Clear logging of decisions and actions in work log
- Tasks executed incrementally (atomic units)
- Commit after each subtask: `[AGENT]: <task-slug> - <summary>`
- Work log after each subtask (directive 014):
    - Token count: [cumulative from start]
    - Timing: [duration in minutes for this unit]
    - Context size: [files/directives referenced]
    - Timestamps: [ISO 8601 start/end]
- Verify acceptance criteria before marking done
- Save prompt with improvements to work/logs/prompts/ when complete

Context Management:
- Prefer links/references over inlining full docs
- Drop non-essential sections when scope is narrow
- Keep transient reasoning in work/notes (not prompt transcript)

Ambiguity Handling:
- If uncertainty >30%: pause, document, request clarification
- If uncertainty <30%: document assumption, proceed
- Never guess on critical decisions

Avoid:
- Spending time on ambiguity (signal early)
- Silent assumptions (document in work log)
- Skipping acceptance criteria verification