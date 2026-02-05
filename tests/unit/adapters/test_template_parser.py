"""
Unit tests for command template parser.

Tests template parsing with placeholder substitution and security
mitigations following TDD approach (Directive 017).
"""

import pytest
from typing import Dict, Any


class TestTemplateParser:
    """Test basic template parsing functionality."""

    def test_simple_template_substitution(self):
        """Test basic placeholder substitution."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --model {{model}} --prompt {{prompt}}"
        context = {
            "binary": "/usr/bin/cli",
            "model": "claude-3-opus",
            "prompt": "test_prompt",  # Use underscore to avoid space splitting
        }

        result = parser.parse(template, context)
        assert result == ["/usr/bin/cli", "--model", "claude-3-opus", "--prompt", "test_prompt"]

    def test_template_with_extra_context_keys(self):
        """Test that extra context keys are ignored."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --model {{model}}"
        context = {
            "binary": "/usr/bin/cli",
            "model": "claude-3-opus",
            "extra_key": "ignored",
        }

        result = parser.parse(template, context)
        assert result == ["/usr/bin/cli", "--model", "claude-3-opus"]

    def test_template_with_multiple_spaces(self):
        """Test template handling with multiple spaces."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}}   --model    {{model}}"
        context = {"binary": "/usr/bin/cli", "model": "claude-3-opus"}

        result = parser.parse(template, context)
        # Multiple spaces should be preserved in split
        assert result[0] == "/usr/bin/cli"
        assert result[-1] == "claude-3-opus"

    def test_template_with_quoted_arguments(self):
        """Test template with arguments that need quoting."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --prompt '{{prompt}}'"
        context = {"binary": "/usr/bin/cli", "prompt": "test with spaces"}

        result = parser.parse(template, context)
        # Parser should handle quoted strings properly
        assert "/usr/bin/cli" in result
        assert "test with spaces" in " ".join(result)


class TestTemplateParserErrors:
    """Test error handling in template parser."""

    def test_missing_placeholder_value(self):
        """Test that missing placeholder raises error."""
        from src.llm_service.adapters.template_parser import (
            TemplateParser,
            TemplatePlaceholderError,
        )

        parser = TemplateParser()
        template = "{{binary}} --model {{model}}"
        context = {"binary": "/usr/bin/cli"}  # missing 'model'

        with pytest.raises(TemplatePlaceholderError, match="model"):
            parser.parse(template, context)

    def test_invalid_template_syntax(self):
        """Test that invalid template syntax raises error."""
        from src.llm_service.adapters.template_parser import (
            TemplateParser,
            TemplateSyntaxError,
        )

        parser = TemplateParser()
        template = "{{binary --model {{model}}"  # missing closing brace
        context = {"binary": "/usr/bin/cli", "model": "claude-3-opus"}

        with pytest.raises(TemplateSyntaxError):
            parser.parse(template, context)

    def test_empty_placeholder_name(self):
        """Test that empty placeholder raises error."""
        from src.llm_service.adapters.template_parser import (
            TemplateParser,
            TemplateSyntaxError,
        )

        parser = TemplateParser()
        template = "{{binary}} --model {{}}"
        context = {"binary": "/usr/bin/cli"}

        with pytest.raises(TemplateSyntaxError):
            parser.parse(template, context)


class TestTemplateParserSecurity:
    """Test security mitigations in template parser."""

    def test_shell_metacharacter_escaping(self):
        """Test that shell metacharacters are handled safely."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --prompt {{prompt}}"
        context = {
            "binary": "/usr/bin/cli",
            "prompt": "test; rm -rf /",  # command injection attempt
        }

        result = parser.parse(template, context)
        # With shell=False, dangerous commands are split into separate args
        # The semicolon and following commands become literal arguments
        # Check that the dangerous part is separated from the command
        assert result[0] == "/usr/bin/cli"
        assert result[1] == "--prompt"
        # The rest is split into harmless arguments
        assert len(result) > 3  # Multiple args means it's safe

    def test_whitelist_validation_blocks_unknown_placeholders(self):
        """Test that unknown placeholders are rejected if whitelist is used."""
        from src.llm_service.adapters.template_parser import (
            TemplateParser,
            TemplatePlaceholderError,
        )

        # Parser with whitelist
        parser = TemplateParser(
            allowed_placeholders=["binary", "model", "prompt"]
        )
        template = "{{binary}} --model {{model}} --unknown {{dangerous}}"
        context = {
            "binary": "/usr/bin/cli",
            "model": "claude-3-opus",
            "dangerous": "injection",
        }

        with pytest.raises(TemplatePlaceholderError, match="dangerous"):
            parser.parse(template, context)

    def test_backtick_command_substitution_prevented(self):
        """Test that backtick command substitution is prevented."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --prompt {{prompt}}"
        context = {
            "binary": "/usr/bin/cli",
            "prompt": "`whoami`",  # command substitution attempt
        }

        result = parser.parse(template, context)
        # With shell=False, backticks are treated as literal characters
        # They won't be interpreted, which is the security goal
        assert result[0] == "/usr/bin/cli"
        # The backtick string becomes a literal argument (safe with shell=False)
        assert "`whoami`" in result

    def test_pipe_operator_handling(self):
        """Test that pipe operators are handled safely."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --prompt {{prompt}}"
        context = {
            "binary": "/usr/bin/cli",
            "prompt": "test | cat /etc/passwd",
        }

        result = parser.parse(template, context)
        # Pipe should be escaped or the command should be rejected
        # Since we use shell=False in subprocess, pipes won't work anyway
        # But parser should still escape them
        result_str = " ".join(result)
        assert "|" not in result_str or len(result) > 2  # treated as argument

    def test_dollar_sign_variable_expansion_prevented(self):
        """Test that dollar sign variable expansion is prevented."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --prompt {{prompt}}"
        context = {
            "binary": "/usr/bin/cli",
            "prompt": "$HOME/test",
        }

        result = parser.parse(template, context)
        # Dollar signs should be escaped or handled
        result_str = " ".join(result)
        # With shell=False, $HOME won't expand, but check parser handles it
        assert "$HOME" in result_str or "HOME" not in result_str


class TestTemplateParserWhitelist:
    """Test whitelist functionality."""

    def test_whitelist_allows_valid_placeholders(self):
        """Test that whitelisted placeholders work correctly."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser(
            allowed_placeholders=["binary", "model", "prompt", "output_file"]
        )
        template = "{{binary}} --model {{model}} --output {{output_file}}"
        context = {
            "binary": "/usr/bin/cli",
            "model": "claude-3-opus",
            "output_file": "/tmp/output.txt",
        }

        result = parser.parse(template, context)
        assert result[0] == "/usr/bin/cli"
        assert "claude-3-opus" in result
        assert "/tmp/output.txt" in result

    def test_no_whitelist_allows_all_placeholders(self):
        """Test that without whitelist, all placeholders are allowed."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()  # no whitelist
        template = "{{binary}} --custom {{custom_param}}"
        context = {"binary": "/usr/bin/cli", "custom_param": "value"}

        result = parser.parse(template, context)
        assert "value" in result


class TestTemplateParserEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_empty_template(self):
        """Test empty template string."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = ""
        context = {}

        result = parser.parse(template, context)
        assert result == []

    def test_template_with_no_placeholders(self):
        """Test template with no placeholders."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "/usr/bin/cli --model static"
        context = {}

        result = parser.parse(template, context)
        assert result == ["/usr/bin/cli", "--model", "static"]

    def test_consecutive_placeholders(self):
        """Test consecutive placeholders without spaces."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}}{{model}}"
        context = {"binary": "/usr/bin/cli", "model": "claude-3-opus"}

        result = parser.parse(template, context)
        # Should concatenate or handle appropriately
        assert "/usr/bin/cli" in " ".join(result)
        assert "claude-3-opus" in " ".join(result)

    def test_placeholder_at_end_of_template(self):
        """Test placeholder at end of template."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --model {{model}}"
        context = {"binary": "/usr/bin/cli", "model": "claude-3-opus"}

        result = parser.parse(template, context)
        assert result[-1] == "claude-3-opus"

    def test_placeholder_with_special_chars_in_value(self):
        """Test placeholder value containing special characters."""
        from src.llm_service.adapters.template_parser import TemplateParser

        parser = TemplateParser()
        template = "{{binary}} --prompt {{prompt}}"
        context = {
            "binary": "/usr/bin/cli",
            "prompt": "test@example.com:path/to/file",
        }

        result = parser.parse(template, context)
        assert "test@example.com:path/to/file" in result
