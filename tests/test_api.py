"""Tests for the Catchpoint API client."""

import time
from unittest.mock import Mock, patch

import pytest
import requests
from requests.exceptions import RequestException

from catchpoint_configurator.api import (
    APIError,
    AuthenticationError,
    CatchpointAPI,
    RateLimitError,
)


@pytest.fixture
def mock_response():
    response = Mock()
    response.json.return_value = {"access_token": "test_token", "expires_in": 3600}
    return response


@pytest.fixture
def api():
    return CatchpointAPI("test_client", "test_secret")


@pytest.fixture
def api_client():
    return CatchpointAPI("test_client", "test_secret")


@patch("catchpoint_configurator.api.requests.post")
def test_get_token_success(mock_post, api, mock_response):
    """Test successful token retrieval."""
    mock_post.return_value = mock_response
    mock_response.raise_for_status.return_value = None

    token = api._get_token()
    assert token == "test_token"
    mock_post.assert_called_once()


@patch("catchpoint_configurator.api.requests.post")
def test_get_token_failure(mock_post, api):
    """Test token retrieval failure."""
    mock_post.side_effect = RequestException("Connection failed")

    with pytest.raises(AuthenticationError):
        api._get_token()


@patch("catchpoint_configurator.api.requests.request")
def test_request_success(mock_request, api):
    """Test successful API request."""
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response

    with patch.object(api, "_get_token", return_value="test_token"):
        result = api._request("GET", "/test")
        assert result == {"data": "test"}


@patch("catchpoint_configurator.api.requests.request")
def test_request_rate_limit(mock_request, api):
    """Test rate limit handling."""
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.raise_for_status.side_effect = RequestException("Rate limit exceeded")
    mock_request.return_value = mock_response

    with patch.object(api, "_get_token", return_value="test_token"):
        with pytest.raises(RateLimitError):
            api._request("GET", "/test")


@patch("catchpoint_configurator.api.requests.request")
def test_request_api_error(mock_request, api):
    """Test API error handling."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = RequestException("API error")
    mock_request.return_value = mock_response

    with patch.object(api, "_get_token", return_value="test_token"):
        with pytest.raises(RequestException):
            api._request("GET", "/test")


@patch("catchpoint_configurator.api.requests.request")
def test_list_tests(mock_request, api):
    """Test listing tests."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "tests": [{"id": "test1", "name": "Test 1"}, {"id": "test2", "name": "Test 2"}]
    }
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response

    with patch.object(api, "_get_token", return_value="test_token"):
        result = api.list_tests()
        assert len(result) == 2
        assert result[0]["name"] == "Test 1"


def test_create_test(api_client):
    """Test creating a test."""
    test_config = {
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
    }

    with patch.object(api_client, "_request") as mock_request:
        mock_request.return_value = {"id": "test123"}
        result = api_client.create_test(test_config)
        assert result["id"] == "test123"
        mock_request.assert_called_once_with(
            "POST",
            "/tests",
            data=test_config,
        )


def test_update_test(api_client):
    """Test updating a test."""
    test_config = {
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
    }

    with patch.object(api_client, "_request") as mock_request:
        mock_request.return_value = {"id": "test123"}
        result = api_client.update_test("test123", test_config)
        assert result["id"] == "test123"
        mock_request.assert_called_once_with(
            "PUT",
            "/tests/test123",
            data=test_config,
        )


def test_delete_test(api_client):
    """Test deleting a test."""
    with patch.object(api_client, "_request") as mock_request:
        api_client.delete_test("test123")
        mock_request.assert_called_once_with(
            "DELETE",
            "/tests/test123",
        )


def test_get_test(api_client):
    """Test getting test details."""
    with patch.object(api_client, "_request") as mock_request:
        mock_request.return_value = {"id": "test123", "name": "test-web"}
        result = api_client.get_test("test123")
        assert result["id"] == "test123"
        assert result["name"] == "test-web"
        mock_request.assert_called_once_with(
            "GET",
            "/tests/test123",
        )
