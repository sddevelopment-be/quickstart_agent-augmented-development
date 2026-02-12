"""
Unit tests for output normalization framework.

Tests output normalization for different tool formats (JSON, plain text)
following TDD approach (Directive 017).
"""

import json


class TestNormalizedResponse:
    """Test NormalizedResponse dataclass."""

    def test_normalized_response_creation(self):
        """Test creating NormalizedResponse with all fields."""
        from src.llm_service.adapters.output_normalizer import NormalizedResponse

        response = NormalizedResponse(
            response_text="Generated output",
            metadata={"tokens": 150, "model": "claude-3-opus", "cost_usd": 0.05},
            errors=[],
            warnings=["API rate limit approaching"],
            raw_output="Raw JSON output",
        )

        assert response.response_text == "Generated output"
        assert response.metadata["tokens"] == 150
        assert response.metadata["cost_usd"] == 0.05
        assert response.errors == []
        assert len(response.warnings) == 1
        assert response.raw_output == "Raw JSON output"

    def test_normalized_response_is_dataclass(self):
        """Test that NormalizedResponse is a proper dataclass."""
        from dataclasses import is_dataclass

        from src.llm_service.adapters.output_normalizer import NormalizedResponse

        assert is_dataclass(NormalizedResponse)


class TestOutputNormalizer:
    """Test basic output normalization."""

    def test_normalize_json_output(self):
        """Test normalizing JSON structured output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps(
            {
                "response": "Generated text",
                "metadata": {"tokens": 100, "model": "claude-3-opus"},
            }
        )

        result = normalizer.normalize(json_output, format="json")

        assert result.response_text == "Generated text"
        assert result.metadata["tokens"] == 100
        assert result.metadata["model"] == "claude-3-opus"

    def test_normalize_plain_text_output(self):
        """Test normalizing plain text output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        text_output = "This is plain text output from the tool"

        result = normalizer.normalize(text_output, format="text")

        assert result.response_text == "This is plain text output from the tool"
        assert result.metadata == {}

    def test_normalize_auto_detect_json(self):
        """Test auto-detection of JSON format."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = '{"response": "Auto-detected JSON"}'

        result = normalizer.normalize(json_output)  # No format specified

        assert result.response_text == "Auto-detected JSON"

    def test_normalize_auto_detect_text(self):
        """Test auto-detection of plain text format."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        text_output = "Plain text without JSON structure"

        result = normalizer.normalize(text_output)  # No format specified

        assert result.response_text == "Plain text without JSON structure"


class TestOutputNormalizerMetadata:
    """Test metadata extraction from different formats."""

    def test_extract_token_count_from_json(self):
        """Test extracting token count from JSON output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps({"response": "Text", "usage": {"total_tokens": 250}})

        result = normalizer.normalize(json_output, format="json")

        assert result.metadata.get("tokens") == 250

    def test_extract_cost_from_json(self):
        """Test extracting cost from JSON output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps({"response": "Text", "cost": {"total_usd": 0.15}})

        result = normalizer.normalize(json_output, format="json")

        assert result.metadata.get("cost_usd") == 0.15

    def test_extract_model_from_json(self):
        """Test extracting model identifier from JSON output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps(
            {"response": "Text", "model": "claude-3-opus-20240229"}
        )

        result = normalizer.normalize(json_output, format="json")

        assert result.metadata.get("model") == "claude-3-opus-20240229"

    def test_extract_multiple_metadata_fields(self):
        """Test extracting multiple metadata fields."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps(
            {
                "response": "Generated text",
                "model": "gpt-4",
                "usage": {
                    "prompt_tokens": 50,
                    "completion_tokens": 100,
                    "total_tokens": 150,
                },
                "finish_reason": "stop",
            }
        )

        result = normalizer.normalize(json_output, format="json")

        assert result.metadata["model"] == "gpt-4"
        assert result.metadata["tokens"] == 150
        assert result.metadata["finish_reason"] == "stop"


class TestOutputNormalizerErrors:
    """Test error handling in output normalizer."""

    def test_normalize_invalid_json(self):
        """Test handling of invalid JSON."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        invalid_json = '{"response": "incomplete'

        result = normalizer.normalize(invalid_json, format="json")

        # Should fall back to treating as text
        assert result.response_text == invalid_json
        assert len(result.errors) > 0
        assert "JSON" in result.errors[0] or "parse" in result.errors[0].lower()

    def test_normalize_empty_output(self):
        """Test handling of empty output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        result = normalizer.normalize("", format="text")

        assert result.response_text == ""
        assert result.metadata == {}

    def test_identify_error_in_output(self):
        """Test identification of errors in tool output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps({"response": "", "error": "API key invalid"})

        result = normalizer.normalize(json_output, format="json")

        assert len(result.errors) > 0
        assert "API key invalid" in result.errors

    def test_identify_warning_in_output(self):
        """Test identification of warnings in tool output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps(
            {"response": "Text", "warning": "Context length near limit"}
        )

        result = normalizer.normalize(json_output, format="json")

        assert len(result.warnings) > 0
        assert "Context length near limit" in result.warnings


class TestOutputNormalizerFormats:
    """Test different output format support."""

    def test_normalize_json_with_nested_response(self):
        """Test JSON with nested response field."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps({"data": {"response": {"text": "Nested text"}}})

        result = normalizer.normalize(json_output, format="json")

        assert "Nested text" in result.response_text

    def test_normalize_json_with_multiple_response_keys(self):
        """Test JSON with multiple possible response keys."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        # Different tools use different keys: 'output', 'text', 'content', etc.
        json_output = json.dumps({"output": "Tool output text"})

        result = normalizer.normalize(json_output, format="json")

        assert result.response_text == "Tool output text"

    def test_normalize_mixed_format(self):
        """Test mixed format with text and metadata."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        # Some tools output text followed by metadata
        mixed_output = "Generated response\n---\nTokens: 100\nModel: claude-3"

        result = normalizer.normalize(mixed_output, format="text")

        assert "Generated response" in result.response_text


class TestOutputNormalizerExtensibility:
    """Test extensibility for tool-specific normalizers."""

    def test_register_custom_format_handler(self):
        """Test registering custom format handler for tool-specific formats."""
        from src.llm_service.adapters.output_normalizer import (
            NormalizedResponse,
            OutputNormalizer,
        )

        def custom_handler(output: str) -> NormalizedResponse:
            # Custom parsing logic
            return NormalizedResponse(
                response_text=f"Custom: {output}",
                metadata={"custom": True},
                errors=[],
                warnings=[],
                raw_output=output,
            )

        normalizer = OutputNormalizer()
        normalizer.register_format_handler("custom", custom_handler)

        result = normalizer.normalize("test", format="custom")

        assert result.response_text == "Custom: test"
        assert result.metadata["custom"] is True

    def test_tool_specific_normalizer(self):
        """Test creating tool-specific normalizer subclass."""
        from src.llm_service.adapters.output_normalizer import (
            NormalizedResponse,
            OutputNormalizer,
        )

        class ClaudeCodeNormalizer(OutputNormalizer):
            """Tool-specific normalizer for claude-code output."""

            def normalize(
                self, output: str, format: str | None = None
            ) -> NormalizedResponse:
                # Claude-code specific parsing
                result = super().normalize(output, format)
                result.metadata["tool"] = "claude-code"
                return result

        normalizer = ClaudeCodeNormalizer()
        result = normalizer.normalize("test output", format="text")

        assert result.metadata["tool"] == "claude-code"


class TestOutputNormalizerEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_normalize_very_large_output(self):
        """Test handling of very large output."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        large_output = "x" * 1000000  # 1MB of text

        result = normalizer.normalize(large_output, format="text")

        assert len(result.response_text) == 1000000

    def test_normalize_unicode_output(self):
        """Test handling of Unicode characters."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        unicode_output = "Hello 世界 🌍 Привет"

        result = normalizer.normalize(unicode_output, format="text")

        assert result.response_text == unicode_output

    def test_normalize_json_with_null_values(self):
        """Test JSON with null values."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        json_output = json.dumps({"response": "Text", "metadata": None, "cost": None})

        result = normalizer.normalize(json_output, format="json")

        assert result.response_text == "Text"

    def test_normalize_preserves_raw_output(self):
        """Test that raw output is preserved in result."""
        from src.llm_service.adapters.output_normalizer import OutputNormalizer

        normalizer = OutputNormalizer()
        original = '{"response": "test"}'

        result = normalizer.normalize(original, format="json")

        assert result.raw_output == original
