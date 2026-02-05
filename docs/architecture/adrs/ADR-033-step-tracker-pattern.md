# ADR-033: Step Tracker Pattern for Complex Operations

**status**: Accepted  
**date**: 2026-02-05  
**author**: Architect Alphonso  
**approved-by**: Human-in-Charge

## Context

Multi-step operations in `llm-service` currently provide no progress indication, leaving users uncertain about operation status:

**Current State Problems:**

1. **No Progress Visibility**
   - Complex operations (telemetry setup, migrations, multi-stage processing) appear frozen
   - Users cannot tell if operation is progressing or hung
   - No indication of which step is currently executing

2. **Poor Error Context**
   - When operation fails, unclear which step caused the failure
   - No visibility into which steps completed successfully before failure
   - Difficult to resume or debug failed operations

3. **Inconsistent User Experience**
   - Some operations show progress, others don't
   - No standard pattern for multi-step feedback
   - Each developer implements progress differently (or not at all)

**Example Current Behavior:**
```bash
$ llm-service setup telemetry

Setting up telemetry...
# ... 2 minutes pass with no feedback ...
Done.

# What happened? Which steps completed?
# Was it fast or slow? Did anything fail?
```

**Comparative Analysis Finding:**

The [spec-kitty comparative analysis](../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md) showed consistent progress indication patterns:

- Step-by-step feedback for complex workflows
- Clear indication of current step
- Visual progress indicators
- Error context showing which step failed

**User Feedback:**
- Human-in-Charge rated step tracker pattern as ⭐⭐⭐⭐ priority
- Target: "Clear progress indication, better error context"

## Decision

**We will implement a reusable `StepTracker` pattern (context manager) that provides consistent progress tracking for multi-step operations.**

### Core Design

**Implementation Pattern:**
```python
from llm_service.utils import StepTracker

def setup_telemetry():
    """Multi-step operation with progress tracking."""
    
    with StepTracker("Setting up telemetry") as tracker:
        
        tracker.step("Installing dependencies")
        install_dependencies()
        tracker.complete()  # Mark step as done
        
        tracker.step("Configuring environment")
        configure_environment()
        tracker.complete()
        
        tracker.step("Running validation")
        run_validation()
        tracker.complete()
    
    # All steps completed successfully
```

**Visual Output (with Rich integration):**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Setting up telemetry                 ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ [1/3] Installing dependencies  ✅    │
│ [2/3] Configuring environment  ⏳    │
│ [3/3] Running validation       ⏸️     │
└──────────────────────────────────────┘
```

**Features:**

1. **Context Manager Pattern**
   - Automatic setup and cleanup
   - Error handling with step context
   - Resource management

2. **Step Registration**
   - Define steps upfront or dynamically
   - Track step completion
   - Measure step duration

3. **Visual Feedback**
   - Integration with Rich library (ADR-030)
   - Progress indicators (✅ ✗ ⏳ ⏸️)
   - Real-time updates

4. **Dashboard Integration**
   - Emit events for each step (ADR-032)
   - Dashboard shows step progress
   - Historical step analytics

5. **Error Context Preservation**
   - Which step failed
   - Which steps completed before failure
   - Step-specific error messages

## Rationale

### Why Context Manager Pattern?

**Strengths:**

1. **Pythonic & Familiar**
   - Standard Python pattern (`with` statement)
   - Clear resource lifetime
   - Automatic cleanup

2. **Explicit Scope**
   - Progress tracking starts/ends clearly
   - Steps are scoped to tracker lifetime
   - No global state pollution

3. **Exception Safety**
   - `__exit__` runs even on exceptions
   - Can capture which step failed
   - Clean up resources automatically

4. **Composable**
   - Trackers can be nested
   - Subtasks can have their own trackers
   - Parent/child relationships possible

5. **Testable**
   - Easy to mock in tests
   - Can capture step execution for assertions
   - Clear test fixtures

**Trade-offs Accepted:**

1. **Slight Verbosity**
   - Must call `tracker.step()` and `tracker.complete()`
   - *Mitigation*: Clear and explicit is better than implicit
   - *Impact*: Low - improves code readability

2. **Indentation Level**
   - `with` block adds one indentation level
   - *Mitigation*: Python convention, widely accepted
   - *Impact*: None - standard pattern

### Why NOT Alternatives?

**Alternative 1: Decorator Pattern**

**Description:** `@tracked_steps` decorator to wrap functions.

```python
@tracked_steps
def setup_telemetry():
    step("Installing dependencies")
    install_dependencies()
    # ...
```

**Pros:**
- ✅ Less indentation
- ✅ Less boilerplate

**Cons:**
- ❌ Implicit step tracking (magic)
- ❌ Harder to test (decorator behavior)
- ❌ Less flexible (can't conditionally track)
- ❌ Unclear step boundaries

**Rejected Because:** Too implicit. Context manager makes tracking explicit and clear.

**Alternative 2: Manual Progress Calls**

**Description:** Direct calls to progress functions.

```python
def setup_telemetry():
    start_progress("Setting up telemetry", steps=3)
    
    update_progress(1, "Installing dependencies")
    install_dependencies()
    
    update_progress(2, "Configuring environment")
    configure_environment()
    
    end_progress()
```

**Pros:**
- ✅ Simple implementation
- ✅ No special patterns

**Cons:**
- ❌ No automatic cleanup (forget `end_progress()`)
- ❌ Error handling manual
- ❌ Global state required
- ❌ Easy to make mistakes (forget updates)

**Rejected Because:** Error-prone and no automatic resource management.

**Alternative 3: Progress Bar Library Only**

**Description:** Use `rich.Progress` directly everywhere.

```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Setup", total=3)
    
    install_dependencies()
    progress.update(task, advance=1)
    
    configure_environment()
    progress.update(task, advance=1)
```

**Pros:**
- ✅ Battle-tested library
- ✅ Good visual feedback

**Cons:**
- ❌ No step names (just numbers)
- ❌ No error context (which step failed?)
- ❌ No dashboard integration
- ❌ Not semantically meaningful

**Rejected Because:** Insufficient abstraction. Need step semantics, not just progress bar.

### Design Principles

1. **Explicit Over Implicit**
   - Steps are clearly defined in code
   - Progress tracking is visible
   - No hidden magic

2. **Fail-Fast with Context**
   - Errors include step information
   - Easy to identify failure point
   - Aids debugging

3. **Composable & Reusable**
   - Works for any multi-step operation
   - Can nest trackers for subtasks
   - Standard pattern across codebase

4. **Rich Integration**
   - Leverages Rich library for visual feedback (ADR-030)
   - Consistent UI with rest of CLI
   - Dashboard-aware (ADR-032)

## Envisioned Consequences

### Positive Consequences

1. ✅ **Clear Progress Indication**
   - Users know exactly what's happening
   - Can see which step is executing
   - Reduces anxiety during long operations

2. ✅ **Better Error Context**
   - Errors indicate which step failed
   - Can see which steps completed before failure
   - Easier debugging and issue reporting

3. ✅ **Consistent User Experience**
   - All multi-step operations use same pattern
   - Predictable progress feedback
   - Professional appearance

4. ✅ **Improved Testability**
   - Can assert step execution in tests
   - Mock step execution for unit tests
   - Test error handling per step

5. ✅ **Dashboard Integration**
   - Step progress visible in dashboard
   - Historical step metrics
   - Operation analytics

6. ✅ **Developer Productivity**
   - Reusable pattern reduces boilerplate
   - Clear guidelines for progress tracking
   - Standard abstraction for complex operations

### Negative Consequences

1. ⚠️ **Slight Code Verbosity**
   - Must explicitly call `tracker.step()` and `tracker.complete()`
   - *Mitigation*: Clarity is worth verbosity
   - *Impact*: Low - improved readability outweighs cost

2. ⚠️ **Learning Curve for Contributors**
   - New pattern to learn
   - *Mitigation*: Simple API, clear documentation
   - *Impact*: Low - pattern is intuitive

3. ⚠️ **Potential Overuse**
   - Risk of tracking every trivial operation
   - *Mitigation*: Guidelines for when to use tracker
   - *Impact*: Low - code reviews enforce guidelines

### Risk Mitigation Strategies

**Overuse Prevention:**
```python
# Guidelines (enforced in code review):
# ✅ DO use StepTracker for:
#   - Operations with ≥3 steps
#   - Operations taking >5 seconds
#   - Setup/teardown workflows
#   - Migration scripts

# ❌ DON'T use StepTracker for:
#   - Single operations
#   - Quick (<2 second) operations
#   - Internal helper functions
```

**Error Handling:**
```python
# StepTracker captures which step failed
with StepTracker("Operation") as tracker:
    tracker.step("Step 1")
    operation_1()  # If this fails...
    tracker.complete()
    
    tracker.step("Step 2")
    operation_2()
    tracker.complete()

# Error includes: "Failed at step 1/3: Step 1"
# User knows exactly where failure occurred
```

## Implementation Guidance

### Phase 1: Core Implementation (2 hours)

**1. StepTracker Class:**
```python
# src/llm_service/utils/step_tracker.py

from typing import Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

@dataclass
class Step:
    """Represents a single step in an operation."""
    name: str
    index: int
    status: str = "pending"  # pending, running, complete, error
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error: Optional[str] = None
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate step duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    @property
    def status_icon(self) -> str:
        """Get visual icon for step status."""
        return {
            "pending": "⏸️",
            "running": "⏳",
            "complete": "✅",
            "error": "❌"
        }.get(self.status, "❓")


class StepTracker:
    """
    Context manager for tracking multi-step operations.
    
    Usage:
        with StepTracker("Operation Name") as tracker:
            tracker.step("Step 1")
            do_step_1()
            tracker.complete()
            
            tracker.step("Step 2")
            do_step_2()
            tracker.complete()
    """
    
    def __init__(
        self,
        operation_name: str,
        console: Optional[Console] = None,
        emit_events: bool = True
    ):
        self.operation_name = operation_name
        self.console = console or Console()
        self.emit_events = emit_events
        
        self.steps: List[Step] = []
        self.current_step: Optional[Step] = None
        self.start_time: datetime = None
        self.end_time: datetime = None
    
    def __enter__(self):
        """Enter context - start tracking."""
        self.start_time = datetime.utcnow()
        
        # Display header
        self.console.print(Panel.fit(
            f"[bold cyan]{self.operation_name}[/bold cyan]",
            border_style="blue"
        ))
        
        # Emit event
        if self.emit_events:
            from llm_service.events import event_bus, EventType
            event_bus.emit(EventType.OPERATION_START, {
                "operation": self.operation_name,
                "timestamp": self.start_time.isoformat()
            })
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - complete tracking."""
        self.end_time = datetime.utcnow()
        
        # Mark current step as error if exception
        if exc_type is not None and self.current_step:
            self.current_step.status = "error"
            self.current_step.error = str(exc_val)
            self.current_step.end_time = datetime.utcnow()
        
        # Display summary
        self._display_summary(exc_type is not None)
        
        # Emit event
        if self.emit_events:
            from llm_service.events import event_bus, EventType
            event_bus.emit(EventType.OPERATION_COMPLETE, {
                "operation": self.operation_name,
                "success": exc_type is None,
                "steps": len(self.steps),
                "duration": (self.end_time - self.start_time).total_seconds(),
                "error": str(exc_val) if exc_type else None
            })
        
        # Don't suppress exception
        return False
    
    def step(self, name: str):
        """Start a new step."""
        # Complete previous step if not explicitly completed
        if self.current_step and self.current_step.status == "running":
            self.complete()
        
        # Create new step
        step = Step(
            name=name,
            index=len(self.steps) + 1,
            status="running",
            start_time=datetime.utcnow()
        )
        self.steps.append(step)
        self.current_step = step
        
        # Display progress
        self._display_progress()
        
        # Emit event
        if self.emit_events:
            from llm_service.events import event_bus, EventType
            event_bus.emit(EventType.STEP_START, {
                "operation": self.operation_name,
                "step": name,
                "step_index": step.index,
                "total_steps": len(self.steps)
            })
    
    def complete(self):
        """Mark current step as complete."""
        if self.current_step:
            self.current_step.status = "complete"
            self.current_step.end_time = datetime.utcnow()
            
            # Display updated progress
            self._display_progress()
            
            # Emit event
            if self.emit_events:
                from llm_service.events import event_bus, EventType
                event_bus.emit(EventType.STEP_COMPLETE, {
                    "operation": self.operation_name,
                    "step": self.current_step.name,
                    "duration": self.current_step.duration
                })
    
    def _display_progress(self):
        """Display current progress."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Step", style="cyan")
        table.add_column("Status", justify="right")
        
        for step in self.steps:
            step_text = f"[{step.index}/{len(self.steps)}] {step.name}"
            table.add_row(step_text, step.status_icon)
        
        self.console.print(table)
    
    def _display_summary(self, had_error: bool):
        """Display operation summary."""
        duration = (self.end_time - self.start_time).total_seconds()
        
        completed_steps = sum(1 for s in self.steps if s.status == "complete")
        total_steps = len(self.steps)
        
        if had_error:
            failed_step = next((s for s in self.steps if s.status == "error"), None)
            self.console.print(Panel(
                f"[red]Operation failed at step {failed_step.index}/{total_steps}:[/red] {failed_step.name}\n"
                f"[yellow]Completed {completed_steps}/{total_steps} steps[/yellow]\n"
                f"Duration: {duration:.2f}s",
                title="❌ Operation Failed",
                border_style="red"
            ))
        else:
            self.console.print(Panel(
                f"[green]All {total_steps} steps completed successfully[/green]\n"
                f"Duration: {duration:.2f}s",
                title="✅ Operation Complete",
                border_style="green"
            ))
```

### Phase 2: Integration Examples (1 hour)

**Example 1: Telemetry Setup**
```python
# src/llm_service/commands/telemetry.py

def setup_telemetry():
    """Set up telemetry with progress tracking."""
    
    with StepTracker("Setting up telemetry") as tracker:
        
        tracker.step("Installing dependencies")
        subprocess.run(["pip", "install", "opentelemetry-api"], check=True)
        tracker.complete()
        
        tracker.step("Configuring environment")
        setup_environment_variables()
        tracker.complete()
        
        tracker.step("Running validation")
        validate_telemetry_config()
        tracker.complete()
        
        tracker.step("Starting telemetry service")
        start_telemetry_service()
        tracker.complete()
```

**Example 2: Configuration Migration**
```python
# src/llm_service/commands/migrate.py

def migrate_config(old_version: str, new_version: str):
    """Migrate configuration with progress tracking."""
    
    with StepTracker(f"Migrating config {old_version} → {new_version}") as tracker:
        
        tracker.step("Backing up existing configuration")
        backup_path = backup_config()
        tracker.complete()
        
        tracker.step("Validating old configuration")
        validate_config(old_version)
        tracker.complete()
        
        tracker.step("Transforming configuration schema")
        transform_config(old_version, new_version)
        tracker.complete()
        
        tracker.step("Validating new configuration")
        validate_config(new_version)
        tracker.complete()
        
        tracker.step("Writing updated configuration")
        write_config()
        tracker.complete()
```

**Example 3: Batch Processing**
```python
# src/llm_service/commands/batch.py

def process_batch(files: List[Path]):
    """Process multiple files with progress tracking."""
    
    with StepTracker(f"Processing {len(files)} files") as tracker:
        
        for i, file in enumerate(files, 1):
            tracker.step(f"Processing {file.name} ({i}/{len(files)})")
            
            try:
                process_file(file)
                tracker.complete()
            except Exception as e:
                # Step will be marked as error
                # Tracker will show which file failed
                raise ProcessingError(f"Failed to process {file.name}") from e
```

### Phase 3: Dashboard Integration (30 minutes)

**Event Types:**
```python
# src/llm_service/events/types.py

class EventType(str, Enum):
    # ... existing events ...
    
    # Step tracking events
    OPERATION_START = "operation.start"
    OPERATION_COMPLETE = "operation.complete"
    STEP_START = "step.start"
    STEP_COMPLETE = "step.complete"
    STEP_ERROR = "step.error"
```

**Dashboard Display:**
```javascript
// Dashboard shows step progress

function handleStepStart(data) {
    // Show step in progress panel
    updateOperationSteps(data.operation, data.step, data.step_index, data.total_steps);
}

function handleStepComplete(data) {
    // Mark step as complete
    markStepComplete(data.operation, data.step);
}
```

### Testing Strategy

**Unit Tests:**
```python
def test_step_tracker_basic_flow():
    """Test basic step tracker flow."""
    console = Console(file=StringIO())
    
    with StepTracker("Test Operation", console=console, emit_events=False) as tracker:
        tracker.step("Step 1")
        tracker.complete()
        
        tracker.step("Step 2")
        tracker.complete()
    
    assert len(tracker.steps) == 2
    assert all(s.status == "complete" for s in tracker.steps)

def test_step_tracker_error_handling():
    """Test step tracker error handling."""
    console = Console(file=StringIO())
    
    try:
        with StepTracker("Test Operation", console=console, emit_events=False) as tracker:
            tracker.step("Step 1")
            tracker.complete()
            
            tracker.step("Step 2")
            raise ValueError("Simulated error")
    except ValueError:
        pass
    
    # Step 2 should be marked as error
    assert tracker.steps[1].status == "error"
    assert "Simulated error" in tracker.steps[1].error

def test_step_tracker_event_emission():
    """Test that tracker emits events."""
    from llm_service.events import event_bus
    
    events_received = []
    
    def capture_event(event):
        events_received.append(event)
    
    event_bus.subscribe("operation.start", capture_event)
    event_bus.subscribe("step.start", capture_event)
    event_bus.subscribe("step.complete", capture_event)
    event_bus.subscribe("operation.complete", capture_event)
    
    with StepTracker("Test") as tracker:
        tracker.step("Step 1")
        tracker.complete()
    
    assert len(events_received) == 4
    assert events_received[0].type == "operation.start"
    assert events_received[1].type == "step.start"
    assert events_received[2].type == "step.complete"
    assert events_received[3].type == "operation.complete"
```

**Integration Tests:**
```python
def test_step_tracker_in_real_operation():
    """Test step tracker in actual operation."""
    result = runner.invoke(setup_telemetry)
    
    assert result.exit_code == 0
    assert "Installing dependencies" in result.output
    assert "✅" in result.output
    assert "Operation Complete" in result.output
```

## Usage Examples

### Example 1: Setup Operation

```bash
$ llm-service setup telemetry

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Setting up telemetry             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

[1/4] Installing dependencies      ✅
[2/4] Configuring environment      ✅
[3/4] Running validation           ✅
[4/4] Starting telemetry service   ⏳

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ✅ Operation Complete            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ All 4 steps completed            │
│ Duration: 8.3s                   │
└──────────────────────────────────┘
```

### Example 2: Error During Operation

```bash
$ llm-service migrate config --from v1 --to v2

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Migrating config v1 → v2         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

[1/5] Backing up configuration     ✅
[2/5] Validating old config        ✅
[3/5] Transforming schema          ❌

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ❌ Operation Failed              ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Failed at step 3/5:              │
│ Transforming schema              │
│                                  │
│ Completed 2/5 steps              │
│ Duration: 2.1s                   │
│                                  │
│ Error: Invalid field 'model_id'  │
│ in configuration schema          │
└──────────────────────────────────┘

# User knows:
#  - Exactly which step failed (step 3)
#  - What the error was
#  - That steps 1-2 completed successfully
#  - Backup was created (can rollback)
```

### Example 3: Batch Processing

```bash
$ llm-service batch process files/*.txt

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Processing 12 files              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

[1/12] Processing file1.txt        ✅
[2/12] Processing file2.txt        ✅
[3/12] Processing file3.txt        ✅
[4/12] Processing file4.txt        ⏳
...
```

## Considered Alternatives

### Alternative 1: Decorator Pattern
**Rejected:** Too implicit; unclear step boundaries.

### Alternative 2: Manual Progress Calls
**Rejected:** Error-prone; no automatic cleanup.

### Alternative 3: Progress Bar Library Only
**Rejected:** Lacks step semantics and error context.

(See Rationale section for detailed analysis)

## References

**Related ADRs:**
- [ADR-030: Rich Terminal UI](ADR-030-rich-terminal-ui-cli-feedback.md) - Visual feedback
- [ADR-032: Real-Time Dashboard](ADR-032-real-time-execution-dashboard.md) - Dashboard integration

**Related Documents:**
- [spec-kitty Comparative Analysis](../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md)
- [spec-kitty Inspired Enhancements](../design/spec-kitty-inspired-enhancements.md)

**External References:**
- [Context Manager Protocol (PEP 343)](https://www.python.org/dev/peps/pep-0343/)
- [Rich Progress Bars](https://rich.readthedocs.io/en/latest/progress.html)

---

**Status:** ✅ Accepted  
**Implementation Target:** Milestone 4, Phase 3 (Week 3)  
**Estimated Effort:** 2-3 hours  
**Dependencies:** ADR-030 (Rich CLI), ADR-032 (Dashboard events)
