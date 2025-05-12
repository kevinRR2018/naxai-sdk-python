"""
Unit tests for the asynchronous NewslettersResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.email_resources.newsletters import NewslettersResource
from naxai.models.email.requests.newsletters_request import CreateEmailNewsletterRequest
from naxai.models.email.responses.newsletters_responses import (
    CreateNewsletterResponse,
    GetNewsletterResponse,
    UpdateNewsletterResponse,
    ListNewsLettersResponse
)
from naxai.models.base.pagination import Pagination


class TestNewslettersResource:
    """Test suite for the asynchronous NewslettersResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def newsletters_resource(self, mock_client):
        """Create a NewslettersResource instance with a mock client."""
        return NewslettersResource(mock_client, "/email")

    def test_initialization(self, newsletters_resource):
        """Test that the NewslettersResource initializes correctly."""
        assert newsletters_resource.root_path == "/email/newsletters"
        assert newsletters_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_newsletters(self, newsletters_resource, mock_client):
        """Test listing newsletters."""
        # Setup mock response with proper aliases
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 25,
                "totalRecord": 87,
                "returnedRecord": 25,
                "remainingRecord": 62
            },
            "items": [
                {
                    "newsletterId": "nws_123abc",
                    "name": "January Newsletter",
                    "state": "sent",
                    "sentAt": 1703066400000,
                    "subject": "January Updates",
                    "segmentId": "seg_456def"
                },
                {
                    "newsletterId": "nws_456def",
                    "name": "February Newsletter",
                    "state": "scheduled",
                    "scheduledAt": 1706744800000,
                    "subject": "February Updates",
                    "segmentId": "seg_456def"
                },
                {
                    "newsletterId": "nws_789ghi",
                    "name": "March Newsletter",
                    "state": "draft",
                    "subject": "March Updates",
                    "segmentId": "seg_456def"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await newsletters_resource.list(page=1, page_size=25)

        # Verify the result
        assert isinstance(result, ListNewsLettersResponse)
        assert result.pagination.page == 1
        assert result.pagination.page_size == 25
        assert result.pagination.total_record == 87
        assert result.pagination.returned_record == 25
        assert result.pagination.remaining_record == 62
        assert len(result.items) == 3
        assert result.items[0].newsletter_id == "nws_123abc"
        assert result.items[0].name == "January Newsletter"
        assert result.items[0].state == "sent"
        assert result.items[0].sent_at == 1703066400000
        assert result.items[1].newsletter_id == "nws_456def"
        assert result.items[1].name == "February Newsletter"
        assert result.items[1].state == "scheduled"
        assert result.items[1].scheduled_at == 1706744800000
        assert result.items[2].newsletter_id == "nws_789ghi"
        assert result.items[2].name == "March Newsletter"
        assert result.items[2].state == "draft"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/newsletters"
        assert kwargs["params"] == {"page": 1, "pageSize": 25}
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_get_newsletter(self, newsletters_resource, mock_client):
        """Test getting a specific newsletter."""
        # Setup mock response with proper aliases
        mock_response = {
            "newsletterId": "nws_123abc",
            "name": "Monthly Update - January 2023",
            "sentAt": 1703066400000,
            "source": "editor",
            "state": "sent",
            "segmentId": "seg_456def",
            "senderId": "snd_789ghi",
            "replyTo": "support@example.com",
            "subject": "Your January Newsletter Is Here!",
            "preheader": "Check out our latest updates and offers",
            "bodyDesign": {"blocks": [{"type": "header", "text": "January Newsletter"}]},
            "thumbnail": "https://example.com/thumbnails/jan-2023.png",
            "preview": "https://example.com/preview/nws_123abc",
            "createdAt": 1701066400000,
            "modifiedAt": 1702066400000,
            "modifiedBy": "usr_abc123"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        newsletter_id = "nws_123abc"
        result = await newsletters_resource.get(newsletter_id)

        # Verify the result
        assert isinstance(result, GetNewsletterResponse)
        assert result.newsletter_id == "nws_123abc"
        assert result.name == "Monthly Update - January 2023"
        assert result.sent_at == 1703066400000
        assert result.source == "editor"
        assert result.state == "sent"
        assert result.segment_id == "seg_456def"
        assert result.sender_id == "snd_789ghi"
        assert result.reply_to == "support@example.com"
        assert result.subject == "Your January Newsletter Is Here!"
        assert result.preheader == "Check out our latest updates and offers"
        assert result.body_design == {"blocks": [{"type": "header", "text": "January Newsletter"}]}
        assert result.thumbnail == "https://example.com/thumbnails/jan-2023.png"
        assert result.preview == "https://example.com/preview/nws_123abc"
        assert result.created_at == 1701066400000
        assert result.modified_at == 1702066400000
        assert result.modified_by == "usr_abc123"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/newsletters/nws_123abc",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_create_newsletter_html(self, newsletters_resource, mock_client):
        """Test creating an HTML newsletter."""
        # Setup mock response with proper aliases
        mock_response = {
            "newsletterId": "nws_123abc",
            "name": "Product Launch Announcement",
            "source": "html",
            "state": "draft",
            "segmentId": "seg_456def",
            "senderId": "snd_789ghi",
            "subject": "Introducing Our New Product Line",
            "body": "<html><body><h1>Exciting News!</h1>...</body></html>",
            "createdAt": 1703066400000,
            "modifiedBy": "usr_abc123"
        }
        mock_client._request.return_value = mock_response

        # Create request data
        request_data = CreateEmailNewsletterRequest(
            name="Product Launch Announcement",
            source="html",
            segment_id="seg_456def",
            sender_id="snd_789ghi",
            subject="Introducing Our New Product Line",
            body="<html><body><h1>Exciting News!</h1>...</body></html>"
        )

        # Call the method
        result = await newsletters_resource.create(request_data)

        # Verify the result
        assert isinstance(result, CreateNewsletterResponse)
        assert result.newsletter_id == "nws_123abc"
        assert result.name == "Product Launch Announcement"
        assert result.source == "html"
        assert result.state == "draft"
        assert result.segment_id == "seg_456def"
        assert result.sender_id == "snd_789ghi"
        assert result.subject == "Introducing Our New Product Line"
        assert result.body == "<html><body><h1>Exciting News!</h1>...</body></html>"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/email/newsletters"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_create_newsletter_scheduled(self, newsletters_resource, mock_client):
        """Test creating a scheduled newsletter."""
        # Setup mock response with proper aliases
        mock_response = {
            "newsletterId": "nws_456def",
            "name": "February Newsletter",
            "scheduledAt": 1706744800000,
            "source": "editor",
            "state": "scheduled",
            "segmentId": "seg_456def",
            "senderId": "snd_789ghi",
            "subject": "February Updates",
            "bodyDesign": {"blocks": [{"type": "header", "text": "February Newsletter"}]},
            "createdAt": 1703066400000,
            "modifiedBy": "usr_abc123"
        }
        mock_client._request.return_value = mock_response

        # Create request data
        body_design = {"blocks": [{"type": "header", "text": "February Newsletter"}]}
        request_data = CreateEmailNewsletterRequest(
            name="February Newsletter",
            scheduled_at=1706744800000,
            source="editor",
            segment_id="seg_456def",
            sender_id="snd_789ghi",
            subject="February Updates",
            body_design=body_design
        )

        # Call the method
        result = await newsletters_resource.create(request_data)

        # Verify the result
        assert isinstance(result, CreateNewsletterResponse)
        assert result.newsletter_id == "nws_456def"
        assert result.name == "February Newsletter"
        assert result.scheduled_at == 1706744800000
        assert result.source == "editor"
        assert result.state == "scheduled"
        assert result.segment_id == "seg_456def"
        assert result.sender_id == "snd_789ghi"
        assert result.subject == "February Updates"
        assert result.body_design == {"blocks": [{"type": "header", "text": "February Newsletter"}]}

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/email/newsletters"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_update_newsletter(self, newsletters_resource, mock_client):
        """Test updating a newsletter."""
        # Setup mock response with proper aliases
        mock_response = {
            "newsletterId": "nws_123abc",
            "name": "Monthly Update - January 2023 (Revised)",
            "scheduledAt": 1703156400000,
            "source": "editor",
            "state": "scheduled",
            "segmentId": "seg_456def",
            "senderId": "snd_789ghi",
            "subject": "Your January Newsletter Is Here! (Updated)",
            "bodyDesign": {"blocks": [{"type": "header", "text": "January Newsletter"}]},
            "preview": "https://example.com/preview/nws_123abc",
            "createdAt": 1701066400000,
            "modifiedAt": 1702066400000,
            "modifiedBy": "usr_abc123"
        }
        mock_client._request.return_value = mock_response

        # Create request data
        body_design = {"blocks": [{"type": "header", "text": "January Newsletter"}]}
        request_data = CreateEmailNewsletterRequest(
            name="Monthly Update - January 2023 (Revised)",
            scheduled_at=1703156400000,
            source="editor",
            segment_id="seg_456def",
            sender_id="snd_789ghi",
            subject="Your January Newsletter Is Here! (Updated)",
            body_design=body_design
        )

        # Call the method
        newsletter_id = "nws_123abc"
        result = await newsletters_resource.update(request_data, newsletter_id)

        # Verify the result
        assert isinstance(result, UpdateNewsletterResponse)
        assert result.newsletter_id == "nws_123abc"
        assert result.name == "Monthly Update - January 2023 (Revised)"
        assert result.scheduled_at == 1703156400000
        assert result.source == "editor"
        assert result.state == "scheduled"
        assert result.subject == "Your January Newsletter Is Here! (Updated)"
        assert result.modified_at == 1702066400000
        assert result.modified_by == "usr_abc123"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "PUT"
        assert args[1] == "/email/newsletters/nws_123abc"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_delete_newsletter(self, newsletters_resource, mock_client):
        """Test deleting a newsletter."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        newsletter_id = "nws_123abc"
        result = await newsletters_resource.delete(newsletter_id)

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/email/newsletters/nws_123abc",
            headers={"Content-Type": "application/json"}
        )