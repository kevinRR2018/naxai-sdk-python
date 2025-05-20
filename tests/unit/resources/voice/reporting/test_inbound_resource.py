"""
Unit tests for the synchronous InboundResource class.
"""
import pytest
from unittest.mock import MagicMock
from naxai.resources.voice_resources.reporting_resources.inbound import InboundResource
from naxai.base.exceptions import NaxaiValueError

class TestInboundResource:
    """Test suite for the synchronous InboundResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def inbound_resource(self, mock_client):
        """Create an InboundResource instance with a mock client."""
        return InboundResource(mock_client, "/voice/reporting/metrics")

    def test_initialization(self, inbound_resource):
        """Test that the InboundResource initializes correctly."""
        assert inbound_resource.root_path == "/voice/reporting/metrics/inbound"
        assert inbound_resource.headers == {"Content-Type": "application/json"}

    def test_list_with_hour_grouping(self, inbound_resource, mock_client):
        """Test listing metrics with hourly grouping."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01 00:00:00",
            "stopDate": "2023-01-01 23:59:59",
            "direction": "inbound",
            "group": "hour",
            "number": "123456",
            "stats": []
        }

        response = inbound_resource.list(
            group="hour",
            start_date="2023-01-01 00:00:00",
            stop_date="2023-01-01 23:59:59"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/inbound",
            params={
                "group": "hour",
                "startDate": "2023-01-01 00:00:00",
                "stopDate": "2023-01-01 23:59:59"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "inbound"
        assert response.group == "hour"

    def test_list_with_day_grouping(self, inbound_resource, mock_client):
        """Test listing metrics with daily grouping."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "inbound",
            "group": "day",
            "number": "123456",
            "stats": []
        }

        response = inbound_resource.list(
            group="day",
            start_date="2023-01-01",
            stop_date="2023-01-31"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/inbound",
            params={
                "group": "day",
                "startDate": "2023-01-01",
                "stopDate": "2023-01-31"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "inbound"
        assert response.group == "day"

    def test_list_with_month_grouping(self, inbound_resource, mock_client):
        """Test listing metrics with monthly grouping."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-12-31",
            "direction": "inbound",
            "group": "month",
            "number": "123456",
            "stats": []
        }

        response = inbound_resource.list(
            group="month",
            start_date="2023-01-01",
            stop_date="2023-12-31"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/inbound",
            params={
                "group": "month",
                "startDate": "2023-01-01",
                "stopDate": "2023-12-31"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "inbound"
        assert response.group == "month"

    def test_list_with_number_filter(self, inbound_resource, mock_client):
        """Test listing metrics with phone number filter."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "inbound",
            "group": "day",
            "number": "+1234567890",
            "stats": []
        }

        response = inbound_resource.list(
            group="day",
            start_date="2023-01-01",
            stop_date="2023-01-31",
            number="+1234567890"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/inbound",
            params={
                "group": "day",
                "startDate": "2023-01-01",
                "stopDate": "2023-01-31",
                "number": "+1234567890"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.number == "+1234567890"

    @pytest.mark.parametrize("group,start_date,stop_date,error_msg", [
        ("hour", None, None, "startDate must be provided when group is 'hour'"),
        ("hour", "2023-01-01", None, "startDate must be in the format 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS' when group is 'hour'"),
        ("hour", "2023-01-01 00:00:00", "2023-01-01", "stopDate must be in the format 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS' when group is 'hour'"),
        ("day", None, None, "startDate must be provided when group is 'day' or 'month'"),
        ("day", "2023-01-01", None, "stopDate must be provided when group is 'day' or 'month'"),
        ("month", "2023-01", "2023-12", "startDate must be in the format 'YYYY-MM-DD' or 'YY-MM-DD'"),
    ])
    def test_list_validation_errors(self, inbound_resource, group, start_date, stop_date, error_msg):
        """Test validation errors for invalid parameters."""
        with pytest.raises(NaxaiValueError, match=error_msg):
            inbound_resource.list(group=group, start_date=start_date, stop_date=stop_date) 