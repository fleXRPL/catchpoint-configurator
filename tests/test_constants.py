"""Test constants module."""

from catchpoint_configurator.constants import (
    API_BASE_URL,
    API_DASHBOARD_URL,
    API_TEST_URL,
    API_TOKEN_URL,
    CONFIG_FILE,
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    VALID_CONDITIONS,
    VALID_METRICS,
    VALID_NODES,
    VALID_RECIPIENT_TYPES,
    VALID_TEST_TYPES,
)


def test_api_constants():
    """Test API constants."""
    assert API_BASE_URL == "https://api.catchpoint.com/v2"
    assert API_TOKEN_URL == "https://api.catchpoint.com/v2/token"
    assert API_TEST_URL == "https://api.catchpoint.com/v2/tests"
    assert API_DASHBOARD_URL == "https://api.catchpoint.com/v2/dashboards"


def test_test_types():
    """Test test types."""
    assert isinstance(VALID_TEST_TYPES, frozenset)
    assert "web" in VALID_TEST_TYPES
    assert "api" in VALID_TEST_TYPES
    assert "transaction" in VALID_TEST_TYPES
    assert "dns" in VALID_TEST_TYPES
    assert "traceroute" in VALID_TEST_TYPES


def test_metrics():
    """Test metrics."""
    assert isinstance(VALID_METRICS, frozenset)
    assert "response_time" in VALID_METRICS
    assert "availability" in VALID_METRICS
    assert "throughput" in VALID_METRICS
    assert "dns_time" in VALID_METRICS
    assert "connect_time" in VALID_METRICS
    assert "ssl_time" in VALID_METRICS
    assert "wait_time" in VALID_METRICS
    assert "load_time" in VALID_METRICS


def test_nodes():
    """Test nodes."""
    assert isinstance(VALID_NODES, frozenset)
    assert "US-East" in VALID_NODES
    assert "US-West" in VALID_NODES
    assert "EU-West" in VALID_NODES
    assert "EU-Central" in VALID_NODES
    assert "AP-Southeast" in VALID_NODES
    assert "AP-Northeast" in VALID_NODES


def test_conditions():
    """Test conditions."""
    assert isinstance(VALID_CONDITIONS, frozenset)
    assert ">" in VALID_CONDITIONS
    assert "<" in VALID_CONDITIONS
    assert ">=" in VALID_CONDITIONS
    assert "<=" in VALID_CONDITIONS
    assert "==" in VALID_CONDITIONS
    assert "!=" in VALID_CONDITIONS


def test_recipient_types():
    """Test recipient types."""
    assert isinstance(VALID_RECIPIENT_TYPES, frozenset)
    assert "email" in VALID_RECIPIENT_TYPES
    assert "slack" in VALID_RECIPIENT_TYPES
    assert "webhook" in VALID_RECIPIENT_TYPES


def test_file_constants():
    """Test file constants."""
    assert CONFIG_FILE == "catchpoint.yaml"
    assert LOG_FILE == "catchpoint.log"
    assert LOG_FORMAT == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    assert LOG_LEVEL == "INFO"


def test_constant_immutability():
    """Test that constants are immutable."""
    try:
        VALID_TEST_TYPES.add("invalid")
        assert False, "VALID_TEST_TYPES should be immutable"
    except AttributeError:
        pass

    try:
        VALID_METRICS.add("invalid")
        assert False, "VALID_METRICS should be immutable"
    except AttributeError:
        pass

    try:
        VALID_NODES.add("invalid")
        assert False, "VALID_NODES should be immutable"
    except AttributeError:
        pass

    try:
        VALID_CONDITIONS.add("invalid")
        assert False, "VALID_CONDITIONS should be immutable"
    except AttributeError:
        pass

    try:
        VALID_RECIPIENT_TYPES.add("invalid")
        assert False, "VALID_RECIPIENT_TYPES should be immutable"
    except AttributeError:
        pass
