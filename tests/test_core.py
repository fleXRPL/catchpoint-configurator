"""Tests for the core CatchpointConfigurator class."""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
import yaml

from catchpoint_configurator.core import CatchpointConfigurator
from catchpoint_configurator.config import ConfigValidator

@pytest.fixture
def configurator():
    """Create a CatchpointConfigurator instance."""
    return CatchpointConfigurator(
        client_id="test_client_id",
        client_secret="test_client_secret",
        debug=True,
    )

@pytest.fixture
def test_config():
    """Create a test configuration."""
    return {
        "type": "test",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
        "alerts": [
            {
                "name": "High Response Time",
                "metric": "response_time",
                "threshold": 2000,
                "operator": ">",
                "recipients": [
                    {"email": "test@example.com"},
                ],
            },
        ],
    }

@pytest.fixture
def test_config_file(test_config):
    """Create a temporary test configuration file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(test_config, f)
        return f.name

def test_validate_config(configurator, test_config_file):
    """Test configuration validation."""
    assert configurator.validate(test_config_file) is True

def test_validate_invalid_config(configurator):
    """Test validation of invalid configuration."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"type": "test", "name": "invalid"}, f)
        with pytest.raises(Exception):
            configurator.validate(f.name)

@patch("catchpoint_configurator.core.CatchpointAPI")
def test_deploy_test(mock_api, configurator, test_config_file):
    """Test deploying a test configuration."""
    mock_api.return_value.list_tests.return_value = []
    mock_api.return_value.create_test.return_value = {"id": "test123"}
    
    result = configurator.deploy(test_config_file)
    assert result["status"] == "success"
    assert result["action"] == "created"
    assert result["test_id"] == "test123"

@patch("catchpoint_configurator.core.CatchpointAPI")
def test_deploy_existing_test(mock_api, configurator, test_config_file):
    """Test deploying an existing test configuration."""
    mock_api.return_value.list_tests.return_value = [{"id": "test123", "name": "test-web"}]
    mock_api.return_value.update_test.return_value = {"id": "test123"}
    
    result = configurator.deploy(test_config_file, force=True)
    assert result["status"] == "success"
    assert result["action"] == "updated"
    assert result["test_id"] == "test123"

@patch("catchpoint_configurator.core.CatchpointAPI")
def test_list_tests(mock_api, configurator):
    """Test listing tests."""
    mock_api.return_value.list_tests.return_value = [
        {"id": "test1", "name": "test1"},
        {"id": "test2", "name": "test2"},
    ]
    
    tests = configurator.list(config_type="test")
    assert len(tests) == 2
    assert all(test["type"] == "test" for test in tests)

@patch("catchpoint_configurator.core.CatchpointAPI")
def test_delete_test(mock_api, configurator, test_config_file):
    """Test deleting a test."""
    mock_api.return_value.list_tests.return_value = [{"id": "test123", "name": "test-web"}]
    
    result = configurator.delete(test_config_file)
    assert result["status"] == "success"
    assert result["action"] == "deleted"
    assert result["name"] == "test-web"

def test_export_config(configurator, test_config_file):
    """Test exporting a configuration."""
    result = configurator.export(test_config_file)
    assert isinstance(result, str)
    assert "type: test" in result
    assert "name: test-web" in result

def test_import_config(configurator, test_config_file):
    """Test importing a configuration."""
    result = configurator.import_config(test_config_file)
    assert result["type"] == "test"
    assert result["name"] == "test-web"
    assert result["url"] == "https://example.com"
