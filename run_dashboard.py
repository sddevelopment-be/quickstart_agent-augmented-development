#!/usr/bin/env python3
"""
Startup script for LLM Service Dashboard.

Usage:
    python run_dashboard.py [--host HOST] [--port PORT] [--debug]

Example:
    python run_dashboard.py --port 8080 --debug
"""

import argparse
import sys
from pathlib import Path

# Ensure src is in Python path
repo_root = Path(__file__).parent
src_path = repo_root / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from llm_service.dashboard import run_dashboard


def main() -> None:
    """Parse arguments and launch dashboard."""
    parser = argparse.ArgumentParser(
        description='Run LLM Service Dashboard for real-time monitoring'
    )
    parser.add_argument(
        '--host',
        default='localhost',
        help='Host to bind to (default: localhost)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port to bind to (default: 8080)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    parser.add_argument(
        '--watch-dir',
        default='work/collaboration',
        help='Directory to watch for task files (default: work/collaboration)'
    )

    args = parser.parse_args()

    # Run dashboard
    run_dashboard(
        host=args.host,
        port=args.port,
        debug=args.debug,
        watch_dir=args.watch_dir
    )


if __name__ == '__main__':
    main()
