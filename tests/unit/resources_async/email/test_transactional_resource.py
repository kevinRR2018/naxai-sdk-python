"""
Unit tests for the asynchronous TransactionalResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.email_resources.transactional import TransactionalResource
from naxai.models.email.requests.transactional_requests import (
    SendTransactionalEmailRequest,
    SenderObject,
    DestinationObject,
    CCObject,
    BCCObject,
    Attachment
)
from naxai.models.email.responses.transactional_responses import SendTransactionalEmailResponse


class TestTransactionalResource:
    """Test suite for the asynchronous TransactionalResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def transactional_resource(self, mock_client):
        """Create a TransactionalResource instance with a mock client."""
        return TransactionalResource(mock_client, "/email")

    def test_initialization(self, transactional_resource):
        """Test that the TransactionalResource initializes correctly."""
        assert transactional_resource.root_path == "/email"
        assert transactional_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_send_email(self, transactional_resource, mock_client):
        """Test sending an email through the transactional resource."""
        # Setup mock response
        mock_response = {"id": "email_123abc"}
        mock_client._request.return_value = mock_response

        # Create request data
        sender = SenderObject(email="sender@example.com", name="Sender Name")
        to = [DestinationObject(email="recipient@example.com", name="Recipient Name")]
        cc = [CCObject(email="cc@example.com", name="CC Recipient")]
        bcc = [BCCObject(email="bcc@example.com", name="BCC Recipient")]

        request_data = SendTransactionalEmailRequest(
            sender=sender,
            to=to,
            cc=cc,
            bcc=bcc,
            reply_to="reply@example.com",
            subject="Test Email",
            text="Plain text content",
            html="<html><body><p>HTML content</p></body></html>",
            enable_tracking=True
        )

        # Call the method
        result = await transactional_resource.send(request_data)

        # Verify the result
        assert isinstance(result, SendTransactionalEmailResponse)
        assert result.id == "email_123abc"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/email/send"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}
        
        # Verify the request data was properly serialized
        request_json = kwargs["json"]
        assert request_json["sender"]["email"] == "sender@example.com"
        assert request_json["sender"]["name"] == "Sender Name"
        assert len(request_json["to"]) == 1
        assert request_json["to"][0]["email"] == "recipient@example.com"
        assert len(request_json["cc"]) == 1
        assert request_json["cc"][0]["email"] == "cc@example.com"
        assert len(request_json["bcc"]) == 1
        assert request_json["bcc"][0]["email"] == "bcc@example.com"
        assert request_json["replyTo"] == "reply@example.com"
        assert request_json["subject"] == "Test Email"
        assert request_json["text"] == "Plain text content"
        assert request_json["html"] == "<html><body><p>HTML content</p></body></html>"
        assert request_json["enableTracking"] is True

    @pytest.mark.asyncio
    async def test_send_email_with_attachments(self, transactional_resource, mock_client):
        """Test sending an email with attachments."""
        # Setup mock response
        mock_response = {"id": "email_456def"}
        mock_client._request.return_value = mock_response

        # Create request data with attachments
        sender = SenderObject(email="sender@example.com", name="Sender Name")
        to = [DestinationObject(email="recipient@example.com", name="Recipient Name")]
        
        attachments = [
            Attachment(
                id="att_123",
                name="document.pdf",
                content_type="application/pdf",
                data="base64encodedcontent"
            ),
            Attachment(
                id="att_456",
                name="image.jpg",
                content_type="image/jpeg",
                data="base64encodedimage"
            )
        ]
        
        request_data = SendTransactionalEmailRequest(
            sender=sender,
            to=to,
            subject="Email with Attachments",
            html="<html><body><p>Please see the attached files</p></body></html>",
            attachments=attachments
        )

        # Call the method
        result = await transactional_resource.send(request_data)

        # Verify the result
        assert isinstance(result, SendTransactionalEmailResponse)
        assert result.id == "email_456def"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/email/send"
        
        # Verify the attachments were properly serialized
        request_json = kwargs["json"]
        assert len(request_json["attachments"]) == 2
        assert request_json["attachments"][0]["id"] == "att_123"
        assert request_json["attachments"][0]["name"] == "document.pdf"
        assert request_json["attachments"][0]["contentType"] == "application/pdf"
        assert request_json["attachments"][0]["data"] == "base64encodedcontent"
        assert request_json["attachments"][1]["id"] == "att_456"
        assert request_json["attachments"][1]["name"] == "image.jpg"