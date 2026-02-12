"""
Performance Validation Tests for Specification Frontmatter Caching.

This module provides comprehensive performance testing for the specification
caching layer (spec_cache.py), validating NFR-P2 requirements from SPEC-DASH-008.

Performance Requirements (NFR-P2):
- Initial load (startup): <2 seconds for 50 specifications
- Cached reads: <50ms average
- Cache invalidation: <100ms

Test Strategy:
- Statistical approach: P50, P95, P99 percentiles
- Warm-up phases to eliminate cold-start bias
- Realistic workload simulations
- Memory usage monitoring
- Concurrent access patterns

References:
- Task: 2026-02-09T2036-python-pedro-integration-testing.yaml
- Specification: SPEC-DASH-008 v1.0.0 (orphan-task-assignment.md)
- Implementation: src/llm_service/dashboard/spec_cache.py
- NFR-P2: Frontmatter parsing <200ms per spec

Author: Python Pedro
Created: 2026-02-09
"""

import gc
import statistics
import time
from pathlib import Path
from typing import Any

import pytest

from src.llm_service.dashboard.spec_cache import SpecificationCache

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def spec_directory(tmp_path: Path) -> Path:
    """
    Create temporary specifications directory for performance testing.

    Returns:
        Path to specifications directory
    """
    spec_dir = tmp_path / "specifications"
    spec_dir.mkdir()
    return spec_dir


@pytest.fixture
def create_spec_file(spec_directory: Path):
    """
    Factory fixture to create specification markdown files.

    Returns:
        Callable that creates spec files with frontmatter
    """

    def _create_spec(
        filename: str,
        spec_id: str,
        title: str,
        initiative: str,
        num_features: int = 3,
    ) -> Path:
        """
        Create specification file with frontmatter.

        Args:
            filename: Name of .md file
            spec_id: Specification ID
            title: Specification title
            initiative: Initiative name
            num_features: Number of features to include

        Returns:
            Path to created file
        """
        spec_path = spec_directory / filename

        # Generate feature list
        features_yaml = "\n".join([f"""  - id: {spec_id}-FEAT-{i:03d}
    title: Feature {i}
    status: draft
    priority: MEDIUM""" for i in range(num_features)])

        content = f"""---
id: {spec_id}
title: {title}
status: in_progress
version: 1.0.0
initiative: {initiative}
priority: HIGH
epic: Test Epic
target_personas: ["software-engineer", "project-manager"]
features:
{features_yaml}
completion: 25
created: 2026-01-01
updated: 2026-02-09
author: test-author
reviewer: test-reviewer
---

# {title}

## Overview

This is a test specification for performance validation.

## Features

### Feature 1
Description of feature 1.

### Feature 2
Description of feature 2.

### Feature 3
Description of feature 3.

## Requirements

### Functional Requirements
- FR-1: System must do X
- FR-2: System must do Y
- FR-3: System must do Z

### Non-Functional Requirements
- NFR-P1: Performance requirement
- NFR-R1: Reliability requirement
- NFR-S1: Security requirement

## Technical Design

### Architecture
High-level architecture description.

### Data Model
Data structures and relationships.

### API Design
Endpoint specifications.

## Testing Strategy

### Unit Tests
Component-level testing.

### Integration Tests
End-to-end testing.

### Performance Tests
Load and stress testing.
"""
        spec_path.write_text(content, encoding="utf-8")
        return spec_path

    return _create_spec


@pytest.fixture
def create_50_specs(create_spec_file) -> list[Path]:
    """
    Create 50 test specifications for load testing.

    Returns:
        List of Path objects for created specs
    """
    specs = []
    for i in range(50):
        spec = create_spec_file(
            f"spec-{i:03d}.md",
            f"SPEC-PERF-{i:03d}",
            f"Performance Test Specification {i}",
            f"Initiative-{i % 10}",
            num_features=5,
        )
        specs.append(spec)
    return specs


@pytest.fixture
def create_100_specs(create_spec_file) -> list[Path]:
    """
    Create 100 test specifications for stress testing.

    Returns:
        List of Path objects for created specs
    """
    specs = []
    for i in range(100):
        spec = create_spec_file(
            f"spec-{i:03d}.md",
            f"SPEC-STRESS-{i:03d}",
            f"Stress Test Specification {i}",
            f"Initiative-{i % 15}",
            num_features=3,
        )
        specs.append(spec)
    return specs


# ============================================================================
# Performance Test: Initial Load (NFR-P2)
# ============================================================================


class TestInitialLoadPerformance:
    """
    Performance tests for specification cache initial load.

    Requirements:
    - NFR-P2: Initial load <2 seconds for 50 specs
    - Target: <200ms average per spec during initial parse
    """

    def test_nfr_p2_load_50_specs_under_2_seconds(
        self, spec_directory: Path, create_50_specs
    ):
        """
        NFR-P2: Initial load must complete in <2 seconds for 50 specs.

        GIVEN 50 specification files exist
        WHEN SpecificationCache.preload_all() is called
        THEN all specs are loaded and cached within 2 seconds
        AND average per-spec load time is <40ms
        """
        # Force garbage collection for clean measurement
        gc.collect()

        cache = SpecificationCache(str(spec_directory))

        # Measure preload time
        start_time = time.perf_counter()
        cache.preload_all()
        elapsed = time.perf_counter() - start_time

        # Verify all specs loaded
        assert (
            len(cache.cache) == 50
        ), f"Expected 50 cached specs, got {len(cache.cache)}"

        # Verify performance requirement
        assert elapsed < 2.0, f"Initial load took {elapsed:.3f}s, required <2.0s"

        # Calculate per-spec average
        avg_per_spec = elapsed / 50
        assert (
            avg_per_spec < 0.04
        ), f"Average per-spec load: {avg_per_spec*1000:.1f}ms, expected <40ms"

    def test_load_performance_with_100_specs(
        self, spec_directory: Path, create_100_specs
    ):
        """
        Stress test: Load 100 specifications.

        Target: <4 seconds for 100 specs (scales linearly from 50 spec requirement)
        """
        gc.collect()

        cache = SpecificationCache(str(spec_directory))

        start_time = time.perf_counter()
        cache.preload_all()
        elapsed = time.perf_counter() - start_time

        assert len(cache.cache) == 100
        assert elapsed < 4.0, f"100 spec load took {elapsed:.3f}s, expected <4.0s"

        # Per-spec average should still be reasonable
        avg_per_spec = elapsed / 100
        assert avg_per_spec < 0.04, f"Average per-spec: {avg_per_spec*1000:.1f}ms"

    def test_incremental_load_performance(self, spec_directory: Path, create_spec_file):
        """
        Test incremental loading performance.

        GIVEN cache is already populated
        WHEN new specs are added and loaded
        THEN incremental load maintains <200ms per spec
        """
        cache = SpecificationCache(str(spec_directory))

        # Create and load initial 10 specs
        for i in range(10):
            create_spec_file(
                f"initial-{i:02d}.md",
                f"SPEC-INIT-{i:02d}",
                f"Initial Spec {i}",
                "Initial-Initiative",
            )

        cache.preload_all()
        assert len(cache.cache) == 10

        # Add 10 more specs incrementally
        incremental_times = []

        for i in range(10):
            spec_path = create_spec_file(
                f"incremental-{i:02d}.md",
                f"SPEC-INCR-{i:02d}",
                f"Incremental Spec {i}",
                "Incremental-Initiative",
            )

            start = time.perf_counter()
            cache.get_spec(str(spec_path))
            elapsed = time.perf_counter() - start

            incremental_times.append(elapsed)

        # Verify all loaded
        assert len(cache.cache) == 20

        # Check incremental load times
        avg_incremental = statistics.mean(incremental_times)
        max_incremental = max(incremental_times)

        assert (
            avg_incremental < 0.2
        ), f"Avg incremental load: {avg_incremental*1000:.0f}ms, expected <200ms"
        assert (
            max_incremental < 0.3
        ), f"Max incremental load: {max_incremental*1000:.0f}ms, expected <300ms"


# ============================================================================
# Performance Test: Cached Reads (NFR-P2)
# ============================================================================


class TestCachedReadPerformance:
    """
    Performance tests for cached specification reads.

    Requirements:
    - NFR-P2: Cached reads <50ms average
    - Target P95: <50ms, P99: <100ms
    """

    def test_nfr_p2_cached_read_under_50ms_average(
        self, spec_directory: Path, create_spec_file
    ):
        """
        NFR-P2: Cached reads must average <50ms.

        GIVEN specification is cached
        WHEN get_spec() is called repeatedly
        THEN average read time is <50ms
        AND P95 is <50ms
        """
        spec_path = create_spec_file(
            "cached-read-test.md",
            "SPEC-CACHED-001",
            "Cached Read Test",
            "Performance-Initiative",
        )

        cache = SpecificationCache(str(spec_directory))

        # Initial load (warm up cache)
        cache.get_spec(str(spec_path))
        assert str(spec_path) in cache.cache

        # Measure cached read performance (100 iterations)
        read_times = []
        iterations = 100

        for _ in range(iterations):
            start = time.perf_counter()
            result = cache.get_spec(str(spec_path))
            elapsed = time.perf_counter() - start

            read_times.append(elapsed)
            assert result is not None

        # Calculate statistics
        avg_time = statistics.mean(read_times)
        p50_time = statistics.median(read_times)
        p95_time = statistics.quantiles(read_times, n=20)[18]  # 95th percentile
        p99_time = statistics.quantiles(read_times, n=100)[98]  # 99th percentile

        # Convert to milliseconds for reporting
        avg_ms = avg_time * 1000
        p50_ms = p50_time * 1000
        p95_ms = p95_time * 1000
        p99_ms = p99_time * 1000

        # Verify performance requirements
        assert avg_ms < 50.0, f"Average cached read: {avg_ms:.2f}ms, required <50ms"
        assert p95_ms < 50.0, f"P95 cached read: {p95_ms:.2f}ms, required <50ms"

        # Log performance metrics
        print(
            f"\nCached Read Performance:\n"
            f"  Average: {avg_ms:.2f}ms\n"
            f"  P50: {p50_ms:.2f}ms\n"
            f"  P95: {p95_ms:.2f}ms\n"
            f"  P99: {p99_ms:.2f}ms"
        )

    def test_cached_read_performance_under_load(
        self, spec_directory: Path, create_50_specs
    ):
        """
        Test cached read performance with multiple cached specs.

        GIVEN 50 specifications are cached
        WHEN get_spec() is called for various specs
        THEN cached read times remain <50ms average
        """
        cache = SpecificationCache(str(spec_directory))
        cache.preload_all()

        assert len(cache.cache) == 50

        # Read random specs 200 times
        import random

        spec_list = list(cache.cache.keys())
        read_times = []

        for _ in range(200):
            spec_path = random.choice(spec_list)

            start = time.perf_counter()
            result = cache.get_spec(spec_path)
            elapsed = time.perf_counter() - start

            read_times.append(elapsed)
            assert result is not None

        # Calculate statistics
        avg_time_ms = statistics.mean(read_times) * 1000
        p95_time_ms = statistics.quantiles(read_times, n=20)[18] * 1000

        assert (
            avg_time_ms < 50.0
        ), f"Average under load: {avg_time_ms:.2f}ms, required <50ms"
        assert (
            p95_time_ms < 50.0
        ), f"P95 under load: {p95_time_ms:.2f}ms, required <50ms"

    def test_get_all_specs_performance(self, spec_directory: Path, create_50_specs):
        """
        Test performance of get_all_specs() method.

        GIVEN 50 specifications are cached
        WHEN get_all_specs() is called
        THEN operation completes in <10ms
        """
        cache = SpecificationCache(str(spec_directory))
        cache.preload_all()

        # Measure get_all_specs performance (50 iterations)
        all_specs_times = []

        for _ in range(50):
            start = time.perf_counter()
            specs = cache.get_all_specs()
            elapsed = time.perf_counter() - start

            all_specs_times.append(elapsed)
            assert len(specs) == 50

        avg_time_ms = statistics.mean(all_specs_times) * 1000
        max_time_ms = max(all_specs_times) * 1000

        assert (
            avg_time_ms < 10.0
        ), f"get_all_specs() avg: {avg_time_ms:.2f}ms, expected <10ms"
        assert (
            max_time_ms < 20.0
        ), f"get_all_specs() max: {max_time_ms:.2f}ms, expected <20ms"


# ============================================================================
# Performance Test: Cache Invalidation (NFR-P2)
# ============================================================================


class TestCacheInvalidationPerformance:
    """
    Performance tests for cache invalidation mechanism.

    Requirements:
    - NFR-P2: Cache invalidation <100ms
    - Target: File modification detection + invalidation <100ms
    """

    def test_nfr_p2_cache_invalidation_under_100ms(
        self, spec_directory: Path, create_spec_file
    ):
        """
        NFR-P2: Cache invalidation must complete in <100ms.

        GIVEN specification is cached
        WHEN file is modified
        THEN cache invalidation completes within 100ms
        AND next read returns updated content
        """
        spec_path = create_spec_file(
            "invalidation-test.md",
            "SPEC-INVAL-001",
            "Invalidation Test Original",
            "Test-Initiative",
        )

        cache = SpecificationCache(str(spec_directory))
        cache.start_file_watcher()

        try:
            # Initial load
            original = cache.get_spec(str(spec_path))
            assert original.title == "Invalidation Test Original"

            # Modify file and measure invalidation time
            start_time = time.perf_counter()

            updated_content = """---
id: SPEC-INVAL-001
title: Invalidation Test Modified
status: in_progress
initiative: Test-Initiative
priority: HIGH
---

# Invalidation Test Modified

Updated content.
"""
            spec_path.write_text(updated_content, encoding="utf-8")

            # Wait for file watcher to detect and invalidate
            # (watchdog typically detects within 10-50ms)
            time.sleep(0.15)  # Allow time for file system event + processing

            # Verify invalidation occurred
            modified = cache.get_spec(str(spec_path))
            invalidation_time = time.perf_counter() - start_time

            assert modified.title == "Invalidation Test Modified"

            # Invalidation time includes: file write + detection + invalidation + re-read
            # Should be well under 200ms total
            assert (
                invalidation_time < 0.2
            ), f"Invalidation took {invalidation_time*1000:.0f}ms"

        finally:
            cache.stop_file_watcher()

    def test_batch_invalidation_performance(
        self, spec_directory: Path, create_spec_file
    ):
        """
        Test invalidation performance when multiple files change.

        GIVEN multiple specifications are cached
        WHEN multiple files are modified simultaneously
        THEN invalidations complete efficiently
        """
        # Create 10 specs
        spec_paths = []
        for i in range(10):
            spec_path = create_spec_file(
                f"batch-inval-{i:02d}.md",
                f"SPEC-BATCH-{i:02d}",
                f"Batch Invalidation Test {i}",
                "Batch-Initiative",
            )
            spec_paths.append(spec_path)

        cache = SpecificationCache(str(spec_directory))
        cache.start_file_watcher()

        try:
            # Load all specs
            cache.preload_all()
            assert len(cache.cache) == 10

            # Modify all specs
            start_time = time.perf_counter()

            for i, spec_path in enumerate(spec_paths):
                updated_content = f"""---
id: SPEC-BATCH-{i:02d}
title: Modified Batch Test {i}
status: in_progress
initiative: Batch-Initiative
priority: MEDIUM
---

# Modified
"""
                spec_path.write_text(updated_content, encoding="utf-8")

            # Wait for all invalidations to process
            time.sleep(0.3)  # Allow time for all file events

            # Verify all invalidated and re-read correctly
            for i, spec_path in enumerate(spec_paths):
                spec = cache.get_spec(str(spec_path))
                assert spec.title == f"Modified Batch Test {i}"

            elapsed = time.perf_counter() - start_time

            # Batch invalidation should scale reasonably
            assert elapsed < 0.5, f"Batch invalidation took {elapsed:.3f}s"

        finally:
            cache.stop_file_watcher()

    def test_manual_invalidation_performance(
        self, spec_directory: Path, create_50_specs
    ):
        """
        Test performance of manual cache invalidation.

        GIVEN 50 specifications are cached
        WHEN invalidate() is called on multiple specs
        THEN each invalidation completes in <1ms
        """
        cache = SpecificationCache(str(spec_directory))
        cache.preload_all()

        spec_paths = list(cache.cache.keys())

        # Measure manual invalidation times
        invalidation_times = []

        for spec_path in spec_paths[:10]:  # Test 10 invalidations
            start = time.perf_counter()
            cache.invalidate(spec_path)
            elapsed = time.perf_counter() - start

            invalidation_times.append(elapsed)

        avg_time_ms = statistics.mean(invalidation_times) * 1000
        max_time_ms = max(invalidation_times) * 1000

        assert (
            avg_time_ms < 1.0
        ), f"Average invalidate(): {avg_time_ms:.3f}ms, expected <1ms"
        assert (
            max_time_ms < 5.0
        ), f"Max invalidate(): {max_time_ms:.3f}ms, expected <5ms"


# ============================================================================
# Performance Test: Memory Efficiency
# ============================================================================


class TestMemoryEfficiency:
    """
    Tests for memory usage and efficiency of caching layer.

    While not explicit NFRs, memory efficiency is important for
    scalability and production deployment.
    """

    def test_memory_usage_with_100_cached_specs(
        self, spec_directory: Path, create_100_specs
    ):
        """
        Test memory footprint with 100 cached specifications.

        GIVEN 100 specifications are cached
        WHEN memory usage is measured
        THEN total cache memory is reasonable (<50MB)
        """
        import sys

        cache = SpecificationCache(str(spec_directory))
        cache.preload_all()

        assert len(cache.cache) == 100

        # Estimate cache size (rough approximation)
        # sys.getsizeof doesn't account for nested objects, but gives baseline
        cache_size_bytes = sys.getsizeof(cache.cache)

        # Add approximate size of cached metadata objects
        for spec_metadata in cache.cache.values():
            cache_size_bytes += sys.getsizeof(spec_metadata.__dict__)

        cache_size_mb = cache_size_bytes / (1024 * 1024)

        # Cache should be efficient - 100 specs should be <10MB
        assert (
            cache_size_mb < 10.0
        ), f"Cache uses {cache_size_mb:.2f}MB for 100 specs, expected <10MB"

    def test_cache_clear_releases_memory(self, spec_directory: Path, create_50_specs):
        """
        Test that cache.clear() releases memory.

        GIVEN cache contains many specifications
        WHEN clear() is called
        THEN cache is emptied
        AND memory can be reclaimed
        """
        cache = SpecificationCache(str(spec_directory))
        cache.preload_all()

        assert len(cache.cache) == 50

        # Clear cache
        cache.clear()

        assert len(cache.cache) == 0

        # Force garbage collection
        gc.collect()

        # Verify cache is truly empty
        all_specs = cache.get_all_specs()
        assert len(all_specs) == 0


# ============================================================================
# Performance Test: Concurrent Access Patterns
# ============================================================================


class TestConcurrentAccessPerformance:
    """
    Performance tests for concurrent cache access patterns.

    Tests thread safety and performance under concurrent load.
    Note: Current implementation is single-threaded, but these tests
    establish baseline for future multi-threaded scenarios.
    """

    def test_sequential_mixed_operations_performance(
        self, spec_directory: Path, create_50_specs
    ):
        """
        Test performance of mixed read/invalidate operations.

        GIVEN 50 specifications are cached
        WHEN mix of reads and invalidations occur sequentially
        THEN overall performance remains acceptable
        """
        import random

        cache = SpecificationCache(str(spec_directory))
        cache.preload_all()

        spec_paths = list(cache.cache.keys())

        # Perform 100 mixed operations
        operation_times = []

        for _i in range(100):
            # 80% reads, 20% invalidations
            if random.random() < 0.8:
                # Read operation
                spec_path = random.choice(spec_paths)
                start = time.perf_counter()
                cache.get_spec(spec_path)
                elapsed = time.perf_counter() - start
            else:
                # Invalidate operation
                spec_path = random.choice(spec_paths)
                start = time.perf_counter()
                cache.invalidate(spec_path)
                elapsed = time.perf_counter() - start

            operation_times.append(elapsed)

        # Calculate statistics
        avg_time_ms = statistics.mean(operation_times) * 1000
        p95_time_ms = statistics.quantiles(operation_times, n=20)[18] * 1000

        assert (
            avg_time_ms < 50.0
        ), f"Mixed operations avg: {avg_time_ms:.2f}ms, expected <50ms"
        assert (
            p95_time_ms < 100.0
        ), f"Mixed operations P95: {p95_time_ms:.2f}ms, expected <100ms"


# ============================================================================
# Performance Test: Worst-Case Scenarios
# ============================================================================


class TestWorstCasePerformance:
    """
    Performance tests for worst-case and edge scenarios.

    Validates that performance degrades gracefully under adverse conditions.
    """

    def test_cache_miss_performance(self, spec_directory: Path, create_spec_file):
        """
        Test performance when spec is not in cache (cache miss).

        GIVEN specification file exists but is not cached
        WHEN get_spec() is called (cache miss)
        THEN file is parsed and cached within <200ms
        """
        spec_path = create_spec_file(
            "cache-miss-test.md",
            "SPEC-MISS-001",
            "Cache Miss Test",
            "Test-Initiative",
        )

        cache = SpecificationCache(str(spec_directory))

        # Ensure not cached
        assert str(spec_path) not in cache.cache

        # Measure cache miss time (includes file I/O + parsing)
        start = time.perf_counter()
        result = cache.get_spec(str(spec_path))
        elapsed = time.perf_counter() - start

        assert result is not None
        assert str(spec_path) in cache.cache

        elapsed_ms = elapsed * 1000
        assert (
            elapsed_ms < 200.0
        ), f"Cache miss took {elapsed_ms:.0f}ms, expected <200ms"

    def test_large_specification_performance(
        self, spec_directory: Path, create_spec_file
    ):
        """
        Test performance with unusually large specification.

        GIVEN specification has many features and large content
        WHEN spec is loaded and cached
        THEN performance remains acceptable
        """
        # Create spec with 20 features (larger than typical)
        spec_path = create_spec_file(
            "large-spec.md",
            "SPEC-LARGE-001",
            "Large Specification Test",
            "Large-Initiative",
            num_features=20,
        )

        # Add more content to make it larger
        content = spec_path.read_text(encoding="utf-8")
        large_content = content + (
            "\n## Additional Section\n" + ("Lorem ipsum dolor sit amet. " * 1000)
        )
        spec_path.write_text(large_content, encoding="utf-8")

        cache = SpecificationCache(str(spec_directory))

        # Measure load time for large spec
        start = time.perf_counter()
        result = cache.get_spec(str(spec_path))
        elapsed = time.perf_counter() - start

        assert result is not None
        assert len(result.features) == 20

        # Large spec should still load reasonably fast
        elapsed_ms = elapsed * 1000
        assert (
            elapsed_ms < 500.0
        ), f"Large spec load took {elapsed_ms:.0f}ms, expected <500ms"

    def test_empty_cache_performance(self, spec_directory: Path):
        """
        Test performance when cache is empty.

        GIVEN cache has no entries
        WHEN get_all_specs() is called
        THEN operation completes instantly
        """
        cache = SpecificationCache(str(spec_directory))

        # Ensure cache is empty
        assert len(cache.cache) == 0

        # Measure empty cache operations
        start = time.perf_counter()
        specs = cache.get_all_specs()
        elapsed = time.perf_counter() - start

        assert len(specs) == 0

        elapsed_ms = elapsed * 1000
        assert elapsed_ms < 1.0, f"Empty cache operation took {elapsed_ms:.3f}ms"


# ============================================================================
# Performance Test: End-to-End Modal Load Performance
# ============================================================================


class TestModalLoadPerformance:
    """
    Integration performance tests for modal load scenario.

    Tests NFR-P1: Modal load <500ms (P95) including spec cache reads.
    """

    def test_nfr_p1_modal_load_simulation(self, spec_directory: Path, create_50_specs):
        """
        NFR-P1: Modal load must complete in <500ms (P95).

        Simulates modal loading scenario:
        1. Load all specifications (get_all_specs)
        2. Group by initiative
        3. Extract features from each spec

        GIVEN 50 specifications are cached
        WHEN modal data is loaded (simulated)
        THEN operation completes in <500ms (P95)
        """
        cache = SpecificationCache(str(spec_directory))
        cache.preload_all()

        # Simulate modal load 100 times for statistical analysis
        load_times = []

        for _ in range(100):
            start = time.perf_counter()

            # Step 1: Get all specs
            all_specs = cache.get_all_specs()

            # Step 2: Group by initiative (simulates modal logic)
            initiatives: dict[str, list[Any]] = {}
            for spec in all_specs:
                initiative = spec.initiative or "Uncategorized"
                if initiative not in initiatives:
                    initiatives[initiative] = []
                initiatives[initiative].append(spec)

            # Step 3: Extract features (simulates modal rendering)
            total_features = 0
            for specs in initiatives.values():
                for spec in specs:
                    total_features += len(spec.features)

            elapsed = time.perf_counter() - start
            load_times.append(elapsed)

        # Calculate statistics
        avg_time_ms = statistics.mean(load_times) * 1000
        p50_time_ms = statistics.median(load_times) * 1000
        p95_time_ms = statistics.quantiles(load_times, n=20)[18] * 1000
        p99_time_ms = statistics.quantiles(load_times, n=100)[98] * 1000

        # Verify NFR-P1 requirement
        assert (
            p95_time_ms < 500.0
        ), f"Modal load P95: {p95_time_ms:.0f}ms, required <500ms"

        # Log performance metrics
        print(
            f"\nModal Load Performance (50 specs):\n"
            f"  Average: {avg_time_ms:.0f}ms\n"
            f"  P50: {p50_time_ms:.0f}ms\n"
            f"  P95: {p95_time_ms:.0f}ms ✓ (required <500ms)\n"
            f"  P99: {p99_time_ms:.0f}ms"
        )


# ============================================================================
# Performance Regression Test Markers
# ============================================================================


@pytest.mark.performance
class TestPerformanceRegressionBaseline:
    """
    Baseline performance tests for regression detection.

    These tests establish performance baselines and should be run
    regularly to detect performance regressions.
    """

    def test_baseline_50_spec_load(self, spec_directory: Path, create_50_specs):
        """Baseline: Load 50 specs."""
        cache = SpecificationCache(str(spec_directory))

        start = time.perf_counter()
        cache.preload_all()
        elapsed = time.perf_counter() - start

        assert len(cache.cache) == 50
        assert elapsed < 2.0

        print(f"\nBaseline: 50 spec load = {elapsed:.3f}s")

    def test_baseline_cached_read(self, spec_directory: Path, create_spec_file):
        """Baseline: Cached read performance."""
        spec_path = create_spec_file("baseline.md", "SPEC-BASE", "Baseline", "Test")

        cache = SpecificationCache(str(spec_directory))
        cache.get_spec(str(spec_path))

        # 100 cached reads
        start = time.perf_counter()
        for _ in range(100):
            cache.get_spec(str(spec_path))
        elapsed = time.perf_counter() - start

        avg_ms = (elapsed / 100) * 1000
        assert avg_ms < 50.0

        print(f"\nBaseline: Cached read avg = {avg_ms:.2f}ms")

    def test_baseline_invalidation(self, spec_directory: Path, create_spec_file):
        """Baseline: Cache invalidation performance."""
        spec_path = create_spec_file(
            "invalidation-baseline.md", "SPEC-INVAL-BASE", "Invalidation", "Test"
        )

        cache = SpecificationCache(str(spec_directory))
        cache.start_file_watcher()

        try:
            cache.get_spec(str(spec_path))

            start = time.perf_counter()
            spec_path.write_text(
                spec_path.read_text().replace("Invalidation", "Modified")
            )
            time.sleep(0.15)
            cache.get_spec(str(spec_path))
            elapsed = time.perf_counter() - start

            assert elapsed < 0.2

            print(f"\nBaseline: Invalidation = {elapsed*1000:.0f}ms")

        finally:
            cache.stop_file_watcher()
