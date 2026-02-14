# Architecture Diagrams

This directory contains PlantUML diagrams that visualize the asynchronous multi-agent orchestration system.

## Diagrams

### task-lifecycle-state-machine.puml

**Purpose:** State machine diagram showing all possible task states and transitions.

**States:**
- `new`: Task created, awaiting assignment
- `assigned`: Task assigned to agent
- `in_progress`: Agent actively working
- `done`: Task completed successfully
- `error`: Task failed, requires intervention
- `archived`: Task moved to long-term storage

**Transitions:**
- Normal flow: new → assigned → in_progress → done → archived
- Error flow: in_progress → error → (assigned or archived)
- Follow-up flow: done → new (via next_agent)

**Annotations:**
- Each state shows its directory location
- Each transition shows who triggers it and how
- Notes explain timeout policies and requirements

**Use Cases:**
- Understanding task lifecycle
- Debugging stuck tasks
- Planning error recovery strategies

### orchestration-workflow.puml

**Purpose:** Sequence diagram showing the complete workflow from task creation to archival.

**Actors:**
- Human (stakeholder)
- Planning Agent (task creation)
- Coordinator Agent (orchestration)
- Structural Agent (domain work)
- Lexical Agent (domain work)

**Key Flows:**
1. Task Creation: Human → Planning → inbox
2. Task Assignment: Coordinator → assigned directories
3. Task Execution: Agents process and complete tasks
4. Workflow Sequencing: Coordinator creates follow-up tasks based on `next_agent`
5. Archival: Old tasks moved to archive

**Use Cases:**
- Understanding end-to-end flow
- Explaining system to new contributors
- Identifying bottlenecks or failure points

### workflow-sequential-flow.puml

**Purpose:** Sequence diagram illustrating agent handoff pattern with sequential execution.

**Pattern:** Agent A completes → Coordinator creates follow-up → Agent B executes

**Example Flow:**
- Structural Agent generates REPO_MAP.md
- Specifies `next_agent: lexical` in result block
- Coordinator automatically creates follow-up task for Lexical Agent
- Lexical Agent refines REPO_MAP.md

**Use Cases:**
- Understanding multi-step workflows
- Designing agent handoff patterns
- Explaining chained task execution

### workflow-parallel-flow.puml

**Purpose:** Sequence diagram showing multiple agents working simultaneously on independent tasks.

**Pattern:** Multiple independent tasks assigned at once, executed in parallel

**Example Flow:**
- Planning Agent creates 3 independent tasks
- Coordinator assigns to Structural, Architect, and Diagrammer agents
- All three agents work simultaneously
- Total time = longest task (not sum of all tasks)

**Use Cases:**
- Maximizing throughput
- Understanding parallel execution benefits
- Designing batch processing workflows

### workflow-convergent-flow.puml

**Purpose:** Sequence diagram demonstrating multiple agents contributing to a synthesis task.

**Pattern:** Multiple agents complete independently → All handoff to single synthesis agent

**Example Flow:**
- Structural, Lexical, and Architect agents work in parallel
- Each completes with `next_agent: curator`
- Coordinator creates single curator task with all artifacts
- Curator validates consistency across all outputs

**Use Cases:**
- Designing validation workflows
- Implementing cross-agent consistency checks
- Understanding convergent patterns

### orchestration-phases-timeline.puml

**Purpose:** Gantt chart showing implementation phases, dependencies, and timeline.

**Phases:**
1. **Phase 1: Core Infrastructure** (2-3 days, CRITICAL)
2. **Phase 2: Coordinator Implementation** (3-4 days, CRITICAL)
3. **Phase 3: Agent Integration** (5-7 days, HIGH)
4. **Phase 4: GitHub Actions** (2-3 days, MEDIUM, Optional)
5. **Phase 5: Validation & Monitoring** (2-3 days, MEDIUM, Optional)

**Critical Path:** Phase 1 → Phase 2 → Phase 3 (10-14 workdays)

**Use Cases:**
- Planning implementation work
- Understanding phase dependencies
- Tracking progress against timeline

### domain-core-c4-container.puml

**Purpose:** C4 Level 2 container diagram showing the four bounded contexts within the domain/core architectural layer.

**Containers:**
- Collaboration: Task lifecycle, repository pattern, query operations
- Doctrine: Immutable governance models, parsers, validators
- Specifications: Feature status tracking (emerging context)
- Common: Shared utilities with no domain semantics

**Use Cases:**
- Understanding domain layer architecture
- Visualizing bounded context boundaries and dependencies
- Onboarding new contributors to the domain module

### domain-collaboration-classes.puml

**Purpose:** Simplified UML class diagram for the Collaboration bounded context.

**Key Classes:**
- TaskStatus: State machine enum with transition validation (7 states)
- TaskMode, TaskPriority: Operating mode and priority enums
- TaskRepository: Repository pattern for task data access
- TaskQueryResult: Chainable query result container

**Use Cases:**
- Understanding task domain model structure
- Reviewing collaboration context API surface
- Planning extensions to the task model

### domain-doctrine-classes.puml

**Purpose:** Simplified UML class diagram for the Doctrine bounded context.

**Key Classes:**
- Agent, Directive, Tactic, Approach, StyleGuide, Template: Frozen domain models
- HandoffPattern, PrimerEntry: Value objects composed into Agent
- DirectiveParser, AgentParser, TacticParser, ApproachParser: Markdown parsers
- CrossReferenceValidator, MetadataValidator, IntegrityChecker: Validators

**Use Cases:**
- Understanding doctrine domain model relationships
- Reviewing parser and validator architecture
- Planning new doctrine artifact types

### domain-specifications-classes.puml

**Purpose:** Simplified UML class diagram for the Specifications bounded context.

**Key Classes:**
- FeatureStatus: Feature lifecycle enum (DRAFT through DEPRECATED)

**Use Cases:**
- Understanding the emerging specifications context
- Planning future specification domain models

### domain-common-classes.puml

**Purpose:** Simplified UML class diagram for Common utilities.

**Key Elements:**
- path_utils module: Repository-aware path resolution functions

**Use Cases:**
- Understanding shared infrastructure available to all contexts
- Verifying no domain logic has leaked into common

## Rendering Diagrams

### Online

Use [PlantUML Web Server](http://www.plantuml.com/plantuml/uml/):

1. Copy diagram source code
2. Paste into web interface
3. View rendered diagram

### Local (requires PlantUML)

```bash
# Install PlantUML
apt-get install plantuml

# Or with Java
java -jar plantuml.jar diagram.puml

# Render all diagrams in directory
plantuml docs/architecture/diagrams/*.puml
```

This generates PNG/SVG files alongside the .puml sources.

### IDE Integration

**VS Code:**
- Install "PlantUML" extension
- Open .puml file
- Press `Alt+D` to preview

**IntelliJ IDEA:**
- Install "PlantUML integration" plugin
- Right-click .puml file
- Select "Preview"

## Adding New Diagrams

1. Create `<name>.puml` file in this directory
2. Use PlantUML syntax (see [documentation](https://plantuml.com/))
3. Add entry to this README explaining purpose and use cases
4. Commit both .puml source and rendered image (optional)

## Diagram Conventions

**Colors:**
- Blue (#E1F5FF): Input/Inbox states
- Yellow (#FFF9E1): Assigned/Active states
- Green (#E8F5E9): Completed states
- Gray (#F5F5F5): Archived states
- Red (#FFCDD2): Error states

**Naming:**
- Use kebab-case: `task-lifecycle-state-machine.puml`
- Be descriptive: `orchestration-workflow.puml` not `workflow.puml`
- Include diagram type in name: `-state-machine`, `-sequence`, `-component`

**Documentation:**
- Add title to diagram: `title Asynchronous Multi-Agent Orchestration`
- Use notes to explain key concepts
- Annotate non-obvious transitions
- Include legends when using custom colors

## Related Documentation

- [Async Multi-Agent Orchestration Architecture](../async_multiagent_orchestration.md)
- [ADR-003: Task Lifecycle and State Management](../ADR-003-task-lifecycle-state-management.md)
- [ADR-005: Coordinator Agent Pattern](../ADR-005-coordinator-agent-pattern.md)
- [Technical Design](../async_orchestration_technical_design.md)

---

_Maintained by: Architect agents_  
_Last updated: 2026-02-14_
