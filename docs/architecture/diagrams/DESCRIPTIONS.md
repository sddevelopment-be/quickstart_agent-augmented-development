# Diagram Accessibility Descriptions

**Purpose:** Provide textual descriptions of architectural diagrams for accessibility and inclusive documentation.  
**Audience:** Vision-impaired users, screen reader users, and all stakeholders requiring text-based diagram interpretation.  
**Last Updated:** 2026-02-14T10:00:00Z  
**Maintained By:** Diagram Daisy (Diagrammer Agent)

---

## How to Use This Document

Each diagram entry provides:
- **Alt Text** (short, <125 characters): High-level summary for quick context
- **Long Description** (2-4 paragraphs): Detailed explanation of structure, flow, and relationships
- **Key Elements**: Major components, transitions, entry/exit points
- **Related Documentation**: Cross-references to architecture documents

Screen reader users can navigate by heading level to find specific diagrams.

---

## 1. Task Lifecycle State Machine

### File
- **Source:** `task-lifecycle-state-machine.puml`
- **Rendered:** `Task_Lifecycle_State_Machine.svg`

### Alt Text
State machine showing task progression through new, assigned, in_progress, done, error, and archived states.

### Long Description

The Task Lifecycle State Machine diagram illustrates all possible states a task can occupy within the file-based orchestration system and the valid transitions between these states. This is a foundational architectural diagram that governs how tasks flow through the system from creation to archival.

The diagram contains six distinct states, each color-coded for visual distinction: **new** (light blue), **assigned** (light yellow), **in_progress** (amber), **done** (light green), **error** (light red), and **archived** (light gray). Each state represents a specific location in the file system and has associated metadata requirements.

The primary flow path begins when a human or planning agent creates a task, entering the **new** state in the `work/inbox/` directory. The coordinator agent then moves it to **assigned** state by relocating the task file to `work/assigned/<agent>/`. When an agent begins execution, the task transitions to **in_progress** state (remaining in the same directory but with updated status metadata). Upon successful completion, the task moves to **done** state in `work/done/`, where it may optionally trigger a follow-up task via the `next_agent` field. After 30 days, completed tasks are moved to **archived** state in `work/archive/YYYY-MM/`.

The error recovery path shows that if an exception occurs during **in_progress**, the task transitions to **error** state. From there, a human can either reset the task back to **assigned** for retry, or move it to **archived** if the failure is unrecoverable. Additionally, completed (**done**) tasks can spawn new tasks through the coordinator's follow-up mechanism, creating a sequential workflow pattern.

### Key Elements

**States:**
- **new**: Initial state, location `work/inbox/`, no owner assigned
- **assigned**: Assigned to specific agent, location `work/assigned/<agent>/`
- **in_progress**: Agent actively working, includes 2-hour timeout policy
- **done**: Completed successfully, location `work/done/`, contains result block
- **error**: Execution failed, requires human intervention
- **archived**: Long-term storage in `work/archive/YYYY-MM/`

**Primary Transitions:**
- **new → assigned**: Coordinator moves task and updates status
- **assigned → in_progress**: Agent starts work, adds `started_at` timestamp
- **in_progress → done**: Agent completes, adds result block, optionally sets `next_agent`
- **done → archived**: Coordinator moves after 30-day retention period
- **done → new**: Coordinator creates follow-up task if `next_agent` specified

**Error Handling Transitions:**
- **in_progress → error**: Exception occurs, agent adds error block
- **error → assigned**: Human resets task for retry
- **error → archived**: Unrecoverable failure, task cancelled

**Entry/Exit Points:**
- **Entry**: System start `[*]` → **new** state
- **Exit**: **archived** → system end `[*]`

### Related Documentation
- [Async Multi-Agent Orchestration Architecture](../async_multiagent_orchestration.md)
- [ADR-003: Task Lifecycle and State Management](../adrs/ADR-003-task-lifecycle-state-management.md)
- [ADR-008: File-Based Async Coordination](../adrs/ADR-008-file-based-async-coordination.md)

---

## 2. Orchestration Workflow (Overview)

### File
- **Source:** `orchestration-workflow.puml`
- **Rendered:** `Agent_Orchestration_Overview_workflow.svg`

### Alt Text
Sequence diagram of complete orchestration workflow from task creation through execution, sequencing, and archival.

### Long Description

The Orchestration Workflow diagram provides a comprehensive sequence view of the file-based asynchronous multi-agent coordination system, showing how all components interact over time. This diagram illustrates the complete lifecycle from initial task request to long-term archival, including coordination logic and handoff patterns.

The workflow begins with a human stakeholder requesting work from a planning agent, who creates a task YAML file in the `work/inbox/` directory with status "new". The coordinator agent polls the inbox every 5 minutes, detects new tasks, and assigns them by moving task files to agent-specific directories under `work/assigned/`. The coordinator also logs all assignments to a workflow log for tracking.

When an agent polls its assigned directory, it picks up the task, updates the status to "in_progress", loads necessary context, and generates the requested artifacts. Upon completion, the agent updates the task with a result block and moves it to `work/done/`. Critically, if the agent specifies a `next_agent` field in the result block, this triggers workflow sequencing.

The coordinator monitors the `work/done/` directory for completed tasks with `next_agent` values. When detected, it automatically creates a new follow-up task in the inbox, assigns it to the specified next agent, and logs the handoff. This enables sequential multi-agent workflows without direct agent-to-agent communication. In this example, a structural agent completes initial work and hands off to a lexical agent for refinement.

Finally, the coordinator performs periodic maintenance by checking task age in the done directory. Tasks older than 30 days are moved to `work/archive/` for long-term storage. Throughout the entire workflow, status updates are maintained in collaboration artifacts like `WORKFLOW_LOG.md`, `HANDOFFS.md`, and `AGENT_STATUS.md`, which humans can review as a monitoring dashboard.

### Key Elements

**Actors:**
- **Human**: Initiates work requests and monitors status
- **Planning Agent**: Creates initial task specifications
- **Coordinator Agent**: Orchestrates task assignment, sequencing, and archival
- **Domain Agents** (Structural, Lexical): Execute specialized work
- **Databases/Directories**: `work/inbox/`, `work/assigned/`, `work/done/`, `work/archive/`
- **Collaboration Artifacts**: Workflow logs, handoff tracking, agent status

**Key Sequences:**
1. **Task Creation**: Human → Planning Agent → inbox directory
2. **Task Assignment**: Coordinator polls inbox → moves to `assigned/<agent>/`
3. **Task Execution**: Agent polls assigned directory → updates status → generates artifacts → moves to done
4. **Workflow Sequencing**: Coordinator detects `next_agent` → creates follow-up task → assigns to next agent
5. **Archival**: Coordinator moves old tasks (>30 days) to archive
6. **Status Monitoring**: Continuous updates to collaboration artifacts, human reviews dashboard

**Workflow Triggers:**
- **Coordinator polling**: Every 5 minutes for new tasks
- **Agent polling**: Each agent checks its assigned directory periodically
- **Handoff trigger**: `next_agent` field in completed task result
- **Archive trigger**: Task age exceeds 30 days

### Related Documentation
- [Async Multi-Agent Orchestration Architecture](../async_multiagent_orchestration.md)
- [ADR-005: Coordinator Agent Pattern](../adrs/ADR-005-coordinator-agent-pattern.md)
- [ADR-008: File-Based Async Coordination](../adrs/ADR-008-file-based-async-coordination.md)
- [Orchestration User Guide](../../../work/docs/orchestration-guide.md)

---

## 3. Simple Sequential Workflow (with Metrics)

### File
- **Source:** `workflow-sequential-flow.puml`
- **Rendered:** `Simple_Sequential_Workflow.svg`
- **Last Updated:** 2025-11-27T08:02:23Z
- **Rendering Status:** ✅ Validated - Successfully rendered with PlantUML v1.2023.13

### Alt Text
Sequential agent handoff pattern with timing, token usage, and artifact metrics annotations per ADR-009 standards.

### Long Description

The Simple Sequential Workflow diagram demonstrates the most basic multi-agent collaboration pattern: two agents working in sequence with automatic handoff coordination, enhanced with metrics visualization to illustrate ADR-009 orchestration standards. This pattern is fundamental to understanding how the orchestration system enables agent chaining without direct communication while maintaining performance observability.

The workflow begins when a planning agent creates task-001.yaml in the inbox, specifying that the structural agent should generate a REPO_MAP.md artifact. The coordinator agent polls the inbox with a 5-minute polling interval and assignment latency under 10 seconds. The coordinator discovers the new task and assigns it to the structural agent by moving the file to `work/assigned/structural/` and updating the status to "assigned", adding an `assigned_at` timestamp for timeout tracking.

The structural agent polls its assigned directory, picks up task-001, and updates the status to "in_progress". The diagram now shows key performance metrics: duration of approximately 15 minutes, token usage of 12K input and 5K output tokens, and creation of 1 artifact. After generating the REPO_MAP.md file, the structural agent completes the task by adding a result block to the YAML that includes a summary of work completed, a list of artifacts created, and critically, `next_agent: lexical` with a description of the follow-up work needed ("Refine REPO_MAP"). The result block also contains the metrics structure per ADR-009: duration_minutes (15), token_count breakdown, and artifacts_created (1). The structural agent then moves the task to `work/done/`.

This triggers the handoff mechanism with measured latency. The coordinator detects that task-001 in the done directory has a `next_agent` field, introducing approximately 2 minutes of handoff latency (time between completed_at and next task created_at). The coordinator creates task-002.yaml in the inbox, specifying the lexical agent, including the REPO_MAP.md artifact as input context, declaring a dependency on task-001, and noting that it was created by the structural agent. The coordinator then assigns task-002 to the lexical agent following the same assignment pattern.

The lexical agent polls its assigned directory, picks up task-002, updates status to "in_progress", and exhibits different performance characteristics: duration of approximately 8 minutes, token usage of 8K input and 3K output tokens, and modification of 1 artifact. The lexical agent refines the REPO_MAP.md file and completes the task with a result block containing the same metrics structure. Since no `next_agent` is specified in this result block, the workflow terminates.

The diagram concludes with aggregate metrics showing the complete sequential workflow: total duration of approximately 25 minutes (15 + 8 + 2 latency), total token usage of 28K (20K input, 8K output), 1 artifact created and 1 modified, and 2 minutes of handoff latency. This demonstrates the fire-and-forget asynchronous pattern with full observability per ADR-009 orchestration metrics standards.

### Key Elements

**Agents in Sequence:**
1. **Structural Agent**: Initial work (generate REPO_MAP.md)
   - Duration: ~15 minutes
   - Tokens: 12K input, 5K output
   - Artifacts: 1 created
2. **Lexical Agent**: Follow-up work (refine REPO_MAP.md)
   - Duration: ~8 minutes
   - Tokens: 8K input, 3K output
   - Artifacts: 1 modified

**Task Files:**
- **task-001.yaml**: Initial task for structural agent
- **task-002.yaml**: Follow-up task for lexical agent (auto-created)

**Handoff Mechanism:**
- Structural agent completes with `next_agent: lexical` field
- Coordinator detects this field in done directory
- Handoff latency: ~2 minutes (completed_at → created_at)
- Coordinator creates task-002 with:
  - `agent: lexical`
  - `dependencies: [task-001]`
  - `created_by: structural`
  - Same artifacts as context

**Directory Flow:**
- Task-001: inbox → assigned/structural → done
- Task-002: inbox → assigned/lexical → done

**Metrics Per ADR-009:**
- Total duration: ~25 minutes (15 + 8 + 2 latency)
- Total tokens: 28K (20K input, 8K output)
- Artifacts: 1 created, 1 modified
- Handoff latency: 2 minutes
- Coordinator polling: 5-minute interval, <10s assignment time

**Timing:**
- Non-blocking: Structural agent doesn't wait for lexical agent
- Asynchronous: Lexical agent picks up task when available
- Measured: All timing captured in metrics block per ADR-009

### Related Documentation
- [Async Multi-Agent Orchestration Architecture](../async_multiagent_orchestration.md)
- [Workflow Patterns Documentation](../design/workflow-patterns.md)
- [Agent Handoff Guide](../../../work/docs/agent-handoffs.md)

---

## 4. Parallel Execution Workflow

### File
- **Source:** `workflow-parallel-flow.puml`
- **Rendered:** `Parallel_Execution_Workflow.svg`

### Alt Text
Parallel workflow pattern showing three independent agents (Structural, Architect, Diagrammer) executing simultaneously.

### Long Description

The Parallel Execution Workflow diagram illustrates how the orchestration system maximizes throughput by enabling multiple agents to work concurrently on independent tasks. This pattern is essential for batch processing scenarios where tasks have no dependencies on each other.

The workflow begins with a planning agent creating three separate task files simultaneously in the inbox: task-001.yaml for the structural agent (to generate REPO_MAP.md), task-002.yaml for the architect agent (to create ADR-005.md), and task-003.yaml for the diagrammer agent (to create workflow.puml). All three tasks are marked with status "new" and have no dependencies declared.

The coordinator agent polls the inbox and discovers all three tasks during a single polling cycle. Because none of these tasks depend on each other, the coordinator can assign all three simultaneously. It moves task-001 to `work/assigned/structural/`, task-002 to `work/assigned/architect/`, and task-003 to `work/assigned/diagrammer/`. The diagram emphasizes this crucial point: all three assignments happen without blocking, enabling true parallel execution.

Each agent independently polls its own assigned directory. When they discover their respective tasks, they all begin work simultaneously. The diagram shows three parallel execution lanes with different durations: the structural agent completes in 15 minutes, the architect agent takes 30 minutes, and the diagrammer agent finishes in 20 minutes. Each agent updates its task status to "in_progress", performs its specialized work, and moves the completed task to the done directory.

The coordinator monitors the done directory and confirms when all three tasks are complete. Because these tasks have no dependencies between them and none specify a `next_agent`, no follow-up tasks are created. The diagram highlights the efficiency gain: instead of requiring 65 minutes (15 + 30 + 20) for sequential execution, the parallel workflow completes in just 30 minutes—the duration of the longest individual task. This demonstrates how the asynchronous, file-based coordination model removes blocking dependencies and maximizes agent throughput.

### Key Elements

**Parallel Agents:**
- **Structural Agent**: Generates REPO_MAP.md (15 min duration)
- **Architect Agent**: Creates ADR-005.md (30 min duration)  
- **Diagrammer Agent**: Creates workflow.puml (20 min duration)

**Task Independence:**
- No dependencies declared between tasks
- Each agent works in isolation
- No shared artifacts during execution
- Results aggregated only after all complete

**Batch Assignment:**
- Coordinator assigns all three tasks in single polling cycle
- No blocking: all assignments happen simultaneously
- Each agent polls independently

**Efficiency Metrics:**
- **Sequential time**: 65 minutes (15 + 30 + 20)
- **Parallel time**: 30 minutes (max of [15, 30, 20])
- **Throughput improvement**: 2.17x faster

**Completion Pattern:**
- All tasks complete independently
- No `next_agent` fields (workflow terminates)
- Coordinator confirms all done before declaring success

### Related Documentation
- [Async Multi-Agent Orchestration Architecture](../async_multiagent_orchestration.md)
- [Performance Benchmarks](../design/performance-analysis.md)
- [Workflow Patterns: Parallel Execution](../design/workflow-patterns.md#parallel)

---

## 5. Convergent Workflow

### File
- **Source:** `workflow-convergent-flow.puml`
- **Rendered:** `Convergent_Workflow.svg`

### Alt Text
Convergent pattern where three parallel agents (Structural, Lexical, Architect) contribute artifacts to single Curator synthesis.

### Long Description

The Convergent Workflow diagram demonstrates an advanced orchestration pattern where multiple independent agents perform parallel work and then converge their outputs to a single synthesis agent for validation and integration. This pattern is critical for cross-agent consistency checks and quality assurance workflows.

The workflow begins with a planning agent creating three independent tasks: task-001 for the structural agent (to generate REPO_MAP.md), task-002 for the lexical agent (to generate LEX_REPORT.md), and task-003 for the architect agent (to create ADR-002.md). Critically, all three task specifications include the same `next_agent: curator` field, signaling that their outputs should converge to a curator agent for synthesis work.

The coordinator assigns all three tasks simultaneously, enabling parallel execution. The structural, lexical, and architect agents work independently in their respective domains, each generating their specialized artifacts without knowledge of the other agents' work. The diagram shows three parallel execution lanes, emphasizing that these agents do not coordinate directly or share state during execution.

When each agent completes its work, it adds a result block containing the `next_agent: curator` field and moves its task to the done directory. The coordinator continuously monitors the done directory, and when it detects that all three tasks (001, 002, and 003) are complete and all specify the same next agent, it triggers the convergent handoff mechanism.

The coordinator creates a single new task (task-004) for the curator agent. This synthesis task bundles all three artifacts—REPO_MAP.md, LEX_REPORT.md, and ADR-002.md—into the artifact list, declares dependencies on all three predecessor tasks (001, 002, 003), and includes explicit instructions for the curator to "validate consistency across structural, lexical, and architecture artifacts." The coordinator assigns this curator task, which now has access to all converged outputs.

The curator agent picks up the synthesis task and performs cross-validation work. It examines all three artifacts, identifies any discrepancies or inconsistencies, and generates a DISCREPANCY_REPORT.md documenting findings. The curator completes without specifying a `next_agent`, terminating the convergent workflow. This pattern demonstrates how the orchestration system enables sophisticated multi-agent validation workflows where parallel specialist work converges to a generalist synthesizer for quality assurance.

### Key Elements

**Parallel Generation Phase:**
- **Structural Agent**: Generates REPO_MAP.md
- **Lexical Agent**: Generates LEX_REPORT.md
- **Architect Agent**: Creates ADR-002.md
- All three complete with `next_agent: curator`

**Convergent Synthesis Phase:**
- **Curator Agent**: Receives all three artifacts
- Performs cross-validation and consistency checking
- Generates DISCREPANCY_REPORT.md

**Handoff Coordination:**
- Coordinator detects three completed tasks with same `next_agent`
- Creates single synthesis task (task-004) bundling all artifacts
- Synthesis task declares dependencies: [task-001, task-002, task-003]
- Instructions explicitly note convergent validation purpose

**Artifact Flow:**
- **Input artifacts**: REPO_MAP.md, LEX_REPORT.md, ADR-002.md (from three parallel agents)
- **Output artifact**: DISCREPANCY_REPORT.md (from curator synthesis)
- No artifact modification by curator—read-only validation

**Workflow Termination:**
- Curator completes without `next_agent` field
- Workflow successfully terminates after synthesis
- Demonstrates: Three parallel → One synthesis pattern

### Related Documentation
- [Async Multi-Agent Orchestration Architecture](../async_multiagent_orchestration.md)
- [Workflow Patterns: Convergent Synthesis](../design/workflow-patterns.md#convergent)
- [Curator Agent Profile](../../.github/agents/profiles/curator.md)
- [Cross-Agent Validation Patterns](../design/validation-patterns.md)

---

## 6. Orchestration Implementation Timeline

### File
- **Source:** `orchestration-phases-timeline.puml`
- **Rendered:** (Gantt chart - typically viewed in PlantUML renderer)

### Alt Text
Gantt chart showing five implementation phases with dependencies, durations, and priorities over 3-4 week timeline.

### Long Description

The Orchestration Implementation Timeline diagram is a Gantt chart that visualizes the planned rollout of the file-based orchestration system across five distinct phases. This timeline shows both critical path dependencies and optional enhancement phases, helping stakeholders understand implementation sequencing and resource allocation.

**Phase 1: Core Infrastructure** (2-3 days, CRITICAL) forms the foundation and has no dependencies. This phase delivers the directory structure (`work/inbox/`, `work/assigned/`, `work/done/`, `work/archive/`), the task YAML schema definition, validation scripts to ensure schema compliance, and comprehensive documentation in `work/README.md`. This phase must complete before any other work can proceed, establishing the file-based communication protocol.

**Phase 2: Coordinator Implementation** (3-4 days, CRITICAL) depends on Phase 1 and implements the orchestration logic. Deliverables include the `agent_orchestrator.py` Python script, task assignment logic (inbox monitoring and file movement), workflow sequencing (detecting `next_agent` and creating follow-ups), timeout detection for stuck tasks, and the coordinator agent profile. This phase completes the critical path for minimal viable orchestration.

**Phase 3: Agent Integration** (5-7 days, HIGH priority) depends on Phase 2 and integrates existing agents with the orchestration system. This phase updates all agent profiles with orchestration instructions, documents the execution protocol (how agents poll, update status, and complete tasks), performs comprehensive end-to-end testing of all workflow patterns (sequential, parallel, convergent), and creates detailed handoff pattern documentation. With Phase 3 complete, the orchestration system is fully operational.

The timeline then splits into two optional enhancement paths that can proceed in parallel:

**Phase 4: GitHub Actions** (2-3 days, MEDIUM priority, Optional) depends on Phase 3 and adds CI/CD automation. Deliverables include GitHub Actions workflow files for automated orchestrator execution, CI configuration for continuous monitoring, manual trigger options for on-demand orchestration, and CI setup documentation. This phase reduces manual orchestration burden.

**Phase 5: Validation & Monitoring** (2-3 days, MEDIUM priority, Optional) can start after Phase 2 completion and runs in parallel with Phase 3-4. It enhances system observability with improved validation tools, a monitoring dashboard for real-time status, metrics collection for performance analysis, and troubleshooting guides for common issues.

The diagram footer summarizes the timeline: the critical path (Phase 1 → Phase 2 → Phase 3) requires 10-14 workdays or 2-3 weeks. Optional enhancements (Phase 4-5) add 4-6 workdays or approximately 1 week. The total implementation timeline spans 14-20 workdays or 3-4 weeks, depending on whether optional phases are pursued.

### Key Elements

**Critical Path Phases (Sequential):**
1. **Phase 1: Core Infrastructure** (2-3 days)
   - Directory structure, YAML schema, validation scripts
   - No dependencies, must complete first
2. **Phase 2: Coordinator Implementation** (3-4 days)
   - Orchestrator logic, assignment, sequencing, timeouts
   - Depends on Phase 1
3. **Phase 3: Agent Integration** (5-7 days)
   - Agent profile updates, execution protocol, E2E testing
   - Depends on Phase 2

**Optional Enhancement Phases (Parallel):**
4. **Phase 4: GitHub Actions** (2-3 days, MEDIUM)
   - CI/CD automation, workflows, manual triggers
   - Depends on Phase 3
5. **Phase 5: Validation & Monitoring** (2-3 days, MEDIUM)
   - Enhanced validation, dashboards, metrics, troubleshooting
   - Can start after Phase 2 (parallel to Phase 3)

**Timeline Metrics:**
- **Critical path duration**: 10-14 workdays (2-3 weeks)
- **Optional path duration**: 4-6 workdays (1 week)
- **Total timeline**: 14-20 workdays (3-4 weeks)

**Milestones:**
- **P1 Complete**: Core infrastructure ready
- **P2 Complete**: Coordinator operational (end of critical path for MVP)
- **P3 Complete**: Agents integrated (full operational capability)
- **P4/P5 Complete**: Enhanced automation and monitoring

### Related Documentation
- [Async Orchestration Technical Design](../design/async_orchestration_technical_design.md)
- [Implementation Roadmap](../design/implementation-roadmap.md)
- [Project Timeline and Milestones](../../../PROJECT_STATUS.md)

---

## 7. Metrics Dashboard Concept

### File
- **Source:** `metrics-dashboard-concept.puml`
- **Rendered:** Generated by CI pipeline (see GitHub Actions workflow artifacts on PRs)
- **Last Updated:** 2025-11-27T08:02:23Z
- **Rendering Status:** ✅ Syntax validated with PlantUML v1.2023.13. Full SVG rendering with Graphviz performed by CI pipeline (see `.github/workflows/diagram-rendering.yml`). Rendered diagrams available as workflow artifacts for 7 days on pull requests.

### Alt Text
Component diagram showing ADR-009 metrics capture points, quality standards, and dashboard output structure.

### Long Description

The Metrics Dashboard Concept diagram visualizes the complete ADR-009 orchestration metrics and quality standards framework as an integrated system. This component diagram maps the relationship between task lifecycle stages, metrics collection points, quality standards enforcement, and dashboard output artifacts, providing a reference architecture for implementing ADR-009 compliance across all agents.

The diagram is organized into four major packages that represent distinct concerns:

**Task Lifecycle Package** defines the temporal flow of agent execution with five key stages: Task Start (when an agent picks up work), Context Loading (reading files for task context), Artifact Generation (creating or modifying deliverables), Artifact Validation (checking quality and correctness), and Task Completion (finalizing results and moving to done directory). Each stage is color-coded in green to indicate these are metrics capture points.

**Metrics Collection Points Package** details the seven data elements required or recommended by ADR-009. Required fields include duration_minutes (total execution time from task pickup to completion), token_count (structured as input, output, and total token usage), context_files_loaded (count of files read), and artifacts_created/artifacts_modified (counts of deliverables by action type). Optional fields include per_artifact_timing (detailed breakdown with name, action, and duration_seconds for each artifact) and handoff_latency_seconds (time between completed_at and next_task created_at). Each metric has an associated note explaining its purpose and measurement methodology.

**Quality Standards Package** defines the four quality assurance mechanisms mandated by ADR-009. Per-Artifact Validation requires explicit integrity markers (✅ for full validation, ⚠️ for partial validation, ❗️ for validation failure) to be applied to every artifact in work logs. Tiered Work Logging establishes a two-tier structure: Core Tier (required, containing Context, Approach, Execution Steps, Artifacts Created with markers, Outcomes, and Metadata, targeting 100-200 lines) and Extended Tier (optional, adding Challenges, Research Notes, Collaboration Notes, and Technical Details). Accessibility Descriptions mandate that all visual artifacts have entries in DESCRIPTIONS.md with alt-text (under 125 characters), long description (2-4 paragraphs), key elements list, related documentation links, and updated timestamp. Rendering Verification requires syntax checking through CI integration (preferred), local script rendering, or manual verification, with unverified diagrams marked with ⚠️.

**Dashboard Output Package** shows the three artifact types that consume collected metrics and quality validations. Task Result Block is the YAML structure added to task files in the done directory, containing summary, artifacts list, structured metrics block, and completion timestamp. Work Log is the markdown narrative stored in work/logs/, structured with Context, Approach, Execution Steps, Artifacts Created (including integrity markers from validation), Outcomes, and Metadata (matching result metrics for consistency). DESCRIPTIONS.md Entry is the accessibility metadata for visual artifacts, structured with diagram filename, alt-text, detailed description, and updated timestamp.

The diagram includes explicit data flow connections showing how lifecycle stages feed metrics collection (Task Start → duration tracking, Context Loading → files and tokens, Generation → artifacts and per-artifact timing, Validation → artifact markers and rendering checks, Completion → handoff latency and result block). Metrics flow into both the Task Result Block and Work Log, ensuring consistency. Quality standards feed their respective outputs (artifact validation to work log, logging structure to work log, accessibility to DESCRIPTIONS.md, rendering to work log). Finally, cross-connections show that result blocks provide metadata consistency to work logs, and work logs cross-reference DESCRIPTIONS.md entries for visual artifacts.

The legend at the bottom summarizes ADR-009 compliance requirements: all orchestrated tasks must include structured metrics blocks, provide per-artifact integrity markers, follow tiered work logging with Core tier minimum, add accessibility descriptions for visual artifacts, and validate diagram rendering or mark unverified. The purpose is stated as enabling benchmarking, quality assurance, inclusive documentation, and framework tuning.

### Key Elements

**Metrics Capture Points (Required):**
- **duration_minutes**: Total task execution time
- **token_count**: Input, output, and total tokens
- **context_files_loaded**: Count of files read
- **artifacts_created**: Count of new files
- **artifacts_modified**: Count of edited files

**Metrics Capture Points (Optional):**
- **per_artifact_timing**: Detailed breakdown per artifact (name, action, duration_seconds)
- **handoff_latency_seconds**: Time between task completion and next task creation

**Quality Validation Markers:**
- ✅ Full validation: Artifact meets all quality criteria
- ⚠️ Partial validation: Artifact created but has known limitations
- ❗️ Validation failed: Artifact has errors requiring correction

**Work Log Tiers:**
- **Core Tier (Required)**: Context, Approach, Execution Steps, Artifacts Created, Outcomes, Metadata (100-200 lines)
- **Extended Tier (Optional)**: Challenges, Research Notes, Collaboration Notes, Technical Details (additional 100-300 lines)

**Accessibility Standards:**
- Alt-text: <125 characters summary
- Long description: 2-4 paragraphs narrative
- Key elements: Structured list of components
- Related documentation: Cross-references
- Updated timestamp: Git-tracked freshness

**Dashboard Outputs:**
- **Task Result Block**: YAML structure in task file (done directory)
- **Work Log**: Markdown narrative in work/logs/
- **DESCRIPTIONS.md Entry**: Accessibility metadata for diagrams

**Data Flow:**
- Lifecycle stages → Metrics collection
- Metrics → Result block + Work log
- Quality standards → Work log + DESCRIPTIONS.md
- Result block → Work log (metadata consistency)
- Work log → DESCRIPTIONS.md (cross-reference)

### Related Documentation
- [ADR-009: Orchestration Metrics and Quality Standards](../adrs/ADR-009-orchestration-metrics-standard.md)
- [Directive 014: Work Log Creation Standards](../../../.github/agents/directives/014_worklog_creation.md)
- [File-Based Orchestration Approach](../../../.github/agents/approaches/file-based-orchestration.md)
- [Task Lifecycle State Machine](#1-task-lifecycle-state-machine) (this document)

---

## 8. Domain Core — C4 Container View

### File
- **Source:** `domain-core-c4-container.puml`

### Alt Text
C4 container diagram showing the four domain modules and their relationships to the framework and file system.

### Long Description
This C4 Level 2 container diagram depicts the Domain Core layer (`src/domain/`) as four bounded contexts within a system boundary. The Collaboration container handles task lifecycle and status state machines via the Repository pattern (ADR-042). The Doctrine container provides immutable models for agents, directives, tactics, approaches, styleguides, and templates with dedicated parsers and validators (ADR-045). The Specifications container tracks feature status and specification lifecycle as an emerging context. The Common container provides shared path resolution utilities with no domain semantics.

External systems include the Framework/Application Layer (orchestration, CLI tools, dashboard) which queries and manages all three domain contexts, and the File System which stores YAML task files and Markdown doctrine sources. All three domain contexts depend on Common for path utilities. Collaboration reads and writes YAML task files; Doctrine reads Markdown doctrine sources.

### Key Elements
**Bounded Contexts:**
- Collaboration: Task lifecycle, status state machine, repository pattern, query operations
- Doctrine: Immutable governance models, parsers, validators, source traceability
- Specifications: Feature status tracking (emerging)
- Common: Path resolution utilities, no domain semantics

**External Systems:**
- Framework / Application Layer: orchestration consumer
- File System: YAML and Markdown persistence

### Related Documentation
- [Domain Core Component Overview](../component-overview.md)
- [ADR-042: Task Lifecycle](../adrs/ADR-042-task-lifecycle-domain-model.md)
- [ADR-045: Doctrine Concept Domain Model](../adrs/ADR-045-doctrine-concept-domain-model.md)
- [ADR-046: Domain Module Refactoring](../adrs/ADR-046-domain-module-refactoring.md)

---

## 9. Collaboration Bounded Context — Class Diagram

### File
- **Source:** `domain-collaboration-classes.puml`

### Alt Text
Class diagram showing TaskStatus state machine, TaskRepository, TaskQueryResult, and supporting enums for the collaboration context.

### Long Description
This class diagram details the Collaboration bounded context. The central element is the TaskStatus enum, a string-based enumeration with seven states (NEW, INBOX, ASSIGNED, IN_PROGRESS, BLOCKED, DONE, ERROR) that enforces valid transitions through methods like `can_transition_to()` and `validate_transition()`. Terminal states are DONE and ERROR. The typical flow proceeds from NEW through INBOX, ASSIGNED, and IN_PROGRESS to DONE.

Supporting enums include TaskMode (ANALYSIS, CREATIVE, META, PROGRAMMING, PLANNING) and TaskPriority (CRITICAL through LOW with ordering and urgency methods). The TaskRepository class provides file-system-backed query methods (`find_all`, `find_open_tasks`, `find_by_status`, `find_by_agent`) and returns TaskQueryResult instances. TaskQueryResult is a chainable dataclass supporting CQRS-style read projections with `filter_by_status()` and `filter_by_agent()` methods.

### Key Elements
**State Machine:**
- TaskStatus: 7 states with validated transitions, terminal state detection
- Flow: NEW → INBOX → ASSIGNED → IN_PROGRESS → DONE

**Supporting Types:**
- TaskMode: reasoning mode classification
- TaskPriority: urgency ordering with `is_urgent()` method

**Query Infrastructure:**
- TaskRepository: file-system-backed query operations
- TaskQueryResult: chainable result set for CQRS read projections

### Related Documentation
- [Collaboration Context README](../../src/domain/collaboration/README.md)
- [ADR-042: Task Lifecycle](../adrs/ADR-042-task-lifecycle-domain-model.md)
- [Task Lifecycle State Machine](#1-task-lifecycle-state-machine) (this document)

---

## 10. Doctrine Bounded Context — Class Diagram

### File
- **Source:** `domain-doctrine-classes.puml`

### Alt Text
Class diagram showing frozen domain models, parsers, and validators for the doctrine governance context.

### Long Description
This class diagram illustrates the Doctrine bounded context, organized into three packages. The Domain Models package contains six frozen (immutable) dataclasses: Agent (with capabilities, required directives, handoff patterns, and primer matrix), Directive (numbered governance rules with enforcement levels), Tactic (procedural steps with prerequisites and outcomes), Approach (conceptual frameworks with principles), StyleGuide (scoped rules with enforcement), and Template (output structure contracts with required and optional sections). Each model tracks its source file path and SHA-256 content hash for change detection. Agent composes HandoffPattern and PrimerEntry value objects.

The Parsers package provides four dedicated parsers (DirectiveParser, AgentParser, TacticParser, ApproachParser), each transforming Markdown source files into their corresponding frozen domain model. The Validators package contains CrossReferenceValidator (checking inter-model references), MetadataValidator (checking agent metadata completeness), and IntegrityChecker (detecting duplicate IDs and circular dependencies). All validators return ValidationResult objects with valid/invalid status, errors, and warnings.

### Key Elements
**Domain Models (all frozen/immutable):**
- Agent: profiles with capabilities, handoff patterns, primer matrix
- Directive, Tactic, Approach: governance artifacts with source traceability
- StyleGuide, Template: output format contracts
- HandoffPattern, PrimerEntry: Agent value objects

**Parsers:**
- DirectiveParser, AgentParser, TacticParser, ApproachParser: Markdown-to-model transformation

**Validators:**
- CrossReferenceValidator, MetadataValidator, IntegrityChecker: batch validation returning ValidationResult

### Related Documentation
- [Doctrine Context README](../../src/domain/doctrine/README.md)
- [ADR-045: Doctrine Concept Domain Model](../adrs/ADR-045-doctrine-concept-domain-model.md)

---

## 11. Common Utilities — Class Diagram

### File
- **Source:** `domain-common-classes.puml`

### Alt Text
Simple class diagram showing the path_utils module with repository path resolution functions.

### Long Description
This minimal class diagram shows the Common utilities layer, which contains a single module: path_utils. The module provides three functions for resolving standard repository paths: `get_repo_root()`, `get_work_dir()`, and `get_agents_dir()`, each accepting a current file path and returning the resolved absolute path. The module carries no domain semantics — it exists as a leaf dependency that all bounded contexts may use without introducing coupling between domain contexts.

### Key Elements
**Module:**
- path_utils: `get_repo_root()`, `get_work_dir()`, `get_agents_dir()`

**Design Principle:**
- No domain semantics — pure infrastructure
- Leaf dependency — all contexts may depend on it

### Related Documentation
- [Common Context README](../../src/domain/common/README.md)
- [ADR-046: Domain Module Refactoring](../adrs/ADR-046-domain-module-refactoring.md)

---

## 12. Specifications Bounded Context — Class Diagram

### File
- **Source:** `domain-specifications-classes.puml`

### Alt Text
Class diagram showing the FeatureStatus enum for the emerging specifications bounded context.

### Long Description
This class diagram represents the Specifications bounded context, which is currently an emerging context with minimal implementation. The only implemented element is the FeatureStatus enum with five states: DRAFT, PLANNED, IN_PROGRESS, IMPLEMENTED, and DEPRECATED. The lifecycle flows from DRAFT through PLANNED and IN_PROGRESS to IMPLEMENTED, with DEPRECATED as a terminal state. The enum provides `is_active()` and `is_complete()` convenience methods.

A note indicates that additional models (Specification, Feature, Initiative, Portfolio) are planned but not yet implemented, marking this as a context that will grow as the framework matures.

### Key Elements
**Implemented:**
- FeatureStatus: 5-state lifecycle enum with active/complete classification

**Planned (not yet implemented):**
- Specification, Feature, Initiative, Portfolio domain models

### Related Documentation
- [Specifications Context README](../../src/domain/specifications/README.md)
- [ADR-046: Domain Module Refactoring](../adrs/ADR-046-domain-module-refactoring.md)

---

## 13. Control Plane Reference Architecture (CQRS)

### File
- **Source:** `control-plane-reference-architecture.puml`

### Alt Text
C4 container diagram showing the Local Agent Control Plane with CQRS separation of command and query paths.

### Long Description
This C4 Level 2 container diagram depicts the target-state reference architecture for the Local Agent Control Plane, organized across six system boundaries with explicit CQRS separation. The diagram uses two visual conventions: default blue for committed scope and yellow for deferred/optional components.

The Human Operator interacts with two Control Planes: a Localhost Dashboard (Flask + SocketIO for real-time monitoring) and an Interactive Console (CLI/TUI for task initiation). Both control planes send commands (start, cancel, retry) to a Coordination Service in the Service Layer, which validates governance constraints and dispatches to the Distributor Layer. The Distributor uses the Strategy pattern with three implementations: Direct Distributor (in-process, default), Queue Distributor (asyncio.Queue/Redis, deferred), and Workflow Distributor (Kestra/Temporal, deferred).

The Execution Layer contains CLI Execution Adapters (wrapping claude-code, codex, opencode via subprocess), an SDK Execution Adapter (direct API calls, deferred), and Other Tool Adapters (YAML-configured). All execution adapters write artifacts, stdout/stderr captures, and execution events to the Storage Layer.

The read path flows through a Query Service facade that aggregates data from the Telemetry Store (JSONL primary + SQLite index), Artifacts & Logs (filesystem), and Task State (YAML files in `work/`). Query flows are shown as dashed purple lines to distinguish them from command flows.

### Key Elements
**Control Planes:**
- Localhost Dashboard: real-time monitoring (ADR-032)
- Interactive Console: task initiation (ADR-025)

**Service Layer:**
- Coordination Service: command validation, governance, dispatch, event emission

**Distributor (Strategy Pattern):**
- Direct Distributor: in-process, default (committed)
- Queue Distributor: buffered dispatch (deferred)
- Workflow Distributor: durable orchestration (deferred)

**Execution Layer:**
- CLI Execution Adapter: subprocess-based tool wrapping (ADR-029)
- SDK Execution Adapter: direct API (deferred)
- Other Tool Adapters: YAML-configured (ADR-025)

**Query Side:**
- Query Service: read-model facade for telemetry, task state, artifacts

**Storage:**
- Telemetry Store: JSONL append-only log + SQLite materialized index
- Artifacts & Logs: filesystem-based captures
- Task State: YAML files (ADR-008)

### Related Documentation
- [Technical Design: Local Agent Control Plane](../design/local-agent-control-plane-architecture.md)
- [ADR-047: CQRS Pattern](../adrs/ADR-047-cqrs-local-agent-control-plane.md)
- [ADR-048: Run Container Concept](../adrs/ADR-048-run-container-concept.md)
- [ADR-049: Async Execution Engine](../adrs/ADR-049-async-execution-engine.md)
- [Implementation Mapping](../design/control-plane-implementation-mapping.md)

---

## Maintenance and Updates

### Updating Descriptions

When diagrams are modified or new diagrams added:

1. **Add new entry** to this document following the template structure
2. **Update alt text** to reflect changes (keep <125 characters)
3. **Revise long description** to explain new flows or components
4. **Update key elements** list with new states, agents, or transitions
5. **Cross-reference** new or updated architecture documentation
6. **Update "Last Updated" date** at top of document

### Description Template

```markdown
## N. [Diagram Title]

### File
- **Source:** `filename.puml`
- **Rendered:** `Filename.svg`

### Alt Text
[One sentence, <125 characters, high-level purpose]

### Long Description

[2-4 paragraphs explaining:
- What the diagram shows (type, scope, purpose)
- How components relate and flow
- Critical decision points or transitions
- Why this pattern/structure matters]

### Key Elements

**[Category 1]:**
- Element 1: Description
- Element 2: Description

**[Category 2]:**
- Element A: Description
- Element B: Description

[Include entry/exit points, major components, transitions, timing, etc.]

### Related Documentation
- [Link to related doc 1](../path/to/doc1.md)
- [Link to related doc 2](../path/to/doc2.md)
```

### Accessibility Best Practices

- **Alt text**: Answer "What is this diagram?" in one sentence
- **Long description**: Answer "How does it work?" in narrative form
- **Key elements**: Answer "What are the parts?" in structured list
- **Avoid visual-only language**: Don't say "the blue box" without also naming it
- **Use directional language carefully**: "Left to right" may not be meaningful; use "first to last" or "input to output"
- **Explain symbols and colors**: Define what visual conventions mean (e.g., "dashed lines indicate optional transitions")

### Feedback and Contributions

If you identify accessibility gaps or need additional description detail:
- Open an issue with tag `accessibility` and `documentation`
- Suggest specific improvements to descriptions
- Request descriptions for new diagrams

Maintained by the Diagrammer agent team. Contact via repository issues.

---

_Document version: 1.1.0_  
_Last updated: 2026-02-14_  
_Format: Accessibility metadata for architecture diagrams_
