"""Test utilities for integration test runners."""

import subprocess


def run_command(cmd: list[str]) -> tuple[int, str, str]:
    """
    Run a command and return exit code, stdout, stderr.

    Args:
        cmd: Command and arguments as list

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


def print_test_header(test_name: str, width: int = 50) -> None:
    """
    Print a formatted test header.

    Args:
        test_name: Name of the test being run
        width: Width of separator line
    """
    print(f"Testing {test_name}...")
    print("=" * width)
    print()


def print_test_result(
    test_num: int, description: str, passed: bool, details: str = ""
) -> None:
    """
    Print a formatted test result.

    Args:
        test_num: Test number
        description: Test description
        passed: Whether the test passed
        details: Additional details to print
    """
    symbol = "✅" if passed else "❌"
    print(f"[TEST {test_num}] {description}")
    print(f"{symbol} {details}")
    print()


def print_test_footer(all_passed: bool = True) -> None:
    """
    Print a formatted test footer.

    Args:
        all_passed: Whether all tests passed
    """
    print("=" * 50)
    if all_passed:
        print("All tests passed! ✅")
    else:
        print("Some tests failed! ❌")
