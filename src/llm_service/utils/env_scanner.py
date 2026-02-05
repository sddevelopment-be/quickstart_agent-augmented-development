"""
Environment Scanner for Configuration Generation

Scans the system environment to detect:
- API keys in environment variables
- Tool binaries in PATH
- Operating system platform

Implements ADR-031: Template-Based Configuration Generation

Usage:
    scanner = EnvironmentScanner()
    env_info = scanner.scan_all()
    
    if env_info['api_keys']['ANTHROPIC_API_KEY']:
        print("Claude API key detected")
"""

import os
import shutil
import platform
from pathlib import Path
from typing import Dict, Optional, List, Any


class EnvironmentScanner:
    """
    Scans system environment for LLM service dependencies.
    
    Detects:
    - API keys (ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY)
    - Tool binaries in PATH
    - Operating system platform
    """
    
    # API keys to check
    COMMON_API_KEYS = [
        'ANTHROPIC_API_KEY',
        'OPENAI_API_KEY',
        'GOOGLE_API_KEY',
    ]
    
    # Common tool binaries to search for
    COMMON_TOOLS = [
        'claude',
        'claude-code',
        'openai',
        'gpt',
    ]
    
    def __init__(self):
        """Initialize environment scanner."""
        pass
    
    def scan_api_keys(self) -> Dict[str, bool]:
        """
        Scan for API keys in environment variables.
        
        Returns:
            Dictionary mapping API key names to presence (True/False)
        """
        api_keys = {}
        for key in self.COMMON_API_KEYS:
            api_keys[key] = self.is_api_key_valid(key)
        return api_keys
    
    def is_api_key_valid(self, key_name: str) -> bool:
        """
        Check if API key is present and non-empty.
        
        Args:
            key_name: Environment variable name
        
        Returns:
            True if key exists and is non-empty
        """
        value = os.environ.get(key_name, '')
        return bool(value and len(value.strip()) > 0)
    
    def find_binary(self, binary_name: str) -> Optional[Path]:
        """
        Find binary in system PATH.
        
        Args:
            binary_name: Name of binary to find
        
        Returns:
            Path to binary if found, None otherwise
        """
        path = shutil.which(binary_name)
        return Path(path) if path else None
    
    def check_binary_exists(self, binary_name: str) -> bool:
        """
        Check if binary exists in PATH.
        
        Args:
            binary_name: Name of binary to check
        
        Returns:
            True if binary found in PATH
        """
        return self.find_binary(binary_name) is not None
    
    def detect_platform(self) -> str:
        """
        Detect operating system platform.
        
        Returns:
            Platform name: 'linux', 'darwin' (macOS), 'windows', or 'linux' (default)
        """
        system = platform.system().lower()
        
        # Map to standard names
        platform_map = {
            'linux': 'linux',
            'darwin': 'darwin',  # macOS
            'windows': 'windows',
        }
        
        return platform_map.get(system, 'linux')  # Default to linux
    
    def scan_binaries(self) -> Dict[str, Optional[Path]]:
        """
        Scan for common tool binaries.
        
        Returns:
            Dictionary mapping tool names to their paths (or None if not found)
        """
        binaries = {}
        for tool in self.COMMON_TOOLS:
            binaries[tool] = self.find_binary(tool)
        return binaries
    
    def scan_all(self) -> Dict[str, Any]:
        """
        Perform complete environment scan.
        
        Returns:
            Dictionary with 'api_keys', 'binaries', and 'platform' information
        """
        return {
            'api_keys': self.scan_api_keys(),
            'binaries': self.scan_binaries(),
            'platform': self.detect_platform(),
        }
    
    def get_missing_api_keys(self) -> List[str]:
        """
        Get list of missing API keys.
        
        Returns:
            List of API key names that are not set
        """
        api_keys = self.scan_api_keys()
        return [key for key, present in api_keys.items() if not present]
    
    def get_available_tools(self) -> List[str]:
        """
        Get list of available tool binaries.
        
        Returns:
            List of tool names that were found in PATH
        """
        binaries = self.scan_binaries()
        return [tool for tool, path in binaries.items() if path is not None]
    
    def generate_context_for_template(self) -> Dict[str, Any]:
        """
        Generate context dictionary for template substitution.
        
        Returns context with detected binary paths and platform info.
        
        Returns:
            Dictionary suitable for Jinja2 template context
        """
        binaries = self.scan_binaries()
        platform_name = self.detect_platform()
        
        context = {
            'platform': platform_name,
        }
        
        # Add binary paths to context
        if binaries.get('claude'):
            context['claude_binary'] = str(binaries['claude'])
        if binaries.get('openai'):
            context['openai_binary'] = str(binaries['openai'])
        
        return context


__all__ = ['EnvironmentScanner']
