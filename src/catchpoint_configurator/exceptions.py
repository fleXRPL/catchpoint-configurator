"""Custom exceptions for Catchpoint Configurator."""

from typing import Any, Dict, Optional


class CatchpointConfiguratorError(Exception):
    """Base exception for all Catchpoint Configurator errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize the error.

        Args:
            message: Error message
            details: Optional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details


class ValidationError(CatchpointConfiguratorError):
    """Raised when configuration validation fails."""

    pass


class ConfigError(CatchpointConfiguratorError):
    """Raised when there is a configuration error."""

    pass


class ContestError(CatchpointConfiguratorError):
    """Raised when there is a contest error."""

    pass


class DeploymentError(CatchpointConfiguratorError):
    """Raised when deployment fails."""

    pass


class APIError(CatchpointConfiguratorError):
    """Raised when an API request fails."""

    pass


class AuthError(CatchpointConfiguratorError):
    """Raised when authentication fails."""

    pass


class RateLimitError(CatchpointConfiguratorError):
    """Raised when API rate limit is exceeded."""

    pass


class NotFoundError(CatchpointConfiguratorError):
    """Raised when a resource is not found."""

    pass


class AuthenticationError(CatchpointConfiguratorError):
    """Raised when authentication fails."""

    pass


class TemplateError(CatchpointConfiguratorError):
    """Raised when template rendering fails."""

    def __init__(self, message: str, details: dict = None):
        """Initialize the error.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.details = details or {}
