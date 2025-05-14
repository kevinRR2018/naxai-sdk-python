"""
Unit tests for the asynchronous HolidaysTemplatesResource class.
"""
import pytest
from unittest.mock import MagicMock, AsyncMock
from naxai.resources_async.calendars_resources.holidays_templates import HolidaysTemplatesResource
from naxai.models.calendars.responses.holidays_template_responses import ListHolidaysTemplatesResponse, GetHolidaysTemplateResponse, HolidaysTemplate


class TestHolidaysTemplatesResource:
    """Test suite for the asynchronous HolidaysTemplatesResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def holidays_templates_resource(self, mock_client):
        """Create a HolidaysTemplatesResource instance with a mock client."""
        return HolidaysTemplatesResource(mock_client, "/calendars")

    def test_initialization(self, holidays_templates_resource):
        """Test that the HolidaysTemplatesResource initializes correctly."""
        assert holidays_templates_resource.root_path == "/calendars/holidays"
        assert holidays_templates_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_holiday_templates(self, holidays_templates_resource, mock_client):
        """Test listing holiday templates."""
        # Setup mock response
        mock_response = [
            {
                "id": "ht_123",
                "name": "US Federal Holidays 2024",
                "dates": [
                    "2024-01-01",
                    "2024-01-15",
                    "2024-02-19"
                ]
            },
            {
                "id": "ht_456",
                "name": "UK Bank Holidays 2024",
                "dates": [
                    "2024-01-01",
                    "2024-03-29",
                    "2024-04-01"
                ]
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = await holidays_templates_resource.list()

        # Verify the result
        assert isinstance(result, ListHolidaysTemplatesResponse)
        assert len(result) == 2
        assert all(isinstance(template, HolidaysTemplate) for template in result)
        assert result[0].id == "ht_123"
        assert result[0].name == "US Federal Holidays 2024"
        assert len(result[0].dates) == 3
        assert result[1].id == "ht_456"
        assert result[1].name == "UK Bank Holidays 2024"
        assert len(result[1].dates) == 3

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/calendars/holidays",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_get_holiday_template(self, holidays_templates_resource, mock_client):
        """Test getting a specific holiday template."""
        # Setup mock response
        mock_response = {
            "id": "ht_123",
            "name": "US Federal Holidays 2024",
            "dates": [
                "2024-01-01",
                "2024-01-15",
                "2024-02-19",
                "2024-05-27",
                "2024-06-19",
                "2024-07-04",
                "2024-09-02",
                "2024-10-14",
                "2024-11-11",
                "2024-11-28",
                "2024-12-25"
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        template_id = "ht_123"
        result = await holidays_templates_resource.get(template_id)

        # Verify the result
        assert isinstance(result, GetHolidaysTemplateResponse)
        assert result.id == "ht_123"
        assert result.name == "US Federal Holidays 2024"
        assert len(result.dates) == 11
        assert "2024-01-01" in result.dates
        assert "2024-12-25" in result.dates

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/calendars/holidays/ht_123",
            headers={"Content-Type": "application/json"}
        )