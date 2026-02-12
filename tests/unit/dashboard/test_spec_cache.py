"""
Unit tests for SpecificationCache.

Implements TDD (Directive 017) - RED-GREEN-REFACTOR cycle.
Tests individual units of functionality in isolation.

Tests:
- Cache hit/miss logic
- Manual invalidation
- File watcher integration
- Edge cases (malformed YAML, missing files, permissions)
"""

import time
from pathlib import Path

import pytest


class TestSpecificationCacheUnit:
    """Unit tests for SpecificationCache implementation."""

    @pytest.fixture
    def spec_dir(self, tmp_path: Path) -> Path:
        """Create temporary directory for test specifications."""
        specs_dir = tmp_path / "specifications"
        specs_dir.mkdir()
        return specs_dir

    @pytest.fixture
    def sample_spec_file(self, spec_dir: Path) -> Path:
        """Create a sample specification file."""
        spec_path = spec_dir / "test-spec.md"
        content = """---
id: SPEC-TEST-001
title: Test Specification
status: draft
initiative: Test Initiative
priority: MEDIUM
features:
  - id: FEAT-001
    title: Feature One
---

# Test Specification

Content here.
"""
        spec_path.write_text(content)
        return spec_path

    # ========================================================================
    # Initialization Tests
    # ========================================================================

    def test_cache_initialization(self, spec_dir: Path):
        """
        Test cache initializes with empty cache and no file watcher.

        GREEN phase: Implementation complete.
        """
        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        assert cache.cache == {}
        assert cache.file_watcher is None
        assert cache.base_dir == Path(spec_dir)

    def test_cache_initialization_with_relative_path(self, tmp_path: Path):
        """Test cache converts relative paths to absolute."""
        # Use relative path
        import os

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        os.chdir(tmp_path)

        cache = SpecificationCache("specifications")

        # Assert: Path is converted to absolute
        assert cache.base_dir.is_absolute()

    # ========================================================================
    # Cache Hit/Miss Tests
    # ========================================================================

    def test_cache_miss_parses_and_caches(self, spec_dir: Path, sample_spec_file: Path):
        """
        Test cache miss triggers parse and stores in cache.

        GIVEN a spec not in cache
        WHEN get_spec is called
        THEN the spec is parsed and cached
        """
        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        # Initial cache is empty
        assert len(cache.cache) == 0

        # Get spec (cache miss)
        result = cache.get_spec(str(sample_spec_file))

        # Assert: Spec was parsed
        assert result is not None
        assert result.id == "SPEC-TEST-001"
        assert result.title == "Test Specification"

        # Assert: Spec is now cached
        assert len(cache.cache) == 1
        assert str(sample_spec_file) in cache.cache

    def test_cache_hit_returns_cached_data(
        self, spec_dir: Path, sample_spec_file: Path
    ):
        """
        Test cache hit returns cached data without re-parsing.

        GIVEN a spec already in cache
        WHEN get_spec is called
        THEN cached data is returned (no file I/O)
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        # First call (cache miss)
        first_result = cache.get_spec(str(sample_spec_file))

        # Modify file (but cache should not re-read)
        sample_spec_file.write_text("---\nid: MODIFIED\n---\n")

        # Second call (cache hit)
        second_result = cache.get_spec(str(sample_spec_file))

        # Assert: Returns cached data (not modified data)
        assert second_result.id == "SPEC-TEST-001"  # Original, not MODIFIED

        # Assert: Both results are the same object reference
        assert first_result is second_result

    def test_get_spec_returns_none_for_missing_file(self, spec_dir: Path):
        """
        Test get_spec returns None for non-existent file.

        GIVEN a file that doesn't exist
        WHEN get_spec is called
        THEN None is returned (no exception)
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        result = cache.get_spec(str(spec_dir / "nonexistent.md"))

        assert result is None

    def test_get_spec_handles_malformed_yaml(self, spec_dir: Path):
        """
        Test get_spec handles malformed YAML gracefully.

        GIVEN a file with invalid YAML frontmatter
        WHEN get_spec is called
        THEN None is returned with logged warning
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        bad_spec = spec_dir / "bad-spec.md"
        bad_spec.write_text("""---
id: SPEC-BAD
title: Unclosed quote "
---
""")

        cache = SpecificationCache(str(spec_dir))

        # Should not raise exception
        result = cache.get_spec(str(bad_spec))

        assert result is None

    def test_get_spec_handles_missing_required_fields(self, spec_dir: Path):
        """
        Test get_spec handles specs missing required frontmatter fields.

        GIVEN a file missing required fields (e.g., no 'title')
        WHEN get_spec is called
        THEN None is returned
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        incomplete_spec = spec_dir / "incomplete.md"
        incomplete_spec.write_text("""---
id: SPEC-INCOMPLETE
status: draft
---
""")

        cache = SpecificationCache(str(spec_dir))
        result = cache.get_spec(str(incomplete_spec))

        assert result is None

    # ========================================================================
    # Manual Invalidation Tests
    # ========================================================================

    def test_invalidate_removes_from_cache(
        self, spec_dir: Path, sample_spec_file: Path
    ):
        """
        Test invalidate() removes spec from cache.

        GIVEN a cached spec
        WHEN invalidate is called
        THEN the spec is removed from cache
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        # Load into cache
        cache.get_spec(str(sample_spec_file))
        assert str(sample_spec_file) in cache.cache

        # Invalidate
        cache.invalidate(str(sample_spec_file))

        # Assert: Removed from cache
        assert str(sample_spec_file) not in cache.cache

    def test_invalidate_nonexistent_spec_is_safe(self, spec_dir: Path):
        """
        Test invalidate() handles non-existent cache entry safely.

        GIVEN a spec not in cache
        WHEN invalidate is called
        THEN no error is raised
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        # Should not raise exception
        cache.invalidate("nonexistent-path")

    def test_invalidate_triggers_reparse_on_next_get(
        self, spec_dir: Path, sample_spec_file: Path
    ):
        """
        Test spec is re-parsed after invalidation.

        GIVEN a cached spec
        WHEN invalidate is called and file is modified
        THEN next get_spec returns updated data
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        # Initial load
        original = cache.get_spec(str(sample_spec_file))
        assert original.title == "Test Specification"

        # Invalidate
        cache.invalidate(str(sample_spec_file))

        # Modify file
        sample_spec_file.write_text("""---
id: SPEC-TEST-001
title: Updated Title
status: in_progress
initiative: Test Initiative
priority: HIGH
---
""")

        # Get again (should re-parse)
        updated = cache.get_spec(str(sample_spec_file))

        assert updated.title == "Updated Title"
        assert updated.status == "in_progress"

    # ========================================================================
    # Preload Tests
    # ========================================================================

    def test_preload_all_scans_directory(self, spec_dir: Path):
        """
        Test preload_all() scans directory and caches all specs.

        GIVEN a directory with multiple specs
        WHEN preload_all is called
        THEN all valid specs are loaded into cache
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        # Create multiple specs
        for i in range(5):
            spec = spec_dir / f"spec-{i}.md"
            spec.write_text(f"""---
id: SPEC-{i:03d}
title: Spec {i}
status: draft
initiative: Test
priority: MEDIUM
---
""")

        cache = SpecificationCache(str(spec_dir))
        cache.preload_all()

        # Assert: All 5 specs cached
        assert len(cache.cache) == 5

    def test_preload_all_skips_invalid_specs(self, spec_dir: Path):
        """
        Test preload_all() skips invalid specs without failing.

        GIVEN a directory with valid and invalid specs
        WHEN preload_all is called
        THEN only valid specs are cached
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        # Create valid spec
        valid = spec_dir / "valid.md"
        valid.write_text("""---
id: SPEC-VALID
title: Valid
status: draft
initiative: Test
---
""")

        # Create invalid spec (bad YAML)
        invalid = spec_dir / "invalid.md"
        invalid.write_text("""---
bad yaml: [unclosed
---
""")

        cache = SpecificationCache(str(spec_dir))
        cache.preload_all()

        # Assert: Only valid spec cached
        assert len(cache.cache) == 1
        assert str(valid) in cache.cache

    # ========================================================================
    # Get All Specs Tests
    # ========================================================================

    def test_get_all_specs_returns_cached_list(self, spec_dir: Path):
        """
        Test get_all_specs() returns list of all cached specs.

        GIVEN multiple cached specs
        WHEN get_all_specs is called
        THEN list of SpecificationMetadata is returned
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        # Create specs
        for i in range(3):
            spec = spec_dir / f"spec-{i}.md"
            spec.write_text(f"""---
id: SPEC-{i}
title: Spec {i}
status: draft
initiative: Initiative-A
priority: MEDIUM
---
""")

        cache = SpecificationCache(str(spec_dir))
        cache.preload_all()

        all_specs = cache.get_all_specs()

        assert len(all_specs) == 3
        assert all(hasattr(spec, "id") for spec in all_specs)
        assert all(hasattr(spec, "title") for spec in all_specs)

    # ========================================================================
    # File Watcher Tests
    # ========================================================================

    def test_start_file_watcher_creates_observer(self, spec_dir: Path):
        """
        Test start_file_watcher() creates and starts watchdog Observer.

        WHEN start_file_watcher is called
        THEN an Observer is created and started
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))
        cache.start_file_watcher()

        try:
            assert cache.file_watcher is not None
            assert cache.file_watcher.is_alive()  # Observer thread is running
        finally:
            cache.stop_file_watcher()

    def test_stop_file_watcher_stops_observer(self, spec_dir: Path):
        """
        Test stop_file_watcher() stops the Observer.

        GIVEN a running file watcher
        WHEN stop_file_watcher is called
        THEN the Observer is stopped
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))
        cache.start_file_watcher()

        # Stop watcher
        cache.stop_file_watcher()

        # Observer should be stopped
        assert not cache.file_watcher.is_alive()

    def test_file_watcher_detects_modification(
        self, spec_dir: Path, sample_spec_file: Path
    ):
        """
        Test file watcher detects file modifications and invalidates cache.

        GIVEN a running file watcher
        WHEN a spec file is modified
        THEN the cache entry is invalidated
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        # Load spec into cache
        cache.get_spec(str(sample_spec_file))
        assert str(sample_spec_file) in cache.cache

        # Start watcher
        cache.start_file_watcher()

        try:
            # Modify file
            sample_spec_file.write_text("""---
id: SPEC-MODIFIED
title: Modified
status: draft
initiative: Test
---
""")

            # Wait for file watcher event (small delay)
            time.sleep(0.15)

            # Assert: Cache entry was invalidated
            assert str(sample_spec_file) not in cache.cache

        finally:
            cache.stop_file_watcher()

    def test_file_watcher_detects_deletion(
        self, spec_dir: Path, sample_spec_file: Path
    ):
        """
        Test file watcher detects file deletion and removes from cache.

        GIVEN a running file watcher
        WHEN a spec file is deleted
        THEN the cache entry is removed
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        # Load spec
        cache.get_spec(str(sample_spec_file))

        cache.start_file_watcher()

        try:
            # Delete file
            sample_spec_file.unlink()

            # Wait for event
            time.sleep(0.15)

            # Assert: Removed from cache
            assert str(sample_spec_file) not in cache.cache

        finally:
            cache.stop_file_watcher()

    def test_double_start_watcher_is_safe(self, spec_dir: Path):
        """
        Test calling start_file_watcher() twice is safe.

        GIVEN a running file watcher
        WHEN start_file_watcher is called again
        THEN no error occurs (idempotent)
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        cache = SpecificationCache(str(spec_dir))

        try:
            cache.start_file_watcher()
            cache.start_file_watcher()  # Should be safe

            assert cache.file_watcher is not None
        finally:
            cache.stop_file_watcher()

    # ========================================================================
    # Edge Case Tests
    # ========================================================================

    def test_cache_handles_permission_error(self, spec_dir: Path):
        """
        Test cache handles permission errors gracefully.

        GIVEN a file with read permission denied
        WHEN get_spec is called
        THEN None is returned with logged error
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        restricted = spec_dir / "restricted.md"
        restricted.write_text("""---
id: SPEC-RESTRICTED
title: Restricted
status: draft
initiative: Test
---
""")

        # Remove read permissions
        import os

        os.chmod(restricted, 0o000)

        try:
            cache = SpecificationCache(str(spec_dir))
            result = cache.get_spec(str(restricted))

            assert result is None
        finally:
            # Restore permissions for cleanup
            os.chmod(restricted, 0o644)

    def test_cache_handles_empty_file(self, spec_dir: Path):
        """
        Test cache handles empty files gracefully.

        GIVEN an empty file
        WHEN get_spec is called
        THEN None is returned
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        empty = spec_dir / "empty.md"
        empty.write_text("")

        cache = SpecificationCache(str(spec_dir))
        result = cache.get_spec(str(empty))

        assert result is None

    def test_cache_handles_no_frontmatter(self, spec_dir: Path):
        """
        Test cache handles files without frontmatter.

        GIVEN a markdown file without YAML frontmatter
        WHEN get_spec is called
        THEN None is returned
        """

        from src.llm_service.dashboard.spec_cache import SpecificationCache

        no_fm = spec_dir / "no-frontmatter.md"
        no_fm.write_text("""# Just a regular markdown file

No frontmatter here.
""")

        cache = SpecificationCache(str(spec_dir))
        result = cache.get_spec(str(no_fm))

        assert result is None
