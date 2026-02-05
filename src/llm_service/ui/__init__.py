"""
LLM Service UI Module

Provides rich terminal UI components for CLI output.
"""

from llm_service.ui.console import (
    console,
    get_console,
    print_success,
    print_error,
    print_warning,
    print_info,
)

__all__ = [
    "console",
    "get_console",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
]
