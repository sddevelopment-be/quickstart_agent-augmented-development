"""
Usage Example: SpecificationCache Integration

This example demonstrates how to integrate the SpecificationCache
into the dashboard application for high-performance specification frontmatter access.

Performance characteristics demonstrated:
- Initial load: <2 seconds for 50 specs
- Cached reads: <50ms
- Cache invalidation: <100ms
"""

from src.llm_service.dashboard.spec_cache import SpecificationCache


def example_basic_usage():
    """Basic usage example: Initialize cache and get specifications."""
    print("=== Basic Usage Example ===\n")

    # Initialize cache with specifications directory
    cache = SpecificationCache("specifications/")

    # Preload all specifications at startup
    print("Preloading all specifications...")
    cache.preload_all()
    print(f"Cached {len(cache.cache)} specifications\n")

    # Get a specific specification (from cache)
    spec_path = "specifications/initiatives/dashboard-enhancements/orphan-task-assignment.md"
    spec = cache.get_spec(spec_path)

    if spec:
        print(f"Specification ID: {spec.id}")
        print(f"Title: {spec.title}")
        print(f"Initiative: {spec.initiative}")
        print(f"Status: {spec.status}")
        print(f"Features: {len(spec.features)}")
    else:
        print("Specification not found or invalid")


def example_with_file_watcher():
    """Example with file watcher for automatic cache invalidation."""
    print("\n=== File Watcher Example ===\n")

    cache = SpecificationCache("specifications/")
    cache.preload_all()

    # Start file watcher (monitors for changes)
    print("Starting file watcher...")
    cache.start_file_watcher()
    print("File watcher running - cache will auto-invalidate on file changes\n")

    # Get all cached specifications
    all_specs = cache.get_all_specs()
    print(f"Total specifications: {len(all_specs)}")

    # Group by initiative
    initiatives = {}
    for spec in all_specs:
        initiative = spec.initiative
        if initiative not in initiatives:
            initiatives[initiative] = []
        initiatives[initiative].append(spec)

    print("\nSpecifications by initiative:")
    for initiative, specs in sorted(initiatives.items()):
        print(f"  {initiative}: {len(specs)} specifications")

    # Clean shutdown
    print("\nStopping file watcher...")
    cache.stop_file_watcher()
    print("Done!")


def example_performance_monitoring():
    """Example showing performance monitoring."""
    print("\n=== Performance Monitoring Example ===\n")

    import time

    cache = SpecificationCache("specifications/")

    # Measure preload performance
    start = time.perf_counter()
    cache.preload_all()
    elapsed = time.perf_counter() - start

    print(f"Preloaded {len(cache.cache)} specs in {elapsed*1000:.2f}ms")

    if cache.cache:
        # Get first spec path
        spec_path = next(iter(cache.cache.keys()))

        # Measure cached read performance
        start = time.perf_counter()
        spec = cache.get_spec(spec_path)
        elapsed = time.perf_counter() - start

        print(f"Cached read time: {elapsed*1000:.2f}ms")


def example_error_handling():
    """Example demonstrating error handling."""
    print("\n=== Error Handling Example ===\n")

    cache = SpecificationCache("specifications/")

    # Attempt to get non-existent spec (returns None, no exception)
    spec = cache.get_spec("nonexistent.md")
    print(f"Non-existent spec: {spec}")  # Output: None

    # Invalidate non-existent spec (safe, no exception)
    cache.invalidate("nonexistent.md")
    print("Invalidation of non-existent spec: OK")

    # Empty directory (returns empty list)
    empty_cache = SpecificationCache("/tmp/empty-specs/")
    empty_cache.preload_all()
    print(f"Empty directory specs: {len(empty_cache.get_all_specs())}")


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_with_file_watcher()
    example_performance_monitoring()
    example_error_handling()

    print("\n" + "="*50)
    print("All examples completed successfully!")
    print("="*50)
