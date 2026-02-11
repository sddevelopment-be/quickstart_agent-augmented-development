#!/usr/bin/env python3
"""
Bounded Context Independence Tests

Validates architectural boundaries between bounded contexts per ADR-046.
Ensures contexts remain independent and only depend on domain.common.

Implements Architect Alphonso's Recommendation 1 from M5.1 review.

Related ADRs:
    - ADR-046: Domain Module Refactoring
    - ADR-045: Doctrine Concept Domain Model (future)

Directive Compliance:
    - 016 (ATDD): Architectural acceptance criteria as tests
    - 017 (TDD): Test-first for boundary enforcement
    - 018 (Traceable): References ADR-046 architectural decisions
"""

from __future__ import annotations

import glob
from pathlib import Path
import pytest


class TestBoundedContextIndependence:
    """
    Validates that bounded contexts don't import from each other.
    
    Bounded contexts per ADR-046:
    - collaboration: Agent orchestration and task management
    - doctrine: Framework governance (directives, approaches, tactics)
    - specifications: Product planning and feature specs
    - common: Shared utilities (NO domain semantics)
    
    Rule: Contexts may only import from domain.common, not from each other.
    """
    
    def test_collaboration_doesnt_import_from_doctrine(self):
        """
        Collaboration context should not import from doctrine context.
        
        Ensures collaboration (agent orchestration) remains independent
        from doctrine (framework governance).
        """
        collaboration_files = glob.glob("src/domain/collaboration/**/*.py", recursive=True)
        
        for file_path in collaboration_files:
            if "__pycache__" in file_path:
                continue
                
            with open(file_path) as f:
                content = f.read()
                
            assert "from src.domain.doctrine" not in content, \
                f"{file_path} imports from doctrine context (violates bounded context independence)"
            assert "import src.domain.doctrine" not in content, \
                f"{file_path} imports from doctrine context (violates bounded context independence)"
    
    def test_collaboration_doesnt_import_from_specifications(self):
        """
        Collaboration context should not import from specifications context.
        
        Ensures collaboration (agent orchestration) remains independent
        from specifications (product planning).
        """
        collaboration_files = glob.glob("src/domain/collaboration/**/*.py", recursive=True)
        
        for file_path in collaboration_files:
            if "__pycache__" in file_path:
                continue
                
            with open(file_path) as f:
                content = f.read()
                
            assert "from src.domain.specifications" not in content, \
                f"{file_path} imports from specifications context (violates bounded context independence)"
            assert "import src.domain.specifications" not in content, \
                f"{file_path} imports from specifications context (violates bounded context independence)"
    
    def test_doctrine_doesnt_import_from_specifications(self):
        """
        Doctrine context should not import from specifications context.
        
        Ensures doctrine (framework governance) remains independent
        from specifications (product planning).
        """
        doctrine_files = glob.glob("src/domain/doctrine/**/*.py", recursive=True)
        
        for file_path in doctrine_files:
            if "__pycache__" in file_path:
                continue
                
            with open(file_path) as f:
                content = f.read()
                
            assert "from src.domain.specifications" not in content, \
                f"{file_path} imports from specifications context (violates bounded context independence)"
            assert "import src.domain.specifications" not in content, \
                f"{file_path} imports from specifications context (violates bounded context independence)"
    
    def test_contexts_only_import_from_common(self):
        """
        All contexts should only import from domain.common, not each other.
        
        Validates the architectural rule that bounded contexts may only
        share code through domain.common (generic utilities with no
        domain semantics).
        """
        contexts = ["collaboration", "doctrine", "specifications"]
        
        for context in contexts:
            context_files = glob.glob(f"src/domain/{context}/**/*.py", recursive=True)
            
            for file_path in context_files:
                if "__pycache__" in file_path:
                    continue
                    
                with open(file_path) as f:
                    content = f.read()
                
                # Verify no imports from other contexts
                for other_context in contexts:
                    if other_context != context:
                        assert f"from src.domain.{other_context}" not in content, \
                            f"{file_path} imports from {other_context} context (only domain.common allowed)"
                        assert f"import src.domain.{other_context}" not in content, \
                            f"{file_path} imports from {other_context} context (only domain.common allowed)"
                
                # Note: Imports from domain.common are explicitly allowed
                # This is the only permitted cross-context dependency


class TestDomainLayerIsolation:
    """
    Validates that domain layer doesn't import from framework or llm_service.
    
    Ensures domain models remain pure business logic without infrastructure
    dependencies.
    """
    
    def test_domain_doesnt_import_from_framework(self):
        """
        Domain layer should not import from framework layer.
        
        Domain models should be pure business logic, independent of
        orchestration framework.
        """
        domain_files = glob.glob("src/domain/**/*.py", recursive=True)
        
        for file_path in domain_files:
            if "__pycache__" in file_path:
                continue
                
            with open(file_path) as f:
                content = f.read()
                
            assert "from src.framework" not in content, \
                f"{file_path} imports from framework (domain should be framework-independent)"
            assert "import src.framework" not in content, \
                f"{file_path} imports from framework (domain should be framework-independent)"
    
    def test_domain_doesnt_import_from_llm_service(self):
        """
        Domain layer should not import from llm_service layer.
        
        Domain models should be pure business logic, independent of
        LLM service infrastructure.
        """
        domain_files = glob.glob("src/domain/**/*.py", recursive=True)
        
        for file_path in domain_files:
            if "__pycache__" in file_path:
                continue
                
            with open(file_path) as f:
                content = f.read()
                
            assert "from src.llm_service" not in content, \
                f"{file_path} imports from llm_service (domain should be infrastructure-independent)"
            assert "import src.llm_service" not in content, \
                f"{file_path} imports from llm_service (domain should be infrastructure-independent)"


class TestImportPrefixCompliance:
    """
    Validates that all internal imports use src. prefix.
    
    Ensures consistency and prevents import ambiguity.
    """
    
    @pytest.mark.parametrize("module", [
        "domain",
        "framework",
    ])
    def test_no_unprefixed_internal_imports(self, module: str):
        """
        Internal imports should always use src. prefix.
        
        Prevents ambiguous imports and ensures consistency across
        the codebase.
        
        Note: llm_service is allowed to use intra-package imports
        without src. prefix (e.g., from llm_service.config import X).
        """
        # Check all Python files in src/
        all_files = glob.glob("src/**/*.py", recursive=True)
        
        violations = []
        for file_path in all_files:
            if "__pycache__" in file_path or "src/common/" in file_path:
                # Skip cache and deprecation stubs
                continue
            
            # Skip llm_service checking itself (intra-package imports are fine)
            if "src/llm_service/" in file_path and module == "llm_service":
                continue
                
            with open(file_path) as f:
                for line_num, line in enumerate(f, 1):
                    # Check for unprefixed imports (but allow relative imports with .)
                    # OLD: from domain.collaboration import X
                    # NEW: from src.domain.collaboration import X
                    stripped = line.strip()
                    if (stripped.startswith(f"from {module}.") or 
                        stripped.startswith(f"from {module} import") or 
                        stripped.startswith(f"import {module}")):
                        # Exclude relative imports (from .x import y)
                        if not stripped.startswith("from ."):
                            violations.append(f"{file_path}:{line_num}: {line.strip()}")
        
        assert not violations, \
            f"Found {len(violations)} unprefixed imports of '{module}':\n" + \
            "\n".join(violations[:10])  # Show first 10


# Self-documentation: This test file implements Alphonso's Recommendation 1
# from the M5.1 architectural review. It ensures bounded contexts remain
# independent over time, preventing architectural drift.
#
# Future enhancements:
# - Add import-linter integration for CI/CD enforcement
# - Add tests for circular dependency detection
# - Add tests for maximum context size constraints
