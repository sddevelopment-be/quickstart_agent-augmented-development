"""
Unit tests for TelemetryLogger.

Test-Driven Development: These tests define the expected behavior
before implementation exists. Expected to fail initially (RED phase).
"""

import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from llm_service.telemetry.logger import InvocationRecord, TelemetryLogger


@pytest.fixture
def temp_db(tmp_path):
    """Create temporary database."""
    return tmp_path / "test_telemetry.db"


@pytest.fixture
def logger(temp_db):
    """Create telemetry logger."""
    return TelemetryLogger(temp_db)


def test_schema_initialization(temp_db, logger):
    """Test database schema is created on initialization."""
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}

    assert "invocations" in tables, "invocations table should exist"
    assert "daily_costs" in tables, "daily_costs table should exist"


def test_invocations_table_structure(temp_db, logger):
    """Test invocations table has correct columns."""
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.execute("PRAGMA table_info(invocations)")
        columns = {row[1] for row in cursor.fetchall()}

    required_columns = {
        "id",
        "invocation_id",
        "timestamp",
        "agent_name",
        "tool_name",
        "model_name",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "cost_usd",
        "latency_ms",
        "status",
        "error_message",
        "privacy_level",
    }
    assert required_columns.issubset(
        columns
    ), f"Missing columns: {required_columns - columns}"


def test_daily_costs_table_structure(temp_db, logger):
    """Test daily_costs table has correct columns."""
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.execute("PRAGMA table_info(daily_costs)")
        columns = {row[1] for row in cursor.fetchall()}

    required_columns = {
        "date",
        "agent_name",
        "tool_name",
        "model_name",
        "invocations",
        "total_tokens",
        "total_cost_usd",
    }
    assert required_columns.issubset(
        columns
    ), f"Missing columns: {required_columns - columns}"


def test_indexes_created(temp_db, logger):
    """Test that indexes are created for common queries."""
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = {row[0] for row in cursor.fetchall()}

    expected_indexes = {
        "idx_invocations_timestamp",
        "idx_invocations_agent",
        "idx_invocations_tool",
        "idx_invocations_model",
        "idx_invocations_status",
        "idx_daily_costs_date",
    }

    assert expected_indexes.issubset(
        indexes
    ), f"Missing indexes: {expected_indexes - indexes}"


def test_log_invocation_success(logger):
    """Test logging a successful invocation."""
    record = InvocationRecord(
        invocation_id="test-123",
        agent_name="test-agent",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success",
    )

    logger.log_invocation(record)

    # Verify logged
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            "SELECT * FROM invocations WHERE invocation_id = ?", ("test-123",)
        )
        row = cursor.fetchone()

    assert row is not None, "Invocation should be logged"
    # Get column names
    columns = [desc[0] for desc in cursor.description]
    row_dict = dict(zip(columns, row))

    assert row_dict["agent_name"] == "test-agent"
    assert row_dict["tool_name"] == "claude-code"
    assert row_dict["model_name"] == "claude-3.5-sonnet"
    assert row_dict["prompt_tokens"] == 100
    assert row_dict["completion_tokens"] == 200
    assert row_dict["total_tokens"] == 300
    assert abs(row_dict["cost_usd"] - 0.015) < 0.0001
    assert row_dict["latency_ms"] == 1500
    assert row_dict["status"] == "success"


def test_log_invocation_with_error(logger):
    """Test logging an invocation with error."""
    record = InvocationRecord(
        invocation_id="error-123",
        agent_name="test-agent",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=0,
        completion_tokens=0,
        total_tokens=0,
        cost_usd=0.0,
        latency_ms=500,
        status="error",
        error_message="Connection timeout",
    )

    logger.log_invocation(record)

    # Verify error logged
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            "SELECT status, error_message FROM invocations WHERE invocation_id = ?",
            ("error-123",),
        )
        row = cursor.fetchone()

    assert row is not None
    assert row[0] == "error"
    assert "timeout" in row[1].lower()


def test_daily_cost_aggregation_single_invocation(logger):
    """Test daily costs are aggregated for a single invocation."""
    record = InvocationRecord(
        invocation_id="agg-test-1",
        agent_name="test-agent",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success",
        timestamp=datetime.now(timezone.utc),
    )

    logger.log_invocation(record)

    # Check aggregation
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("""
            SELECT invocations, total_tokens, total_cost_usd
            FROM daily_costs
            WHERE agent_name = 'test-agent'
            AND tool_name = 'claude-code'
            AND model_name = 'claude-3.5-sonnet'
        """)
        row = cursor.fetchone()

    assert row is not None
    assert row[0] == 1  # 1 invocation
    assert row[1] == 300  # 300 tokens
    assert abs(row[2] - 0.015) < 0.0001  # 0.015 USD


def test_daily_cost_aggregation_multiple_invocations(logger):
    """Test daily costs aggregate correctly across multiple invocations."""
    # Log three invocations
    for i in range(3):
        record = InvocationRecord(
            invocation_id=f"multi-test-{i}",
            agent_name="test-agent",
            tool_name="claude-code",
            model_name="claude-3.5-sonnet",
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300,
            cost_usd=0.015,
            latency_ms=1500,
            status="success",
            timestamp=datetime.now(timezone.utc),
        )
        logger.log_invocation(record)

    # Check aggregation
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("""
            SELECT invocations, total_tokens, total_cost_usd
            FROM daily_costs
            WHERE agent_name = 'test-agent'
        """)
        row = cursor.fetchone()

    assert row is not None
    assert row[0] == 3  # 3 invocations
    assert row[1] == 900  # 3 * 300 tokens
    assert abs(row[2] - 0.045) < 0.001  # 3 * 0.015 USD


def test_daily_cost_aggregation_different_agents(logger):
    """Test daily costs are separated by agent."""
    # Log invocations for two different agents
    for agent in ["agent-a", "agent-b"]:
        record = InvocationRecord(
            invocation_id=f"{agent}-test",
            agent_name=agent,
            tool_name="claude-code",
            model_name="claude-3.5-sonnet",
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300,
            cost_usd=0.015,
            latency_ms=1500,
            status="success",
        )
        logger.log_invocation(record)

    # Check each agent has separate aggregation
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("""
            SELECT agent_name, invocations
            FROM daily_costs
            ORDER BY agent_name
        """)
        rows = cursor.fetchall()

    assert len(rows) == 2
    assert rows[0][0] == "agent-a"
    assert rows[0][1] == 1
    assert rows[1][0] == "agent-b"
    assert rows[1][1] == 1


def test_daily_cost_aggregation_different_days(logger):
    """Test daily costs are separated by date."""
    today = datetime.now(timezone.utc)
    yesterday = today - timedelta(days=1)

    # Log invocations on different days
    for day, timestamp in [("today", today), ("yesterday", yesterday)]:
        record = InvocationRecord(
            invocation_id=f"{day}-test",
            agent_name="test-agent",
            tool_name="claude-code",
            model_name="claude-3.5-sonnet",
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300,
            cost_usd=0.015,
            latency_ms=1500,
            status="success",
            timestamp=timestamp,
        )
        logger.log_invocation(record)

    # Check we have two separate day records
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("SELECT COUNT(DISTINCT date) FROM daily_costs")
        count = cursor.fetchone()[0]

    assert count == 2, "Should have records for 2 different days"


def test_privacy_level_metadata(logger):
    """Test privacy level is recorded correctly (metadata mode)."""
    record = InvocationRecord(
        invocation_id="privacy-metadata-test",
        agent_name="test-agent",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success",
        privacy_level="metadata",
    )

    logger.log_invocation(record)

    # Verify privacy level
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            "SELECT privacy_level FROM invocations WHERE invocation_id = ?",
            ("privacy-metadata-test",),
        )
        row = cursor.fetchone()

    assert row[0] == "metadata"


def test_privacy_level_full(logger):
    """Test privacy level is recorded correctly (full mode)."""
    record = InvocationRecord(
        invocation_id="privacy-full-test",
        agent_name="test-agent",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success",
        privacy_level="full",
    )

    logger.log_invocation(record)

    # Verify privacy level
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            "SELECT privacy_level FROM invocations WHERE invocation_id = ?",
            ("privacy-full-test",),
        )
        row = cursor.fetchone()

    assert row[0] == "full"


def test_default_privacy_level(logger):
    """Test default privacy level is 'metadata'."""
    record = InvocationRecord(
        invocation_id="privacy-default-test",
        agent_name="test-agent",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success",
        # No privacy_level specified - should default to 'metadata'
    )

    logger.log_invocation(record)

    # Verify privacy level defaults to metadata
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            "SELECT privacy_level FROM invocations WHERE invocation_id = ?",
            ("privacy-default-test",),
        )
        row = cursor.fetchone()

    assert row[0] == "metadata"


def test_optional_agent_name(logger):
    """Test invocation can be logged without agent name."""
    record = InvocationRecord(
        invocation_id="no-agent-test",
        agent_name=None,  # Optional agent
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success",
    )

    logger.log_invocation(record)

    # Verify logged with NULL agent
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            "SELECT agent_name FROM invocations WHERE invocation_id = ?",
            ("no-agent-test",),
        )
        row = cursor.fetchone()

    assert row[0] is None


def test_timestamp_default(logger):
    """Test timestamp defaults to current time if not provided."""
    record = InvocationRecord(
        invocation_id="timestamp-test",
        agent_name="test-agent",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success",
        # No timestamp provided
    )

    before_log = datetime.now(timezone.utc)
    logger.log_invocation(record)
    after_log = datetime.now(timezone.utc)

    # Verify timestamp is within expected range
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            "SELECT timestamp FROM invocations WHERE invocation_id = ?",
            ("timestamp-test",),
        )
        row = cursor.fetchone()

    assert row[0] is not None
    # Parse timestamp from database
    logged_time = datetime.fromisoformat(
        row[0].replace("Z", "+00:00") if "Z" in row[0] else row[0]
    )

    # Should be between before and after log time
    assert before_log <= logged_time <= after_log + timedelta(seconds=1)


def test_unique_invocation_id_constraint(logger):
    """Test that duplicate invocation_id raises an error."""
    record = InvocationRecord(
        invocation_id="duplicate-test",
        agent_name="test-agent",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success",
    )

    # First log should succeed
    logger.log_invocation(record)

    # Second log with same ID should fail
    with pytest.raises(sqlite3.IntegrityError):
        logger.log_invocation(record)


def test_query_invocations_by_agent(logger):
    """Test querying invocations by agent name."""
    # Log invocations for multiple agents
    agents = ["agent-a", "agent-b", "agent-c"]
    for agent in agents:
        for i in range(2):
            record = InvocationRecord(
                invocation_id=f"{agent}-{i}",
                agent_name=agent,
                tool_name="claude-code",
                model_name="claude-3.5-sonnet",
                prompt_tokens=100,
                completion_tokens=200,
                total_tokens=300,
                cost_usd=0.015,
                latency_ms=1500,
                status="success",
            )
            logger.log_invocation(record)

    # Query for specific agent
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            """
            SELECT COUNT(*) FROM invocations WHERE agent_name = ?
        """,
            ("agent-b",),
        )
        count = cursor.fetchone()[0]

    assert count == 2


def test_query_invocations_by_status(logger):
    """Test querying invocations by status."""
    # Log mix of success and error invocations
    statuses = ["success", "success", "error", "success", "error"]
    for i, status in enumerate(statuses):
        record = InvocationRecord(
            invocation_id=f"status-test-{i}",
            agent_name="test-agent",
            tool_name="claude-code",
            model_name="claude-3.5-sonnet",
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300,
            cost_usd=0.015,
            latency_ms=1500,
            status=status,
            error_message="Error occurred" if status == "error" else None,
        )
        logger.log_invocation(record)

    # Query for errors
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute(
            """
            SELECT COUNT(*) FROM invocations WHERE status = ?
        """,
            ("error",),
        )
        error_count = cursor.fetchone()[0]

        cursor = conn.execute(
            """
            SELECT COUNT(*) FROM invocations WHERE status = ?
        """,
            ("success",),
        )
        success_count = cursor.fetchone()[0]

    assert error_count == 2
    assert success_count == 3
