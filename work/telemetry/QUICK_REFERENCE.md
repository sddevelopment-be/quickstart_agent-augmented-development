# Telemetry Module - Quick Reference Card

## Import
```python
from llm_service.telemetry import TelemetryLogger, InvocationRecord
from llm_service.config.schemas import TelemetryConfig
```

## Initialize
```python
from pathlib import Path

logger = TelemetryLogger(
    db_path=Path.home() / ".llm-service" / "telemetry.db",
    privacy_level="metadata"
)
```

## Log Invocation
```python
import uuid
import time

invocation_id = str(uuid.uuid4())
start = time.time()

# ... execute LLM request ...

record = InvocationRecord(
    invocation_id=invocation_id,
    agent_name="backend-dev",
    tool_name="claude-code",
    model_name="claude-3.5-sonnet",
    prompt_tokens=100,
    completion_tokens=200,
    total_tokens=300,
    cost_usd=0.015,
    latency_ms=int((time.time() - start) * 1000),
    status="success"  # or "error", "timeout"
)

logger.log_invocation(record)
```

## Query Costs
```python
from datetime import date, timedelta

# Daily costs
costs = logger.get_daily_costs(
    start_date=date.today() - timedelta(days=7),
    end_date=date.today(),
    agent_name="backend-dev"
)

for cost in costs:
    print(f"{cost['date']}: ${cost['total_cost_usd']:.3f}")
```

## Query Invocations
```python
# Get recent invocations
invocations = logger.get_invocations(
    agent_name="backend-dev",
    tool_name="claude-code",
    status="success",
    limit=100
)

# Get errors only
errors = logger.get_invocations(status="error", limit=50)
```

## Get Statistics
```python
# Last 7 days
stats = logger.get_statistics(agent_name="backend-dev", days=7)

print(f"Total invocations: {stats['total_invocations']}")
print(f"Total cost: ${stats['total_cost_usd']:.2f}")
print(f"Success rate: {stats['success_rate']*100:.1f}%")
print(f"Avg latency: {stats['avg_latency_ms']:.0f}ms")
print(f"Error count: {stats['error_count']}")
```

## Configuration (config/telemetry.yaml)
```yaml
enabled: true
db_path: "~/.llm-service/telemetry.db"
privacy_level: "metadata"  # metadata, full, none
retention_days: 30
```

## Direct SQL Queries
```python
import sqlite3

with sqlite3.connect(logger.db_path) as conn:
    # Cost by agent
    cursor = conn.execute("""
        SELECT agent_name, SUM(total_cost_usd) as cost
        FROM daily_costs
        WHERE date >= date('now', '-7 days')
        GROUP BY agent_name
        ORDER BY cost DESC
    """)
    
    for row in cursor:
        print(f"{row[0]}: ${row[1]:.2f}")
```

## Files Created
```
src/llm_service/telemetry/
├── __init__.py              # Module exports
├── logger.py                # Main implementation
├── schema.sql               # Database schema
└── README.md                # Full documentation

config/
└── telemetry.yaml.example   # Configuration template

tests/
├── unit/telemetry/
│   ├── test_logger.py       # 18 unit tests
│   └── test_queries.py      # 15 query tests
└── integration/telemetry/
    └── test_end_to_end.py   # 8 integration tests

work/telemetry/
├── implementation_log.md    # Technical details
└── COMPLETION_SUMMARY.md    # Final report
```

## Test Coverage
- **41 tests passing** (100%)
- **99% code coverage**
- **0.75 seconds** execution time

## Key Metrics
- Write overhead: <10ms per invocation
- Storage: ~500-1000 bytes per invocation
- Throughput: 100-500 invocations/second
- Privacy: Metadata-only (no prompts/responses)

## Next Steps (M3 Batch 3.2)
1. Integrate with routing engine
2. Add cost calculation from models.yaml
3. Implement budget enforcement
4. Add cost pre-estimation

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Agent:** Backend Benny  
**Date:** 2025-02-05
