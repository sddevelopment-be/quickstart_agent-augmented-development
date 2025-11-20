# Architecture Diagrams

This directory contains PlantUML diagrams that visualize the asynchronous multi-agent orchestration system.

## Diagrams

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
_Last updated: 2025-11-20_
