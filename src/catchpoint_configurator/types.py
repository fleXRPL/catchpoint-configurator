"""Type definitions for Catchpoint Configurator."""

from typing import Any, Dict, List, NewType, TypedDict, Union

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
