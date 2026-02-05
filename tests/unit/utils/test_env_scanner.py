"""
Unit Tests for Environment Scanner (TDD)

Following TDD (Directive 017), write tests first.

Test Coverage:
- API key detection in environment
- Binary path detection
- Platform detection
- Complete environment scan
- Helpful error/warning messages
"""

import pytest
import os
import platform
from pathlib import Path
from unittest.mock import patch, MagicMock

from llm_service.utils.env_scanner import EnvironmentScanner


class TestAPIKeyDetection:
    """Test API key detection in environment"""
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'sk-ant-test123'})
    def test_detects_anthropic_api_key(self):
        """Should detect ANTHROPIC_API_KEY when present"""
        scanner = EnvironmentScanner()
        keys = scanner.scan_api_keys()
        
        assert 'ANTHROPIC_API_KEY' in keys
        assert keys['ANTHROPIC_API_KEY'] is True
    
    @patch.dict(os.environ, {}, clear=True)
    def test_reports_missing_anthropic_key(self):
        """Should report ANTHROPIC_API_KEY as missing"""
        scanner = EnvironmentScanner()
        keys = scanner.scan_api_keys()
        
        assert 'ANTHROPIC_API_KEY' in keys
        assert keys['ANTHROPIC_API_KEY'] is False
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'sk-test456'})
    def test_detects_openai_api_key(self):
        """Should detect OPENAI_API_KEY when present"""
        scanner = EnvironmentScanner()
        keys = scanner.scan_api_keys()
        
        assert 'OPENAI_API_KEY' in keys
        assert keys['OPENAI_API_KEY'] is True
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'AIza-test789'})
    def test_detects_google_api_key(self):
        """Should detect GOOGLE_API_KEY when present"""
        scanner = EnvironmentScanner()
        keys = scanner.scan_api_keys()
        
        assert 'GOOGLE_API_KEY' in keys
        assert keys['GOOGLE_API_KEY'] is True
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'key1',
        'OPENAI_API_KEY': 'key2',
        'GOOGLE_API_KEY': 'key3'
    })
    def test_detects_multiple_keys(self):
        """Should detect multiple API keys simultaneously"""
        scanner = EnvironmentScanner()
        keys = scanner.scan_api_keys()
        
        assert keys['ANTHROPIC_API_KEY'] is True
        assert keys['OPENAI_API_KEY'] is True
        assert keys['GOOGLE_API_KEY'] is True


class TestBinaryDetection:
    """Test tool binary detection in PATH"""
    
    @patch('shutil.which', return_value='/usr/local/bin/claude')
    def test_finds_binary_in_path(self, mock_which):
        """Should find binary when in PATH"""
        scanner = EnvironmentScanner()
        result = scanner.find_binary('claude')
        
        assert result is not None
        assert result == Path('/usr/local/bin/claude')
        mock_which.assert_called_once_with('claude')
    
    @patch('shutil.which', return_value=None)
    def test_returns_none_when_binary_missing(self, mock_which):
        """Should return None when binary not found"""
        scanner = EnvironmentScanner()
        result = scanner.find_binary('nonexistent-binary')
        
        assert result is None
    
    @patch('shutil.which', side_effect=[
        '/usr/local/bin/claude',
        '/usr/bin/openai',
        None
    ])
    def test_finds_multiple_binaries(self, mock_which):
        """Should detect multiple binaries"""
        scanner = EnvironmentScanner()
        
        claude = scanner.find_binary('claude')
        openai = scanner.find_binary('openai')
        missing = scanner.find_binary('missing')
        
        assert claude == Path('/usr/local/bin/claude')
        assert openai == Path('/usr/bin/openai')
        assert missing is None


class TestPlatformDetection:
    """Test OS platform detection"""
    
    @patch('platform.system', return_value='Linux')
    def test_detects_linux_platform(self, mock_system):
        """Should detect Linux platform"""
        scanner = EnvironmentScanner()
        platform_name = scanner.detect_platform()
        
        assert platform_name == 'linux'
    
    @patch('platform.system', return_value='Darwin')
    def test_detects_macos_platform(self, mock_system):
        """Should detect macOS (Darwin) platform"""
        scanner = EnvironmentScanner()
        platform_name = scanner.detect_platform()
        
        assert platform_name == 'darwin'
    
    @patch('platform.system', return_value='Windows')
    def test_detects_windows_platform(self, mock_system):
        """Should detect Windows platform"""
        scanner = EnvironmentScanner()
        platform_name = scanner.detect_platform()
        
        assert platform_name == 'windows'
    
    @patch('platform.system', return_value='UnknownOS')
    def test_handles_unknown_platform(self, mock_system):
        """Should handle unknown OS gracefully"""
        scanner = EnvironmentScanner()
        platform_name = scanner.detect_platform()
        
        # Should default to linux
        assert platform_name == 'linux'


class TestCompleteScan:
    """Test complete environment scan"""
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('shutil.which', return_value='/usr/local/bin/claude')
    @patch('platform.system', return_value='Linux')
    def test_complete_scan_returns_all_info(
        self,
        mock_system,
        mock_which,
    ):
        """Should return complete environment information"""
        scanner = EnvironmentScanner()
        result = scanner.scan_all()
        
        assert 'api_keys' in result
        assert 'binaries' in result
        assert 'platform' in result
        
        assert result['platform'] == 'linux'
        assert result['api_keys']['ANTHROPIC_API_KEY'] is True
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('shutil.which', return_value=None)
    def test_scan_all_with_missing_dependencies(self, mock_which):
        """Should report missing dependencies in scan"""
        scanner = EnvironmentScanner()
        result = scanner.scan_all()
        
        # All API keys should be missing
        for key, present in result['api_keys'].items():
            assert present is False


class TestScannedToolsDict:
    """Test getting scanned tools as dict"""
    
    @patch('shutil.which', side_effect=lambda name: {
        'claude': '/usr/local/bin/claude',
        'openai': '/usr/bin/openai',
    }.get(name))
    def test_scan_common_tools(self, mock_which):
        """Should scan for common LLM tool binaries"""
        scanner = EnvironmentScanner()
        result = scanner.scan_all()
        
        binaries = result['binaries']
        assert 'claude' in binaries or 'claude-code' in binaries


class TestScannerMethods:
    """Test scanner helper methods"""
    
    def test_is_api_key_valid_checks_presence(self):
        """Should validate if API key is present and non-empty"""
        scanner = EnvironmentScanner()
        
        with patch.dict(os.environ, {'TEST_KEY': 'valid-key'}):
            assert scanner.is_api_key_valid('TEST_KEY')
        
        with patch.dict(os.environ, {'TEST_KEY': ''}):
            assert not scanner.is_api_key_valid('TEST_KEY')
        
        with patch.dict(os.environ, {}, clear=True):
            assert not scanner.is_api_key_valid('TEST_KEY')
    
    @patch('shutil.which', side_effect=lambda name: '/usr/bin/tool' if name == 'tool' else None)
    def test_check_binary_exists(self, mock_which):
        """Should check if binary exists in PATH"""
        scanner = EnvironmentScanner()
        
        assert scanner.check_binary_exists('tool')
        assert not scanner.check_binary_exists('missing-tool')


# pytest markers
pytestmark = [
    pytest.mark.unit,
    pytest.mark.tdd,
]
