"""Logging configuration for the Catchpoint Configurator."""

import logging
import os
from contextlib import contextmanager
from enum import Enum
from typing import Any, Generator, Optional, Union

from .constants import LOG_FILE

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    """Log level enumeration."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __eq__(self, other: Any) -> bool:
        """Compare log levels."""
        if isinstance(other, LogLevel):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, str):
            try:
                return self.value == LogLevel[other.upper()].value
            except KeyError:
                return False
        return False

    def __str__(self) -> str:
        """Return string representation."""
        return self.name


def _get_log_level(level: Union[str, int, LogLevel, None]) -> int:
    """Convert string or LogLevel to integer level value."""
    if isinstance(level, LogLevel):
        return level.value
    if isinstance(level, str):
        try:
            return LogLevel[level.upper()].value
        except KeyError:
            raise ValueError(f"Invalid log level: {level}")
    if isinstance(level, int):
        if level in [log_level.value for log_level in LogLevel]:
            return level
        raise ValueError(f"Invalid log level: {level}")
    return LogLevel.INFO.value


def setup_logging(
    level: Union[str, int, LogLevel, None] = None,
    log_file: Optional[str] = None,
    debug: bool = False,
) -> None:
    """Set up logging configuration."""
    if os.environ.get("CATCHPOINT_DEBUG") == "true":
        debug = True

    log_level = LogLevel.DEBUG.value if debug else _get_log_level(level)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Create file handler if log file is specified
    if log_file or LOG_FILE:
        file_path = log_file or LOG_FILE
        if file_path:
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)


def get_logger(
    name: str,
    level: Union[str, int, LogLevel, None] = None,
    handler: Optional[logging.Handler] = None,
) -> logging.Logger:
    """Get a logger instance."""
    logger = logging.getLogger(name)
    log_level = _get_log_level(level)
    logger.setLevel(log_level)

    if handler:
        handler.setLevel(log_level)
        logger.addHandler(handler)

    return logger


@contextmanager
def logger_context(
    name: str,
    level: Union[str, int, LogLevel, None] = None,
    handler: Optional[logging.Handler] = None,
) -> Generator[logging.Logger, None, None]:
    """Get a logger instance as a context manager."""
    logger = get_logger(name, level, handler)
    try:
        yield logger
    finally:
        if handler:
            logger.removeHandler(handler)
