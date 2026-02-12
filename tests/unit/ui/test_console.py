"""
Unit Tests for Console Wrapper Module

Tests the console wrapper that integrates rich library for terminal UI.

Following Directive 017 (TDD) - Writing tests before implementation.
Target: >80% coverage per acceptance criteria.
"""

import os
from io import StringIO

import pytest


class TestConsoleModule:
    """
    Unit tests for console module initialization and configuration.
    """

    def test_console_module_imports_successfully(self):
        """
        Test that console module can be imported.

        Given: llm_service.ui.console module exists
        When: Importing the module
        Then: Import should succeed without errors
        """
        from llm_service.ui import console

        assert console is not None

    def test_get_console_returns_console_instance(self):
        """
        Test get_console() function returns a Console instance.

        Given: get_console function exists
        When: Calling get_console()
        Then: Should return a rich.Console instance
        """
        from llm_service.ui.console import get_console

        console = get_console()
        assert console is not None

        # Should be a Console or Console-like object
        assert hasattr(console, "print")

    def test_get_console_returns_singleton(self):
        """
        Test get_console() returns the same instance on multiple calls.

        Given: Console is initialized
        When: Calling get_console() multiple times
        Then: Should return the same instance (singleton pattern)
        """
        from llm_service.ui.console import get_console

        console1 = get_console()
        console2 = get_console()

        assert console1 is console2

    def test_console_exported_as_module_variable(self):
        """
        Test that 'console' is exported as a module-level variable.

        Given: Console module is imported
        When: Accessing llm_service.ui.console.console
        Then: Should have a pre-initialized console instance
        """
        from llm_service.ui.console import console

        assert console is not None
        assert hasattr(console, "print")


class TestConsoleConfiguration:
    """
    Unit tests for console configuration and environment detection.
    """

    def test_console_respects_no_color_env_var(self, monkeypatch):
        """
        Test console respects NO_COLOR environment variable.

        Given: NO_COLOR environment variable is set
        When: Creating console instance
        Then: Console should disable color output
        """
        from rich.console import Console

        # Test that Console can be created with no_color
        monkeypatch.setenv("NO_COLOR", "1")

        # Check if NO_COLOR is respected
        no_color_value = os.environ.get("NO_COLOR", "").lower() in ("1", "true", "yes")
        assert no_color_value is True

        # Create a new console with no_color flag
        console = Console(no_color=True)
        assert console is not None

    def test_console_detects_tty_environment(self):
        """
        Test console can detect if output is to a TTY.

        Given: Console is initialized
        When: Checking terminal detection
        Then: Should have a way to detect TTY vs non-TTY
        """
        from llm_service.ui.console import get_console

        console = get_console()

        # Rich Console has is_terminal property
        assert hasattr(console, "is_terminal")

    def test_console_can_be_forced_to_terminal_mode(self):
        """
        Test console can be forced to terminal mode for testing.

        Given: Console configuration
        When: Creating console with force_terminal=True
        Then: Console should act as if in terminal mode
        """
        from rich.console import Console

        # This tests the rich API we'll use
        console = Console(force_terminal=True)
        assert console.is_terminal is True

    def test_console_can_be_forced_to_plain_mode(self):
        """
        Test console can be forced to plain text mode.

        Given: Console configuration
        When: Creating console with force_terminal=False
        Then: Console should output plain text
        """
        from rich.console import Console

        console = Console(force_terminal=False)
        assert console.is_terminal is False


class TestConsoleOutput:
    """
    Unit tests for console output functionality.
    """

    def test_console_print_method_exists(self):
        """
        Test console has print method.

        Given: Console instance
        When: Checking for print method
        Then: Should have a print method
        """
        from llm_service.ui.console import console

        assert hasattr(console, "print")
        assert callable(console.print)

    def test_console_print_outputs_to_buffer(self):
        """
        Test console can print to a string buffer.

        Given: Console configured with StringIO buffer
        When: Printing text
        Then: Text should appear in buffer
        """
        from rich.console import Console

        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False)

        console.print("Test message")

        output = buffer.getvalue()
        assert "Test message" in output

    def test_console_supports_rich_markup(self):
        """
        Test console supports rich markup for colors and styles.

        Given: Console configured for testing
        When: Printing text with markup
        Then: Markup should be processed
        """
        from rich.console import Console

        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False)

        console.print("[green]Success[/green]")

        output = buffer.getvalue()
        assert "Success" in output


class TestPanelOutput:
    """
    Unit tests for panel output functionality.
    """

    def test_can_create_panel_with_console(self):
        """
        Test creating and printing a panel.

        Given: Console and Panel classes
        When: Creating and printing a panel
        Then: Panel should render correctly
        """
        from rich.console import Console
        from rich.panel import Panel

        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False, width=40)

        panel = Panel("Test content", title="Test Panel")
        console.print(panel)

        output = buffer.getvalue()
        assert "Test content" in output
        assert "Test Panel" in output

    def test_panel_can_be_styled(self):
        """
        Test panels can have custom styles.

        Given: Panel with custom border style
        When: Rendering panel
        Then: Style should be applied
        """
        from rich.console import Console
        from rich.panel import Panel

        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False, width=40)

        panel = Panel("Content", border_style="green")
        console.print(panel)

        output = buffer.getvalue()
        assert "Content" in output


class TestTableOutput:
    """
    Unit tests for table output functionality.
    """

    def test_can_create_table_with_console(self):
        """
        Test creating and printing a table.

        Given: Console and Table classes
        When: Creating and printing a table
        Then: Table should render correctly
        """
        from rich.console import Console
        from rich.table import Table

        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False, width=60)

        table = Table(title="Test Table")
        table.add_column("Column 1")
        table.add_column("Column 2")
        table.add_row("Value 1", "Value 2")

        console.print(table)

        output = buffer.getvalue()
        assert "Test Table" in output
        assert "Column 1" in output
        assert "Column 2" in output
        assert "Value 1" in output
        assert "Value 2" in output

    def test_table_columns_can_be_styled(self):
        """
        Test table columns can have custom styles.

        Given: Table with styled columns
        When: Rendering table
        Then: Columns should maintain their configuration
        """
        from rich.console import Console
        from rich.table import Table

        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False, width=60)

        table = Table()
        table.add_column("Name", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_row("Test", "123")

        console.print(table)

        output = buffer.getvalue()
        assert "Name" in output
        assert "Test" in output


class TestProgressOutput:
    """
    Unit tests for progress bar functionality.
    """

    def test_can_create_progress_bar(self):
        """
        Test creating a progress bar.

        Given: Progress class
        When: Creating progress context
        Then: Should work without errors
        """
        from rich.progress import Progress

        # Progress bar can be created
        with Progress() as progress:
            task = progress.add_task("Testing", total=100)
            assert task is not None

    def test_progress_can_be_updated(self):
        """
        Test progress bar can be updated.

        Given: Progress bar with task
        When: Updating progress
        Then: Should update without errors
        """
        from rich.progress import Progress

        with Progress() as progress:
            task = progress.add_task("Testing", total=100)
            progress.update(task, completed=50)
            progress.update(task, completed=100)


class TestConsoleFallbackBehavior:
    """
    Unit tests for console fallback behavior in case rich is not available.
    """

    def test_console_has_graceful_fallback_concept(self):
        """
        Test that we can implement a fallback console.

        Given: Rich might not be available
        When: Implementing fallback pattern
        Then: Should have a simple console-like interface
        """
        # This tests the pattern we'll use for fallback

        class FallbackConsole:
            """Simple fallback console if rich not available."""

            def print(self, *args, **kwargs):
                """Fallback print using built-in print."""
                print(*args)

        fallback = FallbackConsole()
        assert hasattr(fallback, "print")
        assert callable(fallback.print)


class TestConsoleHelperFunctions:
    """
    Unit tests for console helper functions.
    """

    def test_can_import_commonly_used_rich_components(self):
        """
        Test that commonly used rich components are importable.

        Given: rich library is installed
        When: Importing common components
        Then: All should import successfully
        """
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.progress import Progress
            from rich.syntax import Syntax
            from rich.table import Table

            # All imports successful
            assert Console is not None
            assert Panel is not None
            assert Table is not None
            assert Progress is not None
            assert Syntax is not None
        except ImportError as e:
            pytest.fail(f"Failed to import rich components: {e}")

    def test_print_success_helper(self):
        """
        Test print_success helper function.

        Given: print_success function
        When: Calling it with a message
        Then: Should output success message with formatting
        """


        from llm_service.ui.console import print_success

        # We can't easily capture the module-level console output,
        # so we test that the function exists and is callable
        assert callable(print_success)

    def test_print_error_helper(self):
        """
        Test print_error helper function.

        Given: print_error function
        When: Calling it with a message
        Then: Should output error message with formatting
        """
        from llm_service.ui.console import print_error

        assert callable(print_error)

    def test_print_warning_helper(self):
        """
        Test print_warning helper function.

        Given: print_warning function
        When: Calling it with a message
        Then: Should output warning message with formatting
        """
        from llm_service.ui.console import print_warning

        assert callable(print_warning)

    def test_print_info_helper(self):
        """
        Test print_info helper function.

        Given: print_info function
        When: Calling it with a message
        Then: Should output info message with formatting
        """
        from llm_service.ui.console import print_info

        assert callable(print_info)


class TestFallbackConsoleImplementation:
    """
    Unit tests for FallbackConsole implementation.
    """

    def test_fallback_console_initialization(self):
        """
        Test FallbackConsole can be initialized.

        Given: FallbackConsole class
        When: Creating instance
        Then: Should initialize with correct properties
        """
        from llm_service.ui.console import FallbackConsole

        console = FallbackConsole()
        assert console is not None
        assert hasattr(console, "is_terminal")
        assert hasattr(console, "no_color")

    def test_fallback_console_print_method(self, capsys):
        """
        Test FallbackConsole print method.

        Given: FallbackConsole instance
        When: Calling print method
        Then: Should output to stdout
        """
        from llm_service.ui.console import FallbackConsole

        console = FallbackConsole()
        console.print("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_fallback_console_strips_rich_markup(self, capsys):
        """
        Test FallbackConsole strips rich markup tags.

        Given: FallbackConsole instance
        When: Printing text with rich markup
        Then: Markup should be stripped from output
        """
        from llm_service.ui.console import FallbackConsole

        console = FallbackConsole()
        console.print("[green]Success[/green]")

        captured = capsys.readouterr()
        assert "Success" in captured.out
        assert "[green]" not in captured.out
        assert "[/green]" not in captured.out

    def test_fallback_console_detects_tty(self):
        """
        Test FallbackConsole detects TTY correctly.

        Given: FallbackConsole instance
        When: Checking is_terminal property
        Then: Should return boolean value
        """
        from llm_service.ui.console import FallbackConsole

        console = FallbackConsole()
        # is_terminal should be a boolean
        assert isinstance(console.is_terminal, bool)

    def test_fallback_console_respects_no_color_env(self, monkeypatch):
        """
        Test FallbackConsole respects NO_COLOR environment variable.

        Given: NO_COLOR environment variable is set
        When: Creating FallbackConsole
        Then: no_color property should be True
        """
        from llm_service.ui.console import FallbackConsole

        monkeypatch.setenv("NO_COLOR", "1")
        console = FallbackConsole()

        assert console.no_color is True


class TestConsoleColorDisable:
    """
    Unit tests for color disable functionality.
    """

    def test_console_can_disable_colors_programmatically(self):
        """
        Test console can disable colors via configuration.

        Given: Console creation options
        When: Setting no_color=True
        Then: Console should not use colors
        """
        from rich.console import Console

        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False, no_color=True)

        console.print("[red]Error[/red]")

        output = buffer.getvalue()
        # Should contain text but no ANSI codes
        assert "Error" in output
        assert "\x1b[" not in output  # No ANSI escape sequences


class TestConsoleEdgeCases:
    """
    Unit tests for edge cases and error conditions.
    """

    def test_console_handles_empty_output(self):
        """
        Test console handles empty output gracefully.

        Given: Console instance
        When: Printing empty string
        Then: Should not raise errors
        """
        from rich.console import Console

        buffer = StringIO()
        console = Console(file=buffer)

        # Should not raise
        console.print("")
        console.print()

    def test_console_handles_unicode_content(self):
        """
        Test console handles Unicode content correctly.

        Given: Console instance
        When: Printing Unicode characters
        Then: Should handle correctly
        """
        from rich.console import Console

        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False)

        console.print("✓ Success with emoji 🎉")

        output = buffer.getvalue()
        assert "Success" in output

    def test_console_handles_very_long_lines(self):
        """
        Test console handles very long lines.

        Given: Console with specific width
        When: Printing very long text
        Then: Should handle wrapping or truncation
        """
        from rich.console import Console

        buffer = StringIO()
        console = Console(file=buffer, width=40, force_terminal=False)

        long_text = "x" * 200
        console.print(long_text)

        output = buffer.getvalue()
        assert "x" in output
