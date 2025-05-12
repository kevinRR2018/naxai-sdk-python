"""
Unit tests for the asynchronous ActivityLogsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.email_resources.activity_logs import ActivityLogsResource
from naxai.models.email.responses.activity_logs_responses import (
    ListEmailActivityLogsResponse,
    GetEmailActivityLogsResponse,
    BaseActivityLogs
)
from naxai.models.base.pagination import Pagination


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
        return ActivityLogsResource(mock_client, "/email")

    def test_initialization(self, activity_logs_resource):
        """Test that the ActivityLogsResource initializes correctly."""
        assert activity_logs_resource.root_path == "/email/activity-logs"
        assert activity_logs_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_activity_logs(self, activity_logs_resource, mock_client):
        """Test listing email activity logs."""
        # Setup mock response with proper structure
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 25,
                "totalRecord": 87,
                "returnedRecord": 25,
                "remainingRecord": 62
            },
            "messages": [
                {
                    "messageId": "email_123abc",
                    "fromEmail": "sender@example.com",
                    "toEmail": "recipient1@example.com",
                    "subject": "Test Email 1",
                    "status": "delivered",
                    "createdAt": 1672567200000,
                    "updatedAt": 1672567300000,
                    "opens": 2,
                    "clicks": 1
                },
                {
                    "messageId": "email_456def",
                    "fromEmail": "sender@example.com",
                    "toEmail": "recipient2@example.com",
                    "subject": "Test Email 2",
                    "status": "failed",
                    "createdAt": 1672567500000,
                    "updatedAt": 1672567600000,
                    "opens": 0,
                    "clicks": 0
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await activity_logs_resource.list(
            page=1,
            page_size=25,
            start=1672531200000,  # Jan 1, 2023
            stop=1704067199000,   # Dec 31, 2023
            status="delivered"
        )

        # Verify the result
        assert isinstance(result, ListEmailActivityLogsResponse)
        assert result.pagination.page == 1
        assert result.pagination.page_size == 25
        assert result.pagination.total_record == 87
        assert result.pagination.returned_record == 25
        assert result.pagination.remaining_record == 62
        assert len(result.messages) == 2
        assert result.messages[0].message_id == "email_123abc"
        assert result.messages[0].from_email == "sender@example.com"
        assert result.messages[0].to_email == "recipient1@example.com"
        assert result.messages[0].subject == "Test Email 1"
        assert result.messages[0].status == "delivered"
        assert result.messages[0].opens == 2
        assert result.messages[0].clicks == 1
        assert result.messages[1].message_id == "email_456def"
        assert result.messages[1].status == "failed"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/activity-logs"
        assert kwargs["params"]["page"] == 1
        assert kwargs["params"]["pageSize"] == 25
        assert kwargs["params"]["start"] == 1672531200000
        assert kwargs["params"]["stop"] == 1704067199000
        assert kwargs["params"]["status"] == "delivered"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_get_activity_log(self, activity_logs_resource, mock_client):
        """Test getting a specific email activity log."""
        # Setup mock response with proper structure
        mock_response = {
            "messageId": "email_123abc",
            "fromEmail": "sender@example.com",
            "toEmail": "recipient@example.com",
            "email": "recipient@example.com",
            "subject": "Test Email",
            "status": "delivered",
            "createdAt": 1672567200000,
            "updatedAt": 1672567300000,
            "opens": 2,
            "clicks": 1,
            "clientId": "client_789",
            "campaignId": "campaign_456",
            "events": [
                {
                    "name": "sent",
                    "processed": 1672567200000,
                    "reason": None
                },
                {
                    "name": "delivered",
                    "processed": 1672567300000,
                    "reason": "success"
                },
                {
                    "name": "opened",
                    "processed": 1672570800000,
                    "reason": None
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        message_id = "email_123abc"
        email = "recipient@example.com"
        result = await activity_logs_resource.get(message_id, email)

        # Verify the result
        assert isinstance(result, GetEmailActivityLogsResponse)
        assert result.message_id == "email_123abc"
        assert result.from_email == "sender@example.com"
        assert result.to_email == "recipient@example.com"
        assert result.email == "recipient@example.com"
        assert result.subject == "Test Email"
        assert result.status == "delivered"
        assert result.created_at == 1672567200000
        assert result.updated_at == 1672567300000
        assert result.opens == 2
        assert result.clicks == 1
        assert result.client_id == "client_789"
        assert result.campaign_id == "campaign_456"
        assert len(result.events) == 3
        assert result.events[0].name == "sent"
        assert result.events[0].processed == 1672567200000
        assert result.events[1].name == "delivered"
        assert result.events[1].reason == "success"
        assert result.events[2].name == "opened"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/activity-logs/email_123abc/recipient@example.com",
            headers={"Content-Type": "application/json"}
        )