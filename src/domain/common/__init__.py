"""
Common Utilities Module.

This module contains truly shared utilities with NO domain semantics.
These are generic, reusable components that can be used across any bounded context.

⚠️ Important: This module should NOT contain domain logic. If a utility is
specific to collaboration, doctrine, or specifications, it belongs in that
bounded context instead.

Domain: None (generic utilities only)

Key Concepts
------------
Validators
    Generic validation functions (schema validation, format checking, etc.)
    that have no domain-specific logic.

Parsers
    Generic parsing utilities (YAML, JSON, Markdown) without domain semantics.

File Utilities
    Generic file system operations (reading, writing, path manipulation)
    independent of domain concerns.

String Utilities
    Generic string manipulation functions (slugify, sanitize, format).

Related ADRs
------------
- ADR-046: Domain Module Refactoring

Examples
--------
>>> # Future usage after Task 2 (file migration)
>>> # from src.domain.common import validate_yaml_schema
>>> # from src.domain.common import sanitize_filename
>>> # is_valid = validate_yaml_schema(content, schema)
>>> # safe_name = sanitize_filename("my file!.txt")  # -> "my_file.txt"
"""

__all__ = []  # Will be populated in Task 2 when files are moved
