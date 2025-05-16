"""
Unit tests for the asynchronous BroadcastsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.voice_resources.broadcast import BroadcastsResource
from naxai.models.voice.requests.broadcasts_requests import CreateBroadcastRequest
from naxai.models.voice.responses.broadcasts_responses import (
    ListBroadcastResponse,
    CreateBroadcastResponse,
    GetBroadcastResponse,
    UpdateBroadcastResponse,
    StartBroadcastResponse,
    PauseBroadcastResponse,
    ResumeBroadcastResponse,
    CancelBroadcastResponse
)


class TestBroadcastsResource:
    """Test suite for the asynchronous BroadcastsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def broadcasts_resource(self, mock_client):
        """Create a BroadcastsResource instance with a mock client."""
        return BroadcastsResource(mock_client, "/voice")

    def test_initialization(self, broadcasts_resource):
        """Test that the BroadcastsResource initializes correctly."""
        assert broadcasts_resource.root_path == "/voice/broadcasts"
        assert broadcasts_resource.headers == {"Content-Type": "application/json"}
        assert broadcasts_resource.metrics is not None
        assert broadcasts_resource.recipients is not None

    @pytest.mark.asyncio
    async def test_list_broadcasts(self, broadcasts_resource, mock_client):
        """Test listing broadcasts."""
        # Setup mock response with proper aliases
        mock_response = {
            "items": [
                {
                    "broadcastId": "broadcast_123",
                    "name": "Test Broadcast",
                    "state": "completed",
                    "totalCount": 100,
                    "completedCount": 100,
                    "createdAt": 1672531200000
                },
                {
                    "broadcastId": "broadcast_456",
                    "name": "Another Broadcast",
                    "state": "processing",
                    "totalCount": 50,
                    "completedCount": 25,
                    "createdAt": 1672531200000
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
        result = await broadcasts_resource.list(page=1, page_size=25)

        # Verify the result
        assert isinstance(result, ListBroadcastResponse)
        assert len(result.items) == 2
        assert result.items[0].broadcast_id == "broadcast_123"
        assert result.items[0].name == "Test Broadcast"
        assert result.items[0].state == "completed"
        assert result.items[1].broadcast_id == "broadcast_456"
        assert result.pagination.page == 1
        assert result.pagination.total_record == 2

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/broadcasts"
        assert kwargs["params"] == {"page": 1, "pageSize": 25}
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_create_broadcast(self, broadcasts_resource, mock_client):
        """Test creating a broadcast."""
        # Setup mock response with proper aliases
        mock_response = {
            "broadcastId": "broadcast_789",
            "name": "New Broadcast",
            "state": "draft",
            "from": "9876543210",
            "segmentIds": ["segment_123"],
            "voiceFlow": {"welcome": {"say": "Welcome message"}},
            "totalCount": 0,
            "completedCount": 0,
            "createdAt": 1672531200000
        }
        mock_client._request.return_value = mock_response

        # Create request data
        request_data = CreateBroadcastRequest(
            name="New Broadcast",
            from_="9876543210",
            segment_ids=["segment_123"],
            voice_flow={"welcome": {"say": "Welcome message"}}
        )

        # Call the method
        result = await broadcasts_resource.create(request_data)

        # Verify the result
        assert isinstance(result, CreateBroadcastResponse)
        assert result.broadcast_id == "broadcast_789"
        assert result.name == "New Broadcast"
        assert result.from_ == "9876543210"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/voice/broadcasts"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_get_broadcast(self, broadcasts_resource, mock_client):
        """Test getting a broadcast."""
        # Setup mock response with proper aliases
        mock_response = {
            "broadcastId": "broadcast_123",
            "name": "Test Broadcast",
            "state": "completed",
            "from": "9876543210",
            "segmentIds": ["segment_123"],
            "voiceFlow": {"welcome": {"say": "Welcome message"}},
            "totalCount": 100,
            "completedCount": 100,
            "createdAt": 1672531200000
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = await broadcasts_resource.get(broadcast_id)

        # Verify the result
        assert isinstance(result, GetBroadcastResponse)
        assert result.broadcast_id == "broadcast_123"
        assert result.name == "Test Broadcast"
        assert result.state == "completed"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/broadcasts/broadcast_123"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_delete_broadcast(self, broadcasts_resource, mock_client):
        """Test deleting a broadcast."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = await broadcasts_resource.delete(broadcast_id)

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "DELETE"
        assert args[1] == "/voice/broadcasts/broadcast_123"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_update_broadcast(self, broadcasts_resource, mock_client):
        """Test updating a broadcast."""
        # Setup mock response with proper aliases
        mock_response = {
            "broadcastId": "broadcast_123",
            "name": "Updated Broadcast",
            "state": "draft",
            "from": "9876543210",
            "segmentIds": ["segment_123"],
            "voiceFlow": {"welcome": {"say": "Updated welcome message"}},
            "totalCount": 0,
            "completedCount": 0,
            "createdAt": 1672531200000
        }
        mock_client._request.return_value = mock_response

        # Create request data
        request_data = CreateBroadcastRequest(
            name="Updated Broadcast",
            from_="9876543210",
            segment_ids=["segment_123"],
            voice_flow={"welcome": {"say": "Updated welcome message"}}
        )

        # Call the method
        broadcast_id = "broadcast_123"
        result = await broadcasts_resource.update(broadcast_id, request_data)

        # Verify the result
        assert isinstance(result, UpdateBroadcastResponse)
        assert result.broadcast_id == "broadcast_123"
        assert result.name == "Updated Broadcast"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "PUT"
        assert args[1] == "/voice/broadcasts/broadcast_123"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_start_broadcast(self, broadcasts_resource, mock_client):
        """Test starting a broadcast."""
        # Setup mock response with proper aliases
        mock_response = {
            "broadcastId": "broadcast_123",
            "state": "starting"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = await broadcasts_resource.start(broadcast_id)

        # Verify the result
        assert isinstance(result, StartBroadcastResponse)
        assert result.broadcast_id == "broadcast_123"
        assert result.state == "starting"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/voice/broadcasts/broadcast_123/start"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_pause_broadcast(self, broadcasts_resource, mock_client):
        """Test pausing a broadcast."""
        # Setup mock response with proper aliases
        mock_response = {
            "broadcastId": "broadcast_123",
            "state": "pausing"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = await broadcasts_resource.pause(broadcast_id)

        # Verify the result
        assert isinstance(result, PauseBroadcastResponse)
        assert result.broadcast_id == "broadcast_123"
        assert result.state == "pausing"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/voice/broadcasts/broadcast_123/pause"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_resume_broadcast(self, broadcasts_resource, mock_client):
        """Test resuming a broadcast."""
        # Setup mock response with proper aliases
        mock_response = {
            "broadcastId": "broadcast_123",
            "state": "resuming"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = await broadcasts_resource.resume(broadcast_id)

        # Verify the result
        assert isinstance(result, ResumeBroadcastResponse)
        assert result.broadcast_id == "broadcast_123"
        assert result.state == "resuming"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/voice/broadcasts/broadcast_123/resume"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_cancel_broadcast(self, broadcasts_resource, mock_client):
        """Test canceling a broadcast."""
        # Setup mock response with proper aliases
        mock_response = {
            "broadcastId": "broadcast_123",
            "state": "canceling"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = await broadcasts_resource.cancel(broadcast_id)

        # Verify the result
        assert isinstance(result, CancelBroadcastResponse)
        assert result.broadcast_id == "broadcast_123"
        assert result.state == "canceling"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/voice/broadcasts/broadcast_123/cancel"
        assert kwargs["headers"] == {"Content-Type": "application/json"}