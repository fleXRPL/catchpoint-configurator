"""Configuration management for the Catchpoint Configurator."""

import logging
import os
from typing import Any, Dict

import yaml

from .constants import VALID_NODES
from .exceptions import ValidationError
from .utils import validate_url

logger = logging.getLogger(__name__)


class ConfigValidator:
    """Configuration validator."""

    def __init__(self) -> None:
        """Initialize the configuration validator."""
        self.logger = logger

    def validate(self, config: Dict[str, Any]) -> bool:
        """Basic validation for MVP.

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
        if config_type in ["test", "web"]:
            return self.validate_test_config(config)
        elif config_type == "dashboard":
            return self.validate_dashboard_config(config)
        else:
            raise ValidationError(f"Invalid configuration type: {config_type}")

    def validate_test_config(self, config: Dict[str, Any]) -> bool:
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

        return True

    def validate_dashboard_config(self, config: Dict[str, Any]) -> bool:
        """Validate a dashboard configuration.

        Args:
            config: Dashboard configuration to validate

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["name", "type", "layout"]
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        if not isinstance(config["layout"], list):
            raise ValidationError("Layout must be a list of widgets")

        return True

    def validate_alert_config(self, config: Dict[str, Any]) -> bool:
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

        valid_metrics = ["response_time", "availability", "throughput"]
        if config["metric"] not in valid_metrics:
            raise ValidationError(f"Invalid metric: {config['metric']}")

        valid_conditions = [">", "<", ">=", "<=", "=="]
        if config["condition"] not in valid_conditions:
            raise ValidationError(f"Invalid condition: {config['condition']}")

        if not isinstance(config["threshold"], (int, float)) or config["threshold"] <= 0:
            raise ValidationError("Threshold must be a positive number")

        if not isinstance(config["recipients"], list) or not config["recipients"]:
            raise ValidationError("Recipients must be a non-empty list")

        return True

    def validate_yaml(self, data: Any) -> bool:
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

        return self.validate(data)


class ConfigParser:
    """Parser for dashboard configuration files."""

    def __init__(self, config_path: str) -> None:
        """Initialize the configuration parser.

        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = config_path
        self._validate_path()

    def _validate_path(self) -> None:
        """Validate that the configuration file exists and is readable."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        if not os.path.isfile(self.config_path):
            raise ValueError(f"Configuration path is not a file: {self.config_path}")
        if not os.access(self.config_path, os.R_OK):
            raise PermissionError(f"Cannot read configuration file: {self.config_path}")

    def parse(self) -> Dict[str, Any]:
        """Parse and apply defaults to the configuration file.

        Returns:
            Dict containing the parsed configuration
        """
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)

            logger.info(f"Successfully parsed configuration from {self.config_path}")
            return config

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing configuration: {e}")
            raise
