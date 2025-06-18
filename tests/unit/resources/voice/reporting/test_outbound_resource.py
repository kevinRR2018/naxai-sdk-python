"""
Unit tests for the synchronous OutboundResource class.
"""
import pytest
from unittest.mock import MagicMock
from naxai.resources.voice_resources.reporting_resources.outbound import OutboundResource
from naxai.base.exceptions import NaxaiValueError

class TestOutboundResource:
    """Test suite for the synchronous OutboundResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def outbound_resource(self, mock_client):
        """Create an OutboundResource instance with a mock client."""
        return OutboundResource(mock_client, "/voice/reporting/metrics")

    def test_initialization(self, outbound_resource):
        """Test that the OutboundResource initializes correctly."""
        assert outbound_resource.root_path == "/voice/reporting/metrics/outbound"
        assert outbound_resource.previous_path == "/voice/reporting/metrics"
        assert outbound_resource.headers == {"Content-Type": "application/json"}

    def test_list_with_hour_grouping(self, outbound_resource, mock_client):
        """Test listing metrics with hourly grouping."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01 00:00:00",
            "stopDate": "2023-01-01 23:59:59",
            "direction": "outbound",
            "group": "hour",
            "number": "123456",
            "stats": []
        }

        response = outbound_resource.list(
            group="hour",
            start_date="2023-01-01 00:00:00",
            stop_date="2023-01-01 23:59:59"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/outbound",
            params={
                "group": "hour",
                "startDate": "2023-01-01 00:00:00",
                "stopDate": "2023-01-01 23:59:59"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "outbound"
        assert response.group == "hour"

    def test_list_with_day_grouping(self, outbound_resource, mock_client):
        """Test listing metrics with daily grouping."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "outbound",
            "group": "day",
            "number": "123456",
            "stats": []
        }

        response = outbound_resource.list(
            group="day",
            start_date="2023-01-01",
            stop_date="2023-01-31"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/outbound",
            params={
                "group": "day",
                "startDate": "2023-01-01",
                "stopDate": "2023-01-31"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "outbound"
        assert response.group == "day"

    def test_list_with_month_grouping(self, outbound_resource, mock_client):
        """Test listing metrics with monthly grouping."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-12-31",
            "direction": "outbound",
            "group": "month",
            "number": "123456",
            "stats": []
        }

        response = outbound_resource.list(
            group="month",
            start_date="2023-01-01",
            stop_date="2023-12-31"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/outbound",
            params={
                "group": "month",
                "startDate": "2023-01-01",
                "stopDate": "2023-12-31"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "outbound"
        assert response.group == "month"

    def test_list_with_number_filter(self, outbound_resource, mock_client):
        """Test listing metrics with phone number filter."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "outbound",
            "group": "day",
            "number": "+1234567890",
            "stats": []
        }

        response = outbound_resource.list(
            group="day",
            start_date="2023-01-01",
            stop_date="2023-01-31",
            number="+1234567890"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/outbound",
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
        ("hour", "2023-01-01", "2023-01-02", "start_date must be in the format 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS' when group is 'hour'"),
        ("hour", "2023-01-01 00:00:00", "2023-01-02", "stop_date must be in the format 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS' when group is 'hour'"),
        ("day", "2023-01", "2023-01-01", "start_date must be in the format 'YYYY-MM-DD' or 'YY-MM-DD'"),
        ("month", "2023-01-01", "2023-12", "stop_date must be in the format 'YYYY-MM-DD' or 'YY-MM-DD'"),
    ])
    def test_list_validation_errors(self, outbound_resource, group, start_date, stop_date, error_msg):
        """Test validation errors for invalid parameters."""
        with pytest.raises(NaxaiValueError, match=error_msg):
            outbound_resource.list(group=group, start_date=start_date, stop_date=stop_date)

    def test_list_by_country(self, outbound_resource, mock_client):
        """Test listing metrics by country."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-12-31",
            "direction": "outbound",
            "number": "123456",
            "stats": []
        }

        response = outbound_resource.list_by_country(
            start_date="2023-01-01",
            stop_date="2023-12-31"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/outbound-by-country",
            params={
                "startDate": "2023-01-01",
                "stopDate": "2023-12-31"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "outbound"

    def test_list_by_country_with_number(self, outbound_resource, mock_client):
        """Test listing metrics by country with phone number filter."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-12-31",
            "direction": "outbound",
            "number": "+1234567890",
            "stats": []
        }

        response = outbound_resource.list_by_country(
            start_date="2023-01-01",
            stop_date="2023-12-31",
            number="+1234567890"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/outbound-by-country",
            params={
                "startDate": "2023-01-01",
                "stopDate": "2023-12-31",
                "number": "+1234567890"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.number == "+1234567890"

    @pytest.mark.parametrize("start_date,stop_date,error_msg", [
        ("2023-1-1", "2023-12-31", "startDate must be in the format 'YYYY-MM-DD'"),
        ("2023-01-01", "2023-12-1", "stopDate must be in the format 'YYYY-MM-DD'"),
    ])
    def test_list_by_country_validation_errors(self, outbound_resource, start_date, stop_date, error_msg):
        """Test validation errors for list_by_country method."""
        with pytest.raises(NaxaiValueError, match=error_msg):
            outbound_resource.list_by_country(start_date=start_date, stop_date=stop_date) 