"""Path utilities for ops scripts."""

from pathlib import Path


def get_repo_root(current_file: Path) -> Path:
    """
    Get repository root from current file location.

    Assumes scripts are in ops/* subdirectories, so repo root is 2-3 levels up.

    Args:
        current_file: Path to current file (__file__)

    Returns:
        Path to repository root
    """
    # From ops/subdir/script.py -> go up 3 levels
    # From ops/script.py -> go up 2 levels
    current = Path(current_file).resolve()

    # Check if we're in ops/subdir/
    if current.parent.parent.name == "ops":
        return current.parent.parent.parent
    # Check if we're in ops/
    elif current.parent.name == "ops":
        return current.parent.parent

    # Fallback: go up 3 levels from ops/subdir/script.py
    return current.parent.parent.parent


def get_work_dir(current_file: Path) -> Path:
    """
    Get work directory from current file location.

    Args:
        current_file: Path to current file (__file__)

    Returns:
        Path to work directory
    """
    return get_repo_root(current_file) / "work"


def get_agents_dir(current_file: Path) -> Path:
    """
    Get agents directory from current file location.

    Args:
        current_file: Path to current file (__file__)

    Returns:
        Path to .github/agents directory
    """
    return get_repo_root(current_file) / ".github" / "agents"
