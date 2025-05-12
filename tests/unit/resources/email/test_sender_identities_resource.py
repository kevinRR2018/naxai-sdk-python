"""
Unit tests for the synchronous SenderIdentitiesResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.email_resources.sender_identities import SenderIdentitiesResource
from naxai.models.email.responses.senders_responses import (
    ListSendersResponse,
    GetSenderResponse,
    CreateSenderResponse,
    UpdateSenderResponse
)


class TestSenderIdentitiesResource:
    """Test suite for the synchronous SenderIdentitiesResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def sender_identities_resource(self, mock_client):
        """Create a SenderIdentitiesResource instance with a mock client."""
        return SenderIdentitiesResource(mock_client, "/email")

    def test_initialization(self, sender_identities_resource):
        """Test that the SenderIdentitiesResource initializes correctly."""
        assert sender_identities_resource.root_path == "/email/senders"
        assert sender_identities_resource.headers == {"Content-Type": "application/json"}

    def test_list_senders(self, sender_identities_resource, mock_client):
        """Test listing sender identities."""
        # Setup mock response with proper structure
        mock_response = [
            {
                "id": "snd_123abc",
                "email": "sender1@example.com",
                "name": "Sender One",
                "verified": True,
                "domainId": "dom_456def",
                "domainName": "example.com"
            },
            {
                "id": "snd_789ghi",
                "email": "sender2@example.com",
                "name": "Sender Two",
                "verified": False,
                "domainId": "dom_456def",
                "domainName": "example.com"
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = sender_identities_resource.list()

        # Verify the result
        assert isinstance(result, ListSendersResponse)
        assert len(result) == 2
        assert result[0].id == "snd_123abc"
        assert result[0].email == "sender1@example.com"
        assert result[0].name == "Sender One"
        assert result[0].verified is True
        assert result[0].domain_id == "dom_456def"
        assert result[0].domain_name == "example.com"
        assert result[1].id == "snd_789ghi"
        assert result[1].verified is False

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/senders",
            params={},
            headers={"Content-Type": "application/json"}
        )

    def test_list_senders_with_filters(self, sender_identities_resource, mock_client):
        """Test listing sender identities with filters."""
        # Setup mock response
        mock_response = [
            {
                "id": "snd_123abc",
                "email": "sender1@example.com",
                "name": "Sender One",
                "verified": True,
                "domainId": "dom_456def",
                "domainName": "example.com"
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method with filters
        result = sender_identities_resource.list(
            domain_id="dom_456def",
            verified=True,
            shared=True
        )

        # Verify the result
        assert isinstance(result, ListSendersResponse)
        assert len(result) == 1
        assert result[0].id == "snd_123abc"

        # Verify the client was called correctly with filters
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/senders"
        assert kwargs["params"] == {
            "domainId": "dom_456def",
            "verified": True,
            "shared": True
        }

    def test_get_sender(self, sender_identities_resource, mock_client):
        """Test getting a specific sender identity."""
        # Setup mock response with proper structure
        mock_response = {
            "id": "snd_123abc",
            "email": "sender1@example.com",
            "name": "Sender One",
            "verified": True,
            "domainId": "dom_456def",
            "domainName": "example.com",
            "modifiedAt": 1703066400000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        sender_id = "snd_123abc"
        result = sender_identities_resource.get(sender_id)

        # Verify the result
        assert isinstance(result, GetSenderResponse)
        assert result.id == "snd_123abc"
        assert result.email == "sender1@example.com"
        assert result.name == "Sender One"
        assert result.verified is True
        assert result.domain_id == "dom_456def"
        assert result.domain_name == "example.com"
        assert result.modified_at == 1703066400000
        assert result.modified_by == "usr_789xyz"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/senders/snd_123abc",
            headers={"Content-Type": "application/json"}
        )

    def test_create_sender(self, sender_identities_resource, mock_client):
        """Test creating a sender identity."""
        # Setup mock response with proper structure
        mock_response = {
            "id": "snd_123abc",
            "email": "new-sender@example.com",
            "name": "New Sender",
            "verified": False,
            "domainId": "dom_456def",
            "domainName": "example.com",
            "modifiedAt": 1703066400000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        domain_id = "dom_456def"
        email = "new-sender@example.com"
        name = "New Sender"
        result = sender_identities_resource.create(domain_id, email, name)

        # Verify the result
        assert isinstance(result, CreateSenderResponse)
        assert result.id == "snd_123abc"
        assert result.email == "new-sender@example.com"
        assert result.name == "New Sender"
        assert result.verified is False
        assert result.domain_id == "dom_456def"
        assert result.domain_name == "example.com"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/email/senders"
        assert kwargs["json"] == {
            "domainId": "dom_456def",
            "email": "new-sender@example.com",
            "name": "New Sender"
        }
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_update_sender(self, sender_identities_resource, mock_client):
        """Test updating a sender identity."""
        # Setup mock response with proper structure
        mock_response = {
            "id": "snd_123abc",
            "email": "updated-sender@example.com",
            "name": "Updated Sender",
            "verified": True,
            "domainId": "dom_456def",
            "domainName": "example.com",
            "modifiedAt": 1703152800000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        sender_id = "snd_123abc"
        name = "Updated Sender"
        email = "updated-sender@example.com"
        result = sender_identities_resource.update(sender_id, name, email)

        # Verify the result
        assert isinstance(result, UpdateSenderResponse)
        assert result.id == "snd_123abc"
        assert result.email == "updated-sender@example.com"
        assert result.name == "Updated Sender"
        assert result.verified is True
        assert result.domain_id == "dom_456def"
        assert result.domain_name == "example.com"
        assert result.modified_at == 1703152800000
        assert result.modified_by == "usr_789xyz"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "PUT"
        assert args[1] == "/email/senders/snd_123abc"
        assert kwargs["json"] == {
            "name": "Updated Sender",
            "email": "updated-sender@example.com"
        }
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_delete_sender(self, sender_identities_resource, mock_client):
        """Test deleting a sender identity."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        sender_id = "snd_123abc"
        result = sender_identities_resource.delete(sender_id)

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/email/senders/snd_123abc",
            headers={"Content-Type": "application/json"}
        )