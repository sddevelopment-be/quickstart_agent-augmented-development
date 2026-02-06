"""
Acceptance tests for Initiative Tracking portfolio view.

Implements ATDD (Directive 016) for ADR-037 Dashboard Initiative Tracking.
These tests define the complete expected behavior before implementation.

Test Scenarios:
1. Parse specification frontmatter correctly
2. Link tasks to features correctly via specification field
3. Calculate progress accurately (task status weights)
4. Handle orphan tasks (no specification link)
5. API returns correct portfolio structure
6. Performance meets targets (<500ms uncached, <50ms cached)
7. Cache invalidation on file changes
"""

import pytest
import os
import tempfile
import time
from pathlib import Path
from typing import Dict, Any
import yaml


@pytest.fixture
def temp_work_dir(tmp_path: Path) -> Path:
    """Create temporary work directory structure."""
    work_dir = tmp_path / "work" / "collaboration"
    
    # Create status directories
    (work_dir / "inbox").mkdir(parents=True)
    (work_dir / "assigned" / "python-pedro").mkdir(parents=True)
    (work_dir / "done" / "python-pedro").mkdir(parents=True)
    
    return work_dir


@pytest.fixture
def temp_spec_dir(tmp_path: Path) -> Path:
    """Create temporary specifications directory."""
    spec_dir = tmp_path / "specifications" / "test-initiative"
    spec_dir.mkdir(parents=True)
    return spec_dir


@pytest.fixture
def sample_spec_with_frontmatter(temp_spec_dir: Path) -> Path:
    """Create a sample specification file with valid frontmatter."""
    spec_content = """---
id: "test-spec-001"
title: "Test Feature Specification"
status: "in_progress"
initiative: "Test Initiative"
priority: "HIGH"
features:
  - id: "feat-001"
    title: "Feature One"
  - id: "feat-002"
    title: "Feature Two"
completion: null
created: "2026-02-06"
updated: "2026-02-06"
author: "analyst-annie"
---

# Test Feature Specification

This is a test specification for acceptance testing.

## Details

Feature details here...
"""
    
    spec_path = temp_spec_dir / "test-feature.md"
    spec_path.write_text(spec_content)
    return spec_path


@pytest.fixture
def sample_tasks(temp_work_dir: Path, sample_spec_with_frontmatter: Path) -> Dict[str, Path]:
    """Create sample task files with various statuses."""
    tasks = {}
    
    # Task 1: Done task linked to feat-001
    task1 = {
        "id": "2026-02-06T1000-test-task-1",
        "title": "Completed Task for Feature One",
        "agent": "python-pedro",
        "status": "done",
        "priority": "HIGH",
        "specification": "test-initiative/test-feature.md",
        "feature": "feat-001",
        "created": "2026-02-06T10:00:00Z",
    }
    task1_path = temp_work_dir / "done" / "python-pedro" / f"{task1['id']}.yaml"
    task1_path.write_text(yaml.dump(task1))
    tasks["task1"] = task1_path
    
    # Task 2: In progress task linked to feat-001
    task2 = {
        "id": "2026-02-06T1100-test-task-2",
        "title": "In Progress Task for Feature One",
        "agent": "python-pedro",
        "status": "in_progress",
        "priority": "MEDIUM",
        "specification": "test-initiative/test-feature.md",
        "feature": "feat-001",
        "created": "2026-02-06T11:00:00Z",
    }
    task2_path = temp_work_dir / "assigned" / "python-pedro" / f"{task2['id']}.yaml"
    task2_path.write_text(yaml.dump(task2))
    tasks["task2"] = task2_path
    
    # Task 3: Inbox task linked to feat-002
    task3 = {
        "id": "2026-02-06T1200-test-task-3",
        "title": "Inbox Task for Feature Two",
        "agent": "python-pedro",
        "status": "inbox",
        "priority": "LOW",
        "specification": "test-initiative/test-feature.md",
        "feature": "feat-002",
        "created": "2026-02-06T12:00:00Z",
    }
    task3_path = temp_work_dir / "inbox" / f"{task3['id']}.yaml"
    task3_path.write_text(yaml.dump(task3))
    tasks["task3"] = task3_path
    
    # Task 4: Orphan task (no specification field)
    task4 = {
        "id": "2026-02-06T1300-test-task-4",
        "title": "Orphan Task Without Specification",
        "agent": "backend-dev",
        "status": "inbox",
        "priority": "MEDIUM",
        "created": "2026-02-06T13:00:00Z",
    }
    task4_path = temp_work_dir / "inbox" / f"{task4['id']}.yaml"
    task4_path.write_text(yaml.dump(task4))
    tasks["task4"] = task4_path
    
    return tasks


class TestSpecificationParsing:
    """Acceptance tests for specification frontmatter parsing."""
    
    def test_parse_valid_specification_frontmatter(
        self, temp_spec_dir: Path, sample_spec_with_frontmatter: Path
    ):
        """
        Given a specification file with valid YAML frontmatter
        When the parser processes the file
        Then it extracts all required metadata fields correctly
        """
        # This test will fail until we implement SpecificationParser
        pytest.skip("Implementation pending: SpecificationParser")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        parser = SpecificationParser(str(temp_spec_dir.parent))
        metadata = parser.parse_frontmatter(str(sample_spec_with_frontmatter))
        
        assert metadata is not None
        assert metadata.id == "test-spec-001"
        assert metadata.title == "Test Feature Specification"
        assert metadata.status == "in_progress"
        assert metadata.initiative == "Test Initiative"
        assert metadata.priority == "HIGH"
        assert len(metadata.features) == 2
        assert metadata.features[0]["id"] == "feat-001"
        assert metadata.features[0]["title"] == "Feature One"
    
    def test_parse_specification_without_frontmatter(self, temp_spec_dir: Path):
        """
        Given a specification file without frontmatter
        When the parser processes the file
        Then it returns None or empty metadata gracefully
        """
        pytest.skip("Implementation pending: SpecificationParser")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        # Create spec without frontmatter
        spec_path = temp_spec_dir / "no-frontmatter.md"
        spec_path.write_text("# Just a title\n\nSome content.")
        
        parser = SpecificationParser(str(temp_spec_dir.parent))
        metadata = parser.parse_frontmatter(str(spec_path))
        
        assert metadata is None
    
    def test_parse_specification_with_malformed_yaml(self, temp_spec_dir: Path):
        """
        Given a specification file with malformed YAML frontmatter
        When the parser processes the file
        Then it handles the error gracefully without crashing
        """
        pytest.skip("Implementation pending: SpecificationParser")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        # Create spec with malformed YAML
        spec_content = """---
id: "test-001"
title: "Missing closing quote
status: in_progress
---

# Content
"""
        spec_path = temp_spec_dir / "malformed.md"
        spec_path.write_text(spec_content)
        
        parser = SpecificationParser(str(temp_spec_dir.parent))
        metadata = parser.parse_frontmatter(str(spec_path))
        
        assert metadata is None  # Should handle gracefully


class TestTaskLinking:
    """Acceptance tests for linking tasks to specifications."""
    
    def test_link_tasks_to_features(
        self, temp_work_dir: Path, sample_spec_with_frontmatter: Path, sample_tasks: Dict[str, Path]
    ):
        """
        Given tasks with specification field pointing to spec files
        When the linker groups tasks by specification
        Then tasks are correctly associated with their features
        """
        pytest.skip("Implementation pending: TaskLinker")
        
        from src.llm_service.dashboard.task_linker import TaskLinker
        
        linker = TaskLinker(str(temp_work_dir))
        task_groups = linker.group_by_specification()
        
        # Should have linked tasks to test-feature.md
        assert "test-initiative/test-feature.md" in task_groups
        linked_tasks = task_groups["test-initiative/test-feature.md"]
        
        # Should have 3 linked tasks (task1, task2, task3)
        assert len(linked_tasks) == 3
        
        # Check feature grouping
        feat_001_tasks = [t for t in linked_tasks if t.get("feature") == "feat-001"]
        feat_002_tasks = [t for t in linked_tasks if t.get("feature") == "feat-002"]
        
        assert len(feat_001_tasks) == 2  # task1 (done), task2 (in_progress)
        assert len(feat_002_tasks) == 1  # task3 (inbox)
    
    def test_identify_orphan_tasks(
        self, temp_work_dir: Path, sample_tasks: Dict[str, Path]
    ):
        """
        Given tasks without specification field
        When the linker scans for orphans
        Then orphan tasks are correctly identified
        """
        pytest.skip("Implementation pending: TaskLinker")
        
        from src.llm_service.dashboard.task_linker import TaskLinker
        
        linker = TaskLinker(str(temp_work_dir))
        orphans = linker.get_orphan_tasks()
        
        # Should identify task4 as orphan
        assert len(orphans) == 1
        assert orphans[0]["id"] == "2026-02-06T1300-test-task-4"
    
    def test_handle_missing_specification_file(self, temp_work_dir: Path):
        """
        Given a task referencing a non-existent specification file
        When the linker processes the task
        Then it handles the missing file gracefully (treat as orphan)
        """
        pytest.skip("Implementation pending: TaskLinker")
        
        from src.llm_service.dashboard.task_linker import TaskLinker
        
        # Create task with invalid spec reference
        invalid_task = {
            "id": "2026-02-06T1400-invalid",
            "title": "Task with missing spec",
            "specification": "non-existent/spec.md",
            "status": "inbox",
        }
        task_path = temp_work_dir / "inbox" / f"{invalid_task['id']}.yaml"
        task_path.write_text(yaml.dump(invalid_task))
        
        linker = TaskLinker(str(temp_work_dir))
        orphans = linker.get_orphan_tasks()
        
        # Should treat as orphan
        assert any(t["id"] == "2026-02-06T1400-invalid" for t in orphans)


class TestProgressCalculation:
    """Acceptance tests for progress calculation logic."""
    
    def test_calculate_feature_progress_with_mixed_statuses(self):
        """
        Given tasks with different statuses (done, in_progress, inbox)
        When calculating feature progress
        Then weighted progress is calculated correctly:
        - done: 100% weight
        - in_progress: 50% weight
        - inbox/assigned: 0% weight
        """
        pytest.skip("Implementation pending: ProgressCalculator")
        
        from src.llm_service.dashboard.progress_calculator import ProgressCalculator
        
        calculator = ProgressCalculator()
        
        # Scenario: 2 done, 1 in_progress, 1 inbox = (2*1.0 + 1*0.5 + 1*0) / 4 = 62.5%
        tasks = [
            {"status": "done"},
            {"status": "done"},
            {"status": "in_progress"},
            {"status": "inbox"},
        ]
        
        progress = calculator.calculate_feature_progress(tasks)
        assert progress == 62  # Rounded to 62%
    
    def test_calculate_initiative_progress_from_features(self):
        """
        Given an initiative with multiple features
        When calculating initiative progress
        Then progress is averaged across features
        """
        pytest.skip("Implementation pending: ProgressCalculator")
        
        from src.llm_service.dashboard.progress_calculator import ProgressCalculator
        
        calculator = ProgressCalculator()
        
        # Scenario: Feature A: 100%, Feature B: 50%, Feature C: 0% = (100+50+0)/3 = 50%
        features = [
            {"progress": 100},
            {"progress": 50},
            {"progress": 0},
        ]
        
        progress = calculator.calculate_initiative_progress(features)
        assert progress == 50
    
    def test_calculate_progress_with_empty_tasks(self):
        """
        Given a feature with no linked tasks
        When calculating progress
        Then progress should be 0%
        """
        pytest.skip("Implementation pending: ProgressCalculator")
        
        from src.llm_service.dashboard.progress_calculator import ProgressCalculator
        
        calculator = ProgressCalculator()
        progress = calculator.calculate_feature_progress([])
        assert progress == 0
    
    def test_respect_manual_completion_override(self):
        """
        Given a specification with manual completion field set
        When calculating initiative progress
        Then manual value takes precedence over calculated value
        """
        pytest.skip("Implementation pending: ProgressCalculator")
        
        from src.llm_service.dashboard.progress_calculator import ProgressCalculator
        
        calculator = ProgressCalculator()
        
        # Metadata with manual completion override
        metadata = {
            "completion": 75,  # Manual override
            "features": [
                {"progress": 100},  # Would calculate to 100%, but override is 75%
            ],
        }
        
        progress = calculator.calculate_initiative_progress_with_override(metadata)
        assert progress == 75  # Uses manual override


class TestPortfolioAPI:
    """Acceptance tests for /api/portfolio endpoint."""
    
    def test_portfolio_endpoint_returns_correct_structure(
        self, temp_work_dir: Path, temp_spec_dir: Path, 
        sample_spec_with_frontmatter: Path, sample_tasks: Dict[str, Path]
    ):
        """
        Given specifications and linked tasks exist
        When GET /api/portfolio is called
        Then response contains initiatives → features → tasks hierarchy
        """
        pytest.skip("Implementation pending: /api/portfolio endpoint")
        
        # This test will integrate with Flask app
        from src.llm_service.dashboard.app import create_app
        
        app, _ = create_app({
            "WORK_DIR": str(temp_work_dir),
            "SPEC_DIR": str(temp_spec_dir.parent),
        })
        
        with app.test_client() as client:
            response = client.get("/api/portfolio")
            assert response.status_code == 200
            
            data = response.get_json()
            
            # Check structure
            assert "initiatives" in data
            assert "orphans" in data
            
            # Check initiative data
            initiatives = data["initiatives"]
            assert len(initiatives) == 1
            
            initiative = initiatives[0]
            assert initiative["id"] == "test-spec-001"
            assert initiative["title"] == "Test Feature Specification"
            assert "progress" in initiative
            assert "features" in initiative
            
            # Check features
            features = initiative["features"]
            assert len(features) == 2
            
            # Feature 1 should have 2 tasks (1 done, 1 in_progress)
            feat1 = next(f for f in features if f["id"] == "feat-001")
            assert len(feat1["tasks"]) == 2
            assert feat1["progress"] == 75  # (1*100 + 1*50) / 2 = 75%
            
            # Check orphans
            orphans = data["orphans"]
            assert len(orphans) == 1
            assert orphans[0]["id"] == "2026-02-06T1300-test-task-4"
    
    def test_portfolio_endpoint_handles_no_specifications(self, temp_work_dir: Path, tmp_path: Path):
        """
        Given no specification files exist
        When GET /api/portfolio is called
        Then response contains empty initiatives list and all tasks as orphans
        """
        pytest.skip("Implementation pending: /api/portfolio endpoint")
        
        from src.llm_service.dashboard.app import create_app
        
        empty_spec_dir = tmp_path / "empty_specs"
        empty_spec_dir.mkdir()
        
        app, _ = create_app({
            "WORK_DIR": str(temp_work_dir),
            "SPEC_DIR": str(empty_spec_dir),
        })
        
        with app.test_client() as client:
            response = client.get("/api/portfolio")
            assert response.status_code == 200
            
            data = response.get_json()
            assert len(data["initiatives"]) == 0


class TestPerformance:
    """Acceptance tests for performance requirements."""
    
    def test_uncached_portfolio_load_performance(
        self, temp_work_dir: Path, temp_spec_dir: Path,
        sample_spec_with_frontmatter: Path, sample_tasks: Dict[str, Path]
    ):
        """
        Given a portfolio with specifications and tasks
        When loading portfolio without cache (cold start)
        Then response time is under 500ms
        """
        pytest.skip("Implementation pending: Performance optimization")
        
        from src.llm_service.dashboard.app import create_app
        
        app, _ = create_app({
            "WORK_DIR": str(temp_work_dir),
            "SPEC_DIR": str(temp_spec_dir.parent),
        })
        
        with app.test_client() as client:
            start_time = time.time()
            response = client.get("/api/portfolio")
            elapsed_ms = (time.time() - start_time) * 1000
            
            assert response.status_code == 200
            assert elapsed_ms < 500, f"Uncached load took {elapsed_ms:.2f}ms (target: <500ms)"
    
    def test_cached_portfolio_load_performance(
        self, temp_work_dir: Path, temp_spec_dir: Path,
        sample_spec_with_frontmatter: Path, sample_tasks: Dict[str, Path]
    ):
        """
        Given a portfolio that has been loaded once
        When loading portfolio again (cached)
        Then response time is under 50ms
        """
        pytest.skip("Implementation pending: Caching layer")
        
        from src.llm_service.dashboard.app import create_app
        
        app, _ = create_app({
            "WORK_DIR": str(temp_work_dir),
            "SPEC_DIR": str(temp_spec_dir.parent),
        })
        
        with app.test_client() as client:
            # Warm up cache
            client.get("/api/portfolio")
            
            # Measure cached load
            start_time = time.time()
            response = client.get("/api/portfolio")
            elapsed_ms = (time.time() - start_time) * 1000
            
            assert response.status_code == 200
            assert elapsed_ms < 50, f"Cached load took {elapsed_ms:.2f}ms (target: <50ms)"


class TestCacheInvalidation:
    """Acceptance tests for cache invalidation on file changes."""
    
    def test_cache_invalidates_on_specification_change(
        self, temp_work_dir: Path, temp_spec_dir: Path,
        sample_spec_with_frontmatter: Path, sample_tasks: Dict[str, Path]
    ):
        """
        Given a cached portfolio
        When a specification file is modified
        Then cache is invalidated and fresh data is returned
        """
        pytest.skip("Implementation pending: File watcher integration")
        
        from src.llm_service.dashboard.app import create_app
        
        app, _ = create_app({
            "WORK_DIR": str(temp_work_dir),
            "SPEC_DIR": str(temp_spec_dir.parent),
        })
        
        with app.test_client() as client:
            # Load portfolio (cache it)
            response1 = client.get("/api/portfolio")
            data1 = response1.get_json()
            original_title = data1["initiatives"][0]["title"]
            
            # Modify specification
            spec_content = sample_spec_with_frontmatter.read_text()
            modified_content = spec_content.replace(
                'title: "Test Feature Specification"',
                'title: "Modified Feature Specification"'
            )
            sample_spec_with_frontmatter.write_text(modified_content)
            
            # Give file watcher time to detect change
            time.sleep(0.2)
            
            # Load portfolio again
            response2 = client.get("/api/portfolio")
            data2 = response2.get_json()
            new_title = data2["initiatives"][0]["title"]
            
            # Should reflect the change
            assert new_title == "Modified Feature Specification"
            assert new_title != original_title
    
    def test_cache_invalidates_on_task_status_change(
        self, temp_work_dir: Path, temp_spec_dir: Path,
        sample_spec_with_frontmatter: Path, sample_tasks: Dict[str, Path]
    ):
        """
        Given a cached portfolio
        When a task status changes
        Then progress calculation is updated
        """
        pytest.skip("Implementation pending: Task change detection")
        
        from src.llm_service.dashboard.app import create_app
        
        app, _ = create_app({
            "WORK_DIR": str(temp_work_dir),
            "SPEC_DIR": str(temp_spec_dir.parent),
        })
        
        with app.test_client() as client:
            # Load portfolio (cache it)
            response1 = client.get("/api/portfolio")
            data1 = response1.get_json()
            original_progress = data1["initiatives"][0]["features"][0]["progress"]
            
            # Move task from in_progress to done
            task2_path = sample_tasks["task2"]
            task2_data = yaml.safe_load(task2_path.read_text())
            task2_data["status"] = "done"
            task2_path.write_text(yaml.dump(task2_data))
            
            # Give file watcher time to detect change
            time.sleep(0.2)
            
            # Load portfolio again
            response2 = client.get("/api/portfolio")
            data2 = response2.get_json()
            new_progress = data2["initiatives"][0]["features"][0]["progress"]
            
            # Progress should increase (was 75%, now 100%)
            assert new_progress > original_progress
            assert new_progress == 100  # Both tasks for feat-001 now done


# Test coverage summary for work log
"""
Acceptance Test Coverage:
- ✅ Specification parsing (3 scenarios)
- ✅ Task linking (3 scenarios)
- ✅ Progress calculation (4 scenarios)
- ✅ API endpoint (2 scenarios)
- ✅ Performance (2 scenarios)
- ✅ Cache invalidation (2 scenarios)

Total: 16 acceptance test scenarios
All tests currently skipped (RED phase) - will pass as implementation progresses
"""
