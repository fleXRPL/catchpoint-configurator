"""
Configuration parsing and validation module.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

import yaml
from jsonschema import ValidationError, validate

from catchpoint_configurator.types import (
    AlertConfig,
    DashboardConfig,
    LayoutConfig,
    TestConfig,
)

logger = logging.getLogger(__name__)

# Schema for dashboard configuration validation
DASHBOARD_SCHEMA = {
    "type": "object",
    "required": ["version", "dashboards"],
    "properties": {
        "version": {"type": "string"},
        "defaults": {
            "type": "object",
            "properties": {
                "layout_type": {"type": "string", "enum": ["ordered", "free"]},
                "refresh_interval": {"type": "integer", "minimum": 0},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
        },
        "dashboards": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "widgets"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "layout_type": {"type": "string", "enum": ["ordered", "free"]},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "widgets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["title", "type"],
                            "properties": {
                                "title": {"type": "string"},
                                "type": {"type": "string"},
                                "query": {"type": "string"},
                                "size": {"type": "string"},
                                "visualization": {"type": "object"},
                                "conditional_formats": {
                                    "type": "array",
                                    "items": {"type": "object"},
                                },
                                "custom_links": {
                                    "type": "array",
                                    "items": {"type": "object"},
                                },
                            },
                        },
                    },
                    "template_variables": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name"],
                            "properties": {
                                "name": {"type": "string"},
                                "prefix": {"type": "string"},
                                "default": {"type": "string"},
                            },
                        },
                    },
                },
            },
        },
    },
}


class ConfigParser:
    """Parser for dashboard configuration files."""

    def __init__(self, config_path: str) -> None:
        """
        Initialize the configuration parser.

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
        """
        Parse and validate the configuration file.

        Returns:
            Dict containing the parsed configuration
        """
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)

            # Validate against schema
            self._validate_config(config)

            # Apply defaults
            self._apply_defaults(config)

            logger.info(f"Successfully parsed configuration from {self.config_path}")
            return config

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing configuration: {e}")
            raise

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate configuration against schema.

        Args:
            config: Configuration dictionary to validate
        """
        try:
            validate(instance=config, schema=DASHBOARD_SCHEMA)
        except ValidationError as e:
            logger.error(f"Configuration validation failed: {e.message}")
            raise

    def _apply_defaults(self, config: Dict[str, Any]) -> None:
        """
        Apply default values to dashboard configurations.

        Args:
            config: Configuration dictionary to update
        """
        defaults = config.get("defaults", {})
        for dashboard in config["dashboards"]:
            # Apply layout type
            if "layout_type" not in dashboard and "layout_type" in defaults:
                dashboard["layout_type"] = defaults["layout_type"]

            # Apply tags
            if "tags" in defaults:
                dashboard_tags = set(dashboard.get("tags", []))
                dashboard_tags.update(defaults["tags"])
                dashboard["tags"] = list(dashboard_tags)

            # Apply refresh interval
            if "refresh_interval" in defaults:
                dashboard["refresh_interval"] = defaults["refresh_interval"]


class ConfigValidator:
    """Configuration validator."""

    def __init__(self):
        """Initialize validator."""
        self.schemas = self._load_schemas()

    def _load_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Load JSON schemas.

        Returns:
            Dictionary of schemas
        """
        schemas_dir = Path(__file__).parent / "schemas"
        schemas = {}
        for schema_file in schemas_dir.glob("*.json"):
            with open(schema_file) as f:
                schema = json.load(f)
                schemas[schema_file.stem] = schema
        return schemas

    def validate_test_config(self, config: TestConfig) -> bool:
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
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        valid_types = ["web", "api", "transaction", "dns", "traceroute"]
        if config["type"] not in valid_types:
            raise ValidationError(f"Invalid test type: {config['type']}")

        return True

    def validate_alert_config(self, config: AlertConfig) -> bool:
        """Validate an alert configuration.

        Args:
            config: Alert configuration to validate

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["name", "metric", "operator", "threshold", "recipients"]
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        valid_metrics = ["response_time", "availability", "throughput"]
        if config["metric"] not in valid_metrics:
            raise ValidationError(f"Invalid metric: {config['metric']}")

        valid_operators = [">", "<", ">=", "<=", "=="]
        if config["operator"] not in valid_operators:
            raise ValidationError(f"Invalid operator: {config['operator']}")

        for recipient in config["recipients"]:
            if not isinstance(recipient, dict) or "email" not in recipient:
                raise ValidationError("Invalid recipient format")

        return True

    def validate_dashboard_config(self, config: DashboardConfig) -> bool:
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
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        if config["type"] != "dashboard":
            raise ValidationError(f"Invalid type: {config['type']}")

        for widget in config["layout"]:
            self.validate_layout_config(widget)

        return True

    def validate_layout_config(self, config: LayoutConfig) -> bool:
        """Validate a layout configuration.

        Args:
            config: Layout configuration to validate

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["type", "title", "test_id"]
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        valid_types = ["chart", "table", "gauge"]
        if config["type"] not in valid_types:
            raise ValidationError(f"Invalid widget type: {config['type']}")

        return True

    def validate(self, config: Dict[str, Any]) -> bool:
        """Validate a configuration against its schema.

        Args:
            config: Configuration dictionary to validate

        Returns:
            True if validation succeeds

        Raises:
            ValidationError: If validation fails
        """
        if "type" not in config:
            raise ValidationError("Configuration must specify a type")

        config_type = config["type"]
        if config_type not in [
            "web",
            "api",
            "transaction",
            "dns",
            "traceroute",
            "dashboard",
        ]:
            raise ValidationError(f"Unknown configuration type: {config_type}")

        if config_type == "dashboard":
            return self.validate_dashboard_config(config)
        else:
            return self.validate_test_config(config)

    def validate_yaml(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate YAML data.

        Args:
            data: YAML data to validate

        Returns:
            Validated YAML data

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(data, dict):
            raise ValidationError("YAML data must be a dictionary")

        return self.validate(data)
