"""
Doctrine artifact parsers.

Parsers for loading doctrine files (agents, directives, tactics, approaches) from
Markdown files with YAML frontmatter into immutable domain objects.

All parsers follow the same pattern:
1. Load file content
2. Parse YAML frontmatter
3. Extract structured sections from markdown
4. Validate required fields
5. Calculate source hash for traceability
6. Construct immutable domain object

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model

Design Principles
-----------------
1. Read-only: Never modify source files
2. Error handling: Explicit exceptions with context
3. Validation: Check required fields and formats
4. Traceability: Calculate source hashes for change detection
5. Immutability: Return frozen dataclasses

Examples
--------
>>> from pathlib import Path
>>> parser = DirectiveParser()
>>> directive = parser.parse(Path("doctrine/directives/017_tdd.md"))
>>> assert directive.id == "017"
>>> assert directive.enforcement == "mandatory"

>>> agent_parser = AgentParser()
>>> agent = agent_parser.parse(Path(".github/agents/python-pedro.agent.md"))
>>> assert "python" in agent.capabilities
"""

import hashlib
import re
from pathlib import Path

import frontmatter  # type: ignore
import yaml

from .exceptions import (
    InvalidDirectiveId,
    MissingRequiredField,
    ParseError,
    ValidationError,
)
from .models import Agent, Approach, Directive, Tactic


class DirectiveParser:
    """
    Parser for directive Markdown files.

    Parses directive files (e.g., `001_context_notes.md`) with YAML frontmatter
    and structured Markdown sections into Directive domain objects.

    Examples
    --------
    >>> parser = DirectiveParser()
    >>> directive = parser.parse(Path("directives/017_tdd.md"))
    >>> assert directive.number == 17
    >>> assert directive.category == "testing"
    """

    def parse(self, file_path: Path) -> Directive:
        """
        Parse directive file into Directive domain object.

        Args:
            file_path: Path to directive file (e.g., 001_context_notes.md)

        Returns:
            Directive domain object

        Raises:
            ParseError: If file cannot be parsed (missing, malformed YAML)
            ValidationError: If parsed data is invalid
            InvalidDirectiveId: If directive ID format is invalid
        """
        # Check file exists
        if not file_path.exists():
            raise ParseError(
                f"Directive file does not exist: {file_path}",
                file_path=file_path,
            )

        # Load file content
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            raise ParseError(
                f"Failed to read file: {e}",
                file_path=file_path,
            ) from e

        # Calculate source hash
        source_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # Parse frontmatter
        try:
            post = frontmatter.loads(content)
        except yaml.YAMLError as e:
            raise ParseError(
                f"Invalid YAML frontmatter: {e}",
                file_path=file_path,
            ) from e

        metadata = post.metadata
        markdown_content = post.content

        # Extract directive ID from filename
        directive_id = self._extract_directive_id(file_path.name, file_path)

        # Extract title from markdown
        title = self._extract_title(markdown_content)

        # Extract sections
        description = self._extract_section(markdown_content, "## Description")
        rationale = self._extract_section(markdown_content, "## Rationale")
        examples = self._extract_examples(markdown_content)

        # Extract metadata with defaults
        category = metadata.get("category", "uncategorized")
        scope = metadata.get("scope", "all-agents")
        enforcement = metadata.get("enforcement", "mandatory")
        version = metadata.get("version", "1.0")
        status = metadata.get("status", "active")
        tags_list = metadata.get("tags", [])
        tags = frozenset(tags_list) if isinstance(tags_list, list) else frozenset()

        # Construct Directive domain object
        return Directive(
            id=directive_id,
            number=int(directive_id),
            title=title,
            category=category,
            scope=scope,
            enforcement=enforcement,
            description=description,
            rationale=rationale,
            examples=tuple(examples),
            source_file=file_path,
            source_hash=source_hash,
            version=str(version),
            status=status,
            tags=tags,
        )

    def _extract_directive_id(self, filename: str, file_path: Path) -> str:
        """
        Extract directive ID from filename.

        Examples: '001_context_notes.md' -> '001'
                  '017_tdd.md' -> '017'

        Args:
            filename: Filename to extract ID from
            file_path: Full file path (for error reporting)

        Returns:
            Directive ID as string

        Raises:
            InvalidDirectiveId: If ID format is invalid
        """
        # Match pattern: NNN_*.md where NNN is 3 digits
        match = re.match(r"^(\d{3})_", filename)
        if not match:
            raise InvalidDirectiveId(
                directive_id=filename,
                file_path=file_path,
            )

        return match.group(1)

    def _extract_title(self, content: str) -> str:
        """
        Extract title from markdown content.

        Looks for first level-1 heading (# Title) or level-2 heading with "Directive".

        Args:
            content: Markdown content

        Returns:
            Extracted title

        Raises:
            ValidationError: If no title found
        """
        # Try to find "# Directive NNN: Title" pattern
        match = re.search(r"^#\s+Directive\s+\d+:\s*(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Fallback: First level-1 heading
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            # Remove "Directive NNN:" prefix if present
            title = re.sub(r"^Directive\s+\d+:\s*", "", title)
            return title

        raise ValidationError("No title found in directive content")

    def _extract_section(self, content: str, heading: str) -> str:
        """
        Extract section content under a markdown heading.

        Args:
            content: Markdown content
            heading: Heading to search for (e.g., "## Description")

        Returns:
            Section content (empty string if not found)
        """
        # Escape special regex characters in heading
        escaped_heading = re.escape(heading)

        # Find section from heading to next heading of same or higher level
        pattern = rf"{escaped_heading}\s*\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

        if match:
            section_content = match.group(1).strip()
            return section_content

        return ""

    def _extract_examples(self, content: str) -> list[str]:
        """
        Extract examples from ## Examples section.

        Looks for code blocks or list items under ## Examples heading.

        Args:
            content: Markdown content

        Returns:
            List of example strings
        """
        examples_section = self._extract_section(content, "## Examples")
        if not examples_section:
            return []

        examples = []

        # Extract code blocks
        code_blocks = re.findall(r"```.*?\n(.*?)```", examples_section, re.DOTALL)
        examples.extend([block.strip() for block in code_blocks if block.strip()])

        # Extract bold/strong example headers (e.g., **Example 1:**)
        example_headers = re.findall(
            r"\*\*Example.*?\*\*", examples_section, re.IGNORECASE
        )
        examples.extend([header.strip() for header in example_headers])

        return examples


class AgentParser:
    """
    Parser for agent profile Markdown files.

    Parses agent profile files (e.g., `python-pedro.agent.md`) into Agent domain objects.

    Examples
    --------
    >>> parser = AgentParser()
    >>> agent = parser.parse(Path(".github/agents/python-pedro.agent.md"))
    >>> assert agent.id == "python-pedro"
    """

    def parse(self, file_path: Path) -> Agent:
        """
        Parse agent profile file into Agent domain object.

        Args:
            file_path: Path to agent file (e.g., python-pedro.agent.md)

        Returns:
            Agent domain object

        Raises:
            ParseError: If file cannot be parsed
            ValidationError: If parsed data is invalid
            MissingRequiredField: If required fields are missing
        """
        # Check file exists
        if not file_path.exists():
            raise ParseError(
                f"Agent file does not exist: {file_path}",
                file_path=file_path,
            )

        # Load file content
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            raise ParseError(
                f"Failed to read file: {e}",
                file_path=file_path,
            ) from e

        # Calculate source hash
        source_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # Parse frontmatter
        try:
            post = frontmatter.loads(content)
        except yaml.YAMLError as e:
            raise ParseError(
                f"Invalid YAML frontmatter: {e}",
                file_path=file_path,
            ) from e

        metadata = post.metadata
        markdown_content = post.content

        # Extract required fields from frontmatter
        agent_id = metadata.get("name")
        if not agent_id:
            raise MissingRequiredField("name", "Agent", file_path)

        description = metadata.get("description")
        if not description:
            raise MissingRequiredField("description", "Agent", file_path)

        # Extract name from markdown heading
        name = self._extract_agent_name(markdown_content, agent_id)

        # Extract sections
        specialization = self._extract_section(markdown_content, "## 2. Purpose")
        if not specialization:
            specialization = self._extract_section(markdown_content, "## Purpose")
        if not specialization:
            specialization = description  # Fallback to description

        # Extract capabilities
        capabilities = self._extract_capabilities(markdown_content)

        # Extract required directives
        required_directives = self._extract_directive_ids(markdown_content)

        # Extract primers
        primers = self._extract_primers(markdown_content)

        # Extract metadata with defaults
        version = metadata.get("version", "1.0")
        status = metadata.get("status", "active")
        tags_list = metadata.get("tags", [])
        tags = frozenset(tags_list) if isinstance(tags_list, list) else frozenset()

        # Construct Agent domain object
        return Agent(
            id=agent_id,
            name=name,
            specialization=specialization,
            capabilities=capabilities,
            required_directives=required_directives,
            primers=primers,
            source_file=file_path,
            source_hash=source_hash,
            version=str(version),
            status=status,
            tags=tags,
        )

    def _extract_agent_name(self, content: str, agent_id: str) -> str:
        """Extract agent name from markdown heading."""
        # Look for "# Agent Profile: Name" pattern
        match = re.search(
            r"^#\s+Agent\s+Profile:\s*([^(]+)", content, re.MULTILINE | re.IGNORECASE
        )
        if match:
            name = match.group(1).strip()
            return name

        # Fallback: Convert ID to title case
        return agent_id.replace("-", " ").title()

    def _extract_section(self, content: str, heading: str) -> str:
        """Extract section content under a heading."""
        escaped_heading = re.escape(heading)
        pattern = rf"{escaped_heading}\s*\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

        if match:
            return match.group(1).strip()

        return ""

    def _extract_capabilities(self, content: str) -> frozenset[str]:
        """Extract agent capabilities from ## Capabilities section."""
        section = self._extract_section(content, "## 7. Capabilities")
        if not section:
            section = self._extract_section(content, "## Capabilities")
        if not section:
            section = self._extract_section(content, "## 3. Specialization")

        capabilities = set()

        # Extract from bullet lists
        bullet_items = re.findall(r"^[-*]\s+(.+)$", section, re.MULTILINE)
        for item in bullet_items:
            # Clean up markdown formatting
            clean_item = re.sub(r"\*\*(.+?)\*\*", r"\1", item)
            clean_item = clean_item.split(":")[0].strip().lower()
            if clean_item and len(clean_item) < 50:  # Reasonable capability name length
                capabilities.add(clean_item)

        return frozenset(capabilities) if capabilities else frozenset(["general"])

    def _extract_directive_ids(self, content: str) -> frozenset[str]:
        """Extract required directive IDs."""
        section = self._extract_section(content, "## 5. Required Directives")
        if not section:
            section = self._extract_section(content, "## Required Directives")

        directive_ids = set()

        # Find patterns like "016:", "Directive 017", etc.
        matches = re.findall(r"\b(\d{3})\b", section)
        directive_ids.update(matches)

        return frozenset(directive_ids)

    def _extract_primers(self, content: str) -> frozenset[str]:
        """Extract execution primers."""
        section = self._extract_section(content, "## 6. Primers")
        if not section:
            section = self._extract_section(content, "## Primers")

        primers = set()

        # Extract from bullet lists
        bullet_items = re.findall(r"^[-*]\s+(.+?):", section, re.MULTILINE)
        for item in bullet_items:
            clean_item = item.strip()
            if clean_item and len(clean_item) < 30:
                primers.add(clean_item)

        return frozenset(primers)


class TacticParser:
    """
    Parser for tactic Markdown files.

    Parses tactic files (e.g., `red-green-refactor.tactic.md`) into Tactic domain objects.

    Examples
    --------
    >>> parser = TacticParser()
    >>> tactic = parser.parse(Path("tactics/red-green-refactor.tactic.md"))
    >>> assert tactic.id == "red-green-refactor"
    """

    def parse(self, file_path: Path) -> Tactic:
        """
        Parse tactic file into Tactic domain object.

        Args:
            file_path: Path to tactic file

        Returns:
            Tactic domain object

        Raises:
            ParseError: If file cannot be parsed
        """
        # Check file exists
        if not file_path.exists():
            raise ParseError(
                f"Tactic file does not exist: {file_path}",
                file_path=file_path,
            )

        # Load file content
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            raise ParseError(
                f"Failed to read file: {e}",
                file_path=file_path,
            ) from e

        # Calculate source hash
        source_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # Parse frontmatter (optional for tactics)
        try:
            post = frontmatter.loads(content)
            metadata = post.metadata
            markdown_content = post.content
        except yaml.YAMLError:
            # No frontmatter is OK for tactics
            metadata = {}
            markdown_content = content

        # Extract tactic ID from filename
        tactic_id = self._extract_tactic_id(file_path.name)

        # Extract title
        title = self._extract_title(markdown_content)

        # Extract sections
        description = self._extract_section(markdown_content, "## Intent")
        if not description:
            description = self._extract_section(markdown_content, "## Description")

        steps = self._extract_steps(markdown_content)
        prerequisites = self._extract_list_items(markdown_content, "## Preconditions")
        outcomes = self._extract_list_items(
            markdown_content, "## Expected Outcomes"
        )

        # Extract metadata with defaults
        version = metadata.get("version", "1.0")
        status = metadata.get("status", "active")
        tags_list = metadata.get("tags", [])
        tags = frozenset(tags_list) if isinstance(tags_list, list) else frozenset()

        # Construct Tactic domain object
        return Tactic(
            id=tactic_id,
            title=title,
            description=description,
            steps=tuple(steps),
            prerequisites=prerequisites,
            outcomes=outcomes,
            source_file=file_path,
            source_hash=source_hash,
            version=str(version),
            status=status,
            tags=tags,
        )

    def _extract_tactic_id(self, filename: str) -> str:
        """Extract tactic ID from filename (remove .tactic.md extension)."""
        # Remove .tactic.md or .md extension
        tactic_id = filename.replace(".tactic.md", "").replace(".md", "")
        return tactic_id

    def _extract_title(self, content: str) -> str:
        """Extract title from markdown heading."""
        # Look for "# Tactic: Title" pattern
        match = re.search(
            r"^#\s+Tactic:\s*(.+)$", content, re.MULTILINE | re.IGNORECASE
        )
        if match:
            return match.group(1).strip()

        # Fallback: First level-1 heading
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        return "Untitled Tactic"

    def _extract_section(self, content: str, heading: str) -> str:
        """Extract section content under a heading."""
        escaped_heading = re.escape(heading)
        pattern = rf"{escaped_heading}\s*\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

        if match:
            return match.group(1).strip()

        return ""

    def _extract_steps(self, content: str) -> list[str]:
        """Extract execution steps from ## Execution Steps section."""
        section = self._extract_section(content, "## Execution Steps")
        if not section:
            # Try numbered list format
            section = content

        steps = []

        # Extract numbered steps (1., 2., etc.)
        numbered_steps = re.findall(
            r"^\d+\.\s+\*\*(.+?)\*\*", section, re.MULTILINE
        )
        if numbered_steps:
            steps.extend(numbered_steps)
        else:
            # Extract bullet points
            bullet_items = re.findall(r"^[-*]\s+(.+)$", section, re.MULTILINE)
            steps.extend([item.strip() for item in bullet_items if item.strip()])

        return steps if steps else ["Execute tactic"]

    def _extract_list_items(self, content: str, heading: str) -> frozenset[str]:
        """Extract list items from a section as frozenset."""
        section = self._extract_section(content, heading)
        if not section:
            return frozenset()

        items = set()

        # Extract bullet points
        bullet_items = re.findall(r"^[-*]\s+(.+)$", section, re.MULTILINE)
        for item in bullet_items:
            clean_item = item.strip()
            if clean_item:
                items.add(clean_item)

        return frozenset(items)


class ApproachParser:
    """
    Parser for approach Markdown files.

    Parses approach documents into Approach domain objects.

    Examples
    --------
    >>> parser = ApproachParser()
    >>> approach = parser.parse(Path("approaches/test-first-development.md"))
    >>> assert "test" in approach.id.lower()
    """

    def parse(self, file_path: Path) -> Approach:
        """
        Parse approach file into Approach domain object.

        Args:
            file_path: Path to approach file

        Returns:
            Approach domain object

        Raises:
            ParseError: If file cannot be parsed
        """
        # Check file exists
        if not file_path.exists():
            raise ParseError(
                f"Approach file does not exist: {file_path}",
                file_path=file_path,
            )

        # Load file content
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            raise ParseError(
                f"Failed to read file: {e}",
                file_path=file_path,
            ) from e

        # Calculate source hash
        source_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # Parse frontmatter (optional for approaches)
        try:
            post = frontmatter.loads(content)
            metadata = post.metadata
            markdown_content = post.content
        except yaml.YAMLError:
            metadata = {}
            markdown_content = content

        # Extract approach ID from filename
        approach_id = self._extract_approach_id(file_path.name)

        # Extract title
        title = self._extract_title(markdown_content)

        # Extract sections
        purpose = self._extract_section(markdown_content, "## Purpose")
        principles = self._extract_list_items(markdown_content, "## Principles")
        when_to_use = self._extract_list_items(markdown_content, "## When to Use")
        when_to_avoid = self._extract_list_items(markdown_content, "## When to Avoid")
        related_directives = self._extract_directive_ids(markdown_content)

        # Extract metadata with defaults
        version = metadata.get("version", "1.0")
        status = metadata.get("status", "active")
        tags_list = metadata.get("tags", [])
        tags = frozenset(tags_list) if isinstance(tags_list, list) else frozenset()

        # Construct Approach domain object
        return Approach(
            id=approach_id,
            title=title,
            purpose=purpose,
            principles=principles,
            when_to_use=when_to_use,
            when_to_avoid=when_to_avoid,
            related_directives=related_directives,
            source_file=file_path,
            source_hash=source_hash,
            version=str(version),
            status=status,
            tags=tags,
        )

    def _extract_approach_id(self, filename: str) -> str:
        """Extract approach ID from filename (remove .md extension)."""
        return filename.replace(".md", "")

    def _extract_title(self, content: str) -> str:
        """Extract title from markdown heading."""
        # First level-1 heading
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        return "Untitled Approach"

    def _extract_section(self, content: str, heading: str) -> str:
        """Extract section content under a heading."""
        escaped_heading = re.escape(heading)
        pattern = rf"{escaped_heading}\s*\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

        if match:
            return match.group(1).strip()

        return ""

    def _extract_list_items(self, content: str, heading: str) -> tuple[str, ...]:
        """Extract list items from a section as tuple."""
        section = self._extract_section(content, heading)
        if not section:
            return ()

        items = []

        # Extract numbered items (1., 2., etc.)
        numbered_items = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", section, re.MULTILINE)
        if numbered_items:
            items.extend(numbered_items)
        else:
            # Extract bullet points
            bullet_items = re.findall(r"^[-*]\s+(.+)$", section, re.MULTILINE)
            items.extend([item.strip() for item in bullet_items if item.strip()])

        return tuple(items)

    def _extract_directive_ids(self, content: str) -> frozenset[str]:
        """Extract related directive IDs from ## Related Directives section."""
        section = self._extract_section(content, "## Related Directives")
        if not section:
            return frozenset()

        directive_ids = set()

        # Find patterns like "016:", "Directive 017", etc.
        matches = re.findall(r"\b(\d{3})\b", section)
        directive_ids.update(matches)

        return frozenset(directive_ids)


__all__ = [
    "DirectiveParser",
    "AgentParser",
    "TacticParser",
    "ApproachParser",
]
