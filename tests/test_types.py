"""Tests for type definitions."""

from unittest.mock import Mock, patch

import pytest

from catchpoint_configurator.types import (
    AlertConfig,
    ConfigDict,
    ConfigPath,
    DashboardConfig,
    LayoutConfig,
    MetricConfig,
    NodeList,
    RecipientConfig,
    TestConfig,
    to_alert_config,
    to_test_config,
)


@pytest.fixture
def mock_type_validator():
    """Create a mock type validator."""
    return Mock()


def test_config_path(mock_type_validator):
    """Test ConfigPath type."""
    with patch("catchpoint_configurator.types.ConfigPath") as mock_path:
        mock_path.validate.return_value = True
        # Test valid paths
        assert mock_path.validate("config.yaml")
        assert mock_path.validate("/path/to/config.yaml")
        # Test invalid paths
        mock_path.validate.side_effect = TypeError("Invalid path")
        with pytest.raises(TypeError):
            mock_path.validate(123)


def test_config_dict(mock_type_validator):
    """Test ConfigDict type."""
    with patch("catchpoint_configurator.types.ConfigDict") as mock_dict:
        mock_dict.validate.return_value = True
        # Test valid dict
        valid_dict = {
            "name": "test",
            "type": "web",
            "url": "https://example.com",
        }
        assert mock_dict.validate(valid_dict)
        # Test invalid dict
        mock_dict.validate.side_effect = TypeError("Invalid dict")
        with pytest.raises(TypeError):
            mock_dict.validate("not a dict")


def test_node_list(mock_type_validator):
    """Test NodeList type."""
    with patch("catchpoint_configurator.types.NodeList") as mock_list:
        mock_list.validate.return_value = True
        # Test valid nodes
        valid_nodes = ["US-East", "US-West", "EU-West"]
        assert mock_list.validate(valid_nodes)
        # Test invalid nodes
        mock_list.validate.side_effect = TypeError("Invalid node list")
        with pytest.raises(TypeError):
            mock_list.validate("not a list")


def test_alert_config(mock_type_validator):
    """Test AlertConfig type."""
    with patch("catchpoint_configurator.types.AlertConfig") as mock_alert:
        mock_alert.validate.return_value = True
        # Test valid alert config
        valid_alert = {
            "metric": "response_time",
            "threshold": 3000,
            "condition": ">",
            "recipients": [
                {"type": "email", "address": "test@example.com"},
                {"type": "slack", "channel": "#alerts"},
            ],
        }
        assert mock_alert.validate(valid_alert)
        # Test invalid alert config
        mock_alert.validate.side_effect = TypeError("Invalid alert config")
        with pytest.raises(TypeError):
            mock_alert.validate("not a dict")


def test_test_config(mock_type_validator):
    """Test TestConfig type."""
    with patch("catchpoint_configurator.types.TestConfig") as mock_test:
        mock_test.validate.return_value = True
        # Test valid test config
        valid_test = {
            "name": "test-web",
            "type": "web",
            "url": "https://example.com",
            "frequency": 300,
            "nodes": ["US-East", "US-West"],
            "alerts": [
                {
                    "metric": "response_time",
                    "threshold": 3000,
                    "condition": ">",
                    "recipients": [
                        {"type": "email", "address": "test@example.com"},
                    ],
                },
            ],
        }
        assert mock_test.validate(valid_test)
        # Test invalid test config
        mock_test.validate.side_effect = TypeError("Invalid test config")
        with pytest.raises(TypeError):
            mock_test.validate("not a dict")


def test_dashboard_config(mock_type_validator):
    """Test DashboardConfig type."""
    with patch("catchpoint_configurator.types.DashboardConfig") as mock_dashboard:
        mock_dashboard.validate.return_value = True
        # Test valid dashboard config
        valid_dashboard = {
            "name": "test-dashboard",
            "type": "dashboard",
            "description": "Test dashboard",
            "layout": [
                {
                    "type": "metric",
                    "title": "Response Time",
                    "metric": "response_time",
                    "test": "test-web",
                },
            ],
        }
        assert mock_dashboard.validate(valid_dashboard)
        # Test invalid dashboard config
        mock_dashboard.validate.side_effect = TypeError("Invalid dashboard config")
        with pytest.raises(TypeError):
            mock_dashboard.validate("not a dict")


def test_metric_config(mock_type_validator):
    """Test MetricConfig type."""
    with patch("catchpoint_configurator.types.MetricConfig") as mock_metric:
        mock_metric.validate.return_value = True
        # Test valid metric config
        valid_metric = {
            "type": "metric",
            "title": "Response Time",
            "metric": "response_time",
            "test": "test-web",
        }
        assert mock_metric.validate(valid_metric)
        # Test invalid metric config
        mock_metric.validate.side_effect = TypeError("Invalid metric config")
        with pytest.raises(TypeError):
            mock_metric.validate("not a dict")


def test_layout_config(mock_type_validator):
    """Test LayoutConfig type."""
    with patch("catchpoint_configurator.types.LayoutConfig") as mock_layout:
        mock_layout.validate.return_value = True
        # Test valid layout config
        valid_layout = [
            {
                "type": "metric",
                "title": "Response Time",
                "metric": "response_time",
                "test": "test-web",
            },
        ]
        assert mock_layout.validate(valid_layout)
        # Test invalid layout config
        mock_layout.validate.side_effect = TypeError("Invalid layout config")
        with pytest.raises(TypeError):
            mock_layout.validate("not a list")


def test_recipient_config(mock_type_validator):
    """Test RecipientConfig type."""
    with patch("catchpoint_configurator.types.RecipientConfig") as mock_recipient:
        mock_recipient.validate.return_value = True
        # Test valid recipient configs
        valid_email = {
            "type": "email",
            "address": "test@example.com",
        }
        valid_slack = {
            "type": "slack",
            "channel": "#alerts",
        }
        assert mock_recipient.validate(valid_email)
        assert mock_recipient.validate(valid_slack)
        # Test invalid recipient config
        mock_recipient.validate.side_effect = TypeError("Invalid recipient config")
        with pytest.raises(TypeError):
            mock_recipient.validate("not a dict")


def test_type_compatibility(mock_type_validator):
    """Test type compatibility."""
    with patch("catchpoint_configurator.types.TestConfig") as mock_test:
        mock_test.validate.return_value = True
        # Test nested types
        test_config = {
            "name": "test-web",
            "type": "web",
            "url": "https://example.com",
            "frequency": 300,
            "nodes": ["US-East", "US-West"],
            "alerts": [
                {
                    "metric": "response_time",
                    "threshold": 3000,
                    "condition": ">",
                    "recipients": [
                        {"type": "email", "address": "test@example.com"},
                    ],
                },
            ],
        }
        assert mock_test.validate(test_config)


def test_to_test_config_invalid():
    """Test converting invalid dictionary to TestConfig."""
    invalid_test = {
        "name": "test-web",
        # Missing required fields
    }
    with pytest.raises(ValueError, match="Invalid test configuration"):
        to_test_config(invalid_test)


def test_to_alert_config_invalid():
    """Test converting invalid dictionary to AlertConfig."""
    invalid_alert = {
        "metric": "response_time",
        # Missing required fields
    }
    with pytest.raises(ValueError, match="Invalid alert configuration"):
        to_alert_config(invalid_alert)
