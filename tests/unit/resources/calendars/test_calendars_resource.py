"""
Unit tests for the synchronous CalendarsResource class.
"""
import json
import datetime
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.calendars import CalendarsResource
from naxai.models.calendars.calendar import Calendar, ScheduleObject
from naxai.models.calendars.requests.create_calendars_request import CreateCalendarRequest
from naxai.models.calendars.responses.create_calendar_response import CreateCalendarResponse
from naxai.models.calendars.responses.check_calendar_response import CheckCalendarResponse
from naxai.models.calendars.responses.exclusion_response import ExclusionResponse
from naxai.base.exceptions import NaxaiValueError


class TestCalendarsResource:
    """Test suite for the synchronous CalendarsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def calendars_resource(self, mock_client):
        """Create a CalendarsResource instance with a mock client."""
        return CalendarsResource(mock_client)

    @pytest.fixture
    def sample_schedule(self):
        """Create a sample schedule for testing."""
        return [
            {"day": 1, "open": True, "start": "09:00", "stop": "17:00"},
            {"day": 2, "open": True, "start": "09:00", "stop": "17:00"},
            {"day": 3, "open": True, "start": "09:00", "stop": "17:00"},
            {"day": 4, "open": True, "start": "09:00", "stop": "17:00"},
            {"day": 5, "open": True, "start": "09:00", "stop": "17:00"},
            {"day": 6, "open": False},
            {"day": 7, "open": False}
        ]

    def test_initialization(self, calendars_resource):
        """Test that the CalendarsResource initializes correctly."""
        assert calendars_resource.root_path == "/calendars"
        assert calendars_resource.headers == {"Content-Type": "application/json"}
        assert calendars_resource.holidays_templates is not None

    def test_list_calendars(self, calendars_resource, mock_client, sample_schedule):
        """Test listing calendars."""
        # Setup mock response
        mock_response = [
            {
                "id": "cal_123",
                "name": "Business Hours",
                "timezone": "Europe/Brussels",
                "schedule": [
                    {"day": 1, "open": True, "start": "09:00", "stop": "17:00"},
                    {"day": 2, "open": True, "start": "09:00", "stop": "17:00"},
                    {"day": 3, "open": True, "start": "09:00", "stop": "17:00"},
                    {"day": 4, "open": True, "start": "09:00", "stop": "17:00"},
                    {"day": 5, "open": True, "start": "09:00", "stop": "17:00"},
                    {"day": 6, "open": False},
                    {"day": 7, "open": False}
                ],
                "exclusions": ["2023-12-25", "2024-01-01"]
            },
            {
                "id": "cal_456",
                "name": "Support Hours",
                "timezone": "America/New_York",
                "schedule": [
                    {"day": 1, "open": True, "start": "08:00", "stop": "20:00"},
                    {"day": 2, "open": True, "start": "08:00", "stop": "20:00"},
                    {"day": 3, "open": True, "start": "08:00", "stop": "20:00"},
                    {"day": 4, "open": True, "start": "08:00", "stop": "20:00"},
                    {"day": 5, "open": True, "start": "08:00", "stop": "20:00"},
                    {"day": 6, "open": True, "start": "10:00", "stop": "16:00"},
                    {"day": 7, "open": False}
                ],
                "exclusions": []
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = calendars_resource.list()

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(calendar, Calendar) for calendar in result)
        assert result[0].id == "cal_123"
        assert result[0].name == "Business Hours"
        assert result[1].id == "cal_456"
        assert result[1].name == "Support Hours"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/calendars",
            headers={"Content-Type": "application/json"}
        )

    def test_get_calendar(self, calendars_resource, mock_client, sample_schedule):
        """Test getting a specific calendar."""
        # Setup mock response
        mock_response = {
            "id": "cal_123",
            "name": "Business Hours",
            "timezone": "Europe/Brussels",
            "schedule": [
                {"day": 1, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 2, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 3, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 4, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 5, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 6, "open": False},
                {"day": 7, "open": False}
            ],
            "exclusions": ["2023-12-25", "2024-01-01"]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        calendar_id = "cal_123"
        result = calendars_resource.get(calendar_id)

        # Verify the result
        assert isinstance(result, Calendar)
        assert result.id == "cal_123"
        assert result.name == "Business Hours"
        assert result.timezone == "Europe/Brussels"
        assert len(result.schedule) == 7
        assert result.schedule[0].day == 1
        assert result.schedule[0].open is True
        assert result.schedule[0].start == "09:00"
        assert result.schedule[0].stop == "17:00"
        assert result.exclusions == ["2023-12-25", "2024-01-01"]

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/calendars/cal_123",
            headers={"Content-Type": "application/json"}
        )

    def test_create_calendar(self, calendars_resource, mock_client, sample_schedule):
        """Test creating a calendar."""
        # Setup mock response
        mock_response = {
            "id": "cal_789",
            "name": "New Calendar",
            "timezone": "Europe/Brussels",
            "schedule": [
                {"day": 1, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 2, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 3, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 4, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 5, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 6, "open": False},
                {"day": 7, "open": False}
            ],
            "exclusions": []
        }
        mock_client._request.return_value = mock_response

        # Create request data
        request_data = CreateCalendarRequest(
            name="New Calendar",
            timezone="Europe/Brussels",
            schedule=sample_schedule
        )

        # Call the method
        result = calendars_resource.create(request_data)

        # Verify the result
        assert isinstance(result, CreateCalendarResponse)
        assert result.id == "cal_789"
        assert result.name == "New Calendar"
        assert result.timezone == "Europe/Brussels"
        assert len(result.schedule) == 7

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/calendars"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_update_calendar(self, calendars_resource, mock_client, sample_schedule):
        """Test updating a calendar."""
        # Setup mock response
        mock_response = {
            "id": "cal_123",
            "name": "Updated Calendar",
            "timezone": "Europe/London",
            "schedule": [
                {"day": 1, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 2, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 3, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 4, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 5, "open": True, "start": "09:00", "stop": "17:00"},
                {"day": 6, "open": False},
                {"day": 7, "open": False}
            ],
            "exclusions": []
        }
        mock_client._request.return_value = mock_response

        # Create request data
        request_data = CreateCalendarRequest(
            name="Updated Calendar",
            timezone="Europe/London",
            schedule=sample_schedule
        )

        # Call the method
        calendar_id = "cal_123"
        result = calendars_resource.update(calendar_id, request_data)

        # Verify the result
        assert isinstance(result, Calendar)
        assert result.id == "cal_123"
        assert result.name == "Updated Calendar"
        assert result.timezone == "Europe/London"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "PUT"
        assert args[1] == "/calendars/cal_123"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_delete_calendar(self, calendars_resource, mock_client):
        """Test deleting a calendar."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        calendar_id = "cal_123"
        result = calendars_resource.delete(calendar_id)

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/calendars/cal_123",
            headers={"Content-Type": "application/json"}
        )

    def test_check_calendar(self, calendars_resource, mock_client):
        """Test checking a calendar's availability."""
        # Setup mock response
        mock_response = {
            "match": True,
            "next": None
        }
        mock_client._request.return_value = mock_response

        # Call the method
        calendar_id = "cal_123"
        timestamp = 1672531200000  # 2023-01-01T00:00:00Z
        result = calendars_resource.check(calendar_id, timestamp)

        # Verify the result
        assert isinstance(result, CheckCalendarResponse)
        assert result.match_ is True
        assert result.next_ is None

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/calendars/cal_123/check"
        assert kwargs["params"] == {"timestamp": timestamp}
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_check_calendar_not_available(self, calendars_resource, mock_client):
        """Test checking a calendar when time is not available."""
        # Setup mock response
        next_available = 1672574400000  # 2023-01-01T12:00:00Z
        mock_response = {
            "match": False,
            "next": next_available
        }
        mock_client._request.return_value = mock_response

        # Call the method
        calendar_id = "cal_123"
        timestamp = 1672531200000  # 2023-01-01T00:00:00Z
        result = calendars_resource.check(calendar_id, timestamp)

        # Verify the result
        assert isinstance(result, CheckCalendarResponse)
        assert result.match_ is False
        assert result.next_ == next_available

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/calendars/cal_123/check"
        assert kwargs["params"] == {"timestamp": timestamp}

    def test_add_exclusions(self, calendars_resource, mock_client):
        """Test adding exclusions to a calendar."""
        # Setup mock response
        mock_response = {
            "exclusions": ["2023-12-25", "2024-01-01", "2024-12-25"]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        calendar_id = "cal_123"
        exclusions = ["2024-12-25"]
        result = calendars_resource.add_exclusions(calendar_id, exclusions)

        # Verify the result
        assert isinstance(result, ExclusionResponse)
        assert result.exclusions == ["2023-12-25", "2024-01-01", "2024-12-25"]

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/calendars/cal_123/exclusions/add"
        assert kwargs["json"] == {"exclusions": exclusions}
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_add_exclusions_too_many(self, calendars_resource):
        """Test adding too many exclusions to a calendar."""
        # Create a list with more than 1000 exclusions
        exclusions = [f"2024-01-{i:02d}" for i in range(1, 1002)]
        
        # Call the method and expect an exception
        with pytest.raises(NaxaiValueError) as excinfo:
            calendars_resource.add_exclusions("cal_123", exclusions)
        
        assert "You can only add up to 1000 exclusions at a time" in str(excinfo.value)

    def test_delete_exclusions(self, calendars_resource, mock_client):
        """Test deleting exclusions from a calendar."""
        # Setup mock response
        mock_response = {
            "exclusions": ["2024-01-01"]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        calendar_id = "cal_123"
        exclusions = ["2023-12-25"]
        result = calendars_resource.delete_exclusions(calendar_id, exclusions)

        # Verify the result
        assert isinstance(result, ExclusionResponse)
        assert result.exclusions == ["2024-01-01"]

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/calendars/cal_123/exclusions/remove"
        assert kwargs["json"] == {"exclusions": exclusions}
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_delete_exclusions_too_many(self, calendars_resource):
        """Test deleting too many exclusions from a calendar."""
        # Create a list with more than 1000 exclusions
        exclusions = [f"2024-01-{i:02d}" for i in range(1, 1002)]
        
        # Call the method and expect an exception
        with pytest.raises(NaxaiValueError) as excinfo:
            calendars_resource.delete_exclusions("cal_123", exclusions)
        
        assert "You can only delete up to 1000 exclusions at a time" in str(excinfo.value)