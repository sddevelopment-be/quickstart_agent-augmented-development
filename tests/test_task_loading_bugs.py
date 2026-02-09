"""
Test suite for task loading bug fixes.

Directive 028: Bug Fixing Techniques - TDD approach
- RED: Write failing test that reproduces bug
- GREEN: Fix code to make test pass
- REFACTOR: Clean up implementation

Bug reports from dashboard:
1. YAML multi-document error (line 9 has ---)
2. Missing 'id' field (old format uses 'task_id')
"""

import pytest
from pathlib import Path

from src.common.task_schema import read_task, TaskIOError, TaskValidationError


# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "tasks" / "broken"


class TestYAMLMultiDocumentBug:
    """
    Bug: Dashboard fails with 'expected a single document in the stream'
    
    Root cause: YAML file has --- on line 1 AND line 9
    Expected: Single YAML document with frontmatter-style format
    """
    
    def test_multi_document_separator_causes_parse_error(self, tmp_path):
        """RED: Test reproduces the exact error from dashboard logs."""
        # Create broken YAML with multiple --- separators
        broken_yaml = tmp_path / "multi-doc.yaml"
        broken_yaml.write_text("""---
id: test-task
agent: test-agent
status: inbox
title: "Test Task"
---

# Task Description
Content here
""")
        
        # This should fail with the exact error from dashboard
        with pytest.raises(TaskIOError, match="expected a single document"):
            read_task(broken_yaml)
    
    def test_single_document_loads_successfully(self, tmp_path):
        """GREEN: After fix, single-document format should work."""
        # Create correct YAML (single --- at top, description as multiline string)
        correct_yaml = tmp_path / "single-doc.yaml"
        correct_yaml.write_text("""---
id: test-task
agent: test-agent
status: inbox
title: "Test Task"
description: |
  # Task Description
  Content here
""")
        
        # This should succeed
        task = read_task(correct_yaml)
        assert task["id"] == "test-task"
        assert "# Task Description" in task["description"]


class TestMissingIdFieldBug:
    """
    Bug: Dashboard fails with "Missing required fields: {'id'}"
    
    Root cause: Old task format uses 'task_id' instead of 'id'
    Expected: Migrate old format or fail gracefully with clear error
    """
    
    def test_old_format_with_task_id_auto_migrates_with_warning(self, tmp_path):
        """GREEN: Auto-migration converts task_id → id with deprecation warning."""
        # Create old-format YAML with 'task_id' instead of 'id'
        old_format_yaml = tmp_path / "old-format.yaml"
        old_format_yaml.write_text("""task_id: "mfd-task-1.5-base-validator"
from_agent: "Project Manager"
to_agent: "Backend Benny"
status: "COMPLETE"
priority: "MEDIUM"
""")
        
        # Should auto-migrate with deprecation warning
        with pytest.warns(DeprecationWarning, match="Auto-migrating old task format"):
            task = read_task(old_format_yaml)
        
        # Verify migration worked
        assert task["id"] == "mfd-task-1.5-base-validator"
        assert task["task_id"] == "mfd-task-1.5-base-validator"  # Preserved for compatibility
    
    def test_new_format_with_id_loads_successfully(self, tmp_path):
        """GREEN: After fix or migration, new format should work."""
        # Create new-format YAML with 'id' field
        new_format_yaml = tmp_path / "new-format.yaml"
        new_format_yaml.write_text("""---
id: mfd-task-1.5-base-validator
agent: backend-dev
status: done
priority: medium
title: "Base Validator"
description: "Implement base validator framework"
""")
        
        # This should succeed
        task = read_task(new_format_yaml)
        assert task["id"] == "mfd-task-1.5-base-validator"
        assert task["agent"] == "backend-dev"


class TestRealBrokenFixtures:
    """
    Test against actual broken files from work/ directory.
    These are the REAL files causing dashboard errors.
    """
    
    def test_multi_document_fixture_fails(self):
        """Test against actual broken file copied from work/collaboration/inbox/"""
        fixture_path = FIXTURES_DIR / "multi-document-separator.yaml.broken"
        
        if not fixture_path.exists():
            pytest.skip("Fixture not found - may have been fixed already")
        
        with pytest.raises(TaskIOError, match="expected a single document"):
            read_task(fixture_path)
    
    def test_missing_id_fixture_auto_migrates(self):
        """Test against actual broken file - should auto-migrate now."""
        fixture_path = FIXTURES_DIR / "missing-id-field.yaml.broken"
        
        if not fixture_path.exists():
            pytest.skip("Fixture not found - may have been fixed already")
        
        # Should auto-migrate with deprecation warning
        with pytest.warns(DeprecationWarning, match="Auto-migrating old task format"):
            task = read_task(fixture_path)
        
        # Verify migration worked
        assert "id" in task
        assert task["id"] == task.get("task_id")  # Should be same value


class TestMigrationStrategy:
    """
    Tests for automatic migration from old format to new format.
    
    Strategy options:
    1. Reject old format with clear error (current behavior - GOOD)
    2. Auto-migrate task_id → id (convenience, but hides drift)
    3. Provide migration script (manual, but traceable)
    
    Recommendation: Keep current behavior (option 1) + provide migration script
    """
    
    def test_migration_script_should_convert_task_id_to_id(self, tmp_path):
        """Future: Migration script should convert old format to new."""
        # This test documents the expected migration behavior
        # Implementation would be a separate script: tools/migrate-old-task-format.py
        pytest.skip("Migration script not yet implemented - manual fix for now")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
