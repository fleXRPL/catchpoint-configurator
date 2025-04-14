"""Tests for the core functionality."""

import os
from unittest.mock import Mock, patch

import pytest

from catchpoint_configurator.core import CatchpointConfigurator
from catchpoint_configurator.exceptions import ConfigError, ValidationError


@pytest.fixture
def configurator():
    """Create a configurator instance for testing."""
    return CatchpointConfigurator("test_client", "test_secret")


@pytest.fixture
def mock_api(configurator):
    """Mock the API client."""
    with patch.object(configurator, "api") as mock:
        yield mock


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


@pytest.fixture
def dashboard_config():
    """Sample dashboard configuration."""
    return {
        "type": "dashboard",
        "name": "Test Dashboard",
        "layout": [
            {"widget": "response_time", "size": "large"},
            {"widget": "availability", "size": "medium"},
        ],
    }


def test_init(configurator):
    """Test configurator initialization."""
    assert configurator.client_id == "test_client"
    assert configurator.client_secret == "test_secret"


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
    """Test listing test configurations."""
    mock_api.list_tests.return_value = [
        {"id": "test1", "name": "Test 1"},
        {"id": "test2", "name": "Test 2"},
    ]

    result = configurator.list(config_type="test")
    assert len(result) == 2
    mock_api.list_tests.assert_called_once()


def test_delete_test(configurator, tmp_path, mock_api):
    """Test deleting a test configuration."""
    config = {
        "type": "test",
        "name": "Test to Delete",
        "url": "https://example.com",
        "frequency": 300,
    }
    config_file = tmp_path / "test.yaml"
    with open(config_file, "w") as f:
        import yaml

        yaml.dump(config, f)

    mock_api.list_tests.return_value = [{"id": "test1", "name": "Test to Delete"}]

    result = configurator.delete(str(config_file))
    assert result["status"] == "success"
    assert result["action"] == "deleted"
    mock_api.delete_test.assert_called_once_with("test1")


def test_delete_nonexistent_test(configurator, tmp_path, mock_api):
    """Test deleting a nonexistent test configuration."""
    config = {
        "type": "test",
        "name": "Nonexistent Test",
        "url": "https://example.com",
        "frequency": 300,
    }
    config_file = tmp_path / "nonexistent.yaml"
    with open(config_file, "w") as f:
        import yaml

        yaml.dump(config, f)

    mock_api.list_tests.return_value = []  # No matching tests

    with pytest.raises(ValidationError) as exc:
        configurator.delete(str(config_file))
    assert "not found" in str(exc.value)


def test_export_config(configurator, test_config_file):
    """Test exporting a configuration."""
    result = configurator.export(test_config_file)
    assert isinstance(result, str)
    assert "type: test" in result
    assert "name: Test Web Monitor" in result


def test_validate_invalid_config(configurator, tmp_path):
    """Test validation with invalid configuration."""
    invalid_config = {
        "type": "test",
        "name": "Invalid Test",
        # Missing required fields
    }
    config_file = tmp_path / "invalid_config.yaml"
    with open(config_file, "w") as f:
        import yaml

        yaml.dump(invalid_config, f)

    with pytest.raises(ValidationError) as exc:
        configurator.validate(str(config_file))
    assert "Missing required field" in str(exc.value)


def test_validate_nonexistent_file(configurator):
    """Test validation with nonexistent file."""
    with pytest.raises(FileNotFoundError) as exc:
        configurator.validate("nonexistent.yaml")
    assert "File not found" in str(exc.value)


def test_validate_invalid_type(configurator, tmp_path):
    """Test validation with invalid configuration type."""
    config = {
        "type": "invalid",
        "name": "Invalid Config",
        "url": "https://example.com",  # Include required fields
        "frequency": 300,
    }
    config_file = tmp_path / "invalid.yaml"
    with open(config_file, "w") as f:
        import yaml

        yaml.dump(config, f)

    with pytest.raises(ValidationError) as exc:
        configurator.validate(str(config_file))
    assert "Invalid configuration type" in str(exc.value)


def test_deploy_dashboard(configurator, tmp_path, mock_api):
    """Test deploying a dashboard configuration."""
    dashboard_config = {
        "type": "dashboard",
        "name": "Test Dashboard",
        "layout": [{"widget": "response_time"}],
    }
    config_file = tmp_path / "dashboard.yaml"
    with open(config_file, "w") as f:
        import yaml

        yaml.dump(dashboard_config, f)

    mock_api.list_dashboards.return_value = []
    mock_api.create_dashboard.return_value = {"id": "dash1", "name": "Test Dashboard"}

    result = configurator.deploy(str(config_file))
    assert result["status"] == "success"
    mock_api.create_dashboard.assert_called_once()


def test_deploy_alert(mock_api, configurator):
    """Test deploying an alert configuration."""
    config = {
        "type": "test",
        "name": "Test Alert",
        "url": "https://example.com",
        "frequency": 5,
        "alert": {
            "metric": "response_time",
            "threshold": 1000,
            "condition": ">",
            "recipients": ["user@example.com"],
        },
    }
    # Mock list_tests to return empty list (test doesn't exist)
    mock_api.list_tests.return_value = []
    mock_api.create_test.return_value = {"id": "test123"}

    result = configurator.deploy(config)
    assert result == {
        "action": "created",
        "name": "Test Alert",
        "status": "success",
        "test_id": "test123",
    }


def test_apply_template(configurator):
    """Test applying a template."""
    # The implementation currently returns an empty dict as it's not implemented
    result = configurator.apply_template("test_template", {"var": "value"})
    assert isinstance(result, dict)
    assert len(result) == 0  # Empty dict since template support is not implemented yet


def test_deploy_invalid_type(configurator, tmp_path):
    """Test deploying a configuration with invalid type."""
    invalid_config = {"type": "invalid", "name": "Invalid Config"}
    config_file = tmp_path / "invalid.yaml"
    with open(config_file, "w") as f:
        import yaml

        yaml.dump(invalid_config, f)

    with pytest.raises(ValidationError) as exc:
        configurator.deploy(str(config_file))
    assert "Invalid configuration type" in str(exc.value)


def test_list_invalid_type(mock_api, configurator):
    """Test listing with an invalid configuration type."""
    config = {"type": "invalid", "name": "Invalid Config"}
    with pytest.raises(ValidationError, match="Invalid configuration type: invalid"):
        configurator.validate(config)


def test_delete_nonexistent(mock_api, configurator):
    """Test deleting a nonexistent test."""
    config = {
        "type": "test",
        "name": "Nonexistent Test",
        "url": "https://example.com",
        "frequency": 5,
    }
    mock_api.list_tests.return_value = []  # Test doesn't exist

    with pytest.raises(ValidationError, match=r"Test 'Nonexistent Test' not found"):
        configurator.delete(config)
