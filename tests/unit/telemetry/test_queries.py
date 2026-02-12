"""
Tests for TelemetryLogger query methods.
"""

from datetime import datetime, timedelta, timezone

import pytest

from llm_service.telemetry.logger import InvocationRecord, TelemetryLogger


@pytest.fixture
def temp_db(tmp_path):
    """Create temporary database."""
    return tmp_path / "test_queries.db"


@pytest.fixture
def logger_with_data(temp_db):
    """Create logger with sample data."""
    logger = TelemetryLogger(temp_db)

    # Add sample invocations
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    sample_data = [
        (
            "inv-001",
            "agent-a",
            "claude-code",
            "claude-3.5-sonnet",
            100,
            200,
            0.015,
            1500,
            "success",
            today,
        ),
        (
            "inv-002",
            "agent-a",
            "cursor",
            "gpt-4-turbo",
            150,
            250,
            0.020,
            1800,
            "success",
            today,
        ),
        (
            "inv-003",
            "agent-b",
            "claude-code",
            "claude-3.5-sonnet",
            120,
            220,
            0.016,
            1600,
            "error",
            today,
        ),
        (
            "inv-004",
            "agent-a",
            "claude-code",
            "claude-3.5-sonnet",
            110,
            210,
            0.015,
            1550,
            "success",
            yesterday,
        ),
    ]

    for (
        inv_id,
        agent,
        tool,
        model,
        prompt_tok,
        compl_tok,
        cost,
        latency,
        status,
        date,
    ) in sample_data:
        record = InvocationRecord(
            invocation_id=inv_id,
            agent_name=agent,
            tool_name=tool,
            model_name=model,
            prompt_tokens=prompt_tok,
            completion_tokens=compl_tok,
            total_tokens=prompt_tok + compl_tok,
            cost_usd=cost,
            latency_ms=latency,
            status=status,
            timestamp=datetime.combine(date, datetime.min.time()),
        )
        logger.log_invocation(record)

    return logger


def test_get_daily_costs_no_filters(logger_with_data):
    """Test getting all daily costs without filters."""
    costs = logger_with_data.get_daily_costs()

    assert len(costs) > 0
    assert all("date" in c for c in costs)
    assert all("total_cost_usd" in c for c in costs)


def test_get_daily_costs_with_agent_filter(logger_with_data):
    """Test filtering daily costs by agent."""
    costs = logger_with_data.get_daily_costs(agent_name="agent-a")

    assert len(costs) > 0
    assert all(c["agent_name"] == "agent-a" for c in costs)


def test_get_daily_costs_with_date_range(logger_with_data):
    """Test filtering daily costs by date range."""
    today = datetime.now(timezone.utc).date()
    costs = logger_with_data.get_daily_costs(start_date=today, end_date=today)

    assert len(costs) > 0
    for cost in costs:
        cost_date = datetime.fromisoformat(str(cost["date"])).date()
        assert cost_date == today


def test_get_invocations_no_filters(logger_with_data):
    """Test getting invocations without filters."""
    invocations = logger_with_data.get_invocations()

    assert len(invocations) == 4  # All sample data
    assert all("invocation_id" in inv for inv in invocations)


def test_get_invocations_with_agent_filter(logger_with_data):
    """Test filtering invocations by agent."""
    invocations = logger_with_data.get_invocations(agent_name="agent-a")

    assert len(invocations) == 3  # agent-a has 3 invocations
    assert all(inv["agent_name"] == "agent-a" for inv in invocations)


def test_get_invocations_with_tool_filter(logger_with_data):
    """Test filtering invocations by tool."""
    invocations = logger_with_data.get_invocations(tool_name="claude-code")

    assert len(invocations) == 3  # 3 invocations use claude-code
    assert all(inv["tool_name"] == "claude-code" for inv in invocations)


def test_get_invocations_with_status_filter(logger_with_data):
    """Test filtering invocations by status."""
    invocations = logger_with_data.get_invocations(status="error")

    assert len(invocations) == 1  # Only one error
    assert invocations[0]["status"] == "error"


def test_get_invocations_with_limit(logger_with_data):
    """Test limiting number of invocations returned."""
    invocations = logger_with_data.get_invocations(limit=2)

    assert len(invocations) == 2


def test_get_invocations_with_date_filter(logger_with_data):
    """Test filtering invocations by date."""
    today = datetime.now(timezone.utc).date()
    invocations = logger_with_data.get_invocations(start_date=today, end_date=today)

    assert len(invocations) == 3  # 3 invocations today


def test_get_statistics_all_agents(logger_with_data):
    """Test getting statistics for all agents."""
    stats = logger_with_data.get_statistics(days=7)

    assert stats["total_invocations"] == 4
    assert stats["total_cost_usd"] > 0
    assert stats["total_tokens"] > 0
    assert 0 <= stats["success_rate"] <= 1.0
    assert stats["avg_latency_ms"] > 0
    assert stats["error_count"] == 1  # One error in sample data


def test_get_statistics_specific_agent(logger_with_data):
    """Test getting statistics for specific agent."""
    stats = logger_with_data.get_statistics(agent_name="agent-a", days=7)

    assert stats["total_invocations"] == 3  # agent-a has 3 invocations
    assert stats["error_count"] == 0  # agent-a has no errors
    assert stats["success_rate"] == 1.0  # All successful


def test_get_statistics_different_time_ranges(logger_with_data):
    """Test getting statistics for different time ranges."""
    # Last 1 day (only today's invocations)
    stats_1day = logger_with_data.get_statistics(days=1)

    # Last 7 days (all invocations)
    stats_7days = logger_with_data.get_statistics(days=7)

    # 7 days should have more invocations (includes yesterday)
    assert stats_7days["total_invocations"] >= stats_1day["total_invocations"]


def test_telemetry_config_validation():
    """Test TelemetryConfig validation from schemas."""
    from llm_service.config.schemas import TelemetryConfig

    # Valid metadata config
    config = TelemetryConfig(
        enabled=True,
        db_path="~/.llm-service/telemetry.db",
        privacy_level="metadata",
        retention_days=30,
    )
    assert config.enabled is True
    assert config.privacy_level == "metadata"

    # Valid full config
    config_full = TelemetryConfig(
        enabled=True, db_path="/tmp/test.db", privacy_level="full", retention_days=7
    )
    assert config_full.privacy_level == "full"

    # Valid none config
    config_none = TelemetryConfig(
        enabled=False, db_path="/tmp/test.db", privacy_level="none", retention_days=0
    )
    assert config_none.privacy_level == "none"


def test_telemetry_config_invalid_privacy_level():
    """Test TelemetryConfig rejects invalid privacy level."""
    from pydantic import ValidationError

    from llm_service.config.schemas import TelemetryConfig

    with pytest.raises(ValidationError):
        TelemetryConfig(
            enabled=True,
            db_path="/tmp/test.db",
            privacy_level="invalid",  # Invalid privacy level
            retention_days=30,
        )


def test_telemetry_config_path_expansion():
    """Test TelemetryConfig expands ~ in paths."""
    from llm_service.config.schemas import TelemetryConfig

    config = TelemetryConfig(
        enabled=True,
        db_path="~/.llm-service/telemetry.db",
        privacy_level="metadata",
        retention_days=30,
    )

    expanded_path = config.get_db_path()
    assert "~" not in str(expanded_path)
    assert ".llm-service" in str(expanded_path)
