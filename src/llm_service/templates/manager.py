"""
Template Manager for Configuration Generation

Manages Jinja2 templates for generating LLM service configurations.
Implements ADR-031: Template-Based Configuration Generation.

Features:
- Load templates from package directory
- Jinja2 variable substitution
- Environment variable expansion (${VAR} syntax)
- Generate configuration files from templates
- Validate generated YAML

Usage:
    manager = TemplateManager()
    manager.generate_config(
        template_name='quick-start',
        output_path=Path('config.yaml'),
        context={'claude_binary': '/usr/local/bin/claude'}
    )
"""

import os
import re
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class TemplateManager:
    """
    Manages configuration templates for LLM service.

    Provides template discovery, loading, variable substitution,
    and configuration generation from Jinja2 templates.
    """

    def __init__(self, template_dir: Path | None = None):
        """
        Initialize template manager.

        Args:
            template_dir: Optional custom template directory.
                         Defaults to package templates directory.

        Raises:
            FileNotFoundError: If template directory doesn't exist
        """
        if template_dir is None:
            # Use package templates directory
            self.template_dir = Path(__file__).parent
        else:
            self.template_dir = Path(template_dir)

        # Verify directory exists
        if not self.template_dir.exists():
            raise FileNotFoundError(
                f"Template directory not found: {self.template_dir}"
            )

        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

    def list_templates(self) -> list[str]:
        """
        List available template names (without .j2 extension).

        Returns:
            List of template names
        """
        templates = []
        for template_file in self.template_dir.glob("*.yaml.j2"):
            # Remove .yaml.j2 extension to get template name
            name = template_file.stem.replace(".yaml", "")
            templates.append(name)
        return templates

    def template_exists(self, template_name: str) -> bool:
        """
        Check if template exists.

        Args:
            template_name: Template name (without extension)

        Returns:
            True if template file exists
        """
        template_file = self.template_dir / f"{template_name}.yaml.j2"
        return template_file.exists()

    def load_template(self, template_name: str) -> str:
        """
        Load template file content as string.

        Args:
            template_name: Template name (without extension)

        Returns:
            Template content as string

        Raises:
            ValueError: If template doesn't exist
        """
        template_file = self.template_dir / f"{template_name}.yaml.j2"

        if not template_file.exists():
            raise ValueError(
                f"Template '{template_name}' not found in {self.template_dir}"
            )

        return template_file.read_text()

    def substitute_variables(self, template: str, context: dict[str, Any]) -> str:
        """
        Substitute Jinja2 variables in template.

        Args:
            template: Template string with Jinja2 variables
            context: Dictionary of variable values

        Returns:
            Template with variables substituted
        """
        # Create a template from string
        jinja_template = self.jinja_env.from_string(template)

        # Render with context
        return jinja_template.render(**context)

    def expand_env_vars(self, yaml_content: str) -> str:
        """
        Expand ${VAR} environment variables in YAML content.

        Replaces ${VAR_NAME} with os.environ['VAR_NAME'].
        Leaves undefined variables as empty strings.

        Args:
            yaml_content: YAML content with ${VAR} placeholders

        Returns:
            YAML content with environment variables expanded
        """

        def replace_env_var(match):
            var_name = match.group(1)
            # Get from environment, empty string if not defined
            return os.environ.get(var_name, "")

        # Pattern: ${VAR_NAME}
        pattern = r"\$\{([A-Z_][A-Z0-9_]*)\}"
        return re.sub(pattern, replace_env_var, yaml_content)

    def generate_config(
        self,
        template_name: str,
        output_path: Path,
        context: dict[str, Any] | None = None,
    ) -> None:
        """
        Generate configuration file from template.

        Process:
        1. Load template file
        2. Substitute Jinja2 variables from context
        3. Expand ${VAR} environment variables
        4. Write to output file

        Args:
            template_name: Template name (without extension)
            output_path: Output file path
            context: Optional context dictionary for Jinja2

        Raises:
            ValueError: If template doesn't exist
            OSError: If output path is invalid
        """
        context = context or {}

        # Step 1: Load template
        template_file = self.template_dir / f"{template_name}.yaml.j2"

        if not template_file.exists():
            raise ValueError(
                f"Template '{template_name}' not found in {self.template_dir}"
            )

        # Step 2: Render Jinja2 template with context
        try:
            jinja_template = self.jinja_env.get_template(f"{template_name}.yaml.j2")
            rendered = jinja_template.render(**context)
        except TemplateNotFound:
            raise ValueError(
                f"Template '{template_name}' not found in {self.template_dir}"
            ) from None

        # Step 3: Expand environment variables (${VAR} syntax)
        # Note: We keep ${VAR} as-is in the file for runtime expansion
        # This allows users to configure API keys without hardcoding
        config_content = rendered

        # Step 4: Create parent directories if needed
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Step 5: Write to file
        output_path.write_text(config_content)

    def validate_template(self, template_name: str) -> bool:
        """
        Validate that template generates valid YAML.

        Args:
            template_name: Template name to validate

        Returns:
            True if template is valid YAML

        Raises:
            ValueError: If template is invalid
        """
        content = self.load_template(template_name)

        # Try to render with empty context
        rendered = self.substitute_variables(content, {})

        # Try to parse as YAML
        try:
            yaml.safe_load(rendered)
            return True
        except yaml.YAMLError as e:
            raise ValueError(f"Template '{template_name}' generates invalid YAML: {e}") from e
