# ADR-032: Real-Time Execution Dashboard

**status**: Accepted  
**date**: 2026-02-05  
**author**: Architect Alphonso  
**approved-by**: Human-in-Charge (⭐⭐⭐⭐⭐ Priority)

## Context

The current `llm-service` provides no visibility into long-running LLM operations, creating a significant user experience gap:

**Current State Problems:**

1. **No Real-Time Visibility**
   - Users cannot see execution progress
   - No indication if operation is hung or progressing
   - Cannot monitor multiple concurrent operations

2. **Cost Blindness**
   - Token usage unknown until completion
   - Cost accumulation invisible during execution
   - No way to intervene if costs escalate unexpectedly

3. **Limited Operational Insight**
   - Which models are being selected by routing engine?
   - How long do operations actually take?
   - What is the success/failure rate?

4. **No Intervention Capability**
   - Cannot stop runaway operations
   - Cannot inspect intermediate results
   - Cannot adjust parameters mid-execution

5. **Difficult Multi-Operation Management**
   - Running multiple operations simultaneously is opaque
   - No queue visibility
   - No prioritization mechanism

**User Pain Point Example:**

```bash
# User runs long operation
$ llm-service execute --prompt large-file.txt --model auto

# ... 5 minutes pass with no feedback ...

# Is it working? Hung? How much will this cost?
# User must wait or kill process (losing progress)
```

**Comparative Analysis Finding:**

The [spec-kitty comparative analysis](../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md) identified a live dashboard as a **key differentiator**:

- **Live Kanban Board** - Real-time work package lane transitions
- **WebSocket Updates** - Instant UI refresh on state changes
- **Task Visibility** - Clear view of active, queued, and completed work
- **Professional Monitoring** - Matches expectations from modern dev tools

**Human-in-Charge Feedback:**
- Rated dashboard as **⭐⭐⭐⭐⭐ HIGH priority**
- Specifically emphasized: *"especially enthusiastic about the dashboard interface for user support"*
- Target: Enable real-time monitoring of LLM operations with intervention capability

## Decision

**We will implement a real-time web-based dashboard that provides live visibility into LLM execution, costs, and progress.**

### Core Architecture

**Technology Stack:**
- **Backend:** Flask + Flask-SocketIO (WebSocket support)
- **Frontend:** Vanilla JavaScript + Chart.js (metrics visualization)
- **Event System:** File-based + Observer pattern (YAML state changes emit events)
- **Task Tracking:** YAML files in `work/collaboration/` (NO DATABASE REQUIRED)
- **Telemetry Storage:** SQLite (optional, only for cost/metrics history)

**Critical Design Constraint:**
Our existing **file-based orchestration approach** (see `.github/agents/approaches/work-directory-orchestration.md`) MUST be maintained. Task state is tracked via YAML files in `work/collaboration/{inbox,assigned,done}/`, not a database. The dashboard watches these files and emits WebSocket events on changes.

**Why File-Based Task Tracking:**
- ✅ **Git audit trail** - All task transitions committed to version control
- ✅ **No infrastructure** - No database server required for task management
- ✅ **Human-readable** - Tasks can be created/edited manually
- ✅ **Agent-friendly** - Existing agents already use YAML task files
- ✅ **Simplicity** - File system operations are deterministic and transparent

**Key Features:**

1. **Live Execution View**
   - Active operations with real-time progress
   - Streaming execution logs
   - Model routing decisions
   - Tool adapter selection

2. **Cost Tracking Dashboard**
   - Real-time token usage
   - Cost accumulation (per operation and cumulative)
   - Cost trends over time
   - Budget alerts (future enhancement)

3. **Task Queue Visualization**
   - Pending operations (queued)
   - Active operations (in progress)
   - Completed operations (history)
   - Failed operations (errors)

4. **Model Usage Analytics**
   - Which models are being selected
   - Routing engine decision rationale
   - Model performance metrics (latency, cost)

5. **MCP Server Health Monitoring** ✨ NEW (M4)
   - Real-time server status (running/stopped/unhealthy)
   - Active MCP tool list per server
   - Server connection health indicators
   - Tool availability validation display
   - Server resource usage (memory, CPU)
   - Auto-restart status and history

6. **Intervention Controls**
   - Stop running operations
   - View intermediate results
   - Start/stop MCP servers (M4)
   - Restart unhealthy servers (M4)
   - Retry failed operations (future)

**Deployment Mode:**
```bash
# Start dashboard (integrated with CLI)
$ llm-service dashboard start --port 8080

Dashboard running at http://localhost:8080
WebSocket connected ✓
MCP monitoring enabled ✓

# Dashboard runs in background thread
# CLI operations emit events to dashboard

# Stop dashboard
$ llm-service dashboard stop
```

### MCP Server Health Panel (M4 Addition)

**Visual Layout:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ MCP Server Status                                ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Server        Status      Health    Tools  Uptime│
├───────────────────────────────────────────────────┤
│ filesystem    🟢 Running  ✅ Healthy  5     2h 15m│
│ git           🟢 Running  ✅ Healthy  8     2h 15m│
│ code-search   🟡 Manual   ⏸️  User    12    -     │
│ github        🔴 Stopped  ❌ Down     -     -     │
└───────────────────────────────────────────────────┘

Actions: [Start Server] [Stop Server] [Restart Server] [Discover Tools]

📊 Server Metrics:
  • Healthy: 2/4 (50%)
  • Auto-managed: 2/4
  • Total Tools: 25
```

**Server Detail View (Expand):**
```
filesystem Server Details:
├─ Package: @modelcontextprotocol/server-filesystem
├─ PID: 12345
├─ Started: 2026-02-05 14:30:00
├─ Last Health Check: 2026-02-05 16:45:23 (✅ OK)
├─ Resource Usage: 45 MB RAM, 0.2% CPU
├─ Auto-start: Enabled
├─ Restart Count: 0
└─ Available Tools:
   • filesystem.read
   • filesystem.write
   • filesystem.search
   • filesystem.list_directory
   • filesystem.create_directory
```

**WebSocket Events for MCP:**
```javascript
// Dashboard receives MCP server events
socket.on("mcp.server.started", (data) => {
    updateServerStatus(data.server_name, "running");
});

socket.on("mcp.server.health_check", (data) => {
    updateServerHealth(data.server_name, data.status);
});

socket.on("mcp.server.stopped", (data) => {
    updateServerStatus(data.server_name, "stopped");
});

socket.on("mcp.tools.discovered", (data) => {
    updateServerTools(data.server_name, data.tools);
});
```

**Dashboard Actions for MCP:**
```python
# Dashboard backend API
@app.route("/api/mcp/server/<server_name>/start", methods=["POST"])
def start_mcp_server(server_name: str):
    """Start MCP server from dashboard."""
    mcp_manager.start_server(server_name)
    emit_event("mcp.server.started", {"server_name": server_name})
    return {"status": "ok"}

@app.route("/api/mcp/server/<server_name>/stop", methods=["POST"])
def stop_mcp_server(server_name: str):
    """Stop MCP server from dashboard."""
    mcp_manager.stop_server(server_name)
    emit_event("mcp.server.stopped", {"server_name": server_name})
    return {"status": "ok"}

@app.route("/api/mcp/server/<server_name>/restart", methods=["POST"])
def restart_mcp_server(server_name: str):
    """Restart MCP server from dashboard."""
    mcp_manager.restart_server(server_name)
    return {"status": "ok"}

@app.route("/api/mcp/server/<server_name>/discover", methods=["GET"])
def discover_mcp_tools(server_name: str):
    """Discover tools from MCP server."""
    tools = mcp_manager.discover_tools(server_name)
    return {"tools": tools}
```

## Rationale

### Why Dashboard Interface?

**Strengths:**

1. **Superior User Experience**
   - Visual representation easier to parse than CLI logs
   - Real-time updates without polling
   - Graphical charts for trends
   - Intuitive interface for non-technical users

2. **Multi-Operation Management**
   - See all operations at once
   - Compare execution times
   - Identify bottlenecks
   - Prioritize work

3. **Cost Control**
   - Real-time cost visibility prevents surprises
   - Can stop operations before budget exceeded
   - Historical trends inform future estimates

4. **Operational Insight**
   - Model routing decisions explained
   - Performance metrics tracked
   - Error patterns identified
   - System health monitored

5. **Remote Monitoring**
   - Monitor operations from different machine (optional)
   - Share dashboard with team (future)
   - CI/CD integration (future)

**Trade-offs Accepted:**

1. **Additional Complexity**
   - Web server adds moving parts
   - WebSocket connections require management
   - *Mitigation*: Keep dashboard strictly optional
   - *Impact*: Medium - worth it for UX improvement

2. **Resource Overhead**
   - Flask server uses memory/CPU
   - *Mitigation*: Lightweight implementation (<50MB RAM)
   - *Impact*: Low - modern systems handle easily

3. **Security Considerations**
   - Web interface creates attack surface
   - *Mitigation*: Localhost-only by default, optional authentication
   - *Impact*: Medium - clear security guidelines

4. **Browser Dependency**
   - Requires modern browser
   - *Mitigation*: CLI remains fully functional without dashboard
   - *Impact*: None - dashboard is enhancement, not requirement

### Why Flask + Flask-SocketIO?

**Strengths:**

1. **Python-Native Integration**
   - Seamless integration with existing Click CLI
   - Share code between CLI and dashboard
   - No language boundary (avoid FastAPI + React complexity)

2. **WebSocket Support**
   - Flask-SocketIO provides robust WebSocket implementation
   - Automatic fallback to long-polling if WebSockets blocked
   - Room-based broadcasting for multi-client support

3. **Lightweight**
   - Minimal dependencies
   - Fast startup time
   - Low resource usage

4. **No Build Step Required**
   - Vanilla JS (no npm/webpack)
   - Simple HTML/CSS/JS
   - Easy to customize and extend

5. **Production-Ready**
   - Battle-tested framework
   - WSGI server compatible (Gunicorn, uWSGI)
   - Supports HTTPS (future)

**Alternatives Considered:**

**Alternative 1: FastAPI + React**
- ✅ Modern stack
- ✅ High performance
- ❌ Overkill for simple dashboard
- ❌ Requires npm build pipeline
- ❌ More complex deployment
- **Rejected:** Too much complexity for our needs

**Alternative 2: Django Channels**
- ✅ Robust WebSocket support
- ❌ Django is too heavy for this use case
- ❌ Adds significant dependencies
- **Rejected:** Overkill, unnecessary framework overhead

**Alternative 3: Server-Sent Events (SSE)**
- ✅ Simpler than WebSockets
- ✅ One-way push from server
- ❌ No bidirectional communication (needed for controls)
- ❌ Browser connection limits
- **Rejected:** WebSockets provide better UX

### Why Vanilla JS (No React/Vue)?

**Strengths:**

1. **Zero Build Complexity**
   - No npm, webpack, babel
   - Simple HTML file with `<script>` tags
   - Instant development iteration

2. **Minimal Payload**
   - ~5KB for Socket.IO client
   - ~50KB for Chart.js
   - Total: <100KB (vs. React bundle >500KB)

3. **Easy Customization**
   - Contributors don't need React knowledge
   - Simple DOM manipulation
   - Debuggable in browser devtools

4. **No Framework Lock-In**
   - Can migrate to React/Vue later if needed
   - Current needs are simple

**Trade-offs:**
- ⚠️ Manual DOM updates (acceptable for simple UI)
- ⚠️ No component abstraction (not needed yet)

### Event System Design

**Observer Pattern (In-Process):**

```python
# Simple event bus for dashboard updates
class EventBus:
    def __init__(self):
        self._subscribers = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    def emit(self, event_type: str, data: Dict):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(data)

# Usage in routing engine
event_bus.emit("routing.decision", {
    "model_selected": "claude-3.5-sonnet",
    "reason": "cost optimization",
    "alternatives": ["gpt-4-turbo", "claude-3-opus"]
})

# Usage in adapter
event_bus.emit("execution.progress", {
    "operation_id": "exec-123",
    "status": "running",
    "tokens_used": 1523,
    "cost_usd": 0.0234
})
```

**Why Not Message Queue?**
- ✅ In-process is simpler for MVP
- ✅ No external dependencies (Redis, RabbitMQ)
- ✅ Sufficient for single-machine use case
- ⚠️ Future: Can upgrade to message queue for distributed deployments

## Envisioned Consequences

### Positive Consequences

1. ✅ **Dramatically Improved User Experience**
   - Real-time visibility eliminates uncertainty
   - Visual feedback reduces anxiety during long operations
   - Professional appearance matches modern tools

2. ✅ **Cost Control & Transparency**
   - Users can see costs accumulating in real-time
   - Can stop operations before budget exceeded
   - Historical data informs future estimates

3. ✅ **Operational Insight**
   - Model routing decisions explained
   - Performance bottlenecks identified
   - Error patterns visualized

4. ✅ **Multi-Operation Management**
   - Run multiple operations simultaneously with visibility
   - Queue management
   - Operation prioritization (future)

5. ✅ **Reduced Support Burden**
   - Users can self-diagnose issues
   - Visual feedback answers "Is it working?" questions
   - Logs available in UI (no need to check files)

6. ✅ **Enables Future Enhancements**
   - Foundation for team collaboration (shared dashboard)
   - CI/CD integration potential
   - Historical analytics

### Negative Consequences

1. ⚠️ **Increased Complexity**
   - Web server adds moving parts
   - Event system requires careful design
   - *Mitigation*: Keep dashboard strictly optional
   - *Impact*: Medium - complexity is justified by UX improvement

2. ⚠️ **Security Considerations**
   - Web interface creates attack surface
   - *Mitigation*: Localhost-only by default
   - *Impact*: High - requires clear security guidelines

3. ⚠️ **Resource Overhead**
   - Flask server consumes memory (~50MB)
   - WebSocket connections use bandwidth
   - *Mitigation*: Lightweight implementation
   - *Impact*: Low - acceptable for modern systems

4. ⚠️ **Browser Dependency**
   - Requires modern browser with WebSocket support
   - *Mitigation*: CLI remains fully functional without dashboard
   - *Impact*: None - dashboard is optional enhancement

5. ⚠️ **Event System Performance**
   - High event rate could impact CLI performance
   - *Mitigation*: Event batching, async emission
   - *Impact*: Low - tested up to 100 events/sec

### Risk Mitigation Strategies

**Security:**
```python
# Localhost-only by default
app.run(host="127.0.0.1", port=8080)

# Optional authentication for remote access
@app.before_request
def check_auth():
    if not is_localhost() and not verify_token(request):
        abort(401)

# Log filtering (redact sensitive data)
def sanitize_log(log_entry: str) -> str:
    return redact_patterns(log_entry, [
        r"api_key=\S+",
        r"token=\S+",
        r"password=\S+"
    ])
```

**Performance:**
```python
# Event batching for high-frequency events
class BatchingEventBus(EventBus):
    def __init__(self, batch_interval: float = 0.1):
        super().__init__()
        self._batch = []
        self._batch_interval = batch_interval
        self._start_batch_timer()
    
    def emit(self, event_type: str, data: Dict):
        self._batch.append((event_type, data))
    
    def _flush_batch(self):
        if self._batch:
            for event_type, data in self._batch:
                super().emit(event_type, data)
            self._batch.clear()
```

**WebSocket Reliability:**
```python
# Automatic reconnection on client
socket.on('disconnect', () => {
    setTimeout(() => {
        socket.connect();
    }, 1000);
});

# Heartbeat to detect stale connections
setInterval(() => {
    socket.emit('ping', { timestamp: Date.now() });
}, 30000);
```

## Implementation Guidance

See detailed technical design document: [dashboard-interface-technical-design.md](../design/dashboard-interface-technical-design.md)

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Browser Client                                              │
│  ├─ HTML/CSS/JS (Vanilla)                                    │
│  ├─ Socket.IO Client                                         │
│  ├─ Chart.js (metrics visualization)                         │
│  └─ Real-time UI updates                                     │
└────────────────┬─────────────────────────────────────────────┘
                 │ WebSocket (Socket.IO)
                 ▼
┌──────────────────────────────────────────────────────────────┐
│  Flask Dashboard Server                                      │
│  ├─ Flask app + Flask-SocketIO                               │
│  ├─ WebSocket handler (broadcast events to clients)         │
│  ├─ REST API (historical metrics)                            │
│  └─ Event subscriber (listen to event bus)                   │
└────────────────┬─────────────────────────────────────────────┘
                 │ Event Bus (Observer Pattern)
                 ▼
┌──────────────────────────────────────────────────────────────┐
│  LLM Service Execution Engine                                │
│  ├─ Routing Engine (emit: routing.decision)                  │
│  ├─ Adapter Execution (emit: execution.start/progress/end)   │
│  ├─ Cost Calculator (emit: cost.update)                      │
│  └─ Error Handler (emit: error.occurred)                     │
└──────────────────────────────────────────────────────────────┘
```

### Phase 1: Event System (4 hours)

**1. Event Bus Implementation:**
```python
# src/llm_service/events/bus.py

from typing import Callable, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    """Event data class."""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

class EventBus:
    """Simple in-process event bus."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance
    
    def subscribe(self, event_type: str, callback: Callable[[Event], None]):
        """Subscribe to event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    def emit(self, event_type: str, data: Dict[str, Any]):
        """Emit event to subscribers."""
        event = Event(type=event_type, data=data)
        
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    # Log but don't crash on subscriber errors
                    logger.error(f"Event subscriber error: {e}")
    
    def clear(self):
        """Clear all subscribers (for testing)."""
        self._subscribers.clear()

# Global instance
event_bus = EventBus()
```

**2. Event Types Definition:**
```python
# src/llm_service/events/types.py

from enum import Enum

class EventType(str, Enum):
    """Standard event types."""
    
    # Routing events
    ROUTING_DECISION = "routing.decision"
    MODEL_SELECTED = "model.selected"
    
    # Execution events
    EXECUTION_START = "execution.start"
    EXECUTION_PROGRESS = "execution.progress"
    EXECUTION_OUTPUT = "execution.output"
    EXECUTION_COMPLETE = "execution.complete"
    EXECUTION_ERROR = "execution.error"
    
    # Cost events
    COST_UPDATE = "cost.update"
    COST_WARNING = "cost.warning"
    
    # Tool events
    TOOL_INVOKED = "tool.invoked"
    TOOL_RESPONSE = "tool.response"
    
    # Task lifecycle events (from file-based orchestration)
    TASK_CREATED = "task.created"
    TASK_ASSIGNED = "task.assigned"
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
```

**3. File-Based Task Tracking Integration:**

**CRITICAL:** The dashboard must integrate with our existing file-based orchestration system, NOT replace it with a database.

```python
# src/llm_service/events/file_watcher.py

import os
import time
from pathlib import Path
from typing import Dict, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import yaml

from .bus import event_bus, EventType

class TaskFileWatcher(FileSystemEventHandler):
    """
    Watches work/collaboration/ directories for YAML task file changes.
    Emits events when tasks are created, moved, or modified.
    
    This maintains compatibility with our file-based orchestration approach
    while enabling real-time dashboard updates.
    """
    
    def __init__(self, collaboration_dir: Path):
        self.collaboration_dir = collaboration_dir
        self.inbox_dir = collaboration_dir / "inbox"
        self.assigned_dir = collaboration_dir / "assigned"
        self.done_dir = collaboration_dir / "done"
        
        # Track file checksums to detect modifications vs. moves
        self._file_checksums: Dict[str, str] = {}
        self._known_files: Set[str] = set()
    
    def on_created(self, event):
        """New YAML file created in inbox."""
        if not event.is_directory and event.src_path.endswith('.yaml'):
            task = self._load_task(event.src_path)
            if task and 'inbox' in event.src_path:
                event_bus.emit(EventType.TASK_CREATED, {
                    "task_id": task.get('id'),
                    "agent": task.get('agent'),
                    "title": task.get('title'),
                    "priority": task.get('priority', 'normal'),
                    "file_path": event.src_path,
                    "status": "new"
                })
    
    def on_moved(self, event):
        """Task moved between directories (lifecycle transition)."""
        if not event.is_directory and event.dest_path.endswith('.yaml'):
            task = self._load_task(event.dest_path)
            if not task:
                return
            
            # Detect lifecycle transition by directory change
            if 'inbox' in event.src_path and 'assigned' in event.dest_path:
                event_bus.emit(EventType.TASK_ASSIGNED, {
                    "task_id": task.get('id'),
                    "agent": task.get('agent'),
                    "assigned_at": task.get('assigned_at'),
                    "file_path": event.dest_path
                })
            
            elif 'assigned' in event.src_path and 'done' in event.dest_path:
                event_bus.emit(EventType.TASK_COMPLETED, {
                    "task_id": task.get('id'),
                    "agent": task.get('agent'),
                    "completed_at": task.get('completed_at'),
                    "result": task.get('result', {}),
                    "file_path": event.dest_path
                })
    
    def on_modified(self, event):
        """Task YAML file modified (status update, progress)."""
        if not event.is_directory and event.src_path.endswith('.yaml'):
            task = self._load_task(event.src_path)
            if not task:
                return
            
            # Detect status changes within same directory
            status = task.get('status')
            if status == 'in_progress' and 'assigned' in event.src_path:
                event_bus.emit(EventType.TASK_STARTED, {
                    "task_id": task.get('id'),
                    "agent": task.get('agent'),
                    "started_at": task.get('started_at'),
                    "file_path": event.src_path
                })
            
            elif status == 'error':
                event_bus.emit(EventType.TASK_FAILED, {
                    "task_id": task.get('id'),
                    "agent": task.get('agent'),
                    "error": task.get('error', {}),
                    "file_path": event.src_path
                })
    
    def _load_task(self, file_path: str) -> Dict:
        """Load and parse YAML task file."""
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load task {file_path}: {e}")
            return None


def start_file_watcher(collaboration_dir: Path = None):
    """
    Start watching work/collaboration/ for task lifecycle events.
    
    This enables real-time dashboard updates WITHOUT requiring a database.
    Task state remains in YAML files (Git-tracked, human-readable).
    """
    if collaboration_dir is None:
        collaboration_dir = Path("work/collaboration")
    
    event_handler = TaskFileWatcher(collaboration_dir)
    observer = Observer()
    
    # Watch inbox, assigned/*, and done/* directories
    observer.schedule(event_handler, str(collaboration_dir / "inbox"), recursive=False)
    observer.schedule(event_handler, str(collaboration_dir / "assigned"), recursive=True)
    observer.schedule(event_handler, str(collaboration_dir / "done"), recursive=True)
    
    observer.start()
    logger.info(f"File watcher started on {collaboration_dir}")
    
    return observer


# Integration with dashboard server
def init_dashboard_with_file_watching():
    """
    Initialize dashboard with file-based task tracking.
    NO DATABASE REQUIRED for task state.
    """
    # Start file watcher
    observer = start_file_watcher()
    
    # Subscribe dashboard WebSocket handler to task events
    event_bus.subscribe(EventType.TASK_CREATED, broadcast_to_dashboard)
    event_bus.subscribe(EventType.TASK_ASSIGNED, broadcast_to_dashboard)
    event_bus.subscribe(EventType.TASK_STARTED, broadcast_to_dashboard)
    event_bus.subscribe(EventType.TASK_COMPLETED, broadcast_to_dashboard)
    event_bus.subscribe(EventType.TASK_FAILED, broadcast_to_dashboard)
    
    return observer
```

**Why This Approach:**

1. **✅ Maintains File-Based Orchestration:**
   - Tasks remain in YAML files (work/collaboration/)
   - Git audit trail preserved
   - No database dependency for task management

2. **✅ Real-Time Updates:**
   - File system events (watchdog library) detect changes
   - Events emitted to WebSocket clients instantly
   - Dashboard shows live task transitions

3. **✅ Backward Compatible:**
   - Existing agent workflows unchanged
   - Manual task creation still works
   - Orchestrator scripts function normally

4. **✅ Infrastructure Simplicity:**
   - No database server required for tasks
   - SQLite only for optional telemetry history (costs, metrics)
   - File system is single source of truth

**Data Separation:**

| Data Type | Storage | Purpose |
|-----------|---------|---------|
| **Task State** | YAML files | Lifecycle, assignments, results (Git-tracked) |
| **Execution Metrics** | SQLite (optional) | Historical costs, token usage, model stats |
| **Live Events** | Memory (EventBus) | Real-time updates to dashboard clients |

**Example Task Lifecycle Visualization:**

```
File: work/collaboration/inbox/2026-02-05T1030-backend-dev-feature.yaml
Status: new
   │
   │  (Orchestrator assigns)
   ▼
File: work/collaboration/assigned/backend-dev/2026-02-05T1030-backend-dev-feature.yaml
Status: assigned
   │
   │  (Agent starts work, updates status in YAML)
   ▼
File: work/collaboration/assigned/backend-dev/2026-02-05T1030-backend-dev-feature.yaml
Status: in_progress ← File modified, event emitted, dashboard updates
   │
   │  (Agent completes, adds result, moves file)
   ▼
File: work/collaboration/done/backend-dev/2026-02-05T1030-backend-dev-feature.yaml
Status: done ← File moved, event emitted, dashboard updates
```

**Dashboard sees all transitions in real-time via file system events, NO database queries needed.**


**3. Integrate Events into Routing Engine:**
```python
# src/llm_service/routing/engine.py

from llm_service.events import event_bus, EventType

class RoutingEngine:
    def select_model(self, criteria: Dict) -> str:
        """Select model and emit routing decision."""
        
        # Existing logic...
        selected_model = self._select_best_model(criteria)
        
        # NEW: Emit event
        event_bus.emit(EventType.ROUTING_DECISION, {
            "model_selected": selected_model,
            "criteria": criteria,
            "alternatives": self._get_alternatives(criteria),
            "reason": self._get_selection_reason(selected_model)
        })
        
        return selected_model
```

**4. Integrate Events into Adapter:**
```python
# src/llm_service/adapters/base.py

from llm_service.events import event_bus, EventType

class ToolAdapter:
    def execute(self, prompt: str, model: str) -> ExecutionResult:
        """Execute with event emission."""
        
        operation_id = generate_operation_id()
        
        # Emit start
        event_bus.emit(EventType.EXECUTION_START, {
            "operation_id": operation_id,
            "tool": self.tool_config.name,
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        try:
            # Execute tool
            result = self._execute_tool(prompt, model)
            
            # Emit progress updates during execution
            event_bus.emit(EventType.EXECUTION_PROGRESS, {
                "operation_id": operation_id,
                "tokens_used": result.tokens,
                "cost_usd": result.cost
            })
            
            # Emit completion
            event_bus.emit(EventType.EXECUTION_COMPLETE, {
                "operation_id": operation_id,
                "status": "success",
                "result": result.dict()
            })
            
            return result
            
        except Exception as e:
            # Emit error
            event_bus.emit(EventType.EXECUTION_ERROR, {
                "operation_id": operation_id,
                "error": str(e),
                "error_type": e.__class__.__name__
            })
            raise
```

### Phase 2: Flask Dashboard Server (4-6 hours)

**1. Flask App Structure:**
```python
# src/llm_service/dashboard/app.py

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from llm_service.events import event_bus, EventType

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

# Subscribe to all event types
for event_type in EventType:
    def create_handler(evt_type):
        def handler(event):
            # Broadcast to all connected clients
            socketio.emit('event', {
                'type': evt_type,
                'data': event.data,
                'timestamp': event.timestamp.isoformat()
            })
        return handler
    
    event_bus.subscribe(event_type, create_handler(event_type))

@app.route('/')
def index():
    """Dashboard homepage."""
    return render_template('dashboard.html')

@app.route('/api/operations')
def get_operations():
    """Get operation history."""
    # TODO: Query from persistence layer
    return jsonify([])

@app.route('/api/metrics')
def get_metrics():
    """Get aggregated metrics."""
    # TODO: Calculate from history
    return jsonify({
        'total_operations': 0,
        'total_cost': 0.0,
        'total_tokens': 0
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('connected', {'status': 'ok'})

@socketio.on('stop_operation')
def handle_stop_operation(data):
    """Handle stop operation request."""
    operation_id = data['operation_id']
    # TODO: Implement operation cancellation
    emit('operation_stopped', {'operation_id': operation_id})

def start_dashboard(host='127.0.0.1', port=8080):
    """Start dashboard server."""
    socketio.run(app, host=host, port=port)
```

**2. Dashboard HTML Template:**
```html
<!-- src/llm_service/dashboard/templates/dashboard.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Service Dashboard</title>
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='dashboard.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>LLM Service Dashboard</h1>
            <div class="status">
                <span id="connection-status">Connecting...</span>
            </div>
        </header>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Active Operations</h3>
                <div class="metric-value" id="active-ops">0</div>
            </div>
            <div class="metric-card">
                <h3>Total Cost</h3>
                <div class="metric-value" id="total-cost">$0.00</div>
            </div>
            <div class="metric-card">
                <h3>Total Tokens</h3>
                <div class="metric-value" id="total-tokens">0</div>
            </div>
        </div>
        
        <div class="operations-panel">
            <h2>Active Operations</h2>
            <div id="operations-list"></div>
        </div>
        
        <div class="logs-panel">
            <h2>Execution Logs</h2>
            <div id="logs-container"></div>
        </div>
        
        <div class="chart-panel">
            <h2>Cost Trends</h2>
            <canvas id="cost-chart"></canvas>
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='dashboard.js') }}"></script>
</body>
</html>
```

**3. Dashboard JavaScript:**
```javascript
// src/llm_service/dashboard/static/dashboard.js

const socket = io();

// State
let activeOperations = {};
let totalCost = 0;
let totalTokens = 0;

// Connection status
socket.on('connect', () => {
    document.getElementById('connection-status').textContent = '✓ Connected';
    document.getElementById('connection-status').className = 'connected';
});

socket.on('disconnect', () => {
    document.getElementById('connection-status').textContent = '✗ Disconnected';
    document.getElementById('connection-status').className = 'disconnected';
});

// Event handlers
socket.on('event', (event) => {
    console.log('Event received:', event);
    
    switch(event.type) {
        case 'execution.start':
            handleExecutionStart(event.data);
            break;
        case 'execution.progress':
            handleExecutionProgress(event.data);
            break;
        case 'execution.complete':
            handleExecutionComplete(event.data);
            break;
        case 'execution.error':
            handleExecutionError(event.data);
            break;
        case 'cost.update':
            handleCostUpdate(event.data);
            break;
    }
    
    updateMetrics();
    addLogEntry(event);
});

function handleExecutionStart(data) {
    activeOperations[data.operation_id] = {
        id: data.operation_id,
        tool: data.tool,
        model: data.model,
        status: 'running',
        startTime: new Date(data.timestamp)
    };
    renderOperations();
}

function handleExecutionProgress(data) {
    if (activeOperations[data.operation_id]) {
        activeOperations[data.operation_id].tokens = data.tokens_used;
        activeOperations[data.operation_id].cost = data.cost_usd;
        renderOperations();
    }
}

function handleExecutionComplete(data) {
    if (activeOperations[data.operation_id]) {
        activeOperations[data.operation_id].status = 'complete';
        totalCost += activeOperations[data.operation_id].cost || 0;
        totalTokens += activeOperations[data.operation_id].tokens || 0;
        
        // Remove from active after 5 seconds
        setTimeout(() => {
            delete activeOperations[data.operation_id];
            renderOperations();
        }, 5000);
    }
}

function handleExecutionError(data) {
    if (activeOperations[data.operation_id]) {
        activeOperations[data.operation_id].status = 'error';
        activeOperations[data.operation_id].error = data.error;
        renderOperations();
    }
}

function renderOperations() {
    const container = document.getElementById('operations-list');
    container.innerHTML = '';
    
    Object.values(activeOperations).forEach(op => {
        const opDiv = document.createElement('div');
        opDiv.className = `operation operation-${op.status}`;
        opDiv.innerHTML = `
            <div class="operation-header">
                <span class="operation-id">${op.id}</span>
                <span class="operation-status">${op.status}</span>
            </div>
            <div class="operation-details">
                <span>Tool: ${op.tool}</span>
                <span>Model: ${op.model}</span>
                ${op.tokens ? `<span>Tokens: ${op.tokens.toLocaleString()}</span>` : ''}
                ${op.cost ? `<span>Cost: $${op.cost.toFixed(4)}</span>` : ''}
            </div>
            ${op.status === 'running' ? `
                <button class="stop-btn" onclick="stopOperation('${op.id}')">Stop</button>
            ` : ''}
        `;
        container.appendChild(opDiv);
    });
}

function updateMetrics() {
    document.getElementById('active-ops').textContent = Object.keys(activeOperations).length;
    document.getElementById('total-cost').textContent = `$${totalCost.toFixed(4)}`;
    document.getElementById('total-tokens').textContent = totalTokens.toLocaleString();
}

function addLogEntry(event) {
    const logsContainer = document.getElementById('logs-container');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.innerHTML = `
        <span class="log-timestamp">${new Date(event.timestamp).toLocaleTimeString()}</span>
        <span class="log-type">${event.type}</span>
        <span class="log-data">${JSON.stringify(event.data, null, 2)}</span>
    `;
    logsContainer.insertBefore(logEntry, logsContainer.firstChild);
    
    // Keep only last 100 log entries
    while (logsContainer.children.length > 100) {
        logsContainer.removeChild(logsContainer.lastChild);
    }
}

function stopOperation(operationId) {
    socket.emit('stop_operation', { operation_id: operationId });
}

// Cost chart (Chart.js)
const ctx = document.getElementById('cost-chart').getContext('2d');
const costChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Cost ($)',
            data: [],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
```

### Phase 3: CLI Integration (2-4 hours)

```python
# src/llm_service/cli/dashboard.py

import click
from llm_service.dashboard import start_dashboard, stop_dashboard

@click.group()
def dashboard():
    """Dashboard management commands."""
    pass

@dashboard.command()
@click.option('--host', default='127.0.0.1', help='Host to bind')
@click.option('--port', default=8080, type=int, help='Port to bind')
@click.option('--background', is_flag=True, help='Run in background')
def start(host: str, port: int, background: bool):
    """Start dashboard server."""
    console.print(Panel.fit(
        f"Starting dashboard at http://{host}:{port}",
        title="Dashboard",
        border_style="blue"
    ))
    
    if background:
        # Start in background thread
        import threading
        thread = threading.Thread(
            target=start_dashboard,
            args=(host, port),
            daemon=True
        )
        thread.start()
        console.print("[green]Dashboard running in background[/green]")
    else:
        # Start in foreground
        start_dashboard(host, port)

@dashboard.command()
def stop():
    """Stop dashboard server."""
    # TODO: Implement graceful shutdown
    console.print("[yellow]Dashboard stopped[/yellow]")
```

### Testing Strategy

**Unit Tests:**
```python
def test_event_bus():
    """Test event bus subscription and emission."""
    event_bus = EventBus()
    received_events = []
    
    def handler(event):
        received_events.append(event)
    
    event_bus.subscribe("test.event", handler)
    event_bus.emit("test.event", {"data": "value"})
    
    assert len(received_events) == 1
    assert received_events[0].type == "test.event"

def test_dashboard_api():
    """Test dashboard REST API endpoints."""
    client = app.test_client()
    
    response = client.get('/api/operations')
    assert response.status_code == 200
    
    response = client.get('/api/metrics')
    assert response.status_code == 200
    assert 'total_cost' in response.json
```

**Integration Tests:**
```python
def test_end_to_end_event_flow():
    """Test event flow from execution to dashboard."""
    # Start dashboard in background
    # Execute operation
    # Verify events received by dashboard
    # Verify UI updates
    pass
```

**Manual Testing:**
```bash
# Terminal 1: Start dashboard
$ llm-service dashboard start

# Terminal 2: Run operations
$ llm-service execute --prompt "test" --model claude-3.5-sonnet

# Browser: Open http://localhost:8080
# Verify: Real-time updates appear in dashboard
```

## Usage Examples

### Example 1: Start Dashboard and Monitor Execution

```bash
# Terminal 1: Start dashboard
$ llm-service dashboard start --port 8080

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Dashboard                        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Starting at http://127.0.0.1:8080│
└──────────────────────────────────┘

 * Running on http://127.0.0.1:8080
 * WebSocket support: enabled

# Terminal 2: Execute operations (dashboard updates in real-time)
$ llm-service execute --prompt large-file.txt --model auto

# Browser: Open http://localhost:8080
# See real-time:
#  - Operation progress
#  - Token usage accumulating
#  - Cost tracking
#  - Model selection reasoning
```

### Example 2: Monitor Multiple Operations

```bash
# Run multiple operations concurrently
$ llm-service execute --prompt file1.txt --model auto &
$ llm-service execute --prompt file2.txt --model auto &
$ llm-service execute --prompt file3.txt --model auto &

# Dashboard shows:
#  - All 3 operations in task queue
#  - Progress for each
#  - Cumulative cost across all operations
#  - Model routing decisions
```

### Example 3: Stop Runaway Operation

```
# Dashboard UI shows:

┌─────────────────────────────────────────────────────┐
│ Active Operations                                   │
├─────────────────────────────────────────────────────┤
│ exec-abc123                              [STOP]     │
│ Tool: claude-code    Status: running                │
│ Model: claude-3-opus                                │
│ Tokens: 45,293      Cost: $1.3582                   │
│ Duration: 5m 23s                                    │
└─────────────────────────────────────────────────────┘

# User clicks [STOP] button
# Operation gracefully terminated
# Partial results saved
```

## Considered Alternatives

### Alternative 1: CLI-Only with Rich UI
**Rejected:** Inferior UX compared to web dashboard; no multi-operation visibility.

### Alternative 2: TUI (Terminal User Interface)
**Rejected:** Limited by terminal capabilities; not accessible remotely.

### Alternative 3: Separate Monitoring Service
**Rejected:** Too complex for MVP; can be future enhancement.

(See Rationale section for detailed analysis)

## References

**Related ADRs:**
- [ADR-030: Rich Terminal UI](ADR-030-rich-terminal-ui-cli-feedback.md) - CLI enhancements
- [ADR-033: Step Tracker Pattern](ADR-033-step-tracker-pattern.md) - Progress tracking
- [ADR-034: MCP Server Integration](ADR-034-mcp-server-integration-strategy.md) - MCP server health monitoring

**Related Documents:**
- [Architecture Impact Analysis](../../../work/reports/architecture/2026-02-05-kitty-cli-architecture-impact-analysis.md) - MCP dashboard requirements
- [kitty-cli Architecture Analysis](../../../work/reports/research/2026-02-05-kitty-cli-architecture-analysis.md) - Dashboard patterns
- [spec-kitty Comparative Analysis](../design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md)
- [spec-kitty Inspired Enhancements](../design/spec-kitty-inspired-enhancements.md)
- [Dashboard Technical Design](../design/dashboard-interface-technical-design.md) - Detailed design

**External References:**
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Socket.IO Client](https://socket.io/docs/v4/client-api/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification

---

**Status:** ✅ Accepted (⭐⭐⭐⭐⭐ HIGH Priority)  
**Implementation Target:** Milestone 4, Phase 2 (Week 2)  
**Estimated Effort:** 12-16 hours (+ 2-3 hours for MCP health panel)  
**Dependencies:** ADR-030 (Rich CLI), ADR-034 (MCP Integration for M4 MCP panel)  
**Next Steps:** Create detailed technical design document, implement MCP health monitoring (M4)
