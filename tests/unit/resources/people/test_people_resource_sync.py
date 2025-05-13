"""
Unit tests for the synchronous PeopleResource class.
"""
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.people import PeopleResource
from naxai.resources.people_resources.attributes import AttributesResource
from naxai.resources.people_resources.contacts import ContactsResource
from naxai.resources.people_resources.exports import ExportsResource
from naxai.resources.people_resources.imports import ImportsResource
from naxai.resources.people_resources.segments import SegmentsResource


class TestPeopleResourceSync:
    """Test suite for the synchronous PeopleResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def people_resource(self, mock_client):
        """Create a PeopleResource instance with a mock client."""
        return PeopleResource(mock_client)

    def test_initialization(self, people_resource, mock_client):
        """Test that the PeopleResource initializes correctly."""
        assert people_resource.root_path == "/people"
        
        # Test that all sub-resources are initialized correctly
        assert isinstance(people_resource.attributes, AttributesResource)
        assert isinstance(people_resource.contacts, ContactsResource)
        assert isinstance(people_resource.exports, ExportsResource)
        assert isinstance(people_resource.imports, ImportsResource)
        assert isinstance(people_resource.segments, SegmentsResource)
        
        # Test that all sub-resources have the correct root path
        assert people_resource.attributes.root_path == "/people/attributes"
        assert people_resource.contacts.root_path == "/people/contacts"
        assert people_resource.exports.root_path == "/people/exports"
        assert people_resource.imports.root_path == "/people/imports"
        assert people_resource.segments.root_path == "/people/segments"
        
        # Test that all sub-resources have the correct client
        assert people_resource.attributes._client == mock_client
        assert people_resource.contacts._client == mock_client
        assert people_resource.exports._client == mock_client
        assert people_resource.imports._client == mock_client
        assert people_resource.segments._client == mock_client