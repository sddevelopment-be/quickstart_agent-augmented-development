"""
Root pytest configuration for agent-augmented-development.

Sets up Python path before test collection to allow importing from
src/ and tools/ directories. Ensures src/ takes precedence over root-level
modules.
"""

import sys
from pathlib import Path

# Add src/ and tools/ to Python path immediately, at the beginning
# to ensure src/framework takes precedence over root/framework
repo_root = Path(__file__).parent
src_path = str(repo_root / "src")
tools_path = str(repo_root / "tools")

# Remove if already present to avoid duplicates
for path in [src_path, tools_path]:
    if path in sys.path:
        sys.path.remove(path)

# Insert at the very beginning
sys.path.insert(0, tools_path)
sys.path.insert(0, src_path)
