"""
Subprocess execution wrapper with security and error handling.

This module provides safe subprocess execution for tool adapters with:
- Timeout enforcement
- Separate stdout/stderr capture
- Platform compatibility (Linux/macOS/Windows)
- Security: shell=False enforcement

Security Design:
    - Always uses shell=False (per security review)
    - Command passed as list, not string
    - No shell expansion or metacharacter interpretation
    - Environment variable control
    
Examples:
    >>> from src.llm_service.adapters.subprocess_wrapper import SubprocessWrapper
    >>> 
    >>> wrapper = SubprocessWrapper(timeout=30)
    >>> result = wrapper.execute(["ls", "-la"])
    >>> print(f"Exit code: {result.exit_code}")
    >>> print(f"Output: {result.stdout}")
"""

import subprocess
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


class CommandNotFoundError(Exception):
    """Raised when command is not found."""

    pass


class InvalidCommandError(Exception):
    """Raised when command format is invalid."""

    pass


class SubprocessExecutionError(Exception):
    """Raised when subprocess execution fails."""

    pass


@dataclass
class ExecutionResult:
    """
    Result of subprocess execution.
    
    This dataclass provides complete information about subprocess execution
    including output, errors, timing, and exit status.
    
    Attributes:
        exit_code: Process exit code (0 for success, non-zero for error)
        stdout: Standard output from process (decoded as UTF-8)
        stderr: Standard error from process (decoded as UTF-8)
        duration_seconds: Execution duration in seconds
        command: Original command that was executed (copy of input)
        timed_out: Whether process exceeded timeout and was terminated
    
    Examples:
        >>> result = ExecutionResult(
        ...     exit_code=0,
        ...     stdout="Success",
        ...     stderr="",
        ...     duration_seconds=1.5,
        ...     command=["echo", "test"],
        ...     timed_out=False
        ... )
    """

    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    command: List[str]
    timed_out: bool = False


class SubprocessWrapper:
    """
    Safe subprocess execution wrapper for tool adapters.
    
    Executes external CLI tools with:
    - Configurable timeout enforcement
    - Separate stdout/stderr capture
    - Platform compatibility
    - Security (shell=False)
    - Error handling
    
    Security Features:
        - Always uses shell=False (no shell interpretation)
        - Command passed as list (prevents injection)
        - No shell metacharacter interpretation
        - Controlled environment variables
    
    Attributes:
        timeout: Default timeout in seconds (None = no timeout)
    
    Examples:
        >>> # Basic usage
        >>> wrapper = SubprocessWrapper(timeout=30)
        >>> result = wrapper.execute(["echo", "hello"])
        >>> print(result.stdout)
        'hello'
        
        >>> # With custom timeout
        >>> result = wrapper.execute(["long-command"], timeout=60)
        
        >>> # With environment variables
        >>> result = wrapper.execute(["cmd"], env={"VAR": "value"})
    """

    def __init__(self, timeout: Optional[float] = None):
        """
        Initialize subprocess wrapper.
        
        Args:
            timeout: Default timeout in seconds for command execution.
                    None means no timeout. Can be overridden per execution.
        """
        self.timeout = timeout

    def execute(
        self,
        command: List[str],
        timeout: Optional[float] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> ExecutionResult:
        """
        Execute command with subprocess.
        
        Executes command with:
        - Timeout enforcement (terminates if exceeded)
        - Separate stdout/stderr capture
        - shell=False for security
        - Error handling
        
        Args:
            command: Command as list of strings (e.g., ["ls", "-la"])
            timeout: Optional timeout override (uses default if not provided)
            env: Optional environment variables dictionary
        
        Returns:
            ExecutionResult with execution details
        
        Raises:
            InvalidCommandError: Command format is invalid
            CommandNotFoundError: Command binary not found
        
        Examples:
            >>> wrapper = SubprocessWrapper()
            >>> result = wrapper.execute(["echo", "test"])
            >>> assert result.exit_code == 0
        """
        # Validate command
        if not isinstance(command, list):
            raise InvalidCommandError(
                f"Command must be a list, not {type(command).__name__}"
            )

        if not command:
            raise InvalidCommandError("Command list cannot be empty")

        # Use provided timeout or default
        exec_timeout = timeout if timeout is not None else self.timeout

        # Prepare environment (merge with current if custom env provided)
        import os

        proc_env = os.environ.copy()
        if env:
            proc_env.update(env)

        # Store command copy for result
        command_copy = command.copy()

        # Execute subprocess
        start_time = time.time()
        timed_out = False
        exit_code = 0
        stdout_str = ""
        stderr_str = ""

        try:
            # Execute with shell=False for security
            process = subprocess.run(
                command,
                capture_output=True,
                shell=False,  # Security: no shell interpretation
                timeout=exec_timeout,
                env=proc_env,
                text=False,  # Get bytes, decode manually for better error handling
            )

            exit_code = process.returncode

            # Decode output with error handling
            stdout_str = self._decode_output(process.stdout)
            stderr_str = self._decode_output(process.stderr)

        except subprocess.TimeoutExpired:
            # Command exceeded timeout
            timed_out = True
            exit_code = -1  # Indicate timeout
            stdout_str = ""
            stderr_str = f"Command timed out after {exec_timeout} seconds"

        except FileNotFoundError as e:
            # Command binary not found
            raise CommandNotFoundError(
                f"Command not found: {command[0]}"
            ) from e

        except Exception as e:
            # Other execution errors
            raise SubprocessExecutionError(
                f"Failed to execute command {command}: {str(e)}"
            ) from e

        finally:
            # Calculate duration
            duration = time.time() - start_time

        # Return result
        return ExecutionResult(
            exit_code=exit_code,
            stdout=stdout_str,
            stderr=stderr_str,
            duration_seconds=duration,
            command=command_copy,
            timed_out=timed_out,
        )

    def _decode_output(self, output_bytes: bytes) -> str:
        """
        Decode subprocess output bytes to string.
        
        Tries UTF-8 first, falls back to latin-1 for binary data.
        
        Args:
            output_bytes: Raw bytes from subprocess
        
        Returns:
            Decoded string
        """
        if not output_bytes:
            return ""

        try:
            return output_bytes.decode("utf-8")
        except UnicodeDecodeError:
            # Fall back to latin-1 which never fails
            return output_bytes.decode("latin-1", errors="replace")
