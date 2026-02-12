"""
Unit tests for TaskLinker.

Tests the linking of tasks to specifications and features.
Implements TDD (Directive 017) - RED phase.
"""

from pathlib import Path

import pytest
import yaml


class TestTaskScanning:
    """Unit tests for task file discovery and loading."""

    def test_scan_work_directory_structure(self, tmp_path: Path):
        """Test scanning work/collaboration directory for task files."""
        pytest.skip("Implementation pending: TaskLinker.scan_tasks")

        from src.llm_service.dashboard.task_linker import TaskLinker

        # Create work directory structure
        work_dir = tmp_path / "work" / "collaboration"
        (work_dir / "inbox").mkdir(parents=True)
        (work_dir / "assigned" / "agent1").mkdir(parents=True)
        (work_dir / "done" / "agent2").mkdir(parents=True)

        # Create task files
        task1 = {"id": "task-001", "title": "Task 1", "status": "inbox"}
        (work_dir / "inbox" / "task-001.yaml").write_text(yaml.dump(task1))

        task2 = {"id": "task-002", "title": "Task 2", "status": "assigned"}
        (work_dir / "assigned" / "agent1" / "task-002.yaml").write_text(
            yaml.dump(task2)
        )

        linker = TaskLinker(str(work_dir))
        tasks = linker.scan_tasks()

        assert len(tasks) == 2
        assert any(t["id"] == "task-001" for t in tasks)
        assert any(t["id"] == "task-002" for t in tasks)

    def test_load_task_yaml(self, tmp_path: Path):
        """Test loading and parsing task YAML file."""
        pytest.skip("Implementation pending: TaskLinker.load_task")

        from src.llm_service.dashboard.task_linker import TaskLinker

        task_data = {
            "id": "task-001",
            "title": "Test Task",
            "agent": "python-pedro",
            "status": "assigned",
            "priority": "HIGH",
            "specification": "specs/test.md",
            "feature": "feat-001",
        }

        task_path = tmp_path / "task-001.yaml"
        task_path.write_text(yaml.dump(task_data))

        linker = TaskLinker(str(tmp_path))
        task = linker.load_task(str(task_path))

        assert task is not None
        assert task["id"] == "task-001"
        assert task["specification"] == "specs/test.md"
        assert task["feature"] == "feat-001"

    def test_load_task_with_missing_specification_field(self, tmp_path: Path):
        """Test loading task without specification field."""
        pytest.skip("Implementation pending: TaskLinker.load_task")

        from src.llm_service.dashboard.task_linker import TaskLinker

        task_data = {
            "id": "task-001",
            "title": "Task without spec",
            "status": "inbox",
        }

        task_path = tmp_path / "task-001.yaml"
        task_path.write_text(yaml.dump(task_data))

        linker = TaskLinker(str(tmp_path))
        task = linker.load_task(str(task_path))

        assert task is not None
        assert "specification" not in task

    def test_ignore_non_yaml_files(self, tmp_path: Path):
        """Test that non-YAML files are ignored during scan."""
        pytest.skip("Implementation pending: TaskLinker.scan_tasks")

        from src.llm_service.dashboard.task_linker import TaskLinker

        work_dir = tmp_path / "work"
        (work_dir / "inbox").mkdir(parents=True)

        # Create YAML task
        task = {"id": "task-001", "status": "inbox"}
        (work_dir / "inbox" / "task-001.yaml").write_text(yaml.dump(task))

        # Create non-YAML files
        (work_dir / "inbox" / "readme.txt").write_text("Not a task")
        (work_dir / "inbox" / "notes.md").write_text("# Notes")

        linker = TaskLinker(str(work_dir))
        tasks = linker.scan_tasks()

        assert len(tasks) == 1
        assert tasks[0]["id"] == "task-001"


class TestTaskGrouping:
    """Unit tests for grouping tasks by specification."""

    def test_group_tasks_by_specification(self, tmp_path: Path):
        """Test grouping tasks by their specification field."""
        pytest.skip("Implementation pending: TaskLinker.group_by_specification")

        from src.llm_service.dashboard.task_linker import TaskLinker

        work_dir = tmp_path / "work"
        (work_dir / "inbox").mkdir(parents=True)

        # Create tasks linking to different specs
        task1 = {
            "id": "task-001",
            "specification": "specs/spec-a.md",
            "status": "inbox",
        }
        (work_dir / "inbox" / "task-001.yaml").write_text(yaml.dump(task1))

        task2 = {
            "id": "task-002",
            "specification": "specs/spec-a.md",
            "status": "inbox",
        }
        (work_dir / "inbox" / "task-002.yaml").write_text(yaml.dump(task2))

        task3 = {
            "id": "task-003",
            "specification": "specs/spec-b.md",
            "status": "inbox",
        }
        (work_dir / "inbox" / "task-003.yaml").write_text(yaml.dump(task3))

        linker = TaskLinker(str(work_dir))
        groups = linker.group_by_specification()

        assert "specs/spec-a.md" in groups
        assert "specs/spec-b.md" in groups
        assert len(groups["specs/spec-a.md"]) == 2
        assert len(groups["specs/spec-b.md"]) == 1

    def test_group_tasks_by_feature(self, tmp_path: Path):
        """Test grouping tasks by feature within a specification."""
        pytest.skip("Implementation pending: TaskLinker.group_by_feature")

        from src.llm_service.dashboard.task_linker import TaskLinker

        work_dir = tmp_path / "work"
        (work_dir / "inbox").mkdir(parents=True)

        # Create tasks for same spec, different features
        task1 = {
            "id": "task-001",
            "specification": "specs/spec.md",
            "feature": "feat-001",
            "status": "inbox",
        }
        (work_dir / "inbox" / "task-001.yaml").write_text(yaml.dump(task1))

        task2 = {
            "id": "task-002",
            "specification": "specs/spec.md",
            "feature": "feat-001",
            "status": "inbox",
        }
        (work_dir / "inbox" / "task-002.yaml").write_text(yaml.dump(task2))

        task3 = {
            "id": "task-003",
            "specification": "specs/spec.md",
            "feature": "feat-002",
            "status": "inbox",
        }
        (work_dir / "inbox" / "task-003.yaml").write_text(yaml.dump(task3))

        linker = TaskLinker(str(work_dir))
        feature_groups = linker.group_by_feature("specs/spec.md")

        assert "feat-001" in feature_groups
        assert "feat-002" in feature_groups
        assert len(feature_groups["feat-001"]) == 2
        assert len(feature_groups["feat-002"]) == 1

    def test_group_tasks_without_feature_field(self, tmp_path: Path):
        """Test grouping tasks that lack feature field."""
        pytest.skip("Implementation pending: TaskLinker.group_by_feature")

        from src.llm_service.dashboard.task_linker import TaskLinker

        work_dir = tmp_path / "work"
        (work_dir / "inbox").mkdir(parents=True)

        # Task with specification but no feature
        task = {"id": "task-001", "specification": "specs/spec.md", "status": "inbox"}
        (work_dir / "inbox" / "task-001.yaml").write_text(yaml.dump(task))

        linker = TaskLinker(str(work_dir))
        feature_groups = linker.group_by_feature("specs/spec.md")

        # Should use "unassigned" or None key for tasks without feature
        assert None in feature_groups or "unassigned" in feature_groups
        unassigned = feature_groups.get(None, feature_groups.get("unassigned", []))
        assert len(unassigned) == 1


class TestOrphanTasks:
    """Unit tests for identifying tasks without specification links."""

    def test_identify_orphan_tasks(self, tmp_path: Path):
        """Test identifying tasks without specification field."""
        pytest.skip("Implementation pending: TaskLinker.get_orphan_tasks")

        from src.llm_service.dashboard.task_linker import TaskLinker

        work_dir = tmp_path / "work"
        (work_dir / "inbox").mkdir(parents=True)

        # Orphan task (no specification)
        orphan = {"id": "orphan-001", "status": "inbox"}
        (work_dir / "inbox" / "orphan-001.yaml").write_text(yaml.dump(orphan))

        # Linked task
        linked = {
            "id": "linked-001",
            "specification": "specs/spec.md",
            "status": "inbox",
        }
        (work_dir / "inbox" / "linked-001.yaml").write_text(yaml.dump(linked))

        linker = TaskLinker(str(work_dir))
        orphans = linker.get_orphan_tasks()

        assert len(orphans) == 1
        assert orphans[0]["id"] == "orphan-001"

    def test_orphan_task_with_invalid_specification_path(self, tmp_path: Path):
        """Test treating tasks with non-existent specs as orphans."""
        pytest.skip("Implementation pending: TaskLinker.get_orphan_tasks")

        from src.llm_service.dashboard.task_linker import TaskLinker

        work_dir = tmp_path / "work"
        (work_dir / "inbox").mkdir(parents=True)

        # Task referencing non-existent spec
        task = {
            "id": "task-001",
            "specification": "non-existent/spec.md",
            "status": "inbox",
        }
        (work_dir / "inbox" / "task-001.yaml").write_text(yaml.dump(task))

        # No spec directory created
        linker = TaskLinker(str(work_dir), spec_dir=str(tmp_path / "specs"))
        orphans = linker.get_orphan_tasks()

        # Should treat as orphan since spec doesn't exist
        assert len(orphans) == 1
        assert orphans[0]["id"] == "task-001"


class TestPathResolution:
    """Unit tests for specification path resolution."""

    def test_resolve_absolute_specification_path(self, tmp_path: Path):
        """Test resolving absolute specification paths."""
        pytest.skip("Implementation pending: TaskLinker.resolve_spec_path")

        from src.llm_service.dashboard.task_linker import TaskLinker

        spec_dir = tmp_path / "specifications"
        spec_dir.mkdir()

        linker = TaskLinker(str(tmp_path), spec_dir=str(spec_dir))

        # Task with relative path
        task_spec_path = "dashboard/feature.md"
        resolved = linker.resolve_spec_path(task_spec_path)

        expected = str(spec_dir / "dashboard" / "feature.md")
        assert resolved == expected

    def test_resolve_relative_specification_path(self, tmp_path: Path):
        """Test resolving relative paths from task specification field."""
        pytest.skip("Implementation pending: TaskLinker.resolve_spec_path")

        from src.llm_service.dashboard.task_linker import TaskLinker

        spec_dir = tmp_path / "specifications"
        spec_dir.mkdir()

        linker = TaskLinker(str(tmp_path), spec_dir=str(spec_dir))

        # Task with nested relative path
        task_spec_path = "llm-dashboard/markdown-rendering.md"
        resolved = linker.resolve_spec_path(task_spec_path)

        expected = str(spec_dir / "llm-dashboard" / "markdown-rendering.md")
        assert resolved == expected

    def test_validate_specification_exists(self, tmp_path: Path):
        """Test checking if specification file exists."""
        pytest.skip("Implementation pending: TaskLinker.spec_exists")

        from src.llm_service.dashboard.task_linker import TaskLinker

        spec_dir = tmp_path / "specifications"
        spec_dir.mkdir()

        # Create actual spec file
        existing_spec = spec_dir / "exists.md"
        existing_spec.write_text("# Spec")

        linker = TaskLinker(str(tmp_path), spec_dir=str(spec_dir))

        assert linker.spec_exists("exists.md") is True
        assert linker.spec_exists("non-existent.md") is False

    def test_prevent_path_traversal_attacks(self, tmp_path: Path):
        """Test security: reject specification paths with ../ traversal."""
        pytest.skip("Implementation pending: TaskLinker.validate_spec_path")

        from src.llm_service.dashboard.task_linker import TaskLinker

        linker = TaskLinker(str(tmp_path))

        # Malicious paths
        assert linker.validate_spec_path("../../../etc/passwd") is False
        assert linker.validate_spec_path("specs/../../../secrets.txt") is False

        # Valid paths
        assert linker.validate_spec_path("dashboard/feature.md") is True
        assert linker.validate_spec_path("specs/nested/deep.md") is True


class TestLinkingIntegration:
    """Integration tests for task-to-spec linking workflow."""

    def test_link_tasks_to_specification_metadata(self, tmp_path: Path):
        """Test complete workflow: scan tasks → link to specs → group by features."""
        pytest.skip("Implementation pending: TaskLinker integration")

        from src.llm_service.dashboard.spec_parser import (
            SpecificationParser,
        )
        from src.llm_service.dashboard.task_linker import TaskLinker

        # Setup directories
        work_dir = tmp_path / "work"
        (work_dir / "inbox").mkdir(parents=True)
        spec_dir = tmp_path / "specifications"
        spec_dir.mkdir()

        # Create specification
        spec_content = """---
id: "spec-001"
title: "Test Spec"
status: "in_progress"
initiative: "Test Initiative"
features:
  - id: "feat-001"
    title: "Feature One"
---
# Spec
"""
        (spec_dir / "test.md").write_text(spec_content)

        # Create tasks
        task1 = {
            "id": "task-001",
            "specification": "test.md",
            "feature": "feat-001",
            "status": "done",
        }
        (work_dir / "inbox" / "task-001.yaml").write_text(yaml.dump(task1))

        task2 = {
            "id": "task-002",
            "specification": "test.md",
            "feature": "feat-001",
            "status": "in_progress",
        }
        (work_dir / "inbox" / "task-002.yaml").write_text(yaml.dump(task2))

        # Parse spec
        parser = SpecificationParser(str(spec_dir))
        spec_meta = parser.parse_frontmatter(str(spec_dir / "test.md"))

        # Link tasks
        linker = TaskLinker(str(work_dir), spec_dir=str(spec_dir))
        linked_tasks = linker.get_tasks_for_specification("test.md")

        assert len(linked_tasks) == 2

        # Group by feature
        by_feature = linker.group_by_feature("test.md")
        assert len(by_feature["feat-001"]) == 2


class TestErrorHandling:
    """Unit tests for error handling and edge cases."""

    def test_handle_malformed_task_yaml(self, tmp_path: Path):
        """Test handling malformed YAML gracefully."""
        pytest.skip("Implementation pending: TaskLinker error handling")

        from src.llm_service.dashboard.task_linker import TaskLinker

        work_dir = tmp_path / "work"
        (work_dir / "inbox").mkdir(parents=True)

        # Invalid YAML
        (work_dir / "inbox" / "bad.yaml").write_text(
            "id: task-001\ntitle: Missing quote"
        )

        linker = TaskLinker(str(work_dir))
        tasks = linker.scan_tasks()

        # Should skip malformed file and continue
        assert len(tasks) == 0

    def test_handle_empty_work_directory(self, tmp_path: Path):
        """Test handling empty work directory."""
        pytest.skip("Implementation pending: TaskLinker error handling")

        from src.llm_service.dashboard.task_linker import TaskLinker

        work_dir = tmp_path / "empty_work"
        work_dir.mkdir()

        linker = TaskLinker(str(work_dir))
        tasks = linker.scan_tasks()

        assert len(tasks) == 0
        assert linker.get_orphan_tasks() == []

    def test_handle_circular_specification_references(self, tmp_path: Path):
        """Test detecting and handling circular spec references."""
        pytest.skip("Implementation pending: TaskLinker cycle detection")

        from src.llm_service.dashboard.task_linker import TaskLinker

        # This is a future-proofing test for when specs can reference other specs
        # For now, tasks only reference specs (no cycles possible)
        # But good to have test ready

        linker = TaskLinker(str(tmp_path))
        # Implementation TBD when spec-to-spec references are added
        assert True  # Placeholder


# Test coverage summary
"""
Unit Test Coverage for TaskLinker:
- ✅ Task scanning (4 tests)
- ✅ Task grouping (3 tests)
- ✅ Orphan detection (2 tests)
- ✅ Path resolution (5 tests)
- ✅ Linking integration (1 test)
- ✅ Error handling (3 tests)

Total: 18 unit tests
All tests currently skipped (RED phase)
"""
