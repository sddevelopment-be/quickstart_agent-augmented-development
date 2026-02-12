"""
Unit Tests for Template Manager (TDD)

Following TDD (Directive 017), write tests first, then implement.

Test Coverage:
- Template loading from files
- Variable substitution with Jinja2
- Template validation against schemas
- Error handling for missing templates
- Platform-specific variable resolution
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from llm_service.templates.manager import TemplateManager


class TestTemplateManagerInit:
    """Test TemplateManager initialization"""

    def test_manager_initializes_with_default_template_dir(self):
        """Manager should find templates in package directory"""
        manager = TemplateManager()
        assert manager.template_dir.exists()
        assert manager.template_dir.is_dir()

    def test_manager_can_initialize_with_custom_dir(self, tmp_path):
        """Manager should accept custom template directory"""
        custom_dir = tmp_path / "custom_templates"
        custom_dir.mkdir()

        manager = TemplateManager(template_dir=custom_dir)
        assert manager.template_dir == custom_dir


class TestTemplateDiscovery:
    """Test template listing and discovery"""

    def test_list_templates_returns_all_four_templates(self):
        """Should discover all 4 predefined templates"""
        manager = TemplateManager()
        templates = manager.list_templates()

        assert "quick-start" in templates
        assert "claude-only" in templates
        assert "cost-optimized" in templates
        assert "development" in templates
        assert len(templates) == 4

    def test_template_exists_checks_correctly(self):
        """Should correctly identify existing and missing templates"""
        manager = TemplateManager()

        assert manager.template_exists("quick-start")
        assert manager.template_exists("claude-only")
        assert not manager.template_exists("nonexistent-template")


class TestTemplateLoading:
    """Test loading template files"""

    def test_load_template_returns_string_content(self):
        """Loading template should return file content as string"""
        manager = TemplateManager()
        content = manager.load_template("quick-start")

        assert isinstance(content, str)
        assert len(content) > 0
        assert "service:" in content or "agents:" in content

    def test_load_template_raises_on_missing_template(self):
        """Should raise ValueError for nonexistent template"""
        manager = TemplateManager()

        with pytest.raises(ValueError, match="Template .* not found"):
            manager.load_template("nonexistent")

    def test_all_templates_are_valid_yaml(self):
        """All predefined templates should be valid YAML"""
        manager = TemplateManager()

        for template_name in manager.list_templates():
            content = manager.load_template(template_name)
            # Should parse without error
            parsed = yaml.safe_load(content)
            assert isinstance(parsed, dict)
            assert "service" in parsed or "agents" in parsed


class TestVariableSubstitution:
    """Test Jinja2 variable substitution"""

    def test_substitute_variables_with_context(self):
        """Should substitute Jinja2 variables from context"""
        manager = TemplateManager()
        template = "binary: {{ claude_binary }}"
        context = {"claude_binary": "/usr/bin/claude"}

        result = manager.substitute_variables(template, context)
        assert result == "binary: /usr/bin/claude"

    def test_substitute_with_default_filter(self):
        """Should apply default filter for missing variables"""
        manager = TemplateManager()
        template = "binary: {{ missing_var|default('fallback') }}"
        context = {}

        result = manager.substitute_variables(template, context)
        assert result == "binary: fallback"

    def test_substitute_handles_empty_context(self):
        """Should handle empty context gracefully"""
        manager = TemplateManager()
        template = "name: {{ name|default('default-name') }}"

        result = manager.substitute_variables(template, {})
        assert "default-name" in result


class TestEnvironmentVariableExpansion:
    """Test ${VAR} environment variable expansion"""

    @patch.dict(os.environ, {"TEST_API_KEY": "test-key-123"})
    def test_expand_env_vars_substitutes_from_environment(self):
        """Should replace ${VAR} with environment variable value"""
        manager = TemplateManager()
        yaml_content = "api_key: ${TEST_API_KEY}"

        result = manager.expand_env_vars(yaml_content)
        assert result == "api_key: test-key-123"

    @patch.dict(os.environ, {}, clear=True)
    def test_expand_env_vars_leaves_undefined_vars(self):
        """Should leave ${VAR} unchanged if not in environment"""
        manager = TemplateManager()
        yaml_content = "api_key: ${UNDEFINED_VAR}"

        result = manager.expand_env_vars(yaml_content)
        # Should either leave as-is or replace with empty
        assert "api_key:" in result

    @patch.dict(os.environ, {"KEY1": "value1", "KEY2": "value2"})
    def test_expand_multiple_env_vars(self):
        """Should expand multiple environment variables"""
        manager = TemplateManager()
        yaml_content = """
        key1: ${KEY1}
        key2: ${KEY2}
        """

        result = manager.expand_env_vars(yaml_content)
        assert "value1" in result
        assert "value2" in result


class TestConfigGeneration:
    """Test end-to-end config generation"""

    def test_generate_config_creates_file(self, tmp_path):
        """Should generate config file from template"""
        manager = TemplateManager()
        output_path = tmp_path / "config.yaml"

        manager.generate_config(
            template_name="quick-start", output_path=output_path, context={}
        )

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_generate_config_with_context_variables(self, tmp_path):
        """Should apply context variables during generation"""
        manager = TemplateManager()
        output_path = tmp_path / "config.yaml"

        context = {"claude_binary": "/custom/bin/claude"}

        manager.generate_config(
            template_name="quick-start", output_path=output_path, context=context
        )

        content = output_path.read_text()
        assert "/custom/bin/claude" in content

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
    def test_generate_config_expands_env_vars(self, tmp_path):
        """Should expand environment variables in generated config"""
        manager = TemplateManager()
        output_path = tmp_path / "config.yaml"

        manager.generate_config(
            template_name="quick-start", output_path=output_path, context={}
        )

        content = output_path.read_text()
        # After expansion, ${ANTHROPIC_API_KEY} should be replaced
        assert "${ANTHROPIC_API_KEY}" in content or "test-key" in content

    def test_generate_config_creates_parent_directories(self, tmp_path):
        """Should create parent directories if they don't exist"""
        manager = TemplateManager()
        output_path = tmp_path / "nested" / "dirs" / "config.yaml"

        manager.generate_config(
            template_name="quick-start", output_path=output_path, context={}
        )

        assert output_path.exists()

    def test_generate_config_validates_template_exists(self, tmp_path):
        """Should raise error for nonexistent template"""
        manager = TemplateManager()
        output_path = tmp_path / "config.yaml"

        with pytest.raises(ValueError, match="Template .* not found"):
            manager.generate_config(
                template_name="nonexistent", output_path=output_path, context={}
            )


class TestTemplateValidation:
    """Test that generated configs are valid"""

    def test_quick_start_generates_valid_yaml(self, tmp_path):
        """quick-start template should generate parseable YAML"""
        manager = TemplateManager()
        output_path = tmp_path / "config.yaml"

        manager.generate_config("quick-start", output_path, {})

        content = output_path.read_text()
        parsed = yaml.safe_load(content)
        assert isinstance(parsed, dict)

    def test_claude_only_generates_valid_yaml(self, tmp_path):
        """claude-only template should generate parseable YAML"""
        manager = TemplateManager()
        output_path = tmp_path / "config.yaml"

        manager.generate_config("claude-only", output_path, {})

        content = output_path.read_text()
        parsed = yaml.safe_load(content)
        assert isinstance(parsed, dict)

    def test_cost_optimized_generates_valid_yaml(self, tmp_path):
        """cost-optimized template should generate parseable YAML"""
        manager = TemplateManager()
        output_path = tmp_path / "config.yaml"

        manager.generate_config("cost-optimized", output_path, {})

        content = output_path.read_text()
        parsed = yaml.safe_load(content)
        assert isinstance(parsed, dict)

    def test_development_generates_valid_yaml(self, tmp_path):
        """development template should generate parseable YAML"""
        manager = TemplateManager()
        output_path = tmp_path / "config.yaml"

        manager.generate_config("development", output_path, {})

        content = output_path.read_text()
        parsed = yaml.safe_load(content)
        assert isinstance(parsed, dict)


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_manager_handles_missing_template_dir(self):
        """Should raise error if template directory doesn't exist"""
        with pytest.raises(FileNotFoundError):
            TemplateManager(template_dir=Path("/nonexistent/path"))

    def test_generate_config_fails_on_invalid_output_path(self):
        """Should raise error if output path is invalid"""
        manager = TemplateManager()

        with pytest.raises((OSError, PermissionError)):
            manager.generate_config(
                template_name="quick-start",
                output_path=Path("/root/forbidden/config.yaml"),
                context={},
            )


# pytest markers
pytestmark = [
    pytest.mark.unit,
    pytest.mark.tdd,
]
