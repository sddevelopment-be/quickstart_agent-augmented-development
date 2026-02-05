"""
Unit tests for Dashboard Telemetry API.

Tests cost/metrics query endpoints following TDD (Directive 017).
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import sqlite3
from datetime import datetime, timezone, timedelta


class TestTelemetryAPI:
    """Test suite for telemetry API module."""

    def test_api_initialization(self):
        """Test: TelemetryAPI can be initialized with database path."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            api = TelemetryAPI(db_path=db_path)
            
            assert api is not None
            assert api.db_path == db_path

    def test_get_total_cost(self):
        """Test: API can query total cost from database."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            
            # Create test database with schema
            self._create_test_db(db_path)
            
            # Insert test data
            with sqlite3.connect(db_path) as conn:
                conn.execute("""
                    INSERT INTO invocations (
                        invocation_id, tool_name, model_name, total_tokens, cost_usd, status
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, ('test-1', 'claude-code', 'claude-3.5-sonnet', 1000, 0.05, 'success'))
            
            api = TelemetryAPI(db_path=db_path)
            total_cost = api.get_total_cost()
            
            assert total_cost == 0.05

    def test_get_today_cost(self):
        """Test: API can query cost for today."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            self._create_test_db(db_path)
            
            # Insert data for today
            today = datetime.now(timezone.utc).date()
            with sqlite3.connect(db_path) as conn:
                conn.execute("""
                    INSERT INTO invocations (
                        invocation_id, timestamp, tool_name, model_name, 
                        total_tokens, cost_usd, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, ('test-today', today.isoformat(), 'claude-code', 
                      'claude-3.5-sonnet', 1000, 0.03, 'success'))
            
            api = TelemetryAPI(db_path=db_path)
            today_cost = api.get_today_cost()
            
            assert today_cost == 0.03

    def test_get_monthly_cost(self):
        """Test: API can query cost for current month."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            self._create_test_db(db_path)
            
            # Insert data for this month
            now = datetime.now(timezone.utc)
            with sqlite3.connect(db_path) as conn:
                conn.execute("""
                    INSERT INTO invocations (
                        invocation_id, timestamp, tool_name, model_name, 
                        total_tokens, cost_usd, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, ('test-month', now.isoformat(), 'claude-code', 
                      'claude-3.5-sonnet', 2000, 0.10, 'success'))
            
            api = TelemetryAPI(db_path=db_path)
            monthly_cost = api.get_monthly_cost()
            
            assert monthly_cost == 0.10

    def test_get_model_usage_stats(self):
        """Test: API can query model usage statistics."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            self._create_test_db(db_path)
            
            # Insert usage for multiple models
            with sqlite3.connect(db_path) as conn:
                conn.execute("""
                    INSERT INTO invocations (invocation_id, tool_name, model_name, total_tokens, cost_usd, status)
                    VALUES 
                        ('inv-1', 'claude-code', 'claude-3.5-sonnet', 1000, 0.05, 'success'),
                        ('inv-2', 'claude-code', 'claude-3.5-sonnet', 2000, 0.10, 'success'),
                        ('inv-3', 'openai', 'gpt-4', 1500, 0.08, 'success')
                """)
            
            api = TelemetryAPI(db_path=db_path)
            stats = api.get_model_usage_stats()
            
            assert isinstance(stats, list)
            assert len(stats) == 2  # Two distinct models
            
            # Check structure
            claude_stats = next(s for s in stats if s['model_name'] == 'claude-3.5-sonnet')
            assert claude_stats['invocations'] == 2
            assert claude_stats['total_tokens'] == 3000
            assert abs(claude_stats['total_cost_usd'] - 0.15) < 0.001  # Floating point tolerance

    def test_get_cost_trend(self):
        """Test: API can query cost trend over time."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            self._create_test_db(db_path)
            
            # Insert data for multiple days
            today = datetime.now(timezone.utc)
            yesterday = today - timedelta(days=1)
            
            with sqlite3.connect(db_path) as conn:
                conn.execute("""
                    INSERT INTO invocations (invocation_id, timestamp, tool_name, model_name, total_tokens, cost_usd, status)
                    VALUES 
                        ('inv-today', ?, 'claude-code', 'claude-3.5-sonnet', 1000, 0.05, 'success'),
                        ('inv-yesterday', ?, 'claude-code', 'claude-3.5-sonnet', 2000, 0.10, 'success')
                """, (today.isoformat(), yesterday.isoformat()))
            
            api = TelemetryAPI(db_path=db_path)
            trend = api.get_cost_trend(days=7)
            
            assert isinstance(trend, list)
            assert len(trend) > 0

    def test_get_active_operations(self):
        """Test: API can query currently active operations."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            self._create_test_db(db_path)
            
            # For now, operations are inferred from recent invocations
            now = datetime.now(timezone.utc)
            
            with sqlite3.connect(db_path) as conn:
                conn.execute("""
                    INSERT INTO invocations (invocation_id, timestamp, tool_name, model_name, total_tokens, cost_usd, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, ('inv-recent', now.isoformat(), 'claude-code', 
                      'claude-3.5-sonnet', 1000, 0.05, 'success'))
            
            api = TelemetryAPI(db_path=db_path)
            active = api.get_active_operations()
            
            assert isinstance(active, list)

    def test_to_dict_conversion(self):
        """Test: API can convert query results to dashboard-friendly dict."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            self._create_test_db(db_path)
            
            api = TelemetryAPI(db_path=db_path)
            dashboard_data = api.to_dashboard_dict()
            
            assert 'costs' in dashboard_data
            assert 'models' in dashboard_data
            assert 'trends' in dashboard_data
            assert 'active_operations' in dashboard_data
            assert 'timestamp' in dashboard_data

    def test_empty_database_handling(self):
        """Test: API handles empty database gracefully."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            self._create_test_db(db_path)
            
            api = TelemetryAPI(db_path=db_path)
            
            # Should return 0.0 for costs, empty lists for stats
            assert api.get_total_cost() == 0.0
            assert api.get_today_cost() == 0.0
            assert api.get_monthly_cost() == 0.0
            assert api.get_model_usage_stats() == []

    def test_socketio_event_emission(self):
        """Test: API can emit cost update events via SocketIO."""
        from llm_service.dashboard.telemetry_api import TelemetryAPI
        
        mock_socketio = Mock()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / 'telemetry.db'
            self._create_test_db(db_path)
            
            # Insert test data
            with sqlite3.connect(db_path) as conn:
                conn.execute("""
                    INSERT INTO invocations (invocation_id, tool_name, model_name, total_tokens, cost_usd, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, ('test-1', 'claude-code', 'claude-3.5-sonnet', 1000, 0.05, 'success'))
            
            api = TelemetryAPI(db_path=db_path, socketio=mock_socketio)
            api.emit_cost_update()
            
            # Verify SocketIO emit was called
            assert mock_socketio.emit.called
            call_args = mock_socketio.emit.call_args
            assert call_args[0][0] == 'cost.update'

    @staticmethod
    def _create_test_db(db_path: Path):
        """Helper: Create test database with schema."""
        # Read schema from telemetry module
        schema_path = Path(__file__).parent.parent.parent / 'src' / 'llm_service' / 'telemetry' / 'schema.sql'
        
        if not schema_path.exists():
            # Fallback: minimal schema for testing
            minimal_schema = """
            CREATE TABLE IF NOT EXISTS invocations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invocation_id TEXT UNIQUE NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                agent_name TEXT,
                tool_name TEXT NOT NULL,
                model_name TEXT NOT NULL,
                prompt_tokens INTEGER DEFAULT 0,
                completion_tokens INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0.0,
                latency_ms INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                error_message TEXT,
                privacy_level TEXT DEFAULT 'metadata'
            );
            """
            with sqlite3.connect(db_path) as conn:
                conn.executescript(minimal_schema)
        else:
            with open(schema_path) as f:
                schema = f.read()
            with sqlite3.connect(db_path) as conn:
                conn.executescript(schema)
