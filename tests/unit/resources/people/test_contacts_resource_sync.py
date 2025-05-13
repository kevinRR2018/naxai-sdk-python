"""
Unit tests for the synchronous ContactsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.people_resources.contacts import ContactsResource
from naxai.models.people.helper_models.search_condition import SearchCondition
from naxai.models.people.responses.contacts_responses import (
    SearchContactsResponse,
    CountContactsResponse,
    CreateOrUpdateContactResponse,
    GetContactResponse
)
from naxai.models.base.pagination import Pagination


class TestContactsResourceSync:
    """Test suite for the synchronous ContactsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def contacts_resource(self, mock_client):
        """Create a ContactsResource instance with a mock client."""
        return ContactsResource(mock_client, "/people")

    def test_initialization(self, contacts_resource):
        """Test that the ContactsResource initializes correctly."""
        assert contacts_resource.root_path == "/people/contacts"
        assert contacts_resource.headers == {"Content-Type": "application/json"}
        
        # Test that all sub-resources are initialized correctly
        assert hasattr(contacts_resource, "events")
        assert hasattr(contacts_resource, "identifier")
        assert hasattr(contacts_resource, "segments")
        
        assert contacts_resource.events.root_path == "/people/contacts"
        assert contacts_resource.identifier.root_path == "/people/contacts/keyIdentifier"
        assert contacts_resource.segments.root_path == "/people/contacts"

    def test_search_without_condition(self, contacts_resource, mock_client):
        """Test searching contacts without a condition."""
        # Setup mock response
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 50,
                "totalRecord": 100,
                "returnedRecord": 50,
                "remainingRecord": 50
            },
            "items": [
                {
                    "nxId": "cnt_123abc",
                    "email": "john.doe@example.com",
                    "phone": "+1234567890",
                    "smsCapable": True,
                    "externalId": "cust_456",
                    "unsubscribed": False,
                    "language": "en",
                    "createdAt": 1703066400000,
                    "createdAtNaxai": 1703066400000,
                    "first_name": "John",
                    "last_name": "Doe"
                },
                {
                    "nxId": "cnt_456def",
                    "email": "jane.doe@example.com",
                    "externalId": "cust_789",
                    "language": "en",
                    "createdAt": 1703066500000,
                    "createdAtNaxai": 1703066500000,
                    "first_name": "Jane",
                    "last_name": "Doe"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = contacts_resource.search(page=1, page_size=50, sort="createdAt:desc")

        # Verify the result
        assert isinstance(result, SearchContactsResponse)
        assert isinstance(result.pagination, Pagination)
        assert result.pagination.page == 1
        assert result.pagination.page_size == 50
        assert result.pagination.total_record == 100
        assert result.pagination.returned_record == 50
        assert result.pagination.remaining_record == 50
        
        assert len(result.items) == 2
        assert result.items[0].nx_id == "cnt_123abc"
        assert result.items[0].email == "john.doe@example.com"
        assert result.items[0].phone == "+1234567890"
        assert result.items[0].sms_capable is True
        assert result.items[0].external_id == "cust_456"
        assert result.items[0].first_name == "John"
        assert result.items[0].last_name == "Doe"
        
        assert result.items[1].nx_id == "cnt_456def"
        assert result.items[1].email == "jane.doe@example.com"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/people/contacts"
        assert kwargs["params"] == {"page": 1, "pageSize": 50, "sort": "createdAt:desc"}
        assert kwargs["headers"] == {"Content-Type": "application/json"}
        assert "json" not in kwargs

    def test_search_with_condition(self, contacts_resource, mock_client):
        """Test searching contacts with a condition."""
        # Setup mock response
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 50,
                "totalRecord": 2,
                "returnedRecord": 2,
                "remainingRecord": 0
            },
            "items": [
                {
                    "nxId": "cnt_123abc",
                    "email": "john.doe@example.com",
                    "country": "US"
                },
                {
                    "nxId": "cnt_456def",
                    "email": "jane.doe@example.com",
                    "country": "US"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Create search condition
        condition = SearchCondition(
            all=[
                {"attribute": {"field": "country", "operator": "eq", "value": "US"}}
            ]
        )

        # Call the method
        result = contacts_resource.search(condition=condition)

        # Verify the result
        assert isinstance(result, SearchContactsResponse)
        assert len(result.items) == 2
        assert result.items[0].nx_id == "cnt_123abc"
        assert result.items[0].country == "US"
        assert result.items[1].nx_id == "cnt_456def"
        assert result.items[1].country == "US"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/people/contacts"
        assert "json" in kwargs
        assert kwargs["json"] == {"condition": condition}

    def test_count(self, contacts_resource, mock_client):
        """Test counting contacts."""
        # Setup mock response
        mock_response = {"count": 100}
        mock_client._request.return_value = mock_response

        # Call the method
        result = contacts_resource.count()

        # Verify the result
        assert isinstance(result, CountContactsResponse)
        assert result.count == 100

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/contacts/count",
            headers={"Content-Type": "application/json"}
        )

    def test_create_or_update(self, contacts_resource, mock_client):
        """Test creating or updating a contact."""
        # Setup mock response
        mock_response = {
            "nxId": "cnt_123abc",
            "email": "john.doe@example.com",
            "externalId": "cust_456",
            "unsubscribed": False,
            "language": "en",
            "createdAt": 1703066400000,
            "createdAtNaxai": 1703066400000,
            "first_name": "John",
            "last_name": "Doe",
            "company": "Acme Inc."
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = contacts_resource.create_or_update(
            identifier="john.doe@example.com",
            email="john.doe@example.com",
            external_id="cust_456",
            language="en",
            first_name="John",
            last_name="Doe",
            company="Acme Inc."
        )

        # Verify the result
        assert isinstance(result, CreateOrUpdateContactResponse)
        assert result.nx_id == "cnt_123abc"
        assert result.email == "john.doe@example.com"
        assert result.external_id == "cust_456"
        assert result.language == "en"
        assert result.first_name == "John"
        assert result.last_name == "Doe"
        assert result.company == "Acme Inc."

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "PUT"
        assert args[1] == "/people/contacts/john.doe@example.com"
        assert "json" in kwargs
        expected_data = {
            "email": "john.doe@example.com",
            "externalId": "cust_456",
            "unsubscribe": None,
            "language": "en",
            "createdAt": None,
            "first_name": "John",
            "last_name": "Doe",
            "company": "Acme Inc."
        }
        assert kwargs["json"] == expected_data

    def test_get(self, contacts_resource, mock_client):
        """Test getting a contact."""
        # Setup mock response
        mock_response = {
            "nxId": "cnt_123abc",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "smsCapable": True,
            "externalId": "cust_456",
            "unsubscribed": False,
            "language": "en",
            "createdAt": 1703066400000,
            "createdAtNaxai": 1703066400000,
            "first_name": "John",
            "last_name": "Doe"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = contacts_resource.get("john.doe@example.com")

        # Verify the result
        assert isinstance(result, GetContactResponse)
        assert result.nx_id == "cnt_123abc"
        assert result.email == "john.doe@example.com"
        assert result.phone == "+1234567890"
        assert result.sms_capable is True
        assert result.external_id == "cust_456"
        assert result.unsubscribed is False
        assert result.language == "en"
        assert result.created_at == 1703066400000
        assert result.created_at_naxai == 1703066400000
        assert result.first_name == "John"
        assert result.last_name == "Doe"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/contacts/john.doe@example.com",
            headers={"Content-Type": "application/json"}
        )

    def test_delete(self, contacts_resource, mock_client):
        """Test deleting a contact."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        result = contacts_resource.delete("john.doe@example.com")

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/people/contacts/john.doe@example.com",
            headers={"Content-Type": "application/json"}
        )