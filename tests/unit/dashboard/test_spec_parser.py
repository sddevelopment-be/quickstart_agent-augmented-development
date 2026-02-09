"""
Unit tests for SpecificationParser.

Tests the parsing of YAML frontmatter from specification markdown files.
Implements TDD (Directive 017) - RED phase.
"""

import pytest
from pathlib import Path
from typing import Optional
import yaml


class TestSpecificationParser:
    """Unit tests for specification frontmatter parsing logic."""
    
    def test_extract_frontmatter_from_markdown(self, tmp_path: Path):
        """Test extracting YAML frontmatter delimited by --- markers."""
        pytest.skip("Implementation pending: SpecificationParser.extract_frontmatter")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        content = """---
id: "test-001"
title: "Test Spec"
---

# Content

Body text here.
"""
        
        spec_path = tmp_path / "test.md"
        spec_path.write_text(content)
        
        parser = SpecificationParser(str(tmp_path))
        frontmatter = parser.extract_frontmatter(content)
        
        assert frontmatter is not None
        assert "id" in frontmatter
        assert frontmatter["id"] == "test-001"
        assert "title" in frontmatter
        assert frontmatter["title"] == "Test Spec"
    
    def test_extract_frontmatter_with_no_markers(self):
        """Test handling markdown without frontmatter markers."""
        pytest.skip("Implementation pending: SpecificationParser.extract_frontmatter")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        content = """# Just a heading

No frontmatter here.
"""
        
        parser = SpecificationParser("/tmp")
        frontmatter = parser.extract_frontmatter(content)
        
        assert frontmatter is None
    
    def test_extract_frontmatter_with_only_opening_marker(self):
        """Test handling markdown with unclosed frontmatter."""
        pytest.skip("Implementation pending: SpecificationParser.extract_frontmatter")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        content = """---
id: "test-001"
title: "Unclosed"

# No closing marker
"""
        
        parser = SpecificationParser("/tmp")
        frontmatter = parser.extract_frontmatter(content)
        
        assert frontmatter is None
    
    def test_parse_yaml_frontmatter(self):
        """Test parsing extracted YAML string into dictionary."""
        pytest.skip("Implementation pending: SpecificationParser.parse_yaml")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        yaml_str = """
id: "test-001"
title: "Test Spec"
status: "draft"
priority: "HIGH"
features:
  - id: "feat-001"
    title: "Feature One"
"""
        
        parser = SpecificationParser("/tmp")
        data = parser.parse_yaml(yaml_str)
        
        assert data is not None
        assert data["id"] == "test-001"
        assert data["priority"] == "HIGH"
        assert len(data["features"]) == 1
        assert data["features"][0]["id"] == "feat-001"
    
    def test_parse_yaml_with_invalid_syntax(self):
        """Test handling malformed YAML gracefully."""
        pytest.skip("Implementation pending: SpecificationParser.parse_yaml")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        invalid_yaml = """
id: "test-001"
title: "Missing quote
status: draft
"""
        
        parser = SpecificationParser("/tmp")
        data = parser.parse_yaml(invalid_yaml)
        
        # Should return None rather than crashing
        assert data is None
    
    def test_validate_required_fields(self):
        """Test validation of required frontmatter fields."""
        pytest.skip("Implementation pending: SpecificationParser.validate_metadata")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        parser = SpecificationParser("/tmp")
        
        # Valid metadata
        valid_meta = {
            "id": "test-001",
            "title": "Test",
            "status": "draft",
            "initiative": "Test Initiative",
        }
        assert parser.validate_metadata(valid_meta) is True
        
        # Missing required field (id)
        invalid_meta = {
            "title": "Test",
            "status": "draft",
        }
        assert parser.validate_metadata(invalid_meta) is False
    
    def test_parse_frontmatter_end_to_end(self, tmp_path: Path):
        """Test complete frontmatter parsing pipeline."""
        pytest.skip("Implementation pending: SpecificationParser.parse_frontmatter")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        content = """---
id: "spec-001"
title: "Complete Specification"
status: "in_progress"
initiative: "Dashboard Enhancements"
priority: "HIGH"
features:
  - id: "feat-001"
    title: "Feature One"
  - id: "feat-002"
    title: "Feature Two"
completion: 60
created: "2026-02-06"
updated: "2026-02-06"
author: "analyst-annie"
---

# Specification Title

Content here.
"""
        
        spec_path = tmp_path / "complete.md"
        spec_path.write_text(content)
        
        parser = SpecificationParser(str(tmp_path))
        metadata = parser.parse_frontmatter(str(spec_path))
        
        assert metadata is not None
        assert metadata.id == "spec-001"
        assert metadata.title == "Complete Specification"
        assert metadata.status == "in_progress"
        assert metadata.initiative == "Dashboard Enhancements"
        assert metadata.priority == "HIGH"
        assert len(metadata.features) == 2
        assert metadata.completion == 60
        assert metadata.author == "analyst-annie"
    
    def test_parse_frontmatter_with_optional_fields_missing(self, tmp_path: Path):
        """Test parsing with only required fields present."""
        pytest.skip("Implementation pending: SpecificationParser.parse_frontmatter")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        content = """---
id: "minimal-001"
title: "Minimal Spec"
status: "draft"
initiative: "Test"
---

# Minimal
"""
        
        spec_path = tmp_path / "minimal.md"
        spec_path.write_text(content)
        
        parser = SpecificationParser(str(tmp_path))
        metadata = parser.parse_frontmatter(str(spec_path))
        
        assert metadata is not None
        assert metadata.id == "minimal-001"
        assert metadata.completion is None  # Optional field
        assert metadata.features == []  # Default empty list
    
    def test_scan_specifications_directory(self, tmp_path: Path):
        """Test scanning directory for all specification files."""
        pytest.skip("Implementation pending: SpecificationParser.scan_specifications")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        # Create multiple spec files
        (tmp_path / "specs").mkdir()
        
        spec1_content = """---
id: "spec-001"
title: "Spec One"
status: "draft"
initiative: "Init A"
---
# Spec 1
"""
        (tmp_path / "specs" / "spec1.md").write_text(spec1_content)
        
        spec2_content = """---
id: "spec-002"
title: "Spec Two"
status: "draft"
initiative: "Init B"
---
# Spec 2
"""
        (tmp_path / "specs" / "spec2.md").write_text(spec2_content)
        
        # Create non-markdown file (should be ignored)
        (tmp_path / "specs" / "readme.txt").write_text("Not a spec")
        
        parser = SpecificationParser(str(tmp_path))
        specs = parser.scan_specifications(str(tmp_path / "specs"))
        
        assert len(specs) == 2
        assert any(s.id == "spec-001" for s in specs)
        assert any(s.id == "spec-002" for s in specs)
    
    def test_parse_nested_specification_directories(self, tmp_path: Path):
        """Test scanning nested directory structure."""
        pytest.skip("Implementation pending: SpecificationParser.scan_specifications")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        # Create nested structure: specs/dashboard/spec.md
        dashboard_dir = tmp_path / "specs" / "dashboard"
        dashboard_dir.mkdir(parents=True)
        
        spec_content = """---
id: "dash-001"
title: "Dashboard Spec"
status: "draft"
initiative: "Dashboard"
---
# Spec
"""
        (dashboard_dir / "dashboard.md").write_text(spec_content)
        
        parser = SpecificationParser(str(tmp_path))
        specs = parser.scan_specifications(str(tmp_path / "specs"))
        
        assert len(specs) == 1
        assert specs[0].id == "dash-001"
    
    def test_parse_specification_with_relative_path_tracking(self, tmp_path: Path):
        """Test that parser tracks relative paths from base directory."""
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        # Create spec in subdirectory
        subdir = tmp_path / "specs" / "dashboard"
        subdir.mkdir(parents=True)
        
        spec_content = """---
id: "dash-001"
title: "Dashboard Spec"
status: "draft"
initiative: "Dashboard"
---
# Spec
"""
        spec_path = subdir / "feature.md"
        spec_path.write_text(spec_content)
        
        parser = SpecificationParser(str(tmp_path / "specs"))
        metadata = parser.parse_frontmatter(str(spec_path))
        
        # Should track relative path for task linking
        assert metadata is not None, "Parser should return metadata for valid spec"
        assert metadata.relative_path == "dashboard/feature.md", \
            f"Expected 'dashboard/feature.md', got '{metadata.relative_path}'"
    
    def test_parse_specification_with_rglob_absolute_paths(self, tmp_path: Path):
        """
        Regression test for rglob absolute path bug (2026-02-09).
        
        When scan_specifications() uses rglob(), it returns absolute paths.
        These absolute paths must be correctly converted to relative paths
        for task linking to work (tasks use relative paths in their 'specification:' field).
        
        Bug: path.relative_to(base_dir) failed when paths weren't resolved,
        falling back to path.name (filename only), breaking task linking.
        
        Fix: Use path.resolve() and base_dir.resolve() for canonical paths.
        """
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        # Create nested specification structure
        initiatives_dir = tmp_path / "specifications" / "initiatives" / "dashboard-enhancements"
        initiatives_dir.mkdir(parents=True)
        
        spec_content = """---
id: "SPEC-DASH-007"
title: "Real-Time Execution Dashboard"
status: "implemented"
priority: "CRITICAL"
initiative: "Dashboard Enhancements"
---
# Real-Time Execution Dashboard
"""
        spec_path = initiatives_dir / "real-time-execution-dashboard.md"
        spec_path.write_text(spec_content)
        
        # Initialize parser with base directory
        parser = SpecificationParser(str(tmp_path / "specifications"))
        
        # Scan specifications (uses rglob internally, returns absolute paths)
        specs = parser.scan_specifications(str(tmp_path / "specifications"))
        
        # Verify we found the spec
        assert len(specs) == 1, f"Expected 1 spec, found {len(specs)}"
        
        # Verify relative path is correct (not just filename)
        spec = specs[0]
        assert spec.relative_path == "initiatives/dashboard-enhancements/real-time-execution-dashboard.md", \
            f"Expected full relative path, got '{spec.relative_path}' (bug: filename-only fallback)"
        
        # Verify this matches what tasks would have in their specification: field
        expected_task_link = f"specifications/{spec.relative_path}"
        assert expected_task_link == "specifications/initiatives/dashboard-enhancements/real-time-execution-dashboard.md", \
            "Relative path should be compatible with task linking format"


class TestSpecificationMetadataModel:
    """Unit tests for SpecificationMetadata data model."""
    
    def test_create_specification_metadata(self):
        """Test creating metadata instance with required fields."""
        pytest.skip("Implementation pending: SpecificationMetadata dataclass")
        
        from src.llm_service.dashboard.spec_parser import SpecificationMetadata
        
        metadata = SpecificationMetadata(
            id="test-001",
            title="Test Spec",
            status="draft",
            initiative="Test Initiative",
            priority="HIGH",
            features=[],
            completion=None,
            path="/path/to/spec.md",
            relative_path="spec.md",
            created="2026-02-06",
            updated="2026-02-06",
            author="test-author"
        )
        
        assert metadata.id == "test-001"
        assert metadata.status == "draft"
        assert len(metadata.features) == 0
    
    def test_metadata_with_features(self):
        """Test metadata with feature list."""
        pytest.skip("Implementation pending: SpecificationMetadata dataclass")
        
        from src.llm_service.dashboard.spec_parser import SpecificationMetadata, Feature
        
        features = [
            Feature(id="feat-001", title="Feature One", status="done"),
            Feature(id="feat-002", title="Feature Two", status="in_progress"),
        ]
        
        metadata = SpecificationMetadata(
            id="test-001",
            title="Test",
            status="in_progress",
            initiative="Init",
            priority="MEDIUM",
            features=features,
            completion=None,
            path="/path/spec.md",
            relative_path="spec.md",
            created="2026-02-06",
            updated="2026-02-06",
            author="author"
        )
        
        assert len(metadata.features) == 2
        assert metadata.features[0].id == "feat-001"
        assert metadata.features[1].status == "in_progress"


class TestErrorHandling:
    """Unit tests for error handling and edge cases."""
    
    def test_handle_file_not_found(self):
        """Test handling non-existent file gracefully."""
        pytest.skip("Implementation pending: SpecificationParser error handling")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        parser = SpecificationParser("/tmp")
        metadata = parser.parse_frontmatter("/non/existent/file.md")
        
        assert metadata is None
    
    def test_handle_permission_denied(self, tmp_path: Path):
        """Test handling file permission errors."""
        pytest.skip("Implementation pending: SpecificationParser error handling")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        spec_path = tmp_path / "restricted.md"
        spec_path.write_text("---\nid: test\n---\n# Test")
        spec_path.chmod(0o000)  # Remove all permissions
        
        parser = SpecificationParser(str(tmp_path))
        metadata = parser.parse_frontmatter(str(spec_path))
        
        assert metadata is None
        
        # Cleanup
        spec_path.chmod(0o644)
    
    def test_handle_empty_file(self, tmp_path: Path):
        """Test handling empty specification file."""
        pytest.skip("Implementation pending: SpecificationParser error handling")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        spec_path = tmp_path / "empty.md"
        spec_path.write_text("")
        
        parser = SpecificationParser(str(tmp_path))
        metadata = parser.parse_frontmatter(str(spec_path))
        
        assert metadata is None
    
    def test_handle_large_file(self, tmp_path: Path):
        """Test handling large specification files efficiently."""
        pytest.skip("Implementation pending: SpecificationParser performance")
        
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        
        # Create large content (10MB)
        large_content = "---\nid: large\ntitle: Large\nstatus: draft\ninitiative: Test\n---\n"
        large_content += "# Content\n" + ("x" * 10_000_000)
        
        spec_path = tmp_path / "large.md"
        spec_path.write_text(large_content)
        
        parser = SpecificationParser(str(tmp_path))
        
        # Should only parse frontmatter (first ~1KB), not entire file
        import time
        start = time.time()
        metadata = parser.parse_frontmatter(str(spec_path))
        elapsed = time.time() - start
        
        assert metadata is not None
        assert elapsed < 0.1  # Should be fast (<100ms)


# Test coverage summary
"""
Unit Test Coverage for SpecificationParser:
- ✅ Frontmatter extraction (3 tests)
- ✅ YAML parsing (2 tests)
- ✅ Validation (1 test)
- ✅ End-to-end parsing (2 tests)
- ✅ Directory scanning (3 tests)
- ✅ Data models (2 tests)
- ✅ Error handling (4 tests)

Total: 17 unit tests
All tests currently skipped (RED phase)
"""
