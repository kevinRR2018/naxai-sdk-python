"""
Unit tests for the synchronous ActivityLogsResource class for SMS.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.sms_resources.activity_logs import ActivityLogsResource
from naxai.models.sms.responses.activity_logs_responses import (
    ListSMSActivityLogsResponse,
    GetSMSActivityLogsResponse,
    BaseMessage
)
from naxai.models.base.pagination import Pagination


class TestActivityLogsResourceSync:
    """Test suite for the synchronous ActivityLogsResource class for SMS."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def activity_logs_resource(self, mock_client):
        """Create an ActivityLogsResource instance with a mock client."""
        return ActivityLogsResource(mock_client, "/sms")

    def test_initialization(self, activity_logs_resource):
        """Test that the ActivityLogsResource initializes correctly."""
        assert activity_logs_resource.root_path == "/sms/activity-logs"
        assert activity_logs_resource.headers == {"Content-Type": "application/json"}

    def test_list_activity_logs(self, activity_logs_resource, mock_client):
        """Test listing SMS activity logs."""
        # Setup mock response
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 25,
                "totalRecord": 100,
                "returnedRecord": 25,
                "remainingRecord": 75
            },
            "messages": [
                {
                    "messageId": "msg_123abc",
                    "from": "+18005551234",
                    "to": "+1234567890",
                    "body": "Test message 1",
                    "parts": 1,
                    "encoding": "text",
                    "direction": "outgoing",
                    "sentAt": 1703066400000,
                    "submittedAt": 1703066401000,
                    "deliveredAt": 1703066405000,
                    "status": "delivered",
                    "statusCode": 0,
                    "statusReason": "success"
                },
                {
                    "messageId": "msg_456def",
                    "from": "+18005551234",
                    "to": "+1987654321",
                    "body": "Test message 2",
                    "parts": 1,
                    "encoding": "text",
                    "direction": "outgoing",
                    "sentAt": 1703066500000,
                    "submittedAt": 1703066501000,
                    "status": "failed",
                    "statusCode": 1,
                    "statusReason": "destination_unreachable"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = activity_logs_resource.list(
            page=1,
            page_size=25,
            start=1672531200000,  # Jan 1, 2023
            stop=1704067199000,   # Dec 31, 2023
            direction="outbound",
            status="delivered",
            phone_number="+1234567890"
        )

        # Verify the result
        assert isinstance(result, ListSMSActivityLogsResponse)
        assert isinstance(result.pagination, Pagination)
        assert result.pagination.page == 1
        assert result.pagination.page_size == 25
        assert result.pagination.total_record == 100
        assert result.pagination.returned_record == 25
        assert result.pagination.remaining_record == 75
        
        assert len(result.messages) == 2
        assert isinstance(result.messages[0], BaseMessage)
        assert result.messages[0].message_id == "msg_123abc"
        assert result.messages[0].from_ == "+18005551234"
        assert result.messages[0].to == "+1234567890"
        assert result.messages[0].body == "Test message 1"
        assert result.messages[0].parts == 1
        assert result.messages[0].encoding == "text"
        assert result.messages[0].direction == "outgoing"
        assert result.messages[0].sent_at == 1703066400000
        assert result.messages[0].submitted_at == 1703066401000
        assert result.messages[0].delivered_at == 1703066405000
        assert result.messages[0].status == "delivered"
        assert result.messages[0].status_code == 0
        assert result.messages[0].status_reason == "success"
        
        assert result.messages[1].message_id == "msg_456def"
        assert result.messages[1].status == "failed"
        assert result.messages[1].status_reason == "destination_unreachable"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/sms/activity-logs"
        assert kwargs["headers"] == {"Content-Type": "application/json"}
        
        # Check query parameters
        expected_params = {
            "page": 1,
            "pageSize": 25,
            "start": 1672531200000,
            "stop": 1704067199000,
            "direction": "outbound",
            "status": "delivered",
            "phoneNumber": "+1234567890"
        }
        assert kwargs["params"] == expected_params

    def test_list_activity_logs_minimal_params(self, activity_logs_resource, mock_client):
        """Test listing SMS activity logs with minimal parameters."""
        # Setup mock response
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 25,
                "totalRecord": 50,
                "returnedRecord": 25,
                "remainingRecord": 25
            },
            "messages": [
                {
                    "messageId": "msg_123abc",
                    "from": "+18005551234",
                    "to": "+1234567890",
                    "body": "Test message",
                    "parts": 1,
                    "encoding": "text",
                    "direction": "outgoing",
                    "sentAt": 1703066400000,
                    "status": "delivered"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method with minimal parameters
        result = activity_logs_resource.list()

        # Verify the result
        assert isinstance(result, ListSMSActivityLogsResponse)
        assert len(result.messages) == 1

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/sms/activity-logs"
        
        # Check query parameters
        expected_params = {
            "page": 1,
            "pageSize": 25,
        }
        assert kwargs["params"] == expected_params

    def test_get_activity_log(self, activity_logs_resource, mock_client):
        """Test getting a specific SMS activity log."""
        # Setup mock response
        mock_response = {
            "messageId": "msg_123abc",
            "from": "+18005551234",
            "to": "+1234567890",
            "mcc": "310",
            "mnc": "410",
            "body": "Test message details",
            "parts": 1,
            "encoding": "text",
            "direction": "outgoing",
            "sentAt": 1703066400000,
            "submittedAt": 1703066401000,
            "deliveredAt": 1703066405000,
            "status": "delivered",
            "statusCode": 0,
            "statusReason": "success",
            "statusDetails": "Message delivered to handset",
            "reference": "test-ref-123",
            "clientId": "client_789",
            "campaignId": "camp_456"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        message_id = "msg_123abc"
        result = activity_logs_resource.get(message_id)

        # Verify the result
        assert isinstance(result, GetSMSActivityLogsResponse)
        assert result.message_id == "msg_123abc"
        assert result.from_ == "+18005551234"
        assert result.to == "+1234567890"
        assert result.mcc == "310"
        assert result.mnc == "410"
        assert result.body == "Test message details"
        assert result.parts == 1
        assert result.encoding == "text"
        assert result.direction == "outgoing"
        assert result.sent_at == 1703066400000
        assert result.submitted_at == 1703066401000
        assert result.delivered_at == 1703066405000
        assert result.status == "delivered"
        assert result.status_code == 0
        assert result.status_reason == "success"
        assert result.status_details == "Message delivered to handset"
        assert result.reference == "test-ref-123"
        assert result.client_id == "client_789"
        assert result.campaign_id == "camp_456"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/sms/activity-logs/msg_123abc",
            headers={"Content-Type": "application/json"}
        )