"""Tests for configuration validation."""

import pytest
import yaml

from catchpoint_configurator.validation import (
    validate_config,
    validate_test_config,
    validate_alert_config,
    validate_dashboard_config,
    validate_yaml,
    ValidationError,
)

def test_validate_config():
    """Test validating a configuration."""
    config = {
        "type": "web",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
    }
    assert validate_config(config) is True

def test_validate_config_invalid_type():
    """Test validating a configuration with invalid type."""
    config = {
        "type": "invalid",
        "name": "test-web",
        "url": "https://example.com",
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_config(config)
    assert "Invalid configuration type" in str(exc_info.value)

def test_validate_test_config():
    """Test validating a test configuration."""
    config = {
        "type": "web",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
    }
    assert validate_test_config(config) is True

def test_validate_test_config_missing_fields():
    """Test validating a test configuration with missing fields."""
    config = {
        "type": "web",
        "name": "test-web",
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_test_config(config)
    assert "Missing required field" in str(exc_info.value)

def test_validate_test_config_invalid_url():
    """Test validating a test configuration with invalid URL."""
    config = {
        "type": "web",
        "name": "test-web",
        "url": "invalid-url",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_test_config(config)
    assert "Invalid URL" in str(exc_info.value)

def test_validate_test_config_invalid_frequency():
    """Test validating a test configuration with invalid frequency."""
    config = {
        "type": "web",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": "invalid",
        "nodes": ["US-East", "US-West"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_test_config(config)
    assert "Invalid frequency" in str(exc_info.value)

def test_validate_test_config_invalid_nodes():
    """Test validating a test configuration with invalid nodes."""
    config = {
        "type": "web",
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["invalid-node"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_test_config(config)
    assert "Invalid node" in str(exc_info.value)

def test_validate_alert_config():
    """Test validating an alert configuration."""
    config = {
        "metric": "response_time",
        "threshold": 3000,
        "condition": ">",
        "recipients": ["email@example.com"],
    }
    assert validate_alert_config(config) is True

def test_validate_alert_config_invalid_metric():
    """Test validating an alert configuration with invalid metric."""
    config = {
        "metric": "invalid-metric",
        "threshold": 3000,
        "condition": ">",
        "recipients": ["email@example.com"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_alert_config(config)
    assert "Invalid metric" in str(exc_info.value)

def test_validate_alert_config_invalid_threshold():
    """Test validating an alert configuration with invalid threshold."""
    config = {
        "metric": "response_time",
        "threshold": "invalid",
        "condition": ">",
        "recipients": ["email@example.com"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_alert_config(config)
    assert "Invalid threshold" in str(exc_info.value)

def test_validate_alert_config_invalid_condition():
    """Test validating an alert configuration with invalid condition."""
    config = {
        "metric": "response_time",
        "threshold": 3000,
        "condition": "invalid",
        "recipients": ["email@example.com"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_alert_config(config)
    assert "Invalid condition" in str(exc_info.value)

def test_validate_alert_config_invalid_recipients():
    """Test validating an alert configuration with invalid recipients."""
    config = {
        "metric": "response_time",
        "threshold": 3000,
        "condition": ">",
        "recipients": ["invalid-recipient"],
    }
    with pytest.raises(ValidationError) as exc_info:
        validate_alert_config(config)
    assert "Invalid recipient" in str(exc_info.value)

def test_validate_dashboard_config():
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
    assert validate_dashboard_config(config) is True

def test_validate_dashboard_config_invalid_layout():
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
    with pytest.raises(ValidationError) as exc_info:
        validate_dashboard_config(config)
    assert "Invalid widget type" in str(exc_info.value)

def test_validate_yaml():
    """Test validating a YAML configuration."""
    yaml_content = """
    type: web
    name: test-web
    url: https://example.com
    frequency: 300
    nodes:
      - US-East
      - US-West
    """
    assert validate_yaml(yaml_content) is True

def test_validate_yaml_invalid():
    """Test validating an invalid YAML configuration."""
    yaml_content = """
    type: web
    name: test-web
    url: invalid-url
    """
    with pytest.raises(ValidationError) as exc_info:
        validate_yaml(yaml_content)
    assert "Invalid URL" in str(exc_info.value)

def test_validate_yaml_syntax_error():
    """Test validating a YAML configuration with syntax error."""
    yaml_content = """
    type: web
    name: test-web
    url: https://example.com
    frequency: invalid: yaml
    """
    with pytest.raises(ValidationError) as exc_info:
        validate_yaml(yaml_content)
    assert "Invalid YAML syntax" in str(exc_info.value)

def test_validation_error():
    """Test ValidationError exception."""
    error = ValidationError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)

def test_validation_error_with_details():
    """Test ValidationError exception with details."""
    error = ValidationError(
        "Test error",
        details={"field": "name", "value": "invalid", "reason": "too long"},
    )
    assert str(error) == "Test error"
    assert error.details == {
        "field": "name",
        "value": "invalid",
        "reason": "too long",
    } 