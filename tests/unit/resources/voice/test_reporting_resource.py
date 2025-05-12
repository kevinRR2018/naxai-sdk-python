"""
Unit tests for the synchronous ReportingResource class.
"""
import pytest
from unittest.mock import MagicMock
from naxai.resources.voice_resources.reporting import ReportingResource
from naxai.resources.voice_resources.reporting_resources.outbound import OutboundResource
from naxai.resources.voice_resources.reporting_resources.inbound import InboundResource
from naxai.resources.voice_resources.reporting_resources.transfer import TransferResource


class TestReportingResource:
    """Test suite for the synchronous ReportingResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def reporting_resource(self, mock_client):
        """Create a ReportingResource instance with a mock client."""
        return ReportingResource(mock_client, "/voice")

    def test_initialization(self, reporting_resource):
        """Test that the ReportingResource initializes correctly with all sub-resources."""
        assert reporting_resource.root_path == "/voice/reporting/metrics"
        assert isinstance(reporting_resource.outbound, OutboundResource)
        assert isinstance(reporting_resource.inbound, InboundResource)
        assert isinstance(reporting_resource.transfer, TransferResource)