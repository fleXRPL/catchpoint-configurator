"""Tests for configuration validation."""

import pytest
import yaml

from catchpoint_configurator.config import (
    ConfigError,
    ConfigValidator,
    TestConfig,
    AlertConfig,
)

@pytest.fixture
def validator():
    """Create a ConfigValidator instance."""
    return ConfigValidator()

def test_validate_test_config(validator):
    """Test validating a test configuration."""
    config = {
        "type": "web",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
    }
    result = validator.validate_test_config(config)
    assert result is True

def test_validate_test_config_missing_required(validator):
    """Test validating a test configuration with missing required fields."""
    config = {
        "type": "web",
        "name": "test-web",
    }
    with pytest.raises(ConfigError) as exc_info:
        validator.validate_test_config(config)
    assert "Missing required field" in str(exc_info.value)

def test_validate_test_config_invalid_type(validator):
    """Test validating a test configuration with invalid type."""
    config = {
        "type": "invalid",
        "name": "test-web",
        "url": "https://example.com",
    }
    with pytest.raises(ConfigError) as exc_info:
        validator.validate_test_config(config)
    assert "Invalid test type" in str(exc_info.value)

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
    with pytest.raises(ConfigError) as exc_info:
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
    with pytest.raises(ConfigError) as exc_info:
        validator.validate_alert_config(config)
    assert "Invalid condition" in str(exc_info.value)

def test_validate_dashboard_config(validator):
    """Test validating a dashboard configuration."""
    config = {
        "type": "dashboard",
        "name": "test-dashboard",
        "description": "Test dashboard",
        "layout": [
            {
                "type": "metric",
                "title": "Response Time",
                "metric": "response_time",
                "test_id": "test123",
            }
        ],
    }
    result = validator.validate_dashboard_config(config)
    assert result is True

def test_validate_dashboard_config_invalid_layout(validator):
    """Test validating a dashboard configuration with invalid layout."""
    config = {
        "type": "dashboard",
        "name": "test-dashboard",
        "description": "Test dashboard",
        "layout": [
            {
                "type": "invalid",
                "title": "Response Time",
            }
        ],
    }
    with pytest.raises(ConfigError) as exc_info:
        validator.validate_dashboard_config(config)
    assert "Invalid widget type" in str(exc_info.value)

def test_validate_yaml_file(validator):
    """Test validating a YAML configuration file."""
    yaml_content = """
    type: web
    name: test-web
    url: https://example.com
    frequency: 300
    nodes:
      - US-East
      - US-West
    """
    result = validator.validate_yaml(yaml_content)
    assert result is True

def test_validate_yaml_file_invalid(validator):
    """Test validating an invalid YAML configuration file."""
    yaml_content = """
    type: web
    name: test-web
    url: invalid-url
    """
    with pytest.raises(ConfigError) as exc_info:
        validator.validate_yaml(yaml_content)
    assert "Invalid URL" in str(exc_info.value)

def test_test_config_class():
    """Test the TestConfig class."""
    config = TestConfig(
        type="web",
        name="test-web",
        url="https://example.com",
        frequency=300,
        nodes=["US-East", "US-West"],
    )
    assert config.type == "web"
    assert config.name == "test-web"
    assert config.url == "https://example.com"
    assert config.frequency == 300
    assert config.nodes == ["US-East", "US-West"]

def test_alert_config_class():
    """Test the AlertConfig class."""
    config = AlertConfig(
        metric="response_time",
        threshold=3000,
        condition=">",
        recipients=["email@example.com"],
    )
    assert config.metric == "response_time"
    assert config.threshold == 3000
    assert config.condition == ">"
    assert config.recipients == ["email@example.com"]
