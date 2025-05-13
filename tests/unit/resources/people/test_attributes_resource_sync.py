"""
Unit tests for the synchronous AttributesResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.people_resources.attributes import AttributesResource
from naxai.models.people.responses.attributes_responses import (
    ListAttributesResponse,
    GetAttributeResponse,
    CreateAttributeResponse,
    BaseListObject
)


class TestAttributesResourceSync:
    """Test suite for the synchronous AttributesResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def attributes_resource(self, mock_client):
        """Create an AttributesResource instance with a mock client."""
        return AttributesResource(mock_client, "/people")

    def test_initialization(self, attributes_resource):
        """Test that the AttributesResource initializes correctly."""
        assert attributes_resource.root_path == "/people/attributes"
        assert attributes_resource.headers == {"Content-Type": "application/json"}

    def test_list_attributes(self, attributes_resource, mock_client):
        """Test listing attributes."""
        # Setup mock response
        mock_response = [
            {"name": "first_name"},
            {"name": "last_name"},
            {"name": "email"},
            {"name": "custom_field"}
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = attributes_resource.list()

        # Verify the result
        assert isinstance(result, ListAttributesResponse)
        assert len(result) == 4
        assert result[0].name == "first_name"
        assert result[1].name == "last_name"
        assert result[2].name == "email"
        assert result[3].name == "custom_field"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/attributes",
            headers={"Content-Type": "application/json"}
        )

    def test_get_attribute(self, attributes_resource, mock_client):
        """Test getting a specific attribute."""
        # Setup mock response
        mock_response = {
            "name": "custom_field",
            "segmentIds": ["seg_123abc", "seg_456def"]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        attribute_name = "custom_field"
        result = attributes_resource.get(attribute_name)

        # Verify the result
        assert isinstance(result, GetAttributeResponse)
        assert result.name == "custom_field"
        assert result.segment_ids == ["seg_123abc", "seg_456def"]

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/attributes/custom_field",
            headers={"Content-Type": "application/json"}
        )

    def test_create_attribute(self, attributes_resource, mock_client):
        """Test creating an attribute."""
        # Setup mock response
        mock_response = {
            "name": "new_custom_field",
            "segmentIds": []
        }
        mock_client._request.return_value = mock_response

        # Call the method
        attribute_name = "new_custom_field"
        result = attributes_resource.create(attribute_name)

        # Verify the result
        assert isinstance(result, CreateAttributeResponse)
        assert result.name == "new_custom_field"
        assert result.segment_ids == []

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "POST",
            "/people/attributes",
            json={"name": "new_custom_field"},
            headers={"Content-Type": "application/json"}
        )

    def test_delete_attribute(self, attributes_resource, mock_client):
        """Test deleting an attribute."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        attribute_name = "custom_field"
        result = attributes_resource.delete(attribute_name)

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/people/attributes/custom_field",
            headers={"Content-Type": "application/json"}
        )