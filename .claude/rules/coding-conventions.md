<!-- Source: python-conventions.md -->
# Coding Conventions

**Version:** 1.0.0  
**Last Updated:** 2026-02-08  
**Status:** Active


## Purpose

This document captures Python coding conventions and best practices for agent-augmented development. These guidelines ensure consistency, readability, and maintainability across Python codebases, with special emphasis on test quality and validation patterns.


## Table of Contents

1. [Formatting & Style](#formatting--style)
2. [Test Structure (Quad-A Pattern)](#test-structure-quad-a-pattern)
3. [Validation & Guard Clauses](#validation--guard-clauses)
4. [Type Hints](#type-hints)
5. [String Formatting](#string-formatting)
6. [Testing Pyramid](#testing-pyramid)
7. [Tooling](#tooling)


## Formatting & Style {#formatting--style}

### Use Black for Consistent Formatting

**Tool:** `black` (version 25.11.0+)

**Command:**
```bash
python -m black path/to/file.py
```

**What Black Handles:**
- Line length (88 characters default)
- Consistent spacing around operators
- String quote normalization (prefer double quotes)
- Trailing commas in multi-line structures
- Blank line management

**Example:**
```python
def function(arg1,arg2,arg3):
    return{
        'key1':arg1,'key2':arg2,
        'key3':arg3
    }

def function(arg1, arg2, arg3):
    return {
        "key1": arg1,
        "key2": arg2,
        "key3": arg3,
    }
```

### Use Ruff for Linting

**Tool:** `ruff` (version 0.14.7+)

**Command:**
```bash
python -m ruff check path/to/file.py --fix
```

**What Ruff Catches:**
- Unused imports
- Undefined variables
- Code quality issues
- Common anti-patterns
- PEP 8 violations


## Test Structure (Quad-A Pattern) {#test-structure-quad-a-pattern}

### The Correct Quad-A Structure
