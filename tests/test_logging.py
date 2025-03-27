"""Tests for logging configuration."""

import logging
import os
from unittest.mock import patch

import pytest

from catchpoint_configurator.logging import (
    setup_logging,
    get_logger,
    LogLevel,
)

def test_setup_logging():
    """Test setting up logging configuration."""
    with patch("logging.basicConfig") as mock_basic_config:
        setup_logging(level=LogLevel.DEBUG)
        mock_basic_config.assert_called_once_with(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

def test_setup_logging_with_file():
    """Test setting up logging configuration with file handler."""
    with tempfile.NamedTemporaryFile(suffix=".log") as log_file:
        with patch("logging.FileHandler") as mock_file_handler:
            setup_logging(level=LogLevel.INFO, log_file=log_file.name)
            mock_file_handler.assert_called_once_with(log_file.name)

def test_setup_logging_with_environment():
    """Test setting up logging configuration with environment variable."""
    with patch.dict(os.environ, {"CATCHPOINT_DEBUG": "true"}):
        with patch("logging.basicConfig") as mock_basic_config:
            setup_logging()
            mock_basic_config.assert_called_once_with(
                level=logging.DEBUG,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

def test_get_logger():
    """Test getting a logger instance."""
    logger = get_logger("test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
    assert logger.level == logging.INFO

def test_get_logger_with_level():
    """Test getting a logger instance with custom level."""
    logger = get_logger("test", level=LogLevel.DEBUG)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
    assert logger.level == logging.DEBUG

def test_logger_output(caplog):
    """Test logger output."""
    logger = get_logger("test")
    
    # Test different log levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Check log records
    assert len(caplog.records) == 4
    assert caplog.records[0].levelname == "DEBUG"
    assert caplog.records[1].levelname == "INFO"
    assert caplog.records[2].levelname == "WARNING"
    assert caplog.records[3].levelname == "ERROR"
    
    # Check log messages
    assert caplog.records[0].message == "Debug message"
    assert caplog.records[1].message == "Info message"
    assert caplog.records[2].message == "Warning message"
    assert caplog.records[3].message == "Error message"

def test_logger_format(caplog):
    """Test logger message format."""
    logger = get_logger("test")
    logger.info("Test message")
    
    # Check log record format
    record = caplog.records[0]
    assert record.name == "test"
    assert record.levelname == "INFO"
    assert record.message == "Test message"
    assert "asctime" in record.__dict__

def test_logger_propagation():
    """Test logger propagation."""
    parent_logger = get_logger("parent")
    child_logger = get_logger("parent.child")
    
    assert child_logger.parent == parent_logger
    assert child_logger.propagate is True

def test_logger_handlers():
    """Test logger handlers."""
    logger = get_logger("test")
    
    # Add a test handler
    test_handler = logging.StreamHandler()
    logger.addHandler(test_handler)
    
    assert len(logger.handlers) == 1
    assert logger.handlers[0] == test_handler

def test_logger_levels():
    """Test logger level filtering."""
    logger = get_logger("test", level=LogLevel.WARNING)
    
    # Test different log levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Check filtered records
    assert len(logger.handlers[0].filters) == 0
    assert logger.level == logging.WARNING

def test_logger_exception():
    """Test logger exception handling."""
    logger = get_logger("test")
    
    try:
        raise ValueError("Test error")
    except ValueError as e:
        logger.exception("Exception occurred")
    
    # Check exception logging
    assert len(logger.handlers[0].filters) == 0
    assert "Exception occurred" in logger.handlers[0].stream.getvalue()

def test_logger_context():
    """Test logger context manager."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = logging.Logger("test")
        mock_get_logger.return_value = mock_logger
        
        with get_logger("test") as logger:
            assert logger == mock_logger
            logger.info("Test message")
        
        # Check cleanup
        assert len(mock_logger.handlers) == 0

def test_log_level_enum():
    """Test LogLevel enum."""
    assert LogLevel.DEBUG == logging.DEBUG
    assert LogLevel.INFO == logging.INFO
    assert LogLevel.WARNING == logging.WARNING
    assert LogLevel.ERROR == logging.ERROR
    assert LogLevel.CRITICAL == logging.CRITICAL
    
    # Test string representation
    assert str(LogLevel.DEBUG) == "DEBUG"
    assert str(LogLevel.INFO) == "INFO"
    assert str(LogLevel.WARNING) == "WARNING"
    assert str(LogLevel.ERROR) == "ERROR"
    assert str(LogLevel.CRITICAL) == "CRITICAL"
    
    # Test comparison
    assert LogLevel.DEBUG < LogLevel.INFO
    assert LogLevel.INFO < LogLevel.WARNING
    assert LogLevel.WARNING < LogLevel.ERROR
    assert LogLevel.ERROR < LogLevel.CRITICAL 