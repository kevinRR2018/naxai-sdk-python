"""
Unit tests for the asynchronous SegmentsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.people_resources.segments import SegmentsResource
from naxai.models.people.helper_models.segments_condition import Condition, AttributeObject, AttributeCondSimple
from naxai.models.people.requests.segments_requests import CreateSegmentRequest
from naxai.models.people.responses.segments_responses import (
    ListSegmentsResponse,
    GetSegmentResponse,
    CreateSegmentResponse,
    UpdateSegmentResponse,
    GetSegmentsHistoryResponse,
    GetSegmentUsageResponse,
    SegmentHistoryDay
)


class TestSegmentsResourceAsync:
    """Test suite for the asynchronous SegmentsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def segments_resource(self, mock_client):
        """Create a SegmentsResource instance with a mock client."""
        return SegmentsResource(mock_client, "/people")

    def test_initialization(self, segments_resource):
        """Test that the SegmentsResource initializes correctly."""
        assert segments_resource.root_path == "/people/segments"
        assert segments_resource.headers == {"Content-Type": "application/json"}
        assert hasattr(segments_resource, "contacts")
        assert segments_resource.contacts.root_path == "/people/segments"

    @pytest.mark.asyncio
    async def test_list_segments(self, segments_resource, mock_client):
        """Test listing segments."""
        # Setup mock response
        mock_response = [
            {
                "id": "seg_123abc",
                "name": "US Customers",
                "description": "All customers from the United States",
                "state": "ready",
                "predefined": False,
                "type": "dynamic",
                "modifiedAt": 1703066400000,
                "modifiedBy": "usr_789xyz"
            },
            {
                "id": "seg_456def",
                "name": "High Value Customers",
                "description": "Customers with high lifetime value",
                "state": "ready",
                "predefined": False,
                "type": "dynamic",
                "modifiedAt": 1703066500000,
                "modifiedBy": "usr_789xyz"
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = await segments_resource.list(type_="dynamic", exclude_predefined=True)

        # Verify the result
        assert isinstance(result, ListSegmentsResponse)
        assert len(result) == 2
        assert result[0].id == "seg_123abc"
        assert result[0].name == "US Customers"
        assert result[0].description == "All customers from the United States"
        assert result[0].state == "ready"
        assert result[0].predefined is False
        assert result[0].type_ == "dynamic"
        assert result[0].modified_at == 1703066400000
        assert result[0].modified_by == "usr_789xyz"
        assert result[1].id == "seg_456def"
        assert result[1].name == "High Value Customers"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/segments",
            headers={"Content-Type": "application/json"},
            params={"exclude-predefined": True, "type": "dynamic"}
        )

    @pytest.mark.asyncio
    async def test_get_segment(self, segments_resource, mock_client):
        """Test getting a specific segment."""
        # Setup mock response
        mock_response = {
            "id": "seg_123abc",
            "name": "US Customers",
            "description": "All customers from the United States",
            "state": "ready",
            "predefined": False,
            "type": "dynamic",
            "condition": {
                "all": [
                    {
                        "attribute": {
                            "field": "country",
                            "operator": "eq",
                            "value": "US"
                        }
                    }
                ]
            },
            "modifiedAt": 1703066400000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        segment_id = "seg_123abc"
        result = await segments_resource.get(segment_id)

        # Verify the result
        assert isinstance(result, GetSegmentResponse)
        assert result.id == "seg_123abc"
        assert result.name == "US Customers"
        assert result.description == "All customers from the United States"
        assert result.state == "ready"
        assert result.predefined is False
        assert result.type_ == "dynamic"
        assert result.modified_at == 1703066400000
        assert result.modified_by == "usr_789xyz"
        assert result.condition is not None
        assert result.condition.all is not None
        assert len(result.condition.all) == 1
        assert result.condition.all[0].attribute.field == "country"
        assert result.condition.all[0].attribute.operator == "eq"
        assert result.condition.all[0].attribute.value == "US"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/segments/seg_123abc",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_create_segment(self, segments_resource, mock_client):
        """Test creating a segment."""
        # Setup mock response
        mock_response = {
            "id": "seg_123abc",
            "name": "New Segment",
            "description": "A new test segment",
            "state": "building",
            "predefined": False,
            "type": "dynamic",
            "condition": {
                "all": [
                    {
                        "attribute": {
                            "field": "country",
                            "operator": "eq",
                            "value": "US"
                        }
                    }
                ]
            },
            "modifiedAt": 1703066400000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Create request data
        condition = Condition(
            all=[
                AttributeCondSimple(
                    attribute=AttributeObject(
                        field="country",
                        operator="eq",
                        value="US"
                    )
                )
            ]
        )
        
        request_data = CreateSegmentRequest(
            name="New Segment",
            description="A new test segment",
            type_="dynamic",
            condition=condition
        )

        # Call the method
        result = await segments_resource.create(request_data)

        # Verify the result
        assert isinstance(result, CreateSegmentResponse)
        assert result.id == "seg_123abc"
        assert result.name == "New Segment"
        assert result.description == "A new test segment"
        assert result.state == "building"
        assert result.predefined is False
        assert result.type_ == "dynamic"
        assert result.modified_at == 1703066400000
        assert result.modified_by == "usr_789xyz"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/people/segments"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_update_segment(self, segments_resource, mock_client):
        """Test updating a segment."""
        # Setup mock response
        mock_response = {
            "id": "seg_123abc",
            "name": "Updated Segment",
            "description": "An updated test segment",
            "state": "building",
            "predefined": False,
            "type": "dynamic",
            "condition": {
                "all": [
                    {
                        "attribute": {
                            "field": "country",
                            "operator": "eq",
                            "value": "US"
                        }
                    }
                ]
            },
            "modifiedAt": 1703066500000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Create request data
        condition = Condition(
            all=[
                AttributeCondSimple(
                    attribute=AttributeObject(
                        field="country",
                        operator="eq",
                        value="US"
                    )
                )
            ]
        )
        
        request_data = CreateSegmentRequest(
            name="Updated Segment",
            description="An updated test segment",
            type_="dynamic",
            condition=condition
        )

        # Call the method
        segment_id = "seg_123abc"
        result = await segments_resource.update(segment_id, request_data)

        # Verify the result
        assert isinstance(result, UpdateSegmentResponse)
        assert result.id == "seg_123abc"
        assert result.name == "Updated Segment"
        assert result.description == "An updated test segment"
        assert result.state == "building"
        assert result.predefined is False
        assert result.type_ == "dynamic"
        assert result.modified_at == 1703066500000
        assert result.modified_by == "usr_789xyz"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "PUT"
        assert args[1] == "/people/segments/seg_123abc"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_delete_segment(self, segments_resource, mock_client):
        """Test deleting a segment."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        segment_id = "seg_123abc"
        result = await segments_resource.delete(segment_id)

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/people/segments/seg_123abc",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_history(self, segments_resource, mock_client):
        """Test getting segment history."""
        # Setup mock response
        mock_response = {
            "history": [
                {
                    "date": 1703066400000,
                    "added": 25,
                    "removed": 10,
                    "change": 15,
                    "current": 1250
                },
                {
                    "date": 1703152800000,
                    "added": 18,
                    "removed": 5,
                    "change": 13,
                    "current": 1263
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        segment_id = "seg_123abc"
        start = 1703066400000
        stop = 1703152800000
        result = await segments_resource.history(segment_id, start, stop)

        # Verify the result
        assert isinstance(result, GetSegmentsHistoryResponse)
        assert len(result.history) == 2
        assert isinstance(result.history[0], SegmentHistoryDay)
        assert result.history[0].date == 1703066400000
        assert result.history[0].added == 25
        assert result.history[0].removed == 10
        assert result.history[0].change == 15
        assert result.history[0].current == 1250
        assert result.history[1].date == 1703152800000
        assert result.history[1].current == 1263

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/segments/seg_123abc/history",
            headers={"Content-Type": "application/json"},
            params={"start": start, "stop": stop}
        )

    @pytest.mark.asyncio
    async def test_usage(self, segments_resource, mock_client):
        """Test getting segment usage."""
        # Setup mock response
        mock_response = {
            "campaignIds": ["cmp_123", "cmp_456"],
            "broadcastIds": ["brd_789"]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        segment_id = "seg_123abc"
        result = await segments_resource.usage(segment_id)

        # Verify the result
        assert isinstance(result, GetSegmentUsageResponse)
        assert result.campaign_ids == ["cmp_123", "cmp_456"]
        assert result.broadcast_ids == ["brd_789"]


        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/segments/seg_123abc/usage",
            headers={"Content-Type": "application/json"}
        )