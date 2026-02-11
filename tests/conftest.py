"""
Pytest configuration for agent-augmented-development tests.

Sets up Python path to allow importing from src/ and tools/ directories.
"""

import sys
from pathlib import Path


def pytest_configure(config):
    """Configure pytest before test collection."""
    # Add src/ to Python path for framework and common module imports
    repo_root = Path(__file__).parent.parent
    src_path = str(repo_root / "src")
    tools_path = str(repo_root / "tools")

    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    if tools_path not in sys.path:
        sys.path.insert(0, tools_path)
