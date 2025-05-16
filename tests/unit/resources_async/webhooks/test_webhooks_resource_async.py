"""
Unit tests for the asynchronous WebhooksResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.webhooks import WebhooksResource
from naxai.models.webhooks.requests.webhooks_requests import (
    CreateWebhookRequest,
    UpdateWebhookJsonPathRequestAddReplace,
    UpdateWebhookJsonPathRequestMoveCopy,
    UpdateWebhookJsonPathRequestRemove
)
from naxai.models.webhooks.responses.webhooks_responses import (
    ListWebhooksResponse,
    CreateWebhookResponse,
    GetWebhookResponse,
    UpdateWebhookResponse,
    ListLastWebhookEventsResponse,
    ListEventTypesResponse
)
from naxai.models.webhooks.helper_models.authentication import (
    NoAuthModel,
    BasicAuthModel,
    OAuth2AuthModel,
    HeaderAuthModel
)


class TestWebhooksResourceAsync:
    """Test suite for the asynchronous WebhooksResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def webhooks_resource(self, mock_client):
        """Create a WebhooksResource instance with a mock client."""
        return WebhooksResource(mock_client)

    def test_initialization(self, webhooks_resource):
        """Test that the WebhooksResource initializes correctly."""
        assert webhooks_resource.root_path == "/webhooks/endpoints"
        assert webhooks_resource.events_root_path == "/webhooks"
        assert webhooks_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list(self, webhooks_resource, mock_client):
        """Test listing webhooks."""
        # Setup mock response
        mock_response = [
            {
                "id": "wh_123",
                "name": "Test Webhook",
                "url": "https://example.com/webhook",
                "authentication": {"type": "none"},
                "active": True,
                "eventObject": "Sms",
                "eventFilter": ["*"],
                "eventNames": ["sms.delivered"]
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = await webhooks_resource.list()

        # Verify the result
        assert isinstance(result, ListWebhooksResponse)
        assert len(result) == 1
        assert result[0].id == "wh_123"
        assert result[0].name == "Test Webhook"
        assert result[0].url == "https://example.com/webhook"
        assert result[0].active is True
        assert result[0].event_object == "Sms"
        assert result[0].event_filter == ["*"]
        assert result[0].event_names == ["sms.delivered"]

        # Verify the request
        mock_client._request.assert_called_once_with(
            "GET",
            "/webhooks/endpoints",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_create(self, webhooks_resource, mock_client):
        """Test creating a webhook."""
        # Setup mock response
        mock_response = {
            "id": "wh_123",
            "name": "Test Webhook",
            "url": "https://example.com/webhook",
            "authentication": {"type": "none"},
            "active": True,
            "eventObject": "Sms",
            "eventFilter": ["*"],
            "eventNames": ["sms.delivered"]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await webhooks_resource.create(
            name="Test Webhook",
            url="https://example.com/webhook",
            authentication=NoAuthModel(),
            event_object="Sms",
            event_filter=["*"],
            event_names=["sms.delivered"]
        )

        # Verify the result
        assert isinstance(result, CreateWebhookResponse)
        assert result.id == "wh_123"
        assert result.name == "Test Webhook"
        assert result.url == "https://example.com/webhook"
        assert result.active is True
        assert result.event_object == "Sms"
        assert result.event_filter == ["*"]
        assert result.event_names == ["sms.delivered"]

        # Verify the request
        mock_client._request.assert_called_once()
        args = mock_client._request.call_args
        assert args[0] == ("POST", "/webhooks/endpoints")
        assert args[1]["headers"] == {"Content-Type": "application/json"}
        assert isinstance(args[1]["json"], dict)

    @pytest.mark.asyncio
    async def test_get(self, webhooks_resource, mock_client):
        """Test getting a specific webhook."""
        # Setup mock response
        mock_response = {
            "id": "wh_123",
            "name": "Test Webhook",
            "url": "https://example.com/webhook",
            "authentication": {"type": "none"},
            "active": True,
            "eventObject": "Sms",
            "eventFilter": ["*"],
            "eventNames": ["sms.delivered"]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await webhooks_resource.get("wh_123")

        # Verify the result
        assert isinstance(result, GetWebhookResponse)
        assert result.id == "wh_123"
        assert result.name == "Test Webhook"
        assert result.url == "https://example.com/webhook"
        assert result.active is True
        assert result.event_object == "Sms"
        assert result.event_filter == ["*"]
        assert result.event_names == ["sms.delivered"]

        # Verify the request
        mock_client._request.assert_called_once_with(
            "GET",
            "/webhooks/endpoints/wh_123",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_delete(self, webhooks_resource, mock_client):
        """Test deleting a webhook."""
        # Setup mock response
        mock_client._request.return_value = None

        # Call the method
        result = await webhooks_resource.delete("wh_123")

        # Verify the result
        assert result is None

        # Verify the request
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/webhooks/endpoints/wh_123",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_update(self, webhooks_resource, mock_client):
        """Test updating a webhook."""
        # Setup mock response
        mock_response = {
            "id": "wh_123",
            "name": "Updated Webhook",
            "url": "https://example.com/webhook",
            "authentication": {"type": "none"},
            "active": True,
            "eventObject": "Sms",
            "eventFilter": ["*"],
            "eventNames": ["sms.delivered"]
        }
        mock_client._request.return_value = mock_response

        # Create update operations
        update_ops = [
            UpdateWebhookJsonPathRequestAddReplace(
                path="/name",
                value="Updated Webhook"
            )
        ]

        # Call the method
        result = await webhooks_resource.update("wh_123", update_ops)

        # Verify the result
        assert isinstance(result, UpdateWebhookResponse)
        assert result.id == "wh_123"
        assert result.name == "Updated Webhook"

        # Verify the request
        mock_client._request.assert_called_once()
        args = mock_client._request.call_args
        assert args[0] == ("PATCH", "/webhooks/endpoints/wh_123")
        assert args[1]["headers"] == {"Content-Type": "application/json"}
        assert isinstance(args[1]["json"], list)

    @pytest.mark.asyncio
    async def test_list_last_events(self, webhooks_resource, mock_client):
        """Test listing last events for a webhook."""
        # Setup mock response
        mock_response = [
            {
                "eventName": "sms.delivered",
                "eventWebhookId": "wh_123",
                "eventTimestamp": 1234567890,
                "eventId": "evt_123",
                "eventData": {"status": "delivered"}
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = await webhooks_resource.list_last_events("wh_123")

        # Verify the result
        assert isinstance(result, ListLastWebhookEventsResponse)
        assert len(result) == 1
        assert result[0].event_name == "sms.delivered"
        assert result[0].event_webhook_id == "wh_123"
        assert result[0].event_timestamp == 1234567890
        assert result[0].event_id == "evt_123"
        assert result[0].event_data.status == "delivered"

        # Verify the request
        mock_client._request.assert_called_once_with(
            "GET",
            "/webhooks/wh_123/last",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_list_events(self, webhooks_resource, mock_client):
        """Test listing available event types."""
        # Setup mock response
        mock_response = {
            "events": ["sms.delivered", "sms.failed", "email.sent"]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await webhooks_resource.list_events()

        # Verify the result
        assert isinstance(result, ListEventTypesResponse)
        assert result.events == ["sms.delivered", "sms.failed", "email.sent"]

        # Verify the request
        mock_client._request.assert_called_once_with(
            "GET",
            "/webhooks/events",
            headers={"Content-Type": "application/json"}
        ) 