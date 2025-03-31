"""Tests for the CLI interface."""

import os
import sys
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from catchpoint_configurator.cli import (
    cli,
    delete,
    deploy,
    export,
    import_config,
    list,
    validate,
)


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def mock_api():
    """Mock the CatchpointAPI."""
    with patch("catchpoint_configurator.cli.CatchpointAPI") as mock:
        yield mock


def test_deploy_command(runner, mock_api):
    """Test the deploy command."""
    mock_instance = mock_api.return_value
    mock_instance.deploy.return_value = {"id": "test123"}

    result = runner.invoke(
        deploy,
        ["--config", "examples/web-test.yaml", "--dry-run"],
    )
    assert result.exit_code == 0
    assert "Successfully deployed configuration" in result.output
    mock_instance.deploy.assert_called_once_with(
        "examples/web-test.yaml",
        dry_run=True,
        force=False,
        timeout=30,
    )


def test_deploy_command_error(runner, mock_api):
    """Test the deploy command with an error."""
    mock_instance = mock_api.return_value
    mock_instance.deploy.side_effect = Exception("Deployment failed")

    result = runner.invoke(
        deploy,
        ["--config", "examples/web-test.yaml"],
    )
    assert result.exit_code == 1
    assert "Error deploying configuration" in result.output


def test_validate_command(runner, mock_api):
    """Test the validate command."""
    mock_instance = mock_api.return_value
    mock_instance.validate.return_value = True

    result = runner.invoke(
        validate,
        ["--config", "examples/web-test.yaml"],
    )
    assert result.exit_code == 0
    assert "Configuration is valid" in result.output
    mock_instance.validate.assert_called_once_with("examples/web-test.yaml")


def test_validate_command_error(runner, mock_api):
    """Test the validate command with an error."""
    mock_instance = mock_api.return_value
    mock_instance.validate.side_effect = Exception("Validation failed")

    result = runner.invoke(
        validate,
        ["--config", "examples/web-test.yaml"],
    )
    assert result.exit_code == 1
    assert "Error validating configuration" in result.output


def test_list_command(runner, mock_api):
    """Test the list command."""
    mock_instance = mock_api.return_value
    mock_instance.list_tests.return_value = [
        {"id": "test1", "name": "test1"},
        {"id": "test2", "name": "test2"},
    ]

    result = runner.invoke(list)
    assert result.exit_code == 0
    assert "test1" in result.output
    assert "test2" in result.output
    mock_instance.list_tests.assert_called_once()


def test_list_command_error(runner, mock_api):
    """Test the list command with an error."""
    mock_instance = mock_api.return_value
    mock_instance.list_tests.side_effect = Exception("List failed")

    result = runner.invoke(list)
    assert result.exit_code == 1
    assert "Error listing tests" in result.output


def test_delete_command(runner, mock_api):
    """Test the delete command."""
    mock_instance = mock_api.return_value
    mock_instance.delete.return_value = True

    result = runner.invoke(
        delete,
        ["--test-id", "test123"],
    )
    assert result.exit_code == 0
    assert "Successfully deleted test" in result.output
    mock_instance.delete.assert_called_once_with("test123")


def test_delete_command_error(runner, mock_api):
    """Test the delete command with an error."""
    mock_instance = mock_api.return_value
    mock_instance.delete.side_effect = Exception("Delete failed")

    result = runner.invoke(
        delete,
        ["--test-id", "test123"],
    )
    assert result.exit_code == 1
    assert "Error deleting test" in result.output


def test_export_command(runner, mock_api):
    """Test the export command."""
    mock_instance = mock_api.return_value
    mock_instance.export.return_value = {"test": "config"}

    with runner.isolated_filesystem():
        result = runner.invoke(
            export,
            ["--output", "config.yaml"],
        )
        assert result.exit_code == 0
        assert "Successfully exported configuration" in result.output
        assert os.path.exists("config.yaml")
        mock_instance.export.assert_called_once()


def test_export_command_error(runner, mock_api):
    """Test the export command with an error."""
    mock_instance = mock_api.return_value
    mock_instance.export.side_effect = Exception("Export failed")

    result = runner.invoke(
        export,
        ["--output", "config.yaml"],
    )
    assert result.exit_code == 1
    assert "Error exporting configuration" in result.output


def test_import_command(runner, mock_api):
    """Test the import command."""
    mock_instance = mock_api.return_value
    mock_instance.import_config.return_value = {"id": "test123"}

    with runner.isolated_filesystem():
        with open("config.yaml", "w") as f:
            f.write("test: config")
        result = runner.invoke(
            import_config,
            ["--config", "config.yaml"],
        )
        assert result.exit_code == 0
        assert "Successfully imported configuration" in result.output
        mock_instance.import_config.assert_called_once_with("config.yaml")


def test_import_command_error(runner, mock_api):
    """Test the import command with an error."""
    mock_instance = mock_api.return_value
    mock_instance.import_config.side_effect = Exception("Import failed")

    result = runner.invoke(
        import_config,
        ["--config", "config.yaml"],
    )
    assert result.exit_code == 1
    assert "Error importing configuration" in result.output


def test_cli_with_invalid_credentials(runner):
    """Test CLI with invalid credentials."""
    with patch.dict(
        os.environ,
        {"CATCHPOINT_CLIENT_ID": "", "CATCHPOINT_CLIENT_SECRET": ""},
    ):
        result = runner.invoke(cli)
        assert result.exit_code == 1
        assert "Missing required credentials" in result.output


def test_cli_with_valid_credentials(runner, mock_api):
    """Test CLI with valid credentials."""
    with patch.dict(
        os.environ,
        {
            "CATCHPOINT_CLIENT_ID": "test_id",
            "CATCHPOINT_CLIENT_SECRET": "test_secret",
        },
    ):
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert "Catchpoint Configurator CLI" in result.output


def test_cli_help(runner):
    """Test CLI help output."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Catchpoint Configurator CLI" in result.output
    assert "Commands:" in result.output
    assert "deploy" in result.output
    assert "validate" in result.output
    assert "list" in result.output
    assert "delete" in result.output
    assert "export" in result.output
    assert "import" in result.output


def test_command_help(runner):
    """Test command help output."""
    commands = [deploy, validate, list, delete, export, import_config]
    for command in commands:
        result = runner.invoke(command, ["--help"])
        assert result.exit_code == 0
        assert "Options:" in result.output
        assert "--help" in result.output


def test_invalid_command(runner):
    """Test invalid command."""
    result = runner.invoke(cli, ["invalid"])
    assert result.exit_code == 2
    assert "No such command" in result.output


def test_command_with_invalid_options(runner):
    """Test command with invalid options."""
    result = runner.invoke(deploy, ["--invalid"])
    assert result.exit_code == 2
    assert "No such option" in result.output
