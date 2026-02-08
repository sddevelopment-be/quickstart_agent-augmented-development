"""Unit tests for model router validator.

Tests follow TDD (Test-Driven Development) pattern per Directive 017.
These tests verify individual validator components in isolation.

References:
    - .github/agents/directives/017_tdd.md
    - .github/agents/directives/016_atdd.md
    - docs/styleguides/python_conventions.md (Quad-A pattern)
"""

import importlib.util
from pathlib import Path
from typing import Any, Dict

import pytest

# Import validator by loading as module
import importlib.util

_validator_path = Path(__file__).parent.parent.parent / "ops" / "scripts" / "validate-model-router.py"
_spec = importlib.util.spec_from_file_location("validate_model_router", _validator_path)
_validator_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validator_module)

ModelRouterValidator = _validator_module.ModelRouterValidator
ValidationResult = _validator_module.ValidationResult
load_config = _validator_module.load_config


class TestValidationResult:
    """Unit tests for ValidationResult class."""

    def test_init_creates_empty_lists(self) -> None:
        """Test ValidationResult initializes with empty lists."""
        # Arrange & Act
        result = ValidationResult()

        # Assert
        assert result.errors == []
        assert result.warnings == []
        assert result.info == []

    def test_add_error_appends_to_list(self) -> None:
        """Test adding error message."""
        # Arrange
        result = ValidationResult()

        # Act
        result.add_error("Test error")

        # Assert
        assert len(result.errors) == 1
        assert result.errors[0] == "Test error"

    def test_add_warning_appends_to_list(self) -> None:
        """Test adding warning message."""
        # Arrange
        result = ValidationResult()

        # Act
        result.add_warning("Test warning")

        # Assert
        assert len(result.warnings) == 1
        assert result.warnings[0] == "Test warning"

    def test_add_info_appends_to_list(self) -> None:
        """Test adding info message."""
        # Arrange
        result = ValidationResult()

        # Act
        result.add_info("Test info")

        # Assert
        assert len(result.info) == 1
        assert result.info[0] == "Test info"

    def test_is_valid_returns_true_when_no_errors(self) -> None:
        """Test is_valid returns True when no errors."""
        # Arrange
        result = ValidationResult()
        result.add_info("Info message")

        # Act
        is_valid = result.is_valid()

        # Assert
        assert is_valid is True

    def test_is_valid_returns_false_when_errors_exist(self) -> None:
        """Test is_valid returns False when errors exist."""
        # Arrange
        result = ValidationResult()
        result.add_error("Error message")

        # Act
        is_valid = result.is_valid()

        # Assert
        assert is_valid is False

    def test_is_valid_strict_mode_treats_warnings_as_errors(self) -> None:
        """Test is_valid in strict mode treats warnings as errors."""
        # Arrange
        result = ValidationResult()
        result.add_warning("Warning message")

        # Act
        is_valid_normal = result.is_valid(strict=False)
        is_valid_strict = result.is_valid(strict=True)

        # Assert
        assert is_valid_normal is True
        assert is_valid_strict is False

    def test_to_dict_returns_expected_structure(self) -> None:
        """Test to_dict returns proper dictionary structure."""
        # Arrange
        result = ValidationResult()
        result.add_error("Error 1")
        result.add_warning("Warning 1")
        result.add_info("Info 1")

        # Act
        dict_result = result.to_dict()

        # Assert
        assert isinstance(dict_result, dict)
        assert "valid" in dict_result
        assert "errors" in dict_result
        assert "warnings" in dict_result
        assert "info" in dict_result
        assert "summary" in dict_result
        assert dict_result["summary"]["error_count"] == 1
        assert dict_result["summary"]["warning_count"] == 1
        assert dict_result["summary"]["info_count"] == 1


class TestModelRouterValidator:
    """Unit tests for ModelRouterValidator class."""

    @pytest.fixture
    def minimal_valid_config(self) -> Dict[str, Any]:
        """Minimal valid configuration for testing."""
        return {
            "version": "1.0.0",
            "pricing_ceilings": {
                "openrouter": {
                    "max_input_price": 10.0,
                    "max_output_price": 50.0,
                    "daily_budget": 100.0,
                }
            },
            "fallback_policy": {
                "priority_order": [
                    {"router": "openrouter", "priority": 1}
                ],
                "max_retries": 3,
            },
            "models": {
                "test-model": {
                    "router": "openrouter",
                    "identifier": "test/model",
                    "context_window": 8000,
                    "pricing": {
                        "input_per_1k": 0.5,
                        "output_per_1k": 1.5,
                    },
                    "default_role": "general",
                }
            },
            "validation": {
                "required_fields": [
                    "router",
                    "identifier",
                    "context_window",
                    "pricing",
                    "default_role",
                ],
                "allowed_routers": ["openrouter", "opencode_ai", "direct_api"],
                "allowed_roles": ["analysis", "creative", "coding", "general"],
            },
        }

    def test_validator_init_sets_config(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator initialization sets config."""
        # Arrange & Act
        validator = ModelRouterValidator(minimal_valid_config)

        # Assert
        assert validator.config == minimal_valid_config
        assert validator.strict is False
        assert isinstance(validator.result, ValidationResult)

    def test_validator_init_respects_strict_flag(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator initialization respects strict flag."""
        # Arrange & Act
        validator = ModelRouterValidator(minimal_valid_config, strict=True)

        # Assert
        assert validator.strict is True

    def test_validate_minimal_config_passes(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validation passes for minimal valid config."""
        # Arrange
        validator = ModelRouterValidator(minimal_valid_config)

        # Act
        result = validator.validate()

        # Assert
        assert result.is_valid()
        assert len(result.errors) == 0

    def test_validate_detects_missing_version(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects missing version."""
        # Arrange
        config = minimal_valid_config.copy()
        del config["version"]
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("version" in error.lower() for error in result.errors)

    def test_validate_detects_missing_models_section(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects missing models section."""
        # Arrange
        config = minimal_valid_config.copy()
        del config["models"]
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("models" in error.lower() for error in result.errors)

    def test_validate_detects_invalid_router(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects invalid router type."""
        # Arrange
        config = minimal_valid_config.copy()
        config["models"]["test-model"]["router"] = "invalid_router"
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("invalid router" in error.lower() for error in result.errors)

    def test_validate_detects_missing_required_model_field(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects missing required field in model."""
        # Arrange
        config = minimal_valid_config.copy()
        del config["models"]["test-model"]["identifier"]
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any(
            "identifier" in error.lower() and "missing" in error.lower()
            for error in result.errors
        )

    def test_validate_detects_context_window_too_small(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects context window below minimum."""
        # Arrange
        config = minimal_valid_config.copy()
        config["models"]["test-model"]["context_window"] = 100  # Too small
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("context_window" in error.lower() for error in result.errors)

    def test_validate_detects_negative_pricing(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects negative pricing."""
        # Arrange
        config = minimal_valid_config.copy()
        config["models"]["test-model"]["pricing"]["input_per_1k"] = -1.0
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("negative" in error.lower() for error in result.errors)

    def test_validate_detects_pricing_ceiling_violation(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects pricing exceeding ceiling."""
        # Arrange
        config = minimal_valid_config.copy()
        config["models"]["test-model"]["pricing"]["input_per_1k"] = 20.0  # Exceeds 10.0 ceiling
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("exceeds ceiling" in error.lower() for error in result.errors)

    def test_validate_detects_invalid_fallback_reference(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects fallback to non-existent model."""
        # Arrange
        config = minimal_valid_config.copy()
        config["models"]["test-model"]["fallback_to"] = "non-existent-model"
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any(
            "fallback" in error.lower() and "does not exist" in error.lower()
            for error in result.errors
        )

    def test_validate_detects_fallback_cycle(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects circular fallback references."""
        # Arrange
        config = minimal_valid_config.copy()
        config["models"]["model-a"] = config["models"]["test-model"].copy()
        config["models"]["model-b"] = config["models"]["test-model"].copy()
        config["models"]["model-a"]["fallback_to"] = "model-b"
        config["models"]["model-b"]["fallback_to"] = "model-a"
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("cycle" in error.lower() for error in result.errors)

    def test_validate_detects_duplicate_priority(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator detects duplicate priority values."""
        # Arrange
        config = minimal_valid_config.copy()
        config["fallback_policy"]["priority_order"] = [
            {"router": "openrouter", "priority": 1},
            {"router": "opencode_ai", "priority": 1},  # Duplicate priority
        ]
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("duplicate priority" in error.lower() for error in result.errors)

    def test_validate_warns_on_large_context_window(
        self, minimal_valid_config: Dict[str, Any]
    ) -> None:
        """Test validator warns on unusually large context window."""
        # Arrange
        config = minimal_valid_config.copy()
        config["models"]["test-model"]["context_window"] = 1_500_000  # Above 1M threshold
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert len(result.warnings) > 0
        assert any("context_window" in warning.lower() for warning in result.warnings)


class TestLoadConfig:
    """Unit tests for load_config function."""

    def test_load_config_returns_none_for_missing_file(self, tmp_path: Path) -> None:
        """Test load_config returns None for non-existent file."""
        # Arrange
        missing_file = tmp_path / "nonexistent.yaml"

        # Assumption check
        assert not missing_file.exists()

        # Act
        result = load_config(missing_file)

        # Assert
        assert result is None

    def test_load_config_returns_dict_for_valid_yaml(self, tmp_path: Path) -> None:
        """Test load_config returns dict for valid YAML."""
        # Arrange
        config_file = tmp_path / "config.yaml"
        config_file.write_text("key: value\nlist:\n  - item1\n  - item2\n")

        # Act
        result = load_config(config_file)

        # Assert
        assert result is not None
        assert isinstance(result, dict)
        assert result["key"] == "value"
        assert result["list"] == ["item1", "item2"]

    def test_load_config_returns_none_for_invalid_yaml(
        self, tmp_path: Path
    ) -> None:
        """Test load_config returns None for invalid YAML."""
        # Arrange
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("invalid: yaml: structure: bad\n  - no list")

        # Act
        result = load_config(config_file)

        # Assert
        assert result is None


class TestEdgeCases:
    """Unit tests for edge cases and error conditions."""

    def test_validator_handles_empty_config(self) -> None:
        """Test validator handles empty configuration."""
        # Arrange
        config: Dict[str, Any] = {}
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert len(result.errors) > 0

    def test_validator_handles_none_fallback(self) -> None:
        """Test validator handles null fallback_to value."""
        # Arrange
        config = {
            "version": "1.0.0",
            "pricing_ceilings": {},
            "fallback_policy": {},
            "models": {
                "model-a": {
                    "router": "openrouter",
                    "identifier": "test/model",
                    "context_window": 8000,
                    "pricing": {"input_per_1k": 0.5, "output_per_1k": 1.5},
                    "default_role": "general",
                    "fallback_to": None,  # Explicit null
                }
            },
            "validation": {
                "required_fields": ["router", "identifier"],
                "allowed_routers": ["openrouter"],
                "allowed_roles": ["general"],
            },
        }
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        # Should not error on null fallback
        assert not any("fallback" in error.lower() for error in result.errors)

    def test_validator_handles_missing_pricing_fields(self) -> None:
        """Test validator detects missing pricing subfields."""
        # Arrange
        config = {
            "version": "1.0.0",
            "pricing_ceilings": {},
            "fallback_policy": {},
            "models": {
                "test-model": {
                    "router": "openrouter",
                    "identifier": "test/model",
                    "context_window": 8000,
                    "pricing": {},  # Missing input_per_1k and output_per_1k
                    "default_role": "general",
                }
            },
            "validation": {
                "required_fields": ["router", "identifier"],
                "allowed_routers": ["openrouter"],
                "allowed_roles": ["general"],
            },
        }
        validator = ModelRouterValidator(config)

        # Act
        result = validator.validate()

        # Assert
        assert not result.is_valid()
        assert any("pricing" in error.lower() for error in result.errors)
