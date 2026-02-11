"""
Doctrine parsing exceptions.

Custom exceptions for parsing errors, validation failures, and file handling issues.
Provides detailed error messages with context (line numbers, file paths) to aid debugging.

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model

Examples
--------
>>> from pathlib import Path
>>> try:
...     raise ParseError("Invalid YAML syntax", file_path=Path("test.md"), line_number=42)
... except ParseError as e:
...     print(f"Error at {e.file_path}:{e.line_number}")
Error at test.md:42
"""

from pathlib import Path


class DoctrineParseError(Exception):
    """
    Base exception for all doctrine parsing errors.

    All parser exceptions inherit from this base class to enable
    catch-all error handling when needed.
    """

    pass


class ParseError(DoctrineParseError):
    """
    Failed to parse file due to syntax errors, malformed structure, or file not found.

    Attributes
    ----------
    message : str
        Human-readable error description
    file_path : Path | None
        Path to file that failed parsing
    line_number : int | None
        Line number where error occurred (if applicable)
    """

    def __init__(
        self,
        message: str,
        file_path: Path | None = None,
        line_number: int | None = None,
    ):
        self.message = message
        self.file_path = file_path
        self.line_number = line_number

        # Build detailed error message
        error_parts = [message]
        if file_path:
            error_parts.append(f"File: {file_path}")
        if line_number is not None:
            error_parts.append(f"Line: {line_number}")

        super().__init__(" | ".join(error_parts))


class ValidationError(DoctrineParseError):
    """
    Parsed data failed validation (missing required fields, invalid values).

    Attributes
    ----------
    message : str
        Human-readable validation error description
    field_name : str | None
        Name of field that failed validation
    file_path : Path | None
        Path to file with validation error
    """

    def __init__(
        self,
        message: str,
        field_name: str | None = None,
        file_path: Path | None = None,
    ):
        self.message = message
        self.field_name = field_name
        self.file_path = file_path

        # Build detailed error message
        error_parts = [message]
        if field_name:
            error_parts.append(f"Field: {field_name}")
        if file_path:
            error_parts.append(f"File: {file_path}")

        super().__init__(" | ".join(error_parts))


class InvalidDirectiveId(ValidationError):
    """
    Directive ID format is invalid (e.g., non-numeric, missing).

    Directive IDs must be numeric strings like "001", "016", "017".
    """

    def __init__(self, directive_id: str, file_path: Path | None = None):
        message = f"Invalid directive ID format: {directive_id!r}"
        super().__init__(message, field_name="id", file_path=file_path)
        self.directive_id = directive_id


class MissingRequiredField(ValidationError):
    """
    Required field is missing from parsed data.

    Attributes
    ----------
    field_name : str
        Name of missing required field
    artifact_type : str
        Type of artifact (e.g., "Agent", "Directive")
    """

    def __init__(
        self, field_name: str, artifact_type: str, file_path: Path | None = None
    ):
        message = f"Missing required field in {artifact_type}"
        super().__init__(message, field_name=field_name, file_path=file_path)
        self.artifact_type = artifact_type


__all__ = [
    "DoctrineParseError",
    "ParseError",
    "ValidationError",
    "InvalidDirectiveId",
    "MissingRequiredField",
]
