"""
Unit tests for the synchronous ClickedUrlsResource class.
"""
import json
import datetime
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.email_resources.reporting_resources.clicked_urls import ClickedUrlsResource
from naxai.models.email.responses.metrics_responses import ListClickedUrlsMetricsResponse, BaseClickedUrlsStats


class TestClickedUrlsResource:
    """Test suite for the synchronous ClickedUrlsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def clicked_urls_resource(self, mock_client):
        """Create a ClickedUrlsResource instance with a mock client."""
        return ClickedUrlsResource(mock_client, "/email/reporting")

    def test_initialization(self, clicked_urls_resource):
        """Test that the ClickedUrlsResource initializes correctly."""
        assert clicked_urls_resource.root_path == "/email/reporting/clicks"
        assert clicked_urls_resource.headers == {"Content-Type": "application/json"}

    def test_list_clicked_urls_default_params(self, clicked_urls_resource, mock_client):
        """Test listing clicked URLs metrics with default parameters."""
        # Setup mock response
        mock_response = {
            "start": 1672531200000,  # Jan 1, 2023
            "stop": 1704067199000,   # Dec 31, 2023
            "stats": [
                {
                    "url": "https://example.com/product",
                    "clicked": 250,
                    "clickedUnique": 180
                },
                {
                    "url": "https://example.com/pricing",
                    "clicked": 150,
                    "clickedUnique": 120
                },
                {
                    "url": "https://example.com/contact",
                    "clicked": 80,
                    "clickedUnique": 75
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method with default parameters
        result = clicked_urls_resource.list()

        # Verify the result
        assert isinstance(result, ListClickedUrlsMetricsResponse)
        assert result.start == 1672531200000
        assert result.stop == 1704067199000
        assert len(result.stats) == 3
        
        # Check first URL stats
        assert isinstance(result.stats[0], BaseClickedUrlsStats)
        assert result.stats[0].url == "https://example.com/product"
        assert result.stats[0].clicked == 250
        assert result.stats[0].clicked_unique == 180
        
        # Check second URL stats
        assert result.stats[1].url == "https://example.com/pricing"
        assert result.stats[1].clicked == 150
        assert result.stats[1].clicked_unique == 120
        
        # Check third URL stats
        assert result.stats[2].url == "https://example.com/contact"
        assert result.stats[2].clicked == 80
        assert result.stats[2].clicked_unique == 75

        # Verify the client was called correctly with default parameters
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/reporting/clicks"
        assert "params" in kwargs
        assert "start" in kwargs["params"]
        assert "stop" in kwargs["params"]
        assert kwargs["params"]["group"] == "day"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_list_clicked_urls_custom_params(self, clicked_urls_resource, mock_client):
        """Test listing clicked URLs metrics with custom parameters."""
        # Setup mock response
        mock_response = {
            "start": 1672531200000,  # Jan 1, 2023
            "stop": 1704067199000,   # Dec 31, 2023
            "stats": [
                {
                    "url": "https://example.com/product",
                    "clicked": 2500,
                    "clickedUnique": 1800
                },
                {
                    "url": "https://example.com/pricing",
                    "clicked": 1500,
                    "clickedUnique": 1200
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method with custom parameters
        start = 1672531200  # Jan 1, 2023 (in seconds)
        stop = 1704067199   # Dec 31, 2023 (in seconds)
        group = "month"
        result = clicked_urls_resource.list(start=start, stop=stop, group=group)

        # Verify the result
        assert isinstance(result, ListClickedUrlsMetricsResponse)
        assert result.start == 1672531200000
        assert result.stop == 1704067199000
        assert len(result.stats) == 2
        
        # Check URL stats
        assert result.stats[0].url == "https://example.com/product"
        assert result.stats[0].clicked == 2500
        assert result.stats[0].clicked_unique == 1800
        assert result.stats[1].url == "https://example.com/pricing"
        assert result.stats[1].clicked == 1500
        assert result.stats[1].clicked_unique == 1200

        # Verify the client was called correctly with custom parameters
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/reporting/clicks"
        assert kwargs["params"] == {
            "start": start,
            "stop": stop,
            "group": group
        }
        assert kwargs["headers"] == {"Content-Type": "application/json"}