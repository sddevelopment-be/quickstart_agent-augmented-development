"""
Test for task_query.py module location after ADR-046 refactoring.

This test verifies that the task_query module has been properly moved
to the domain layer and can be imported correctly.

ADR-046 Context:
    - task_query.py moved from framework.orchestration to domain.collaboration
    - This aligns with bounded context architecture
    - Dashboard and framework both depend on domain layer (no circular deps)

Expected Behavior:
    - All production code imports from src.domain.collaboration.task_query
    - No imports from old src.framework.orchestration.task_query location
"""

import sys
from pathlib import Path

# Add repository root to path (simulates how tests normally run)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_task_query_module_can_be_imported():
    """
    Test that task_query module can be imported from domain layer.
    """
    try:
        # Import from new domain location (ADR-046)
        from src.domain.collaboration import task_query

        # Verify the module loaded successfully
        assert hasattr(task_query, "find_task_files")
        assert hasattr(task_query, "load_open_tasks")
        assert hasattr(task_query, "filter_tasks")

        print("✅ PASS: task_query module imported successfully from domain layer")
        return True

    except ModuleNotFoundError as e:
        print(f"❌ FAIL: task_query module import failed: {e}")
        return False


def test_task_query_imports_use_domain_layer():
    """
    Verify task_query.py is in domain layer (ADR-046).
    """
    # New location after ADR-046
    task_query_path = Path("src/domain/collaboration/task_query.py")
    assert task_query_path.exists(), "task_query.py should be in domain.collaboration"

    # Old location should not exist
    old_path = Path("src/framework/orchestration/task_query.py")
    assert not old_path.exists(), "Old task_query.py should be removed from framework"

    print("✅ PASS: task_query.py correctly located in domain layer")
    return True


def test_dashboard_can_import_task_query_functions():
    """
    Test that dashboard can import task_query functions from domain layer.

    This verifies the architectural fix where dashboard depends on domain
    instead of framework (prevents circular dependencies).
    """
    # Import from domain layer (ADR-046)
    from src.domain.collaboration.task_query import (
        filter_tasks,
        find_task_files,
        load_open_tasks,
    )

    # Verify functions are callable
    assert callable(find_task_files)
    assert callable(load_open_tasks)
    assert callable(filter_tasks)

    # Verify they have correct signatures
    import inspect

    find_sig = inspect.signature(find_task_files)
    assert "work_dir" in find_sig.parameters

    load_sig = inspect.signature(load_open_tasks)
    assert "work_dir" in load_sig.parameters

    filter_sig = inspect.signature(filter_tasks)
    assert "tasks" in filter_sig.parameters

    return True


if __name__ == "__main__":
    # Run tests
    print("=" * 70)
    print("Testing task_query.py location after ADR-046 refactoring")
    print("=" * 70)
    print()

    results = []

    print("Test 1: Module can be imported from domain layer")
    print("-" * 70)
    results.append(test_task_query_module_can_be_imported())
    print()

    print("Test 2: Module is in correct location (domain)")
    print("-" * 70)
    try:
        test_task_query_imports_use_domain_layer()
        print("✅ PASS: Correctly located in domain layer")
        results.append(True)
    except AssertionError as e:
        print(f"❌ FAIL: {e}")
        results.append(False)
    print()

    print("Test 3: Dashboard can import from domain layer")
    print("-" * 70)
    try:
        test_dashboard_can_import_task_query_functions()
        print("✅ PASS: Dashboard import successful")
        results.append(True)
    except Exception as e:
        print(f"❌ FAIL: {e}")
        results.append(False)
    print()

    print("=" * 70)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    if all(results):
        print("✅ ALL TESTS PASSED (GREEN)")
        sys.exit(0)
    else:
        print("❌ TESTS FAILED (RED) - Fix needed")
        sys.exit(1)
