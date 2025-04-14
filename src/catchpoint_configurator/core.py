"""
Core functionality for the Catchpoint Configurator.
"""

import logging
from typing import Any, Dict, List, Optional, Union

import yaml

from .api import APIError, CatchpointAPI
from .config import ConfigValidator
from .exceptions import DeploymentError, ValidationError
from .utils import load_yaml, save_yaml

logger = logging.getLogger(__name__)


class CatchpointConfigurator:
    """Main class for managing Catchpoint configurations."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        debug: bool = False,
        timeout: int = 30,
    ):
        """Initialize the Catchpoint Configurator.

        Args:
            client_id: Catchpoint API client ID
            client_secret: Catchpoint API client secret
            debug: Enable debug logging
            timeout: API request timeout in seconds
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.validator = ConfigValidator()
        self.api = CatchpointAPI(
            client_id=client_id,
            client_secret=client_secret,
            timeout=timeout,
            debug=debug,
        )

        if debug:
            logging.basicConfig(level=logging.DEBUG)

    def validate(self, config: Union[str, Dict[str, Any]]) -> bool:
        """Validate a configuration.

        Args:
            config: Configuration dictionary or path to YAML file

        Returns:
            True if validation succeeds

        Raises:
            ValidationError: If validation fails
        """
        if isinstance(config, str):
            config = load_yaml(config)
        return self.validator.validate(config)

    def deploy(
        self,
        config_path: str,
        dry_run: bool = False,
        force: bool = False,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Deploy a configuration to Catchpoint.

        Args:
            config_path: Path to the configuration file
            dry_run: If True, only validate the configuration
            force: If True, overwrite existing configurations
            timeout: Override the default timeout for this operation

        Returns:
            Dict containing deployment results

        Raises:
            ValidationError: If the configuration is invalid
            DeploymentError: If deployment fails
        """
        config = load_yaml(config_path)
        self.validate(config)

        if dry_run:
            return {"status": "validated", "config": config}

        config_type = config["type"]
        try:
            if config_type in ["test", "web"]:
                # Check if test exists
                existing_tests = self.api.list_tests({"name": config["name"]})
                if existing_tests and not force:
                    raise ValidationError(
                        f"Test '{config['name']}' already exists. Use --force to overwrite."
                    )

                if existing_tests:
                    result = self.api.update_test(existing_tests[0]["id"], config)
                    action = "updated"
                else:
                    result = self.api.create_test(config)
                    action = "created"

                return {
                    "status": "success",
                    "action": action,
                    "test_id": result["id"],
                    "name": config["name"],
                }

            elif config_type == "dashboard":
                # Check if dashboard exists
                existing_dashboards = self.api.list_dashboards({"name": config["name"]})
                if existing_dashboards and not force:
                    raise ValidationError(
                        f"Dashboard '{config['name']}' already exists. Use --force to overwrite."
                    )

                if existing_dashboards:
                    result = self.api.update_dashboard(existing_dashboards[0]["id"], config)
                    action = "updated"
                else:
                    result = self.api.create_dashboard(config)
                    action = "created"

                return {
                    "status": "success",
                    "action": action,
                    "dashboard_id": result["id"],
                    "name": config["name"],
                }

            else:
                raise ValidationError(f"Unknown configuration type: {config_type}")

        except APIError as e:
            raise DeploymentError(f"Failed to deploy configuration: {e}") from e

    def list(self, config_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List existing configurations.

        Args:
            config_type: Filter by configuration type

        Returns:
            List of configuration dictionaries

        Raises:
            APIError: If the API request fails
        """
        try:
            if config_type == "test" or not config_type:
                tests = self.api.list_tests()
                for test in tests:
                    test["type"] = "test"
                if config_type == "test":
                    return tests

            if config_type == "dashboard" or not config_type:
                dashboards = self.api.list_dashboards()
                for dashboard in dashboards:
                    dashboard["type"] = "dashboard"
                if config_type == "dashboard":
                    return dashboards

            if not config_type:
                return tests + dashboards

            return []

        except APIError as e:
            raise APIError(f"Failed to list configurations: {e}")

    def apply_template(
        self,
        template_name: str,
        variables: Dict[str, Any],
        output_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Apply a template with variables.

        Args:
            template_name: Name of the template to apply
            variables: Template variables
            output_path: Optional path to save the rendered configuration

        Returns:
            Rendered configuration dictionary

        Raises:
            TemplateError: If template rendering fails
        """
        # TODO: Implement template logic
        config = {}

        if output_path:
            save_yaml(config, output_path)

        return config

    def update(
        self,
        config_path: str,
        updates: Dict[str, Any],
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Update an existing configuration.

        Args:
            config_path: Path to the configuration file
            updates: Updates to apply
            dry_run: If True, only show what would be updated

        Returns:
            Updated configuration dictionary

        Raises:
            ValidationError: If the updated configuration is invalid
            UpdateError: If update fails
        """
        config = load_yaml(config_path)
        config.update(updates)
        self.validate(config)

        if dry_run:
            return {"status": "validated", "config": config}

        try:
            if config["type"] == "test":
                existing_tests = self.api.list_tests({"name": config["name"]})
                if not existing_tests:
                    raise ValidationError(f"Test '{config['name']}' not found")
                result = self.api.update_test(existing_tests[0]["id"], config)
            elif config["type"] == "dashboard":
                existing_dashboards = self.api.list_dashboards({"name": config["name"]})
                if not existing_dashboards:
                    raise ValidationError(f"Dashboard '{config['name']}' not found")
                result = self.api.update_dashboard(existing_dashboards[0]["id"], config)
            else:
                raise ValidationError(f"Unknown configuration type: {config['type']}")

            return {
                "status": "success",
                "action": "updated",
                "id": result["id"],
                "name": config["name"],
            }

        except APIError as e:
            raise UpdateError(f"Failed to update configuration: {e}")

    def delete(
        self,
        config_path: str,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Delete a configuration.

        Args:
            config_path: Path to the configuration file
            dry_run: If True, only show what would be deleted

        Returns:
            Dict containing deletion results

        Raises:
            DeletionError: If deletion fails
        """
        config = load_yaml(config_path)
        self.validate(config)

        if dry_run:
            return {"status": "would_delete", "path": config_path}

        try:
            if config["type"] == "test":
                existing_tests = self.api.list_tests({"name": config["name"]})
                if not existing_tests:
                    raise ValidationError(f"Test '{config['name']}' not found")
                self.api.delete_test(existing_tests[0]["id"])
            elif config["type"] == "dashboard":
                existing_dashboards = self.api.list_dashboards({"name": config["name"]})
                if not existing_dashboards:
                    raise ValidationError(f"Dashboard '{config['name']}' not found")
                self.api.delete_dashboard(existing_dashboards[0]["id"])
            else:
                raise ValidationError(f"Unknown configuration type: {config['type']}")

            return {
                "status": "success",
                "action": "deleted",
                "name": config["name"],
            }

        except APIError as e:
            raise DeletionError(f"Failed to delete configuration: {e}")

    def export(
        self,
        config_path: str,
        output_path: Optional[str] = None,
        format: str = "yaml",
    ) -> Union[str, Dict[str, Any]]:
        """Export a configuration.

        Args:
            config_path: Path to the configuration file
            output_path: Optional path to save the export
            format: Export format (yaml or json)

        Returns:
            Exported configuration

        Raises:
            ExportError: If export fails
        """
        config = load_yaml(config_path)

        if format == "json":
            output = config
        else:
            output = yaml.dump(config, default_flow_style=False)

        if output_path:
            with open(output_path, "w") as f:
                f.write(output)

        return output

    def import_config(
        self,
        import_path: str,
        output_path: Optional[str] = None,
        format: str = "yaml",
    ) -> Dict[str, Any]:
        """Import a configuration.

        Args:
            import_path: Path to the configuration to import
            output_path: Optional path to save the imported configuration
            format: Import format (yaml or json)

        Returns:
            Imported configuration dictionary

        Raises:
            ImportError: If import fails
        """
        if format == "json":
            with open(import_path, "r") as f:
                config = f.read()
        else:
            config = load_yaml(import_path)

        self.validate(config)

        if output_path:
            save_yaml(config, output_path)

        return config

    def _get_test_id_by_name(self, name: str) -> str:
        """Get test ID by name."""
        tests = self.list_tests()
        for test in tests:
            if test["name"] == name:
                return test["id"]
        raise ValidationError(f"Test '{name}' not found")


class UpdateError(Exception):
    """Raised when update fails."""

    pass


class DeletionError(Exception):
    """Raised when deletion fails."""

    pass
