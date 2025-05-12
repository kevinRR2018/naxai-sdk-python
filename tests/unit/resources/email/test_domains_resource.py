"""
Unit tests for the synchronous DomainsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.email_resources.domains import DomainsResource
from naxai.models.email.responses.domains_responses import (
    ListDomainsResponse,
    GetDomainResponse,
    CreateDomainResponse,
    UpdateDomainResponse,
    VerifyDomainResponse,
    BaseRecord
)


class TestDomainsResource:
    """Test suite for the synchronous DomainsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def domains_resource(self, mock_client):
        """Create a DomainsResource instance with a mock client."""
        return DomainsResource(mock_client, "/email")

    def test_initialization(self, domains_resource):
        """Test that the DomainsResource initializes correctly."""
        assert domains_resource.root_path == "/email/domains"
        assert domains_resource.headers == {"Content-Type": "application/json"}
        assert hasattr(domains_resource, "shared_domains")

    def test_list_domains(self, domains_resource, mock_client):
        """Test listing email domains."""
        # Setup mock response with proper structure
        mock_response = [
            {
                "id": "dom_123abc",
                "domainName": "example.com",
                "verified": True,
                "sharedWithSubaccounts": True,
                "verificationToken": "naxai-verification=abc123def456",
                "dkimName": "_dkim.example.com",
                "dkimValue": "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
                "spfRecord": "v=spf1 include:spf.naxai.com ~all",
                "trackingName": "track.example.com",
                "trackingEnabled": True,
                "trackingValidated": True,
                "trackingRecord": "CNAME track.naxai.com",
                "modifiedAt": 1703066400000,
                "modifiedBy": "usr_789xyz"
            },
            {
                "id": "dom_456def",
                "domainName": "another-example.com",
                "verified": False,
                "sharedWithSubaccounts": False,
                "verificationToken": "naxai-verification=xyz789abc012",
                "dkimName": "_dkim.another-example.com",
                "dkimValue": "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
                "spfRecord": "v=spf1 include:spf.naxai.com ~all",
                "trackingName": "track.another-example.com",
                "trackingEnabled": True,
                "trackingValidated": False,
                "trackingRecord": "CNAME track.naxai.com",
                "modifiedAt": 1702980000000,
                "modifiedBy": "usr_789xyz"
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = domains_resource.list()

        # Verify the result
        assert isinstance(result, ListDomainsResponse)
        assert len(result) == 2
        assert result[0].id == "dom_123abc"
        assert result[0].domain_name == "example.com"
        assert result[0].verified is True
        assert result[0].shared_with_subaccounts is True
        assert result[0].verification_token == "naxai-verification=abc123def456"
        assert result[0].dkim_name == "_dkim.example.com"
        assert result[0].tracking_enabled is True
        assert result[0].tracking_validated is True
        
        assert result[1].id == "dom_456def"
        assert result[1].domain_name == "another-example.com"
        assert result[1].verified is False
        assert result[1].tracking_validated is False

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/domains",
            headers={"Content-Type": "application/json"}
        )

    def test_get_domain(self, domains_resource, mock_client):
        """Test getting a specific email domain."""
        # Setup mock response with proper structure
        mock_response = {
            "id": "dom_123abc",
            "domainName": "example.com",
            "verified": True,
            "sharedWithSubaccounts": True,
            "verificationToken": "naxai-verification=abc123def456",
            "dkimName": "_dkim.example.com",
            "dkimValue": "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
            "spfRecord": "v=spf1 include:spf.naxai.com ~all",
            "trackingName": "track.example.com",
            "trackingEnabled": True,
            "trackingValidated": True,
            "trackingRecord": "CNAME track.naxai.com",
            "modifiedAt": 1703066400000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        domain_id = "dom_123abc"
        result = domains_resource.get(domain_id)

        # Verify the result
        assert isinstance(result, GetDomainResponse)
        assert result.id == "dom_123abc"
        assert result.domain_name == "example.com"
        assert result.verified is True
        assert result.shared_with_subaccounts is True
        assert result.verification_token == "naxai-verification=abc123def456"
        assert result.dkim_name == "_dkim.example.com"
        assert result.dkim_value == "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA..."
        assert result.spf_record == "v=spf1 include:spf.naxai.com ~all"
        assert result.tracking_name == "track.example.com"
        assert result.tracking_enabled is True
        assert result.tracking_validated is True
        assert result.tracking_record == "CNAME track.naxai.com"
        assert result.modified_at == 1703066400000
        assert result.modified_by == "usr_789xyz"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/domains/dom_123abc",
            headers={"Content-Type": "application/json"}
        )

    def test_create_domain(self, domains_resource, mock_client):
        """Test creating an email domain."""
        # Setup mock response with proper structure
        mock_response = {
            "id": "dom_789ghi",
            "domainName": "new-example.com",
            "verified": False,
            "sharedWithSubaccounts": True,
            "verificationToken": "naxai-verification=ghi789jkl012",
            "dkimName": "_dkim.new-example.com",
            "dkimValue": "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
            "spfRecord": "v=spf1 include:spf.naxai.com ~all",
            "trackingName": "track.new-example.com",
            "trackingEnabled": True,
            "trackingValidated": False,
            "trackingRecord": "CNAME track.naxai.com",
            "modifiedAt": 1703066400000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        domain_name = "new-example.com"
        shared_with_subaccounts = True
        result = domains_resource.create(domain_name, shared_with_subaccounts)

        # Verify the result
        assert isinstance(result, CreateDomainResponse)
        assert result.id == "dom_789ghi"
        assert result.domain_name == "new-example.com"
        assert result.verified is False
        assert result.shared_with_subaccounts is True
        assert result.verification_token == "naxai-verification=ghi789jkl012"
        assert result.dkim_name == "_dkim.new-example.com"
        assert result.tracking_enabled is True
        assert result.tracking_validated is False

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/email/domains"
        assert kwargs["json"] == {
            "domainName": "new-example.com",
            "sharedWithSubaccounts": True
        }
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_update_domain(self, domains_resource, mock_client):
        """Test updating an email domain."""
        # Setup mock response with proper structure
        mock_response = {
            "id": "dom_123abc",
            "domainName": "example.com",
            "verified": True,
            "sharedWithSubaccounts": True,
            "verificationToken": "naxai-verification=abc123def456",
            "dkimName": "_dkim.example.com",
            "dkimValue": "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
            "spfRecord": "v=spf1 include:spf.naxai.com ~all",
            "trackingName": "track.example.com",
            "trackingEnabled": True,
            "trackingValidated": True,
            "trackingRecord": "CNAME track.naxai.com",
            "modifiedAt": 1703152800000,
            "modifiedBy": "usr_789xyz"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        domain_id = "dom_123abc"
        result = domains_resource.update(domain_id)

        # Verify the result
        assert isinstance(result, UpdateDomainResponse)
        assert result.id == "dom_123abc"
        assert result.domain_name == "example.com"
        assert result.verified is True
        assert result.shared_with_subaccounts is True
        assert result.modified_at == 1703152800000
        assert result.modified_by == "usr_789xyz"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "PUT",
            "/email/domains/dom_123abc",
            headers={"Content-Type": "application/json"}
        )

    def test_delete_domain(self, domains_resource, mock_client):
        """Test deleting an email domain."""
        # Setup mock response
        mock_response = {}
        mock_client._request.return_value = mock_response

        # Call the method
        domain_id = "dom_123abc"
        result = domains_resource.delete(domain_id)

        # Verify the result
        assert result == {}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "DELETE",
            "/email/domains/dom_123abc",
            headers={"Content-Type": "application/json"}
        )

    def test_verify_domain(self, domains_resource, mock_client):
        """Test verifying an email domain."""
        # Setup mock response with proper structure
        mock_response = {
            "spfRecord": {
                "currentValue": "v=spf1 include:spf.naxai.com ~all",
                "verified": True
            },
            "dkimRecord": {
                "currentValue": "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
                "verified": True
            },
            "trackingRecord": {
                "currentValue": "track.naxai.com",
                "verified": True
            },
            "mxRecord": {
                "currentValue": "10 mx.naxai.com",
                "verified": True
            },
            "verificationToken": {
                "currentValue": "naxai-verification=abc123def456",
                "verified": True
            }
        }
        mock_client._request.return_value = mock_response

        # Call the method
        domain_id = "dom_123abc"
        result = domains_resource.verify(domain_id)

        # Verify the result
        assert isinstance(result, VerifyDomainResponse)
        assert isinstance(result.spf_record, BaseRecord)
        assert result.spf_record.current_value == "v=spf1 include:spf.naxai.com ~all"
        assert result.spf_record.verified is True
        assert result.dkim_record.verified is True
        assert result.tracking_record.verified is True
        assert result.mx_record.verified is True
        assert result.verification_token.verified is True

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/email/domains/dom_123abc/verify",
            headers={"Content-Type": "application/json"}
        )

    def test_update_tracking_settings(self, domains_resource, mock_client):
        """Test updating tracking settings for a domain."""
        # Setup mock response
        mock_response = {"success": True}
        mock_client._request.return_value = mock_response

        # Call the method
        domain_id = "dom_123abc"
        enabled = True
        result = domains_resource.update_tracking_settings(domain_id, enabled)

        # Verify the result
        assert result == {"success": True}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "PUT",
            "/email/domains/dom_123abc/tracking/activities",
            json={"enabled": True},
            headers={"Content-Type": "application/json"}
        )

    def test_update_tracking_cname(self, domains_resource, mock_client):
        """Test updating tracking CNAME for a domain."""
        # Setup mock response
        mock_response = {"success": True}
        mock_client._request.return_value = mock_response

        # Call the method
        domain_id = "dom_123abc"
        prefix = "custom-track"
        result = domains_resource.update_tracking_cname(domain_id, prefix)

        # Verify the result
        assert result == {"success": True}

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "PUT",
            "/email/domains/dom_123abc/tracking/prefix",
            json={"prefix": "custom-track"},
            headers={"Content-Type": "application/json"}
        )

    def test_shared_domains_initialization(self, domains_resource):
        """Test that the shared_domains sub-resource is initialized correctly."""
        assert hasattr(domains_resource, "shared_domains")
        assert domains_resource.shared_domains.root_path == "/email/domains/shared-domains"