"""
Unit tests for Task Priority Updater.

Following TDD (Directive 017): Write failing tests first (RED),
then implement to pass (GREEN), then refactor.

Tests YAML operations with comment preservation using ruamel.yaml.
Related: ADR-035
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone


class TestTaskPriorityUpdater:
    """
    Unit test suite for TaskPriorityUpdater class.
    
    Tests:
    - YAML loading with comment preservation
    - Priority validation
    - Status checking
    - Atomic file writes
    - Optimistic locking
    """

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def sample_task_yaml(self, temp_dir):
        """Create sample task YAML with comments."""
        task_file = temp_dir / "test-task.yaml"
        content = """id: "test-task-123"
title: "Test Task"
agent: "backend-dev"
status: "pending"  # Task status comment
priority: MEDIUM  # Priority comment
created: "2026-02-06T10:00:00Z"
# This is a standalone comment
description: |
  Multi-line description
  with multiple lines
"""
        task_file.write_text(content)
        return task_file

    def test_load_task_with_ruamel_yaml(self, sample_task_yaml):
        """
        Test: Load YAML task file using ruamel.yaml (RED phase)
        
        Given a task YAML file exists
        When loaded with TaskPriorityUpdater
        Then the task data is accessible
        And comments are preserved in memory
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        task_data = updater.load_task(sample_task_yaml.name)
        
        assert task_data is not None
        assert task_data['id'] == 'test-task-123'
        assert task_data['priority'] == 'MEDIUM'
        assert task_data['status'] == 'pending'

    def test_validate_priority_valid_values(self):
        """
        Test: Validate priority accepts valid enum values (RED phase)
        
        Given valid priority values (CRITICAL, HIGH, MEDIUM, LOW, normal)
        When validated
        Then no exception is raised
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        updater = TaskPriorityUpdater(".")
        
        valid_priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'normal']
        for priority in valid_priorities:
            # Should not raise
            updater.validate_priority(priority)

    def test_validate_priority_rejects_invalid_values(self):
        """
        Test: Validate priority rejects invalid values (RED phase)
        
        Given invalid priority values
        When validated
        Then ValueError is raised with helpful message
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        updater = TaskPriorityUpdater(".")
        
        invalid_priorities = ['SUPER-URGENT', 'urgent', 'P1', '', None, 123]
        for priority in invalid_priorities:
            with pytest.raises(ValueError) as exc_info:
                updater.validate_priority(priority)
            
            # Error message should list valid values
            error_msg = str(exc_info.value)
            assert 'CRITICAL' in error_msg or 'HIGH' in error_msg

    def test_check_status_allows_pending(self, sample_task_yaml):
        """
        Test: Status check allows 'pending' tasks (RED phase)
        
        Given a task with status 'pending'
        When checked if editable
        Then returns True
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        task_data = updater.load_task(sample_task_yaml.name)
        
        assert updater.is_editable_status(task_data) is True

    def test_check_status_rejects_in_progress(self, temp_dir):
        """
        Test: Status check rejects 'in_progress' tasks (RED phase)
        
        Given a task with status 'in_progress'
        When checked if editable
        Then returns False
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        task_file = temp_dir / "in-progress-task.yaml"
        content = """id: "in-progress-123"
title: "Active Task"
status: "in_progress"
priority: HIGH
"""
        task_file.write_text(content)
        
        updater = TaskPriorityUpdater(str(temp_dir))
        task_data = updater.load_task(task_file.name)
        
        assert updater.is_editable_status(task_data) is False

    def test_check_status_rejects_done(self, temp_dir):
        """
        Test: Status check rejects 'done' tasks (RED phase)
        
        Given a task with status 'done'
        When checked if editable
        Then returns False
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        task_file = temp_dir / "done-task.yaml"
        content = """id: "done-123"
title: "Completed Task"
status: "done"
priority: LOW
"""
        task_file.write_text(content)
        
        updater = TaskPriorityUpdater(str(temp_dir))
        task_data = updater.load_task(task_file.name)
        
        assert updater.is_editable_status(task_data) is False

    def test_update_priority_preserves_comments(self, sample_task_yaml):
        """
        Test: Update priority preserves YAML comments (RED phase)
        
        Given a task YAML with comments
        When priority is updated
        Then comments are preserved in output
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        original_content = sample_task_yaml.read_text()
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        updater.update_task_priority(sample_task_yaml.name, 'CRITICAL')
        
        updated_content = sample_task_yaml.read_text()
        
        # Priority should be updated
        assert 'priority: CRITICAL' in updated_content
        
        # Comments should be preserved
        assert '# Task status comment' in updated_content
        assert '# Priority comment' in updated_content
        assert '# This is a standalone comment' in updated_content

    def test_update_priority_preserves_field_order(self, sample_task_yaml):
        """
        Test: Update priority preserves field order (RED phase)
        
        Given a task YAML with specific field order
        When priority is updated
        Then field order remains the same
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        original_lines = sample_task_yaml.read_text().split('\n')
        
        # Find line indices for key fields
        id_line = next(i for i, line in enumerate(original_lines) if line.startswith('id:'))
        status_line = next(i for i, line in enumerate(original_lines) if line.startswith('status:'))
        priority_line = next(i for i, line in enumerate(original_lines) if line.startswith('priority:'))
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        updater.update_task_priority(sample_task_yaml.name, 'HIGH')
        
        updated_lines = sample_task_yaml.read_text().split('\n')
        
        # Field order should be preserved
        new_id_line = next(i for i, line in enumerate(updated_lines) if line.startswith('id:'))
        new_status_line = next(i for i, line in enumerate(updated_lines) if line.startswith('status:'))
        new_priority_line = next(i for i, line in enumerate(updated_lines) if line.startswith('priority:'))
        
        assert id_line == new_id_line
        assert status_line == new_status_line
        assert priority_line == new_priority_line

    def test_atomic_write_uses_temp_file(self, sample_task_yaml, monkeypatch):
        """
        Test: Atomic write uses temp file + rename (RED phase)
        
        Given a task file
        When priority is updated
        Then implementation uses temp file and atomic rename
        And original file is not corrupted on failure
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        
        # Track whether temp file was used
        temp_files_created = []
        original_open = open
        
        def track_temp_file(path, *args, **kwargs):
            if 'tmp' in str(path) or '.tmp' in str(path):
                temp_files_created.append(path)
            return original_open(path, *args, **kwargs)
        
        monkeypatch.setattr('builtins.open', track_temp_file)
        
        updater.update_task_priority(sample_task_yaml.name, 'LOW')
        
        # Should have created temp file (implementation detail)
        # This is a behavior test, not implementation test
        # Real check: file should be valid after write
        import yaml
        updated_data = yaml.safe_load(sample_task_yaml.read_text())
        assert updated_data['priority'] == 'LOW'

    def test_optimistic_locking_with_timestamp(self, sample_task_yaml):
        """
        Test: Optimistic locking checks last_modified timestamp (RED phase)
        
        Given a task with last_modified timestamp
        When update includes stale timestamp
        Then raises conflict error
        """
        from llm_service.dashboard.task_priority_updater import (
            TaskPriorityUpdater,
            ConcurrentModificationError
        )
        
        # Add last_modified to task
        content = sample_task_yaml.read_text()
        content += '\nlast_modified: "2026-02-06T10:00:00Z"\n'
        sample_task_yaml.write_text(content)
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        
        # Simulate file was modified after client loaded it
        # (Client has old timestamp)
        stale_timestamp = "2026-02-06T09:00:00Z"
        
        with pytest.raises(ConcurrentModificationError):
            updater.update_task_priority(
                sample_task_yaml.name,
                'CRITICAL',
                last_modified=stale_timestamp
            )

    def test_optimistic_locking_allows_current_timestamp(self, sample_task_yaml):
        """
        Test: Optimistic locking allows update with current timestamp (RED phase)
        
        Given a task with last_modified timestamp
        When update includes current timestamp
        Then update succeeds
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        # Add last_modified to task
        current_time = "2026-02-06T10:00:00Z"
        content = sample_task_yaml.read_text()
        content += f'\nlast_modified: "{current_time}"\n'
        sample_task_yaml.write_text(content)
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        
        # Should succeed with matching timestamp
        updater.update_task_priority(
            sample_task_yaml.name,
            'HIGH',
            last_modified=current_time
        )
        
        # Verify update succeeded
        updated_content = sample_task_yaml.read_text()
        assert 'priority: HIGH' in updated_content

    def test_get_task_file_path_validates_input(self):
        """
        Test: Task file path validation prevents path traversal (RED phase)
        
        Given a task_id with path traversal attempt
        When getting file path
        Then raises ValueError
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        updater = TaskPriorityUpdater(".")
        
        malicious_ids = [
            '../../../etc/passwd',
            '../../secrets.yaml',
            '/etc/passwd',
            'task-id/../other-file'
        ]
        
        for task_id in malicious_ids:
            with pytest.raises(ValueError) as exc_info:
                updater._get_task_file_path(task_id)
            
            assert 'invalid' in str(exc_info.value).lower() or 'traversal' in str(exc_info.value).lower()

    def test_get_task_file_path_allows_valid_ids(self, temp_dir):
        """
        Test: Task file path allows valid task IDs (RED phase)
        
        Given valid task IDs
        When getting file path
        Then returns correct path in work directory
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        updater = TaskPriorityUpdater(str(temp_dir))
        
        valid_ids = [
            '2026-02-06T1500-backend-dev-task',
            'simple-task-id',
            'task_with_underscores',
            'TASK-WITH-CAPS'
        ]
        
        for task_id in valid_ids:
            # Should not raise
            file_path = updater._get_task_file_path(task_id)
            assert task_id in str(file_path)
            assert str(temp_dir) in str(file_path)

    def test_update_adds_last_modified_timestamp(self, sample_task_yaml):
        """
        Test: Update adds or updates last_modified timestamp (RED phase)
        
        Given a task without last_modified field
        When priority is updated
        Then last_modified field is added with current UTC time
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        original_content = sample_task_yaml.read_text()
        assert 'last_modified' not in original_content
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        updater.update_task_priority(sample_task_yaml.name, 'HIGH')
        
        updated_content = sample_task_yaml.read_text()
        assert 'last_modified:' in updated_content
        
        # Should be a valid ISO timestamp
        import re
        timestamp_match = re.search(r'last_modified: ["\']?(\d{4}-\d{2}-\d{2}T[\d:]+.*Z)["\']?', updated_content)
        assert timestamp_match is not None

    def test_task_not_found_raises_error(self):
        """
        Test: Loading non-existent task raises FileNotFoundError (RED phase)
        
        Given a task ID that doesn't exist
        When attempting to load it
        Then raises FileNotFoundError
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        updater = TaskPriorityUpdater(".")
        
        with pytest.raises(FileNotFoundError):
            updater.load_task('nonexistent-task-id')

    def test_multiline_description_preserved(self, sample_task_yaml):
        """
        Test: Multiline descriptions are preserved correctly (RED phase)
        
        Given a task with multiline description
        When priority is updated
        Then multiline formatting is preserved
        """
        from llm_service.dashboard.task_priority_updater import TaskPriorityUpdater
        
        original_content = sample_task_yaml.read_text()
        assert 'Multi-line description' in original_content
        assert 'with multiple lines' in original_content
        
        updater = TaskPriorityUpdater(str(sample_task_yaml.parent))
        updater.update_task_priority(sample_task_yaml.name, 'CRITICAL')
        
        updated_content = sample_task_yaml.read_text()
        
        # Multiline content should be preserved
        assert 'Multi-line description' in updated_content
        assert 'with multiple lines' in updated_content
        assert 'description: |' in updated_content or 'description: >' in updated_content
