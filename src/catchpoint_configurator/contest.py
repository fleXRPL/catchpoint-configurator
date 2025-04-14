"""Contest management functionality."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .api import CatchpointAPI
from .config import ConfigValidator
from .exceptions import ContestError
from .types import ContestResult

logger = logging.getLogger(__name__)


class ContestManager:
    """Contest manager class."""

    def __init__(
        self,
        api: CatchpointAPI,
        validator: Optional[ConfigValidator] = None,
    ) -> None:
        """Initialize the contest manager.

        Args:
            api: CatchpointAPI instance
            validator: Optional ConfigValidator instance
        """
        self.api = api
        self.validator = validator or ConfigValidator()

    def create_contest(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new test contest.

        Args:
            config: Test configuration

        Returns:
            Created contest details

        Raises:
            ContestError: If contest creation fails
            APIError: If the API request fails
        """
        try:
            # Add contest type if not present
            if "type" not in config:
                config["type"] = "contest"
            self.validator.validate(config)
            return self.api.create_test(config)
        except Exception as e:
            logger.error(f"Failed to create contest: {e}")
            raise ContestError(f"Failed to create contest: {str(e)}")

    def get_contest(self, contest_id: str) -> Dict[str, Any]:
        """Get contest details.

        Args:
            contest_id: Contest ID

        Returns:
            Contest details

        Raises:
            ContestError: If contest retrieval fails
            APIError: If the API request fails
        """
        try:
            return self.api.get_test(contest_id)
        except Exception as e:
            logger.error(f"Failed to get contest {contest_id}: {e}")
            raise ContestError(f"Failed to get contest: {str(e)}")

    def update_contest(self, contest_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
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
        try:
            # Add contest type if not present
            if "type" not in config:
                config["type"] = "contest"
            self.validator.validate(config)
            return self.api.update_test(contest_id, config)
        except Exception as e:
            logger.error(f"Failed to update contest {contest_id}: {e}")
            raise ContestError(f"Failed to update contest: {str(e)}")

    def delete_contest(self, contest_id: str) -> None:
        """Delete a contest.

        Args:
            contest_id: Contest ID

        Raises:
            ContestError: If contest deletion fails
            APIError: If the API request fails
        """
        try:
            self.api.delete_test(contest_id)
        except Exception as e:
            logger.error(f"Failed to delete contest {contest_id}: {e}")
            raise ContestError(f"Failed to delete contest: {str(e)}")

    def list_contests(
        self,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """List contests.

        Args:
            status: Optional status filter
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of contests

        Raises:
            ContestError: If contest listing fails
            APIError: If the API request fails
        """
        try:
            filters = {}
            if status:
                filters["status"] = status
            if start_date:
                filters["start_date"] = start_date.isoformat()
            if end_date:
                filters["end_date"] = end_date.isoformat()

            return self.api.list_tests(filters)
        except Exception as e:
            logger.error(f"Failed to list contests: {e}")
            raise ContestError(f"Failed to list contests: {str(e)}")

    def get_contest_results(self, contest_id: str) -> List[ContestResult]:
        """Get contest results.

        Args:
            contest_id: Contest ID

        Returns:
            List of contest results

        Raises:
            ContestError: If contest results retrieval fails
            APIError: If the API request fails
        """
        try:
            results = self.api.get_test_results(contest_id)
            return [ContestResult(**result) for result in results]
        except Exception as e:
            logger.error(f"Failed to get contest results for {contest_id}: {e}")
            raise ContestError(f"Failed to get contest results: {str(e)}")

    def get_contest_leaderboard(self, contest_id: str) -> List[Dict[str, Any]]:
        """Get contest leaderboard.

        Args:
            contest_id: Contest ID

        Returns:
            Contest leaderboard

        Raises:
            ContestError: If contest leaderboard retrieval fails
            APIError: If the API request fails
        """
        try:
            return self.api.get_test_leaderboard(contest_id)
        except Exception as e:
            logger.error(f"Failed to get contest leaderboard for {contest_id}: {e}")
            raise ContestError(f"Failed to get contest leaderboard: {str(e)}")

    def get_contest_analytics(self, contest_id: str) -> Dict[str, Any]:
        """Get contest analytics.

        Args:
            contest_id: Contest ID

        Returns:
            Contest analytics

        Raises:
            ContestError: If contest analytics retrieval fails
            APIError: If the API request fails
        """
        try:
            return self.api.get_test_analytics(contest_id)
        except Exception as e:
            logger.error(f"Failed to get contest analytics for {contest_id}: {e}")
            raise ContestError(f"Failed to get contest analytics: {str(e)}")

    def export_contest_results(self, contest_id: str, format: str = "csv") -> bytes:
        """Export contest results.

        Args:
            contest_id: Contest ID
            format: Export format (csv or json)

        Returns:
            Exported contest results

        Raises:
            ContestError: If contest results export fails
            APIError: If the API request fails
        """
        try:
            return self.api.export_test_results(contest_id, format)
        except Exception as e:
            logger.error(f"Failed to export contest results for {contest_id}: {e}")
            raise ContestError(f"Failed to export contest results: {str(e)}")

    def import_contest_results(self, contest_id: str, data: bytes) -> None:
        """Import contest results.

        Args:
            contest_id: Contest ID
            data: Contest results data

        Raises:
            ContestError: If contest results import fails
            APIError: If the API request fails
        """
        try:
            self.api.import_test_results(contest_id, data)
        except Exception as e:
            logger.error(f"Failed to import contest results for {contest_id}: {e}")
            raise ContestError(f"Failed to import contest results: {str(e)}")
