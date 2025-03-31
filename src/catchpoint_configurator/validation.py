"""Validation module for Catchpoint Configurator."""

from typing import Any, Dict

import yaml

from .constants import (
    VALID_CONDITIONS,
    VALID_METRICS,
    VALID_NODES,
    VALID_RECIPIENT_TYPES,
    VALID_TEST_TYPES,
    VALID_WIDGET_TYPES,
)
from .exceptions import ValidationError
from .utils import validate_url


def validate_yaml(data: Any) -> bool:
    """Validate YAML data.

    Args:
        data: Data to validate

    Returns:
        True if validation passes

    Raises:
        ValidationError: If validation fails
    """
    try:
        if isinstance(data, str):
            data = yaml.safe_load(data)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML syntax: {str(e)}")

    if not isinstance(data, dict):
        raise ValidationError("YAML data must be a dictionary")

    if "url" in data and not validate_url(data["url"]):
        raise ValidationError(f"Invalid URL: {data['url']}")

    return True


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate a configuration.

    Args:
        config: Configuration to validate

    Returns:
        True if validation passes

    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(config, dict):
        raise ValidationError("Configuration must be a dictionary")

    if "type" not in config:
        raise ValidationError("Configuration must have a type")

    config_type = config["type"]
    if config_type not in VALID_TEST_TYPES:
        raise ValidationError(f"Invalid configuration type: {config_type}")

    if config_type == "web":
        validate_test_config(config)
    elif config_type == "dashboard":
        validate_dashboard_config(config)
    else:
        validate_test_config(config)

    return True


def validate_test_config(config: Dict[str, Any]) -> bool:
    """Validate a test configuration.

    Args:
        config: Test configuration to validate

    Returns:
        True if validation passes

    Raises:
        ValidationError: If validation fails
    """
    required_fields = ["name", "type", "url", "frequency"]
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    if not validate_url(config["url"]):
        raise ValidationError(f"Invalid URL: {config['url']}")

    if not isinstance(config["frequency"], int) or config["frequency"] <= 0:
        raise ValidationError("Invalid frequency: must be a positive integer")

    if "nodes" in config:
        invalid_nodes = [node for node in config["nodes"] if node not in VALID_NODES]
        if invalid_nodes:
            raise ValidationError(f"Invalid nodes: {', '.join(invalid_nodes)}")

    if "alerts" in config:
        for alert in config["alerts"]:
            validate_alert_config(alert)

    return True


def validate_alert_config(config: Dict[str, Any]) -> bool:
    """Validate an alert configuration.

    Args:
        config: Alert configuration to validate

    Returns:
        True if validation passes

    Raises:
        ValidationError: If validation fails
    """
    required_fields = ["metric", "threshold", "condition", "recipients"]
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    if config["metric"] not in VALID_METRICS:
        raise ValidationError(f"Invalid metric: {config['metric']}")

    if not isinstance(config["threshold"], (int, float)):
        raise ValidationError("Invalid threshold: must be a number")

    if config["condition"] not in VALID_CONDITIONS:
        raise ValidationError(f"Invalid condition: {config['condition']}")

    if not isinstance(config["recipients"], list) or not config["recipients"]:
        raise ValidationError("Recipients must be a non-empty list")

    for recipient in config["recipients"]:
        if isinstance(recipient, str):
            recipient = {"type": "email", "address": recipient}
        validate_recipient_config(recipient)

    return True


def validate_recipient_config(config: Dict[str, str]) -> None:
    """Validate a recipient configuration.

    Args:
        config: Recipient configuration to validate

    Raises:
        ValidationError: If validation fails
    """
    if isinstance(config, str):
        config = {"type": "email", "address": config}

    required_fields = ["type", "address"]
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    if config["type"] not in VALID_RECIPIENT_TYPES:
        raise ValidationError(f"Invalid recipient type: {config['type']}")


def validate_dashboard_config(config: Dict[str, Any]) -> bool:
    """Validate a dashboard configuration.

    Args:
        config: Dashboard configuration to validate

    Returns:
        True if validation passes

    Raises:
        ValidationError: If validation fails
    """
    required_fields = ["name", "layout"]
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    if not isinstance(config["layout"], list):
        raise ValidationError("Layout must be a list of widgets")

    for widget in config["layout"]:
        validate_layout_config(widget)

    return True


def validate_layout_config(config: Dict[str, Any]) -> None:
    """Validate a layout configuration.

    Args:
        config: Layout configuration to validate

    Raises:
        ValidationError: If validation fails
    """
    required_fields = ["type", "title", "test_id"]
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    if config["type"] not in VALID_WIDGET_TYPES:
        raise ValidationError(f"Invalid widget type: {config['type']}")

    if "test_id" not in config:
        raise ValidationError("Each widget must have a test_id")

    if "title" not in config:
        raise ValidationError("Each widget must have a title")
