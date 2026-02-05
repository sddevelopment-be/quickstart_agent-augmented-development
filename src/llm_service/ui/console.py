"""
Console Wrapper Module for Rich Terminal UI

Provides a singleton console instance with rich formatting capabilities.
Automatically detects TTY environments and respects NO_COLOR environment variable.

Implementation of ADR-030: Rich Terminal UI for CLI Feedback

Features:
- Singleton pattern for consistent console instance
- Automatic TTY detection with fallback to plain text
- NO_COLOR environment variable support
- Graceful fallback if rich is not available
"""

import os
import sys
from typing import Optional

try:
    from rich.console import Console as RichConsole
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    RichConsole = None


# Module-level singleton console instance
_console: Optional[RichConsole] = None


class FallbackConsole:
    """
    Fallback console implementation when rich is not available.
    
    Provides a minimal console interface that mimics rich.Console
    but uses standard print() for output.
    """
    
    def __init__(self):
        """Initialize fallback console."""
        self.is_terminal = sys.stdout.isatty()
        self.no_color = os.environ.get('NO_COLOR', '').lower() in ('1', 'true', 'yes')
    
    def print(self, *args, **kwargs):
        """
        Print to stdout using built-in print.
        
        Args:
            *args: Positional arguments to print
            **kwargs: Keyword arguments (ignored for compatibility)
        """
        # Strip rich markup tags for plain output
        output = ' '.join(str(arg) for arg in args)
        # Simple regex to remove [tag]...[/tag] markup
        import re
        output = re.sub(r'\[/?[^\]]+\]', '', output)
        print(output)


def get_console() -> RichConsole:
    """
    Get singleton console instance.
    
    Returns:
        Console instance (rich.Console or FallbackConsole)
        
    The console instance:
    - Automatically detects TTY vs non-TTY environments
    - Respects NO_COLOR environment variable
    - Falls back to plain output if rich is not available
    - Uses singleton pattern for consistency across application
    """
    global _console
    
    if _console is None:
        if RICH_AVAILABLE:
            # Check for NO_COLOR environment variable
            no_color = os.environ.get('NO_COLOR', '').lower() in ('1', 'true', 'yes')
            
            # Create rich console with automatic TTY detection
            _console = RichConsole(
                force_terminal=None,  # Auto-detect
                no_color=no_color,
                soft_wrap=True,
            )
        else:
            # Fallback to simple console if rich not available
            _console = FallbackConsole()
    
    return _console


# Pre-initialize console for convenience
console = get_console()


# Convenience exports for common use cases
def print_success(message: str):
    """
    Print a success message with green color and checkmark.
    
    Args:
        message: Success message to display
    """
    console.print(f"[green]✓ {message}[/green]")


def print_error(message: str):
    """
    Print an error message with red color and X mark.
    
    Args:
        message: Error message to display
    """
    console.print(f"[red]✗ {message}[/red]")


def print_warning(message: str):
    """
    Print a warning message with yellow color and warning symbol.
    
    Args:
        message: Warning message to display
    """
    console.print(f"[yellow]⚠ {message}[/yellow]")


def print_info(message: str):
    """
    Print an informational message with blue color.
    
    Args:
        message: Info message to display
    """
    console.print(f"[blue]ℹ {message}[/blue]")


__all__ = [
    'console',
    'get_console',
    'print_success',
    'print_error',
    'print_warning',
    'print_info',
]
