"""
Unit tests for the synchronous ReportingResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.email_resources.reporting import ReportingResource
from naxai.resources.email_resources.reporting_resources.metrics import MetricsResource
from naxai.resources.email_resources.reporting_resources.clicked_urls import ClickedUrlsResource


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
        return ReportingResource(mock_client, "/email")

    def test_initialization(self, reporting_resource):
        """Test that the ReportingResource initializes correctly with all sub-resources."""
        assert reporting_resource.root_path == "/email/reporting"
        
        # Verify sub-resources are initialized
        assert isinstance(reporting_resource.metrics, MetricsResource)
        assert isinstance(reporting_resource.cliqued_urls, ClickedUrlsResource)
        
        # Verify sub-resources have correct root paths
        assert reporting_resource.metrics.root_path == "/email/reporting/metrics"
        assert reporting_resource.cliqued_urls.root_path == "/email/reporting/clicks"