"""
Test for task_query.py import consistency bug.

This test verifies that the task_query module can be imported correctly
when the dashboard runs, exposing the import path inconsistency bug.

Bug Description:
    - task_query.py uses: from common.task_schema import load_task_safe
    - app.py uses: from src.common.task_schema import load_task_safe
    - When dashboard runs, PYTHONPATH doesn't include 'src/', causing ModuleNotFoundError

Expected Behavior:
    - All production code should use consistent import paths
    - task_query.py should use 'from src.common...' like other production modules

Related:
    - Issue: Empty dashboard UI (tasks not loading)
    - Root Cause: task_query module import failure on dashboard startup
"""

import sys
from pathlib import Path

# Add repository root to path (simulates how tests normally run)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_task_query_module_can_be_imported():
    """
    Test that task_query module can be imported successfully.
    
    This test FAILS with current code because task_query.py uses
    'from common...' instead of 'from src.common...'
    """
    # Simulate dashboard import context (no PYTHONPATH manipulation)
    # Dashboard runs from repository root without adding 'src/' to path
    
    try:
        # This import should work like app.py imports work
        from src.framework.orchestration import task_query
        
        # Verify the module loaded successfully
        assert hasattr(task_query, 'find_task_files')
        assert hasattr(task_query, 'load_open_tasks')
        assert hasattr(task_query, 'filter_tasks')
        
        print("✅ PASS: task_query module imported successfully")
        return True
        
    except ModuleNotFoundError as e:
        # This is the bug we're catching
        print(f"❌ FAIL: task_query module import failed: {e}")
        print("Root cause: Inconsistent import paths in task_query.py")
        print("Expected: 'from src.common...' (like app.py)")
        print("Actual: 'from common...' (missing src. prefix)")
        return False


def test_task_query_imports_match_dashboard_convention():
    """
    Verify task_query.py uses the same import convention as app.py.
    
    This ensures import consistency across production modules.
    """
    task_query_path = Path("src/framework/orchestration/task_query.py")
    assert task_query_path.exists(), "task_query.py not found"
    
    content = task_query_path.read_text()
    
    # Check for incorrect imports (without src. prefix)
    incorrect_imports = [
        line for line in content.splitlines()
        if line.strip().startswith("from common.")
    ]
    
    # Should use 'from src.common...' not 'from common...'
    if len(incorrect_imports) == 0:
        print("✅ PASS: All imports use correct 'src.' prefix")
        return True
    else:
        print(f"❌ FAIL: Found {len(incorrect_imports)} imports without 'src.' prefix:")
        for line in incorrect_imports:
            print(f"  - {line.strip()}")
        print("\nAll production modules should use 'from src.common...' for consistency")
        return False


def test_dashboard_can_import_task_query_functions():
    """
    Test that dashboard app.py can successfully import and use task_query functions.
    
    This simulates the actual dashboard startup import sequence.
    """
    # Import as dashboard does
    from src.framework.orchestration.task_query import (
        find_task_files,
        load_open_tasks,
        filter_tasks,
    )
    
    # Verify functions are callable
    assert callable(find_task_files)
    assert callable(load_open_tasks)
    assert callable(filter_tasks)
    
    # Verify they have correct signatures (basic check)
    import inspect
    
    find_sig = inspect.signature(find_task_files)
    assert 'work_dir' in find_sig.parameters
    
    load_sig = inspect.signature(load_open_tasks)
    assert 'work_dir' in load_sig.parameters
    
    filter_sig = inspect.signature(filter_tasks)
    assert 'tasks' in filter_sig.parameters
    
    return True


if __name__ == "__main__":
    # Run tests to expose the bug
    print("=" * 70)
    print("Testing task_query.py import consistency (TDD RED phase)")
    print("=" * 70)
    print()
    
    results = []
    
    print("Test 1: Module can be imported")
    print("-" * 70)
    results.append(test_task_query_module_can_be_imported())
    print()
    
    print("Test 2: Import paths match dashboard convention")
    print("-" * 70)
    results.append(test_task_query_imports_match_dashboard_convention())
    print()
    
    print("Test 3: Dashboard can import task_query functions")
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
