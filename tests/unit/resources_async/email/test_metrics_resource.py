"""
Unit tests for the asynchronous MetricsResource class.
"""
import json
import datetime
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.email_resources.reporting_resources.metrics import MetricsResource
from naxai.models.email.responses.metrics_responses import ListMetricsResponse, BaseStats


class TestMetricsResource:
    """Test suite for the asynchronous MetricsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def metrics_resource(self, mock_client):
        """Create a MetricsResource instance with a mock client."""
        return MetricsResource(mock_client, "/email/reporting")

    def test_initialization(self, metrics_resource):
        """Test that the MetricsResource initializes correctly."""
        assert metrics_resource.root_path == "/email/reporting/metrics"
        assert metrics_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_metrics_default_params(self, metrics_resource, mock_client):
        """Test listing email metrics with default parameters."""
        # Setup mock response
        mock_response = {
            "start": 1672531200000,  # Jan 1, 2023
            "stop": 1704067199000,   # Dec 31, 2023
            "group": "day",
            "stats": [
                {
                    "date": 1672531200000,
                    "sent": 1000,
                    "delivered": 950,
                    "opened": 500,
                    "openedUnique": 400,
                    "cliqued": 250,
                    "cliquedUnique": 200,
                    "bounced": 30,
                    "rejected": 20
                },
                {
                    "date": 1672617600000,
                    "sent": 1200,
                    "delivered": 1150,
                    "opened": 600,
                    "openedUnique": 500,
                    "cliqued": 300,
                    "cliquedUnique": 250,
                    "bounced": 35,
                    "rejected": 15
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method with default parameters
        result = await metrics_resource.list()

        # Verify the result
        assert isinstance(result, ListMetricsResponse)
        assert result.start == 1672531200000
        assert result.stop == 1704067199000
        assert result.group == "day"
        assert len(result.stats) == 2
        
        # Check first stats entry
        assert isinstance(result.stats[0], BaseStats)
        assert result.stats[0].date == 1672531200000
        assert result.stats[0].sent == 1000
        assert result.stats[0].delivered == 950
        assert result.stats[0].opened == 500
        assert result.stats[0].opened_unique == 400
        assert result.stats[0].cliqued == 250
        assert result.stats[0].cliqued_unique == 200
        assert result.stats[0].bounced == 30
        assert result.stats[0].rejected == 20
        
        # Check second stats entry
        assert result.stats[1].date == 1672617600000
        assert result.stats[1].sent == 1200
        assert result.stats[1].delivered == 1150

        # Verify the client was called correctly with default parameters
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/reporting/metrics"
        assert "params" in kwargs
        assert "start" in kwargs["params"]
        assert "stop" in kwargs["params"]
        assert kwargs["params"]["group"] == "day"
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_metrics_custom_params(self, metrics_resource, mock_client):
        """Test listing email metrics with custom parameters."""
        # Setup mock response
        mock_response = {
            "start": 1672531200000,  # Jan 1, 2023
            "stop": 1704067199000,   # Dec 31, 2023
            "group": "month",
            "stats": [
                {
                    "date": 1672531200000,  # January 2023
                    "sent": 30000,
                    "delivered": 29000,
                    "opened": 15000,
                    "openedUnique": 12000,
                    "cliqued": 7500,
                    "cliquedUnique": 6000
                },
                {
                    "date": 1675209600000,  # February 2023
                    "sent": 28000,
                    "delivered": 27000,
                    "opened": 14000,
                    "openedUnique": 11000,
                    "cliqued": 7000,
                    "cliquedUnique": 5500
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method with custom parameters
        start = 1672531200  # Jan 1, 2023 (in seconds)
        stop = 1704067199   # Dec 31, 2023 (in seconds)
        group = "month"
        result = await metrics_resource.list(start=start, stop=stop, group=group)

        # Verify the result
        assert isinstance(result, ListMetricsResponse)
        assert result.start == 1672531200000
        assert result.stop == 1704067199000
        assert result.group == "month"
        assert len(result.stats) == 2
        
        # Check first stats entry (January)
        assert result.stats[0].date == 1672531200000
        assert result.stats[0].sent == 30000
        assert result.stats[0].delivered == 29000
        assert result.stats[0].opened_unique == 12000
        assert result.stats[0].cliqued_unique == 6000
        
        # Check second stats entry (February)
        assert result.stats[1].date == 1675209600000
        assert result.stats[1].sent == 28000

        # Verify the client was called correctly with custom parameters
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/reporting/metrics"
        assert kwargs["params"] == {
            "start": start,
            "stop": stop,
            "group": group
        }
        assert kwargs["headers"] == {"Content-Type": "application/json"}