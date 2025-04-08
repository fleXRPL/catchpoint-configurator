"""Tests for configuration validation."""

import pytest
import yaml

from catchpoint_configurator.config import ConfigValidator
from catchpoint_configurator.exceptions import ValidationError
from catchpoint_configurator.types import (
    AlertConfig,
    TestConfig,
    to_alert_config,
    to_test_config,
)


@pytest.fixture
def validator():
    """Create a ConfigValidator instance."""
    return ConfigValidator()


def test_validate_test_config(validator):
    """Test validating a test configuration."""
    config = {
        "type": "test",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
        "alerts": [],
    }
    result = validator.validate(config)
    assert result is True


def test_validate_test_config_missing_required(validator):
    """Test validating a test configuration with missing required fields."""
    config = {
        "type": "test",
        "name": "test-web",
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(config)
    assert "Missing required fields" in str(exc_info.value)


def test_validate_test_config_invalid_type(validator):
    """Test validating a test configuration with invalid type."""
    config = {
        "type": "invalid",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(config)
    assert "Invalid configuration type" in str(exc_info.value)


def test_validate_alert_config(validator):
    """Test validating an alert configuration."""
    config = {
        "metric": "response_time",
        "threshold": 3000,
        "condition": ">",
        "recipients": ["email@example.com"],
    }
    result = validator.validate_alert_config(config)
    assert result is True


def test_validate_alert_config_invalid_metric(validator):
    """Test validating an alert configuration with invalid metric."""
    config = {
        "metric": "invalid_metric",
        "threshold": 3000,
        "condition": ">",
        "recipients": ["email@example.com"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate_alert_config(config)
    assert "Invalid metric" in str(exc_info.value)


def test_validate_alert_config_invalid_condition(validator):
    """Test validating an alert configuration with invalid condition."""
    config = {
        "metric": "response_time",
        "threshold": 3000,
        "condition": "invalid",
        "recipients": ["email@example.com"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate_alert_config(config)
    assert "Invalid condition" in str(exc_info.value)


def test_validate_dashboard_config(validator):
    """Test validating a dashboard configuration."""
    config = {
        "type": "dashboard",
        "name": "test-dashboard",
        "layout": [
            {
                "type": "metric",
                "title": "Response Time",
                "test_id": "test123",
            }
        ],
    }
    result = validator.validate(config)
    assert result is True


def test_validate_dashboard_config_invalid_layout(validator):
    """Test validating a dashboard configuration with invalid layout."""
    config = {
        "type": "dashboard",
        "name": "test-dashboard",
        "layout": "invalid",
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(config)
    assert "Layout must be a list" in str(exc_info.value)


def test_validate_yaml_file(validator):
    """Test validating a YAML configuration file."""
    yaml_content = """
    type: test
    name: test-web
    url: https://example.com
    frequency: 300
    nodes:
      - US-East
      - US-West
    alerts: []
    """
    result = validator.validate_yaml(yaml_content)
    assert result is True


def test_validate_yaml_file_invalid(validator):
    """Test validating an invalid YAML configuration file."""
    yaml_content = """
    type: test
    name: test-web
    url: invalid-url
    """
    with pytest.raises(ValidationError) as exc_info:
        validator.validate_yaml(yaml_content)
    assert "Missing required fields" in str(exc_info.value)


def test_validate_invalid_dict(validator):
    """Test validating a non-dictionary input."""
    with pytest.raises(ValidationError) as exc_info:
        validator.validate("not a dict")
    assert "must be a dictionary" in str(exc_info.value)


def test_validate_missing_type(validator):
    """Test validating config without type field."""
    config = {
        "name": "test-web",
        "url": "https://example.com",
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(config)
    assert "must have a type" in str(exc_info.value)


def test_test_config_class():
    """Test the TestConfig class."""
    config = {
        "type": "web",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
        "alerts": [],
    }
    test_config = to_test_config(config)
    assert test_config["type"] == "web"
    assert test_config["name"] == "test-web"
    assert test_config["url"] == "https://example.com"
    assert test_config["frequency"] == 300
    assert test_config["nodes"] == ["US-East", "US-West"]
    assert test_config["alerts"] == []


def test_alert_config_class():
    """Test the AlertConfig class."""
    config = {
        "metric": "response_time",
        "threshold": 3000,
        "condition": ">",
        "recipients": ["email@example.com"],
    }
    alert_config = to_alert_config(config)
    assert alert_config["metric"] == "response_time"
    assert alert_config["threshold"] == 3000
    assert alert_config["condition"] == ">"
    assert alert_config["recipients"] == ["email@example.com"]
