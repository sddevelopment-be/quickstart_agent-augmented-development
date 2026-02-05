# Technical Design: Real-Time Execution Dashboard

**Document Type:** Technical Design  
**Date:** 2026-02-05  
**Architect:** Architect Alphonso  
**Status:** Approved  
**Related ADR:** [ADR-032: Real-Time Execution Dashboard](../adrs/ADR-032-real-time-execution-dashboard.md)

---

## Executive Summary

This document provides detailed technical design for the real-time web-based dashboard that monitors LLM Service executions. The dashboard provides live visibility into execution progress, costs, model routing decisions, and operational metrics.

**Key Objectives:**
1. Real-time visibility into LLM operations (< 100ms latency)
2. Cost tracking and budget awareness
3. Multi-operation management
4. Intervention capability (stop operations)
5. Historical analytics and trends

**Technology Stack:**
- **Backend:** Flask + Flask-SocketIO (Python 3.9+)
- **Frontend:** Vanilla JavaScript + Chart.js + Socket.IO Client
- **Event System:** In-process Observer pattern
- **Persistence:** Optional SQLite for history

---

## 1. Architecture Overview

### 1.1 System Context Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                         User Environment                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                      ┌──────────────┐       │
│  │   Terminal   │                      │   Browser    │       │
│  │              │                      │  (Dashboard) │       │
│  │ llm-service  │                      │              │       │
│  │   execute    │                      │ localhost:   │       │
│  │              │                      │   8080       │       │
│  └──────┬───────┘                      └──────┬───────┘       │
│         │                                      │               │
│         │ CLI Commands                         │ WebSocket     │
│         ▼                                      ▼               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │          LLM Service (Python Process)                   │  │
│  ├─────────────────────────────────────────────────────────┤  │
│  │                                                          │  │
│  │  ┌──────────────┐         ┌──────────────────────────┐ │  │
│  │  │ CLI Layer    │         │  Dashboard Server        │ │  │
│  │  │ (Click)      │         │  (Flask + SocketIO)      │ │  │
│  │  └──────┬───────┘         └────────┬─────────────────┘ │  │
│  │         │                           │                   │  │
│  │         │                           │ Subscribe         │  │
│  │         ▼                           ▼                   │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │           Event Bus (Observer Pattern)          │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │         ▲                           │                   │  │
│  │         │ Emit Events               │ Broadcast         │  │
│  │         │                           ▼                   │  │
│  │  ┌──────────────┐         ┌──────────────────────────┐ │  │
│  │  │ Routing      │         │  WebSocket Handler       │ │  │
│  │  │ Engine       │         │  (Push to clients)       │ │  │
│  │  └──────────────┘         └──────────────────────────┘ │  │
│  │                                                          │  │
│  │  ┌──────────────┐         ┌──────────────────────────┐ │  │
│  │  │ Adapter      │         │  Optional:               │ │  │
│  │  │ Execution    │         │  SQLite History Store    │ │  │
│  │  └──────────────┘         └──────────────────────────┘ │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                     │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────┐ │
│  │ Operations     │  │ Cost Tracker   │  │ Logs Panel  │ │
│  │ Panel          │  │ Chart          │  │             │ │
│  │ (active tasks) │  │ (Chart.js)     │  │ (streaming) │ │
│  └────────┬───────┘  └────────┬───────┘  └──────┬──────┘ │
│           │                   │                  │        │
│           └───────────────────┴──────────────────┘        │
│                              │                            │
│                    ┌─────────▼─────────┐                  │
│                    │ Socket.IO Client  │                  │
│                    │ (WebSocket)       │                  │
│                    └─────────┬─────────┘                  │
└──────────────────────────────┼─────────────────────────────┘
                              │ WebSocket Connection
┌──────────────────────────────▼─────────────────────────────┐
│                    Backend (Flask)                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │           Flask-SocketIO Server                    │   │
│  │  ┌──────────────┐  ┌──────────────────────────┐   │   │
│  │  │ WebSocket    │  │ HTTP Routes              │   │   │
│  │  │ Handlers     │  │ /api/operations          │   │   │
│  │  │              │  │ /api/metrics             │   │   │
│  │  └──────┬───────┘  └──────┬───────────────────┘   │   │
│  └─────────┼──────────────────┼───────────────────────┘   │
│            │                  │                           │
│            │                  │                           │
│  ┌─────────▼──────────────────▼───────────────────────┐   │
│  │         Event Subscriber                          │   │
│  │  (Listens to Event Bus)                           │   │
│  └─────────┬───────────────────────────────────────────┘   │
│            │ Subscribe to all event types                 │
│            ▼                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Event Bus (Observer Pattern)               │   │
│  │  - routing.decision                                │   │
│  │  - execution.start/progress/complete/error         │   │
│  │  - cost.update                                     │   │
│  │  - step.start/complete                             │   │
│  └─────────▲───────────────────────────────────────────┘   │
│            │ Emit events                                  │
│            │                                              │
│  ┌─────────┴──────────┐  ┌──────────────────────────┐    │
│  │ Routing Engine     │  │ Adapter Execution        │    │
│  └────────────────────┘  └──────────────────────────┘    │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Optional: History Store (SQLite)                  │   │
│  │  - operations table                                │   │
│  │  - metrics table                                   │   │
│  │  - events table                                    │   │
│  └────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

---

## 2. Data Models

### 2.1 Event Data Structures

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List

@dataclass
class ExecutionStartEvent:
    """Event emitted when execution starts."""
    operation_id: str
    tool: str
    model: str
    timestamp: datetime
    prompt_length: int
    user: Optional[str] = None

@dataclass
class ExecutionProgressEvent:
    """Event emitted during execution."""
    operation_id: str
    tokens_used: int
    cost_usd: float
    elapsed_seconds: float
    timestamp: datetime

@dataclass
class ExecutionCompleteEvent:
    """Event emitted on successful completion."""
    operation_id: str
    status: str  # 'success'
    output_length: int
    total_tokens: int
    total_cost_usd: float
    duration_seconds: float
    timestamp: datetime

@dataclass
class ExecutionErrorEvent:
    """Event emitted on execution error."""
    operation_id: str
    status: str  # 'error'
    error_type: str
    error_message: str
    step_failed: Optional[str]
    timestamp: datetime

@dataclass
class RoutingDecisionEvent:
    """Event emitted when routing engine selects model."""
    operation_id: str
    model_selected: str
    criteria: Dict[str, Any]
    alternatives: List[str]
    reason: str
    timestamp: datetime

@dataclass
class CostUpdateEvent:
    """Event emitted when cost accumulates."""
    operation_id: str
    tokens_delta: int
    cost_delta_usd: float
    cumulative_tokens: int
    cumulative_cost_usd: float
    timestamp: datetime

@dataclass
class StepEvent:
    """Event emitted for step tracking."""
    operation_id: str
    operation_name: str
    step_name: str
    step_index: int
    total_steps: int
    status: str  # 'start' | 'complete' | 'error'
    duration_seconds: Optional[float] = None
    timestamp: datetime = None
```

### 2.2 WebSocket Message Protocol

```typescript
// Client → Server messages

interface StopOperationMessage {
    type: 'stop_operation';
    operation_id: string;
}

interface PingMessage {
    type: 'ping';
    timestamp: number;
}

// Server → Client messages

interface ConnectedMessage {
    type: 'connected';
    status: 'ok';
    server_version: string;
}

interface EventMessage {
    type: 'event';
    event_type: string;
    data: {
        operation_id?: string;
        [key: string]: any;
    };
    timestamp: string;  // ISO 8601
}

interface OperationStoppedMessage {
    type: 'operation_stopped';
    operation_id: string;
    status: 'stopped' | 'error';
    message: string;
}

interface PongMessage {
    type: 'pong';
    timestamp: number;
}
```

### 2.3 Persistence Schema (Optional SQLite)

```sql
-- Operations table
CREATE TABLE operations (
    operation_id TEXT PRIMARY KEY,
    tool TEXT NOT NULL,
    model TEXT NOT NULL,
    status TEXT NOT NULL,  -- 'running', 'success', 'error', 'stopped'
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_seconds REAL,
    total_tokens INTEGER,
    total_cost_usd REAL,
    prompt_length INTEGER,
    output_length INTEGER,
    error_message TEXT,
    user TEXT
);

-- Events table (complete event log)
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_id TEXT,
    event_type TEXT NOT NULL,
    event_data JSON NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (operation_id) REFERENCES operations(operation_id)
);

-- Metrics aggregations (pre-computed for dashboard)
CREATE TABLE metrics_hourly (
    hour_timestamp TIMESTAMP PRIMARY KEY,
    total_operations INTEGER,
    successful_operations INTEGER,
    failed_operations INTEGER,
    total_tokens INTEGER,
    total_cost_usd REAL,
    avg_duration_seconds REAL
);

-- Indexes for query performance
CREATE INDEX idx_operations_start_time ON operations(start_time);
CREATE INDEX idx_operations_status ON operations(status);
CREATE INDEX idx_events_operation_id ON events(operation_id);
CREATE INDEX idx_events_timestamp ON events(timestamp);
```

---

## 3. Deployment Architectures

### 3.1 Integrated Mode (MVP)

**Use Case:** Local development, single-user

**Architecture:**
```
┌────────────────────────────────────┐
│  Single Python Process             │
├────────────────────────────────────┤
│                                    │
│  Main Thread:                      │
│  ├─ Click CLI                      │
│  ├─ Routing Engine                 │
│  └─ Adapter Execution              │
│                                    │
│  Background Thread:                │
│  └─ Flask-SocketIO Server          │
│     └─ Port 8080 (localhost only)  │
│                                    │
│  Shared:                           │
│  └─ Event Bus (in-process)         │
│                                    │
└────────────────────────────────────┘
```

**Implementation:**
```python
# src/llm_service/dashboard/integrated.py

import threading
from llm_service.dashboard import create_app, socketio

class IntegratedDashboard:
    """Dashboard running in background thread."""
    
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.thread = None
        self.running = False
    
    def start(self):
        """Start dashboard in background thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        self.thread.start()
    
    def _run_server(self):
        """Run Flask-SocketIO server."""
        app = create_app()
        socketio.run(
            app,
            host=self.host,
            port=self.port,
            debug=False,
            use_reloader=False
        )
    
    def stop(self):
        """Stop dashboard server."""
        # Flask-SocketIO doesn't support clean shutdown from thread
        # Daemon thread will exit with main process
        self.running = False

# Global instance
_dashboard = None

def get_dashboard() -> IntegratedDashboard:
    """Get singleton dashboard instance."""
    global _dashboard
    if _dashboard is None:
        _dashboard = IntegratedDashboard()
    return _dashboard
```

**Pros:**
- ✅ Simple deployment (single process)
- ✅ No IPC overhead
- ✅ Easy debugging

**Cons:**
- ⚠️ Dashboard stops when CLI exits
- ⚠️ Shared resources (CPU/memory)

**Best For:** Local development, quick operations

### 3.2 Standalone Mode (Future)

**Use Case:** Long-running monitoring, team dashboard

**Architecture:**
```
┌────────────────────┐         ┌────────────────────┐
│  CLI Clients       │         │  Dashboard Server  │
│  (Multiple)        │         │  (Separate Process)│
├────────────────────┤         ├────────────────────┤
│ llm-service        │  Emit   │ Flask + SocketIO   │
│ execute            ├────────▶│                    │
└────────────────────┘  Events └──────────┬─────────┘
                                          │ Broadcast
┌────────────────────┐         ┌──────────▼─────────┐
│  Message Queue     │◀────────│  Browser Clients   │
│  (Redis/RabbitMQ)  │         │  (Multiple)        │
└────────────────────┘         └────────────────────┘
```

**Implementation:**
```python
# Future enhancement - not MVP

class StandaloneDashboard:
    """Dashboard server with message queue."""
    
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe('llm_service_events')
    
    def run(self):
        """Run dashboard with Redis events."""
        app = create_app()
        
        # Listen to Redis pubsub in background
        threading.Thread(
            target=self._consume_redis_events,
            daemon=True
        ).start()
        
        # Run Flask-SocketIO
        socketio.run(app, host='0.0.0.0', port=8080)
    
    def _consume_redis_events(self):
        """Consume events from Redis and broadcast to WebSocket."""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                event = json.loads(message['data'])
                socketio.emit('event', event)
```

**Pros:**
- ✅ Dashboard survives CLI process restarts
- ✅ Multiple CLI clients share one dashboard
- ✅ Better resource isolation

**Cons:**
- ⚠️ Requires message queue (Redis/RabbitMQ)
- ⚠️ More complex deployment
- ⚠️ Additional dependencies

**Best For:** Production deployments, team monitoring

---

## 4. Security Architecture

### 4.1 Threat Model

| Threat | Severity | Mitigation |
|--------|----------|------------|
| **Unauthorized Access** | High | Localhost-only default, optional token auth |
| **Data Leakage (Logs)** | High | Log sanitization, redact secrets |
| **CSRF Attacks** | Medium | CORS restrictions, WebSocket origin validation |
| **XSS Injection** | Medium | Sanitize all user input, CSP headers |
| **Denial of Service** | Low | Rate limiting, event queue max size |
| **Man-in-the-Middle** | Medium | Optional HTTPS (future) |

### 4.2 Security Controls

**Localhost-Only Default:**
```python
# src/llm_service/dashboard/app.py

def create_app(secure=True):
    """Create Flask app with security controls."""
    app = Flask(__name__)
    
    if secure:
        # Force localhost binding
        @app.before_request
        def localhost_only():
            if not is_localhost_request(request):
                abort(403, "Dashboard only accessible from localhost")
    
    return app

def is_localhost_request(request):
    """Check if request originates from localhost."""
    remote_addr = request.remote_addr
    return remote_addr in ['127.0.0.1', '::1', 'localhost']
```

**Optional Token Authentication:**
```python
# For remote access (opt-in)

import secrets

class TokenAuth:
    """Token-based authentication for remote access."""
    
    def __init__(self):
        self.token = os.getenv('DASHBOARD_TOKEN') or self._generate_token()
    
    def _generate_token(self) -> str:
        """Generate secure random token."""
        return secrets.token_urlsafe(32)
    
    def validate(self, request) -> bool:
        """Validate token from request."""
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header[7:]
        return secrets.compare_digest(token, self.token)

# Enable via environment variable
@app.before_request
def check_auth():
    if os.getenv('DASHBOARD_REMOTE_ACCESS'):
        auth = TokenAuth()
        if not auth.validate(request):
            abort(401, "Invalid authentication token")
```

**Log Sanitization:**
```python
import re

class LogSanitizer:
    """Redact sensitive patterns from logs."""
    
    PATTERNS = [
        (r'api[_-]?key["\s:=]+([A-Za-z0-9-_]+)', 'api_key=***REDACTED***'),
        (r'token["\s:=]+([A-Za-z0-9-_.]+)', 'token=***REDACTED***'),
        (r'password["\s:=]+(\S+)', 'password=***REDACTED***'),
        (r'ANTHROPIC_API_KEY=\S+', 'ANTHROPIC_API_KEY=***REDACTED***'),
    ]
    
    def sanitize(self, log_entry: str) -> str:
        """Redact sensitive patterns."""
        result = log_entry
        for pattern, replacement in self.PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result

# Use in event emission
def emit_event(event_type: str, data: Dict):
    """Emit event with sanitized data."""
    sanitizer = LogSanitizer()
    sanitized_data = {
        k: sanitizer.sanitize(str(v)) if isinstance(v, str) else v
        for k, v in data.items()
    }
    socketio.emit('event', {'type': event_type, 'data': sanitized_data})
```

**CORS Configuration:**
```python
# Strict CORS for WebSocket
socketio = SocketIO(
    app,
    cors_allowed_origins=[
        'http://localhost:8080',
        'http://127.0.0.1:8080'
    ],
    cors_credentials=True
)
```

**Content Security Policy:**
```python
@app.after_request
def set_csp_header(response):
    """Set Content Security Policy header."""
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.socket.io https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' ws://localhost:8080 wss://localhost:8080"
    )
    return response
```

### 4.3 Security Best Practices

**DO:**
- ✅ Bind to localhost (127.0.0.1) by default
- ✅ Require explicit opt-in for remote access
- ✅ Sanitize all logs before display
- ✅ Validate WebSocket message types
- ✅ Rate-limit event emissions
- ✅ Use HTTPS for production deployments (future)

**DON'T:**
- ❌ Bind to 0.0.0.0 by default
- ❌ Log raw API keys or tokens
- ❌ Trust client-supplied data without validation
- ❌ Allow arbitrary WebSocket origins
- ❌ Expose internal stack traces to clients

---

## 5. Performance Considerations

### 5.1 Event System Performance

**Event Batching:**
```python
from collections import deque
from threading import Thread, Lock
import time

class BatchingEventBus(EventBus):
    """Event bus with batching for high-frequency events."""
    
    def __init__(self, batch_interval: float = 0.1, max_batch_size: int = 100):
        super().__init__()
        self.batch_interval = batch_interval
        self.max_batch_size = max_batch_size
        self.batch_queue = deque()
        self.lock = Lock()
        self._start_flush_thread()
    
    def emit(self, event_type: str, data: Dict):
        """Add event to batch queue."""
        with self.lock:
            self.batch_queue.append((event_type, data))
            
            # Flush if batch full
            if len(self.batch_queue) >= self.max_batch_size:
                self._flush_batch()
    
    def _start_flush_thread(self):
        """Start background thread to flush batches."""
        def flush_loop():
            while True:
                time.sleep(self.batch_interval)
                self._flush_batch()
        
        thread = Thread(target=flush_loop, daemon=True)
        thread.start()
    
    def _flush_batch(self):
        """Flush batched events."""
        with self.lock:
            if not self.batch_queue:
                return
            
            events = list(self.batch_queue)
            self.batch_queue.clear()
        
        # Process batch
        for event_type, data in events:
            super().emit(event_type, data)
```

**Event Queue Size Limiting:**
```python
class BoundedEventQueue:
    """Event queue with max size to prevent memory exhaustion."""
    
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.queue = deque(maxlen=max_size)
    
    def append(self, event):
        """Append event (oldest dropped if full)."""
        if len(self.queue) >= self.max_size:
            logger.warning(f"Event queue full ({self.max_size}), dropping oldest event")
        self.queue.append(event)
```

### 5.2 WebSocket Optimization

**Heartbeat Mechanism:**
```python
# Server-side heartbeat
@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('connected', {'status': 'ok'})
    
    # Start heartbeat
    def heartbeat():
        while True:
            time.sleep(30)
            emit('heartbeat', {'timestamp': time.time()})
    
    threading.Thread(target=heartbeat, daemon=True).start()

# Client-side heartbeat response
socket.on('heartbeat', (data) => {
    socket.emit('heartbeat_ack', { timestamp: data.timestamp });
});
```

**Connection Pool Management:**
```python
class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self, max_connections: int = 100):
        self.max_connections = max_connections
        self.connections = {}
        self.lock = Lock()
    
    def add_connection(self, sid: str):
        """Add client connection."""
        with self.lock:
            if len(self.connections) >= self.max_connections:
                raise RuntimeError("Max connections reached")
            
            self.connections[sid] = {
                'connected_at': datetime.utcnow(),
                'last_heartbeat': datetime.utcnow()
            }
    
    def remove_connection(self, sid: str):
        """Remove client connection."""
        with self.lock:
            self.connections.pop(sid, None)
    
    def cleanup_stale_connections(self, timeout: int = 300):
        """Remove connections without heartbeat."""
        with self.lock:
            now = datetime.utcnow()
            stale = [
                sid for sid, info in self.connections.items()
                if (now - info['last_heartbeat']).seconds > timeout
            ]
            
            for sid in stale:
                self.connections.pop(sid)
                logger.info(f"Cleaned up stale connection: {sid}")
```

### 5.3 Resource Usage Targets

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Dashboard Memory** | < 50MB | `ps aux | grep flask` |
| **Event Latency** | < 100ms | Event timestamp - emission timestamp |
| **WebSocket Throughput** | > 100 events/sec | Benchmark test |
| **CPU Usage (idle)** | < 5% | `top` command |
| **CPU Usage (active)** | < 20% | During heavy operations |

---

## 6. Testing Strategy

### 6.1 Unit Tests

```python
# tests/dashboard/test_event_bus.py

def test_event_bus_subscription():
    """Test event bus subscription and emission."""
    bus = EventBus()
    received = []
    
    def handler(event):
        received.append(event)
    
    bus.subscribe('test.event', handler)
    bus.emit('test.event', {'key': 'value'})
    
    assert len(received) == 1
    assert received[0].type == 'test.event'

def test_event_batching():
    """Test batched event processing."""
    bus = BatchingEventBus(batch_interval=0.1, max_batch_size=10)
    
    # Emit 5 events (below batch size)
    for i in range(5):
        bus.emit('test', {'index': i})
    
    time.sleep(0.2)  # Wait for flush
    
    # Verify all events processed
    assert len(bus.processed_events) == 5

# tests/dashboard/test_websocket.py

def test_websocket_connect():
    """Test WebSocket connection."""
    client = socketio.test_client(app)
    
    assert client.is_connected()
    
    received = client.get_received()
    assert len(received) > 0
    assert received[0]['name'] == 'connected'

def test_websocket_event_broadcast():
    """Test event broadcast to clients."""
    client1 = socketio.test_client(app)
    client2 = socketio.test_client(app)
    
    # Emit event from server
    event_bus.emit('test.event', {'data': 'test'})
    
    time.sleep(0.1)
    
    # Both clients should receive
    assert len(client1.get_received()) > 0
    assert len(client2.get_received()) > 0
```

### 6.2 Integration Tests

```python
# tests/dashboard/test_integration.py

def test_end_to_end_execution_tracking():
    """Test complete execution flow with dashboard."""
    # Start dashboard
    dashboard = IntegratedDashboard()
    dashboard.start()
    
    # Connect WebSocket client
    client = socketio.test_client(app)
    
    # Execute LLM operation
    result = runner.invoke(execute, ['--prompt', 'test'])
    
    # Wait for events
    time.sleep(0.5)
    
    # Verify events received
    events = client.get_received()
    event_types = [e['args'][0]['event_type'] for e in events]
    
    assert 'execution.start' in event_types
    assert 'execution.complete' in event_types
    
    # Cleanup
    dashboard.stop()
```

### 6.3 Load Tests

```python
# tests/dashboard/test_performance.py

import pytest
from locust import HttpUser, task, between

class DashboardLoadTest(HttpUser):
    """Load test for dashboard."""
    wait_time = between(1, 3)
    
    @task
    def view_operations(self):
        """Load operations list."""
        self.client.get('/api/operations')
    
    @task
    def view_metrics(self):
        """Load metrics."""
        self.client.get('/api/metrics')

# Run: locust -f tests/dashboard/test_performance.py --host http://localhost:8080
```

---

## 7. Implementation Roadmap

### Phase 1: MVP (Week 2 of M4)
**Estimated: 12-16 hours**

**Tasks:**
1. Event bus implementation (2h)
2. Flask app + WebSocket handler (3h)
3. Basic HTML/CSS/JS frontend (4h)
4. Integration with CLI (2h)
5. Testing (2h)
6. Documentation (1h)

**Deliverables:**
- ✅ Working dashboard (localhost only)
- ✅ Real-time execution visibility
- ✅ Cost tracking
- ✅ Basic intervention (stop operations)

### Phase 2: Enhancement (Week 3 of M4)
**Estimated: 6-8 hours**

**Tasks:**
1. Step tracking integration (2h)
2. Historical metrics (SQLite) (3h)
3. Chart.js visualizations (2h)
4. Security hardening (1h)

**Deliverables:**
- ✅ Step progress in dashboard
- ✅ Historical analytics
- ✅ Cost trend charts
- ✅ Security controls

### Phase 3: Polish (Week 4 of M4)
**Estimated: 4-6 hours**

**Tasks:**
1. UI/UX improvements (2h)
2. Error handling refinement (1h)
3. Performance optimization (1h)
4. User documentation (1h)

**Deliverables:**
- ✅ Polished UI
- ✅ Robust error handling
- ✅ Optimized performance
- ✅ Complete user guide

---

## 8. References

**Related Documents:**
- [ADR-032: Real-Time Execution Dashboard](../adrs/ADR-032-real-time-execution-dashboard.md)
- [spec-kitty Inspired Enhancements](spec-kitty-inspired-enhancements.md)
- [spec-kitty Comparative Analysis](comparative_study/2026-02-05-spec-kitty-comparative-analysis.md)

**External References:**
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Socket.IO Protocol Specification](https://socket.io/docs/v4/socket-io-protocol/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [WebSocket Security Best Practices](https://owasp.org/www-community/vulnerabilities/WebSocket_security)

---

**Document Status:** ✅ Complete  
**Review Date:** 2026-03-05 (1 month post-implementation)
