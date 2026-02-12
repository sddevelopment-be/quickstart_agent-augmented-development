"""
TelemetryLogger - Core telemetry logging for LLM Service Layer.

Provides SQLite-backed logging of LLM invocations with:
- Token usage tracking
- Cost calculation
- Performance metrics (latency)
- Error tracking
- Privacy controls (metadata vs. full logging)
- Daily cost aggregation

Thread-safe for concurrent invocations.
"""

import sqlite3
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class InvocationRecord:
    """
    Record of a single LLM invocation.

    Attributes:
        invocation_id: Unique identifier for this invocation
        agent_name: Name of agent making the request (optional)
        tool_name: Tool used (claude-code, cursor, etc.)
        model_name: Model used (claude-3.5-sonnet, gpt-4, etc.)
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens
        total_tokens: Sum of prompt + completion tokens
        cost_usd: Cost in USD
        latency_ms: Execution time in milliseconds
        status: success, error, timeout
        error_message: Error details if status != success
        privacy_level: metadata, full, none (default: metadata)
        timestamp: When invocation occurred (defaults to now)
    """

    invocation_id: str
    agent_name: str | None
    tool_name: str
    model_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: int
    status: str  # success, error, timeout
    error_message: str | None = None
    privacy_level: str = "metadata"  # metadata, full, none
    timestamp: datetime | None = None


class TelemetryLogger:
    """
    Logs LLM invocations to SQLite database.

    Features:
    - Automatic schema initialization
    - Daily cost aggregation
    - Privacy controls (metadata-only vs. full logging)
    - Thread-safe operations
    - Efficient bulk operations

    Example:
        >>> logger = TelemetryLogger(Path("telemetry.db"))
        >>> record = InvocationRecord(
        ...     invocation_id="abc-123",
        ...     agent_name="backend-dev",
        ...     tool_name="claude-code",
        ...     model_name="claude-3.5-sonnet",
        ...     prompt_tokens=100,
        ...     completion_tokens=200,
        ...     total_tokens=300,
        ...     cost_usd=0.015,
        ...     latency_ms=1500,
        ...     status="success"
        ... )
        >>> logger.log_invocation(record)
    """

    def __init__(self, db_path: Path, privacy_level: str = "metadata"):
        """
        Initialize telemetry logger.

        Args:
            db_path: Path to SQLite database file
            privacy_level: Default privacy level (metadata, full, none)
        """
        self.db_path = Path(db_path)
        self.privacy_level = privacy_level
        self._lock = threading.Lock()

        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize schema
        self._ensure_schema()

    def _ensure_schema(self):
        """Initialize database schema if not exists."""
        schema_path = Path(__file__).parent / "schema.sql"

        if not schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {schema_path}. "
                "Ensure schema.sql is in the same directory as logger.py"
            )

        with open(schema_path) as f:
            schema = f.read()

        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema)

    def log_invocation(self, record: InvocationRecord):
        """
        Log an invocation to the database.

        Args:
            record: InvocationRecord with invocation details

        Raises:
            sqlite3.IntegrityError: If invocation_id already exists
        """
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                # Use record timestamp or current time
                timestamp = record.timestamp or datetime.now(timezone.utc)

                # Insert invocation
                conn.execute(
                    """
                    INSERT INTO invocations (
                        invocation_id, timestamp, agent_name, tool_name, model_name,
                        prompt_tokens, completion_tokens, total_tokens, cost_usd,
                        latency_ms, status, error_message, privacy_level
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        record.invocation_id,
                        timestamp,
                        record.agent_name,
                        record.tool_name,
                        record.model_name,
                        record.prompt_tokens,
                        record.completion_tokens,
                        record.total_tokens,
                        record.cost_usd,
                        record.latency_ms,
                        record.status,
                        record.error_message,
                        record.privacy_level,
                    ),
                )

                # Update daily aggregates
                self._update_daily_costs(conn, record, timestamp)

    def _update_daily_costs(
        self, conn: sqlite3.Connection, record: InvocationRecord, timestamp: datetime
    ):
        """
        Update daily cost aggregates.

        Args:
            conn: Active database connection
            record: InvocationRecord being logged
            timestamp: Timestamp for the invocation
        """
        date = timestamp.date()

        # Use INSERT OR REPLACE pattern for SQLite (UPSERT)
        conn.execute(
            """
            INSERT INTO daily_costs (
                date, agent_name, tool_name, model_name,
                invocations, total_tokens, total_cost_usd
            ) VALUES (?, ?, ?, ?, 1, ?, ?)
            ON CONFLICT(date, agent_name, tool_name, model_name) DO UPDATE SET
                invocations = invocations + 1,
                total_tokens = total_tokens + ?,
                total_cost_usd = total_cost_usd + ?
        """,
            (
                date,
                record.agent_name,
                record.tool_name,
                record.model_name,
                record.total_tokens,
                record.cost_usd,
                record.total_tokens,
                record.cost_usd,
            ),
        )

    def get_daily_costs(self, start_date=None, end_date=None, agent_name=None):
        """
        Query daily cost aggregates.

        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
            agent_name: Optional agent name filter

        Returns:
            List of daily cost records as dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            query = "SELECT * FROM daily_costs WHERE 1=1"
            params = []

            if start_date:
                query += " AND date >= ?"
                params.append(start_date)

            if end_date:
                query += " AND date <= ?"
                params.append(end_date)

            if agent_name:
                query += " AND agent_name = ?"
                params.append(agent_name)

            query += " ORDER BY date DESC"

            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_invocations(
        self,
        start_date=None,
        end_date=None,
        agent_name=None,
        tool_name=None,
        status=None,
        limit=100,
    ):
        """
        Query individual invocations.

        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
            agent_name: Optional agent name filter
            tool_name: Optional tool name filter
            status: Optional status filter
            limit: Maximum number of results (default: 100)

        Returns:
            List of invocation records as dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            query = "SELECT * FROM invocations WHERE 1=1"
            params = []

            if start_date:
                query += " AND DATE(timestamp) >= ?"
                params.append(start_date)

            if end_date:
                query += " AND DATE(timestamp) <= ?"
                params.append(end_date)

            if agent_name:
                query += " AND agent_name = ?"
                params.append(agent_name)

            if tool_name:
                query += " AND tool_name = ?"
                params.append(tool_name)

            if status:
                query += " AND status = ?"
                params.append(status)

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_statistics(self, agent_name=None, days=7):
        """
        Get usage statistics for the specified period.

        Args:
            agent_name: Optional agent name filter
            days: Number of days to include (default: 7)

        Returns:
            Dictionary with statistics:
            - total_invocations
            - total_cost_usd
            - total_tokens
            - success_rate
            - avg_latency_ms
            - error_count
        """
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT
                    COUNT(*) as total_invocations,
                    SUM(cost_usd) as total_cost_usd,
                    SUM(total_tokens) as total_tokens,
                    AVG(CASE WHEN status = 'success' THEN 1.0 ELSE 0.0 END) as success_rate,
                    AVG(latency_ms) as avg_latency_ms,
                    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as error_count
                FROM invocations
                WHERE timestamp >= datetime('now', '-' || ? || ' days')
            """
            params = [days]

            if agent_name:
                query += " AND agent_name = ?"
                params.append(agent_name)

            cursor = conn.execute(query, params)
            row = cursor.fetchone()

            return {
                "total_invocations": row[0] or 0,
                "total_cost_usd": row[1] or 0.0,
                "total_tokens": row[2] or 0,
                "success_rate": row[3] or 0.0,
                "avg_latency_ms": row[4] or 0.0,
                "error_count": row[5] or 0,
            }
