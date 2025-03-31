"""Tests for custom exceptions."""

import pytest

from catchpoint_configurator.exceptions import (
    APIError,
    AuthError,
    CatchpointConfiguratorError,
    ConfigError,
    DeploymentError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from catchpoint_configurator.template import TemplateError


def test_base_exception():
    """Test base exception."""
    error = CatchpointConfiguratorError("Test error")
    assert str(error) == "Test error"
    assert error.message == "Test error"
    assert error.details is None


def test_base_exception_with_details():
    """Test base exception with details."""
    details = {"field": "test", "error": "invalid"}
    error = CatchpointConfiguratorError("Test error", details)
    assert str(error) == "Test error"
    assert error.message == "Test error"
    assert error.details == details


def test_validation_error():
    """Test validation error."""
    error = ValidationError("Invalid configuration")
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Invalid configuration"
    assert error.message == "Invalid configuration"


def test_validation_error_with_details():
    """Test validation error with details."""
    details = {"field": "url", "error": "invalid URL"}
    error = ValidationError("Invalid configuration", details)
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Invalid configuration"
    assert error.details == details


def test_deployment_error():
    """Test deployment error."""
    error = DeploymentError("Deployment failed")
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Deployment failed"
    assert error.message == "Deployment failed"


def test_deployment_error_with_details():
    """Test deployment error with details."""
    details = {"test_id": "123", "status": "failed"}
    error = DeploymentError("Deployment failed", details)
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Deployment failed"
    assert error.details == details


def test_template_error():
    """Test template error."""
    error = TemplateError("Template rendering failed")
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Template rendering failed"
    assert error.message == "Template rendering failed"


def test_template_error_with_details():
    """Test template error with details."""
    details = {"template": "test.yaml", "variable": "missing"}
    error = TemplateError("Template rendering failed", details)
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Template rendering failed"
    assert error.details == details


def test_api_error():
    """Test API error."""
    error = APIError("API request failed")
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "API request failed"
    assert error.message == "API request failed"


def test_api_error_with_details():
    """Test API error with details."""
    details = {"status_code": 500, "response": "server error"}
    error = APIError("API request failed", details)
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "API request failed"
    assert error.details == details


def test_config_error():
    """Test config error."""
    error = ConfigError("Configuration error")
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Configuration error"
    assert error.message == "Configuration error"


def test_config_error_with_details():
    """Test config error with details."""
    details = {"file": "config.yaml", "error": "missing required field"}
    error = ConfigError("Configuration error", details)
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Configuration error"
    assert error.details == details


def test_auth_error():
    """Test authentication error."""
    error = AuthError("Authentication failed")
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Authentication failed"
    assert error.message == "Authentication failed"


def test_auth_error_with_details():
    """Test authentication error with details."""
    details = {"reason": "invalid credentials"}
    error = AuthError("Authentication failed", details)
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Authentication failed"
    assert error.details == details


def test_not_found_error():
    """Test not found error."""
    error = NotFoundError("Resource not found")
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Resource not found"
    assert error.message == "Resource not found"


def test_not_found_error_with_details():
    """Test not found error with details."""
    details = {"resource": "test", "id": "123"}
    error = NotFoundError("Resource not found", details)
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Resource not found"
    assert error.details == details


def test_rate_limit_error():
    """Test rate limit error."""
    error = RateLimitError("Rate limit exceeded")
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Rate limit exceeded"
    assert error.message == "Rate limit exceeded"


def test_rate_limit_error_with_details():
    """Test rate limit error with details."""
    details = {"limit": 100, "remaining": 0, "reset": 3600}
    error = RateLimitError("Rate limit exceeded", details)
    assert isinstance(error, CatchpointConfiguratorError)
    assert str(error) == "Rate limit exceeded"
    assert error.details == details


def test_exception_hierarchy():
    """Test exception hierarchy."""
    assert issubclass(ValidationError, CatchpointConfiguratorError)
    assert issubclass(DeploymentError, CatchpointConfiguratorError)
    assert issubclass(TemplateError, CatchpointConfiguratorError)
    assert issubclass(APIError, CatchpointConfiguratorError)
    assert issubclass(ConfigError, CatchpointConfiguratorError)
    assert issubclass(AuthError, CatchpointConfiguratorError)
    assert issubclass(NotFoundError, CatchpointConfiguratorError)
    assert issubclass(RateLimitError, CatchpointConfiguratorError)
