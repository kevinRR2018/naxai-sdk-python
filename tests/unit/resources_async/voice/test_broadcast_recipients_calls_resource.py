"""
Unit tests for the asynchronous CallsResource class.
"""
import json
import pytest
from unittest.mock import MagicMock, AsyncMock
from naxai.resources_async.voice_resources.broadcast_resources.recipients_resources.calls import CallsResource
from naxai.models.voice.responses.broadcasts_responses import GetBroadcastRecipientCallsResponse


class TestCallsResource:
    """Test suite for the asynchronous CallsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def calls_resource(self, mock_client):
        """Create a CallsResource instance with a mock client."""
        return CallsResource(mock_client, "/voice/broadcasts")

    def test_initialization(self, calls_resource):
        """Test that the CallsResource initializes correctly."""
        assert calls_resource.root_path == "/voice/broadcasts"
        assert calls_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_calls(self, calls_resource, mock_client):
        """Test listing calls for a recipient."""
        # Setup mock response
        mock_response = [
            {
                "callId": "call_123",
                "status": "delivered",
                "reason": "success",
                "attemptOrder": 1,
                "duration": 60,
                "callAt": 1672531200000
            },
            {
                "callId": "call_456",
                "status": "failed",
                "reason": "no-answer",
                "attemptOrder": 2,
                "duration": 0,
                "callAt": 1672534800000
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        recipient_id = "recipient_123"
        result = await calls_resource.list(broadcast_id, recipient_id)

        # Verify the result
        assert isinstance(result, GetBroadcastRecipientCallsResponse)
        assert len(result) == 2
        assert result[0].call_id == "call_123"
        assert result[0].status == "delivered"
        assert result[0].reason == "success"
        assert result[0].attempt_order == 1
        assert result[0].duration == 60
        assert result[1].call_id == "call_456"
        assert result[1].status == "failed"
        assert result[1].reason == "no-answer"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/broadcasts/broadcast_123/recipients/recipient_123/calls"
        assert kwargs["headers"] == {"Content-Type": "application/json"}