# Telemetry Module

**Version:** 1.0.0  
**Status:** Production Ready  
**Coverage:** 99%

## Overview

The telemetry module provides comprehensive cost tracking and performance monitoring for the LLM Service Layer. It logs every LLM invocation to a SQLite database, enabling data-driven optimization and budget enforcement.

## Features

✅ **Cost Tracking**
- Token usage (input, output, total)
- USD cost per invocation
- Daily aggregations by agent/tool/model

✅ **Performance Monitoring**
- Latency tracking (milliseconds)
- Success/error status
- Error message capture

✅ **Privacy Controls**
- Metadata mode: Only metrics (no prompts/responses)
- Full mode: Everything (future feature)
- None mode: Disable telemetry

✅ **Database**
- SQLite backend (zero-config)
- Automatic schema initialization
- Optimized indexes for fast queries
- Thread-safe operations

## Quick Start

### 1. Import and Initialize

```python
from pathlib import Path
from llm_service.telemetry import TelemetryLogger, InvocationRecord

# Create logger
logger = TelemetryLogger(
    db_path=Path.home() / ".llm-service" / "telemetry.db",
    privacy_level="metadata"
)
```

### 2. Log an Invocation

```python
import uuid
import time

# Start timing
start_time = time.time()
invocation_id = str(uuid.uuid4())

try:
    # Execute LLM request...
    result = execute_llm_request(prompt)
    
    # Calculate metrics
    latency_ms = int((time.time() - start_time) * 1000)
    
    # Log success
    record = InvocationRecord(
        invocation_id=invocation_id,
        agent_name="backend-dev",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=result['usage']['prompt_tokens'],
        completion_tokens=result['usage']['completion_tokens'],
        total_tokens=result['usage']['total_tokens'],
        cost_usd=calculate_cost(result),
        latency_ms=latency_ms,
        status="success"
    )
    logger.log_invocation(record)
    
except Exception as e:
    # Log error
    latency_ms = int((time.time() - start_time) * 1000)
    
    record = InvocationRecord(
        invocation_id=invocation_id,
        agent_name="backend-dev",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=0,
        completion_tokens=0,
        total_tokens=0,
        cost_usd=0.0,
        latency_ms=latency_ms,
        status="error",
        error_message=str(e)
    )
    logger.log_invocation(record)
    raise
```

### 3. Query Costs and Statistics

```python
from datetime import date, timedelta

# Get daily costs for last 7 days
today = date.today()
week_ago = today - timedelta(days=7)

costs = logger.get_daily_costs(
    start_date=week_ago,
    end_date=today,
    agent_name="backend-dev"
)

for cost in costs:
    print(f"{cost['date']}: ${cost['total_cost_usd']:.3f} ({cost['invocations']} invocations)")

# Get statistics
stats = logger.get_statistics(agent_name="backend-dev", days=7)
print(f"Total cost: ${stats['total_cost_usd']:.2f}")
print(f"Success rate: {stats['success_rate']*100:.1f}%")
print(f"Avg latency: {stats['avg_latency_ms']:.0f}ms")
```

## Configuration

Create `config/telemetry.yaml`:

```yaml
enabled: true
db_path: "~/.llm-service/telemetry.db"
privacy_level: "metadata"  # metadata, full, none
retention_days: 30
```

Load configuration:

```python
from llm_service.config.schemas import TelemetryConfig

config = TelemetryConfig(
    enabled=True,
    db_path="~/.llm-service/telemetry.db",
    privacy_level="metadata",
    retention_days=30
)

logger = TelemetryLogger(
    db_path=config.get_db_path(),
    privacy_level=config.privacy_level
)
```

## Database Schema

### `invocations` Table
Stores every LLM invocation with full metadata.

| Column              | Type     | Description                          |
|---------------------|----------|--------------------------------------|
| id                  | INTEGER  | Primary key (auto-increment)         |
| invocation_id       | TEXT     | Unique UUID for this invocation      |
| timestamp           | DATETIME | When invocation occurred (UTC)       |
| agent_name          | TEXT     | Agent making request (nullable)      |
| tool_name           | TEXT     | Tool used (claude-code, cursor, etc.)|
| model_name          | TEXT     | Model used (claude-3.5-sonnet, etc.) |
| prompt_tokens       | INTEGER  | Input token count                    |
| completion_tokens   | INTEGER  | Output token count                   |
| total_tokens        | INTEGER  | Sum of input + output                |
| cost_usd            | REAL     | Cost in USD                          |
| latency_ms          | INTEGER  | Execution time (milliseconds)        |
| status              | TEXT     | success, error, timeout              |
| error_message       | TEXT     | Error details (if status=error)      |
| privacy_level       | TEXT     | metadata, full, none                 |

### `daily_costs` Table
Pre-aggregated daily statistics for fast dashboard queries.

| Column              | Type     | Description                          |
|---------------------|----------|--------------------------------------|
| date                | DATE     | Date of aggregation                  |
| agent_name          | TEXT     | Agent name (nullable)                |
| tool_name           | TEXT     | Tool name                            |
| model_name          | TEXT     | Model name                           |
| invocations         | INTEGER  | Number of invocations                |
| total_tokens        | INTEGER  | Sum of all tokens                    |
| total_cost_usd      | REAL     | Sum of all costs (USD)               |

**Primary Key:** (date, agent_name, tool_name, model_name)

## Query Examples

### SQL Queries

```sql
-- Total cost by agent (last 7 days)
SELECT 
    agent_name,
    SUM(total_cost_usd) as total_cost,
    SUM(invocations) as total_invocations
FROM daily_costs
WHERE date >= date('now', '-7 days')
GROUP BY agent_name
ORDER BY total_cost DESC;

-- Error rate by tool
SELECT 
    tool_name,
    COUNT(*) as total,
    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors,
    ROUND(SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as error_rate_pct
FROM invocations
WHERE timestamp >= datetime('now', '-7 days')
GROUP BY tool_name;

-- Average latency by model
SELECT 
    model_name,
    COUNT(*) as invocations,
    ROUND(AVG(latency_ms), 0) as avg_latency_ms,
    MIN(latency_ms) as min_latency_ms,
    MAX(latency_ms) as max_latency_ms
FROM invocations
WHERE status = 'success'
  AND timestamp >= datetime('now', '-7 days')
GROUP BY model_name
ORDER BY avg_latency_ms;

-- Most expensive invocations (top 10)
SELECT 
    invocation_id,
    agent_name,
    tool_name,
    model_name,
    total_tokens,
    cost_usd,
    timestamp
FROM invocations
WHERE timestamp >= datetime('now', '-7 days')
ORDER BY cost_usd DESC
LIMIT 10;
```

### Python API

```python
# Get all invocations for an agent
invocations = logger.get_invocations(
    agent_name="backend-dev",
    limit=100
)

# Get only errors
errors = logger.get_invocations(
    status="error",
    limit=50
)

# Get invocations by tool
tool_invocations = logger.get_invocations(
    tool_name="claude-code",
    limit=100
)

# Get statistics for specific agent
stats = logger.get_statistics(
    agent_name="backend-dev",
    days=30
)
```

## Performance

### Write Performance
- **Overhead per invocation:** <10ms
- **Throughput:** ~100-500 invocations/second (single thread)
- **Storage:** ~500-1000 bytes per invocation (metadata mode)

### Query Performance
- **Daily aggregations:** O(1) - single row lookup
- **Time-series queries:** O(log n) with timestamp index
- **Statistics:** O(n) with optimized WHERE clauses

### Storage Estimates
- 10,000 invocations ≈ 5-10 MB
- 100,000 invocations ≈ 50-100 MB
- Daily aggregates: ~1 KB per day (negligible)

## Privacy & Security

### Metadata Mode (Default)
**What is logged:**
- Token counts (input, output, total)
- Costs (USD)
- Latency (milliseconds)
- Status (success/error)
- Error messages (if applicable)
- Agent, tool, model names

**What is NOT logged:**
- Prompts
- Responses
- User data
- API keys
- Sensitive content

### Full Mode (Future)
**Reserved for audit trail use cases.**
- Logs prompts and responses in addition to metadata
- Requires explicit opt-in
- Subject to retention policies

### None Mode
**Disables all telemetry logging.**

## Testing

Run the test suite:

```bash
# All telemetry tests
pytest tests/unit/telemetry/ tests/integration/telemetry/ -v

# With coverage
pytest tests/unit/telemetry/ tests/integration/telemetry/ --cov=src/llm_service/telemetry --cov-report=term-missing

# Quick smoke test
pytest tests/unit/telemetry/test_logger.py::test_schema_initialization -v
```

**Test Coverage:** 99% (41 tests passing)

## Known Limitations

1. **SQLite concurrency:** Single-file database with thread locking
2. **Retention not enforced:** `retention_days` config parameter not yet implemented
3. **No distributed support:** Not suitable for multi-process deployments
4. **Python 3.12 warnings:** Deprecation warnings for datetime.utcnow() (cosmetic only)

## Roadmap

### M3 Batch 3.2: Integration
- [ ] Integrate with routing engine
- [ ] Implement budget enforcement
- [ ] Add cost pre-estimation

### M3 Batch 3.3: Retention
- [ ] Implement retention_days enforcement
- [ ] Add database vacuum/optimization
- [ ] Export historical data to archive

### M4: Production Hardening
- [ ] PostgreSQL backend option
- [ ] Connection pooling
- [ ] Distributed tracing correlation
- [ ] Prometheus metrics export

## API Reference

### `TelemetryLogger`

**Constructor:**
```python
TelemetryLogger(db_path: Path, privacy_level: str = "metadata")
```

**Methods:**
- `log_invocation(record: InvocationRecord)` - Log an invocation
- `get_daily_costs(start_date, end_date, agent_name)` - Query daily aggregates
- `get_invocations(start_date, end_date, agent_name, tool_name, status, limit)` - Query invocations
- `get_statistics(agent_name, days)` - Get usage statistics

### `InvocationRecord`

**Dataclass:**
```python
@dataclass
class InvocationRecord:
    invocation_id: str
    agent_name: Optional[str]
    tool_name: str
    model_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: int
    status: str  # success, error, timeout
    error_message: Optional[str] = None
    privacy_level: str = "metadata"
    timestamp: Optional[datetime] = None
```

## Support

- **Documentation:** See `work/telemetry/implementation_log.md`
- **Examples:** See `tests/integration/telemetry/test_end_to_end.py`
- **Configuration:** See `config/telemetry.yaml.example`

## License

Part of the LLM Service Layer - see project LICENSE.
