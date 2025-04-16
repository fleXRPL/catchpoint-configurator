"""Tests for utility functions."""

import logging
import os
import tempfile
from pathlib import Path

import pytest
import yaml

from catchpoint_configurator.exceptions import ValidationError
from catchpoint_configurator.utils import (
    format_duration,
    get_env_var,
    get_logger,
    load_yaml,
    parse_duration,
    save_yaml,
    validate_email,
    validate_slack_channel,
    validate_url,
)


def get_temp_dir():
    """Get appropriate temp directory based on platform."""
    if os.name == "nt" and "GITHUB_WORKSPACE" in os.environ:
        # On Windows in GitHub Actions, use the workspace directory
        temp_dir = os.path.join(os.environ["GITHUB_WORKSPACE"], "tmp")
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir
    return tempfile.gettempdir()


def test_load_yaml():
    """Test loading YAML files."""
    yaml_content = """
    test:
      name: test-web
      url: https://example.com
    """
    temp_dir = get_temp_dir()
    temp_file = os.path.join(temp_dir, f"test_{os.getpid()}.yaml")
    try:
        with open(temp_file, "w") as f:
            f.write(yaml_content)
        data = load_yaml(temp_file)
        assert data["test"]["name"] == "test-web"
        assert data["test"]["url"] == "https://example.com"
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_load_yaml_not_found():
    """Test loading non-existent YAML file."""
    with pytest.raises(FileNotFoundError):
        load_yaml("non-existent.yaml")


def test_load_yaml_invalid():
    """Test loading invalid YAML file."""
    yaml_content = """
    test:
      name: test-web
      url: https://example.com
      invalid: yaml: content
    """
    temp_dir = get_temp_dir()
    temp_file = os.path.join(temp_dir, f"test_invalid_{os.getpid()}.yaml")
    try:
        with open(temp_file, "w") as f:
            f.write(yaml_content)
        with pytest.raises(yaml.YAMLError):
            load_yaml(temp_file)
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_save_yaml():
    """Test saving YAML files."""
    data = {
        "test": {
            "name": "test-web",
            "url": "https://example.com",
        }
    }
    temp_dir = get_temp_dir()
    temp_file = os.path.join(temp_dir, f"test_save_{os.getpid()}.yaml")
    try:
        file_path = save_yaml(data, temp_file)
        loaded_data = load_yaml(file_path)
        assert loaded_data == data
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_get_logger():
    """Test getting a logger instance."""
    logger = get_logger("test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
    assert logger.level == 20  # INFO level


def test_format_duration():
    """Test formatting duration."""
    assert format_duration(60) == "1m"
    assert format_duration(3600) == "1h"
    assert format_duration(86400) == "1d"
    assert format_duration(90000) == "1d 1h"
    assert format_duration(3660) == "1h 1m"
    assert format_duration(65) == "1m 5s"


def test_parse_duration():
    """Test parsing duration strings."""
    assert parse_duration("1m") == 60
    assert parse_duration("1h") == 3600
    assert parse_duration("1d") == 86400
    assert parse_duration("1d 1h") == 90000
    assert parse_duration("1h 1m") == 3660
    assert parse_duration("1m 5s") == 65


def test_parse_duration_invalid():
    """Test parsing invalid duration strings."""
    with pytest.raises(ValueError):
        parse_duration("invalid")


def test_validate_url():
    """Test URL validation."""
    assert validate_url("https://example.com")
    assert validate_url("http://example.com")
    assert validate_url("https://sub.example.com")
    assert validate_url("https://example.com/path")
    assert validate_url("https://example.com:8080")
    assert not validate_url("invalid-url")
    assert not validate_url("ftp://example.com")
    assert not validate_url("http://")


def test_validate_email():
    """Test email validation."""
    assert validate_email("user@example.com")
    assert validate_email("user.name@example.com")
    assert validate_email("user+tag@example.com")
    assert validate_email("user@sub.example.com")
    assert validate_email("user@example.co.uk")
    assert not validate_email("invalid-email")
    assert not validate_email("user@")
    assert not validate_email("@example.com")
    assert not validate_email("user@.com")


def test_validate_slack_channel():
    """Test Slack channel validation."""
    assert validate_slack_channel("#general")
    assert validate_slack_channel("#test-channel")
    assert validate_slack_channel("#test_channel")
    assert validate_slack_channel("#test-channel-123")
    assert not validate_slack_channel("invalid-channel")
    assert not validate_slack_channel("general")
    assert not validate_slack_channel("@user")
    assert not validate_slack_channel("")


def test_path_operations():
    """Test path operations."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_file = Path(temp_dir) / "test.yaml"
        test_file.write_text("test: data")

        # Test path operations
        assert test_file.exists()
        assert test_file.suffix == ".yaml"
        assert test_file.stem == "test"

        # Test directory operations
        test_dir = Path(temp_dir) / "test_dir"
        test_dir.mkdir()
        assert test_dir.is_dir()
        assert test_dir.exists()

        # Test file operations
        new_file = test_dir / "new.yaml"
        new_file.write_text("new: data")
        assert new_file.exists()
        assert new_file.read_text() == "new: data"

        # Test cleanup
        new_file.unlink()
        test_dir.rmdir()
        test_file.unlink()
        assert not test_file.exists()
        assert not test_dir.exists()
        assert not new_file.exists()


def test_get_env_var_required():
    """Test getting a required environment variable that doesn't exist."""
    with pytest.raises(ValidationError, match="Required environment variable TEST_VAR not found"):
        get_env_var("TEST_VAR", required=True)


def test_get_env_var_not_required():
    """Test getting an optional environment variable that doesn't exist."""
    assert get_env_var("TEST_VAR", required=False) is None


def test_save_yaml_serialization_error(monkeypatch):
    """Test saving YAML with non-serializable data."""

    def mock_dump(*args, **kwargs):
        raise yaml.YAMLError("Test serialization error")

    monkeypatch.setattr(yaml, "dump", mock_dump)
    with pytest.raises(yaml.YAMLError, match="Failed to serialize data to YAML"):
        save_yaml({"test": "data"})


def test_save_yaml_write_error(monkeypatch):
    """Test saving YAML with write permission error."""

    def mock_open(*args, **kwargs):
        raise IOError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)
    with pytest.raises(IOError, match="Failed to write YAML file"):
        save_yaml({"test": "data"}, "test.yaml")


def test_save_yaml_temp_write_error(monkeypatch):
    """Test saving YAML to temp file with write error."""

    def mock_open(*args, **kwargs):
        raise IOError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)
    with pytest.raises(IOError, match="Failed to write to temporary file"):
        save_yaml({"test": "data"})


def test_validate_url_invalid_scheme():
    """Test validating URL with invalid scheme."""
    assert not validate_url("ftp://example.com")
    assert not validate_url("invalid://example.com")


def test_validate_url_missing_netloc():
    """Test validating URL with missing network location."""
    assert not validate_url("http://")
    assert not validate_url("https://")
