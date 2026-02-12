"""
Telemetry API for Dashboard - Query cost/metrics from SQLite.

Provides read-only access to telemetry database for dashboard visualization.
"""

import logging
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class TelemetryAPI:
    """
    API for querying telemetry data from SQLite database.

    Provides:
        - Cost aggregation (total, today, month)
        - Model usage statistics
        - Cost trends over time
        - Active operation metrics

    Note: This is READ-ONLY. Write operations handled by TelemetryLogger.
    """

    def __init__(self, db_path: str | Path, socketio: Any | None = None):
        """
        Initialize telemetry API.

        Args:
            db_path: Path to SQLite telemetry database
            socketio: SocketIO instance for event emission (optional)
        """
        self.db_path = Path(db_path)
        self.socketio = socketio

        # Ensure database exists
        if not self.db_path.exists():
            logger.warning(f"Telemetry database not found: {db_path}")
            # Create empty database with schema
            self._init_empty_db()

    def _init_empty_db(self) -> None:
        """Initialize empty database with schema."""
        schema_path = Path(__file__).parent.parent / "telemetry" / "schema.sql"

        if schema_path.exists():
            with open(schema_path) as f:
                schema = f.read()

            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(schema)
        else:
            logger.error(f"Schema file not found: {schema_path}")

    def get_total_cost(self) -> float:
        """
        Get total cost across all invocations.

        Returns:
            Total cost in USD
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT COALESCE(SUM(cost_usd), 0.0) FROM invocations
            """)
            return cursor.fetchone()[0]

    def get_today_cost(self) -> float:
        """
        Get cost for today (UTC).

        Returns:
            Today's cost in USD
        """
        today = datetime.now(timezone.utc).date()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT COALESCE(SUM(cost_usd), 0.0)
                FROM invocations
                WHERE DATE(timestamp) = ?
            """,
                (today.isoformat(),),
            )
            return cursor.fetchone()[0]

    def get_monthly_cost(self) -> float:
        """
        Get cost for current month (UTC).

        Returns:
            Current month's cost in USD
        """
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT COALESCE(SUM(cost_usd), 0.0)
                FROM invocations
                WHERE timestamp >= ?
            """,
                (month_start.isoformat(),),
            )
            return cursor.fetchone()[0]

    def get_model_usage_stats(self) -> list[dict[str, Any]]:
        """
        Get usage statistics grouped by model.

        Returns:
            List of dicts with model_name, invocations, total_tokens, total_cost_usd
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT
                    model_name,
                    COUNT(*) as invocations,
                    SUM(total_tokens) as total_tokens,
                    SUM(cost_usd) as total_cost_usd
                FROM invocations
                GROUP BY model_name
                ORDER BY total_cost_usd DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

    def get_cost_trend(self, days: int = 7) -> list[dict[str, Any]]:
        """
        Get cost trend over recent days.

        Args:
            days: Number of days to include (default: 7)

        Returns:
            List of dicts with date and cost_usd for each day
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT
                    DATE(timestamp) as date,
                    SUM(cost_usd) as cost_usd
                FROM invocations
                WHERE timestamp >= ?
                GROUP BY DATE(timestamp)
                ORDER BY date ASC
            """,
                (cutoff.isoformat(),),
            )

            return [dict(row) for row in cursor.fetchall()]

    def get_active_operations(self) -> list[dict[str, Any]]:
        """
        Get currently active or recent operations.

        For now, returns invocations from the last 5 minutes.
        Future: Could integrate with real-time operation tracking.

        Returns:
            List of recent invocation records
        """
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=5)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT
                    invocation_id,
                    timestamp,
                    agent_name,
                    tool_name,
                    model_name,
                    total_tokens,
                    cost_usd,
                    latency_ms,
                    status
                FROM invocations
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT 10
            """,
                (cutoff.isoformat(),),
            )

            return [dict(row) for row in cursor.fetchall()]

    def to_dashboard_dict(self) -> dict[str, Any]:
        """
        Convert telemetry data to dashboard-friendly dictionary.

        Returns:
            Dictionary with all dashboard metrics
        """
        return {
            "costs": {
                "total": self.get_total_cost(),
                "today": self.get_today_cost(),
                "month": self.get_monthly_cost(),
            },
            "models": self.get_model_usage_stats(),
            "trends": self.get_cost_trend(days=30),
            "active_operations": self.get_active_operations(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def emit_cost_update(self) -> None:
        """
        Emit cost update event via WebSocket.

        Sends current cost metrics to all connected dashboard clients.
        """
        if not self.socketio:
            logger.warning("SocketIO not configured, cannot emit cost update")
            return

        data = self.to_dashboard_dict()

        self.socketio.emit("cost.update", data, namespace="/dashboard")
        logger.debug("Cost update emitted to dashboard clients")

    def emit_telemetry_update(self, invocation_data: dict[str, Any]) -> None:
        """
        Emit telemetry update for a specific invocation.

        Args:
            invocation_data: Invocation record data to emit
        """
        if not self.socketio:
            return

        self.socketio.emit(
            "telemetry.update",
            {
                "invocation": invocation_data,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            namespace="/dashboard",
        )


def create_telemetry_api(
    db_path: str | Path = "telemetry.db", socketio: Any | None = None
) -> TelemetryAPI:
    """
    Convenience function to create TelemetryAPI instance.

    Args:
        db_path: Path to telemetry database
        socketio: SocketIO instance for event emission

    Returns:
        Configured TelemetryAPI instance

    Example:
        >>> from llm_service.dashboard.app import create_app
        >>> from llm_service.dashboard.telemetry_api import create_telemetry_api
        >>> app, socketio = create_app()
        >>> telemetry = create_telemetry_api('telemetry.db', socketio)
        >>> cost = telemetry.get_total_cost()
    """
    return TelemetryAPI(db_path=db_path, socketio=socketio)
