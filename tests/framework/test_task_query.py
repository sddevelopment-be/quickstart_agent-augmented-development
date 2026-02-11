"""
Tests for task_query module - Task discovery and filtering.

Tests cover:
- find_task_files() - File discovery across directory structure
- load_open_tasks() - Loading non-terminal tasks
- filter_tasks() - Multi-criteria filtering
- count_tasks_by_status() - Status distribution metrics
- count_tasks_by_agent() - Agent workload metrics

Note: Module moved to domain layer as part of ADR-046
"""

import pytest
from pathlib import Path
from src.domain.collaboration.task_query import (
    find_task_files,
    load_open_tasks,
    filter_tasks,
    count_tasks_by_status,
    count_tasks_by_agent,
)
from src.domain.collaboration.types import TaskStatus


@pytest.fixture
def mock_work_dir(tmp_path):
    """Create mock work directory structure with sample tasks."""
    work_dir = tmp_path / "collaboration"
    
    # Create directory structure
    inbox_dir = work_dir / "inbox"
    inbox_dir.mkdir(parents=True)
    
    assigned_dir = work_dir / "assigned"
    (assigned_dir / "python-pedro").mkdir(parents=True)
    (assigned_dir / "backend-benny").mkdir(parents=True)
    
    done_dir = work_dir / "done"
    (done_dir / "python-pedro").mkdir(parents=True)
    
    # Create sample tasks
    # Inbox task
    (inbox_dir / "2026-02-10T1000-inbox-task.yaml").write_text("""
id: 2026-02-10T1000-inbox-task
status: inbox
priority: normal
description: Inbox task
""")
    
    # Assigned tasks
    (assigned_dir / "python-pedro" / "2026-02-10T1001-pedro-task.yaml").write_text("""
id: 2026-02-10T1001-pedro-task
agent: python-pedro
status: assigned
priority: high
description: Pedro task
""")
    
    (assigned_dir / "python-pedro" / "2026-02-10T1002-pedro-inprogress.yaml").write_text("""
id: 2026-02-10T1002-pedro-inprogress
agent: python-pedro
status: in_progress
priority: normal
description: Pedro in progress
""")
    
    (assigned_dir / "backend-benny" / "2026-02-10T1003-benny-task.yaml").write_text("""
id: 2026-02-10T1003-benny-task
agent: backend-benny
status: assigned
priority: medium
description: Benny task
""")
    
    # Done task (terminal state)
    (done_dir / "python-pedro" / "2026-02-10T1004-pedro-done.yaml").write_text("""
id: 2026-02-10T1004-pedro-done
agent: python-pedro
status: done
priority: normal
description: Completed task
result:
  outcome: success
""")
    
    return work_dir


class TestFindTaskFiles:
    """Tests for find_task_files()"""
    
    def test_finds_all_active_tasks(self, mock_work_dir):
        """Should find tasks in inbox and assigned directories."""
        files = find_task_files(mock_work_dir, include_done=False)
        
        assert len(files) == 4  # 1 inbox + 3 assigned
        assert all(f.suffix == ".yaml" for f in files)
        assert any("inbox" in str(f) for f in files)
        assert any("assigned" in str(f) for f in files)
    
    def test_excludes_done_by_default(self, mock_work_dir):
        """Should exclude done directory by default."""
        files = find_task_files(mock_work_dir, include_done=False)
        
        # Check that no files are from the done/ directory
        assert not any("/done/" in str(f) or str(f).endswith("/done") for f in files)
    
    def test_includes_done_when_requested(self, mock_work_dir):
        """Should include done directory when include_done=True."""
        files = find_task_files(mock_work_dir, include_done=True)
        
        assert len(files) == 5  # 1 inbox + 3 assigned + 1 done
        assert any("done" in str(f) for f in files)
    
    def test_returns_sorted_list(self, mock_work_dir):
        """Should return deterministic sorted order."""
        files1 = find_task_files(mock_work_dir)
        files2 = find_task_files(mock_work_dir)
        
        assert files1 == files2  # Same order
        assert files1 == sorted(files1)  # Sorted
    
    def test_handles_empty_directory(self, tmp_path):
        """Should handle work directory with no tasks."""
        work_dir = tmp_path / "empty"
        work_dir.mkdir()
        
        files = find_task_files(work_dir)
        
        assert files == []
    
    def test_handles_nonexistent_directory(self, tmp_path):
        """Should handle nonexistent work directory gracefully."""
        work_dir = tmp_path / "nonexistent"
        
        files = find_task_files(work_dir)
        
        assert files == []


class TestLoadOpenTasks:
    """Tests for load_open_tasks()"""
    
    def test_loads_only_nonterminal_tasks(self, mock_work_dir):
        """Should load only tasks not in terminal states."""
        tasks = load_open_tasks(mock_work_dir)
        
        assert len(tasks) == 4  # Excludes done task
        
        # Verify no terminal states
        for task in tasks:
            status = TaskStatus(task["status"])
            assert not TaskStatus.is_terminal(status)
    
    def test_includes_all_nonterminal_states(self, mock_work_dir):
        """Should include inbox, assigned, in_progress states."""
        tasks = load_open_tasks(mock_work_dir)
        
        statuses = {task["status"] for task in tasks}
        assert "inbox" in statuses
        assert "assigned" in statuses
        assert "in_progress" in statuses
    
    def test_skips_invalid_tasks(self, tmp_path):
        """Should skip tasks with invalid YAML or structure."""
        work_dir = tmp_path / "collaboration"
        inbox_dir = work_dir / "inbox"
        inbox_dir.mkdir(parents=True)
        
        # Invalid YAML
        (inbox_dir / "invalid.yaml").write_text("invalid: yaml: content:")
        
        # Valid task
        (inbox_dir / "valid.yaml").write_text("""
id: valid-task
status: inbox
description: Valid task
""")
        
        tasks = load_open_tasks(work_dir)
        
        assert len(tasks) == 1  # Only valid task loaded
        assert tasks[0]["id"] == "valid-task"
    
    def test_returns_empty_for_no_tasks(self, tmp_path):
        """Should return empty list when no open tasks exist."""
        work_dir = tmp_path / "collaboration"
        work_dir.mkdir()
        
        tasks = load_open_tasks(work_dir)
        
        assert tasks == []


class TestFilterTasks:
    """Tests for filter_tasks()"""
    
    def test_filter_by_status_string(self, mock_work_dir):
        """Should filter by status using string value."""
        tasks = load_open_tasks(mock_work_dir)
        
        assigned = filter_tasks(tasks, status="assigned")
        
        assert len(assigned) == 2
        assert all(t["status"] == "assigned" for t in assigned)
    
    def test_filter_by_status_enum(self, mock_work_dir):
        """Should filter by status using TaskStatus enum."""
        tasks = load_open_tasks(mock_work_dir)
        
        assigned = filter_tasks(tasks, status=TaskStatus.ASSIGNED)
        
        assert len(assigned) == 2
        assert all(t["status"] == "assigned" for t in assigned)
    
    def test_filter_by_agent(self, mock_work_dir):
        """Should filter by agent identifier."""
        tasks = load_open_tasks(mock_work_dir)
        
        pedro_tasks = filter_tasks(tasks, agent="python-pedro")
        
        assert len(pedro_tasks) == 2
        assert all(t["agent"] == "python-pedro" for t in pedro_tasks)
    
    def test_filter_by_priority(self, mock_work_dir):
        """Should filter by priority level."""
        tasks = load_open_tasks(mock_work_dir)
        
        normal_priority = filter_tasks(tasks, priority="normal")
        
        assert len(normal_priority) == 2
        assert all(t["priority"] == "normal" for t in normal_priority)
    
    def test_filter_multiple_criteria(self, mock_work_dir):
        """Should apply AND logic for multiple filters."""
        tasks = load_open_tasks(mock_work_dir)
        
        result = filter_tasks(
            tasks,
            status="assigned",
            agent="python-pedro",
            priority="high"
        )
        
        assert len(result) == 1
        assert result[0]["id"] == "2026-02-10T1001-pedro-task"
    
    def test_filter_returns_empty_on_no_match(self, mock_work_dir):
        """Should return empty list when no tasks match."""
        tasks = load_open_tasks(mock_work_dir)
        
        result = filter_tasks(tasks, agent="nonexistent-agent")
        
        assert result == []
    
    def test_filter_with_no_criteria(self, mock_work_dir):
        """Should return all tasks when no filters specified."""
        tasks = load_open_tasks(mock_work_dir)
        
        result = filter_tasks(tasks)
        
        assert result == tasks


class TestCountTasksByStatus:
    """Tests for count_tasks_by_status()"""
    
    def test_counts_by_status(self, mock_work_dir):
        """Should count tasks grouped by status."""
        counts = count_tasks_by_status(mock_work_dir)
        
        assert counts["inbox"] == 1
        assert counts["assigned"] == 2
        assert counts["in_progress"] == 1
    
    def test_excludes_terminal_states(self, mock_work_dir):
        """Should not include done/error states."""
        counts = count_tasks_by_status(mock_work_dir)
        
        assert "done" not in counts
        assert "error" not in counts
    
    def test_returns_empty_for_no_tasks(self, tmp_path):
        """Should return empty dict when no tasks exist."""
        work_dir = tmp_path / "collaboration"
        work_dir.mkdir()
        
        counts = count_tasks_by_status(work_dir)
        
        assert counts == {}


class TestCountTasksByAgent:
    """Tests for count_tasks_by_agent()"""
    
    def test_counts_by_agent(self, mock_work_dir):
        """Should count tasks grouped by agent."""
        counts = count_tasks_by_agent(mock_work_dir)
        
        assert counts["python-pedro"] == 2
        assert counts["backend-benny"] == 1
    
    def test_handles_unassigned_tasks(self, tmp_path):
        """Should count tasks without agent as 'unassigned'."""
        work_dir = tmp_path / "collaboration"
        inbox_dir = work_dir / "inbox"
        inbox_dir.mkdir(parents=True)
        
        (inbox_dir / "unassigned.yaml").write_text("""
id: unassigned-task
status: inbox
description: No agent assigned
""")
        
        counts = count_tasks_by_agent(work_dir)
        
        assert counts["unassigned"] == 1
    
    def test_returns_empty_for_no_tasks(self, tmp_path):
        """Should return empty dict when no tasks exist."""
        work_dir = tmp_path / "collaboration"
        work_dir.mkdir()
        
        counts = count_tasks_by_agent(work_dir)
        
        assert counts == {}
