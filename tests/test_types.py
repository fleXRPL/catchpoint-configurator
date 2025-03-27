"""Tests for type definitions."""

from typing import Dict, List, Optional, Union

import pytest

from catchpoint_configurator.types import (
    ConfigPath,
    ConfigDict,
    NodeList,
    AlertConfig,
    TestConfig,
    DashboardConfig,
    MetricConfig,
    LayoutConfig,
    RecipientConfig,
)

def test_config_path():
    """Test ConfigPath type."""
    # Valid paths
    assert isinstance("config.yaml", ConfigPath)
    assert isinstance("/path/to/config.yaml", ConfigPath)
    assert isinstance("path/to/config.yaml", ConfigPath)
    
    # Invalid paths
    with pytest.raises(TypeError):
        ConfigPath(123)  # type: ignore
    with pytest.raises(TypeError):
        ConfigPath(None)  # type: ignore

def test_config_dict():
    """Test ConfigDict type."""
    # Valid dictionaries
    valid_dict = {
        "name": "test",
        "type": "web",
        "url": "https://example.com",
    }
    assert isinstance(valid_dict, ConfigDict)
    
    # Invalid dictionaries
    with pytest.raises(TypeError):
        ConfigDict("not a dict")  # type: ignore
    with pytest.raises(TypeError):
        ConfigDict(None)  # type: ignore

def test_node_list():
    """Test NodeList type."""
    # Valid node lists
    valid_nodes = ["US-East", "US-West", "EU-West"]
    assert isinstance(valid_nodes, NodeList)
    
    # Invalid node lists
    with pytest.raises(TypeError):
        NodeList("not a list")  # type: ignore
    with pytest.raises(TypeError):
        NodeList([123])  # type: ignore

def test_alert_config():
    """Test AlertConfig type."""
    # Valid alert config
    valid_alert = {
        "metric": "response_time",
        "threshold": 3000,
        "condition": ">",
        "recipients": [
            {"type": "email", "address": "test@example.com"},
            {"type": "slack", "channel": "#alerts"},
        ],
    }
    assert isinstance(valid_alert, AlertConfig)
    
    # Invalid alert config
    with pytest.raises(TypeError):
        AlertConfig("not a dict")  # type: ignore
    with pytest.raises(TypeError):
        AlertConfig({"invalid": "config"})  # type: ignore

def test_test_config():
    """Test TestConfig type."""
    # Valid test config
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
    assert isinstance(valid_test, TestConfig)
    
    # Invalid test config
    with pytest.raises(TypeError):
        TestConfig("not a dict")  # type: ignore
    with pytest.raises(TypeError):
        TestConfig({"invalid": "config"})  # type: ignore

def test_dashboard_config():
    """Test DashboardConfig type."""
    # Valid dashboard config
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
            {
                "type": "metric",
                "title": "Error Rate",
                "metric": "error_rate",
                "test": "test-web",
            },
        ],
    }
    assert isinstance(valid_dashboard, DashboardConfig)
    
    # Invalid dashboard config
    with pytest.raises(TypeError):
        DashboardConfig("not a dict")  # type: ignore
    with pytest.raises(TypeError):
        DashboardConfig({"invalid": "config"})  # type: ignore

def test_metric_config():
    """Test MetricConfig type."""
    # Valid metric config
    valid_metric = {
        "type": "metric",
        "title": "Response Time",
        "metric": "response_time",
        "test": "test-web",
    }
    assert isinstance(valid_metric, MetricConfig)
    
    # Invalid metric config
    with pytest.raises(TypeError):
        MetricConfig("not a dict")  # type: ignore
    with pytest.raises(TypeError):
        MetricConfig({"invalid": "config"})  # type: ignore

def test_layout_config():
    """Test LayoutConfig type."""
    # Valid layout config
    valid_layout = [
        {
            "type": "metric",
            "title": "Response Time",
            "metric": "response_time",
            "test": "test-web",
        },
        {
            "type": "metric",
            "title": "Error Rate",
            "metric": "error_rate",
            "test": "test-web",
        },
    ]
    assert isinstance(valid_layout, LayoutConfig)
    
    # Invalid layout config
    with pytest.raises(TypeError):
        LayoutConfig("not a list")  # type: ignore
    with pytest.raises(TypeError):
        LayoutConfig([{"invalid": "config"}])  # type: ignore

def test_recipient_config():
    """Test RecipientConfig type."""
    # Valid recipient configs
    valid_email = {
        "type": "email",
        "address": "test@example.com",
    }
    assert isinstance(valid_email, RecipientConfig)
    
    valid_slack = {
        "type": "slack",
        "channel": "#alerts",
    }
    assert isinstance(valid_slack, RecipientConfig)
    
    # Invalid recipient config
    with pytest.raises(TypeError):
        RecipientConfig("not a dict")  # type: ignore
    with pytest.raises(TypeError):
        RecipientConfig({"invalid": "config"})  # type: ignore

def test_type_compatibility():
    """Test type compatibility."""
    # Test nested types
    test_config: TestConfig = {
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
    
    # Test type hints
    def process_config(config: TestConfig) -> None:
        assert isinstance(config, TestConfig)
        assert isinstance(config["alerts"], List[AlertConfig])
        assert isinstance(config["nodes"], NodeList)
    
    process_config(test_config) 