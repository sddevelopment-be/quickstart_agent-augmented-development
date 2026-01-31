#!/usr/bin/env python3
"""Model Router Configuration Validator.

Validates the model router configuration YAML file to ensure:
- Schema compliance (required fields, valid types)
- Fallback references exist and don't create cycles
- Context windows are reasonable (> 0, < 1M tokens)
- Pricing is within defined ceilings per router
- Role defaults reference valid models
- Capability definitions are allowed

Usage:
    # Validate with default config location
    python validate-model-router.py

    # Validate specific file
    python validate-model-router.py --file ops/config/model_router.yaml

    # Strict mode (warnings become errors)
    python validate-model-router.py --strict

    # JSON output for CI integration
    python validate-model-router.py --format json

Exit Codes:
    0: Validation passed
    1: Validation failed (errors found)
    2: File not found or invalid YAML
    3: Invalid arguments

References:
    - docs/architecture/adrs/ADR-021-model-routing-strategy.md
    - docs/architecture/assessments/platform_next_steps.md

Author: DevOps Danny
Created: 2025-11-30
Version: 1.0.0
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


class ValidationResult:
    """Container for validation results."""

    def __init__(self) -> None:
        """Initialize validation result."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        """Add an info message."""
        self.info.append(message)

    def is_valid(self, strict: bool = False) -> bool:
        """Check if validation passed.

        Args:
            strict: If True, warnings are treated as errors.

        Returns:
            True if validation passed, False otherwise.
        """
        if self.errors:
            return False
        if strict and self.warnings:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output."""
        return {
            "valid": self.is_valid(),
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
            "summary": {
                "error_count": len(self.errors),
                "warning_count": len(self.warnings),
                "info_count": len(self.info),
            },
        }


class ModelRouterValidator:
    """Validates model router configuration."""

    # Constants for validation
    MIN_CONTEXT_WINDOW = 1000
    MAX_CONTEXT_WINDOW = 1_000_000
    MAX_REASONABLE_PRICE = 1000.0  # USD per 1K tokens

    def __init__(self, config: Dict[str, Any], strict: bool = False) -> None:
        """Initialize validator.

        Args:
            config: Parsed YAML configuration.
            strict: If True, warnings are treated as errors.
        """
        self.config = config
        self.strict = strict
        self.result = ValidationResult()

    def validate(self) -> ValidationResult:
        """Run all validation checks.

        Returns:
            ValidationResult with all findings.
        """
        # Check top-level structure
        self._validate_top_level_structure()

        # Validate pricing ceilings
        if "pricing_ceilings" in self.config:
            self._validate_pricing_ceilings()

        # Validate fallback policy
        if "fallback_policy" in self.config:
            self._validate_fallback_policy()

        # Validate model catalog
        if "models" in self.config:
            self._validate_model_catalog()
            self._validate_fallback_references()

        # Validate role defaults
        if "role_defaults" in self.config:
            self._validate_role_defaults()

        # Validate validation rules (meta!)
        if "validation" in self.config:
            self._validate_validation_rules()

        # Summary
        self.result.add_info(
            f"Validated {len(self.config.get('models', {}))} model(s)"
        )

        return self.result

    def _validate_top_level_structure(self) -> None:
        """Validate top-level configuration structure."""
        required_sections = [
            "version",
            "pricing_ceilings",
            "fallback_policy",
            "models",
        ]

        for section in required_sections:
            if section not in self.config:
                self.result.add_error(
                    f"Missing required top-level section: {section}"
                )

        # Check version format
        if "version" in self.config:
            version = self.config["version"]
            if not isinstance(version, str):
                self.result.add_error(
                    f"Version must be a string, got {type(version).__name__}"
                )
            elif not version.count(".") == 2:
                self.result.add_warning(
                    f"Version '{version}' doesn't follow semver format (x.y.z)"
                )

    def _validate_pricing_ceilings(self) -> None:
        """Validate pricing ceilings configuration."""
        ceilings = self.config["pricing_ceilings"]

        if not isinstance(ceilings, dict):
            self.result.add_error(
                f"pricing_ceilings must be a dict, got {type(ceilings).__name__}"
            )
            return

        for router, limits in ceilings.items():
            if not isinstance(limits, dict):
                self.result.add_error(
                    f"Pricing ceiling for '{router}' must be a dict"
                )
                continue

            # Check required fields
            required = ["max_input_price", "max_output_price", "daily_budget"]
            for field in required:
                if field not in limits:
                    self.result.add_error(
                        f"Missing '{field}' in pricing ceiling for '{router}'"
                    )
                elif not isinstance(limits[field], (int, float)):
                    self.result.add_error(
                        f"'{field}' for '{router}' must be numeric, "
                        f"got {type(limits[field]).__name__}"
                    )
                elif limits[field] < 0:
                    self.result.add_error(
                        f"'{field}' for '{router}' must be non-negative"
                    )
                elif limits[field] > self.MAX_REASONABLE_PRICE:
                    self.result.add_warning(
                        f"'{field}' for '{router}' seems unusually high: "
                        f"{limits[field]}"
                    )

    def _validate_fallback_policy(self) -> None:
        """Validate fallback policy configuration."""
        policy = self.config["fallback_policy"]

        if not isinstance(policy, dict):
            self.result.add_error(
                f"fallback_policy must be a dict, got {type(policy).__name__}"
            )
            return

        # Validate priority order
        if "priority_order" in policy:
            self._validate_priority_order(policy["priority_order"])

        # Validate triggers
        if "triggers" in policy:
            if not isinstance(policy["triggers"], list):
                self.result.add_error("fallback_policy.triggers must be a list")

        # Validate retry configuration
        if "max_retries" in policy:
            max_retries = policy["max_retries"]
            if not isinstance(max_retries, int) or max_retries < 0:
                self.result.add_error(
                    f"max_retries must be a non-negative integer, got {max_retries}"
                )

    def _validate_priority_order(self, priority_order: Any) -> None:
        """Validate priority order configuration."""
        if not isinstance(priority_order, list):
            self.result.add_error(
                "fallback_policy.priority_order must be a list"
            )
            return

        seen_priorities: Set[int] = set()
        seen_routers: Set[str] = set()

        for entry in priority_order:
            if not isinstance(entry, dict):
                self.result.add_error(
                    f"Priority order entry must be dict, got {type(entry).__name__}"
                )
                continue

            if "router" not in entry or "priority" not in entry:
                self.result.add_error(
                    "Priority order entry missing 'router' or 'priority'"
                )
                continue

            router = entry["router"]
            priority = entry["priority"]

            if router in seen_routers:
                self.result.add_error(
                    f"Duplicate router in priority order: {router}"
                )
            seen_routers.add(router)

            if priority in seen_priorities:
                self.result.add_error(
                    f"Duplicate priority value: {priority}"
                )
            seen_priorities.add(priority)

    def _validate_model_catalog(self) -> None:
        """Validate model catalog entries."""
        models = self.config["models"]

        if not isinstance(models, dict):
            self.result.add_error(
                f"models must be a dict, got {type(models).__name__}"
            )
            return

        # Get validation rules if available
        validation_rules = self.config.get("validation", {})
        required_fields = validation_rules.get(
            "required_fields",
            ["router", "identifier", "context_window", "pricing", "default_role"],
        )
        allowed_routers = validation_rules.get(
            "allowed_routers", ["openrouter", "opencode_ai", "direct_api"]
        )
        allowed_roles = validation_rules.get(
            "allowed_roles", ["analysis", "creative", "coding", "general"]
        )
        allowed_capabilities = validation_rules.get("allowed_capabilities", [])

        for model_key, model_config in models.items():
            self._validate_model_entry(
                model_key,
                model_config,
                required_fields,
                allowed_routers,
                allowed_roles,
                allowed_capabilities,
            )

    def _validate_model_entry(
        self,
        model_key: str,
        model_config: Any,
        required_fields: List[str],
        allowed_routers: List[str],
        allowed_roles: List[str],
        allowed_capabilities: List[str],
    ) -> None:
        """Validate a single model entry.

        Args:
            model_key: Model identifier key.
            model_config: Model configuration dict.
            required_fields: List of required fields.
            allowed_routers: List of allowed router values.
            allowed_roles: List of allowed role values.
            allowed_capabilities: List of allowed capability values.
        """
        if not isinstance(model_config, dict):
            self.result.add_error(
                f"Model '{model_key}' config must be dict, "
                f"got {type(model_config).__name__}"
            )
            return

        # Check required fields
        for field in required_fields:
            if field not in model_config:
                self.result.add_error(
                    f"Model '{model_key}' missing required field: {field}"
                )

        # Validate router
        if "router" in model_config:
            router = model_config["router"]
            if router not in allowed_routers:
                self.result.add_error(
                    f"Model '{model_key}' has invalid router '{router}'. "
                    f"Allowed: {allowed_routers}"
                )

        # Validate identifier
        if "identifier" in model_config:
            identifier = model_config["identifier"]
            if not isinstance(identifier, str) or not identifier.strip():
                self.result.add_error(
                    f"Model '{model_key}' identifier must be non-empty string"
                )

        # Validate context window
        if "context_window" in model_config:
            context = model_config["context_window"]
            if not isinstance(context, int):
                self.result.add_error(
                    f"Model '{model_key}' context_window must be integer, "
                    f"got {type(context).__name__}"
                )
            elif context < self.MIN_CONTEXT_WINDOW:
                self.result.add_error(
                    f"Model '{model_key}' context_window too small: {context} "
                    f"(min: {self.MIN_CONTEXT_WINDOW})"
                )
            elif context > self.MAX_CONTEXT_WINDOW:
                self.result.add_warning(
                    f"Model '{model_key}' context_window unusually large: {context}"
                )

        # Validate pricing
        if "pricing" in model_config:
            self._validate_model_pricing(model_key, model_config)

        # Validate default role
        if "default_role" in model_config:
            role = model_config["default_role"]
            if role not in allowed_roles:
                self.result.add_error(
                    f"Model '{model_key}' has invalid role '{role}'. "
                    f"Allowed: {allowed_roles}"
                )

        # Validate capabilities
        if "capabilities" in model_config:
            capabilities = model_config["capabilities"]
            if not isinstance(capabilities, list):
                self.result.add_error(
                    f"Model '{model_key}' capabilities must be list"
                )
            elif allowed_capabilities:
                for cap in capabilities:
                    if cap not in allowed_capabilities:
                        self.result.add_warning(
                            f"Model '{model_key}' has unknown capability: {cap}"
                        )

    def _validate_model_pricing(
        self, model_key: str, model_config: Dict[str, Any]
    ) -> None:
        """Validate model pricing against ceilings.

        Args:
            model_key: Model identifier key.
            model_config: Model configuration dict.
        """
        pricing = model_config["pricing"]
        router = model_config.get("router")

        if not isinstance(pricing, dict):
            self.result.add_error(
                f"Model '{model_key}' pricing must be dict, "
                f"got {type(pricing).__name__}"
            )
            return

        # Check required pricing fields
        if "input_per_1k" not in pricing:
            self.result.add_error(
                f"Model '{model_key}' missing pricing.input_per_1k"
            )
        if "output_per_1k" not in pricing:
            self.result.add_error(
                f"Model '{model_key}' missing pricing.output_per_1k"
            )

        # Validate against ceilings
        if router and "pricing_ceilings" in self.config:
            ceilings = self.config["pricing_ceilings"].get(router)
            if ceilings:
                input_price = pricing.get("input_per_1k", 0)
                output_price = pricing.get("output_per_1k", 0)

                if input_price > ceilings.get("max_input_price", float("inf")):
                    self.result.add_error(
                        f"Model '{model_key}' input price ${input_price} exceeds "
                        f"ceiling ${ceilings['max_input_price']} for router '{router}'"
                    )

                if output_price > ceilings.get("max_output_price", float("inf")):
                    self.result.add_error(
                        f"Model '{model_key}' output price ${output_price} exceeds "
                        f"ceiling ${ceilings['max_output_price']} for router '{router}'"
                    )

        # Check for negative prices
        for price_type in ["input_per_1k", "output_per_1k"]:
            if price_type in pricing:
                price = pricing[price_type]
                if not isinstance(price, (int, float)):
                    self.result.add_error(
                        f"Model '{model_key}' {price_type} must be numeric"
                    )
                elif price < 0:
                    self.result.add_error(
                        f"Model '{model_key}' {price_type} cannot be negative"
                    )

    def _validate_fallback_references(self) -> None:
        """Validate that fallback_to references exist and don't create cycles."""
        models = self.config.get("models", {})

        # Build fallback graph
        fallback_graph: Dict[str, Optional[str]] = {}
        for model_key, model_config in models.items():
            fallback_graph[model_key] = model_config.get("fallback_to")

        # Check each fallback reference exists
        for model_key, fallback in fallback_graph.items():
            if fallback is not None and fallback not in models:
                self.result.add_error(
                    f"Model '{model_key}' fallback_to '{fallback}' does not exist"
                )

        # Check for cycles
        for start_model in models:
            visited: Set[str] = set()
            current = start_model

            while current is not None:
                if current in visited:
                    cycle = " -> ".join(visited) + f" -> {current}"
                    self.result.add_error(
                        f"Fallback cycle detected starting from '{start_model}': {cycle}"
                    )
                    break

                visited.add(current)
                current = fallback_graph.get(current)

    def _validate_role_defaults(self) -> None:
        """Validate role default model references."""
        role_defaults = self.config["role_defaults"]
        models = self.config.get("models", {})

        if not isinstance(role_defaults, dict):
            self.result.add_error(
                "role_defaults must be dict"
            )
            return

        for role, defaults in role_defaults.items():
            if not isinstance(defaults, dict):
                self.result.add_error(
                    f"Role defaults for '{role}' must be dict"
                )
                continue

            # Check that referenced models exist
            for tier in ["primary", "fallback", "budget_conscious"]:
                if tier in defaults:
                    model_ref = defaults[tier]
                    if model_ref not in models:
                        self.result.add_error(
                            f"Role '{role}' {tier} references non-existent "
                            f"model: {model_ref}"
                        )

    def _validate_validation_rules(self) -> None:
        """Validate the validation rules section (meta-validation)."""
        validation = self.config["validation"]

        if not isinstance(validation, dict):
            self.result.add_error(
                "validation section must be dict"
            )
            return

        # Check that validation rules lists are actually lists
        list_fields = [
            "required_fields",
            "allowed_routers",
            "allowed_roles",
            "allowed_capabilities",
        ]

        for field in list_fields:
            if field in validation and not isinstance(validation[field], list):
                self.result.add_error(
                    f"validation.{field} must be list"
                )


def load_config(file_path: Path) -> Optional[Dict[str, Any]]:
    """Load and parse YAML configuration file.

    Args:
        file_path: Path to YAML file.

    Returns:
        Parsed configuration dict, or None if loading failed.
    """
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config
    except yaml.YAMLError as e:
        print(f"ERROR: Invalid YAML in {file_path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: Failed to read {file_path}: {e}", file=sys.stderr)
        return None


def print_results(result: ValidationResult, format_type: str = "text") -> None:
    """Print validation results.

    Args:
        result: Validation result object.
        format_type: Output format ('text' or 'json').
    """
    if format_type == "json":
        print(json.dumps(result.to_dict(), indent=2))
        return

    # Text output
    if result.errors:
        print("\n❌ ERRORS:")
        for error in result.errors:
            print(f"  • {error}")

    if result.warnings:
        print("\n⚠️  WARNINGS:")
        for warning in result.warnings:
            print(f"  • {warning}")

    if result.info:
        print("\nℹ️  INFO:")
        for info in result.info:
            print(f"  • {info}")

    print("\n" + "=" * 60)
    if result.is_valid():
        print("✅ Validation PASSED")
    else:
        print("❌ Validation FAILED")
    print("=" * 60)


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 = success, non-zero = failure).
    """
    parser = argparse.ArgumentParser(
        description="Validate model router configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --file ops/config/model_router.yaml
  %(prog)s --strict --format json

Exit codes:
  0 = validation passed
  1 = validation failed
  2 = file not found or invalid YAML
  3 = invalid arguments
        """,
    )

    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        default=Path("ops/config/model_router.yaml"),
        help="Path to model router config file (default: ops/config/model_router.yaml)",
    )

    parser.add_argument(
        "--strict",
        "-s",
        action="store_true",
        help="Treat warnings as errors",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.file)
    if config is None:
        return 2

    # Validate
    validator = ModelRouterValidator(config, strict=args.strict)
    result = validator.validate()

    # Print results
    print_results(result, args.format)

    # Return appropriate exit code
    if result.is_valid(strict=args.strict):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
