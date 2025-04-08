"""Logging configuration for the Catchpoint Configurator."""

import logging
import os
from enum import Enum
from typing import Optional, Union


class LogLevel(Enum):
    """Log level enumeration."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __str__(self) -> str:
        """Return string representation of log level."""
        return self.name

    def __eq__(self, other) -> bool:
        """Compare log level with another level."""
        if isinstance(other, LogLevel):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        return NotImplemented

    def __lt__(self, other) -> bool:
        """Compare if this level is less than another level."""
        if isinstance(other, LogLevel):
            return self.value < other.value
        if isinstance(other, int):
            return self.value < other
        return NotImplemented

    def __le__(self, other) -> bool:
        """Compare if this level is less than or equal to another level."""
        if isinstance(other, LogLevel):
            return self.value <= other.value
        if isinstance(other, int):
            return self.value <= other
        return NotImplemented

    def __gt__(self, other) -> bool:
        """Compare if this level is greater than another level."""
        if isinstance(other, LogLevel):
            return self.value > other.value
        if isinstance(other, int):
            return self.value > other
        return NotImplemented

    def __ge__(self, other) -> bool:
        """Compare if this level is greater than or equal to another level."""
        if isinstance(other, LogLevel):
            return self.value >= other.value
        if isinstance(other, int):
            return self.value >= other
        return NotImplemented


def _get_log_level(level: Union[str, LogLevel, None]) -> LogLevel:
    """Convert string or LogLevel to LogLevel enum.

    Args:
        level: Log level as string or LogLevel enum

    Returns:
        LogLevel enum value
    """
    if isinstance(level, LogLevel):
        return level
    if isinstance(level, str):
        try:
            return LogLevel[level.upper()]
        except KeyError:
            raise ValueError(f"Invalid log level: {level}")
    if level is None:
        return LogLevel.INFO
    raise ValueError(f"Invalid log level type: {type(level)}")


def setup_logging(
    level: Union[str, LogLevel] = LogLevel.INFO, log_file: Optional[str] = None
) -> None:
    """Set up logging configuration.

    Args:
        level: Log level to use (string or LogLevel enum)
        log_file: Optional log file path
    """
    # Set log level from environment variable
    if os.environ.get("CATCHPOINT_DEBUG", "").lower() == "true":
        level = LogLevel.DEBUG

    # Convert level to LogLevel enum
    log_level = _get_log_level(level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.value)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    root_logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        root_logger.addHandler(file_handler)


def get_logger(
    name: str, level: Optional[Union[str, LogLevel]] = None, add_handlers: bool = False
) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name
        level: Optional log level (string or LogLevel enum)
        add_handlers: Whether to add handlers to the logger

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)

    if level is not None:
        log_level = _get_log_level(level)
        logger.setLevel(log_level.value)

    if add_handlers and not logger.handlers:
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(console_handler)

    return logger


class LoggerContext:
    """Context manager for logger."""

    def __init__(
        self, name: str, level: Optional[Union[str, LogLevel]] = None, add_handlers: bool = False
    ):
        """Initialize logger context.

        Args:
            name: Logger name
            level: Optional log level (string or LogLevel enum)
            add_handlers: Whether to add handlers to the logger
        """
        self.name = name
        self.level = level
        self.add_handlers = add_handlers
        self.logger = None

    def __enter__(self) -> logging.Logger:
        """Enter context and get logger.

        Returns:
            Logger instance
        """
        self.logger = get_logger(self.name, level=self.level, add_handlers=self.add_handlers)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        pass
