"""
Unit tests for the asynchronous EmailResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.email import EmailResource
from naxai.models.email.requests.transactional_requests import (
    SendTransactionalEmailRequest,
    SenderObject,
    DestinationObject,
    CCObject,
    BCCObject,
    Attachment
)
from naxai.models.email.responses.transactional_responses import SendTransactionalEmailResponse


class TestEmailResource:
    """Test suite for the asynchronous EmailResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def email_resource(self, mock_client):
        """Create an EmailResource instance with a mock client."""
        return EmailResource(mock_client)

    def test_initialization(self, email_resource):
        """Test that the EmailResource initializes correctly with all sub-resources."""
        assert email_resource.root_path == "/email"
        assert email_resource.headers == {"Content-Type": "application/json"}
        
        # Verify all sub-resources are initialized
        assert email_resource.transactional is not None
        assert email_resource.activity_logs is not None
        assert email_resource.reporting is not None

    @pytest.mark.asyncio
    async def test_send_email_basic(self, email_resource, mock_client):
        """Test sending a basic email."""
        # Setup mock response
        mock_response = {"id": "email_123abc"}
        mock_client._request.return_value = mock_response

        # Mock the transactional.send method
        email_resource.transactional.send = AsyncMock()
        email_resource.transactional.send.return_value = SendTransactionalEmailResponse(**mock_response)

        # Call the method
        result = await email_resource.send(
            sender_email="sender@example.com",
            sender_name="Sender Name",
            subject="Test Subject",
            to=[DestinationObject(email="recipient@example.com", name="Recipient Name")],
            html="<html><body><p>Test email content</p></body></html>"
        )

        # Verify the result
        assert isinstance(result, SendTransactionalEmailResponse)
        assert result.id == "email_123abc"

        # Verify the transactional.send method was called with the correct data
        email_resource.transactional.send.assert_called_once()
        call_args = email_resource.transactional.send.call_args[1]
        assert "data" in call_args
        
        data = call_args["data"]
        assert isinstance(data, SendTransactionalEmailRequest)
        assert data.sender.email == "sender@example.com"
        assert data.sender.name == "Sender Name"
        assert data.subject == "Test Subject"
        assert len(data.to) == 1
        assert data.to[0].email == "recipient@example.com"
        assert data.to[0].name == "Recipient Name"
        assert data.html == "<html><body><p>Test email content</p></body></html>"
        assert data.text is None
        assert data.cc is None
        assert data.bcc is None
        assert data.reply_to is None
        assert data.attachments is None
        assert data.enable_tracking is None

    @pytest.mark.asyncio
    async def test_send_email_with_all_options(self, email_resource, mock_client):
        """Test sending an email with all optional parameters."""
        # Setup mock response
        mock_response = {"id": "email_456def"}
        mock_client._request.return_value = mock_response

        # Mock the transactional.send method
        email_resource.transactional.send = AsyncMock()
        email_resource.transactional.send.return_value = SendTransactionalEmailResponse(**mock_response)

        # Create test data
        to_recipients = [
            DestinationObject(email="recipient1@example.com", name="Recipient One"),
            DestinationObject(email="recipient2@example.com", name="Recipient Two")
        ]
        cc_recipients = [CCObject(email="cc@example.com", name="CC Recipient")]
        bcc_recipients = [BCCObject(email="bcc@example.com", name="BCC Recipient")]
        attachments = [
            Attachment(
                id="att_123",
                name="test.pdf",
                content_type="application/pdf",
                data="base64encodedcontent"
            )
        ]

        # Call the method
        result = await email_resource.send(
            sender_email="sender@example.com",
            sender_name="Sender Name",
            subject="Test Subject with Options",
            to=to_recipients,
            cc=cc_recipients,
            bcc=bcc_recipients,
            reply_to="reply@example.com",
            text="Plain text version",
            html="<html><body><p>HTML version</p></body></html>",
            attachments=attachments,
            enable_tracking=True
        )

        # Verify the result
        assert isinstance(result, SendTransactionalEmailResponse)
        assert result.id == "email_456def"

        # Verify the transactional.send method was called with the correct data
        email_resource.transactional.send.assert_called_once()
        call_args = email_resource.transactional.send.call_args[1]
        assert "data" in call_args
        
        data = call_args["data"]
        assert isinstance(data, SendTransactionalEmailRequest)
        assert data.sender.email == "sender@example.com"
        assert data.sender.name == "Sender Name"
        assert data.subject == "Test Subject with Options"
        
        # Check recipients
        assert len(data.to) == 2
        assert data.to[0].email == "recipient1@example.com"
        assert data.to[1].email == "recipient2@example.com"
        
        assert len(data.cc) == 1
        assert data.cc[0].email == "cc@example.com"
        
        assert len(data.bcc) == 1
        assert data.bcc[0].email == "bcc@example.com"
        
        # Check other fields
        assert data.reply_to == "reply@example.com"
        assert data.text == "Plain text version"
        assert data.html == "<html><body><p>HTML version</p></body></html>"
        assert data.enable_tracking is True
        
        # Check attachments
        assert len(data.attachments) == 1
        assert data.attachments[0].id == "att_123"
        assert data.attachments[0].name == "test.pdf"
        assert data.attachments[0].content_type == "application/pdf"
        assert data.attachments[0].data == "base64encodedcontent"