"""
Unit tests for the asynchronous SMSResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.sms import SMSResource
from naxai.models.sms.responses.send_responses import SendSMSResponse, BaseMessageModel
from naxai.base.exceptions import NaxaiValueError
from naxai.resources_async.sms_resources.activity_logs import ActivityLogsResource
from naxai.resources_async.sms_resources.reporting import ReportingResource


class TestSMSResourceAsync:
    """Test suite for the asynchronous SMSResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def sms_resource(self, mock_client):
        """Create an SMSResource instance with a mock client."""
        return SMSResource(mock_client)

    def test_initialization(self, sms_resource, mock_client):
        """Test that the SMSResource initializes correctly."""
        assert sms_resource.root_path == "/sms"
        assert sms_resource.headers == {"Content-Type": "application/json"}
        
        # Test that sub-resources are initialized correctly
        assert isinstance(sms_resource.activity_logs, ActivityLogsResource)
        assert isinstance(sms_resource.reporting, ReportingResource)
        
        assert sms_resource.activity_logs.root_path == "/sms/activity-logs"
        assert sms_resource.reporting.root_path == "/sms/reporting/metrics"
        
        # Test that sub-resources have the correct client
        assert sms_resource.activity_logs._client == mock_client
        assert sms_resource.reporting._client == mock_client

    @pytest.mark.asyncio
    async def test_send_with_from(self, sms_resource, mock_client):
        """Test sending SMS with from_ parameter."""
        # Setup mock response
        mock_response = {
            "batchId": "batch_123abc",
            "count": 2,
            "messages": [
                {
                    "to": "+1234567890",
                    "messageId": "msg_123abc"
                },
                {
                    "to": "+1987654321",
                    "messageId": "msg_456def"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await sms_resource.send(
            to=["+1234567890", "+1987654321"],
            body="Test message",
            from_="+18005551234",
            type_="text",
            reference="test-ref-123"
        )

        # Verify the result
        assert isinstance(result, SendSMSResponse)
        assert result.batch_id == "batch_123abc"
        assert result.count == 2
        assert len(result.messages) == 2
        
        assert isinstance(result.messages[0], BaseMessageModel)
        assert result.messages[0].to == "+1234567890"
        assert result.messages[0].message_id == "msg_123abc"
        
        assert result.messages[1].to == "+1987654321"
        assert result.messages[1].message_id == "msg_456def"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/sms/send"
        assert kwargs["headers"] == {"Content-Type": "application/json"}
        
        # Check request body
        expected_body = {
            "to": ["+1234567890", "+1987654321"],
            "body": "Test message",
            "from": "+18005551234",
            "type": "text",
            "truncate": False,
            "reference": "test-ref-123"
        }
        assert kwargs["json"] == expected_body

    @pytest.mark.asyncio
    async def test_send_with_sender_service_id(self, sms_resource, mock_client):
        """Test sending SMS with sender_service_id parameter."""
        # Setup mock response
        mock_response = {
            "batchId": "batch_789xyz",
            "count": 1,
            "messages": [
                {
                    "to": "+1234567890",
                    "messageId": "msg_789xyz"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await sms_resource.send(
            to=["+1234567890"],
            body="Test message with service ID",
            sender_service_id="svc_marketing_123",
            type_="unicode",
            max_parts=3,
            truncate=True
        )

        # Verify the result
        assert isinstance(result, SendSMSResponse)
        assert result.batch_id == "batch_789xyz"
        assert result.count == 1
        assert len(result.messages) == 1
        assert result.messages[0].to == "+1234567890"
        assert result.messages[0].message_id == "msg_789xyz"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/sms/send"
        
        # Check request body
        expected_body = {
            "to": ["+1234567890"],
            "body": "Test message with service ID",
            "senderServiceId": "svc_marketing_123",
            "type": "unicode",
            "truncate": True,
            "maxParts": 3
        }
        assert kwargs["json"] == expected_body

    @pytest.mark.asyncio
    async def test_send_with_scheduled_at(self, sms_resource, mock_client):
        """Test sending SMS with scheduled_at parameter."""
        # Setup mock response
        mock_response = {
            "batchId": "batch_scheduled_123",
            "count": 1,
            "messages": [
                {
                    "to": "+1234567890",
                    "messageId": "msg_scheduled_123"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await sms_resource.send(
            to=["+1234567890"],
            body="Scheduled message",
            from_="+18005551234",
            scheduled_at="2023-12-31T14:00:00Z",
            validity=60,
            idempotency_key="unique-id-123456"
        )

        # Verify the result
        assert isinstance(result, SendSMSResponse)
        assert result.batch_id == "batch_scheduled_123"
        assert result.count == 1

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/sms/send"
        
        # Check request body
        expected_body = {
            "to": ["+1234567890"],
            "body": "Scheduled message",
            "from": "+18005551234",
            "type": "text",
            "truncate": False,
            "scheduledAt": "2023-12-31T14:00:00Z",
            "validity": 60,
            "idempotencyKey": "unique-id-123456"
        }
        assert kwargs["json"] == expected_body

    @pytest.mark.asyncio
    async def test_send_missing_from_and_sender_service_id(self, sms_resource):
        """Test sending SMS without from_ or sender_service_id raises an error."""
        with pytest.raises(NaxaiValueError) as excinfo:
            await sms_resource.send(
                to=["+1234567890"],
                body="Test message"
            )
        
        assert "Either 'from_' or 'sender_service_id' must be provided" in str(excinfo.value)