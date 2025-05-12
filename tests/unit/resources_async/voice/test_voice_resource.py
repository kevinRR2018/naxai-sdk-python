"""
Unit tests for the asynchronous VoiceResource class.
"""
import pytest
from unittest.mock import MagicMock, AsyncMock
from naxai.resources_async.voice import VoiceResource
from naxai.resources_async.voice_resources.call import CallResource
from naxai.resources_async.voice_resources.broadcast import BroadcastsResource
from naxai.resources_async.voice_resources.reporting import ReportingResource
from naxai.resources_async.voice_resources.activity_logs import ActivityLogsResource


class TestVoiceResource:
    """Test suite for the asynchronous VoiceResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def voice_resource(self, mock_client):
        """Create a VoiceResource instance with a mock client."""
        return VoiceResource(mock_client)

    def test_initialization(self, voice_resource, mock_client):
        """Test that the VoiceResource initializes correctly with all sub-resources."""
        # Test root path
        assert voice_resource.root_path == "/voice"
        
        # Test client assignment
        assert voice_resource._client == mock_client
        
        # Test sub-resources initialization
        assert isinstance(voice_resource.call, CallResource)
        assert isinstance(voice_resource.broadcasts, BroadcastsResource)
        assert isinstance(voice_resource.reporting, ReportingResource)
        assert isinstance(voice_resource.activity_logs, ActivityLogsResource)
        
        # Test sub-resources have correct client
        assert voice_resource.call._client == mock_client
        assert voice_resource.broadcasts._client == mock_client
        assert voice_resource.reporting._client == mock_client
        assert voice_resource.activity_logs._client == mock_client
        
        # Test sub-resources have correct root paths
        assert voice_resource.call.root_path == "/voice/call"
        assert voice_resource.broadcasts.root_path == "/voice/broadcasts"
        assert voice_resource.reporting.root_path == "/voice/reporting/metrics"
        assert voice_resource.activity_logs.root_path == "/voice/activity-logs"