"""
Unit tests for the synchronous RecipientsResource class.
"""
import json
import pytest
from unittest.mock import MagicMock
from naxai.resources.voice_resources.broadcast_resources.recipients import RecipientsResource
from naxai.models.voice.voice_flow import VoiceFlow, Welcome
from naxai.models.voice.responses.broadcasts_responses import ListBroadcastRecipientsResponse, GetBroadcastRecipientResponse


class TestRecipientsResource:
    """Test suite for the synchronous RecipientsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def recipients_resource(self, mock_client):
        """Create a RecipientsResource instance with a mock client."""
        return RecipientsResource(mock_client, "/voice/broadcasts")

    def test_initialization(self, recipients_resource, mock_client):
        """Test that the RecipientsResource initializes correctly."""
        assert recipients_resource.root_path == "/voice/broadcasts"
        assert recipients_resource.headers == {"Content-Type": "application/json"}
        assert recipients_resource.calls is not None
        assert recipients_resource.calls._client == mock_client
        assert recipients_resource.calls.root_path == "/voice/broadcasts"

    def test_list_recipients(self, recipients_resource, mock_client):
        """Test listing recipients for a broadcast."""
        # Setup mock response
        mock_response = {
            "items": [
                {
                    "recipientId": "recipient_123",
                    "broadcastId": "broadcast_123",
                    "phone": "+1234567890",
                    "status": "delivered",
                    "completed": True,
                    "calls": 1,
                    "input": "1",
                    "transferred": False,
                    "lastUpdatedAt": 1672531200000,
                    "voiceFlow": {"welcome": {"say": "Hello from Naxai SDK!"}},
                    "contactId": "contact_123"
                },
                {
                    "recipientId": "recipient_456",
                    "broadcastId": "broadcast_123",
                    "phone": "+1987654321",
                    "status": "failed",
                    "completed": False,
                    "calls": 3,
                    "input": "",
                    "transferred": False,
                    "lastUpdatedAt": 1672531200000,
                    "voiceFlow": {"welcome": {"say": "Hello from Naxai SDK!"}},
                    "contactId": "contact_456"
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 25,
                "totalPage": 1,
                "totalRecord": 2,
                "returnedRecord": 2,
                "remainingRecord": 0
            }
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = recipients_resource.list(broadcast_id, page=1, page_size=25, status="delivered")

        # Verify the result
        assert isinstance(result, ListBroadcastRecipientsResponse)
        assert len(result.items) == 2
        assert result.items[0].recipient_id == "recipient_123"
        assert result.items[0].phone == "+1234567890"
        assert result.items[0].status == "delivered"
        assert result.items[0].completed is True
        assert result.items[1].recipient_id == "recipient_456"
        assert result.pagination.page == 1
        assert result.pagination.total_record == 2

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/broadcasts/broadcast_123/recipients"
        assert kwargs["params"] == {"page": 1, "pagesize": 25, "status": "delivered"}
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_get_recipient(self, recipients_resource, mock_client):
        """Test getting a recipient for a broadcast."""
        # Setup mock response
        mock_response = {
            "recipientId": "recipient_123",
            "broadcastId": "broadcast_123",
            "phone": "+1234567890",
            "status": "delivered",
            "completed": True,
            "calls": 1,
            "input": "1",
            "transferred": False,
            "lastUpdatedAt": 1672531200000,
            "voiceFlow": {"welcome": {"say": "Hello from Naxai SDK!"}},
            "contactId": "contact_123"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        recipient_id = "recipient_123"
        result = recipients_resource.get(broadcast_id, recipient_id)

        # Verify the result
        assert isinstance(result, GetBroadcastRecipientResponse)
        assert result.recipient_id == "recipient_123"
        assert result.phone == "+1234567890"
        assert result.status == "delivered"
        assert result.completed is True
        assert result.calls == 1
        assert result.input_ == "1"
        assert result.transferred is False
        assert result.voice_flow == VoiceFlow(welcome=Welcome(say="Hello from Naxai SDK!"))
        assert result.contact_id == "contact_123"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/broadcasts/broadcast_123/recipients/recipient_123"
        assert kwargs["headers"] == {"Content-Type": "application/json"}