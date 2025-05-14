"""
Unit tests for the synchronous MetricsResource class.
"""
import json
import pytest
from unittest.mock import MagicMock
from naxai.resources.voice_resources.broadcast_resources.metrics import MetricsResource
from naxai.models.voice.responses.broadcasts_responses import GetBroadcastMetricsResponse


class TestMetricsResource:
    """Test suite for the synchronous MetricsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def metrics_resource(self, mock_client):
        """Create a MetricsResource instance with a mock client."""
        return MetricsResource(mock_client, "/voice/broadcasts")

    def test_initialization(self, metrics_resource, mock_client):
        """Test that the MetricsResource initializes correctly."""
        assert metrics_resource.root_path == "/voice/broadcasts"
        assert metrics_resource.headers == {"Content-Type": "application/json"}
        assert metrics_resource.input is not None
        assert metrics_resource.input._client == mock_client
        assert metrics_resource.input.root_path == "/voice/broadcasts"

    def test_get_metrics(self, metrics_resource, mock_client):
        """Test getting metrics for a broadcast."""
        # Setup mock response
        mock_response = {
            "total": 100,
            "completed": 80,
            "delivered": 85,
            "failed": 10,
            "canceled": 5,
            "paused": 0,
            "invalid": 0,
            "inProgress": 0,
            "transferred": 5,
            "calls": 120
        }
        mock_client._request.return_value = mock_response

        # Call the method
        broadcast_id = "broadcast_123"
        result = metrics_resource.get(broadcast_id)

        # Verify the result
        assert isinstance(result, GetBroadcastMetricsResponse)
        assert result.total == 100
        assert result.completed == 80
        assert result.delivered == 85
        assert result.failed == 10
        assert result.canceled == 5
        assert result.paused == 0
        assert result.invalid == 0
        assert result.in_progress == 0
        assert result.transferred == 5
        assert result.calls == 120

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/voice/broadcasts/broadcast_123/metrics"
        assert kwargs["headers"] == {"Content-Type": "application/json"}