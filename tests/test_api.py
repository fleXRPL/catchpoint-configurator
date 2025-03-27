"""Tests for the Catchpoint API client."""

import time
from unittest.mock import patch

import pytest
import requests

from catchpoint_configurator.api import (
    APIError,
    AuthenticationError,
    CatchpointAPI,
    RateLimitError,
)

@pytest.fixture
def api_client():
    """Create a CatchpointAPI instance."""
    return CatchpointAPI(
        client_id="test_client_id",
        client_secret="test_client_secret",
        timeout=30,
    )

def test_get_token(api_client):
    """Test getting an access token."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "access_token": "test_token",
            "expires_in": 3600,
        }
        mock_post.return_value.raise_for_status.return_value = None

        token = api_client._get_token()
        assert token == "test_token"
        assert api_client._token == "test_token"
        assert api_client._token_expiry > time.time()

def test_get_token_expired(api_client):
    """Test getting a new token when the current one is expired."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "access_token": "new_token",
            "expires_in": 3600,
        }
        mock_post.return_value.raise_for_status.return_value = None

        # Set an expired token
        api_client._token = "old_token"
        api_client._token_expiry = time.time() - 1

        token = api_client._get_token()
        assert token == "new_token"
        assert api_client._token == "new_token"
        assert api_client._token_expiry > time.time()

def test_get_token_auth_error(api_client):
    """Test authentication error when getting token."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("Auth failed")
        with pytest.raises(AuthenticationError):
            api_client._get_token()

def test_request_rate_limit(api_client):
    """Test rate limit handling."""
    with patch("requests.request") as mock_request:
        mock_response = requests.Response()
        mock_response.status_code = 429
        mock_request.return_value = mock_response

        with pytest.raises(RateLimitError):
            api_client._request("GET", "/test")

def test_request_auth_error(api_client):
    """Test authentication error in request."""
    with patch("requests.request") as mock_request:
        mock_response = requests.Response()
        mock_response.status_code = 401
        mock_request.return_value = mock_request
        mock_request.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with pytest.raises(AuthenticationError):
            api_client._request("GET", "/test")

def test_request_api_error(api_client):
    """Test general API error handling."""
    with patch("requests.request") as mock_request:
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_request.return_value = mock_request
        mock_request.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with pytest.raises(APIError):
            api_client._request("GET", "/test")

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

def test_list_tests(api_client):
    """Test listing tests."""
    with patch.object(api_client, "_request") as mock_request:
        mock_request.return_value = {
            "tests": [
                {"id": "test1", "name": "test1"},
                {"id": "test2", "name": "test2"},
            ],
        }
        result = api_client.list_tests()
        assert len(result) == 2
        assert result[0]["id"] == "test1"
        assert result[1]["id"] == "test2"
        mock_request.assert_called_once_with(
            "GET",
            "/tests",
        ) 