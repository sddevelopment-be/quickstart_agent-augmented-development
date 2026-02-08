"""Tests for framework.interface module.

Tests the user-facing utilities and shorthand entry points (Layer 0).

References:
    - docs/styleguides/python_conventions.md (Quad-A pattern)
    - framework/interface/
"""

from pathlib import Path

import pytest

from framework.interface import FrameworkClient, create_client


class TestFrameworkClient:
    """Test suite for FrameworkClient class."""

    def test_init_default_values(self) -> None:
        """Test client initialization with default values."""
        # Arrange & Act
        client = FrameworkClient()

        # Assert
        assert client.mode == "analysis"
        assert client.config_path == Path(".github/agents/config.yaml")
        assert not client._initialized

    def test_init_custom_values(self, tmp_path: Path) -> None:
        """Test client initialization with custom values."""
        # Arrange
        custom_config = tmp_path / "custom_config.yaml"
        custom_config.touch()

        # Act
        client = FrameworkClient(config_path=custom_config, mode="creative")

        # Assert
        assert client.mode == "creative"
        assert client.config_path == custom_config
        assert not client._initialized

    def test_init_invalid_mode_raises_error(self) -> None:
        """Test initialization with invalid mode raises ValueError."""
        # Arrange
        invalid_mode = "invalid_mode"

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FrameworkClient(mode=invalid_mode)

        assert "Invalid mode" in str(exc_info.value)
        assert invalid_mode in str(exc_info.value)

    def test_initialize_missing_config_raises_error(self, tmp_path: Path) -> None:
        """Test initialize raises FileNotFoundError when config missing."""
        # Arrange
        missing_config = tmp_path / "nonexistent.yaml"
        client = FrameworkClient(config_path=missing_config)

        # Assumption Check
        assert not missing_config.exists(), (
            "Test precondition failed: config should NOT exist"
        )

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            client.initialize()

        assert str(missing_config) in str(exc_info.value)

    def test_initialize_valid_config_succeeds(self, tmp_path: Path) -> None:
        """Test initialize succeeds with valid config file."""
        # Arrange
        config_file = tmp_path / "config.yaml"
        config_file.write_text("# Minimal config\n")
        client = FrameworkClient(config_path=config_file)

        # Assumption Check
        assert config_file.exists(), "Test precondition failed: config should exist"

        # Act
        client.initialize()

        # Assert
        assert client._initialized

    def test_execute_task_not_initialized_raises_error(
        self, tmp_path: Path
    ) -> None:
        """Test execute_task raises RuntimeError when not initialized."""
        # Arrange
        client = FrameworkClient()
        task_path = tmp_path / "task.yaml"
        task_path.touch()

        # Assumption Check
        assert not client._initialized, (
            "Test precondition failed: client should NOT be initialized"
        )

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            client.execute_task(task_path)

        assert "not initialized" in str(exc_info.value).lower()

    def test_execute_task_missing_file_raises_error(self, tmp_path: Path) -> None:
        """Test execute_task raises FileNotFoundError when task missing."""
        # Arrange
        config_file = tmp_path / "config.yaml"
        config_file.write_text("# Config\n")
        client = FrameworkClient(config_path=config_file)
        client.initialize()

        missing_task = tmp_path / "missing.yaml"

        # Assumption Check
        assert not missing_task.exists(), (
            "Test precondition failed: task file should NOT exist"
        )

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            client.execute_task(missing_task)

        assert str(missing_task) in str(exc_info.value)

    def test_execute_task_returns_result_dict(self, tmp_path: Path) -> None:
        """Test execute_task returns result dictionary for valid task."""
        # Arrange
        config_file = tmp_path / "config.yaml"
        config_file.write_text("# Config\n")
        task_file = tmp_path / "task.yaml"
        task_file.write_text("id: test-task\ntitle: Test\n")

        client = FrameworkClient(config_path=config_file)
        client.initialize()

        # Assumption Check
        assert client._initialized, (
            "Test precondition failed: client should be initialized"
        )
        assert task_file.exists(), (
            "Test precondition failed: task file should exist"
        )

        # Act
        result = client.execute_task(task_file)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "task_path" in result

    def test_list_available_models_not_initialized_raises_error(self) -> None:
        """Test list_available_models raises RuntimeError when not initialized."""
        # Arrange
        client = FrameworkClient()

        # Assumption Check
        assert not client._initialized, (
            "Test precondition failed: client should NOT be initialized"
        )

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            client.list_available_models()

        assert "not initialized" in str(exc_info.value).lower()

    def test_list_available_models_returns_list(self, tmp_path: Path) -> None:
        """Test list_available_models returns list when initialized."""
        # Arrange
        config_file = tmp_path / "config.yaml"
        config_file.write_text("# Config\n")
        client = FrameworkClient(config_path=config_file)
        client.initialize()

        # Assumption Check
        assert client._initialized, (
            "Test precondition failed: client should be initialized"
        )

        # Act
        result = client.list_available_models()

        # Assert
        assert isinstance(result, list)


class TestCreateClient:
    """Test suite for create_client factory function."""

    def test_create_client_default_no_auto_init(self) -> None:
        """Test create_client without auto_initialize."""
        # Arrange & Act
        client = create_client(auto_initialize=False)

        # Assert
        assert isinstance(client, FrameworkClient)
        assert not client._initialized

    def test_create_client_with_auto_init(self, tmp_path: Path) -> None:
        """Test create_client with auto_initialize."""
        # Arrange
        config_file = tmp_path / "config.yaml"
        config_file.write_text("# Config\n")

        # Assumption Check
        assert config_file.exists(), "Test precondition failed: config should exist"

        # Act
        client = create_client(config_path=config_file, auto_initialize=True)

        # Assert
        assert isinstance(client, FrameworkClient)
        assert client._initialized

    def test_create_client_invalid_mode_raises_error(self) -> None:
        """Test create_client with invalid mode raises ValueError."""
        # Arrange
        invalid_mode = "bad_mode"

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            create_client(mode=invalid_mode, auto_initialize=False)

        assert "Invalid mode" in str(exc_info.value)
