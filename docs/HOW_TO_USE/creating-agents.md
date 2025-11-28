# Creating Agents with AgentBase Template

**Version:** 1.0.0  
**Last Updated:** 2025-11-23  
**Audience:** Developers creating new agents for file-based orchestration

## Overview

This guide shows you how to create new agents using the `AgentBase` template, which provides standardized lifecycle hooks, status management, error handling, and work log creation for the file-based orchestration framework.

**Benefits of using AgentBase:**
- Reduces agent creation effort by >50%
- Enforces consistent status transitions (assigned → in_progress → done/error)
- Automatic timing metrics capture
- Built-in work log generation (Directive 014 compliant)
- Artifact validation
- Error handling with proper error blocks
- Agent handoff helpers

## Quick Start

### 1. Create Your Agent File

```python
#!/usr/bin/env python3
"""
My Custom Agent - Brief description
"""

from pathlib import Path
from typing import Any, Dict

from agent_base import AgentBase, timing_decorator


class MyAgent(AgentBase):
    """Agent that does something useful."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_name="my-agent", **kwargs)
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate task requirements."""
        # Check required fields
        if "required_field" not in task.get("context", {}):
            raise ValueError("Missing required_field")
        return True
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent-specific logic."""
        # Do your work here
        self.artifacts_created.append("path/to/artifact.md")
        
        return {
            "summary": "Task completed successfully",
            "artifacts": self.artifacts_created,
        }


if __name__ == "__main__":
    agent = MyAgent(work_dir="work")
    agent.run()
```

### 2. Create Agent Directory

```bash
mkdir -p work/collaboration/assigned/my-agent
mkdir -p work/reports/logs/my-agent
```

### 3. Test Your Agent

```bash
# Create test task
cat > work/collaboration/assigned/my-agent/2025-11-23T1500-my-agent-test.yaml << EOF
id: 2025-11-23T1500-my-agent-test
agent: my-agent
status: assigned
title: Test task
artefacts:
  - output/test.md
context:
  required_field: "test value"
created_at: 2025-11-23T15:00:00Z
created_by: developer
EOF

# Run agent
python ops/scripts/my_agent.py
```

## AgentBase Lifecycle

AgentBase manages a standardized lifecycle for all tasks:

```
┌─────────────────┐
│  Find Tasks     │  find_assigned_tasks()
│  (status=       │  
│   assigned)     │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Update Status  │  update_task_status("in_progress")
│  to in_progress │  Adds started_at timestamp
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Validate Task  │  validate_task(task)
│  (abstract)     │  → Implemented by you
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Initialize     │  init_task(task)
│  (optional)     │  → Override if needed
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Execute Task   │  execute_task(task)
│  (abstract)     │  → Implemented by you
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Create Result  │  create_result_block()
│  Block          │  Adds completed_at
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Update Status  │  update_task_status("done")
│  to done        │  Adds result block
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Move to Done   │  move_to_done()
│  Directory      │  Moves YAML file
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Finalize       │  finalize_task(success=True)
│  (optional)     │  → Override for cleanup/logging
└─────────────────┘
```

**On Error:** Status updates to "error", error block added, task stays in assigned/ directory.

## Implementing Required Methods

### 1. validate_task(task) - Required

Validates that the task is suitable for your agent.

**Purpose:**
- Check required context fields are present
- Verify input files exist
- Validate task configuration
- Fail fast before execution

**Example:**

```python
def validate_task(self, task: Dict[str, Any]) -> bool:
    """Validate task has required fields and files."""
    context = task.get("context", {})
    
    # Check required fields
    required_fields = ["input_path", "output_path", "mode"]
    for field in required_fields:
        if field not in context:
            raise ValueError(f"Task context missing '{field}' field")
    
    # Validate input file exists
    input_path = Path(context["input_path"])
    if not input_path.exists():
        raise ValueError(f"Input file not found: {input_path}")
    
    # Validate mode is supported
    valid_modes = ["summary", "detailed", "analysis"]
    if context["mode"] not in valid_modes:
        raise ValueError(f"Mode must be one of: {valid_modes}")
    
    self._log("✅ Task validation passed")
    return True
```

**Best Practices:**
- Raise `ValueError` with clear message when validation fails
- Don't modify state—just validate
- Check both presence and validity of fields
- Verify file paths exist for inputs (not outputs)

### 2. execute_task(task) - Required

Implements your agent-specific logic.

**Purpose:**
- Perform the actual work
- Create/modify artifacts
- Track created artifacts in `self.artifacts_created`
- Return result summary

**Example:**

```python
@timing_decorator  # Optional: adds timing metrics
def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the agent work."""
    context = task.get("context", {})
    
    # Read inputs
    input_path = Path(context["input_path"])
    output_path = Path(context["output_path"])
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Do the work
    self._log(f"Processing {input_path}...")
    result_data = self._process_file(input_path)
    
    # Write outputs
    with open(output_path, "w") as f:
        f.write(result_data)
    
    self._log(f"Created {output_path}")
    self.artifacts_created.append(str(output_path))
    
    # Validate artifacts were created
    existing, missing = self.validate_artifacts(self.artifacts_created)
    if missing:
        raise RuntimeError(f"Failed to create: {missing}")
    
    # Return result
    return {
        "summary": f"Processed {input_path.name} → {output_path.name}",
        "artifacts": self.artifacts_created,
        # Optional: chain to next agent
        # "next_agent": "writer-editor",
        # "next_task_title": "Polish output",
        # "next_artifacts": self.artifacts_created,
        # "next_task_notes": ["Focus on clarity"],
    }
```

**Best Practices:**
- Use `self._log()` to log progress
- Add artifacts to `self.artifacts_created` list
- Use `Path` objects for file operations
- Create parent directories before writing files
- Validate artifacts were actually created
- Return clear, concise summary

**Return Dictionary Keys:**
- `summary` (required): Brief description of work
- `artifacts` (optional): Defaults to `self.artifacts_created`
- `next_agent` (optional): Agent name for handoff
- `next_task_title` (optional): Title for follow-up task
- `next_artifacts` (optional): Artifacts for follow-up
- `next_task_notes` (optional): Notes for next agent

## Optional Lifecycle Hooks

### 3. init_task(task) - Optional

Called after validation, before execution.

**Use Cases:**
- Pre-load data for validation
- Set up temporary resources
- Initialize agent-specific state
- Parse complex configurations

**Example:**

```python
def init_task(self, task: Dict[str, Any]) -> None:
    """Initialize task-specific state."""
    context = task.get("context", {})
    
    # Pre-load configuration
    config_file = Path(context.get("config_file", "config.yaml"))
    with open(config_file) as f:
        self.config = yaml.safe_load(f)
    
    # Set up temporary directory
    self.temp_dir = Path(f"/tmp/agent-{self.agent_name}-{task['id']}")
    self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    self._log(f"Initialized with config: {self.config}")
```

### 4. finalize_task(success) - Optional

Called after task completion (success or failure).

**Use Cases:**
- Clean up temporary resources
- Create work logs
- Log metrics
- Send notifications

**Example:**

```python
def finalize_task(self, success: bool) -> None:
    """Clean up and log results."""
    if success:
        # Create work log (required for orchestrated tasks)
        self.create_work_log(
            title="Task Execution Report",
            context=f"Processed task {self.current_task['id']}",
            approach="Used XYZ algorithm to process inputs",
            execution_steps=[
                "Validated inputs",
                "Processed data",
                "Generated outputs",
            ],
            outcomes=f"Created {len(self.artifacts_created)} artifacts",
            lessons_learned="Process completed efficiently",
        )
    
    # Clean up temp directory
    if hasattr(self, 'temp_dir') and self.temp_dir.exists():
        shutil.rmtree(self.temp_dir)
        self._log(f"Cleaned up temp dir: {self.temp_dir}")
```

## Error Handling

AgentBase automatically catches exceptions and creates error blocks.

**Automatic Error Handling:**
- Exceptions in any lifecycle method are caught
- Status updates to "error"
- Error block added with message and stacktrace
- Task stays in assigned/ directory for review
- `finalize_task(success=False)` is called

**Custom Error Handling:**

```python
def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
    """Execute with custom error handling."""
    try:
        result = self._risky_operation()
    except SpecificError as exc:
        # Add context to error
        raise RuntimeError(f"Operation failed: {exc}") from exc
    
    return {"summary": "Success"}
```

**Error Strategies:**
- Let exceptions bubble up for automatic handling
- Add context with `raise ... from exc`
- Use `ValueError` for validation errors
- Use `RuntimeError` for execution errors
- Don't catch and suppress errors silently

## Agent Handoffs

Chain multiple agents together with `next_agent` in result block.

**Example Workflow:**

```python
# Architect creates ADR
def execute_task(self, task):
    # Create ADR document
    adr_path = "docs/adrs/ADR-010.md"
    self._create_adr(adr_path)
    self.artifacts_created.append(adr_path)
    
    return {
        "summary": "Created ADR-010",
        "artifacts": [adr_path],
        "next_agent": "writer-editor",
        "next_task_title": "Polish ADR-010 for clarity",
        "next_artifacts": [adr_path],
        "next_task_notes": [
            "Check technical jargon",
            "Add examples if needed",
        ],
    }
```

The orchestrator automatically creates:

```yaml
id: 2025-11-23T1545-writer-editor-adr-polish
agent: writer-editor
status: new
title: "Polish ADR-010 for clarity"
artefacts:
  - docs/adrs/ADR-010.md
context:
  notes:
    - "Check technical jargon"
    - "Add examples if needed"
  dependencies:
    - 2025-11-23T1530-architect-adr-creation
```

## Work Log Creation

Work logs are **required** for orchestrated tasks (Directive 014).

**Automatic Creation in finalize_task:**

```python
def finalize_task(self, success: bool) -> None:
    """Create work log after successful completion."""
    if success:
        self.create_work_log(
            title="Brief title for work log",
            context="What prompted this work",
            approach="Explanation of approach taken",
            execution_steps=[
                "Step 1 description",
                "Step 2 description",
                "Step 3 description",
            ],
            outcomes="Results achieved",
            lessons_learned="Reflections and improvements",
            directives_used={
                "general_guidelines": True,
                "operational_guidelines": True,
                "specific_directives": ["001", "014"],
                "agent_profile": self.agent_name,
                "reasoning_mode": self.mode,
            },
        )
```

**Work Log Location:** `work/reports/logs/<agent-name>/YYYY-MM-DDTHHMM-<agent>-<slug>.md`

## Testing Your Agent

### 1. Unit Testing

```python
# test_my_agent.py
import unittest
from pathlib import Path
from my_agent import MyAgent


class TestMyAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MyAgent(work_dir="work")
    
    def test_validate_task_success(self):
        task = {
            "id": "test-task",
            "context": {"required_field": "value"},
        }
        self.assertTrue(self.agent.validate_task(task))
    
    def test_validate_task_missing_field(self):
        task = {"id": "test-task", "context": {}}
        with self.assertRaises(ValueError):
            self.agent.validate_task(task)
    
    def test_execute_task(self):
        task = {
            "id": "test-task",
            "context": {
                "required_field": "value",
                "input_path": "test.txt",
            },
        }
        # Create test input
        Path("test.txt").write_text("test data")
        
        result = self.agent.execute_task(task)
        self.assertIn("summary", result)
        
        # Clean up
        Path("test.txt").unlink()


if __name__ == "__main__":
    unittest.main()
```

### 2. Integration Testing

```bash
# Create test task
cat > work/assigned/my-agent/test-task.yaml << EOF
id: test-task
agent: my-agent
status: assigned
title: Test task
context:
  required_field: "test value"
created_at: 2025-11-23T15:00:00Z
created_by: developer
EOF

# Run agent
python ops/scripts/my_agent.py

# Check results
cat work/collaboration/done/my-agent/test-task.yaml
cat work/reports/logs/my-agent/*.md
```

### 3. Continuous Mode Testing

```bash
# Start agent in continuous mode
python ops/scripts/my_agent.py --continuous &

# Add tasks
cp test-task.yaml work/collaboration/assigned/my-agent/

# Watch logs
tail -f work/collaboration/WORKFLOW_LOG.md

# Stop agent
pkill -f my_agent.py
```

## Best Practices

### Agent Design

1. **Single Responsibility:** One agent, one domain
2. **Clear Boundaries:** Define what your agent does and doesn't do
3. **Minimal State:** Avoid persistent state between tasks
4. **Idempotent:** Agent should be safe to retry

### Task Processing

1. **Fail Fast:** Validate early in lifecycle
2. **Log Progress:** Use `self._log()` liberally
3. **Track Artifacts:** Add all outputs to `self.artifacts_created`
4. **Validate Outputs:** Check artifacts actually exist
5. **Clear Summaries:** Write concise, informative result summaries

### Error Handling

1. **Don't Swallow Errors:** Let exceptions bubble up
2. **Add Context:** Wrap exceptions with useful info
3. **Use Specific Errors:** ValueError for validation, RuntimeError for execution
4. **Include Details:** Stacktraces are automatically captured

### Work Logs

1. **Always Create:** Required for orchestrated tasks
2. **Be Detailed:** Future you will thank you
3. **Note Challenges:** Document problems and solutions
4. **Actionable Lessons:** Write insights that improve the framework

## Integration with Orchestrator

The orchestrator (`ops/scripts/orchestration/agent_orchestrator.py`) handles:
- Moving tasks from inbox to assigned/
- Creating follow-up tasks from `next_agent`
- Monitoring for timeouts
- Updating agent status dashboard
- Archiving old completed tasks

**Your agent must:**
- Poll `work/collaboration/assigned/<agent-name>/` directory
- Process tasks with `status: assigned`
- Update status to `in_progress` when starting
- Update status to `done` and move to `work/collaboration/done/` on success
- Update status to `error` and stay in assigned/ on failure

**AgentBase handles all of this automatically.**

## Running Modes

### One-Shot Mode

Process a single task and exit:

```python
if __name__ == "__main__":
    agent = MyAgent(work_dir="work")
    agent.run(continuous=False)  # Default
```

```bash
python my_agent.py
```

### Continuous Mode

Keep polling for tasks:

```python
if __name__ == "__main__":
    import sys
    continuous = "--continuous" in sys.argv
    agent = MyAgent(work_dir="work")
    agent.run(continuous=continuous)
```

```bash
python my_agent.py --continuous
```

### CI/CD Integration

```yaml
# .github/workflows/agent-runner.yml
name: My Agent Runner

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:

jobs:
  run-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Agent
        run: python ops/scripts/my_agent.py
      - name: Commit Results
        run: |
          git config user.name "agent-bot"
          git add work/
          git commit -m "Agent work" || true
          git push
```

## Advanced Features

### Custom Timing Metrics

```python
from agent_base import timing_decorator

class MyAgent(AgentBase):
    @timing_decorator
    def _complex_operation(self):
        # Timing automatically logged
        pass
```

### Artifact Validation

```python
def execute_task(self, task):
    # Create artifacts
    self.artifacts_created.extend([
        "output/file1.md",
        "output/file2.json",
    ])
    
    # Validate all exist
    existing, missing = self.validate_artifacts(self.artifacts_created)
    if missing:
        raise RuntimeError(f"Failed to create: {missing}")
    
    return {"summary": "Done"}
```

### Custom Modes

```python
agent = MyAgent(
    work_dir="work",
    mode="/creative-mode",  # or /analysis-mode, /meta-mode
    log_level="DEBUG",
)
```

### Multiple Agent Instances

```python
# Run multiple specialized agents from one script
agents = [
    MyAgent(agent_name="my-agent-fast", mode="/analysis-mode"),
    MyAgent(agent_name="my-agent-slow", mode="/creative-mode"),
]

for agent in agents:
    agent.process_next_task()
```

## Troubleshooting

### "No tasks assigned"

**Problem:** Agent can't find tasks.

**Solutions:**
- Check directory: `ls work/collaboration/assigned/<agent-name>/`
- Verify task status is "assigned"
- Check agent name matches directory
- Run orchestrator to assign tasks: `python ops/scripts/orchestration/agent_orchestrator.py`

### "Task validation failed"

**Problem:** Task doesn't meet requirements.

**Solutions:**
- Check error message for specific field
- Verify task context has required fields
- Check file paths exist
- Review task YAML format

### "Failed to create artifact"

**Problem:** Output file wasn't created.

**Solutions:**
- Check file permissions
- Verify parent directory exists (use `mkdir parents=True`)
- Check disk space
- Review error stacktrace

### Agent crashes without error block

**Problem:** Agent dies before updating status.

**Solutions:**
- Check system logs: `journalctl -u my-agent`
- Run in foreground for debugging
- Add try/except in `main()`
- Check resource limits (memory, disk)

## Example: Complete Agent Implementation

See `ops/scripts/orchestration/example_agent.py` for a complete working example that:
- Validates task requirements
- Loads YAML data
- Generates markdown report
- Handles errors gracefully
- Creates work logs
- Demonstrates all lifecycle hooks

Run it:

```bash
# Create test data
cat > /tmp/test-data.yaml << EOF
title: Test Report
data:
  value1: 100
  value2: 200
items:
  - name: Item 1
  - name: Item 2
EOF

# Create task
cat > work/collaboration/assigned/example/test-task.yaml << EOF
id: test-task
agent: example
status: assigned
title: Test markdown generation
artefacts:
  - /tmp/test-report.md
context:
  input_file: /tmp/test-data.yaml
  output_file: /tmp/test-report.md
  report_title: "My Test Report"
created_at: 2025-11-23T15:00:00Z
created_by: developer
EOF

# Run
python ops/scripts/orchestration/example_agent.py

# Check results
cat /tmp/test-report.md
cat work/reports/logs/example/*.md
```

## References

- **AgentBase Source:** `ops/scripts/orchestration/agent_base.py`
- **Example Agent:** `ops/scripts/orchestration/example_agent.py`
- **Task Utils:** `ops/scripts/orchestration/task_utils.py` - Common task file operations
- **Task Schema:** `docs/templates/agent-tasks/task-descriptor.yaml`
- **File-Based Orchestration:** `.github/agents/approaches/file-based-orchestration.md`
- **Directive 014:** `.github/agents/directives/014_worklog_creation.md`
- **Multi-Agent Guide:** `docs/HOW_TO_USE/multi-agent-orchestration.md`

## Support

For questions or issues:
1. Review this guide and example implementation
2. Check work logs for similar tasks
3. Review orchestrator logs: `work/collaboration/WORKFLOW_LOG.md`
4. Create an issue with: agent name, task YAML, error message, work log

---

_Document Version: 1.0.0_  
_Last Updated: 2025-11-23_  
_Maintained by: DevOps Danny (Build Automation Specialist)_
