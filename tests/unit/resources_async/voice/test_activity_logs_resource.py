"""
Unit tests for the asynchronous ActivityLogsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.voice_resources.activity_logs import ActivityLogsResource
from naxai.models.voice.responses.activity_logs_responses import (
    ListActivityLogsResponse,
    GetActivityLogResponse
)


class TestActivityLogsResource:
    """Test suite for the asynchronous ActivityLogsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def activity_logs_resource(self, mock_client):
        """Create an ActivityLogsResource instance with a mock client."""
        return ActivityLogsResource(mock_client, "/voice")

    def test_initialization(self, activity_logs_resource):
        """Test that the ActivityLogsResource initializes correctly."""
        assert activity_logs_resource.root_path == "/voice/activity-logs"
        assert activity_logs_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_activity_logs(self, activity_logs_resource, mock_client):
        """Test listing activity logs."""
        # Setup mock response with proper aliases
        mock_response = {
            "items": [
                {
                    "callId": "call_123",
                    "from": "9876543210",
                    "to": "1234567890",
                    "direction": "outbound",
                    "status": "delivered",
                    "callDuration": 60,
                    "callDate": 123456,
                    "transferred": False,
                    "network": "landline",
                    "country": "BE",
                    "details": "connected",
                    "reason": "success",
                    "callType": "marketing"
                },
                {
                    "callId": "call_456",
                    "from": "9876543210",
                    "to": "1234567891",
                    "direction": "outbound",
                    "status": "failed",
                    "callDuration": 0,
                    "callDate": 1345678,
                    "transferred": False,
                    "network": "mobile",
                    "country": "BE",
                    "details": "rejected",
                    "reason": "rejected",
                    "callType": "marketing"
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 25,
                "returnedRecord": 2,
                "totalRecord": 2,
                "remainingRecord": 0
            }
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await activity_logs_resource.list(
            page=1,
            page_size=25,
            direction="outbound",
            from_="9876543210"
        )

        # Verify the result
        assert isinstance(result, ListActivityLogsResponse)
        assert len(result.items) == 2
        assert result.items[0].call_id == "call_123"
        assert result.items[0].from_ == "9876543210"
        assert result.items[0].to == "1234567890"
        assert result.items[0].direction == "outbound"
        assert result.items[0].status == "delivered"
        assert result.items[0].call_duration == 60
        assert result.pagination.page == 1
        assert result.pagination.total_record == 2

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/activity-logs"
        assert kwargs["params"]["page"] == 1
        assert kwargs["params"]["page_size"] == 25
        assert kwargs["params"]["direction"] == "outbound"
        assert kwargs["params"]["from"] == "9876543210"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_activity_logs_with_all_filters(self, activity_logs_resource, mock_client):
        """Test listing activity logs with all filters."""
        # Setup mock response with proper aliases
        mock_response = {
            "items": [],
             "pagination": {
                "page": 1,
                "pageSize": 25,
                "totalRecord": 0,
                "returnedRecord": 0,
                "remainingRecord": 0
            }
        }
        mock_client._request.return_value = mock_response

        # Call the method with all filters
        result = await activity_logs_resource.list(
            page=1,
            page_size=25,
            start=1672531200000,  # Jan 1, 2023
            stop=1704067199000,   # Dec 31, 2023
            direction="outbound",
            status="delivered",
            from_="9876543210",
            to="1234567890",
            client_id="client_123",
            campaign_id="campaign_123",
            broadcast_id="broadcast_123"
        )

        # Verify the result
        assert isinstance(result, ListActivityLogsResponse)
        assert len(result.items) == 0
        assert result.pagination.page == 1
        assert result.pagination.total_record == 0

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/activity-logs"
        assert kwargs["params"]["page"] == 1
        assert kwargs["params"]["page_size"] == 25
        assert kwargs["params"]["start"] == 1672531200000
        assert kwargs["params"]["stop"] == 1704067199000
        assert kwargs["params"]["direction"] == "outbound"
        assert kwargs["params"]["status"] == "delivered"
        assert kwargs["params"]["from"] == "9876543210"
        assert kwargs["params"]["to"] == "1234567890"
        assert kwargs["params"]["clientId"] == "client_123"
        assert kwargs["params"]["campaignId"] == "campaign_123"
        assert kwargs["params"]["broadcastId"] == "broadcast_123"

    @pytest.mark.asyncio
    async def test_get_activity_log(self, activity_logs_resource, mock_client):
        """Test getting a specific activity log."""
        # Setup mock response with proper aliases
        mock_response = {
            "callId": "call_123",
            "from": "9876543210",
            "to": "1234567890",
            "direction": "outbound",
            "network": "mobile",
            "country": "BE",
            "details": "success",
            "status": "delivered",
            "callDuration": 60,
            "callDate": 123456,
            "reason": "success",
            "callType": "marketing",
            "transferred": False,
            "transferCallId": None,
            "transferStatus": None
        }
        mock_client._request.return_value = mock_response

        # Call the method
        call_id = "call_123"
        result = await activity_logs_resource.get(call_id)

        # Verify the result
        assert isinstance(result, GetActivityLogResponse)
        assert result.call_id == "call_123"
        assert result.from_ == "9876543210"
        assert result.to == "1234567890"
        assert result.direction == "outbound"
        assert result.status == "delivered"
        assert result.call_duration == 60
        assert result.reason == "success"
        assert result.transferred is False
        assert result.transfer_call_id is None
        assert result.transfer_status is None

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/activity-logs/call_123"
        assert kwargs["headers"] == {"Content-Type": "application/json"}