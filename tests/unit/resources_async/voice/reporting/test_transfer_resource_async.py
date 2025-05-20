"""
Unit tests for the asynchronous TransferResource class.
"""
import pytest
from unittest.mock import MagicMock, AsyncMock
from naxai.resources_async.voice_resources.reporting_resources.transfer import TransferResource
from naxai.base.exceptions import NaxaiValueError

class TestTransferResource:
    """Test suite for the asynchronous TransferResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def transfer_resource(self, mock_client):
        """Create a TransferResource instance with a mock client."""
        return TransferResource(mock_client, "/voice/reporting/metrics")

    def test_initialization(self, transfer_resource):
        """Test that the TransferResource initializes correctly."""
        assert transfer_resource.root_path == "/voice/reporting/metrics/transfer"
        assert transfer_resource.headers == {"Content-Type": "application/json"}


    @pytest.mark.asyncio
    async def test_list_with_day_grouping(self, transfer_resource, mock_client):
        """Test listing metrics with daily grouping."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "transfer",
            "group": "day",
            "number": "123456",
            "stats": []
        }

        response = await transfer_resource.list(
            group="day",
            start_date="2023-01-01",
            stop_date="2023-01-31"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/transfer",
            params={
                "group": "day",
                "startDate": "2023-01-01",
                "stopDate": "2023-01-31"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "transfer"
        assert response.group == "day"

    @pytest.mark.asyncio
    async def test_list_with_month_grouping(self, transfer_resource, mock_client):
        """Test listing metrics with monthly grouping."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-12-31",
            "direction": "transfer",
            "group": "month",
            "number": "123456",
            "stats": []
        }

        response = await transfer_resource.list(
            group="month",
            start_date="2023-01-01",
            stop_date="2023-12-31"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/transfer",
            params={
                "group": "month",
                "startDate": "2023-01-01",
                "stopDate": "2023-12-31"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.direction == "transfer"
        assert response.group == "month"

    @pytest.mark.asyncio
    async def test_list_with_number_filter(self, transfer_resource, mock_client):
        """Test listing metrics with phone number filter."""
        mock_client._request.return_value = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "transfer",
            "group": "day",
            "number": "+1234567890",
            "stats": []
        }

        response = await transfer_resource.list(
            group="day",
            start_date="2023-01-01",
            stop_date="2023-01-31",
            number="+1234567890"
        )

        mock_client._request.assert_called_once_with(
            "GET",
            "/voice/reporting/metrics/transfer",
            params={
                "group": "day",
                "startDate": "2023-01-01",
                "stopDate": "2023-01-31",
                "number": "+1234567890"
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.number == "+1234567890"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("group,start_date,stop_date,error_msg", [
        ("hour", None, None, "startDate must be provided when group is 'hour'"),
        ("hour", "2023-01-01", None, "startDate must be in the format 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS' when group is 'hour'"),
        ("hour", "2023-01-01 00:00:00", "2023-01-01", "stopDate must be in the format 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS' when group is 'hour'"),
        ("day", None, None, "startDate must be provided when group is 'day' or 'month'"),
        ("day", "2023-01-01", None, "stopDate must be provided when group is 'day' or 'month'"),
        ("month", "2023-01", "2023-12", "startDate must be in the format 'YYYY-MM-DD' or 'YY-MM-DD'"),
    ])
    async def test_list_validation_errors(self, transfer_resource, group, start_date, stop_date, error_msg):
        """Test validation errors for invalid parameters."""
        with pytest.raises(NaxaiValueError, match=error_msg):
            await transfer_resource.list(group=group, start_date=start_date, stop_date=stop_date) 