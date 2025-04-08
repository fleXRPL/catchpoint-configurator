"""Tests for the CLI interface."""

from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from catchpoint_configurator.cli import cli


@pytest.fixture
def mock_configurator():
    """Mock CatchpointConfigurator instance."""
    mock = Mock()
    # Set up methods to return success without raising exceptions
    mock.validate.return_value = True
    mock.deploy.return_value = {"status": "success"}
    mock.list.return_value = [{"name": "Test 1", "type": "test"}]
    return mock


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


def test_validate_command(runner, mock_configurator):
    """Test the validate command."""
    with runner.isolated_filesystem():
        with open("test.yaml", "w") as f:
            f.write("test: data")

        with patch("catchpoint_configurator.cli.get_client", return_value=mock_configurator):
            result = runner.invoke(
                cli, ["--client-id", "test", "--client-secret", "test", "validate", "test.yaml"]
            )
            assert result.exit_code == 0
            assert "Configuration is valid" in result.output


def test_deploy_command(runner, mock_configurator):
    """Test the deploy command."""
    with runner.isolated_filesystem():
        with open("test.yaml", "w") as f:
            f.write("test: data")

        with patch("catchpoint_configurator.cli.get_client", return_value=mock_configurator):
            result = runner.invoke(
                cli, ["--client-id", "test", "--client-secret", "test", "deploy", "test.yaml"]
            )
            assert result.exit_code == 0
            assert "Deployment result: {'status': 'success'}" in result.output


def test_list_command(runner, mock_configurator):
    """Test the list command."""
    with patch("catchpoint_configurator.cli.get_client", return_value=mock_configurator):
        result = runner.invoke(cli, ["--client-id", "test", "--client-secret", "test", "list"])
        assert result.exit_code == 0
        assert "Test 1 (test)" in result.output


def test_missing_credentials(runner):
    """Test command without credentials."""
    result = runner.invoke(cli, ["list"], catch_exceptions=False)
    assert result.exit_code == 2
    assert "Error: Missing option '--client-id'" in result.output


def test_help(runner):
    """Test help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output
