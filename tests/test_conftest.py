"""
Tests for contest management functionality.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from catchpoint_configurator.contest import ContestManager
from catchpoint_configurator.exceptions import ContestError
from catchpoint_configurator.types import ContestConfig, ContestResult


@pytest.fixture
def api_mock():
    """Create a mock API instance."""
    return Mock()


@pytest.fixture
def contest_manager(api_mock):
    """Create a ContestManager instance with mocked API."""
    return ContestManager(api_mock)


@pytest.fixture
def contest_config():
    """Create a sample contest configuration."""
    return ContestConfig(
        name="Test Contest",
        description="Test contest description",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7),
        metrics=["response_time", "availability"],
        nodes=["US-East", "US-West"],
        rules={"min_requests": 100, "max_errors": 5},
    )


def test_create_contest(contest_manager, contest_config):
    """Test contest creation."""
    # Setup
    expected_response = {"id": "123", "name": "Test Contest"}
    contest_manager.api.post.return_value = expected_response

    # Execute
    result = contest_manager.create_contest(contest_config)

    # Verify
    assert result == expected_response
    contest_manager.api.post.assert_called_once_with(
        "/contests", json=contest_config.dict()
    )


def test_create_contest_error(contest_manager, contest_config):
    """Test contest creation error handling."""
    # Setup
    contest_manager.api.post.side_effect = Exception("API Error")

    # Execute and verify
    with pytest.raises(ContestError) as exc_info:
        contest_manager.create_contest(contest_config)
    assert "Failed to create contest" in str(exc_info.value)


def test_get_contest(contest_manager):
    """Test getting contest details."""
    # Setup
    contest_id = "123"
    expected_response = {"id": contest_id, "name": "Test Contest"}
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.get_contest(contest_id)

    # Verify
    assert result == expected_response
    contest_manager.api.get.assert_called_once_with(f"/contests/{contest_id}")


def test_list_contests(contest_manager):
    """Test listing contests."""
    # Setup
    expected_response = [
        {"id": "123", "name": "Contest 1"},
        {"id": "456", "name": "Contest 2"},
    ]
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.list_contests()

    # Verify
    assert result == expected_response
    contest_manager.api.get.assert_called_once_with("/contests", params={})


def test_list_contests_with_filters(contest_manager):
    """Test listing contests with filters."""
    # Setup
    status = "active"
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=7)
    expected_response = [{"id": "123", "name": "Contest 1"}]
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.list_contests(
        status=status, start_date=start_date, end_date=end_date
    )

    # Verify
    assert result == expected_response
    contest_manager.api.get.assert_called_once_with(
        "/contests",
        params={
            "status": status,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )


def test_update_contest(contest_manager, contest_config):
    """Test updating a contest."""
    # Setup
    contest_id = "123"
    expected_response = {"id": contest_id, "name": "Updated Contest"}
    contest_manager.api.put.return_value = expected_response

    # Execute
    result = contest_manager.update_contest(contest_id, contest_config)

    # Verify
    assert result == expected_response
    contest_manager.api.put.assert_called_once_with(
        f"/contests/{contest_id}", json=contest_config.dict()
    )


def test_delete_contest(contest_manager):
    """Test deleting a contest."""
    # Setup
    contest_id = "123"

    # Execute
    contest_manager.delete_contest(contest_id)

    # Verify
    contest_manager.api.delete.assert_called_once_with(f"/contests/{contest_id}")


def test_get_contest_results(contest_manager):
    """Test getting contest results."""
    # Setup
    contest_id = "123"
    expected_response = [
        {
            "timestamp": datetime.now().isoformat(),
            "metric": "response_time",
            "value": 100,
        }
    ]
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.get_contest_results(contest_id)

    # Verify
    assert len(result) == 1
    assert isinstance(result[0], ContestResult)
    contest_manager.api.get.assert_called_once_with(
        f"/contests/{contest_id}/results", params={}
    )


def test_get_contest_leaderboard(contest_manager):
    """Test getting contest leaderboard."""
    # Setup
    contest_id = "123"
    expected_response = [
        {"rank": 1, "participant": "Team A", "score": 95},
        {"rank": 2, "participant": "Team B", "score": 90},
    ]
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.get_contest_leaderboard(contest_id)

    # Verify
    assert result == expected_response
    contest_manager.api.get.assert_called_once_with(
        f"/contests/{contest_id}/leaderboard", params={}
    )


def test_get_contest_stats(contest_manager):
    """Test getting contest statistics."""
    # Setup
    contest_id = "123"
    expected_response = {
        "total_participants": 10,
        "total_requests": 1000,
        "average_score": 85.5,
    }
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.get_contest_stats(contest_id)

    # Verify
    assert result == expected_response
    contest_manager.api.get.assert_called_once_with(f"/contests/{contest_id}/stats")


def test_export_contest_results(contest_manager):
    """Test exporting contest results."""
    # Setup
    contest_id = "123"
    expected_response = "timestamp,metric,value\n2024-01-01T00:00:00,response_time,100"
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.export_contest_results(contest_id, format="csv")

    # Verify
    assert result == expected_response
    contest_manager.api.get.assert_called_once_with(
        f"/contests/{contest_id}/export", params={"format": "csv"}
    )


def test_import_contest_results(contest_manager):
    """Test importing contest results."""
    # Setup
    contest_id = "123"
    results = [
        {"timestamp": "2024-01-01T00:00:00", "metric": "response_time", "value": 100}
    ]

    # Execute
    contest_manager.import_contest_results(contest_id, results, format="json")

    # Verify
    contest_manager.api.post.assert_called_once_with(
        f"/contests/{contest_id}/import", json={"format": "json", "results": results}
    )


def test_get_contest_analytics(contest_manager):
    """Test getting contest analytics."""
    # Setup
    contest_id = "123"
    metric = "response_time"
    expected_response = {
        "metric": metric,
        "intervals": [
            {"timestamp": "2024-01-01T00:00:00", "value": 100},
            {"timestamp": "2024-01-01T01:00:00", "value": 95},
        ],
    }
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.get_contest_analytics(contest_id, metric)

    # Verify
    assert result == expected_response
    contest_manager.api.get.assert_called_once_with(
        f"/contests/{contest_id}/analytics", params={"metric": metric, "interval": "1h"}
    )


def test_get_contest_reports(contest_manager):
    """Test getting contest reports."""
    # Setup
    contest_id = "123"
    report_type = "summary"
    expected_response = {
        "type": report_type,
        "data": {
            "total_participants": 10,
            "total_requests": 1000,
            "average_score": 85.5,
        },
    }
    contest_manager.api.get.return_value = expected_response

    # Execute
    result = contest_manager.get_contest_reports(contest_id, report_type)

    # Verify
    assert result == expected_response
    contest_manager.api.get.assert_called_once_with(
        f"/contests/{contest_id}/reports", params={"type": report_type}
    )
