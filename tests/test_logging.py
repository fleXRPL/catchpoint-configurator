"""Tests for logging configuration."""

import logging
import os
import tempfile
from unittest.mock import MagicMock, Mock, patch

import pytest

from catchpoint_configurator.logging import LogLevel, get_logger, logger_context, setup_logging


@pytest.fixture
def mock_logger():
    """Create a mock logger with necessary attributes."""
    logger = Mock(spec=logging.Logger)
    logger.handlers = []
    logger.handle = Mock()
    logger.setLevel = Mock()
    logger.addHandler = Mock()
    logger.removeHandler = Mock()
    return logger


def test_setup_logging():
    """Test setting up logging configuration."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        setup_logging()
        mock_logger.setLevel.assert_called_once_with(logging.INFO)


def test_setup_logging_debug():
    """Test setting up logging configuration in debug mode."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        setup_logging(debug=True)
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)


def test_setup_logging_with_file():
    """Test setting up logging configuration with file handler."""
    with tempfile.NamedTemporaryFile(suffix=".log") as log_file:
        with patch("logging.FileHandler") as mock_file_handler:
            with patch("logging.StreamHandler") as mock_stream_handler:
                setup_logging(level="INFO", log_file=log_file.name)
                mock_file_handler.assert_called_once_with(log_file.name)


def test_setup_logging_with_environment():
    """Test setting up logging configuration with environment variable."""
    with patch.dict(os.environ, {"CATCHPOINT_DEBUG": "true"}):
        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = Mock(spec=logging.Logger)
            mock_logger.handlers = []
            mock_get_logger.return_value = mock_logger
            with patch("logging.StreamHandler") as mock_stream_handler:
                setup_logging()
                mock_logger.setLevel.assert_called_once_with(logging.DEBUG)
                assert mock_logger.addHandler.called


def test_get_logger():
    """Test getting a logger instance."""
    logger = get_logger(__name__)
    assert isinstance(logger, logging.Logger)
    assert logger.name == __name__


def test_get_logger_with_level():
    """Test getting a logger instance with specific level."""
    logger = get_logger(__name__, level=logging.DEBUG)
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.DEBUG


def test_get_logger_with_handler():
    """Test getting a logger instance with a handler."""
    handler = logging.StreamHandler()
    logger = get_logger(__name__, handler=handler)
    assert isinstance(logger, logging.Logger)
    assert handler in logger.handlers


def test_logger_output(caplog):
    """Test logger output."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock(spec=logging.Logger)
        mock_get_logger.return_value = mock_logger
        logger = get_logger("test")

        # Test different log levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        # Check log calls
        assert mock_logger.debug.call_count == 1
        assert mock_logger.info.call_count == 1
        assert mock_logger.warning.call_count == 1
        assert mock_logger.error.call_count == 1


def test_logger_format():
    """Test logger message format."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock(spec=logging.Logger)
        mock_get_logger.return_value = mock_logger
        logger = get_logger("test")
        logger.info("Test message")
        mock_logger.info.assert_called_once_with("Test message")


def test_logger_levels():
    """Test logger level filtering."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock(spec=logging.Logger)
        mock_get_logger.return_value = mock_logger
        logger = get_logger("test", level="WARNING")
        mock_logger.setLevel.assert_called_once_with(logging.WARNING)


def test_logger_exception():
    """Test logger exception handling."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock(spec=logging.Logger)
        mock_get_logger.return_value = mock_logger
        logger = get_logger("test")

        try:
            raise ValueError("Test error")
        except ValueError as e:
            logger.exception("Exception occurred")
            mock_logger.exception.assert_called_once_with("Exception occurred")


def test_logger_context():
    """Test logger context manager."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock(spec=logging.Logger)
        mock_get_logger.return_value = mock_logger
        with logger_context("test") as logger:
            logger.info("Test message")
            mock_logger.info.assert_called_once_with("Test message")


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


def test_log_level_str():
    """Test string representation of log levels."""
    assert str(LogLevel.DEBUG) == "DEBUG"
    assert str(LogLevel.INFO) == "INFO"
    assert str(LogLevel.WARNING) == "WARNING"
    assert str(LogLevel.ERROR) == "ERROR"


def test_setup_logging_basic(mock_logger):
    """Test basic logging setup."""
    with patch("logging.getLogger", return_value=mock_logger):
        setup_logging(level=LogLevel.DEBUG)
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)


def test_setup_logging_with_file_handler(mock_logger, tmp_path):
    """Test logging setup with file handler."""
    log_file = tmp_path / "test.log"
    with patch("logging.getLogger", return_value=mock_logger):
        setup_logging(level=LogLevel.INFO, log_file=str(log_file))
        assert mock_logger.addHandler.call_count == 2  # Console and file handler


def test_get_logger_basic(mock_logger):
    """Test basic logger retrieval."""
    with patch("logging.getLogger", return_value=mock_logger):
        logger = get_logger("test")
        assert logger == mock_logger
        mock_logger.setLevel.assert_called_once_with(logging.INFO)


def test_get_logger_custom_level(mock_logger):
    """Test logger retrieval with custom level."""
    with patch("logging.getLogger", return_value=mock_logger):
        logger = get_logger("test", level=LogLevel.DEBUG)
        assert logger == mock_logger
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)


def test_get_logger_with_handlers(mock_logger):
    """Test getting a logger with handlers."""
    with patch("logging.getLogger", return_value=mock_logger):
        handler = logging.StreamHandler()
        logger = get_logger("test", handler=handler)
        assert logger == mock_logger
        assert mock_logger.addHandler.call_count == 1


def test_logger_basic_output(mock_logger):
    """Test basic logger output."""
    with patch("logging.getLogger", return_value=mock_logger):
        logger = get_logger("test")
        logger.info("Test message")
        mock_logger.info.assert_called_once_with("Test message")


def test_logger_formatter(mock_logger):
    """Test logger formatter configuration."""
    with patch("logging.getLogger", return_value=mock_logger):
        setup_logging(level=LogLevel.INFO)
        assert mock_logger.addHandler.called
        handler = mock_logger.addHandler.call_args[0][0]
        assert isinstance(handler.formatter, logging.Formatter)


def test_logger_all_levels(mock_logger):
    """Test all logging levels."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_get_logger.return_value = mock_logger
        logger = get_logger("test")
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        mock_logger.debug.assert_called_once_with("Debug message")
        mock_logger.info.assert_called_once_with("Info message")
        mock_logger.warning.assert_called_once_with("Warning message")
        mock_logger.error.assert_called_once_with("Error message")


def test_logger_exception_handling(mock_logger):
    """Test exception logging."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_get_logger.return_value = mock_logger
        logger = get_logger("test")
        try:
            raise ValueError("Test error")
        except ValueError as e:
            logger.exception("Error occurred")
            mock_logger.exception.assert_called_once_with("Error occurred")


class LoggerContext:
    """Context manager for logger testing."""

    def __init__(self, name, level=None):
        self.name = name
        self.level = level
        self.logger = None

    def __enter__(self):
        self.logger = get_logger(self.name, level=self.level)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_logger_context_manager():
    """Test logger context manager."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock(spec=logging.Logger)
        mock_get_logger.return_value = mock_logger

        with LoggerContext("test") as logger:
            logger.info("Test message")
            mock_logger.info.assert_called_once_with("Test message")
