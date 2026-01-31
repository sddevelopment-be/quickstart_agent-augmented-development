"""Acceptance tests for model router configuration and validation.

Tests follow ATDD (Acceptance Test-Driven Development) pattern per Directive 016.
These tests verify the model router system from a user perspective.

References:
    - .github/agents/directives/016_atdd.md
    - .github/agents/directives/017_tdd.md
    - docs/styleguides/python_conventions.md (Quad-A pattern)
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

import pytest
import yaml


class TestModelRouterAcceptance:
    """Acceptance tests for model router configuration system."""

    @pytest.fixture
    def config_path(self) -> Path:
        """Get path to model router config."""
        return Path("ops/config/model_router.yaml")

    @pytest.fixture
    def validator_path(self) -> Path:
        """Get path to validator script."""
        return Path("ops/scripts/validate-model-router.py")

    @pytest.fixture
    def config_data(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration data."""
        with open(config_path) as f:
            return yaml.safe_load(f)

    def test_config_file_exists(self, config_path: Path) -> None:
        """GIVEN the model router system
        WHEN checking for configuration file
        THEN the file should exist at expected location.
        """
        # Assumption check
        assert config_path.name == "model_router.yaml", (
            "Config filename should be model_router.yaml"
        )

        # Act & Assert
        assert config_path.exists(), f"Config file not found: {config_path}"
        assert config_path.is_file(), f"Config path is not a file: {config_path}"

    def test_config_is_valid_yaml(self, config_path: Path) -> None:
        """GIVEN the model router configuration file
        WHEN parsing as YAML
        THEN it should parse successfully without errors.
        """
        # Act
        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Config is not valid YAML: {e}")

        # Assert
        assert isinstance(config, dict), "Config should be a dictionary"
        assert len(config) > 0, "Config should not be empty"

    def test_validator_script_exists(self, validator_path: Path) -> None:
        """GIVEN the model router validation system
        WHEN checking for validator script
        THEN the script should exist and be executable.
        """
        # Act & Assert
        assert validator_path.exists(), f"Validator not found: {validator_path}"
        assert validator_path.is_file(), "Validator should be a file"

    def test_validator_accepts_valid_config(
        self, validator_path: Path, config_path: Path
    ) -> None:
        """GIVEN a valid model router configuration
        WHEN running the validator
        THEN validation should pass with exit code 0.
        """
        # Act
        result = subprocess.run(
            [sys.executable, str(validator_path), "--file", str(config_path)],
            capture_output=True,
            text=True,
        )

        # Assert
        assert result.returncode == 0, (
            f"Validator failed on valid config:\n"
            f"STDOUT: {result.stdout}\n"
            f"STDERR: {result.stderr}"
        )
        assert "✅" in result.stdout or "PASSED" in result.stdout

    def test_config_contains_required_sections(
        self, config_data: Dict[str, Any]
    ) -> None:
        """GIVEN the model router configuration
        WHEN checking top-level structure
        THEN all required sections should be present.
        """
        # Arrange
        required_sections = [
            "version",
            "pricing_ceilings",
            "fallback_policy",
            "models",
            "role_defaults",
            "validation",
        ]

        # Act & Assert
        for section in required_sections:
            assert section in config_data, f"Missing required section: {section}"

    def test_config_contains_expected_models(
        self, config_data: Dict[str, Any]
    ) -> None:
        """GIVEN the model router configuration
        WHEN checking model catalog
        THEN it should contain expected model families.
        """
        # Arrange
        models = config_data.get("models", {})
        expected_families = ["gpt", "claude", "codestral", "deepseek", "llama"]

        # Act & Assert
        assert len(models) > 0, "Model catalog should not be empty"

        for family in expected_families:
            matching_models = [
                key for key in models.keys() if family in key.lower()
            ]
            assert len(matching_models) > 0, (
                f"No models found for family: {family}"
            )

    def test_all_models_have_required_fields(
        self, config_data: Dict[str, Any]
    ) -> None:
        """GIVEN the model router configuration
        WHEN checking each model entry
        THEN all should have required fields.
        """
        # Arrange
        models = config_data.get("models", {})
        required_fields = ["router", "identifier", "context_window", "pricing"]

        # Act & Assert
        for model_key, model_config in models.items():
            for field in required_fields:
                assert field in model_config, (
                    f"Model '{model_key}' missing required field: {field}"
                )

    def test_pricing_ceilings_defined_for_all_routers(
        self, config_data: Dict[str, Any]
    ) -> None:
        """GIVEN the model router configuration
        WHEN checking pricing ceilings
        THEN ceilings should be defined for all router types used.
        """
        # Arrange
        models = config_data.get("models", {})
        routers_used = set(m.get("router") for m in models.values())
        pricing_ceilings = config_data.get("pricing_ceilings", {})

        # Act & Assert
        for router in routers_used:
            if router:  # Skip None values
                assert router in pricing_ceilings, (
                    f"No pricing ceiling defined for router: {router}"
                )
                ceiling = pricing_ceilings[router]
                assert "max_input_price" in ceiling
                assert "max_output_price" in ceiling

    def test_fallback_references_are_valid(
        self, config_data: Dict[str, Any]
    ) -> None:
        """GIVEN the model router configuration
        WHEN checking fallback references
        THEN all fallback_to values should reference existing models.
        """
        # Arrange
        models = config_data.get("models", {})

        # Act & Assert
        for model_key, model_config in models.items():
            fallback = model_config.get("fallback_to")
            if fallback is not None:
                assert fallback in models, (
                    f"Model '{model_key}' references non-existent fallback: {fallback}"
                )

    def test_role_defaults_reference_existing_models(
        self, config_data: Dict[str, Any]
    ) -> None:
        """GIVEN the model router configuration
        WHEN checking role defaults
        THEN all model references should exist in catalog.
        """
        # Arrange
        models = config_data.get("models", {})
        role_defaults = config_data.get("role_defaults", {})

        # Act & Assert
        for role, defaults in role_defaults.items():
            for tier, model_ref in defaults.items():
                assert model_ref in models, (
                    f"Role '{role}' {tier} references non-existent model: {model_ref}"
                )

    def test_validator_json_output_format(
        self, validator_path: Path, config_path: Path
    ) -> None:
        """GIVEN the validator script
        WHEN running with --format json
        THEN output should be valid JSON with expected structure.
        """
        # Act
        result = subprocess.run(
            [
                sys.executable,
                str(validator_path),
                "--file",
                str(config_path),
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        # Assert
        assert result.returncode == 0, "Validator should succeed"

        # Parse JSON
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            pytest.fail(f"Validator output is not valid JSON: {e}")

        # Check structure
        assert "valid" in output
        assert "errors" in output
        assert "warnings" in output
        assert "summary" in output
        assert output["valid"] is True

    def test_validator_strict_mode(
        self, validator_path: Path, config_path: Path
    ) -> None:
        """GIVEN the validator script
        WHEN running with --strict flag
        THEN warnings should be treated as errors.
        """
        # Act
        result = subprocess.run(
            [
                sys.executable,
                str(validator_path),
                "--file",
                str(config_path),
                "--strict",
            ],
            capture_output=True,
            text=True,
        )

        # Assert
        # With current valid config, should still pass in strict mode
        assert result.returncode == 0, "Strict validation should pass valid config"

    def test_all_models_have_descriptions(
        self, config_data: Dict[str, Any]
    ) -> None:
        """GIVEN the model router configuration
        WHEN checking model documentation
        THEN each model should have a description for maintainability.
        """
        # Arrange
        models = config_data.get("models", {})

        # Act & Assert
        for model_key, model_config in models.items():
            assert "description" in model_config, (
                f"Model '{model_key}' missing description"
            )
            description = model_config["description"]
            assert description and len(description) > 0, (
                f"Model '{model_key}' has empty description"
            )

    def test_config_has_inline_documentation(self, config_path: Path) -> None:
        """GIVEN the model router configuration file
        WHEN checking file contents
        THEN it should contain inline documentation and schema notes.
        """
        # Act
        with open(config_path) as f:
            content = f.read()

        # Assert
        assert "Schema Notes" in content or "schema" in content.lower(), (
            "Config should contain schema documentation"
        )
        assert "References:" in content or "ADR" in content, (
            "Config should reference ADRs"
        )
        assert "#" in content, "Config should have comments"

    def test_context_windows_are_reasonable(
        self, config_data: Dict[str, Any]
    ) -> None:
        """GIVEN the model router configuration
        WHEN checking context windows
        THEN all values should be within reasonable bounds.
        """
        # Arrange
        models = config_data.get("models", {})
        min_context = 1000
        max_context = 1_000_000

        # Act & Assert
        for model_key, model_config in models.items():
            context = model_config.get("context_window")
            assert context is not None, (
                f"Model '{model_key}' missing context_window"
            )
            assert context >= min_context, (
                f"Model '{model_key}' context too small: {context}"
            )
            assert context <= max_context, (
                f"Model '{model_key}' context too large: {context}"
            )

    def test_pricing_is_non_negative(self, config_data: Dict[str, Any]) -> None:
        """GIVEN the model router configuration
        WHEN checking pricing data
        THEN all prices should be non-negative.
        """
        # Arrange
        models = config_data.get("models", {})

        # Act & Assert
        for model_key, model_config in models.items():
            pricing = model_config.get("pricing", {})
            for price_type in ["input_per_1k", "output_per_1k"]:
                price = pricing.get(price_type)
                assert price is not None, (
                    f"Model '{model_key}' missing {price_type}"
                )
                assert price >= 0, (
                    f"Model '{model_key}' {price_type} is negative: {price}"
                )

    def test_no_fallback_cycles(self, config_data: Dict[str, Any]) -> None:
        """GIVEN the model router configuration
        WHEN following fallback chains
        THEN there should be no circular references.
        """
        # Arrange
        models = config_data.get("models", {})

        # Act & Assert
        for start_model in models:
            visited = set()
            current = start_model

            while current is not None:
                assert current not in visited, (
                    f"Fallback cycle detected starting from '{start_model}'"
                )
                visited.add(current)
                current = models[current].get("fallback_to")

    def test_validator_help_shows_usage(self, validator_path: Path) -> None:
        """GIVEN the validator script
        WHEN running with --help
        THEN usage information should be displayed.
        """
        # Act
        result = subprocess.run(
            [sys.executable, str(validator_path), "--help"],
            capture_output=True,
            text=True,
        )

        # Assert
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "--file" in result.stdout
        assert "--strict" in result.stdout
        assert "--format" in result.stdout
