"""
Unit tests for subprocess execution wrapper.

Tests subprocess execution with timeout handling, error capture,
and platform compatibility following TDD approach (Directive 017).
"""

import pytest
import subprocess
import time
from typing import Optional


class TestExecutionResult:
    """Test ExecutionResult dataclass."""

    def test_execution_result_creation(self):
        """Test creating ExecutionResult with all fields."""
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult

        result = ExecutionResult(
            exit_code=0,
            stdout="Command output",
            stderr="",
            duration_seconds=1.5,
            command=["ls", "-la"],
            timed_out=False,
        )

        assert result.exit_code == 0
        assert result.stdout == "Command output"
        assert result.stderr == ""
        assert result.duration_seconds == 1.5
        assert result.command == ["ls", "-la"]
        assert result.timed_out is False

    def test_execution_result_is_dataclass(self):
        """Test that ExecutionResult is a proper dataclass."""
        from dataclasses import is_dataclass
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult

        assert is_dataclass(ExecutionResult)


class TestSubprocessWrapper:
    """Test basic subprocess execution."""

    def test_execute_simple_command(self):
        """Test executing a simple successful command."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        result = wrapper.execute(["echo", "hello"])

        assert result.exit_code == 0
        assert "hello" in result.stdout
        assert result.stderr == ""
        assert result.duration_seconds > 0
        assert result.timed_out is False

    def test_execute_command_with_arguments(self):
        """Test executing command with multiple arguments."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        result = wrapper.execute(["echo", "hello", "world"])

        assert result.exit_code == 0
        assert "hello world" in result.stdout or ("hello" in result.stdout and "world" in result.stdout)

    def test_execute_captures_stdout(self):
        """Test that stdout is captured correctly."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        result = wrapper.execute(["printf", "line1\\nline2\\nline3"])

        assert result.exit_code == 0
        assert "line1" in result.stdout
        assert "line2" in result.stdout
        assert "line3" in result.stdout

    def test_execute_captures_stderr(self):
        """Test that stderr is captured separately."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        # Use Python to write to stderr
        result = wrapper.execute(
            ["python3", "-c", "import sys; sys.stderr.write('error message')"]
        )

        assert result.exit_code == 0
        assert "error message" in result.stderr
        assert result.stdout == ""

    def test_execute_nonzero_exit_code(self):
        """Test command with non-zero exit code."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        result = wrapper.execute(["python3", "-c", "import sys; sys.exit(42)"])

        assert result.exit_code == 42
        assert result.timed_out is False


class TestSubprocessWrapperTimeout:
    """Test timeout handling."""

    def test_execute_with_timeout_success(self):
        """Test command completes within timeout."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper(timeout=5)
        result = wrapper.execute(["echo", "quick"])

        assert result.exit_code == 0
        assert result.timed_out is False
        assert result.duration_seconds < 5

    def test_execute_timeout_exceeded(self):
        """Test command timeout is enforced."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper(timeout=1)
        # Sleep for longer than timeout
        result = wrapper.execute(["sleep", "5"])

        assert result.timed_out is True
        assert result.duration_seconds >= 1
        assert result.exit_code != 0  # Process should be terminated

    def test_custom_timeout_per_command(self):
        """Test custom timeout can be set per execution."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper(timeout=10)  # Default timeout
        result = wrapper.execute(["sleep", "2"], timeout=1)  # Override with shorter timeout

        assert result.timed_out is True


class TestSubprocessWrapperErrors:
    """Test error handling."""

    def test_execute_command_not_found(self):
        """Test handling of command not found error."""
        from src.llm_service.adapters.subprocess_wrapper import (
            SubprocessWrapper,
            CommandNotFoundError,
        )

        wrapper = SubprocessWrapper()
        with pytest.raises(CommandNotFoundError, match="nonexistent_command"):
            wrapper.execute(["nonexistent_command_12345"])

    def test_execute_empty_command_list(self):
        """Test that empty command raises error."""
        from src.llm_service.adapters.subprocess_wrapper import (
            SubprocessWrapper,
            InvalidCommandError,
        )

        wrapper = SubprocessWrapper()
        with pytest.raises(InvalidCommandError, match="empty"):
            wrapper.execute([])

    def test_execute_with_invalid_command_type(self):
        """Test that non-list command raises error."""
        from src.llm_service.adapters.subprocess_wrapper import (
            SubprocessWrapper,
            InvalidCommandError,
        )

        wrapper = SubprocessWrapper()
        # Command should be a list, not a string
        with pytest.raises((InvalidCommandError, TypeError)):
            wrapper.execute("echo hello")  # type: ignore


class TestSubprocessWrapperSecurity:
    """Test security features."""

    def test_execute_uses_shell_false(self):
        """Test that shell=False is used (security requirement)."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        # This should be treated as literal arguments, not shell expansion
        result = wrapper.execute(["echo", "$HOME"])

        # With shell=False, $HOME is a literal string, not expanded
        assert "$HOME" in result.stdout

    def test_execute_no_shell_injection(self):
        """Test that shell injection is prevented."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        # Try to inject shell command with semicolon
        result = wrapper.execute(["echo", "test; ls"])

        # With shell=False, semicolon is treated as literal argument
        assert result.exit_code == 0
        # The echo command should output the literal string
        assert "test; ls" in result.stdout or result.stdout.strip() == "test; ls"

    def test_execute_command_as_list(self):
        """Test that command is passed as list (security requirement)."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        # Command must be list, not string (enforced by implementation)
        command = ["echo", "safe"]
        result = wrapper.execute(command)

        assert isinstance(command, list)
        assert result.exit_code == 0


class TestSubprocessWrapperPlatformCompatibility:
    """Test platform compatibility."""

    def test_execute_on_current_platform(self):
        """Test basic execution works on current platform."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper
        import sys

        wrapper = SubprocessWrapper()
        # Use Python which works on all platforms
        result = wrapper.execute(["python3", "--version"])

        assert result.exit_code == 0
        assert "Python" in result.stdout or "Python" in result.stderr

    def test_execute_with_environment_variables(self):
        """Test execution with custom environment variables."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        env = {"TEST_VAR": "test_value"}
        result = wrapper.execute(
            ["python3", "-c", "import os; print(os.environ.get('TEST_VAR', ''))"],
            env=env,
        )

        assert result.exit_code == 0
        assert "test_value" in result.stdout


class TestSubprocessWrapperEdgeCases:
    """Test edge cases."""

    def test_execute_command_with_large_output(self):
        """Test handling of large stdout output."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        # Generate large output (10000 lines)
        result = wrapper.execute(
            ["python3", "-c", "for i in range(10000): print(f'Line {i}')"]
        )

        assert result.exit_code == 0
        assert len(result.stdout.split("\n")) >= 10000

    def test_execute_command_with_binary_output(self):
        """Test handling of binary output."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        # Print some bytes
        result = wrapper.execute(
            ["python3", "-c", "import sys; sys.stdout.buffer.write(b'\\x00\\x01\\x02')"]
        )

        # Should handle binary data gracefully
        assert result.exit_code == 0
        # Output handling depends on implementation

    def test_execute_preserves_command_list(self):
        """Test that original command list is preserved in result."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        command = ["echo", "test", "123"]
        result = wrapper.execute(command)

        assert result.command == command
        assert result.command is not command  # Should be a copy

    def test_duration_measurement_accuracy(self):
        """Test that duration measurement is reasonably accurate."""
        from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper

        wrapper = SubprocessWrapper()
        result = wrapper.execute(["sleep", "0.5"])

        # Duration should be approximately 0.5 seconds (with some tolerance)
        assert 0.4 <= result.duration_seconds <= 1.5
