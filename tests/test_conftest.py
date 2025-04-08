"""
Tests for contest management functionality.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from catchpoint_configurator.contest import ContestManager
from catchpoint_configurator.exceptions import ContestError
from catchpoint_configurator.types import ContestResult


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
    return {
        "type": "test",
        "name": "Test Contest",
        "description": "Test contest description",
        "url": "https://example.com",
        "frequency": 300,
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=7),
        "metrics": ["response_time", "availability"],
        "nodes": ["US-East", "US-West"],
        "rules": {"min_requests": 100, "max_errors": 5},
    }


def test_create_contest(contest_manager, contest_config):
    """Test contest creation."""
    # Setup
    expected_response = {"id": "123", "name": "Test Contest"}
    contest_manager.api.create_test.return_value = expected_response

    # Execute
    result = contest_manager.create_contest(contest_config)

    # Verify
    assert result == expected_response
    contest_manager.api.create_test.assert_called_once_with(contest_config)


def test_create_contest_error(contest_manager, contest_config):
    """Test contest creation error handling."""
    # Setup
    contest_manager.api.create_test.side_effect = Exception("API Error")

    # Execute and verify
    with pytest.raises(ContestError) as exc_info:
        contest_manager.create_contest(contest_config)
    assert "Failed to create contest" in str(exc_info.value)


def test_get_contest(contest_manager):
    """Test getting contest details."""
    # Setup
    contest_id = "123"
    expected_response = {"id": contest_id, "name": "Test Contest"}
    contest_manager.api.get_test.return_value = expected_response

    # Execute
    result = contest_manager.get_contest(contest_id)

    # Verify
    assert result == expected_response
    contest_manager.api.get_test.assert_called_once_with(contest_id)


def test_list_contests(contest_manager):
    """Test listing contests."""
    # Setup
    expected_response = [
        {"id": "123", "name": "Contest 1"},
        {"id": "456", "name": "Contest 2"},
    ]
    contest_manager.api.list_tests.return_value = expected_response

    # Execute
    result = contest_manager.list_contests()

    # Verify
    assert result == expected_response
    contest_manager.api.list_tests.assert_called_once_with({})


def test_list_contests_with_filters(contest_manager):
    """Test listing contests with filters."""
    # Setup
    status = "active"
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=7)
    expected_response = [{"id": "123", "name": "Contest 1"}]
    contest_manager.api.list_tests.return_value = expected_response

    # Execute
    result = contest_manager.list_contests(status=status, start_date=start_date, end_date=end_date)

    # Verify
    assert result == expected_response
    contest_manager.api.list_tests.assert_called_once_with(
        {
            "status": status,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
    )


def test_update_contest(contest_manager, contest_config):
    """Test updating a contest."""
    # Setup
    contest_id = "123"
    expected_response = {"id": contest_id, "name": "Updated Contest"}
    contest_manager.api.update_test.return_value = expected_response

    # Execute
    result = contest_manager.update_contest(contest_id, contest_config)

    # Verify
    assert result == expected_response
    contest_manager.api.update_test.assert_called_once_with(contest_id, contest_config)


def test_delete_contest(contest_manager):
    """Test deleting a contest."""
    # Setup
    contest_id = "123"

    # Execute
    contest_manager.delete_contest(contest_id)

    # Verify
    contest_manager.api.delete_test.assert_called_once_with(contest_id)


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
    contest_manager.api.get_test_results.return_value = expected_response

    # Execute
    result = contest_manager.get_contest_results(contest_id)

    # Verify
    assert len(result) == 1
    assert result[0]["metric"] == "response_time"
    assert result[0]["value"] == 100
    contest_manager.api.get_test_results.assert_called_once_with(contest_id)


def test_get_contest_leaderboard(contest_manager):
    """Test getting contest leaderboard."""
    # Setup
    contest_id = "123"
    expected_response = [
        {"rank": 1, "participant": "Team A", "score": 95},
        {"rank": 2, "participant": "Team B", "score": 90},
    ]
    contest_manager.api.get_test_leaderboard.return_value = expected_response

    # Execute
    result = contest_manager.get_contest_leaderboard(contest_id)

    # Verify
    assert result == expected_response
    contest_manager.api.get_test_leaderboard.assert_called_once_with(contest_id)


def test_get_contest_analytics(contest_manager):
    """Test getting contest analytics."""
    # Setup
    contest_id = "123"
    expected_response = {
        "intervals": [
            {"timestamp": "2024-01-01T00:00:00", "value": 100},
            {"timestamp": "2024-01-01T01:00:00", "value": 95},
        ],
    }
    contest_manager.api.get_test_analytics.return_value = expected_response

    # Execute
    result = contest_manager.get_contest_analytics(contest_id)

    # Verify
    assert result == expected_response
    contest_manager.api.get_test_analytics.assert_called_once_with(contest_id)


def test_export_contest_results(contest_manager):
    """Test exporting contest results."""
    # Setup
    contest_id = "123"
    expected_response = b"timestamp,metric,value\n2024-01-01T00:00:00,response_time,100"
    contest_manager.api.export_test_results.return_value = expected_response

    # Execute
    result = contest_manager.export_contest_results(contest_id)

    # Verify
    assert result == expected_response
    contest_manager.api.export_test_results.assert_called_once_with(contest_id, "csv")


def test_import_contest_results(contest_manager):
    """Test importing contest results."""
    # Setup
    contest_id = "123"
    data = b"timestamp,metric,value\n2024-01-01T00:00:00,response_time,100"

    # Execute
    contest_manager.import_contest_results(contest_id, data)

    # Verify
    contest_manager.api.import_test_results.assert_called_once_with(contest_id, data)
