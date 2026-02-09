"""
Shared task schema and I/O operations.

This module provides a single source of truth for task file operations,
ensuring consistency across framework orchestration and dashboard modules.

Related ADR:
- ADR-042: Shared Task Domain Model
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import logging

logger = logging.getLogger(__name__)


class TaskSchemaError(Exception):
    """Base exception for task schema operations"""
    pass


class TaskValidationError(TaskSchemaError):
    """Raised when task structure is invalid"""
    pass


class TaskIOError(TaskSchemaError):
    """Raised when task file I/O fails"""
    pass


def read_task(path: Path) -> Dict[str, Any]:
    """
    Read and parse a task file.
    
    Args:
        path: Path to task YAML file
        
    Returns:
        Task dictionary with all fields
        
    Raises:
        TaskIOError: If file cannot be read or parsed
        TaskValidationError: If task structure is invalid
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            task = yaml.safe_load(f)
    except FileNotFoundError:
        raise TaskIOError(f"Task file not found: {path}")
    except yaml.YAMLError as e:
        raise TaskIOError(f"Invalid YAML in {path}: {e}")
    except Exception as e:
        raise TaskIOError(f"Failed to read task {path}: {e}")
    
    if not isinstance(task, dict):
        raise TaskValidationError(f"Task must be a dictionary, got {type(task)}")
    
    # Validate required fields
    required_fields = {'id', 'status'}
    missing_fields = required_fields - set(task.keys())
    if missing_fields:
        raise TaskValidationError(f"Missing required fields: {missing_fields}")
    
    return task


def write_task(path: Path, task: Dict[str, Any]) -> None:
    """
    Write a task to file.
    
    Args:
        path: Path to task YAML file
        task: Task dictionary to write
        
    Raises:
        TaskIOError: If file cannot be written
        TaskValidationError: If task structure is invalid
    """
    if not isinstance(task, dict):
        raise TaskValidationError(f"Task must be a dictionary, got {type(task)}")
    
    # Validate required fields before writing
    required_fields = {'id', 'status'}
    missing_fields = required_fields - set(task.keys())
    if missing_fields:
        raise TaskValidationError(f"Cannot write task with missing fields: {missing_fields}")
    
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(task, f, sort_keys=False, default_flow_style=False)
    except Exception as e:
        raise TaskIOError(f"Failed to write task to {path}: {e}")


def load_task_safe(path: Path) -> Optional[Dict[str, Any]]:
    """
    Safely load a task file, returning None on error.
    
    This is a convenience wrapper for dashboard/monitoring code that
    needs to handle missing or invalid tasks gracefully.
    
    Args:
        path: Path to task YAML file
        
    Returns:
        Task dictionary if successful, None otherwise
    """
    try:
        return read_task(path)
    except TaskSchemaError as e:
        logger.warning(f"Failed to load task {path}: {e}")
        return None
