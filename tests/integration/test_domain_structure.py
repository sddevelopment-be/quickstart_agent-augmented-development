"""
Acceptance tests for ADR-046 Task 1: Domain Directory Structure.

Tests verify that the domain module structure conforms to ADR-046 specifications.

Related:
- ADR-046: Domain Module Refactoring
- Task: 2026-02-11T0900-adr046-task1-domain-structure
"""

import importlib
import sys
from pathlib import Path

import pytest


class TestDomainStructureExists:
    """Verify domain directory structure exists per ADR-046."""

    def test_domain_directory_exists(self):
        """Domain root directory must exist."""
        domain_path = Path("src/domain")
        assert domain_path.exists(), "src/domain/ directory must exist"
        assert domain_path.is_dir(), "src/domain/ must be a directory"

    def test_bounded_context_directories_exist(self):
        """All four bounded context directories must exist."""
        expected_contexts = [
            "collaboration",
            "doctrine", 
            "specifications",
            "common"
        ]
        
        for context in expected_contexts:
            context_path = Path(f"src/domain/{context}")
            assert context_path.exists(), f"src/domain/{context}/ must exist"
            assert context_path.is_dir(), f"src/domain/{context}/ must be a directory"


class TestDomainInitFiles:
    """Verify all __init__.py files exist with proper content."""

    def test_domain_root_init_exists(self):
        """Domain root must have __init__.py."""
        init_path = Path("src/domain/__init__.py")
        assert init_path.exists(), "src/domain/__init__.py must exist"
        assert init_path.is_file(), "src/domain/__init__.py must be a file"

    def test_domain_root_init_has_docstring(self):
        """Domain root __init__.py must have module docstring."""
        with open("src/domain/__init__.py", "r") as f:
            content = f.read()
        
        # Must have triple-quoted docstring
        assert '"""' in content or "'''" in content, \
            "src/domain/__init__.py must contain a module docstring"

    def test_collaboration_init_exists(self):
        """Collaboration bounded context must have __init__.py."""
        init_path = Path("src/domain/collaboration/__init__.py")
        assert init_path.exists(), "src/domain/collaboration/__init__.py must exist"

    def test_collaboration_init_has_docstring(self):
        """Collaboration __init__.py must explain bounded context purpose."""
        with open("src/domain/collaboration/__init__.py", "r") as f:
            content = f.read()
        
        assert '"""' in content or "'''" in content, \
            "collaboration/__init__.py must have docstring"
        
        # Check for key concept keywords
        content_lower = content.lower()
        assert any(keyword in content_lower for keyword in [
            "agent", "task", "orchestration", "collaboration", "batch"
        ]), "collaboration/__init__.py docstring must explain bounded context"

    def test_doctrine_init_exists(self):
        """Doctrine bounded context must have __init__.py."""
        init_path = Path("src/domain/doctrine/__init__.py")
        assert init_path.exists(), "src/domain/doctrine/__init__.py must exist"

    def test_doctrine_init_has_docstring(self):
        """Doctrine __init__.py must explain bounded context purpose."""
        with open("src/domain/doctrine/__init__.py", "r") as f:
            content = f.read()
        
        assert '"""' in content or "'''" in content, \
            "doctrine/__init__.py must have docstring"
        
        content_lower = content.lower()
        assert any(keyword in content_lower for keyword in [
            "directive", "approach", "tactic", "doctrine", "profile"
        ]), "doctrine/__init__.py docstring must explain bounded context"

    def test_specifications_init_exists(self):
        """Specifications bounded context must have __init__.py."""
        init_path = Path("src/domain/specifications/__init__.py")
        assert init_path.exists(), "src/domain/specifications/__init__.py must exist"

    def test_specifications_init_has_docstring(self):
        """Specifications __init__.py must explain bounded context purpose."""
        with open("src/domain/specifications/__init__.py", "r") as f:
            content = f.read()
        
        assert '"""' in content or "'''" in content, \
            "specifications/__init__.py must have docstring"
        
        content_lower = content.lower()
        assert any(keyword in content_lower for keyword in [
            "specification", "feature", "initiative", "portfolio"
        ]), "specifications/__init__.py docstring must explain bounded context"

    def test_common_init_exists(self):
        """Common utilities bounded context must have __init__.py."""
        init_path = Path("src/domain/common/__init__.py")
        assert init_path.exists(), "src/domain/common/__init__.py must exist"

    def test_common_init_has_docstring(self):
        """Common __init__.py must explain bounded context purpose."""
        with open("src/domain/common/__init__.py", "r") as f:
            content = f.read()
        
        assert '"""' in content or "'''" in content, \
            "common/__init__.py must have docstring"
        
        content_lower = content.lower()
        assert any(keyword in content_lower for keyword in [
            "utility", "utilities", "generic", "shared", "validation"
        ]), "common/__init__.py docstring must explain bounded context"


class TestDomainDocumentation:
    """Verify domain module documentation exists."""

    def test_domain_readme_exists(self):
        """src/domain/README.md must exist."""
        readme_path = Path("src/domain/README.md")
        assert readme_path.exists(), "src/domain/README.md must exist"
        assert readme_path.is_file(), "src/domain/README.md must be a file"

    def test_domain_readme_explains_bounded_contexts(self):
        """README must explain all four bounded contexts."""
        with open("src/domain/README.md", "r") as f:
            content = f.read()
        
        # Must mention all bounded contexts
        assert "collaboration" in content.lower(), \
            "README must explain collaboration bounded context"
        assert "doctrine" in content.lower(), \
            "README must explain doctrine bounded context"
        assert "specifications" in content.lower(), \
            "README must explain specifications bounded context"
        assert "common" in content.lower(), \
            "README must explain common utilities"

    def test_domain_readme_references_adrs(self):
        """README must reference relevant ADRs."""
        with open("src/domain/README.md", "r") as f:
            content = f.read()
        
        # Must reference ADR-046
        assert "ADR-046" in content or "ADR 046" in content, \
            "README must reference ADR-046"


class TestDomainImportability:
    """Verify domain modules can be imported without errors."""

    def test_can_import_domain_package(self):
        """Domain package must be importable."""
        try:
            import src.domain
            importlib.reload(src.domain)
        except Exception as e:
            pytest.fail(f"Failed to import src.domain: {e}")

    def test_can_import_collaboration(self):
        """Collaboration bounded context must be importable."""
        try:
            import src.domain.collaboration
            importlib.reload(src.domain.collaboration)
        except Exception as e:
            pytest.fail(f"Failed to import src.domain.collaboration: {e}")

    def test_can_import_doctrine(self):
        """Doctrine bounded context must be importable."""
        try:
            import src.domain.doctrine
            importlib.reload(src.domain.doctrine)
        except Exception as e:
            pytest.fail(f"Failed to import src.domain.doctrine: {e}")

    def test_can_import_specifications(self):
        """Specifications bounded context must be importable."""
        try:
            import src.domain.specifications
            importlib.reload(src.domain.specifications)
        except Exception as e:
            pytest.fail(f"Failed to import src.domain.specifications: {e}")

    def test_can_import_common(self):
        """Common utilities must be importable."""
        try:
            import src.domain.common
            importlib.reload(src.domain.common)
        except Exception as e:
            pytest.fail(f"Failed to import src.domain.common: {e}")


class TestExistingCodePreserved:
    """Verify existing src/common/ is unchanged (MUST NOT requirement)."""

    def test_src_common_still_exists(self):
        """Existing src/common/ directory must remain unchanged."""
        common_path = Path("src/common")
        assert common_path.exists(), \
            "src/common/ must still exist (Task 2 handles migration)"
        assert common_path.is_dir(), "src/common/ must be a directory"

    def test_src_common_files_unchanged(self):
        """Existing files in src/common/ must remain."""
        expected_files = [
            "src/common/__init__.py",
            "src/common/agent_loader.py",
            "src/common/task_schema.py",
            "src/common/types.py"
        ]
        
        for file_path in expected_files:
            assert Path(file_path).exists(), \
                f"{file_path} must still exist (not moved yet)"
