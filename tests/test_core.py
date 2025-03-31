"""Tests for the core CatchpointConfigurator class."""

import os
import tempfile
from unittest.mock import MagicMock, Mock, patch

import pytest
import yaml

from catchpoint_configurator.config import ConfigValidator
from catchpoint_configurator.core import CatchpointConfigurator
from catchpoint_configurator.exceptions import ValidationError


@pytest.fixture
def mock_api():
    mock = Mock()
    mock.list_tests.return_value = [
        {"id": "test1", "name": "Test Web"},
        {"id": "test2", "name": "Test API"},
    ]
    return mock


@pytest.fixture
def configurator(mock_api):
    with patch("catchpoint_configurator.core.CatchpointAPI", return_value=mock_api):
        return CatchpointConfigurator(
            client_id="test_client", client_secret="test_secret"
        )


@pytest.fixture
def test_config():
    return {
        "type": "web",
        "name": "Test Web Monitor",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
        "alerts": [
            {
                "metric": "response_time",
                "name": "High Response Time",
                "operator": ">",
                "threshold": 3000,
                "recipients": [{"email": "test@example.com"}],
            }
        ],
    }


@pytest.fixture
def test_config_file(test_config):
    """Create a temporary test configuration file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(test_config, f)
        return f.name


def test_validate_config(configurator, test_config):
    """Test config validation."""
    result = configurator.validate(test_config)
    assert result is True


def test_validate_config_invalid(configurator):
    """Test invalid config validation."""
    invalid_config = {"type": "invalid", "name": "Invalid Test"}
    with pytest.raises(ValidationError):
        configurator.validate(invalid_config)


def test_deploy_test(configurator, test_config, mock_api):
    """Test deploying a new test."""
    mock_api.create_test.return_value = {"id": "new_test", "name": test_config["name"]}

    result = configurator.deploy(test_config)
    assert result["id"] == "new_test"
    mock_api.create_test.assert_called_once_with(test_config)


def test_deploy_existing_test(configurator, test_config, mock_api):
    """Test deploying an existing test."""
    mock_api.list_tests.return_value = [
        {"id": "existing_test", "name": test_config["name"]}
    ]
    mock_api.update_test.return_value = {
        "id": "existing_test",
        "name": test_config["name"],
    }

    result = configurator.deploy(test_config)
    assert result["id"] == "existing_test"
    mock_api.update_test.assert_called_once_with("existing_test", test_config)


def test_list_tests(configurator, mock_api):
    """Test listing tests."""
    result = configurator.list(config_type="web")
    assert len(result) == 2
    assert result[0]["name"] == "Test Web"
    mock_api.list_tests.assert_called_once()


def test_delete_test(configurator, test_config, mock_api):
    """Test deleting a test."""
    mock_api.list_tests.return_value = [{"id": "test123", "name": test_config["name"]}]

    result = configurator.delete(test_config)
    assert result is True
    mock_api.delete_test.assert_called_once_with("test123")


def test_export_config(configurator, test_config_file):
    """Test exporting a configuration."""
    result = configurator.export(test_config_file)
    assert isinstance(result, str)
    assert "type: test" in result
    assert "name: test-web" in result


def test_import_config(configurator, test_config):
    """Test importing a configuration."""
    with patch("catchpoint_configurator.core.load_yaml") as mock_load:
        mock_load.return_value = test_config
        result = configurator.import_config("test.yaml")
        assert result == test_config
