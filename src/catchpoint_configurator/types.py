"""Type definitions for Catchpoint Configurator."""

from typing import Any, Dict, List, NewType, TypedDict, Union, cast

# Basic types
ConfigPath = NewType("ConfigPath", str)
NodeList = NewType("NodeList", List[str])


class AlertConfig(TypedDict):
    """Alert configuration type."""

    metric: str
    threshold: float
    condition: str
    recipients: List[Dict[str, str]]


class TestConfig(TypedDict):
    """Test configuration type."""

    name: str
    type: str
    url: str
    frequency: int
    nodes: List[str]
    alerts: List[AlertConfig]


class LayoutConfig(TypedDict):
    """Layout configuration type."""

    type: str
    title: str
    test_id: str
    metrics: List[str]


class DashboardConfig(TypedDict):
    """Dashboard configuration type."""

    name: str
    description: str
    layout: List[LayoutConfig]


class RecipientConfig(TypedDict):
    """Recipient configuration type."""

    type: str
    address: str


class MetricConfig(TypedDict):
    """Metric configuration type."""

    name: str
    type: str
    unit: str
    aggregation: str


class ContestConfig(TypedDict):
    """Contest configuration type."""

    name: str
    description: str
    test_id: str
    metrics: List[MetricConfig]


class ContestResult(TypedDict):
    """Contest result type."""

    id: str
    status: str
    message: str
    data: Dict[str, Any]


ConfigType = Union[TestConfig, DashboardConfig]
ConfigDict = Dict[str, Union[str, int, List, Dict]]


def is_test_config(config: Dict[str, Any]) -> bool:
    """Check if a dictionary matches the TestConfig type.

    Args:
        config: Dictionary to check

    Returns:
        True if the dictionary matches TestConfig
    """
    required_fields = {"name", "type", "url", "frequency", "nodes", "alerts"}
    return all(field in config for field in required_fields)


def is_alert_config(config: Dict[str, Any]) -> bool:
    """Check if a dictionary matches the AlertConfig type.

    Args:
        config: Dictionary to check

    Returns:
        True if the dictionary matches AlertConfig
    """
    required_fields = {"metric", "threshold", "condition", "recipients"}
    return all(field in config for field in required_fields)


def to_test_config(config: Dict[str, Any]) -> TestConfig:
    """Convert a dictionary to a TestConfig.

    Args:
        config: Dictionary to convert

    Returns:
        TestConfig instance
    """
    if not is_test_config(config):
        raise ValueError("Invalid test configuration")
    return cast(TestConfig, config)


def to_alert_config(config: Dict[str, Any]) -> AlertConfig:
    """Convert a dictionary to an AlertConfig.

    Args:
        config: Dictionary to convert

    Returns:
        AlertConfig instance
    """
    if not is_alert_config(config):
        raise ValueError("Invalid alert configuration")
    return cast(AlertConfig, config)
