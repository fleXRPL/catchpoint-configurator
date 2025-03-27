"""Tests for constants."""

import pytest

from catchpoint_configurator.constants import (
    API_BASE_URL,
    API_VERSION,
    DEFAULT_TIMEOUT,
    MAX_TIMEOUT,
    MIN_TIMEOUT,
    VALID_TEST_TYPES,
    VALID_METRICS,
    VALID_NODES,
    VALID_CONDITIONS,
    VALID_RECIPIENT_TYPES,
    DEFAULT_FREQUENCY,
    MIN_FREQUENCY,
    MAX_FREQUENCY,
    DEFAULT_RETRIES,
    MAX_RETRIES,
    MIN_RETRIES,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_FILE,
    CONFIG_FILE,
    TEMPLATE_DIR,
    CACHE_DIR,
    CACHE_TTL,
)

def test_api_constants():
    """Test API-related constants."""
    assert API_BASE_URL == "https://api.catchpoint.com"
    assert API_VERSION == "v2"
    assert isinstance(DEFAULT_TIMEOUT, int)
    assert isinstance(MAX_TIMEOUT, int)
    assert isinstance(MIN_TIMEOUT, int)
    assert MAX_TIMEOUT > MIN_TIMEOUT
    assert DEFAULT_TIMEOUT >= MIN_TIMEOUT
    assert DEFAULT_TIMEOUT <= MAX_TIMEOUT

def test_test_types():
    """Test valid test types."""
    assert isinstance(VALID_TEST_TYPES, set)
    assert all(isinstance(test_type, str) for test_type in VALID_TEST_TYPES)
    assert "web" in VALID_TEST_TYPES
    assert "dns" in VALID_TEST_TYPES
    assert "ping" in VALID_TEST_TYPES

def test_metrics():
    """Test valid metrics."""
    assert isinstance(VALID_METRICS, set)
    assert all(isinstance(metric, str) for metric in VALID_METRICS)
    assert "response_time" in VALID_METRICS
    assert "error_rate" in VALID_METRICS
    assert "availability" in VALID_METRICS

def test_nodes():
    """Test valid nodes."""
    assert isinstance(VALID_NODES, set)
    assert all(isinstance(node, str) for node in VALID_NODES)
    assert "US-East" in VALID_NODES
    assert "US-West" in VALID_NODES
    assert "EU-West" in VALID_NODES

def test_conditions():
    """Test valid conditions."""
    assert isinstance(VALID_CONDITIONS, set)
    assert all(isinstance(condition, str) for condition in VALID_CONDITIONS)
    assert ">" in VALID_CONDITIONS
    assert "<" in VALID_CONDITIONS
    assert ">=" in VALID_CONDITIONS
    assert "<=" in VALID_CONDITIONS
    assert "==" in VALID_CONDITIONS
    assert "!=" in VALID_CONDITIONS

def test_recipient_types():
    """Test valid recipient types."""
    assert isinstance(VALID_RECIPIENT_TYPES, set)
    assert all(isinstance(recipient_type, str) for recipient_type in VALID_RECIPIENT_TYPES)
    assert "email" in VALID_RECIPIENT_TYPES
    assert "slack" in VALID_RECIPIENT_TYPES

def test_frequency_constants():
    """Test frequency-related constants."""
    assert isinstance(DEFAULT_FREQUENCY, int)
    assert isinstance(MIN_FREQUENCY, int)
    assert isinstance(MAX_FREQUENCY, int)
    assert MAX_FREQUENCY > MIN_FREQUENCY
    assert DEFAULT_FREQUENCY >= MIN_FREQUENCY
    assert DEFAULT_FREQUENCY <= MAX_FREQUENCY

def test_retry_constants():
    """Test retry-related constants."""
    assert isinstance(DEFAULT_RETRIES, int)
    assert isinstance(MAX_RETRIES, int)
    assert isinstance(MIN_RETRIES, int)
    assert MAX_RETRIES > MIN_RETRIES
    assert DEFAULT_RETRIES >= MIN_RETRIES
    assert DEFAULT_RETRIES <= MAX_RETRIES

def test_logging_constants():
    """Test logging-related constants."""
    assert isinstance(LOG_FORMAT, str)
    assert isinstance(LOG_LEVEL, str)
    assert isinstance(LOG_FILE, str)
    assert "%" in LOG_FORMAT  # Check for format specifiers
    assert LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def test_file_constants():
    """Test file-related constants."""
    assert isinstance(CONFIG_FILE, str)
    assert isinstance(TEMPLATE_DIR, str)
    assert isinstance(CACHE_DIR, str)
    assert CONFIG_FILE.endswith(".yaml")
    assert TEMPLATE_DIR.endswith("/templates")
    assert CACHE_DIR.endswith("/cache")

def test_cache_constants():
    """Test cache-related constants."""
    assert isinstance(CACHE_TTL, int)
    assert CACHE_TTL > 0

def test_constant_immutability():
    """Test that constants are immutable."""
    with pytest.raises(TypeError):
        VALID_TEST_TYPES.add("invalid")
    
    with pytest.raises(TypeError):
        VALID_METRICS.add("invalid")
    
    with pytest.raises(TypeError):
        VALID_NODES.add("invalid")
    
    with pytest.raises(TypeError):
        VALID_CONDITIONS.add("invalid")
    
    with pytest.raises(TypeError):
        VALID_RECIPIENT_TYPES.add("invalid")

def test_constant_types():
    """Test constant types."""
    # API constants
    assert isinstance(API_BASE_URL, str)
    assert isinstance(API_VERSION, str)
    
    # Test types
    assert isinstance(VALID_TEST_TYPES, frozenset)
    assert all(isinstance(test_type, str) for test_type in VALID_TEST_TYPES)
    
    # Metrics
    assert isinstance(VALID_METRICS, frozenset)
    assert all(isinstance(metric, str) for metric in VALID_METRICS)
    
    # Nodes
    assert isinstance(VALID_NODES, frozenset)
    assert all(isinstance(node, str) for node in VALID_NODES)
    
    # Conditions
    assert isinstance(VALID_CONDITIONS, frozenset)
    assert all(isinstance(condition, str) for condition in VALID_CONDITIONS)
    
    # Recipient types
    assert isinstance(VALID_RECIPIENT_TYPES, frozenset)
    assert all(isinstance(recipient_type, str) for recipient_type in VALID_RECIPIENT_TYPES)
    
    # Numeric constants
    assert isinstance(DEFAULT_TIMEOUT, int)
    assert isinstance(MAX_TIMEOUT, int)
    assert isinstance(MIN_TIMEOUT, int)
    assert isinstance(DEFAULT_FREQUENCY, int)
    assert isinstance(MAX_FREQUENCY, int)
    assert isinstance(MIN_FREQUENCY, int)
    assert isinstance(DEFAULT_RETRIES, int)
    assert isinstance(MAX_RETRIES, int)
    assert isinstance(MIN_RETRIES, int)
    assert isinstance(CACHE_TTL, int)
    
    # String constants
    assert isinstance(LOG_FORMAT, str)
    assert isinstance(LOG_LEVEL, str)
    assert isinstance(LOG_FILE, str)
    assert isinstance(CONFIG_FILE, str)
    assert isinstance(TEMPLATE_DIR, str)
    assert isinstance(CACHE_DIR, str)