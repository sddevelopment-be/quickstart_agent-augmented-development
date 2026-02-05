"""
Integration tests for telemetry end-to-end functionality.

Tests the complete flow from routing engine through telemetry logging.
"""

import pytest
from pathlib import Path
import sqlite3
from datetime import datetime
import time

from llm_service.telemetry.logger import TelemetryLogger, InvocationRecord


@pytest.fixture
def temp_db(tmp_path):
    """Create temporary database for integration tests."""
    return tmp_path / "integration_telemetry.db"


@pytest.fixture
def logger(temp_db):
    """Create telemetry logger for integration tests."""
    return TelemetryLogger(temp_db)


def test_end_to_end_successful_invocation(logger):
    """
    Test complete flow of a successful invocation being logged.
    
    Simulates what routing engine would do:
    1. Start timing
    2. Execute (simulated)
    3. Calculate costs
    4. Log to telemetry
    5. Verify persistence
    """
    # Simulate routing engine flow
    start_time = time.time()
    invocation_id = "e2e-success-001"
    
    # Simulate successful execution
    time.sleep(0.01)  # Minimal delay
    
    # Calculate metrics
    latency_ms = int((time.time() - start_time) * 1000)
    
    # Log invocation
    record = InvocationRecord(
        invocation_id=invocation_id,
        agent_name="backend-dev",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=150,
        completion_tokens=350,
        total_tokens=500,
        cost_usd=0.025,
        latency_ms=latency_ms,
        status="success"
    )
    
    logger.log_invocation(record)
    
    # Verify complete flow
    with sqlite3.connect(logger.db_path) as conn:
        # Check invocation logged
        cursor = conn.execute("""
            SELECT invocation_id, agent_name, tool_name, model_name, 
                   prompt_tokens, completion_tokens, total_tokens, 
                   cost_usd, status
            FROM invocations 
            WHERE invocation_id = ?
        """, (invocation_id,))
        
        inv_row = cursor.fetchone()
        assert inv_row is not None
        assert inv_row[1] == "backend-dev"
        assert inv_row[8] == "success"
        
        # Check daily aggregation
        cursor = conn.execute("""
            SELECT invocations, total_tokens, total_cost_usd
            FROM daily_costs
            WHERE agent_name = 'backend-dev'
            AND tool_name = 'claude-code'
            AND model_name = 'claude-3.5-sonnet'
        """)
        
        daily_row = cursor.fetchone()
        assert daily_row is not None
        assert daily_row[0] == 1  # 1 invocation
        assert daily_row[1] == 500  # 500 tokens
        assert abs(daily_row[2] - 0.025) < 0.0001  # 0.025 USD


def test_end_to_end_error_invocation(logger):
    """
    Test complete flow of an error invocation being logged.
    
    Simulates routing engine error handling:
    1. Start timing
    2. Execute (fails)
    3. Catch exception
    4. Log error to telemetry
    5. Verify error tracking
    """
    start_time = time.time()
    invocation_id = "e2e-error-001"
    
    # Simulate execution failure
    time.sleep(0.005)
    error_message = "API rate limit exceeded"
    
    # Calculate metrics
    latency_ms = int((time.time() - start_time) * 1000)
    
    # Log error invocation
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
        error_message=error_message
    )
    
    logger.log_invocation(record)
    
    # Verify error tracking
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("""
            SELECT status, error_message, cost_usd
            FROM invocations 
            WHERE invocation_id = ?
        """, (invocation_id,))
        
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == "error"
        assert "rate limit" in row[1].lower()
        assert row[2] == 0.0  # No cost for failed requests


def test_end_to_end_multiple_agents_concurrent(logger):
    """
    Test multiple agents making concurrent invocations.
    
    Simulates production scenario with multiple agents active:
    - Different agents
    - Different tools
    - Different models
    - Verify all tracked correctly
    """
    invocations = [
        {
            "invocation_id": "concurrent-001",
            "agent_name": "backend-dev",
            "tool_name": "claude-code",
            "model_name": "claude-3.5-sonnet",
            "tokens": 500,
            "cost": 0.025
        },
        {
            "invocation_id": "concurrent-002",
            "agent_name": "frontend-dev",
            "tool_name": "cursor",
            "model_name": "gpt-4-turbo",
            "tokens": 800,
            "cost": 0.040
        },
        {
            "invocation_id": "concurrent-003",
            "agent_name": "architect",
            "tool_name": "claude-code",
            "model_name": "claude-opus-20240229",
            "tokens": 1200,
            "cost": 0.060
        },
        {
            "invocation_id": "concurrent-004",
            "agent_name": "backend-dev",
            "tool_name": "claude-code",
            "model_name": "claude-3.5-sonnet",
            "tokens": 400,
            "cost": 0.020
        }
    ]
    
    # Log all invocations
    for inv in invocations:
        record = InvocationRecord(
            invocation_id=inv["invocation_id"],
            agent_name=inv["agent_name"],
            tool_name=inv["tool_name"],
            model_name=inv["model_name"],
            prompt_tokens=inv["tokens"] // 2,
            completion_tokens=inv["tokens"] // 2,
            total_tokens=inv["tokens"],
            cost_usd=inv["cost"],
            latency_ms=1000,
            status="success"
        )
        logger.log_invocation(record)
    
    # Verify all tracked
    with sqlite3.connect(logger.db_path) as conn:
        # Check total invocations
        cursor = conn.execute("SELECT COUNT(*) FROM invocations")
        total_count = cursor.fetchone()[0]
        assert total_count == 4
        
        # Check backend-dev has 2 invocations (concurrent-001 and concurrent-004)
        cursor = conn.execute("""
            SELECT invocations, total_tokens, total_cost_usd
            FROM daily_costs
            WHERE agent_name = 'backend-dev'
        """)
        backend_row = cursor.fetchone()
        assert backend_row[0] == 2  # 2 invocations
        assert backend_row[1] == 900  # 500 + 400 tokens
        assert abs(backend_row[2] - 0.045) < 0.001  # 0.025 + 0.020 USD
        
        # Check each agent has separate aggregation
        cursor = conn.execute("SELECT COUNT(DISTINCT agent_name) FROM daily_costs")
        agent_count = cursor.fetchone()[0]
        assert agent_count == 3  # 3 unique agents


def test_end_to_end_privacy_level_metadata(logger):
    """
    Test privacy level 'metadata' mode.
    
    In metadata mode:
    - Invocation details logged
    - Cost and token metrics tracked
    - No prompt/response content (future implementation)
    """
    record = InvocationRecord(
        invocation_id="privacy-metadata-e2e",
        agent_name="backend-dev",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=200,
        completion_tokens=400,
        total_tokens=600,
        cost_usd=0.030,
        latency_ms=1500,
        status="success",
        privacy_level="metadata"
    )
    
    logger.log_invocation(record)
    
    # Verify metadata logged
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("""
            SELECT privacy_level, prompt_tokens, completion_tokens, cost_usd
            FROM invocations 
            WHERE invocation_id = ?
        """, ("privacy-metadata-e2e",))
        
        row = cursor.fetchone()
        assert row[0] == "metadata"
        assert row[1] == 200  # Tokens logged
        assert row[2] == 400
        assert abs(row[3] - 0.030) < 0.0001  # Cost logged


def test_end_to_end_cost_tracking_over_time(logger):
    """
    Test cost tracking across multiple invocations over time.
    
    Simulates a day's worth of invocations and verifies:
    - Individual invocations tracked
    - Daily aggregates updated correctly
    - Cost accumulation accurate
    """
    agent_name = "backend-dev"
    tool_name = "claude-code"
    model_name = "claude-3.5-sonnet"
    
    # Simulate 10 invocations throughout the day
    total_expected_cost = 0.0
    total_expected_tokens = 0
    
    for i in range(10):
        tokens = (i + 1) * 100  # Varying token counts
        cost = tokens * 0.00005  # $0.00005 per token (simplified)
        
        record = InvocationRecord(
            invocation_id=f"cost-tracking-{i:03d}",
            agent_name=agent_name,
            tool_name=tool_name,
            model_name=model_name,
            prompt_tokens=tokens // 2,
            completion_tokens=tokens // 2,
            total_tokens=tokens,
            cost_usd=cost,
            latency_ms=1000 + (i * 100),
            status="success"
        )
        logger.log_invocation(record)
        
        total_expected_cost += cost
        total_expected_tokens += tokens
    
    # Verify accumulation
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("""
            SELECT invocations, total_tokens, total_cost_usd
            FROM daily_costs
            WHERE agent_name = ?
            AND tool_name = ?
            AND model_name = ?
        """, (agent_name, tool_name, model_name))
        
        row = cursor.fetchone()
        assert row[0] == 10  # 10 invocations
        assert row[1] == total_expected_tokens
        assert abs(row[2] - total_expected_cost) < 0.001


def test_end_to_end_database_persistence(logger, temp_db):
    """
    Test database persistence across logger instances.
    
    Verifies:
    - Data survives logger destruction
    - New logger instance can read existing data
    - Schema preserved
    """
    # Log with first logger instance
    record1 = InvocationRecord(
        invocation_id="persistence-001",
        agent_name="backend-dev",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        cost_usd=0.015,
        latency_ms=1500,
        status="success"
    )
    logger.log_invocation(record1)
    
    # Create new logger instance
    logger2 = TelemetryLogger(temp_db)
    
    # Log with second logger instance
    record2 = InvocationRecord(
        invocation_id="persistence-002",
        agent_name="backend-dev",
        tool_name="claude-code",
        model_name="claude-3.5-sonnet",
        prompt_tokens=150,
        completion_tokens=250,
        total_tokens=400,
        cost_usd=0.020,
        latency_ms=1600,
        status="success"
    )
    logger2.log_invocation(record2)
    
    # Verify both records exist
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM invocations")
        count = cursor.fetchone()[0]
        assert count == 2
        
        # Verify daily aggregation includes both
        cursor = conn.execute("""
            SELECT invocations, total_tokens, total_cost_usd
            FROM daily_costs
            WHERE agent_name = 'backend-dev'
        """)
        row = cursor.fetchone()
        assert row[0] == 2  # 2 invocations
        assert row[1] == 700  # 300 + 400 tokens
        assert abs(row[2] - 0.035) < 0.001  # 0.015 + 0.020 USD


def test_end_to_end_error_rate_calculation(logger):
    """
    Test ability to calculate error rates from logged data.
    
    Simulates mix of successes and failures, then queries for error rate.
    """
    # Log mix of success and error invocations
    for i in range(8):
        status = "success" if i % 3 != 0 else "error"  # ~33% error rate
        
        record = InvocationRecord(
            invocation_id=f"error-rate-{i:03d}",
            agent_name="test-agent",
            tool_name="claude-code",
            model_name="claude-3.5-sonnet",
            prompt_tokens=100 if status == "success" else 0,
            completion_tokens=200 if status == "success" else 0,
            total_tokens=300 if status == "success" else 0,
            cost_usd=0.015 if status == "success" else 0.0,
            latency_ms=1500,
            status=status,
            error_message="Simulated error" if status == "error" else None
        )
        logger.log_invocation(record)
    
    # Calculate error rate
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors
            FROM invocations
            WHERE agent_name = 'test-agent'
        """)
        
        row = cursor.fetchone()
        total = row[0]
        errors = row[1]
        
        assert total == 8
        assert errors == 3  # Indices 0, 3, 6 (every 3rd)
        error_rate = errors / total
        assert 0.35 < error_rate < 0.40  # ~37.5%


def test_end_to_end_latency_tracking(logger):
    """
    Test latency tracking and statistical queries.
    
    Verifies ability to track and analyze performance metrics.
    """
    latencies = [100, 500, 1200, 800, 1500, 300, 2000, 600]
    
    for i, latency in enumerate(latencies):
        record = InvocationRecord(
            invocation_id=f"latency-{i:03d}",
            agent_name="test-agent",
            tool_name="claude-code",
            model_name="claude-3.5-sonnet",
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300,
            cost_usd=0.015,
            latency_ms=latency,
            status="success"
        )
        logger.log_invocation(record)
    
    # Query latency statistics
    with sqlite3.connect(logger.db_path) as conn:
        cursor = conn.execute("""
            SELECT 
                MIN(latency_ms) as min_latency,
                MAX(latency_ms) as max_latency,
                AVG(latency_ms) as avg_latency
            FROM invocations
            WHERE agent_name = 'test-agent'
        """)
        
        row = cursor.fetchone()
        min_latency = row[0]
        max_latency = row[1]
        avg_latency = row[2]
        
        assert min_latency == 100
        assert max_latency == 2000
        assert 800 < avg_latency < 900  # Average should be ~875
