# Real-Time Execution Dashboard

**Status**: ✅ COMPLETE (M4 Batch 4.2)  
**Version**: 0.1.0  
**Author**: Backend-dev Benny  
**Reference**: ADR-032

## Overview

A real-time web-based dashboard for monitoring LLM service operations. Provides live visibility into:
- Task workflow (Kanban board watching YAML files)
- Cost/metrics tracking
- Model usage statistics
- Real-time event updates via WebSocket

## Features

✅ **File-Based Orchestration**: Watches `work/collaboration/` YAML files (read-only)  
✅ **Real-Time Updates**: WebSocket events (<100ms latency)  
✅ **Cost Tracking**: SQLite-based telemetry history  
✅ **Live Kanban Board**: Inbox → Assigned → Done visualization  
✅ **Professional UI**: Dark theme, responsive, Chart.js visualizations  
✅ **Auto-Reconnection**: Resilient WebSocket client  
✅ **Test Coverage**: 37/37 tests passing (32 unit + 5 integration)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Dashboard UI                          │
│              (HTML/CSS/JS + Chart.js)                    │
└────────────────────┬────────────────────────────────────┘
                     │ WebSocket (/dashboard)
┌────────────────────┴────────────────────────────────────┐
│              Flask + SocketIO Server                     │
│         (app.py - HTTP/WebSocket endpoints)              │
└──────┬────────────────────────┬─────────────────────────┘
       │                        │
       │                        │
┌──────▼───────────┐    ┌──────▼──────────────────────────┐
│  File Watcher    │    │     Telemetry API               │
│  (watchdog)      │    │  (SQLite queries)               │
│                  │    │                                  │
│  Monitors:       │    │  Provides:                      │
│  - inbox/        │    │  - Cost aggregation             │
│  - assigned/     │    │  - Model usage stats            │
│  - done/         │    │  - Trends & history             │
└──────┬───────────┘    └──────┬──────────────────────────┘
       │                        │
       │ (YAML files)           │ (SQLite DB)
       │                        │
┌──────▼────────────────────────▼─────────────────────────┐
│              File System / Database                      │
│  work/collaboration/{inbox,assigned,done}/*.yaml         │
│  telemetry.db (invocations, daily_costs)                │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Installation

Dependencies are in `pyproject.toml`:
```toml
dependencies = [
    "Flask>=2.3.0",
    "Flask-SocketIO>=5.3.0",
    "Flask-CORS>=4.0.0",
    "watchdog>=3.0.0",
    "python-socketio>=5.10.0",
    "PyYAML>=6.0",
    "pydantic>=2.0.0"
]
```

Install with:
```bash
pip install -e .
```

### 2. Running the Dashboard

**Option A: As a module**
```python
from llm_service.dashboard import run_dashboard

run_dashboard(host='localhost', port=8080, debug=True)
```

**Option B: Integrated with CLI** (future)
```bash
llm-service dashboard start --port 8080
```

**Option C: Direct execution**
```bash
python src/llm_service/dashboard/app.py
```

Dashboard will be available at: `http://localhost:8080`

### 3. Configuration

**Environment Variables:**
```bash
export DASHBOARD_SECRET_KEY="your-secret-key"  # Optional, auto-generated if not set
```

**Directories to Watch:**
```python
from llm_service.dashboard import create_app
from llm_service.dashboard.file_watcher import FileWatcher

app, socketio = create_app()
watcher = FileWatcher(
    watch_dir='work/collaboration',
    socketio=socketio
)
watcher.start()
socketio.run(app, host='localhost', port=8080)
```

## API Endpoints

### HTTP REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI (HTML) |
| `/health` | GET | Health check |
| `/api/stats` | GET | Current statistics (tasks, costs) |
| `/api/tasks` | GET | Task snapshot (inbox/assigned/done) |

### WebSocket Events

**Namespace**: `/dashboard`

**Server → Client Events:**
```javascript
// Task events
socket.on('task.created', (data) => { ... });
socket.on('task.assigned', (data) => { ... });
socket.on('task.completed', (data) => { ... });
socket.on('task.updated', (data) => { ... });

// Cost updates
socket.on('cost.update', (data) => { ... });

// System events
socket.on('connection_ack', (data) => { ... });
socket.on('pong', (data) => { ... });
```

**Client → Server Events:**
```javascript
socket.emit('ping');  // Keep-alive
```

## File Structure

```
src/llm_service/dashboard/
├── __init__.py                 # Module entry point
├── app.py                      # Flask + SocketIO server (192 lines)
├── file_watcher.py             # File monitoring with watchdog (351 lines)
├── telemetry_api.py            # Cost/metrics queries (240 lines)
└── static/
    ├── index.html              # Dashboard UI (152 lines)
    ├── dashboard.css           # Styles (374 lines)
    └── dashboard.js            # Frontend logic (444 lines)

tests/
├── unit/dashboard/
│   ├── test_app.py             # Flask/WebSocket tests (12 tests)
│   ├── test_file_watcher.py    # File watching tests (10 tests)
│   └── test_telemetry_api.py   # Telemetry tests (10 tests)
└── integration/dashboard/
    └── test_dashboard_integration.py  # E2E tests (5 tests)
```

## Testing

**Run all tests:**
```bash
pytest tests/unit/dashboard/ tests/integration/dashboard/ -v
```

**Coverage:**
```bash
pytest tests/unit/dashboard/ --cov=src/llm_service/dashboard --cov-report=term
```

**Current Status**: ✅ 37/37 tests passing (100% success rate)

## Technical Decisions

### 1. File-Based Task Tracking (ADR-032)
**Decision**: Tasks tracked via YAML files in `work/collaboration/`, NOT database.  
**Rationale**: Preserves Git audit trail, maintains existing agent workflows.  
**Trade-off**: Slightly higher latency (~100ms) vs. DB queries, but acceptable.

### 2. WebSocket for Real-Time Updates
**Decision**: Flask-SocketIO for bidirectional communication.  
**Rationale**: Production-ready, integrates with existing Flask ecosystem.  
**Alternatives**: FastAPI (more modern, but adds complexity), plain WebSockets (low-level).

### 3. SQLite for Telemetry Only
**Decision**: Telemetry history in SQLite, task state in YAML files.  
**Rationale**: Clear separation: telemetry = DB (query-optimized), orchestration = files (Git-tracked).

## Performance Characteristics

- **WebSocket Latency**: <100ms file change → UI update
- **File Watcher Debounce**: 100ms window (prevents duplicate events)
- **Dashboard Refresh**: 30s fallback polling (if WebSocket fails)
- **Chart Rendering**: Chart.js handles up to 1000 data points smoothly
- **Memory Footprint**: ~50MB (Flask + SocketIO + watchdog)

## Future Enhancements

### Short-Term (M4 Batch 4.3+)
- [ ] MCP Server Health Monitoring panel
- [ ] Server start/stop/restart controls
- [ ] Tool availability dashboard
- [ ] Budget alerts & notifications

### Medium-Term (M5+)
- [ ] Historical task analysis
- [ ] Multi-dashboard support (authentication)
- [ ] Export metrics (CSV/JSON)
- [ ] Dark/light theme toggle
- [ ] Mobile-optimized layout

### Long-Term
- [ ] Distributed dashboard (multi-node LLM clusters)
- [ ] Advanced analytics (ML-based cost predictions)
- [ ] Integration with external monitoring (Prometheus, Grafana)

## Troubleshooting

### Dashboard Won't Start
**Problem**: `ModuleNotFoundError: No module named 'flask'`  
**Solution**: Install dependencies: `pip install -e .`

### WebSocket Not Connecting
**Problem**: Connection status shows "Disconnected"  
**Solution**: 
1. Check Flask server is running
2. Verify CORS settings allow localhost
3. Check browser console for errors

### Tasks Not Updating
**Problem**: File changes not reflected in dashboard  
**Solution**:
1. Verify file watcher is started: `watcher.start()`
2. Check watched directory path is correct
3. Ensure YAML files are valid (malformed YAML silently ignored)

### High CPU Usage
**Problem**: watchdog consuming excessive CPU  
**Solution**: Reduce watch scope (only `work/collaboration/`, not entire repo)

## Contributing

Follow TDD (Directive 017):
1. Write failing test first (RED)
2. Implement minimal code to pass (GREEN)
3. Refactor for clarity (REFACTOR)

Run tests before committing:
```bash
pytest tests/unit/dashboard/ tests/integration/dashboard/ -v
```

## References

- **ADR-032**: Real-Time Execution Dashboard
- **Directive 014**: Work Log Creation
- **Directive 016**: Acceptance Test Driven Development
- **Directive 017**: Test Driven Development
- **Work Directory Orchestration**: `.github/agents/approaches/work-directory-orchestration.md`

## License

Part of quickstart_agent-augmented-development framework.

## Changelog

### v0.1.0 (2026-02-05)
- ✅ Initial implementation (M4 Batch 4.2)
- ✅ Flask + SocketIO server
- ✅ File watcher with watchdog
- ✅ Telemetry API integration
- ✅ Kanban board UI
- ✅ Cost/metrics visualization (Chart.js)
- ✅ 37/37 tests passing
- ✅ Professional dark theme UI
