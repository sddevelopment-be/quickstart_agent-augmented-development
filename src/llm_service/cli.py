"""
LLM Service Layer CLI

Command-line interface for the LLM service layer.
Provides commands for configuration validation, initialization, and service execution.

Enhanced with rich terminal UI (ADR-030).
"""

import click
import sys
from pathlib import Path
from typing import Optional

from llm_service import __version__
from llm_service.config.loader import load_configuration, ConfigurationError
from llm_service.ui.console import console, print_success, print_error, print_warning
from rich.panel import Panel
from rich.table import Table


@click.group()
@click.version_option(version=__version__, prog_name='llm-service')
@click.option(
    '--config-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default='./config',
    help='Path to configuration directory (default: ./config)',
    show_default=True,
)
@click.option(
    '--no-color',
    is_flag=True,
    help='Disable colored output',
    default=False,
)
@click.pass_context
def cli(ctx, config_dir, no_color):
    """
    LLM Service Layer - Configuration-driven agent-to-LLM routing.
    
    Route agent requests to appropriate LLM tools based on YAML configuration.
    Supports cost optimization, budget enforcement, and automatic fallbacks.
    """
    ctx.ensure_object(dict)
    ctx.obj['config_dir'] = config_dir
    ctx.obj['no_color'] = no_color
    
    # Update console color setting if --no-color flag is used
    if no_color:
        console.no_color = True


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
    
    # Header
    console.print(Panel.fit(
        "[bold cyan]Configuration Validation[/bold cyan]",
        subtitle=f"Directory: {config_dir}",
        border_style="blue"
    ))
    console.print()
    
    try:
        config = load_configuration(str(config_dir))
        
        # Success panel
        print_success("Configuration is valid!")
        console.print()
        
        # Create metrics table
        table = Table(title="Configuration Summary", show_header=True, header_style="bold cyan")
        table.add_column("Component", style="cyan", width=12)
        table.add_column("Count", justify="right", style="magenta")
        
        table.add_row("Agents", str(len(config['agents'].agents)))
        table.add_row("Tools", str(len(config['tools'].tools)))
        table.add_row("Models", str(len(config['models'].models)))
        table.add_row("Policies", str(len(config['policies'].policies)))
        
        console.print(table)
        
        sys.exit(0)
    except ConfigurationError as e:
        print_error("Configuration validation failed!")
        console.print()
        console.print(Panel(
            str(e),
            title="[red]Error Details[/red]",
            border_style="red"
        ))
        sys.exit(1)
    except Exception as e:
        print_error("Unexpected error!")
        console.print()
        console.print(Panel(
            f"[red]{type(e).__name__}:[/red] {e}",
            title="[red]Unexpected Error[/red]",
            border_style="red"
        ))
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
    
    console.print(Panel.fit(
        "[bold cyan]Configuration Initialization[/bold cyan]",
        subtitle=f"Directory: {config_dir}",
        border_style="blue"
    ))
    console.print()
    
    # For MVP, just inform user about example files
    example_files = ['agents.yaml.example', 'tools.yaml.example', 'models.yaml.example', 'policies.yaml.example']
    
    console.print("[bold]Example configuration files are available in the config/ directory:[/bold]")
    for filename in example_files:
        console.print(f"  [cyan]•[/cyan] {filename}")
    
    console.print()
    console.print("[bold]To use them:[/bold]")
    console.print("  [cyan]1.[/cyan] Copy .example files to remove the .example suffix")
    console.print("  [cyan]2.[/cyan] Edit the files to match your environment")
    console.print("  [cyan]3.[/cyan] Run 'llm-service config validate' to check")
    
    console.print()
    print_success("Refer to example files for configuration setup")


@cli.command(name='version')
def version_command():
    """Display version information."""
    console.print(Panel(
        f"[bold cyan]llm-service[/bold cyan] version [bold magenta]{__version__}[/bold magenta]\n\n"
        "LLM Service Layer - Configuration-driven agent-to-LLM routing\n"
        "Python implementation with Pydantic validation",
        title="Version Information",
        border_style="cyan"
    ))


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
    
    # Header
    console.print(Panel.fit(
        "[bold cyan]Agent Request Execution[/bold cyan]",
        subtitle=f"Agent: {agent}",
        border_style="blue"
    ))
    console.print()
    
    console.print(f"[bold]Prompt file:[/bold] {prompt_file}")
    if task_type:
        console.print(f"[bold]Task type:[/bold] {task_type}")
    console.print()
    
    try:
        # Load configuration
        config = load_configuration(str(config_dir))
        
        # Check agent exists
        if agent not in config['agents'].agents:
            available = ', '.join(config['agents'].agents.keys())
            print_error(f"Agent '{agent}' not found in configuration")
            console.print(f"[yellow]Available agents:[/yellow] {available}")
            sys.exit(1)
        
        # For MVP: Show routing decision
        agent_config = config['agents'].agents[agent]
        
        print_success("Agent configuration loaded")
        
        # Create routing info table
        table = Table(title="Routing Information", show_header=True, header_style="bold cyan")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Preferred Tool", agent_config.preferred_tool)
        table.add_row("Preferred Model", agent_config.preferred_model)
        
        if task_type and task_type in (agent_config.task_types or {}):
            override_model = agent_config.task_types[task_type]
            table.add_row("Task Override", override_model)
        
        console.print(table)
        console.print()
        
        print_warning("Tool execution not yet implemented (Milestone 2)")
        console.print("[dim]This command will invoke the actual LLM tool in a future release.[/dim]")
        
    except ConfigurationError as e:
        print_error("Configuration error!")
        console.print()
        console.print(Panel(
            str(e),
            title="[red]Error Details[/red]",
            border_style="red"
        ))
        sys.exit(1)
    except Exception as e:
        print_error("Unexpected error!")
        console.print()
        console.print(Panel(
            f"[red]{type(e).__name__}:[/red] {e}",
            title="[red]Unexpected Error[/red]",
            border_style="red"
        ))
        sys.exit(1)


def main():
    """Entry point for CLI."""
    cli(obj={})


if __name__ == '__main__':
    main()
