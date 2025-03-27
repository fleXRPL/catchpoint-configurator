"""Tests for utility functions."""

import os
import tempfile
from pathlib import Path

import pytest
import yaml
import logging

from catchpoint_configurator.utils import (
    load_yaml,
    save_yaml,
    get_logger,
    format_duration,
    parse_duration,
    validate_url,
    validate_email,
    validate_slack_channel,
)

def test_load_yaml():
    """Test loading YAML files."""
    yaml_content = """
    test:
      name: test-web
      url: https://example.com
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml") as f:
        f.write(yaml_content)
        f.flush()
        data = load_yaml(f.name)
        assert data["test"]["name"] == "test-web"
        assert data["test"]["url"] == "https://example.com"

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
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml") as f:
        f.write(yaml_content)
        f.flush()
        with pytest.raises(yaml.YAMLError):
            load_yaml(f.name)

def test_save_yaml():
    """Test saving YAML files."""
    data = {
        "test": {
            "name": "test-web",
            "url": "https://example.com",
        }
    }
    with tempfile.NamedTemporaryFile(suffix=".yaml") as f:
        save_yaml(data, f.name)
        loaded_data = load_yaml(f.name)
        assert loaded_data == data

def test_save_yaml_invalid_data():
    """Test saving invalid data to YAML."""
    class InvalidData:
        pass

    with tempfile.NamedTemporaryFile(suffix=".yaml") as f:
        with pytest.raises(yaml.YAMLError):
            save_yaml(InvalidData(), f.name)

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
    with pytest.raises(ValueError):
        parse_duration("1x")
    with pytest.raises(ValueError):
        parse_duration("1m 1x")

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
