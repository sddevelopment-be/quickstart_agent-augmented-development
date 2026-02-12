"""
Template System for Configuration Generation

This package provides Jinja2 templates for generating LLM service configurations.
Implements ADR-031: Template-Based Configuration Generation.

Available Templates:
- quick-start.yaml.j2: Minimal setup with claude-code (recommended for new users)
- claude-only.yaml.j2: Claude-focused configuration with fine-tuned cost controls
- cost-optimized.yaml.j2: Multi-model setup with aggressive cost routing
- development.yaml.j2: All features enabled with debug logging for testing
"""

__all__ = ["TemplateManager", "AVAILABLE_TEMPLATES"]

# Template metadata
AVAILABLE_TEMPLATES = {
    "quick-start": {
        "file": "quick-start.yaml.j2",
        "description": "Minimal setup with detected tools (recommended)",
        "suitable_for": "New users, quick onboarding",
    },
    "claude-only": {
        "file": "claude-only.yaml.j2",
        "description": "Claude-focused configuration",
        "suitable_for": "Claude API users, focused workflows",
    },
    "cost-optimized": {
        "file": "cost-optimized.yaml.j2",
        "description": "Multi-model with aggressive cost routing",
        "suitable_for": "Budget-conscious teams, high-volume usage",
    },
    "development": {
        "file": "development.yaml.j2",
        "description": "All features with debug logging",
        "suitable_for": "Development, testing, debugging",
    },
}

from .manager import TemplateManager
