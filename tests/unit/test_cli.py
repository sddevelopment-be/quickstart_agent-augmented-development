"""
Unit tests for CLI commands.
"""


import pytest
import yaml
from click.testing import CliRunner

from llm_service.cli import cli


@pytest.fixture
def runner():
    """Create Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def valid_config(tmp_path):
    """Create valid configuration directory."""
    agents_data = {
        "agents": {
            "test-agent": {
                "preferred_tool": "test-tool",
                "preferred_model": "test-model",
                "fallback_chain": [],
            }
        }
    }
    tools_data = {
        "tools": {
            "test-tool": {
                "binary": "test",
                "command_template": "{binary} {prompt_file} {model}",
                "models": ["test-model"],
            }
        }
    }
    models_data = {
        "models": {
            "test-model": {
                "provider": "test",
                "cost_per_1k_tokens": {"input": 0.01, "output": 0.03},
                "context_window": 8000,
            }
        }
    }
    policies_data = {"policies": {"default": {"daily_budget_usd": 10.0}}}

    (tmp_path / "agents.yaml").write_text(yaml.dump(agents_data))
    (tmp_path / "tools.yaml").write_text(yaml.dump(tools_data))
    (tmp_path / "models.yaml").write_text(yaml.dump(models_data))
    (tmp_path / "policies.yaml").write_text(yaml.dump(policies_data))

    return tmp_path


def test_cli_help(runner):
    """Test CLI help output."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "LLM Service Layer" in result.output
    assert "Configuration-driven agent-to-LLM routing" in result.output


def test_cli_version(runner):
    """Test version command."""
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    # Check for key parts separately since rich adds color codes between words
    assert "llm-service" in result.output
    assert "version" in result.output
    assert "0.1.0" in result.output


def test_config_validate_valid(runner, valid_config):
    """Test config validate with valid configuration."""
    result = runner.invoke(
        cli, ["--config-dir", str(valid_config), "config", "validate"]
    )
    assert result.exit_code == 0
    assert "Configuration is valid" in result.output
    assert "Agents" in result.output  # Now in table, not "Agents:"


def test_config_validate_missing_dir(runner, tmp_path):
    """Test config validate with missing directory."""
    nonexistent = tmp_path / "nonexistent"
    result = runner.invoke(
        cli, ["--config-dir", str(nonexistent), "config", "validate"]
    )
    assert result.exit_code == 1  # Command error for missing directory
    assert "does not exist" in result.output


def test_config_init(runner, tmp_path):
    """Test config init command."""
    result = runner.invoke(cli, ["--config-dir", str(tmp_path), "config", "init"])
    assert result.exit_code == 0
    assert "Setup Instructions" in result.output


def test_exec_command_valid_agent(runner, valid_config):
    """Test exec command with valid agent."""
    prompt_file = valid_config / "test.md"
    prompt_file.write_text("Test prompt")

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
    assert result.exit_code == 0
    assert "Agent configuration loaded" in result.output
    assert "test-tool" in result.output


def test_exec_command_invalid_agent(runner, valid_config):
    """Test exec command with invalid agent."""
    prompt_file = valid_config / "test.md"
    prompt_file.write_text("Test prompt")

    result = runner.invoke(
        cli,
        [
            "--config-dir",
            str(valid_config),
            "exec",
            "--agent",
            "nonexistent-agent",
            "--prompt-file",
            str(prompt_file),
        ],
    )
    assert result.exit_code == 1
    assert "not found in configuration" in result.output
