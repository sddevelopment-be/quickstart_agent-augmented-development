# ADR-024: CLI Integration for Swarm Mode Agent Orchestration

**status**: `Proposed`  
**date**: 2026-01-31  
**supersedes**: None  
**related**: ADR-008 (File-Based Async Coordination), ADR-005 (Coordinator Agent Pattern), ADR-020 (Multi-Tier Agentic Runtime)

## Context

### Problem Statement

The current file-based orchestration system (ADR-008, ADR-005) requires manual task creation and monitoring. While this provides excellent transparency and control, it creates bottlenecks for workflows that involve predictable multi-agent sequences. For example:

**Current Workflow (Manual):**
1. Human creates task YAML in `work/collaboration/inbox/`
2. Coordinator assigns task to Agent A
3. Agent A completes work, creates result with `next_agent: B`
4. Coordinator creates follow-up task for Agent B
5. Agent B completes work, may specify `next_agent: C`
6. **Repeat for each step...**

This pattern works well for exploratory or ad-hoc tasks but becomes inefficient for:

- **Recurring workflows**: "Execute analysis → generate diagrams → write documentation → validate consistency"
- **Batch operations**: "Process 5 architectural patterns using the same agent sequence"
- **Complex chains**: "Architect → Diagrammer → Writer-Editor → Curator → Lexical (5-agent chain)"

### Forces at Play

**Automation Needs:**
- Reduce manual prompting overhead for predictable workflows
- Enable "one command, full chain" execution for known patterns
- Support reusable workflow definitions

**Safety Requirements:**
- Maintain human oversight and intervention capability
- Preserve complete audit trail of automated decisions
- Ensure security boundaries for automated agent execution
- Prevent runaway or uncontrolled agent chains

**Integration Constraints:**
- Must work with existing file-based orchestration (ADR-008)
- Should support multiple CLI tools (claude-code, cursor, codex, copilot, etc.)
- Must maintain cross-platform compatibility (Linux, macOS, Windows)
- Cannot introduce infrastructure dependencies (no running services)

**Traceability:**
- All automated actions must be auditable
- Workflow progress must be visible at any point
- Human must be able to pause/resume/cancel chains
- Logs must explain why each agent was invoked

### Current State

**Existing Infrastructure:**
- File-based task coordination (ADR-008)
- Coordinator agent for task routing (ADR-005)
- YAML task descriptors with lifecycle management (ADR-003)
- Work logs and metrics capture (ADR-009, Directive 014)
- Agent profiles with specialization boundaries (Directive 005)

**Gap:**
No mechanism to pre-define and execute multi-step workflows as atomic operations. Each step requires either human intervention or Coordinator polling cycles (5-minute delays).

### Stakeholders

**Primary Personas:**
- **Jordan (Lead Developer)**: Needs efficient automation for recurring patterns
- **Alex (Systems Architect)**: Requires safety guarantees and auditability
- **Casey (Junior Developer)**: Must understand and use swarm mode without deep knowledge of orchestration internals

## Decision

**We will implement a hybrid CLI approach combining declarative YAML workflow definitions with a Python CLI executor that integrates with existing file-based orchestration.**

### Core Components

#### 1. Workflow Definition Format (YAML)

Declarative workflow files stored in `work/workflows/` define agent sequences:

```yaml
# work/workflows/architecture-pattern-documentation.yaml
workflow:
  id: "architecture-pattern-documentation"
  name: "Document Architecture Pattern"
  description: "Full chain: design → diagram → document → validate"
  version: "1.0.0"
  
  parameters:
    - name: "pattern_name"
      type: "string"
      required: true
      description: "Name of the architecture pattern"
    - name: "pattern_file"
      type: "path"
      required: true
      description: "Path to pattern description file"
  
  agents:
    - agent: "architect"
      task_template: "analyze-pattern"
      input_mapping:
        pattern_file: "{{pattern_file}}"
      output_artifacts:
        - "docs/architecture/patterns/{{pattern_name}}-analysis.md"
      timeout_minutes: 30
      
    - agent: "diagrammer"
      task_template: "create-pattern-diagrams"
      depends_on: "architect"
      input_mapping:
        analysis_file: "{{architect.output_artifacts[0]}}"
      output_artifacts:
        - "docs/architecture/diagrams/{{pattern_name}}-*.puml"
      timeout_minutes: 20
      
    - agent: "writer-editor"
      task_template: "polish-pattern-doc"
      depends_on: "diagrammer"
      input_mapping:
        source_files: "{{architect.output_artifacts + diagrammer.output_artifacts}}"
      output_artifacts:
        - "docs/architecture/patterns/{{pattern_name}}.md"
      timeout_minutes: 15
      
    - agent: "curator"
      task_template: "validate-pattern-doc"
      depends_on: "writer-editor"
      input_mapping:
        document: "{{writer-editor.output_artifacts[0]}}"
      output_artifacts:
        - "docs/architecture/patterns/{{pattern_name}}.md"  # updated
      timeout_minutes: 10
  
  validation:
    pre_execution:
      - check: "file_exists"
        path: "{{pattern_file}}"
        error: "Pattern file not found"
      - check: "agent_available"
        agents: ["architect", "diagrammer", "writer-editor", "curator"]
    
    post_execution:
      - check: "artifacts_created"
        artifacts: "all"
      - check: "work_logs_complete"
        agents: "all"
  
  recovery:
    on_agent_failure:
      action: "pause"  # Options: pause | skip | retry | abort
      notify: true
    
    on_timeout:
      action: "pause"
      notify: true
  
  metadata:
    author: "architect"
    created: "2026-01-31T04:00:00Z"
    tags: ["architecture", "documentation", "pattern"]
    risk_level: "low"  # low | medium | high
```

#### 2. CLI Executor (Python)

Command-line tool for workflow execution:

```bash
# Execute a workflow
swarm run architecture-pattern-documentation \
  --param pattern_name=circuit-breaker \
  --param pattern_file=docs/architecture/patterns/circuit-breaker-draft.md \
  --mode interactive  # Options: interactive | batch | dry-run

# List available workflows
swarm list

# Validate a workflow definition
swarm validate work/workflows/my-workflow.yaml

# Show workflow status
swarm status workflow-run-abc123

# Pause/resume a running workflow
swarm pause workflow-run-abc123
swarm resume workflow-run-abc123

# Show execution history
swarm history --limit 10
```

**Execution Model:**

1. **Parse workflow YAML** and validate against schema
2. **Run pre-execution validation** (files exist, agents available, etc.)
3. **Create root task** in orchestration system with `workflow_id` metadata
4. **Monitor task lifecycle** via file-based coordination:
   - Poll `work/collaboration/assigned/<agent>/` for task status
   - Detect completion via move to `work/collaboration/done/<agent>/`
   - Extract `result` block and validate outputs
5. **Create follow-up tasks** based on `depends_on` chain
6. **Handle failures** according to recovery policy
7. **Generate workflow report** summarizing execution

#### 3. Integration Points

**With File-Based Orchestration:**
- Workflow executor creates standard YAML task descriptors
- Tasks include `workflow_id` and `workflow_step` metadata
- Coordinator and agents operate normally (no changes required)
- Work logs capture workflow context automatically

**With CLI Tools:**
- Executor invokes `claude-code`, `cursor`, `copilot` based on agent profile
- Tool selection configurable per agent via `agent-tool-mapping.yaml`
- Standard prompt templates in `.github/agents/prompts/<agent>/`
- Tool output captured and validated before marking step complete

**Example agent-tool mapping:**
```yaml
# work/config/agent-tool-mapping.yaml
agents:
  architect:
    preferred_tool: "claude-code"
    fallback_tools: ["cursor", "copilot"]
    model: "claude-opus-4-20250514"
    
  diagrammer:
    preferred_tool: "cursor"
    fallback_tools: ["claude-code"]
    model: "claude-sonnet-4-20250514"
```

#### 4. Safety & Security Protocols

**Human Oversight:**
- Interactive mode (default): Requires confirmation before each agent step
- Batch mode: Runs autonomously but sends notifications at checkpoints
- Dry-run mode: Shows planned execution without running agents
- Emergency pause: `Ctrl+C` or `swarm pause <id>` stops execution gracefully

**Audit Trail:**
- All workflow executions logged to `work/reports/workflows/<workflow-run-id>/`
- Execution manifest records parameters, timing, and decisions
- Work logs from each agent linked in manifest
- Git commits tagged with `workflow:<workflow-id>` for traceability

**Security Boundaries:**
- Workflows cannot execute arbitrary commands (only invoke registered agents)
- File system access restricted to workspace directory
- Network access controlled via tool configuration
- Resource limits: max agents per workflow (10), max execution time (4 hours)

**Validation Gates:**
- Pre-execution: Check workflow syntax, agent availability, input files
- Inter-step: Validate previous agent output before proceeding
- Post-execution: Verify all artifacts created, work logs complete
- Schema validation: All YAML validated against JSON Schema

### Implementation Phases

**Phase 1: Foundation (Weeks 1-2)**
- Define workflow YAML schema (JSON Schema for validation)
- Implement basic CLI (list, validate, dry-run)
- Create workflow parser and validator
- Add workflow metadata to task descriptors

**Phase 2: Core Execution (Weeks 3-4)**
- Implement workflow executor (run command)
- Integrate with file-based orchestration
- Add interactive mode with confirmation prompts
- Implement basic error handling and logging

**Phase 3: Tool Integration (Weeks 5-6)**
- Implement agent-tool mapping and selection
- Add CLI tool invocation (claude-code, cursor, copilot)
- Capture and validate tool outputs
- Handle tool failures and fallbacks

**Phase 4: Advanced Features (Weeks 7-8)**
- Add batch mode and scheduling
- Implement pause/resume functionality
- Add workflow history and reporting
- Performance optimization and testing

**Phase 5: Documentation & Hardening (Week 9)**
- User guide for workflow creation
- Security review and hardening
- Integration testing with real workflows
- Migration guide for existing manual workflows

## Rationale

### Why Hybrid YAML + Python CLI?

**Declarative YAML:**
- **Pros**: Human-readable, version-controlled, reusable, easy to validate
- **Cons**: Limited logic capabilities, requires executor to interpret
- **Why chosen**: Aligns with existing file-based orchestration philosophy, promotes transparency

**Python CLI Executor:**
- **Pros**: Rich ecosystem, cross-platform, easy debugging, integrates with existing orchestration scripts
- **Cons**: Requires Python runtime, additional tooling to maintain
- **Why chosen**: Repository already uses Python for orchestration (agent_orchestrator.py), minimal additional dependency

**Alternative: Shell Scripts**
- **Rejected**: Limited error handling, poor cross-platform support, harder to test, no structured data handling

**Alternative: Pure Python Workflows**
- **Rejected**: Less transparent (code vs. declarative), harder for non-developers to author, opaque execution model

**Alternative: GitHub Actions Workflows**
- **Rejected**: Requires network/GitHub, not suitable for local development, verbose syntax, limited local debugging

### Why Interactive Mode Default?

**Safety-first approach**: Automated agent chains pose risks (runaway execution, resource exhaustion, incorrect outputs). Interactive mode provides:
- **Checkpoint review**: Human validates each agent output before next step
- **Early intervention**: Can stop chain if outputs deviate from expectations
- **Learning opportunity**: Users understand workflow progression
- **Trust building**: Gradual confidence in automation before enabling batch mode

**Trade-off**: Slower execution vs. safety. This is acceptable for initial adoption.

### Why Workflow-Specific YAML Files?

**Reusability**: Common patterns (analyze → diagram → document) become reusable workflows  
**Versioning**: Workflows evolve independently from orchestration system  
**Sharing**: Workflows can be shared across projects or teams  
**Validation**: Schema validation catches errors before execution  
**Documentation**: Workflow file serves as documentation of the pattern

**Alternative: Inline Task Chains**
- **Rejected**: No reusability, verbose task creation, harder to validate

**Alternative: Programmatic Workflow API**
- **Rejected**: Higher barrier to entry, opaque to non-developers, harder to review

### Why File-Based Integration?

**Consistency**: Workflows use the same task coordination as manual operations  
**Transparency**: All workflow tasks visible in `work/collaboration/` directories  
**Compatibility**: No changes required to existing agents or Coordinator  
**Auditability**: Git commits provide full workflow execution history  
**Recoverability**: Can manually intervene or resume workflows at any step

**Alternative: In-Memory Coordination**
- **Rejected**: Lost on crash, not auditable, opaque to humans

**Alternative: Database-Backed Workflows**
- **Rejected**: Adds infrastructure dependency, not Git-native

### Trade-Off Analysis

| Dimension | Manual (Current) | Shell Scripts | GitHub Actions | Hybrid YAML+CLI (Proposed) |
|-----------|-----------------|---------------|----------------|---------------------------|
| **Automation** | Low (manual each step) | High (scripted) | High (event-driven) | Medium-High (declarative) |
| **Transparency** | Excellent (all visible) | Poor (opaque scripts) | Medium (workflow logs) | Excellent (YAML + file-based) |
| **Safety** | Excellent (human each step) | Poor (no checkpoints) | Medium (manual approval gates) | Good (interactive mode) |
| **Reusability** | Low (repeat manually) | Medium (copy scripts) | High (workflow templates) | High (YAML library) |
| **Local Support** | Excellent (all local) | Excellent (local) | Poor (requires GitHub) | Excellent (local CLI) |
| **Learning Curve** | Low (simple tasks) | Medium (shell knowledge) | High (Actions syntax) | Medium (YAML + CLI) |
| **Auditability** | Excellent (Git commits) | Poor (log files) | Good (Actions history) | Excellent (Git + manifests) |
| **Error Recovery** | Excellent (manual fix) | Poor (restart script) | Medium (rerun workflow) | Good (pause/resume) |
| **Cross-Platform** | Excellent (file ops) | Poor (shell differences) | N/A (cloud only) | Good (Python cross-platform) |
| **Maintenance** | Low (no automation) | High (brittle scripts) | Medium (YAML maintenance) | Medium (CLI + workflows) |

**Decision Matrix Summary:**
- Hybrid approach scores highest on transparency, safety, and auditability
- Acceptable trade-offs in learning curve and maintenance
- Best alignment with existing file-based orchestration philosophy

## Envisioned Consequences

### Positive Outcomes

✅ **Efficiency Gains:**
- Multi-agent workflows execute in single command
- Predictable patterns become reusable workflows
- Reduces manual overhead by 60-80% for recurring tasks

✅ **Improved Developer Experience:**
- Lower barrier to multi-agent coordination
- Clear workflow definitions serve as documentation
- Interactive mode builds confidence in automation

✅ **Enhanced Traceability:**
- Complete audit trail of automated decisions
- Workflow manifests link all related work logs and artifacts
- Git history shows workflow evolution

✅ **Maintainability:**
- Declarative YAML easier to review and update than scripts
- Schema validation catches errors early
- Workflows version-controlled alongside code

✅ **Safety & Control:**
- Interactive mode prevents runaway execution
- Human can pause/resume/cancel at any point
- Validation gates ensure quality standards

✅ **Extensibility:**
- Easy to add new workflows (just create YAML file)
- Tool-agnostic design supports multiple CLI tools
- Can integrate with external orchestration systems later

✅ **Consistency:**
- All workflow tasks follow same lifecycle as manual tasks
- Agents unaware they're in a workflow (no special cases)
- Coordinator operates normally (no changes required)

### Negative Consequences

⚠️ **Increased Complexity:**
- New CLI tool to learn and maintain
- Workflow YAML syntax adds cognitive load
- Additional failure modes (workflow executor, tool integration)

⚠️ **Initial Setup Overhead:**
- Converting manual workflows to YAML definitions takes time
- Agent-tool mapping configuration required
- Prompt templates need standardization

⚠️ **Execution Latency:**
- Interactive mode adds confirmation delays
- File-based coordination introduces polling delays (5-min cycles)
- No sub-minute responsiveness (acceptable for our use case)

⚠️ **Tooling Dependencies:**
- Requires Python runtime (3.9+)
- Requires CLI tools installed (claude-code, cursor, etc.)
- Cross-platform testing needed for Windows support

⚠️ **Debugging Challenges:**
- Multi-step workflows harder to debug than single tasks
- Error attribution across agent chain can be ambiguous
- Workflow failures require understanding of multiple agent outputs

### Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| **Runaway automation** | High (resource exhaustion) | Low (interactive mode default) | Max agents/time limits, pause mechanism, batch mode gated |
| **Workflow definition errors** | Medium (failed execution) | Medium (YAML complexity) | Schema validation, dry-run mode, clear error messages |
| **Tool integration failures** | Medium (workflow blocked) | Medium (external dependencies) | Fallback tools, graceful degradation, clear error context |
| **Executor crashes** | Medium (workflow interrupted) | Low (Python stability) | State persistence, resume capability, manual recovery |
| **Security boundary violations** | High (unauthorized access) | Low (restricted execution) | Sandboxed execution, file system limits, audit logging |
| **Loss of transparency** | High (opaque decisions) | Low (file-based integration) | Workflow manifests, linked work logs, Git commits |
| **Over-automation** | Medium (loss of learning) | Medium (batch mode adoption) | Interactive mode default, documentation, training |
| **Workflow maintenance burden** | Medium (stale definitions) | Medium (evolution) | Versioned workflows, validation checks, periodic review |

### Success Metrics

**Adoption:**
- 5+ workflows defined in first month
- 50%+ of recurring multi-agent tasks converted to workflows
- <5 user-reported workflow definition errors

**Efficiency:**
- 60%+ reduction in manual prompting time for workflow-based tasks
- Average workflow execution time <2 hours (vs. 4-6 hours manual)
- <10% workflow failure rate (recoverable errors)

**Quality:**
- 100% workflow executions have complete audit trail
- 0 security boundary violations
- Work log quality maintained (ADR-009 metrics compliance)

**Safety:**
- 0 runaway executions (exceeding resource limits)
- 100% of critical workflows use interactive mode
- <1 minute average pause/resume response time

### Validation Criteria

This ADR succeeds if, after 3 months:

1. ✅ **Workflows used regularly**: ≥5 unique workflows executed weekly
2. ✅ **Safety maintained**: 0 security incidents, 0 runaway executions
3. ✅ **Transparency preserved**: 100% audit trail coverage, manual intervention possible at all checkpoints
4. ✅ **Efficiency gained**: ≥50% time savings on workflow-eligible tasks vs. manual
5. ✅ **Quality upheld**: Workflow-generated artifacts meet same standards as manual (ADR-009 metrics)

## Considered Alternatives

### 1. Pure Shell Script Orchestration

**Approach:**
- Bash/PowerShell scripts invoke CLI tools sequentially
- Scripts stored in `ops/scripts/workflows/`
- Environment variables pass data between steps

**Pros:**
- Simple to implement
- No additional dependencies
- Direct control over execution

**Cons:**
- Poor cross-platform support (bash vs. PowerShell)
- Limited error handling and recovery
- Not human-readable (opaque execution logic)
- No structured validation
- Brittle (hard-coded paths, poor abstraction)

**Rejection Reason:** Violates transparency and maintainability principles. Inconsistent with file-based orchestration philosophy.

### 2. Python-Only Workflow Definition

**Approach:**
- Workflows defined as Python classes/functions
- Uses programmatic API for task creation
- Example: `workflow.add_step(ArchitectAgent, inputs=...)`

**Pros:**
- Full programming language power (loops, conditionals, functions)
- Type checking and IDE support
- Easy to test

**Cons:**
- Higher barrier to entry (requires Python knowledge)
- Less transparent (code vs. declarative config)
- Harder to review (must read code to understand workflow)
- Version control diffs less readable

**Rejection Reason:** Reduces accessibility for non-developers. Code-heavy approach conflicts with transparency goals.

### 3. GitHub Actions Workflow Engine

**Approach:**
- Define workflows as `.github/workflows/agent-workflow-*.yml`
- Use GitHub Actions for orchestration
- Trigger via `workflow_dispatch` or API

**Pros:**
- Mature workflow engine with rich features
- Built-in notification and monitoring
- Native GitHub integration

**Cons:**
- Requires network connectivity (no offline support)
- Not suitable for local development workflows
- Verbose syntax for our use case
- Difficult to debug locally
- Ties orchestration to GitHub (vendor lock-in)

**Rejection Reason:** Violates local-first principle. Not all workflows should require cloud infrastructure.

### 4. LangChain/LlamaIndex Agent Frameworks

**Approach:**
- Use heavy agent framework for orchestration
- Define workflows using framework DSL
- Framework handles agent coordination

**Pros:**
- Rich feature set (memory, planning, tools)
- Active ecosystem and community
- Many pre-built patterns

**Cons:**
- Heavy dependency (large codebase)
- Opaque execution model (framework internals complex)
- Poor alignment with file-based orchestration
- Over-engineered for our use case
- Reduces transparency (black-box coordination)

**Rejection Reason:** Architectural misalignment. Introduces complexity that conflicts with file-based transparency. See ADR-020 for similar rationale.

### 5. Message Queue-Based Coordination (RabbitMQ/Redis)

**Approach:**
- Deploy message queue for agent coordination
- Workflows publish messages to queue
- Agents consume from queues and publish results

**Pros:**
- Real-time coordination (no polling delays)
- Mature patterns (pub-sub, work queues)
- Scalable to high throughput

**Cons:**
- Requires infrastructure (running service)
- Operational overhead (monitoring, backups)
- Not Git-native (state outside version control)
- Violates zero-infrastructure principle (ADR-008)
- Loses transparency (hidden queue state)

**Rejection Reason:** Over-engineered. Contradicts file-based, zero-infrastructure foundation of existing orchestration.

### 6. YAML Workflows with CLI Polling (Selected)

**Why This Wins:**
- Best balance of automation, transparency, and safety
- Minimal architectural disruption (extends existing patterns)
- Maintains human oversight capability
- Declarative + executable hybrid provides best UX
- Cross-platform with manageable complexity
- Aligns with file-based orchestration philosophy

## Implementation Considerations

### Workflow Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["workflow"],
  "properties": {
    "workflow": {
      "type": "object",
      "required": ["id", "name", "agents"],
      "properties": {
        "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
        "parameters": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "type", "required"],
            "properties": {
              "name": {"type": "string"},
              "type": {"enum": ["string", "path", "integer", "boolean"]},
              "required": {"type": "boolean"},
              "description": {"type": "string"},
              "default": {}
            }
          }
        },
        "agents": {
          "type": "array",
          "minItems": 1,
          "maxItems": 10,
          "items": {
            "type": "object",
            "required": ["agent", "task_template"],
            "properties": {
              "agent": {"type": "string"},
              "task_template": {"type": "string"},
              "depends_on": {"type": "string"},
              "input_mapping": {"type": "object"},
              "output_artifacts": {
                "type": "array",
                "items": {"type": "string"}
              },
              "timeout_minutes": {"type": "integer", "minimum": 5, "maximum": 240}
            }
          }
        },
        "validation": {
          "type": "object",
          "properties": {
            "pre_execution": {"type": "array"},
            "post_execution": {"type": "array"}
          }
        },
        "recovery": {
          "type": "object",
          "properties": {
            "on_agent_failure": {
              "type": "object",
              "properties": {
                "action": {"enum": ["pause", "skip", "retry", "abort"]},
                "notify": {"type": "boolean"}
              }
            },
            "on_timeout": {
              "type": "object",
              "properties": {
                "action": {"enum": ["pause", "skip", "retry", "abort"]},
                "notify": {"type": "boolean"}
              }
            }
          }
        },
        "metadata": {
          "type": "object",
          "properties": {
            "author": {"type": "string"},
            "created": {"type": "string", "format": "date-time"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "risk_level": {"enum": ["low", "medium", "high"]}
          }
        }
      }
    }
  }
}
```

### CLI Tool Structure

```
ops/scripts/swarm/
├── swarm.py                 # Main CLI entry point
├── executor.py              # Workflow execution engine
├── parser.py                # YAML workflow parser
├── validator.py             # Schema and pre-flight validation
├── coordinator.py           # File-based orchestration integration
├── tools/
│   ├── base.py             # Abstract tool interface
│   ├── claude_code.py      # Claude Code CLI integration
│   ├── cursor.py           # Cursor CLI integration
│   └── copilot.py          # GitHub Copilot CLI integration
├── reporters/
│   ├── manifest.py         # Workflow execution manifest generator
│   └── summary.py          # Human-readable execution report
└── templates/
    └── workflow-template.yaml  # Starter template for new workflows
```

### Directory Structure

```
work/
├── workflows/              # Workflow definitions (YAML)
│   ├── architecture-pattern-documentation.yaml
│   ├── feature-end-to-end.yaml
│   └── documentation-refresh.yaml
├── config/
│   ├── agent-tool-mapping.yaml  # Agent → CLI tool mapping
│   └── swarm-config.yaml        # Global swarm configuration
└── reports/
    └── workflows/          # Workflow execution reports
        └── workflow-run-20260131T0830-abc123/
            ├── manifest.yaml           # Execution metadata
            ├── execution-log.txt       # Real-time execution log
            └── summary.md              # Human-readable summary
```

### Agent-Tool Mapping

```yaml
# work/config/agent-tool-mapping.yaml
version: "1.0.0"

default:
  tool: "claude-code"
  model: "claude-opus-4-20250514"
  timeout_minutes: 30

agents:
  architect:
    tool: "claude-code"
    model: "claude-opus-4-20250514"
    prompt_template: ".github/agents/prompts/architect/default.md"
    
  diagrammer:
    tool: "cursor"
    model: "claude-sonnet-4-20250514"
    prompt_template: ".github/agents/prompts/diagrammer/default.md"
    
  writer-editor:
    tool: "claude-code"
    model: "claude-opus-4-20250514"
    prompt_template: ".github/agents/prompts/writer-editor/default.md"
    
  curator:
    tool: "copilot"
    model: "gpt-4.5-turbo"
    prompt_template: ".github/agents/prompts/curator/default.md"

fallback:
  enabled: true
  order: ["claude-code", "cursor", "copilot"]
  on_failure: "pause"  # Options: pause | skip | abort
```

### Security Configuration

```yaml
# work/config/swarm-config.yaml
version: "1.0.0"

security:
  max_agents_per_workflow: 10
  max_execution_time_minutes: 240  # 4 hours
  max_concurrent_workflows: 3
  
  filesystem:
    allowed_paths:
      - "docs/"
      - "work/"
      - ".github/agents/"
    denied_paths:
      - ".git/"
      - ".env"
      - "ops/scripts/swarm/"  # Prevent workflow self-modification
  
  network:
    enabled: false  # No network access for local workflows
    
execution:
  default_mode: "interactive"  # Options: interactive | batch | dry-run
  polling_interval_seconds: 30  # Check task status every 30s
  checkpoint_notification: true
  
logging:
  level: "INFO"  # DEBUG | INFO | WARNING | ERROR
  console: true
  file: "work/reports/workflows/swarm.log"
  include_tool_output: true
  
notifications:
  enabled: false  # Future: Slack/email notifications
```

### Prompt Template Example

```markdown
<!-- .github/agents/prompts/architect/default.md -->
# Architect Agent: {{task_title}}

You are Architect Alphonso executing as part of workflow: **{{workflow_name}}** (Step {{workflow_step}}/{{workflow_total_steps}})

## Task Context

{{task_context}}

## Input Artifacts

{{#each input_artifacts}}
- `{{this.path}}` - {{this.description}}
{{/each}}

## Expected Outputs

{{#each output_artifacts}}
- `{{this}}` - {{@key}}
{{/each}}

## Workflow Chain

This task is part of a larger workflow:
{{workflow_description}}

**Previous step:** {{previous_agent}} completed at {{previous_completion_time}}
**Next step:** {{next_agent}} will receive {{output_artifacts[0]}}

## Instructions

1. Load the task using file-based collaboration approach (Step 3: Process Tasks)
2. Execute architectural analysis as specified
3. Create artifacts following ADR and pattern documentation standards
4. Complete the task following directive 019
5. Your work will automatically trigger the next agent in the workflow

**Important:** This is an automated workflow execution. Maintain high quality standards as your output will be consumed by {{next_agent}} without human review in between steps.
```

## Integration with Existing ADRs

### ADR-008 (File-Based Async Coordination)

**Integration:** Swarm mode workflows create standard task YAML files, maintaining full compatibility with file-based orchestration.

**Enhancement:** Adds `workflow_id`, `workflow_step`, and `workflow_total_steps` metadata to task descriptors for traceability.

**No Breaking Changes:** Coordinator and agents continue to operate normally, unaware of workflow context.

### ADR-005 (Coordinator Agent Pattern)

**Integration:** Coordinator continues to assign tasks and monitor completion. Swarm executor acts as task creator, not replacement for Coordinator.

**Enhancement:** Workflow executor can optionally bypass Coordinator polling delays by directly monitoring task status for workflow-created tasks.

**Compatibility:** Both manual task creation and workflow-driven creation coexist.

### ADR-003 (Task Lifecycle State Management)

**Integration:** All workflow tasks follow standard lifecycle: new → assigned → in_progress → done

**Enhancement:** Workflow manifest links all tasks in chain for end-to-end traceability.

**Consistency:** Workflow failures don't violate lifecycle rules; tasks still move to `error` state normally.

### ADR-009 (Orchestration Metrics Standard)

**Integration:** All workflow tasks include metrics blocks (duration, tokens, artifacts)

**Enhancement:** Workflow manifest aggregates metrics across entire chain (total duration, total tokens, artifact lineage)

**Quality:** Maintains ADR-009 validation criteria for individual tasks plus workflow-level aggregation.

### ADR-020 (Multi-Tier Agentic Runtime)

**Integration:** Swarm CLI operates at Layer 1 (Orchestration & Governance), invoking Layer 3 tools (claude-code, cursor, copilot)

**Alignment:** Maintains separation of concerns: orchestration (swarm) vs. execution (CLI tools) vs. models (LLM APIs)

**Flexibility:** Agent-tool mapping allows switching Layer 3 tools without changing workflows.

## References

**Related ADRs:**
- [ADR-008: File-Based Asynchronous Agent Coordination](ADR-008-file-based-async-coordination.md)
- [ADR-003: Task Lifecycle and State Management](ADR-003-task-lifecycle-state-management.md)
- [ADR-005: Coordinator Agent Pattern](ADR-005-coordinator-agent-pattern.md)
- [ADR-009: Orchestration Metrics Standard](ADR-009-orchestration-metrics-standard.md)
- [ADR-020: Multi-Tier Agentic Runtime Architecture](ADR-020-multi-tier-agentic-runtime.md)

**Implementation References:**
- `ops/scripts/orchestration/agent_orchestrator.py` - Existing coordinator implementation
- `.github/agents/approaches/file_based_collaboration/` - Task processing patterns
- `work/collaboration/` - Task coordination directory structure

**Directives:**
- [Directive 014: Work Log Creation](.github/agents/directives/014_worklog_creation.md)
- [Directive 019: File-Based Collaboration](.github/agents/directives/019_file_based_collaboration.md)

---

**Maintained by:** Architect Alphonso  
**Next Review:** After first 3 workflows implemented (estimated 2026-02-28)  
**Version:** 1.0.0
