"""Contest management module for Catchpoint Configurator."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .api import CatchpointAPI
from .config import ConfigValidator
from .exceptions import APIError, ContestError
from .types import TestConfig

logger = logging.getLogger(__name__)


class ContestManager:
    """Manager for Catchpoint test contests."""

    def __init__(self, api: CatchpointAPI):
        """Initialize the contest manager.

        Args:
            api: CatchpointAPI instance
        """
        self.api = api
        self.validator = ConfigValidator()

    def create_contest(self, config: TestConfig) -> Dict[str, Any]:
        """Create a new test contest.

        Args:
            config: Test configuration

        Returns:
            Created contest details

        Raises:
            ContestError: If contest creation fails
            APIError: If the API request fails
        """
        self.validator.validate_test_config(config)

        try:
            return self.api.create_test(config)
        except Exception as e:
            logger.error(f"Failed to create contest: {e}")
            raise ContestError(f"Failed to create contest: {e}")

    def get_contest(self, contest_id: str) -> Dict[str, Any]:
        """Get contest details.

        Args:
            contest_id: Contest ID

        Returns:
            Contest details

        Raises:
            APIError: If the API request fails
        """
        try:
            return self.api.get_test(contest_id)
        except Exception as e:
            logger.error(f"Failed to get contest {contest_id}: {e}")
            raise APIError(f"Failed to get contest {contest_id}: {e}")

    def update_contest(self, contest_id: str, config: TestConfig) -> Dict[str, Any]:
        """Update an existing contest.

        Args:
            contest_id: Contest ID
            config: Updated test configuration

        Returns:
            Updated contest details

        Raises:
            ContestError: If contest update fails
            APIError: If the API request fails
        """
        self.validator.validate_test_config(config)

        try:
            return self.api.update_test(contest_id, config)
        except Exception as e:
            logger.error(f"Failed to update contest {contest_id}: {e}")
            raise ContestError(f"Failed to update contest: {e}")

    def delete_contest(self, contest_id: str) -> None:
        """Delete a contest.

        Args:
            contest_id: Contest ID

        Raises:
            APIError: If the API request fails
        """
        try:
            self.api.delete(f"/contests/{contest_id}")
        except Exception as e:
            logger.error(f"Failed to delete contest {contest_id}: {e}")
            raise APIError(f"Failed to delete contest {contest_id}: {e}")

    def list_contests(
        self,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """List all contests.

        Args:
            status: Filter by status
            start_date: Filter by start date
            end_date: Filter by end date

        Returns:
            List of contest details

        Raises:
            APIError: If the API request fails
        """
        params = {}
        if status:
            params["status"] = status
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        try:
            return self.api.list_tests()
        except Exception as e:
            logger.error(f"Failed to list contests: {e}")
            raise APIError(f"Failed to list contests: {e}")

    def enable_contest(self, contest_id: str) -> None:
        """Enable a contest.

        Args:
            contest_id: Contest ID

        Raises:
            APIError: If the API request fails
        """
        try:
            self.api.enable_test(contest_id)
        except Exception as e:
            raise APIError(f"Failed to enable contest {contest_id}: {e}")

    def disable_contest(self, contest_id: str) -> None:
        """Disable a contest.

        Args:
            contest_id: Contest ID

        Raises:
            APIError: If the API request fails
        """
        try:
            self.api.disable_test(contest_id)
        except Exception as e:
            raise APIError(f"Failed to disable contest {contest_id}: {e}")

    def get_contest_results(self, contest_id: str) -> List[Dict[str, Any]]:
        """Get contest results.

        Args:
            contest_id: Contest ID

        Returns:
            Contest results

        Raises:
            APIError: If API request fails
        """
        try:
            return self.api.get(f"/contests/{contest_id}/results")
        except Exception as e:
            logger.error(f"Failed to get contest results for {contest_id}: {e}")
            raise APIError(f"Failed to get contest results for {contest_id}: {e}")

    def get_contest_leaderboard(self, contest_id: str) -> List[Dict[str, Any]]:
        """Get contest leaderboard.

        Args:
            contest_id: Contest ID

        Returns:
            Contest leaderboard

        Raises:
            APIError: If API request fails
        """
        try:
            return self.api.get(f"/contests/{contest_id}/leaderboard", params={})
        except Exception as e:
            logger.error(f"Failed to get contest leaderboard for {contest_id}: {e}")
            raise APIError(f"Failed to get contest leaderboard for {contest_id}: {e}")

    def get_contest_stats(self, contest_id: str) -> Dict[str, Any]:
        """Get contest statistics.

        Args:
            contest_id: Contest ID

        Returns:
            Contest statistics
        """
        return self.api.get(f"/contests/{contest_id}/stats")

    def export_contest_results(
        self, contest_id: str, format: str = "csv"
    ) -> Union[str, Dict[str, Any]]:
        """Export contest results.

        Args:
            contest_id: Contest ID
            format: Export format (csv or json)

        Returns:
            Exported contest results

        Raises:
            APIError: If API request fails
        """
        try:
            return self.api.get(f"/contests/{contest_id}/export", params={"format": format})
        except Exception as e:
            logger.error(f"Failed to export contest results for {contest_id}: {e}")
            raise APIError(f"Failed to export contest results for {contest_id}: {e}")

    def import_contest_results(
        self, contest_id: str, results: List[Dict[str, Any]], format: str = "json"
    ) -> Dict[str, Any]:
        """Import contest results.

        Args:
            contest_id: Contest ID
            results: Results to import
            format: Import format (json)

        Returns:
            Import status

        Raises:
            APIError: If API request fails
        """
        try:
            return self.api.post(
                f"/contests/{contest_id}/import",
                json={"format": format, "results": results},
            )
        except Exception as e:
            logger.error(f"Failed to import contest results for {contest_id}: {e}")
            raise APIError(f"Failed to import contest results for {contest_id}: {e}")

    def get_contest_analytics(
        self, contest_id: str, metric: str, interval: str = "1h"
    ) -> Dict[str, Any]:
        """Get contest analytics.

        Args:
            contest_id: Contest ID
            metric: Metric to analyze
            interval: Time interval for analysis

        Returns:
            Contest analytics

        Raises:
            APIError: If API request fails
        """
        try:
            return self.api.get(
                f"/contests/{contest_id}/analytics",
                params={"metric": metric, "interval": interval},
            )
        except Exception as e:
            logger.error(f"Failed to get contest analytics for {contest_id}: {e}")
            raise APIError(f"Failed to get contest analytics for {contest_id}: {e}")

    def get_contest_reports(self, contest_id: str, report_type: str) -> Dict[str, Any]:
        """Get contest reports.

        Args:
            contest_id: Contest ID
            report_type: Report type

        Returns:
            Contest reports
        """
        return self.api.get(f"/contests/{contest_id}/reports", params={"type": report_type})
