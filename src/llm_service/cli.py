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
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
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
    
    # Validate config directory exists
    if not config_dir.exists():
        print_error(f"Configuration directory does not exist: {config_dir}")
        sys.exit(1)
    
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
    '--template',
    type=click.Choice(['quick-start', 'claude-only', 'cost-optimized', 'development']),
    default='quick-start',
    help='Configuration template to use (default: quick-start)',
)
@click.option(
    '--output',
    type=click.Path(path_type=Path),
    default=None,
    help='Output file path (default: ./config/generated-config.yaml)',
)
@click.option(
    '--force',
    is_flag=True,
    help='Overwrite existing configuration file',
)
@click.pass_context
def config_init(ctx, template, output, force):
    """
    Generate configuration from template.
    
    Creates a working configuration file from predefined templates:
    - quick-start: Minimal setup with Claude (recommended)
    - claude-only: Claude-focused configuration
    - cost-optimized: Multi-model with budget controls
    - development: All features with debug logging
    
    Automatically detects:
    - API keys in environment (ANTHROPIC_API_KEY, etc.)
    - Tool binaries in PATH
    - Operating system platform
    
    Use --force to overwrite existing files.
    """
    from llm_service.templates.manager import TemplateManager
    from llm_service.utils.env_scanner import EnvironmentScanner
    
    config_dir = ctx.obj['config_dir']
    
    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine output path
    if output is None:
        output = Path(config_dir) / "generated-config.yaml"
    else:
        output = Path(output)
    
    # Check if file exists
    if output.exists() and not force:
        console.print(Panel(
            f"Configuration file already exists: [cyan]{output}[/cyan]\n\n"
            "Use [bold]--force[/bold] to overwrite",
            title="⚠️  File Exists",
            border_style="yellow"
        ))
        sys.exit(1)
    
    # Header
    console.print(Panel.fit(
        "[bold cyan]Configuration Generation[/bold cyan]",
        subtitle=f"Template: {template}",
        border_style="blue"
    ))
    console.print()
    
    try:
        # Scan environment
        console.print("[cyan]→[/cyan] Scanning environment...")
        scanner = EnvironmentScanner()
        env_info = scanner.scan_all()
        context = scanner.generate_context_for_template()
        
        # Generate config
        console.print("[cyan]→[/cyan] Generating configuration...")
        manager = TemplateManager()
        manager.generate_config(template, output, context)
        
        # Success
        console.print()
        print_success(f"Configuration generated: [cyan]{output}[/cyan]")
        console.print()
        
        # Show environment status
        table = Table(title="Environment Status", show_header=True, header_style="bold cyan")
        table.add_column("Dependency", style="cyan", width=20)
        table.add_column("Status", style="magenta", width=15)
        
        # API keys
        for key, present in env_info['api_keys'].items():
            symbol = "✅" if present else "❌"
            status = "Found" if present else "Missing"
            table.add_row(key, f"{symbol} {status}")
        
        # Binaries
        for tool, path in env_info['binaries'].items():
            if path:
                table.add_row(f"{tool} binary", f"✅ {path}")
        
        # Platform
        table.add_row("Platform", f"✅ {env_info['platform']}")
        
        console.print(table)
        console.print()
        
        # Next steps
        missing_keys = scanner.get_missing_api_keys()
        if missing_keys:
            console.print(Panel(
                "[bold]Next Steps:[/bold]\n\n"
                f"1. Set missing API keys: {', '.join(missing_keys)}\n"
                f"2. Review configuration: [cyan]llm-service config show {output}[/cyan]\n"
                "3. Validate configuration: [cyan]llm-service config validate[/cyan]\n"
                f"4. Update config file to use your settings: [cyan]{output}[/cyan]",
                title="📋 Setup Instructions",
                border_style="blue"
            ))
        else:
            console.print(Panel(
                "[bold]Next Steps:[/bold]\n\n"
                f"1. Review configuration: [cyan]llm-service config show {output}[/cyan]\n"
                "2. Validate configuration: [cyan]llm-service config validate[/cyan]\n"
                "3. Start using: [cyan]llm-service exec --agent default-agent --prompt-file prompt.txt[/cyan]",
                title="✅ Ready to Use",
                border_style="green"
            ))
        
    except Exception as e:
        console.print()
        console.print(Panel(
            f"[red]Error:[/red] {str(e)}",
            title="❌ Configuration Failed",
            border_style="red"
        ))
        sys.exit(1)


@config_group.command(name='templates')
def config_templates():
    """
    List available configuration templates.
    
    Shows all predefined templates with descriptions.
    """
    from llm_service.templates import AVAILABLE_TEMPLATES
    
    console.print(Panel.fit(
        "[bold cyan]Available Configuration Templates[/bold cyan]",
        border_style="blue"
    ))
    console.print()
    
    table = Table(title="Configuration Templates", show_header=True, header_style="bold cyan")
    table.add_column("Template", style="cyan", width=18)
    table.add_column("Description", style="white", width=40)
    table.add_column("Suitable For", style="dim", width=30)
    
    for name, info in AVAILABLE_TEMPLATES.items():
        table.add_row(name, info['description'], info['suitable_for'])
    
    console.print(table)
    console.print()
    
    console.print(Panel(
        "[bold]Usage:[/bold]\n\n"
        "[cyan]llm-service config init --template <name>[/cyan]\n\n"
        "Example:\n"
        "[cyan]llm-service config init --template quick-start[/cyan]",
        title="💡 How to Use",
        border_style="blue"
    ))


@config_group.command(name='show')
@click.argument('config_file', type=click.Path(exists=True, path_type=Path), required=False)
@click.pass_context
def config_show(ctx, config_file):
    """
    Display configuration file with syntax highlighting.
    
    Shows the current or specified configuration file in formatted YAML.
    
    Arguments:
        config_file: Path to configuration file (optional)
    """
    from rich.syntax import Syntax
    import yaml
    
    # Determine which file to show
    if config_file is None:
        config_dir = ctx.obj['config_dir']
        # Look for generated config first, then default files
        possible_files = [
            Path(config_dir) / "generated-config.yaml",
            Path(config_dir) / "config.yaml",
            Path(config_dir) / "agents.yaml",
        ]
        
        config_file = None
        for f in possible_files:
            if f.exists():
                config_file = f
                break
        
        if config_file is None:
            console.print(Panel(
                f"[yellow]No configuration file found in {config_dir}[/yellow]\n\n"
                "Run [cyan]llm-service config init[/cyan] to generate a configuration.",
                title="⚠️  No Config Found",
                border_style="yellow"
            ))
            sys.exit(1)
    else:
        config_file = Path(config_file)
    
    # Header
    console.print(Panel.fit(
        "[bold cyan]Configuration Display[/bold cyan]",
        subtitle=f"File: {config_file}",
        border_style="blue"
    ))
    console.print()
    
    try:
        # Read and display file
        yaml_content = config_file.read_text()
        
        # Validate it's valid YAML
        yaml.safe_load(yaml_content)
        
        # Display with syntax highlighting
        syntax = Syntax(
            yaml_content,
            "yaml",
            theme="monokai",
            line_numbers=True,
            word_wrap=False
        )
        console.print(syntax)
        
    except yaml.YAMLError as e:
        console.print(Panel(
            f"[red]Invalid YAML:[/red] {str(e)}",
            title="❌ YAML Error",
            border_style="red"
        ))
        sys.exit(1)
    except Exception as e:
        console.print(Panel(
            f"[red]Error:[/red] {str(e)}",
            title="❌ Error Reading File",
            border_style="red"
        ))
        sys.exit(1)


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


@cli.group(name='tool')
def tool_group():
    """Tool management commands."""
    pass


@tool_group.command(name='list')
@click.pass_context
def tool_list(ctx):
    """
    List configured tools.
    
    Displays all tools defined in configuration with their models and status.
    """
    config_dir = ctx.obj['config_dir']
    
    console.print(Panel.fit(
        "[bold cyan]Configured Tools[/bold cyan]",
        subtitle=f"Config: {config_dir}",
        border_style="blue"
    ))
    console.print()
    
    try:
        # Load configuration
        config = load_configuration(str(config_dir))
        tools = config['tools'].tools
        
        if not tools:
            console.print("[yellow]No tools configured[/yellow]")
            sys.exit(0)
        
        # Create table
        table = Table(title="Tools", show_header=True, header_style="bold cyan")
        table.add_column("Tool", style="cyan", width=15)
        table.add_column("Models", style="magenta", width=40)
        table.add_column("Binary", style="white", width=25)
        table.add_column("Status", style="green", width=10)
        
        for tool_name, tool_config in tools.items():
            models = ", ".join(tool_config.models[:3])  # Show first 3
            if len(tool_config.models) > 3:
                models += f" +{len(tool_config.models) - 3} more"
            
            binary = tool_config.binary
            
            # Check if binary exists (simplified check)
            status = "✓" if binary else "?"
            
            table.add_row(tool_name, models, binary, status)
        
        console.print(table)
        console.print()
        console.print(f"[dim]Total: {len(tools)} tools[/dim]")
        
    except ConfigurationError as e:
        print_error("Configuration error!")
        console.print(Panel(str(e), title="[red]Error[/red]", border_style="red"))
        sys.exit(1)


@tool_group.command(name='add')
@click.argument('tool_name')
@click.option('--binary', required=True, help='Binary path or command')
@click.option('--models', required=True, help='Comma-separated list of model names')
@click.option('--command-template', help='Command template (optional)')
@click.pass_context
def tool_add(ctx, tool_name, binary, models, command_template):
    """
    Add a new tool to configuration.
    
    Arguments:
        tool_name: Name for the tool (e.g., 'gemini', 'claude-code')
    
    Examples:
        llm-service tool add gemini --binary gemini-cli --models "gemini-1.5-pro,gemini-1.5-flash"
    """
    console.print(Panel.fit(
        f"[bold cyan]Adding Tool: {tool_name}[/bold cyan]",
        border_style="blue"
    ))
    console.print()
    
    console.print("[yellow]⚠️  Note: Tool management commands are planned for Milestone 5[/yellow]")
    console.print()
    console.print("[dim]For now, please manually edit your configuration files:[/dim]")
    console.print(f"[dim]1. Open tools.yaml[/dim]")
    console.print(f"[dim]2. Add tool configuration for '{tool_name}'[/dim]")
    console.print(f"[dim]3. Run 'llm-service config validate' to verify[/dim]")
    console.print()
    
    # Show what the entry would look like
    models_list = [m.strip() for m in models.split(',')]
    template = command_template or f"{{binary}} --model {{model}} < {{prompt_file}}"
    
    console.print(Panel(
        f"[bold]Example configuration:[/bold]\n\n"
        f"```yaml\n"
        f"{tool_name}:\n"
        f"  binary: \"{binary}\"\n"
        f"  command_template: \"{template}\"\n"
        f"  models:\n" +
        "\n".join(f"    - \"{m}\"" for m in models_list) +
        "\n```",
        title="💡 Configuration Template",
        border_style="blue"
    ))


@tool_group.command(name='remove')
@click.argument('tool_name')
@click.pass_context
def tool_remove(ctx, tool_name):
    """
    Remove a tool from configuration.
    
    Arguments:
        tool_name: Name of tool to remove
    """
    console.print(Panel.fit(
        f"[bold cyan]Removing Tool: {tool_name}[/bold cyan]",
        border_style="blue"
    ))
    console.print()
    
    console.print("[yellow]⚠️  Note: Tool management commands are planned for Milestone 5[/yellow]")
    console.print()
    console.print("[dim]For now, please manually edit your configuration files:[/dim]")
    console.print(f"[dim]1. Open tools.yaml[/dim]")
    console.print(f"[dim]2. Remove tool configuration for '{tool_name}'[/dim]")
    console.print(f"[dim]3. Run 'llm-service config validate' to verify[/dim]")


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
    
    # Validate config directory exists
    if not config_dir.exists():
        print_error(f"Configuration directory does not exist: {config_dir}")
        console.print("\n💡 Tip: Run [bold cyan]llm-service config init[/bold cyan] to create configuration.")
        sys.exit(1)
    
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
