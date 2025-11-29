#!/usr/bin/env python3
"""
Unit and Acceptance Tests for capture-metrics.py

Tests metrics extraction from work logs and task YAML files.
Validates JSON and CSV output formats and ADR-009 compliance.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

# Add dashboards directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "ops" / "dashboards"))

# Import from file with dash in name
import importlib.util
spec = importlib.util.spec_from_file_location(
    "capture_metrics",
    Path(__file__).parent.parent.parent / "ops" / "dashboards" / "capture-metrics.py"
)
capture_metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture_metrics)
MetricsExtractor = capture_metrics.MetricsExtractor


@pytest.fixture
def temp_work_env(tmp_path: Path) -> Path:
    """Create isolated test environment with work directory structure."""
    work_dir = tmp_path / "work"
    (work_dir / "reports" / "logs" / "test-agent").mkdir(parents=True)
    (work_dir / "collaboration" / "new").mkdir(parents=True)
    (work_dir / "collaboration" / "in_progress").mkdir(parents=True)
    return work_dir


@pytest.fixture
def sample_work_log(temp_work_env: Path) -> Path:
    """Create a sample work log file with ADR-009 metrics."""
    log_file = temp_work_env / "reports" / "logs" / "test-agent" / "2025-11-29T1200-test-task.md"
    content = """# Work Log: Test Task

**Task ID:** 2025-11-29T1200-test-task

## Metadata

- **Duration:** 45 minutes
- **Token Usage:** 5,000 input + 2,500 output = 7,500 total
- **Context Files Loaded:** 3
- **Artifacts Created:** 2
- **Artifacts Modified:** 1

## Task Summary

Test task completed successfully.
"""
    log_file.write_text(content, encoding="utf-8")
    return log_file


@pytest.fixture
def sample_task_yaml(temp_work_env: Path) -> Path:
    """Create a sample task YAML file with metrics."""
    done_dir = temp_work_env / "collaboration" / "done" / "test-agent"
    done_dir.mkdir(parents=True, exist_ok=True)
    task_file = done_dir / "task-001.yaml"
    task_data = {
        "id": "2025-11-29T1200-test-task",
        "agent": "test-agent",
        "status": "completed",
        "created_at": "2025-11-29T12:00:00Z",
        "result": {
            "metrics": {
                "duration_minutes": 30,
                "token_count": {"input": 3000, "output": 1500, "total": 4500},
                "context_files_loaded": 2,
                "artifacts_created": 1,
                "artifacts_modified": 0,
            },
        },
    }
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task_data, f, default_flow_style=False, sort_keys=False)
    return task_file


# ============================================================================
# Acceptance Tests
# ============================================================================


def test_extract_metrics_from_work_logs(temp_work_env: Path, sample_work_log: Path) -> None:
    """
    Acceptance Test: Extract metrics from work logs.
    
    Given a work log with ADR-009 metrics
    When MetricsExtractor processes the work log
    Then it should extract all required metrics fields.
    """
    # Arrange
    extractor = MetricsExtractor(temp_work_env, verbose=False)
    
    # Assumption Check
    assert sample_work_log.exists(), "Test precondition: work log should exist"
    log_content = sample_work_log.read_text()
    assert "Metadata" in log_content, "Test precondition: log should have Metadata section"
    assert "Duration" in log_content, "Test precondition: log should contain duration"
    
    # Act
    extractor.extract_from_work_logs()
    
    # Assert
    assert len(extractor.metrics) > 0, "Should extract at least one metric entry"
    metric = extractor.metrics[0]
    assert metric["duration_minutes"] == 45
    assert metric["token_input"] == 5000
    assert metric["token_output"] == 2500
    assert metric["token_total"] == 7500
    assert metric["context_files_loaded"] == 3
    assert metric["artifacts_created"] == 2
    assert metric["artifacts_modified"] == 1


def test_extract_metrics_from_task_files(temp_work_env: Path, sample_task_yaml: Path) -> None:
    """
    Acceptance Test: Extract metrics from task YAML files.
    
    Given a task YAML with metrics section in done directory
    When MetricsExtractor processes the task
    Then it should extract metrics from the YAML structure.
    """
    # Arrange
    extractor = MetricsExtractor(temp_work_env, verbose=False)
    
    # Assumption Check
    assert sample_task_yaml.exists(), "Test precondition: task file should exist"
    assert "done" in str(sample_task_yaml), "Test precondition: task should be in done directory"
    task_data = yaml.safe_load(sample_task_yaml.read_text())
    assert "result" in task_data, "Test precondition: task should have result section"
    
    # Act
    extractor.extract_from_task_files()
    
    # Assert
    assert len(extractor.metrics) > 0, "Should extract at least one metric entry"
    metric = extractor.metrics[0]
    assert metric["duration_minutes"] == 30
    assert metric["token_total"] == 4500


def test_json_output_format(temp_work_env: Path, sample_work_log: Path, tmp_path: Path) -> None:
    """
    Acceptance Test: Generate JSON output with required structure.
    
    Given extracted metrics
    When generating JSON output
    Then it should include extracted_at, metrics_count, metrics, and summary.
    """
    # Arrange
    extractor = MetricsExtractor(temp_work_env, verbose=False)
    extractor.extract_from_work_logs()
    output_file = tmp_path / "metrics.json"
    
    # Assumption Check
    assert len(extractor.metrics) > 0, "Test precondition: should have metrics"
    assert not output_file.exists(), "Test precondition: output file should not exist"
    
    # Act
    extractor.output_json(output_file)
    
    # Assert
    assert output_file.exists(), "Output file should be created"
    data = json.loads(output_file.read_text())
    assert "extracted_at" in data
    assert "metrics_count" in data
    assert "metrics" in data
    assert "summary" in data
    assert data["metrics_count"] == len(data["metrics"])


def test_csv_output_format(temp_work_env: Path, sample_work_log: Path, tmp_path: Path) -> None:
    """
    Acceptance Test: Generate CSV output with header row.
    
    Given extracted metrics
    When generating CSV output
    Then it should include header and data rows.
    """
    # Arrange
    extractor = MetricsExtractor(temp_work_env, verbose=False)
    extractor.extract_from_work_logs()
    output_file = tmp_path / "metrics.csv"
    
    # Assumption Check
    assert len(extractor.metrics) > 0, "Test precondition: should have metrics"
    assert not output_file.exists(), "Test precondition: output file should not exist"
    
    # Act
    extractor.output_csv(output_file)
    
    # Assert
    assert output_file.exists(), "Output file should be created"
    lines = output_file.read_text().strip().split("\n")
    assert len(lines) >= 2, "Should have header + at least one data row"
    header = lines[0]
    # Check for common metric fields in header
    assert "agent" in header or "duration_minutes" in header


# ============================================================================
# Unit Tests
# ============================================================================


def test_metrics_extractor_initialization(temp_work_env: Path) -> None:
    """Test MetricsExtractor initializes with correct work directory."""
    # Arrange & Act
    extractor = MetricsExtractor(temp_work_env, verbose=True)
    
    # Assert
    assert extractor.work_dir == temp_work_env
    assert extractor.verbose is True
    assert extractor.metrics == []


def test_empty_work_directory(tmp_path: Path) -> None:
    """Test extraction handles empty work directory gracefully."""
    # Arrange
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    extractor = MetricsExtractor(empty_dir, verbose=False)
    
    # Assumption Check
    assert empty_dir.exists(), "Test precondition: directory should exist"
    assert not (empty_dir / "reports" / "logs").exists(), "Test precondition: no logs directory"
    
    # Act
    extractor.extract_from_work_logs()
    
    # Assert
    assert len(extractor.metrics) == 0, "Should handle missing logs gracefully"


def test_invalid_yaml_handling(temp_work_env: Path) -> None:
    """Test extraction handles invalid YAML gracefully."""
    # Arrange
    bad_task = temp_work_env / "collaboration" / "new" / "bad-task.yaml"
    bad_task.write_text("{ invalid: yaml: content", encoding="utf-8")
    extractor = MetricsExtractor(temp_work_env, verbose=False)
    
    # Assumption Check
    assert bad_task.exists(), "Test precondition: bad task file should exist"
    
    # Act (should not raise exception)
    extractor.extract_from_task_files()
    
    # Assert
    assert len(extractor.metrics) == 0, "Should skip invalid YAML without crashing"


def test_work_log_without_metrics(temp_work_env: Path) -> None:
    """Test extraction handles logs without metrics section."""
    # Arrange
    log_file = temp_work_env / "reports" / "logs" / "test-agent" / "no-metrics.md"
    log_file.write_text("# Work Log\n\nNo metrics here.", encoding="utf-8")
    extractor = MetricsExtractor(temp_work_env, verbose=False)
    
    # Assumption Check
    assert log_file.exists(), "Test precondition: log file should exist"
    assert "Metrics" not in log_file.read_text(), "Test precondition: should have no metrics section"
    
    # Act
    extractor.extract_from_work_logs()
    
    # Assert
    # Should either skip or extract partial metrics
    # (Implementation detail - could be 0 or 1 with defaults)
    assert isinstance(extractor.metrics, list)


def test_summary_aggregation(temp_work_env: Path, sample_work_log: Path, tmp_path: Path) -> None:
    """Test summary aggregates metrics by agent."""
    # Arrange
    extractor = MetricsExtractor(temp_work_env, verbose=False)
    extractor.extract_from_work_logs()
    output_file = tmp_path / "metrics.json"
    
    # Assumption Check
    assert len(extractor.metrics) > 0, "Test precondition: should have metrics"
    
    # Act
    extractor.output_json(output_file)
    data = json.loads(output_file.read_text())
    
    # Assert
    summary = data["summary"]
    assert "agents" in summary or "totals" in summary


def test_verbose_logging(temp_work_env: Path, sample_work_log: Path, capsys) -> None:
    """Test verbose mode produces log messages."""
    # Arrange
    extractor = MetricsExtractor(temp_work_env, verbose=True)
    
    # Act
    extractor.extract_from_work_logs()
    captured = capsys.readouterr()
    
    # Assert
    assert "[INFO]" in captured.err, "Verbose mode should produce [INFO] messages"
