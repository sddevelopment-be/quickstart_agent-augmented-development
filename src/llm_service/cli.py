"""
LLM Service Layer CLI

Command-line interface for the LLM service layer.
Provides commands for configuration validation, initialization, and service execution.
"""

import click
import sys
from pathlib import Path
from typing import Optional

from llm_service import __version__
from llm_service.config.loader import load_configuration, ConfigurationError


@click.group()
@click.version_option(version=__version__, prog_name='llm-service')
@click.option(
    '--config-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default='./config',
    help='Path to configuration directory (default: ./config)',
    show_default=True,
)
@click.pass_context
def cli(ctx, config_dir):
    """
    LLM Service Layer - Configuration-driven agent-to-LLM routing.
    
    Route agent requests to appropriate LLM tools based on YAML configuration.
    Supports cost optimization, budget enforcement, and automatic fallbacks.
    """
    ctx.ensure_object(dict)
    ctx.obj['config_dir'] = config_dir


@cli.group(name='config')
def config_group():
    """Configuration management commands."""
    pass


@config_group.command(name='validate')
@click.pass_context
def config_validate(ctx):
    """
    Validate configuration files.
    
    Checks:
    - YAML syntax correctness
    - Schema validation (required fields, types)
    - Cross-reference validation (agent→tool, agent→model)
    
    Exit codes:
    - 0: Configuration is valid
    - 1: Configuration has errors
    """
    config_dir = ctx.obj['config_dir']
    
    click.echo(f"Validating configuration in: {config_dir}")
    click.echo()
    
    try:
        config = load_configuration(str(config_dir))
        
        # Report what was loaded
        click.secho("✓ Configuration is valid!", fg='green', bold=True)
        click.echo()
        click.echo(f"  Agents:   {len(config['agents'].agents)} configured")
        click.echo(f"  Tools:    {len(config['tools'].tools)} configured")
        click.echo(f"  Models:   {len(config['models'].models)} configured")
        click.echo(f"  Policies: {len(config['policies'].policies)} configured")
        
        sys.exit(0)
    except ConfigurationError as e:
        click.secho("✗ Configuration validation failed!", fg='red', bold=True)
        click.echo()
        click.echo(str(e), err=True)
        sys.exit(1)
    except Exception as e:
        click.secho("✗ Unexpected error!", fg='red', bold=True)
        click.echo(f"{type(e).__name__}: {e}", err=True)
        sys.exit(1)


@config_group.command(name='init')
@click.option(
    '--force',
    is_flag=True,
    help='Overwrite existing configuration files',
)
@click.pass_context
def config_init(ctx, force):
    """
    Initialize configuration directory with example files.
    
    Creates example configuration files:
    - agents.yaml.example
    - tools.yaml.example
    - models.yaml.example
    - policies.yaml.example
    
    Use --force to overwrite existing files.
    """
    config_dir = ctx.obj['config_dir']
    
    click.echo(f"Initializing configuration in: {config_dir}")
    click.echo()
    
    # For MVP, just inform user about example files
    example_files = ['agents.yaml.example', 'tools.yaml.example', 'models.yaml.example', 'policies.yaml.example']
    
    click.echo("Example configuration files are available in the config/ directory:")
    for filename in example_files:
        click.echo(f"  - {filename}")
    
    click.echo()
    click.echo("To use them:")
    click.echo("  1. Copy .example files to remove the .example suffix")
    click.echo("  2. Edit the files to match your environment")
    click.echo("  3. Run 'llm-service config validate' to check")
    
    click.secho("\n✓ Refer to example files for configuration setup", fg='green')


@cli.command(name='version')
def version_command():
    """Display version information."""
    click.echo(f"llm-service version {__version__}")
    click.echo()
    click.echo("LLM Service Layer - Configuration-driven agent-to-LLM routing")
    click.echo("Python implementation with Pydantic validation")


@cli.command(name='exec')
@click.option(
    '--agent',
    required=True,
    help='Agent name (must exist in agents.yaml)',
)
@click.option(
    '--prompt-file',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    required=True,
    help='Path to prompt file',
)
@click.option(
    '--task-type',
    help='Task type for model selection (e.g., "simple", "complex", "coding")',
)
@click.pass_context
def exec_command(ctx, agent, prompt_file, task_type):
    """
    Execute agent request via configured LLM tool.
    
    Routes the agent's request to the appropriate LLM tool based on:
    - Agent preferences (agents.yaml)
    - Task type (if specified)
    - Model costs and availability
    - Fallback chains
    
    Note: In MVP, this command validates routing but does not execute actual tools.
    Tool execution will be implemented in Milestone 2.
    """
    config_dir = ctx.obj['config_dir']
    
    click.echo(f"Executing request for agent: {agent}")
    click.echo(f"Prompt file: {prompt_file}")
    if task_type:
        click.echo(f"Task type: {task_type}")
    click.echo()
    
    try:
        # Load configuration
        config = load_configuration(str(config_dir))
        
        # Check agent exists
        if agent not in config['agents'].agents:
            available = ', '.join(config['agents'].agents.keys())
            click.secho(f"✗ Agent '{agent}' not found in configuration", fg='red', bold=True)
            click.echo(f"Available agents: {available}", err=True)
            sys.exit(1)
        
        # For MVP: Just show routing decision
        agent_config = config['agents'].agents[agent]
        click.secho("✓ Agent configuration loaded", fg='green')
        click.echo(f"  Preferred tool: {agent_config.preferred_tool}")
        click.echo(f"  Preferred model: {agent_config.preferred_model}")
        
        if task_type and task_type in (agent_config.task_types or {}):
            override_model = agent_config.task_types[task_type]
            click.echo(f"  Task-specific override: {override_model}")
        
        click.echo()
        click.secho("Note: Tool execution not yet implemented (Milestone 2)", fg='yellow')
        click.echo("This command will invoke the actual LLM tool in a future release.")
        
    except ConfigurationError as e:
        click.secho("✗ Configuration error!", fg='red', bold=True)
        click.echo(str(e), err=True)
        sys.exit(1)
    except Exception as e:
        click.secho("✗ Unexpected error!", fg='red', bold=True)
        click.echo(f"{type(e).__name__}: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for CLI."""
    cli(obj={})


if __name__ == '__main__':
    main()
