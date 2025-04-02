"""
Contest management functionality for Catchpoint Configurator.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union

from .api import CatchpointAPI
from .exceptions import ContestError
from .types import ContestConfig, ContestResult
from .utils import get_logger

logger = get_logger(__name__)


class ContestManager:
    """Manages contest functionality for Catchpoint tests."""

    def __init__(self, api: CatchpointAPI):
        """Initialize the contest manager.

        Args:
            api: CatchpointAPI instance for making API calls
        """
        self.api = api
        logger.info("Initialized ContestManager")

    def create_contest(self, config: ContestConfig) -> Dict:
        """Create a new contest.

        Args:
            config: Contest configuration

        Returns:
            Dict containing contest details

        Raises:
            ContestError: If contest creation fails
        """
        try:
            logger.info(f"Creating contest: {config.name}")
            response = self.api.post("/contests", json=config.dict())
            logger.info(f"Created contest: {response['id']}")
            return response
        except Exception as e:
            raise ContestError(f"Failed to create contest: {str(e)}")

    def get_contest(self, contest_id: str) -> Dict:
        """Get contest details.

        Args:
            contest_id: ID of the contest

        Returns:
            Dict containing contest details

        Raises:
            ContestError: If contest retrieval fails
        """
        try:
            logger.info(f"Getting contest: {contest_id}")
            response = self.api.get(f"/contests/{contest_id}")
            return response
        except Exception as e:
            raise ContestError(f"Failed to get contest: {str(e)}")

    def list_contests(
        self,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict]:
        """List contests with optional filtering.

        Args:
            status: Filter by contest status
            start_date: Filter by start date
            end_date: Filter by end date

        Returns:
            List of contest details

        Raises:
            ContestError: If contest listing fails
        """
        try:
            params = {}
            if status:
                params["status"] = status
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()

            logger.info("Listing contests")
            response = self.api.get("/contests", params=params)
            return response
        except Exception as e:
            raise ContestError(f"Failed to list contests: {str(e)}")

    def update_contest(self, contest_id: str, config: ContestConfig) -> Dict:
        """Update an existing contest.

        Args:
            contest_id: ID of the contest to update
            config: Updated contest configuration

        Returns:
            Dict containing updated contest details

        Raises:
            ContestError: If contest update fails
        """
        try:
            logger.info(f"Updating contest: {contest_id}")
            response = self.api.put(f"/contests/{contest_id}", json=config.dict())
            logger.info(f"Updated contest: {contest_id}")
            return response
        except Exception as e:
            raise ContestError(f"Failed to update contest: {str(e)}")

    def delete_contest(self, contest_id: str) -> None:
        """Delete a contest.

        Args:
            contest_id: ID of the contest to delete

        Raises:
            ContestError: If contest deletion fails
        """
        try:
            logger.info(f"Deleting contest: {contest_id}")
            self.api.delete(f"/contests/{contest_id}")
            logger.info(f"Deleted contest: {contest_id}")
        except Exception as e:
            raise ContestError(f"Failed to delete contest: {str(e)}")

    def get_contest_results(
        self,
        contest_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[ContestResult]:
        """Get results for a contest.

        Args:
            contest_id: ID of the contest
            start_date: Optional start date for results
            end_date: Optional end date for results

        Returns:
            List of contest results

        Raises:
            ContestError: If results retrieval fails
        """
        try:
            params = {}
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()

            logger.info(f"Getting results for contest: {contest_id}")
            response = self.api.get(f"/contests/{contest_id}/results", params=params)
            return [ContestResult(**result) for result in response]
        except Exception as e:
            raise ContestError(f"Failed to get contest results: {str(e)}")

    def get_contest_leaderboard(self, contest_id: str, limit: Optional[int] = None) -> List[Dict]:
        """Get the leaderboard for a contest.

        Args:
            contest_id: ID of the contest
            limit: Optional limit on number of entries

        Returns:
            List of leaderboard entries

        Raises:
            ContestError: If leaderboard retrieval fails
        """
        try:
            params = {}
            if limit:
                params["limit"] = limit

            logger.info(f"Getting leaderboard for contest: {contest_id}")
            response = self.api.get(f"/contests/{contest_id}/leaderboard", params=params)
            return response
        except Exception as e:
            raise ContestError(f"Failed to get contest leaderboard: {str(e)}")

    def get_contest_stats(self, contest_id: str) -> Dict:
        """Get statistics for a contest.

        Args:
            contest_id: ID of the contest

        Returns:
            Dict containing contest statistics

        Raises:
            ContestError: If statistics retrieval fails
        """
        try:
            logger.info(f"Getting statistics for contest: {contest_id}")
            response = self.api.get(f"/contests/{contest_id}/stats")
            return response
        except Exception as e:
            raise ContestError(f"Failed to get contest statistics: {str(e)}")

    def export_contest_results(
        self,
        contest_id: str,
        format: str = "csv",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> str:
        """Export contest results in specified format.

        Args:
            contest_id: ID of the contest
            format: Export format (csv, json, etc.)
            start_date: Optional start date for results
            end_date: Optional end date for results

        Returns:
            Exported results as string

        Raises:
            ContestError: If export fails
        """
        try:
            params = {"format": format}
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()

            logger.info(f"Exporting results for contest: {contest_id}")
            response = self.api.get(f"/contests/{contest_id}/export", params=params)
            return response
        except Exception as e:
            raise ContestError(f"Failed to export contest results: {str(e)}")

    def import_contest_results(
        self, contest_id: str, results: Union[str, List[Dict]], format: str = "csv"
    ) -> None:
        """Import results for a contest.

        Args:
            contest_id: ID of the contest
            results: Results to import (string or list of dicts)
            format: Import format (csv, json, etc.)

        Raises:
            ContestError: If import fails
        """
        try:
            data = {"format": format, "results": results}

            logger.info(f"Importing results for contest: {contest_id}")
            self.api.post(f"/contests/{contest_id}/import", json=data)
            logger.info(f"Imported results for contest: {contest_id}")
        except Exception as e:
            raise ContestError(f"Failed to import contest results: {str(e)}")

    def get_contest_analytics(
        self,
        contest_id: str,
        metric: str,
        interval: str = "1h",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict:
        """Get analytics for a contest metric.

        Args:
            contest_id: ID of the contest
            metric: Metric to analyze
            interval: Time interval for analytics
            start_date: Optional start date
            end_date: Optional end date

        Returns:
            Dict containing analytics data

        Raises:
            ContestError: If analytics retrieval fails
        """
        try:
            params = {"metric": metric, "interval": interval}
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()

            logger.info(f"Getting analytics for contest: {contest_id}")
            response = self.api.get(f"/contests/{contest_id}/analytics", params=params)
            return response
        except Exception as e:
            raise ContestError(f"Failed to get contest analytics: {str(e)}")

    def get_contest_reports(
        self,
        contest_id: str,
        report_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict:
        """Get reports for a contest.

        Args:
            contest_id: ID of the contest
            report_type: Type of report to generate
            start_date: Optional start date
            end_date: Optional end date

        Returns:
            Dict containing report data

        Raises:
            ContestError: If report generation fails
        """
        try:
            params = {"type": report_type}
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()

            logger.info(f"Getting reports for contest: {contest_id}")
            response = self.api.get(f"/contests/{contest_id}/reports", params=params)
            return response
        except Exception as e:
            raise ContestError(f"Failed to get contest reports: {str(e)}")
