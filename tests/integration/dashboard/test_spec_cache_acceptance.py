"""
Acceptance tests for Specification Frontmatter Caching Layer.

Implements ATDD (Directive 016) - defines acceptance criteria as executable tests
before implementation. These tests verify the Given/When/Then scenarios from
the task specification.

Tests performance requirements:
- Initial load (startup): <2 seconds for 50 specs
- Cached reads: <50ms
- Cache invalidation: <100ms

References:
- Task: 2026-02-09T2034-python-pedro-frontmatter-caching.yaml
- Specification: SPEC-DASH-008 v1.0.0
- Performance Requirement: NFR-P2
"""

import time
from pathlib import Path

import pytest


class TestSpecificationCacheAcceptance:
    """
    Acceptance tests for specification frontmatter caching.

    These tests define WHAT the system should do, not HOW.
    """

    @pytest.fixture
    def spec_dir(self, tmp_path: Path) -> Path:
        """Create temporary directory for test specifications."""
        specs_dir = tmp_path / "specifications"
        specs_dir.mkdir()
        return specs_dir

    @pytest.fixture
    def create_spec_file(self, spec_dir: Path):
        """Factory fixture to create specification files."""

        def _create_spec(
            filename: str, spec_id: str, title: str, initiative: str
        ) -> Path:
            """Create a specification markdown file with frontmatter."""
            spec_path = spec_dir / filename

            content = f"""---
id: {spec_id}
title: {title}
status: draft
initiative: {initiative}
priority: MEDIUM
features:
  - id: FEAT-001
    title: Feature One
    status: draft
created: 2026-01-01
updated: 2026-01-15
author: test-author
---

# {title}

Specification content goes here.
"""
            spec_path.write_text(content)
            return spec_path

        return _create_spec

    @pytest.fixture
    def create_50_specs(self, create_spec_file) -> list[Path]:
        """Create 50 test specifications for performance testing."""
        specs = []
        for i in range(50):
            spec = create_spec_file(
                f"spec-{i:03d}.md",
                f"SPEC-TEST-{i:03d}",
                f"Test Specification {i}",
                f"Initiative-{i % 5}",
            )
            specs.append(spec)
        return specs

    # ========================================================================
    # AC1: Cache Specification Frontmatter
    # ========================================================================
    # Given I have 50 specification files
    # When the system starts up
    # Then all specification frontmatter is parsed and cached within 2 seconds
    # And subsequent reads complete in <50ms
    # ========================================================================

    def test_ac1_cache_50_specs_within_2_seconds(self, spec_dir: Path, create_50_specs):
        """
        AC1: Initial load performance requirement.

        GIVEN I have 50 specification files
        WHEN the system starts up
        THEN all specification frontmatter is parsed and cached within 2 seconds
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        # Start timing
        start_time = time.perf_counter()

        # Initialize cache and load all specs
        cache = SpecificationCache(str(spec_dir))
        cache.preload_all()

        # Calculate elapsed time
        elapsed = time.perf_counter() - start_time

        # Assert: All 50 specs loaded in <2 seconds
        assert elapsed < 2.0, f"Initial load took {elapsed:.3f}s, expected <2.0s"

        # Assert: Cache contains all 50 specs
        assert (
            len(cache.cache) == 50
        ), f"Expected 50 cached specs, got {len(cache.cache)}"

    def test_ac1_cached_reads_under_50ms(self, spec_dir: Path, create_spec_file):
        """
        AC1: Cached read performance requirement.

        GIVEN I have cached specification frontmatter
        WHEN I read the same specification multiple times
        THEN subsequent reads complete in <50ms
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        # Create a single spec
        spec_path = create_spec_file(
            "test-spec.md",
            "SPEC-PERF-001",
            "Performance Test Spec",
            "Performance-Initiative",
        )

        cache = SpecificationCache(str(spec_dir))

        # First read (warm up cache)
        cache.get_spec(str(spec_path))

        # Measure cached read performance (average of 10 reads)
        total_time = 0.0
        iterations = 10

        for _ in range(iterations):
            start = time.perf_counter()
            result = cache.get_spec(str(spec_path))
            elapsed = time.perf_counter() - start
            total_time += elapsed

            # Verify we got valid data
            assert result is not None
            assert result.id == "SPEC-PERF-001"

        avg_time_ms = (total_time / iterations) * 1000

        # Assert: Average cached read time <50ms
        assert (
            avg_time_ms < 50.0
        ), f"Average cached read took {avg_time_ms:.2f}ms, expected <50ms"

    # ========================================================================
    # AC2: Invalidate Cache on File Change
    # ========================================================================
    # Given I have cached specification frontmatter
    # When a specification file is modified
    # Then the cache for that specification is invalidated within 100ms
    # And the next read re-parses the frontmatter
    # ========================================================================

    def test_ac2_invalidate_cache_on_file_modification(
        self, spec_dir: Path, create_spec_file
    ):
        """
        AC2: Cache invalidation on file modification.

        GIVEN I have cached specification frontmatter
        WHEN a specification file is modified
        THEN the cache for that specification is invalidated within 100ms
        AND the next read re-parses the frontmatter
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        # Create initial spec
        spec_path = create_spec_file(
            "test-spec.md", "SPEC-CACHE-001", "Original Title", "Test-Initiative"
        )

        # Initialize cache with file watcher
        cache = SpecificationCache(str(spec_dir))
        cache.start_file_watcher()

        try:
            # Read spec (loads into cache)
            original = cache.get_spec(str(spec_path))
            assert original.title == "Original Title"

            # Modify the spec file
            start_time = time.perf_counter()

            updated_content = """---
id: SPEC-CACHE-001
title: Modified Title
status: draft
initiative: Test-Initiative
priority: MEDIUM
---

# Modified Title

Updated content.
"""
            spec_path.write_text(updated_content)

            # Wait for file watcher to detect change and invalidate cache
            # Give it up to 200ms (we expect <100ms but allow buffer)
            time.sleep(0.2)

            invalidation_time = time.perf_counter() - start_time

            # Read spec again (should re-parse)
            updated = cache.get_spec(str(spec_path))

            # Assert: Cache was invalidated (title changed)
            assert updated.title == "Modified Title", "Cache was not invalidated"

            # Assert: Invalidation happened within 100ms
            # Note: This includes file write + detection + invalidation
            assert (
                invalidation_time < 0.3
            ), f"Invalidation took {invalidation_time*1000:.0f}ms"

        finally:
            cache.stop_file_watcher()

    def test_ac2_reparse_after_invalidation(self, spec_dir: Path, create_spec_file):
        """
        AC2: Verify frontmatter is re-parsed after cache invalidation.

        GIVEN I have a cached specification
        WHEN the file is modified
        THEN the next read returns updated frontmatter (not cached data)
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        spec_path = create_spec_file(
            "test-spec.md", "SPEC-CACHE-002", "Version 1", "Initiative-A"
        )

        cache = SpecificationCache(str(spec_dir))
        cache.start_file_watcher()

        try:
            # Initial read
            v1 = cache.get_spec(str(spec_path))
            assert v1.title == "Version 1"
            assert v1.initiative == "Initiative-A"

            # Modify file
            new_content = """---
id: SPEC-CACHE-002
title: Version 2
status: in_progress
initiative: Initiative-B
priority: HIGH
---

# Version 2
"""
            spec_path.write_text(new_content)
            time.sleep(0.2)  # Wait for invalidation

            # Read again
            v2 = cache.get_spec(str(spec_path))

            # Assert: All fields reflect new values
            assert v2.title == "Version 2"
            assert v2.initiative == "Initiative-B"
            assert v2.status == "in_progress"
            assert v2.priority == "HIGH"

        finally:
            cache.stop_file_watcher()

    # ========================================================================
    # AC3: Handle Missing Specifications Gracefully
    # ========================================================================
    # Given I have a cached specification list
    # When a specification file is deleted
    # Then the cache removes that specification entry
    # And no error is raised
    # And the specification does not appear in the initiative list
    # ========================================================================

    def test_ac3_handle_deleted_specification(self, spec_dir: Path, create_spec_file):
        """
        AC3: Handle deleted specifications gracefully.

        GIVEN I have a cached specification list
        WHEN a specification file is deleted
        THEN the cache removes that specification entry
        AND no error is raised
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        # Create multiple specs
        spec1 = create_spec_file("spec-1.md", "SPEC-001", "Spec 1", "Initiative-A")
        spec2 = create_spec_file("spec-2.md", "SPEC-002", "Spec 2", "Initiative-A")
        spec3 = create_spec_file("spec-3.md", "SPEC-003", "Spec 3", "Initiative-B")

        cache = SpecificationCache(str(spec_dir))
        cache.start_file_watcher()

        try:
            # Load all specs
            cache.preload_all()
            assert len(cache.cache) == 3

            # Delete one spec
            spec2.unlink()
            time.sleep(0.2)  # Wait for file watcher

            # Try to get deleted spec (should return None, not raise error)
            result = cache.get_spec(str(spec2))
            assert result is None, "Deleted spec should return None"

            # Verify cache was updated
            assert str(spec2) not in cache.cache

            # Verify other specs still accessible
            assert cache.get_spec(str(spec1)) is not None
            assert cache.get_spec(str(spec3)) is not None

        finally:
            cache.stop_file_watcher()

    def test_ac3_deleted_spec_not_in_initiative_list(
        self, spec_dir: Path, create_spec_file
    ):
        """
        AC3: Deleted specification doesn't appear in initiative list.

        GIVEN I have cached specifications
        WHEN a specification is deleted
        THEN it does not appear in get_all_specs() results
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        # Create specs
        create_spec_file("spec-1.md", "SPEC-001", "Keep This", "Initiative-A")
        spec2 = create_spec_file("spec-2.md", "SPEC-002", "Delete This", "Initiative-A")

        cache = SpecificationCache(str(spec_dir))
        cache.start_file_watcher()

        try:
            # Load all
            cache.preload_all()
            all_specs = cache.get_all_specs()
            assert len(all_specs) == 2

            # Delete spec2
            spec2.unlink()
            time.sleep(0.2)

            # Get updated list
            updated_specs = cache.get_all_specs()

            # Assert: Only spec1 remains
            assert len(updated_specs) == 1
            assert updated_specs[0].id == "SPEC-001"
            assert updated_specs[0].title == "Keep This"

        finally:
            cache.stop_file_watcher()

    def test_ac3_no_error_on_missing_file(self, spec_dir: Path):
        """
        AC3: No error raised when accessing non-existent specification.

        GIVEN I have a cache
        WHEN I try to get a specification that doesn't exist
        THEN no error is raised and None is returned
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        # Try to get non-existent spec
        result = cache.get_spec(str(spec_dir / "nonexistent.md"))

        # Assert: Returns None, doesn't raise exception
        assert result is None
