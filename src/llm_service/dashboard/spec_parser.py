"""
Specification Parser for Initiative Tracking.

Parses YAML frontmatter from specification markdown files to extract
initiative, feature, and metadata information for the portfolio view.

Implements ADR-037: Dashboard Initiative Tracking.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import re
import yaml
import logging

# Import status enums (ADR-043)
from src.domain.specifications.types import FeatureStatus

logger = logging.getLogger(__name__)


@dataclass
class Feature:
    """
    Represents a feature within a specification.

    Features are extracted from the specification frontmatter and linked to tasks.
    """

    id: str
    title: str
    status: str | None = None

    def __post_init__(self):
        """Validate feature data."""
        if not self.id:
            raise ValueError("Feature ID cannot be empty")
        if not self.title:
            raise ValueError("Feature title cannot be empty")


@dataclass
class SpecificationMetadata:
    """
    Metadata extracted from specification frontmatter.

    Attributes:
        id: Unique specification identifier
        title: Specification title
        status: Current status (draft, in_progress, implemented, deprecated)
        initiative: High-level initiative/milestone grouping
        priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
        features: List of features defined in this specification
        completion: Manual completion percentage override (0-100)
        path: Absolute filesystem path to specification file
        relative_path: Relative path from specifications directory
        created: Creation date (ISO format)
        updated: Last update date (ISO format)
        author: Specification author
        epic: Optional epic grouping
        target_personas: Optional list of target personas
    """

    id: str
    title: str
    status: str
    initiative: str
    priority: str
    features: list[Feature] = field(default_factory=list)
    completion: int | None = None
    path: str = ""
    relative_path: str = ""
    created: str = ""
    updated: str = ""
    author: str = ""
    epic: str | None = None
    target_personas: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate metadata after initialization."""
        if not self.id:
            raise ValueError("Specification ID is required")
        if not self.title:
            raise ValueError("Specification title is required")
        if not self.status:
            raise ValueError("Specification status is required")
        if not self.initiative:
            raise ValueError("Specification initiative is required")

        # Validate completion if present
        if self.completion is not None:
            if not isinstance(self.completion, int):
                raise ValueError("Completion must be an integer")
            if self.completion < 0 or self.completion > 100:
                raise ValueError("Completion must be between 0 and 100")


class SpecificationParser:
    """
    Parser for specification markdown files with YAML frontmatter.

    Scans specification directories and extracts metadata for portfolio view.
    """

    def __init__(self, base_dir: str):
        """
        Initialize parser with base specifications directory.

        Args:
            base_dir: Base directory containing specification files
        """
        self.base_dir = Path(base_dir)
        if not self.base_dir.is_absolute():
            self.base_dir = self.base_dir.absolute()

    def extract_frontmatter(self, content: str) -> str | None:
        """
        Extract YAML frontmatter from markdown content.

        Frontmatter is delimited by --- markers at the start of the file:
        ---
        key: value
        ---

        Args:
            content: Full markdown file content

        Returns:
            Extracted YAML string, or None if no frontmatter found
        """
        # Match frontmatter: must start with ---, end with ---
        # Use DOTALL flag to match across newlines
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)

        if not match:
            return None

        return match.group(1)

    def parse_yaml(self, yaml_str: str) -> dict[str, Any] | None:
        """
        Parse YAML string into dictionary.

        Args:
            yaml_str: YAML content as string

        Returns:
            Parsed dictionary, or None if parsing fails
        """
        try:
            data = yaml.safe_load(yaml_str)
            return data if isinstance(data, dict) else None
        except yaml.YAMLError as e:
            logger.warning(f"Failed to parse YAML: {e}")
            return None

    def validate_metadata(self, data: dict[str, Any]) -> bool:
        """
        Validate that required frontmatter fields are present.

        Required fields: id, title, status, initiative

        Args:
            data: Parsed frontmatter dictionary

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["id", "title", "status", "initiative"]

        for field_name in required_fields:
            if field_name not in data or not data[field_name]:
                logger.warning(f"Missing required field: {field_name}")
                return False

        return True

    def parse_frontmatter(self, spec_path: str) -> SpecificationMetadata | None:
        """
        Parse frontmatter from a specification file.

        Args:
            spec_path: Path to specification markdown file

        Returns:
            SpecificationMetadata instance, or None if parsing fails
        """
        try:
            path = Path(spec_path)

            # Check file exists
            if not path.exists():
                logger.warning(f"Specification file not found: {spec_path}")
                return None

            # Read content (only first portion for efficiency)
            # Frontmatter is typically <1KB, so read first 5KB max
            with open(path, encoding='utf-8') as f:
                content = f.read(5000)  # Limit to avoid reading huge files

            # Check if file is empty
            if not content.strip():
                logger.warning(f"Empty specification file: {spec_path}")
                return None

            # Extract frontmatter
            frontmatter_str = self.extract_frontmatter(content)
            if not frontmatter_str:
                logger.debug(f"No frontmatter found in: {spec_path}")
                return None

            # Parse YAML
            data = self.parse_yaml(frontmatter_str)
            if not data:
                logger.warning(f"Failed to parse frontmatter YAML: {spec_path}")
                return None

            # Validate required fields
            if not self.validate_metadata(data):
                logger.warning(f"Invalid frontmatter (missing required fields): {spec_path}")
                return None

            # Calculate relative path from base directory
            try:
                # Ensure both paths are absolute for comparison
                abs_path = path.resolve()
                abs_base = self.base_dir.resolve()
                relative_path = str(abs_path.relative_to(abs_base))
            except ValueError:
                # Path is not relative to base_dir (outside base)
                logger.warning(f"Path {path} is outside base_dir {self.base_dir}, using filename only")
                relative_path = path.name

            # Parse features if present
            features = []
            if "features" in data and isinstance(data["features"], list):
                for feat_data in data["features"]:
                    if isinstance(feat_data, dict):
                        try:
                            feature = Feature(
                                id=feat_data.get("id", ""),
                                title=feat_data.get("title", ""),
                                status=feat_data.get("status")
                            )
                            features.append(feature)
                        except ValueError as e:
                            logger.warning(f"Invalid feature in {spec_path}: {e}")
                            continue

            # Create metadata instance
            metadata = SpecificationMetadata(
                id=data["id"],
                title=data["title"],
                status=data["status"],
                initiative=data["initiative"],
                priority=data.get("priority", "MEDIUM"),
                features=features,
                completion=data.get("completion"),
                path=str(path.absolute()),
                relative_path=relative_path,
                created=data.get("created", ""),
                updated=data.get("updated", ""),
                author=data.get("author", ""),
                epic=data.get("epic"),
                target_personas=data.get("target_personas", [])
            )

            return metadata

        except PermissionError:
            logger.error(f"Permission denied reading: {spec_path}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing {spec_path}: {e}", exc_info=True)
            return None

    def scan_specifications(self, directory: str) -> list[SpecificationMetadata]:
        """
        Scan directory recursively for specification markdown files.

        Only processes .md files. Skips files without valid frontmatter.

        Args:
            directory: Directory to scan for specifications

        Returns:
            List of parsed SpecificationMetadata instances
        """
        specs = []
        dir_path = Path(directory)

        if not dir_path.exists():
            logger.warning(f"Specifications directory not found: {directory}")
            return specs

        # Find all .md files recursively
        for md_file in dir_path.rglob("*.md"):
            metadata = self.parse_frontmatter(str(md_file))
            if metadata:
                specs.append(metadata)

        logger.info(f"Scanned {directory}: found {len(specs)} valid specifications")
        return specs

    def get_status_weight(self, status: str) -> float:
        """
        Get the weight for a status value (for progress calculation).

        Helper method for ProgressCalculator integration.

        Args:
            status: Status string

        Returns:
            Weight value (0.0 to 1.0)
        """
        weights = {
            FeatureStatus.IMPLEMENTED.value: 1.0,
            "done": 1.0,  # Alias for backward compatibility
            FeatureStatus.IN_PROGRESS.value: 0.5,
            FeatureStatus.DRAFT.value: 0.0,
            FeatureStatus.PLANNED.value: 0.0,
            FeatureStatus.DEPRECATED.value: 0.0,
        }
        return weights.get(status.lower(), 0.0)
