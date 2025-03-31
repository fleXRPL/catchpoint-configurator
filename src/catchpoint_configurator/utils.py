"""
Utility functions for Catchpoint Configurator.
"""

import logging
import os
import re
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import yaml

from .exceptions import ValidationError


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def get_env_var(name: str, required: bool = True) -> Optional[str]:
    """Get an environment variable.

    Args:
        name: Environment variable name
        required: Whether the variable is required

    Returns:
        Environment variable value or None if not required and not found

    Raises:
        ValidationError: If required variable is not found
    """
    value = os.environ.get(name)
    if required and not value:
        raise ValidationError(f"Required environment variable {name} not found")
    return value


def load_yaml(file_path: str) -> Dict[str, Any]:
    """Load YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        YAML data as dictionary

    Raises:
        FileNotFoundError: If file does not exist
        yaml.YAMLError: If YAML is invalid
    """
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in {file_path}: {e}")


def save_yaml(data: Any, file_path: str) -> None:
    """Save data to YAML file.

    Args:
        data: Data to save
        file_path: Path to YAML file

    Raises:
        yaml.YAMLError: If YAML is invalid
    """
    try:
        # Try to serialize the data to YAML first to catch any issues
        yaml_str = yaml.dump(data, default_flow_style=False)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Failed to serialize data to YAML: {e}")

    try:
        with open(file_path, "w") as f:
            f.write(yaml_str)
    except IOError as e:
        raise IOError(f"Failed to write YAML file: {e}")


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration.

    Args:
        level: Logging level
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def validate_url(url: str) -> bool:
    """Validate URL.

    Args:
        url: URL to validate

    Returns:
        True if URL is valid
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except Exception:
        return False


def validate_email(email: str) -> bool:
    """Validate an email address.

    Args:
        email: Email address to validate

    Returns:
        True if the email address is valid
    """
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_slack_channel(channel: str) -> bool:
    """Validate Slack channel name.

    Args:
        channel: Channel name to validate

    Returns:
        True if channel name is valid
    """
    return bool(re.match(r"^#[a-z0-9_-]+$", channel))


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


def parse_duration(duration_str: str) -> int:
    """Parse a duration string into seconds.

    Args:
        duration_str: Duration string (e.g., "1h", "30m", "1d 6h")

    Returns:
        Duration in seconds

    Raises:
        ValueError: If the duration string is invalid
    """
    total_seconds = 0
    parts = duration_str.split()

    for part in parts:
        if not part[-1].isalpha() or not part[:-1].isdigit():
            raise ValueError(f"Invalid duration format: {part}")

        value = int(part[:-1])
        unit = part[-1]

        if unit == "s":
            total_seconds += value
        elif unit == "m":
            total_seconds += value * 60
        elif unit == "h":
            total_seconds += value * 3600
        elif unit == "d":
            total_seconds += value * 86400
        else:
            raise ValueError(f"Invalid duration unit: {unit}")

    return total_seconds


def validate_environment() -> None:
    """
    Validate required environment variables are set.

    Raises:
        EnvironmentError: If required variables are missing
    """
    required_vars = ["CATCHPOINT_CLIENT_ID", "CATCHPOINT_CLIENT_SECRET"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


def sanitize_string(value: str) -> str:
    """
    Sanitize a string for safe usage.

    Args:
        value: String to sanitize

    Returns:
        Sanitized string
    """
    # Remove potentially dangerous characters
    return "".join(c for c in value if c.isalnum() or c in "._- ")


def format_error(error: Exception) -> str:
    """
    Format an exception for error messages.

    Args:
        error: Exception to format

    Returns:
        Formatted error message
    """
    return f"{error.__class__.__name__}: {str(error)}"


def get_version() -> str:
    """
    Get the package version.

    Returns:
        Package version string
    """
    return "1.0.0"  # TODO: Use dynamic version
