"""
Utility functions for Catchpoint Configurator.
"""

import logging
import os
import sys
from typing import Any, Dict, Optional

import yaml

logger = logging.getLogger(__name__)

def load_yaml(path: str) -> Dict[str, Any]:
    """Load a YAML file.

    Args:
        path: Path to the YAML file

    Returns:
        Dictionary containing the YAML data

    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the YAML is invalid
    """
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {path}: {e}")
        raise

def save_yaml(data: Dict[str, Any], path: str) -> None:
    """Save data to a YAML file.

    Args:
        data: Dictionary to save
        path: Path to save the YAML file

    Raises:
        IOError: If the file can't be written
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
    except IOError as e:
        logger.error(f"Failed to write {path}: {e}")
        raise

def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable.

    Args:
        name: Name of the environment variable
        default: Default value if not set

    Returns:
        Value of the environment variable or default
    """
    return os.environ.get(name, default)

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
    """Validate a URL.

    Args:
        url: URL to validate

    Returns:
        True if the URL is valid
    """
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def format_duration(seconds: int) -> str:
    """Format a duration in seconds to a human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}m{seconds}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h{minutes}m"

def validate_environment() -> None:
    """
    Validate required environment variables are set.

    Raises:
        EnvironmentError: If required variables are missing
    """
    required_vars = ["DATADOG_API_KEY", "DATADOG_APP_KEY"]
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
    from . import __version__

    return __version__
