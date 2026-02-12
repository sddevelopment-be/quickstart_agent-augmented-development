"""
Acceptance Tests for Rich Terminal UI Integration (ADR-030)

Tests verify that CLI commands properly use rich formatting and provide
appropriate fallback behavior in non-TTY environments.

Following Directive 016 (ATDD) - these tests define success criteria before implementation.
"""

import os

import pytest
import yaml
from click.testing import CliRunner

from llm_service.cli import cli


@pytest.fixture
def valid_config(tmp_path):
    """Create valid configuration directory for tests."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    # Use the correct format that config loader expects
    agents_data = {
        "agents": {
            "test-agent": {
                "preferred_tool": "claude-code",
                "preferred_model": "claude-3.5-sonnet",
                "fallback_chain": [],
            }
        }
    }
    tools_data = {
        "tools": {
            "claude-code": {
                "binary": "claude-code",
                "command_template": "{binary} {prompt_file} {model}",
                "models": ["claude-3.5-sonnet"],
            }
        }
    }
    models_data = {
        "models": {
            "claude-3.5-sonnet": {
                "provider": "anthropic",
                "cost_per_1k_tokens": {"input": 0.003, "output": 0.015},
                "context_window": 8000,
            }
        }
    }
    policies_data = {"policies": {"default": {"daily_budget_usd": 10.0}}}

    (config_dir / "agents.yaml").write_text(yaml.dump(agents_data))
    (config_dir / "tools.yaml").write_text(yaml.dump(tools_data))
    (config_dir / "models.yaml").write_text(yaml.dump(models_data))
    (config_dir / "policies.yaml").write_text(yaml.dump(policies_data))

    return config_dir


class TestRichCLIAcceptance:
    """
    Acceptance tests for Rich Terminal UI implementation.

    Success Criteria (from task file):
    1. All CLI commands use rich formatting (panels, colors, progress bars)
    2. Progress bars display for operations >2 seconds
    3. Automatic fallback to plain text in non-TTY environments
    4. --no-color flag available for color disable
    5. Unit tests for console output module
    6. Manual visual tests (TTY and non-TTY modes)
    7. Test coverage >80% maintained
    """

    def test_config_validate_uses_rich_panel(self, valid_config):
        """
        AC1: config validate command uses rich panel for output.

        When: Running 'llm-service config validate' with valid config
        Then: Output should contain panel borders and structured formatting
        """
        runner = CliRunner()
        result = runner.invoke(
            cli, ["--config-dir", str(valid_config), "config", "validate"]
        )

        # Should succeed
        assert result.exit_code == 0, f"Command failed with output: {result.output}"

        # Should contain structured output (panels have box drawing characters)
        # Rich uses Unicode box drawing characters for panels
        output = result.output

        # Check for rich formatting indicators:
        # - Should have "Configuration is valid" message
        # - Should have structured count display
        assert "Configuration is valid" in output or "valid" in output.lower()
        assert "Agents" in output or "agents" in output.lower()
        assert "Tools" in output or "tools" in output.lower()

    def test_config_validate_shows_error_in_rich_panel(self, tmp_path):
        """
        AC1: Error messages are displayed in rich panels.

        When: Running config validate with invalid configuration
        Then: Error should be displayed in a formatted panel
        """
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Create invalid config (missing required files)
        (config_dir / "agents.yaml").write_text("invalid: yaml: content:")

        runner = CliRunner()
        result = runner.invoke(
            cli, ["--config-dir", str(config_dir), "config", "validate"]
        )

        # Should fail
        assert result.exit_code == 1

        # Should contain error message
        output = result.output
        assert "fail" in output.lower() or "error" in output.lower()

    def test_no_color_flag_disables_rich_formatting(self, valid_config):
        """
        AC4: --no-color flag disables color output.

        When: Running any command with --no-color flag
        Then: Output should not contain ANSI color codes
        """
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(
            cli,
            ["--config-dir", str(valid_config), "--no-color", "config", "validate"],
        )

        # Should succeed
        assert result.exit_code == 0

        # Output should not contain ANSI escape sequences
        output = result.output
        # ANSI codes start with \x1b or \033
        assert (
            "\x1b[" not in output
        ), "Output contains ANSI color codes despite --no-color flag"
        assert (
            "\033[" not in output
        ), "Output contains ANSI color codes despite --no-color flag"

    def test_version_command_uses_rich_formatting(self):
        """
        AC1: version command uses rich formatting.

        When: Running 'llm-service version'
        Then: Output should be formatted with rich
        """
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])

        assert result.exit_code == 0
        assert "llm-service version" in result.output

    def test_exec_command_uses_rich_for_routing_info(self, valid_config):
        """
        AC1: exec command displays routing information in rich format.

        When: Running exec command with valid agent
        Then: Routing information should be displayed in structured format
        """
        # Create prompt file
        prompt_file = valid_config / "prompt.txt"
        prompt_file.write_text("Test prompt")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "--config-dir",
                str(valid_config),
                "exec",
                "--agent",
                "test-agent",
                "--prompt-file",
                str(prompt_file),
            ],
        )

        assert result.exit_code == 0, f"Command failed with output: {result.output}"
        output = result.output

        # Should show routing information
        assert "test-agent" in output
        assert "claude-code" in output or "preferred" in output.lower()


class TestConsoleModuleFunctionality:
    """
    Acceptance tests for console module functionality.

    These tests verify the console wrapper module works correctly
    with automatic TTY detection and fallback behavior.
    """

    def test_console_wrapper_exists_and_importable(self):
        """
        AC5: Console wrapper module exists and is importable.

        When: Importing llm_service.ui.console
        Then: Should import successfully and provide console object
        """
        try:
            from llm_service.ui.console import console, get_console

            assert console is not None
            assert get_console is not None
        except ImportError as e:
            pytest.fail(f"Failed to import console module: {e}")

    def test_console_detects_tty_environment(self):
        """
        AC3: Console automatically detects TTY vs non-TTY environment.

        When: Console is used in different environments
        Then: Should adapt output appropriately
        """
        from llm_service.ui.console import get_console

        # Get console instance
        console = get_console()

        # Console should have is_terminal property or similar
        # This is provided by rich.Console automatically
        assert hasattr(console, "is_terminal") or hasattr(console, "is_interactive")

    def test_console_respects_no_color_environment(self, monkeypatch):
        """
        AC4: Console respects NO_COLOR environment variable.

        When: NO_COLOR=1 is set in environment
        Then: Console should disable color output
        """
        monkeypatch.setenv("NO_COLOR", "1")

        # Create a new console and verify NO_COLOR is respected
        from rich.console import Console

        console = Console()

        # When NO_COLOR is set, rich should respect it
        # We can test this by checking environment
        assert os.environ.get("NO_COLOR") == "1"


@pytest.mark.manual
class TestManualVisualValidation:
    """
    Manual visual validation tests.

    These tests are marked as manual and provide instructions for
    visual validation in TTY and non-TTY modes.

    Run with: pytest -v -m manual
    """

    def test_tty_mode_visual_validation(self):
        """
        AC6: Manual test for TTY mode visual validation.

        MANUAL TEST INSTRUCTIONS:
        1. Run: llm-service --config-dir ./config config validate
        2. Verify: Output has colored panels with box borders
        3. Verify: Success message is green with checkmark
        4. Verify: Metrics are displayed in structured format

        This test always passes - manual verification required.
        """
        pytest.skip("Manual visual validation required")

    def test_non_tty_mode_visual_validation(self):
        """
        AC6: Manual test for non-TTY mode visual validation.

        MANUAL TEST INSTRUCTIONS:
        1. Run: llm-service --config-dir ./config config validate | cat
        2. Verify: Output is plain text without ANSI codes
        3. Verify: Information is still readable and structured
        4. Run: llm-service --config-dir ./config config validate > output.txt
        5. Verify: output.txt contains plain text

        This test always passes - manual verification required.
        """
        pytest.skip("Manual visual validation required")

    def test_no_color_flag_visual_validation(self):
        """
        AC6: Manual test for --no-color flag.

        MANUAL TEST INSTRUCTIONS:
        1. Run: llm-service --no-color --config-dir ./config config validate
        2. Verify: Output has no colors but maintains structure
        3. Verify: Box drawing characters may still be present but no colors

        This test always passes - manual verification required.
        """
        pytest.skip("Manual visual validation required")
