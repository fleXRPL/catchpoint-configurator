"""
Catchpoint API client for interacting with the Catchpoint API.
"""

import logging
import time
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class CatchpointAPIError(Exception):
    """Base exception for Catchpoint API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        """Initialize the error.

        Args:
            message: Error message
            status_code: Optional HTTP status code
        """
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(CatchpointAPIError):
    """Raised when authentication fails."""

    pass


class RateLimitError(CatchpointAPIError):
    """Raised when rate limit is exceeded."""

    pass


class APIError(CatchpointAPIError):
    """Raised for general API errors."""

    pass


class CatchpointAPI:
    """Client for interacting with the Catchpoint API."""

    BASE_URL = "https://api.catchpoint.com/api/v2"
    TOKEN_URL = "https://api.catchpoint.com/api/v2/token"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        timeout: int = 30,
        debug: bool = False,
    ):
        """Initialize the API client.

        Args:
            client_id: Catchpoint API client ID
            client_secret: Catchpoint API client secret
            timeout: Request timeout in seconds
            debug: Enable debug logging
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.debug = debug
        self._token = None
        self._token_expiry = 0

    def _get_token(self) -> str:
        """Get a valid access token.

        Returns:
            Access token string

        Raises:
            AuthenticationError: If authentication fails
        """
        if self._token and time.time() < self._token_expiry:
            return self._token

        try:
            response = requests.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            self._token = data["access_token"]
            self._token_expiry = time.time() + data["expires_in"] - 60  # Buffer of 60 seconds
            return self._token
        except RequestException as e:
            raise AuthenticationError(f"Failed to get access token: {e}")

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Make an API request.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            timeout: Override default timeout

        Returns:
            Response data

        Raises:
            RateLimitError: If rate limit is exceeded
            APIError: For other API errors
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self._get_token()}"}

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=timeout or self.timeout,
            )

            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid credentials")
            raise APIError(f"API request failed: {e}")

    def create_test(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new test.

        Args:
            test_config: Test configuration

        Returns:
            Created test data
        """
        return self._request("POST", "/tests", data=test_config)

    def update_test(self, test_id: str, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing test.

        Args:
            test_id: Test ID
            test_config: Updated test configuration

        Returns:
            Updated test data
        """
        return self._request("PUT", f"/tests/{test_id}", data=test_config)

    def delete_test(self, test_id: str) -> None:
        """Delete a test.

        Args:
            test_id: Test ID
        """
        self._request("DELETE", f"/tests/{test_id}")

    def get_test(self, test_id: str) -> Dict[str, Any]:
        """Get test details.

        Args:
            test_id: Test ID

        Returns:
            Test data
        """
        return self._request("GET", f"/tests/{test_id}")

    def list_tests(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List all tests.

        Args:
            params: Optional query parameters

        Returns:
            List of test data
        """
        response = self._request("GET", "/tests", params=params)
        return response.get("tests", [])

    def create_dashboard(self, dashboard_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new dashboard.

        Args:
            dashboard_config: Dashboard configuration

        Returns:
            Created dashboard data
        """
        return self._request("POST", "/dashboards", data=dashboard_config)

    def update_dashboard(
        self, dashboard_id: str, dashboard_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing dashboard.

        Args:
            dashboard_id: Dashboard ID
            dashboard_config: Updated dashboard configuration

        Returns:
            Updated dashboard data
        """
        return self._request("PUT", f"/dashboards/{dashboard_id}", data=dashboard_config)

    def delete_dashboard(self, dashboard_id: str) -> None:
        """Delete a dashboard.

        Args:
            dashboard_id: Dashboard ID
        """
        self._request("DELETE", f"/dashboards/{dashboard_id}")

    def get_dashboard(self, dashboard_id: str) -> Dict[str, Any]:
        """Get dashboard details.

        Args:
            dashboard_id: Dashboard ID

        Returns:
            Dashboard data
        """
        return self._request("GET", f"/dashboards/{dashboard_id}")

    def list_dashboards(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List all dashboards.

        Args:
            params: Optional query parameters

        Returns:
            List of dashboard data
        """
        response = self._request("GET", "/dashboards", params=params)
        return response.get("dashboards", [])

    def get_test_results(
        self, test_id: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get test results.

        Args:
            test_id: Test ID
            params: Optional query parameters

        Returns:
            List of test results
        """
        response = self._request("GET", f"/tests/{test_id}/results", params=params)
        return response.get("results", [])

    def get_test_status(self, test_id: str) -> Dict[str, Any]:
        """Get test status.

        Args:
            test_id: Test ID

        Returns:
            Test status data
        """
        return self._request("GET", f"/tests/{test_id}/status")
