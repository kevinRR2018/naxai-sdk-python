"""
Unit tests for the asynchronous TemplatesResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.email_resources.templates import TemplatesResource
from naxai.models.email.requests.templates_requests import CreateEmailTemplateRequest
from naxai.models.email.responses.templates_responses import (
    CreateTemplateResponse,
    GetTemplateResponse,
    UpdateTemplateResponse,
    ListTemplatesResponse,
    GetSharedTemplateResponse,
    ListSharedTemplatesRespone
)
from naxai.models.base.pagination import Pagination


class TestTemplatesResource:
    """Test suite for the asynchronous TemplatesResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def templates_resource(self, mock_client):
        """Create a TemplatesResource instance with a mock client."""
        return TemplatesResource(mock_client, "/email")

    def test_initialization(self, templates_resource):
        """Test that the TemplatesResource initializes correctly."""
        assert templates_resource.root_path == "/email/templates"
        assert templates_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_templates(self, templates_resource, mock_client):
        """Test listing email templates."""
        # Setup mock response with proper aliases
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 25,
                "totalRecord": 30,
                "returnedRecord": 25,
                "remainingRecord": 5
            },
            "items": [
                {
                    "templateId": "tpl_123abc",
                    "name": "Welcome Email",
                    "source": "html",
                    "body": "<html><body><h1>Welcome!</h1></body></html>",
                    "createdAt": 1703066400000
                },
                {
                    "templateId": "tpl_456def",
                    "name": "Newsletter Template",
                    "source": "editor",
                    "bodyDesign": {"blocks": [{"type": "header", "text": "Newsletter"}]},
                    "createdAt": 1702980000000
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await templates_resource.list(page=1, page_size=25)

        # Verify the result
        assert isinstance(result, ListTemplatesResponse)
        assert result.pagination.page == 1
        assert result.pagination.page_size == 25
        assert result.pagination.total_record == 30
        assert len(result.items) == 2
        assert result.items[0].template_id == "tpl_123abc"
        assert result.items[0].name == "Welcome Email"
        assert result.items[0].source == "html"
        assert result.items[1].template_id == "tpl_456def"
        assert result.items[1].name == "Newsletter Template"
        assert result.items[1].source == "editor"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/templates"
        assert kwargs["params"] == {"page": 1, "pageSize": 25}
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_get_template(self, templates_resource, mock_client):
        """Test getting a specific email template."""
        # Setup mock response with proper aliases
        mock_response = {
            "templateId": "tpl_123abc",
            "name": "Welcome Email",
            "source": "html",
            "body": "<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>",
            "thumbnail": "https://example.com/thumbnails/welcome.png",
            "createdAt": 1703066400000,
            "modifiedAt": 1703066500000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        template_id = "tpl_123abc"
        result = await templates_resource.get(template_id)

        # Verify the result
        assert isinstance(result, GetTemplateResponse)
        assert result.template_id == "tpl_123abc"
        assert result.name == "Welcome Email"
        assert result.source == "html"
        assert result.body == "<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>"
        assert result.thumbnail == "https://example.com/thumbnails/welcome.png"
        assert result.created_at == 1703066400000
        assert result.modified_at == 1703066500000
        assert result.modified_by == "usr_789xyz"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/templates/tpl_123abc",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_create_template_html(self, templates_resource, mock_client):
        """Test creating an HTML email template."""
        # Setup mock response with proper aliases
        mock_response = {
            "templateId": "tpl_123abc",
            "name": "Welcome Email",
            "source": "html",
            "body": "<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>",
            "createdAt": 1703066400000,
            "modifiedAt": 1703066400000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Create request data
        request_data = CreateEmailTemplateRequest(
            name="Welcome Email",
            source="html",
            body="<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>"
        )

        # Call the method
        result = await templates_resource.create(request_data)

        # Verify the result
        assert isinstance(result, CreateTemplateResponse)
        assert result.template_id == "tpl_123abc"
        assert result.name == "Welcome Email"
        assert result.source == "html"
        assert result.body == "<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/email/templates"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}
        
        # Verify the request data was properly serialized
        request_json = kwargs["json"]
        assert request_json["name"] == "Welcome Email"
        assert request_json["source"] == "html"
        assert request_json["body"] == "<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>"

    @pytest.mark.asyncio
    async def test_create_template_editor(self, templates_resource, mock_client):
        """Test creating an editor-based email template."""
        # Setup mock response with proper aliases
        mock_response = {
            "templateId": "tpl_456def",
            "name": "Newsletter Template",
            "source": "editor",
            "bodyDesign": {"blocks": [{"type": "header", "text": "Newsletter"}]},
            "createdAt": 1703066400000,
            "modifiedAt": 1703066400000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Create request data
        body_design = {"blocks": [{"type": "header", "text": "Newsletter"}]}
        request_data = CreateEmailTemplateRequest(
            name="Newsletter Template",
            source="editor",
            body_design=body_design
        )

        # Call the method
        result = await templates_resource.create(request_data)

        # Verify the result
        assert isinstance(result, CreateTemplateResponse)
        assert result.template_id == "tpl_456def"
        assert result.name == "Newsletter Template"
        assert result.source == "editor"
        assert result.body_design == {"blocks": [{"type": "header", "text": "Newsletter"}]}

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/email/templates"
        
        # Verify the request data was properly serialized
        request_json = kwargs["json"]
        assert request_json["name"] == "Newsletter Template"
        assert request_json["source"] == "editor"
        assert request_json["bodyDesign"] == {"blocks": [{"type": "header", "text": "Newsletter"}]}

    @pytest.mark.asyncio
    async def test_update_template(self, templates_resource, mock_client):
        """Test updating an email template."""
        # Setup mock response with proper aliases
        mock_response = {
            "templateId": "tpl_123abc",
            "name": "Updated Welcome Email",
            "source": "html",
            "body": "<html><body><h1>Welcome!</h1><p>Thank you for joining our platform.</p></body></html>",
            "thumbnail": "https://example.com/thumbnails/welcome-updated.png",
            "createdAt": 1703066400000,
            "modifiedAt": 1703152800000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Create request data
        request_data = CreateEmailTemplateRequest(
            name="Updated Welcome Email",
            source="html",
            body="<html><body><h1>Welcome!</h1><p>Thank you for joining our platform.</p></body></html>",
            thumbnail="https://example.com/thumbnails/welcome-updated.png"
        )

        # Call the method
        template_id = "tpl_123abc"
        result = await templates_resource.update(template_id, request_data)

        # Verify the result
        assert isinstance(result, UpdateTemplateResponse)
        assert result.template_id == "tpl_123abc"
        assert result.name == "Updated Welcome Email"
        assert result.body == "<html><body><h1>Welcome!</h1><p>Thank you for joining our platform.</p></body></html>"
        assert result.thumbnail == "https://example.com/thumbnails/welcome-updated.png"
        assert result.modified_at == 1703152800000

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "PUT"
        assert args[1] == "/email/templates/tpl_123abc"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_delete_template(self, templates_resource, mock_client):
        """Test deleting an email template."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        template_id = "tpl_123abc"
        result = await templates_resource.delete(template_id)

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/email/templates/tpl_123abc",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_list_shared_templates(self, templates_resource, mock_client):
        """Test listing shared email templates."""
        # Setup mock response with proper aliases
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 25,
                "totalRecord": 65,
                "returnedRecord": 25,
                "remainingRecord": 40
            },
            "items": [
                {
                    "sharedTemplateId": "stpl_123abc",
                    "name": "Marketing Newsletter",
                    "thumbnail": "https://example.com/thumbnails/marketing.png",
                    "tags": ["marketing", "newsletter"]
                },
                {
                    "sharedTemplateId": "stpl_456def",
                    "name": "Product Announcement",
                    "thumbnail": "https://example.com/thumbnails/product.png",
                    "tags": ["product", "announcement"]
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = await templates_resource.list_shared(page=1, page_size=25)

        # Verify the result
        assert isinstance(result, ListSharedTemplatesRespone)
        assert result.pagination.page == 1
        assert result.pagination.page_size == 25
        assert result.pagination.total_record == 65
        assert len(result.items) == 2
        assert result.items[0].shared_template_id == "stpl_123abc"
        assert result.items[0].name == "Marketing Newsletter"
        assert result.items[0].tags == ["marketing", "newsletter"]
        assert result.items[1].shared_template_id == "stpl_456def"
        assert result.items[1].name == "Product Announcement"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/email/shared-templates"
        assert kwargs["params"] == {"page": 1, "pageSize": 25}
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_get_shared_template(self, templates_resource, mock_client):
        """Test getting a specific shared email template."""
        # Setup mock response with proper aliases
        mock_response = {
            "sharedTemplateId": "stpl_123abc",
            "name": "Marketing Newsletter",
            "thumbnail": "https://example.com/thumbnails/marketing.png",
            "preview": "https://example.com/preview/stpl_123abc",
            "tags": ["marketing", "newsletter"],
            "body": "<html><body><h1>Marketing Newsletter</h1><p>Your content here.</p></body></html>"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        template_id = "stpl_123abc"
        result = await templates_resource.get_shared(template_id)

        # Verify the result
        assert isinstance(result, GetSharedTemplateResponse)
        assert result.shared_template_id == "stpl_123abc"
        assert result.name == "Marketing Newsletter"
        assert result.thumbnail == "https://example.com/thumbnails/marketing.png"
        assert result.preview == "https://example.com/preview/stpl_123abc"
        assert result.tags == ["marketing", "newsletter"]
        assert result.body == "<html><body><h1>Marketing Newsletter</h1><p>Your content here.</p></body></html>"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/shared-templates/stpl_123abc",
            headers={"Content-Type": "application/json"}
        )