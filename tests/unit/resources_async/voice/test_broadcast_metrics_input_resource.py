"""
Unit tests for the asynchronous InputResource class.
"""
import json
import pytest
from unittest.mock import MagicMock, AsyncMock
from naxai.resources_async.voice_resources.broadcast_resources.broadcast_metrics_resources.input import InputResource
from naxai.models.voice.responses.broadcasts_responses import GetBroadcastInputMetricsResponse


class TestInputResource:
    """Test suite for the asynchronous InputResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def input_resource(self, mock_client):
        """Create an InputResource instance with a mock client."""
        return InputResource(mock_client, "/voice/broadcasts")

    def test_initialization(self, input_resource):
        """Test that the InputResource initializes correctly."""
        assert input_resource.root_path == "/voice/broadcasts"
        assert input_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_get_input_metrics(self, input_resource, mock_client):
        """Test getting input metrics for a broadcast."""
        # Setup mock response
        mock_response = {
            "0": 10,
            "1": 25,
            "2": 15,
            "3": 5,
            "4": 3,
            "5": 2,
            "6": 1,
            "7": 0,
            "8": 0,
            "9": 0,
            "star": 5,
            "hash": 2,
            "total": 68
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = await input_resource.get(broadcast_id)

        # Verify the result
        assert isinstance(result, GetBroadcastInputMetricsResponse)
        assert result.input_0 == 10
        assert result.input_1 == 25
        assert result.input_2 == 15
        assert result.input_3 == 5
        assert result.input_4 == 3
        assert result.input_5 == 2
        assert result.input_6 == 1
        assert result.input_7 == 0
        assert result.input_8 == 0
        assert result.input_9 == 0
        assert result.input_star == 5
        assert result.input_hash == 2
        assert result.total == 68

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/broadcasts/broadcast_123/metrics/input"
        assert kwargs["headers"] == {"Content-Type": "application/json"}