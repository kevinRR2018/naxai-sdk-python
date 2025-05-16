"""
Unit tests for the asynchronous NaxaiAsyncClient class.
"""
import json
import os
import time
import pytest
from unittest.mock import patch, MagicMock, PropertyMock, AsyncMock
import httpx
from naxai.async_client import NaxaiAsyncClient
from naxai.base.exceptions import (
    NaxaiValueError,
    NaxaiAuthenticationError,
    NaxaiAuthorizationError,
    NaxaiResourceNotFound,
    NaxaiInvalidRequestError,
    NaxaiRateLimitExceeded,
    NaxaiAPIRequestError
)
from naxai.resources_async.voice import VoiceResource
from naxai.resources_async.calendars import CalendarsResource
from naxai.resources_async.email import EmailResource
from naxai.resources_async.sms import SMSResource
from naxai.resources_async.people import PeopleResource
from naxai.resources_async.webhooks import WebhooksResource


class TestNaxaiAsyncClient:
    """Test suite for the NaxaiAsyncClient class."""

    @pytest.fixture
    def mock_httpx_client(self):
        """Create a mock httpx async client."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            # Make all methods async mocks
            mock_instance.post = AsyncMock()
            mock_instance.request = AsyncMock()
            mock_instance.aclose = AsyncMock()
            yield mock_instance

    @pytest.fixture
    def mock_response(self):
        """Create a mock response."""
        mock_resp = MagicMock()
        mock_resp.is_error = False
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"key": "value"}
        mock_resp.text = '{"key": "value"}'
        return mock_resp

    @pytest.fixture
    def mock_auth_response(self):
        """Create a mock authentication response."""
        mock_resp = MagicMock()
        mock_resp.is_error = False
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "access_token": "test_token",
            "expires_in": 86400,
            "token_type": "bearer"
        }
        mock_resp.text = '{"access_token": "test_token", "expires_in": 86400, "token_type": "bearer"}'
        return mock_resp

    @pytest.fixture
    def client_params(self):
        """Return standard client parameters."""
        return {
            "api_client_id": "test_client_id",
            "api_client_secret": "test_client_secret",
            "api_version": "v1",
            "auth_url": "https://auth.example.com/token",
            "api_base_url": "https://api.example.com"
        }

    def test_initialization_with_params(self, client_params, mock_httpx_client):
        """Test client initialization with explicit parameters."""
        client = NaxaiAsyncClient(**client_params)
        
        assert client.api_client_id == "test_client_id"
        assert client.api_client_secret == "test_client_secret"
        assert client.api_version == "v1"
        assert client.auth_url == "https://auth.example.com/token"
        assert client.api_base_url == "https://api.example.com"
        
        # Test resource initialization
        assert isinstance(client.voice, VoiceResource)
        assert isinstance(client.calendars, CalendarsResource)
        assert isinstance(client.email, EmailResource)
        assert isinstance(client.sms, SMSResource)
        assert isinstance(client.people, PeopleResource)
        assert isinstance(client.webhooks, WebhooksResource)

    def test_initialization_with_env_vars(self, mock_httpx_client):
        """Test client initialization with environment variables."""
        with patch.dict(os.environ, {
            "NAXAI_CLIENT_ID": "env_client_id",
            "NAXAI_SECRET": "env_client_secret",
            "NAXAI_API_VERSION": "v2",
            "NAXAI_AUTH_URL": "https://env-auth.example.com/token",
            "NAXAI_API_URL": "https://env-api.example.com"
        }):
            client = NaxaiAsyncClient()
            
            assert client.api_client_id == "env_client_id"
            assert client.api_client_secret == "env_client_secret"
            assert client.api_version == "v2"
            assert client.auth_url == "https://env-auth.example.com/token"
            assert client.api_base_url == "https://env-api.example.com"

    def test_initialization_missing_client_id(self, mock_httpx_client):
        """Test client initialization with missing client ID."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(NaxaiValueError) as excinfo:
                NaxaiAsyncClient(
                    api_client_secret="test_secret",
                    api_version="v1",
                    auth_url="https://auth.example.com/token",
                    api_base_url="https://api.example.com"
                )
            assert "api_client_id is required" in str(excinfo.value)

    def test_initialization_missing_client_secret(self, mock_httpx_client):
        """Test client initialization with missing client secret."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(NaxaiValueError) as excinfo:
                NaxaiAsyncClient(
                    api_client_id="test_id",
                    api_version="v1",
                    auth_url="https://auth.example.com/token",
                    api_base_url="https://api.example.com"
                )
            assert "api_client_secret is required" in str(excinfo.value)

    def test_initialization_missing_api_base_url(self, mock_httpx_client):
        """Test client initialization with missing API base URL."""
        with patch.dict(os.environ, {}, clear=True):
            # Also patch the API_BASE_URL imported from config to be None
            with patch('naxai.async_client.API_BASE_URL', None):
                with pytest.raises(NaxaiValueError) as excinfo:
                    NaxaiAsyncClient(
                        api_client_id="test_id",
                        api_client_secret="test_secret",
                        api_version="v1",
                        auth_url="https://auth.example.com/token"
                    )
                assert "api_base_url is required" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_authentication_success(self, client_params, mock_httpx_client, mock_auth_response):
        """Test successful authentication."""
        mock_httpx_client.post.return_value = mock_auth_response
        
        client = NaxaiAsyncClient(**client_params)
        await client._authenticate()
        
        assert client.token == "test_token"
        assert client.token_expiry > time.time()
        
        # Verify the authentication request
        mock_httpx_client.post.assert_called_once_with(
            "https://auth.example.com/token",
            data={
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "grant_type": "client_credentials"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    @pytest.mark.asyncio
    async def test_authentication_failure(self, client_params, mock_httpx_client):
        """Test authentication failure."""
        mock_response = MagicMock()
        mock_response.is_error = True
        mock_response.status_code = 401
        mock_response.text = "Invalid credentials"
        mock_httpx_client.post.return_value = mock_response
        
        client = NaxaiAsyncClient(**client_params)
        
        with pytest.raises(NaxaiAuthenticationError) as excinfo:
            await client._authenticate()
        
        assert "Authentication failed" in str(excinfo.value)
        assert excinfo.value.status_code == 401

    @pytest.mark.asyncio
    async def test_token_reuse(self, client_params, mock_httpx_client, mock_auth_response):
        """Test token reuse when not expired."""
        mock_httpx_client.post.return_value = mock_auth_response
        
        client = NaxaiAsyncClient(**client_params)
        await client._authenticate()  # First authentication
        
        # Reset the mock to verify it's not called again
        mock_httpx_client.post.reset_mock()
        
        # Set token to be valid (not expired)
        client.token_expiry = time.time() + 3600  # Valid for 1 hour
        
        await client._authenticate()  # Should reuse token
        
        # Verify no new authentication request was made
        mock_httpx_client.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_token_refresh(self, client_params, mock_httpx_client, mock_auth_response):
        """Test token refresh when expired."""
        mock_httpx_client.post.return_value = mock_auth_response
        
        client = NaxaiAsyncClient(**client_params)
        await client._authenticate()  # First authentication
        
        # Reset the mock to verify it's called again
        mock_httpx_client.post.reset_mock()
        
        # Set token to be expired
        client.token_expiry = time.time() - 60  # Expired 1 minute ago
        
        await client._authenticate()  # Should refresh token
        
        # Verify a new authentication request was made
        mock_httpx_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_request_success(self, client_params, mock_httpx_client, mock_auth_response, mock_response):
        """Test successful request."""
        mock_httpx_client.post.return_value = mock_auth_response
        mock_httpx_client.request.return_value = mock_response
        
        client = NaxaiAsyncClient(**client_params)
        result = await client._request("GET", "/test/path")
        
        assert result == {"key": "value"}
        
        # Verify the request
        mock_httpx_client.request.assert_called_once_with(
            "GET",
            "https://api.example.com/test/path",
            headers={
                "Authorization": "Bearer test_token",
                "X-version": "v1"
            }
        )

    @pytest.mark.asyncio
    async def test_request_with_params(self, client_params, mock_httpx_client, mock_auth_response, mock_response):
        """Test request with query parameters."""
        mock_httpx_client.post.return_value = mock_auth_response
        mock_httpx_client.request.return_value = mock_response
        
        client = NaxaiAsyncClient(**client_params)
        await client._request("GET", "/test/path", params={"param1": "value1", "param2": "value2"})
        
        # Verify the request includes params
        mock_httpx_client.request.assert_called_once_with(
            "GET",
            "https://api.example.com/test/path",
            headers={
                "Authorization": "Bearer test_token",
                "X-version": "v1"
            },
            params={"param1": "value1", "param2": "value2"}
        )

    @pytest.mark.asyncio
    async def test_request_with_json(self, client_params, mock_httpx_client, mock_auth_response, mock_response):
        """Test request with JSON body."""
        mock_httpx_client.post.return_value = mock_auth_response
        mock_httpx_client.request.return_value = mock_response
        
        client = NaxaiAsyncClient(**client_params)
        await client._request("POST", "/test/path", json={"data": "value"})
        
        # Verify the request includes JSON
        mock_httpx_client.request.assert_called_once_with(
            "POST",
            "https://api.example.com/test/path",
            headers={
                "Authorization": "Bearer test_token",
                "X-version": "v1"
            },
            json={"data": "value"}
        )

    @pytest.mark.asyncio
    async def test_request_with_custom_headers(self, client_params, mock_httpx_client, mock_auth_response, mock_response):
        """Test request with custom headers."""
        mock_httpx_client.post.return_value = mock_auth_response
        mock_httpx_client.request.return_value = mock_response
        
        client = NaxaiAsyncClient(**client_params)
        await client._request("GET", "/test/path", headers={"Custom-Header": "value"})
        
        # Verify the request includes custom headers merged with default ones
        mock_httpx_client.request.assert_called_once_with(
            "GET",
            "https://api.example.com/test/path",
            headers={
                "Custom-Header": "value",
                "Authorization": "Bearer test_token",
                "X-version": "v1"
            }
        )

    @pytest.mark.asyncio
    async def test_handle_error_401(self, client_params, mock_httpx_client):
        """Test handling of 401 Unauthorized error."""
        client = NaxaiAsyncClient(**client_params)
        
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": {"code": "unauthorized", "message": "Unauthorized access"}}
        mock_response.text = '{"error": {"code": "unauthorized", "message": "Unauthorized access"}}'
        
        with pytest.raises(NaxaiAuthenticationError) as excinfo:
            await client._handle_error(mock_response)
        
        assert excinfo.value.status_code == 401
        assert excinfo.value.error_code == "unauthorized"
        assert "Unauthorized access" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_handle_error_403(self, client_params, mock_httpx_client):
        """Test handling of 403 Forbidden error."""
        client = NaxaiAsyncClient(**client_params)
        
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"error": {"code": "forbidden", "message": "Forbidden access"}}
        mock_response.text = '{"error": {"code": "forbidden", "message": "Forbidden access"}}'
        
        with pytest.raises(NaxaiAuthorizationError) as excinfo:
            await client._handle_error(mock_response)
        
        assert excinfo.value.status_code == 403
        assert excinfo.value.error_code == "forbidden"
        assert "Forbidden access" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_handle_error_404(self, client_params, mock_httpx_client):
        """Test handling of 404 Not Found error."""
        client = NaxaiAsyncClient(**client_params)
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": {"code": "not_found", "message": "Resource not found"}}
        mock_response.text = '{"error": {"code": "not_found", "message": "Resource not found"}}'
        
        with pytest.raises(NaxaiResourceNotFound) as excinfo:
            await client._handle_error(mock_response)
        
        assert excinfo.value.status_code == 404
        assert excinfo.value.error_code == "not_found"
        assert "Resource not found" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_handle_error_422(self, client_params, mock_httpx_client):
        """Test handling of 422 Validation Error."""
        client = NaxaiAsyncClient(**client_params)
        
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {"error": {"code": "validation_error", "message": "Invalid data"}}
        mock_response.text = '{"error": {"code": "validation_error", "message": "Invalid data"}}'
        
        with pytest.raises(NaxaiInvalidRequestError) as excinfo:
            await client._handle_error(mock_response)
        
        assert excinfo.value.status_code == 422
        assert excinfo.value.error_code == "validation_error"
        assert "Invalid data" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_handle_error_429(self, client_params, mock_httpx_client):
        """Test handling of 429 Rate Limit error."""
        client = NaxaiAsyncClient(**client_params)
        
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": {"code": "rate_limit", "message": "Too many requests"}}
        mock_response.text = '{"error": {"code": "rate_limit", "message": "Too many requests"}}'
        
        with pytest.raises(NaxaiRateLimitExceeded) as excinfo:
            await client._handle_error(mock_response)
        
        assert excinfo.value.status_code == 429
        assert excinfo.value.error_code == "rate_limit"
        assert "Too many requests" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_handle_error_500(self, client_params, mock_httpx_client):
        """Test handling of 500 Server Error."""
        client = NaxaiAsyncClient(**client_params)
        
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": {"code": "server_error", "message": "Internal server error"}}
        mock_response.text = '{"error": {"code": "server_error", "message": "Internal server error"}}'
        
        with pytest.raises(NaxaiAPIRequestError) as excinfo:
            await client._handle_error(mock_response)
        
        assert excinfo.value.status_code == 500
        assert excinfo.value.error_code == "server_error"
        assert "Internal server error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_handle_error_invalid_json(self, client_params, mock_httpx_client):
        """Test handling of error with invalid JSON response."""
        client = NaxaiAsyncClient(**client_params)
        
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Not a JSON response"
        
        with pytest.raises(NaxaiAPIRequestError) as excinfo:
            await client._handle_error(mock_response)
        
        assert excinfo.value.status_code == 500
        assert "Not a JSON response" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_aclose(self, client_params, mock_httpx_client):
        """Test client aclose method."""
        client = NaxaiAsyncClient(**client_params)
        await client.aclose()
        
        mock_httpx_client.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_context_manager(self, client_params, mock_httpx_client):
        """Test using the client as an async context manager."""
        async with NaxaiAsyncClient(**client_params) as client:
            assert isinstance(client, NaxaiAsyncClient)
            # The client should be usable within the context
            assert client.api_client_id == "test_client_id"
        
        # After exiting the context, aclose should have been called
        mock_httpx_client.aclose.assert_called_once()