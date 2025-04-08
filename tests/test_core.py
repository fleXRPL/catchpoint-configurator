"""Tests for the core functionality."""

import os
from unittest.mock import Mock, patch

import pytest

from catchpoint_configurator.core import CatchpointConfigurator
from catchpoint_configurator.exceptions import ValidationError


@pytest.fixture
def mock_api():
    """Create a mock API client."""
    return Mock()


@pytest.fixture
def configurator(mock_api):
    """Create a configurator instance with mock API."""
    with patch("catchpoint_configurator.core.CatchpointAPI") as mock_api_class:
        mock_api_class.return_value = mock_api
        return CatchpointConfigurator(client_id="test", client_secret="test")


@pytest.fixture
def test_config():
    """Sample test configuration."""
    return {
        "type": "test",
        "name": "Test Web Monitor",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
        "alerts": [
            {
                "name": "High Response Time",
                "metric": "response_time",
                "operator": ">",
                "threshold": 3000,
                "recipients": [{"email": "test@example.com"}],
            }
        ],
    }


@pytest.fixture
def test_config_file(test_config, tmp_path):
    """Create a temporary test config file."""
    import yaml

    config_file = tmp_path / "test_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(test_config, f)
    return str(config_file)


def test_init(configurator):
    """Test configurator initialization."""
    assert configurator.client_id == "test"
    assert configurator.client_secret == "test"


def test_validate(configurator, test_config_file):
    """Test configuration validation."""
    assert configurator.validate(test_config_file) is True


def test_deploy_test(configurator, test_config_file, mock_api):
    """Test deploying a new test."""
    mock_api.list_tests.return_value = []  # No existing tests
    mock_api.create_test.return_value = {"id": "new_test", "name": "Test Web Monitor"}

    result = configurator.deploy(test_config_file)
    assert result["status"] == "success"
    mock_api.create_test.assert_called_once()


def test_deploy_existing_test(configurator, test_config_file, mock_api):
    """Test deploying an existing test."""
    mock_api.list_tests.return_value = [{"id": "existing_test", "name": "Test Web Monitor"}]
    mock_api.update_test.return_value = {"id": "existing_test", "name": "Test Web Monitor"}

    result = configurator.deploy(test_config_file, force=True)
    assert result["status"] == "success"
    mock_api.update_test.assert_called_once()


def test_list_tests(configurator, mock_api):
    """Test listing tests."""
    mock_api.list_tests.return_value = [
        {"id": "test1", "name": "Test 1"},
        {"id": "test2", "name": "Test 2"},
    ]
    result = configurator.list(config_type="test")
    assert len(result) == 2
    assert result[0]["name"] == "Test 1"


def test_delete_test(configurator, test_config_file, mock_api):
    """Test deleting a test."""
    mock_api.list_tests.return_value = [{"id": "test123", "name": "Test Web Monitor"}]

    result = configurator.delete(test_config_file)
    assert result["status"] == "success"
    mock_api.delete_test.assert_called_once_with("test123")


def test_export_config(configurator, test_config_file):
    """Test exporting a configuration."""
    result = configurator.export(test_config_file)
    assert isinstance(result, str)
    assert "type: test" in result
    assert "name: Test Web Monitor" in result
