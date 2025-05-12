"""
Unit tests for the synchronous SharedDomainsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.email_resources.domains_resources.shared_domains import SharedDomainsResource
from naxai.models.email.responses.domains_responses import ListSharedDomainsResponse, BaseDomainResponse


class TestSharedDomainsResource:
    """Test suite for the synchronous SharedDomainsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def shared_domains_resource(self, mock_client):
        """Create a SharedDomainsResource instance with a mock client."""
        return SharedDomainsResource(mock_client, "/email/domains")

    def test_initialization(self, shared_domains_resource):
        """Test that the SharedDomainsResource initializes correctly."""
        assert shared_domains_resource.root_path == "/email/domains/shared-domains"
        assert shared_domains_resource.headers == {"Content-Type": "application/json"}

    def test_list_shared_domains(self, shared_domains_resource, mock_client):
        """Test listing shared domains."""
        # Setup mock response with proper structure
        mock_response = [
            {
                "id": "dom_123abc",
                "domainName": "shared1.naxai.com"
            },
            {
                "id": "dom_456def",
                "domainName": "shared2.naxai.com"
            },
            {
                "id": "dom_789ghi",
                "domainName": "marketing.naxai.com"
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = shared_domains_resource.list()

        # Verify the result
        assert isinstance(result, ListSharedDomainsResponse)
        assert len(result) == 3
        assert result[0].id == "dom_123abc"
        assert result[0].domain_name == "shared1.naxai.com"
        assert result[1].id == "dom_456def"
        assert result[1].domain_name == "shared2.naxai.com"
        assert result[2].id == "dom_789ghi"
        assert result[2].domain_name == "marketing.naxai.com"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/domains/shared-domains",
            headers={"Content-Type": "application/json"}
        )