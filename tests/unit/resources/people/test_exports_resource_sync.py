"""
Unit tests for the synchronous ExportsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.people_resources.exports import ExportsResource
from naxai.models.people.helper_models.search_condition import SearchCondition
from naxai.models.people.responses.exports_responses import (
    ListExportsResponse,
    GetExportResponse,
    GetExportDownloadUrlResponse,
    CreateExportResponse
)


class TestExportsResourceSync:
    """Test suite for the synchronous ExportsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def exports_resource(self, mock_client):
        """Create an ExportsResource instance with a mock client."""
        return ExportsResource(mock_client, "/people")

    def test_initialization(self, exports_resource):
        """Test that the ExportsResource initializes correctly."""
        assert exports_resource.root_path == "/people/exports"
        assert exports_resource.headers == {"Content-Type": "application/json"}

    def test_list_exports(self, exports_resource, mock_client):
        """Test listing exports."""
        # Setup mock response
        mock_response = [
            {
                "id": "exp_123abc",
                "export": "contacts",
                "userId": "user_123abc",
                "state": "done",
                "rows": 1000,
                "failed": False,
                "created_at": 1703066400000
            },
            {
                "id": "exp_456def",
                "export": "contacts",
                "userId": "user_123abc",
                "state": "pending",
                "rows": None,
                "failed": False,
                "created_at": 1703066500000
            },
            {
                "id": "exp_789ghi",
                "export": "contacts",
                "userId": "user_123abc",
                "state": "failed",
                "rows": None,
                "failed": True,
                "created_at": 1703066600000
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = exports_resource.list()

        # Verify the result
        assert isinstance(result, ListExportsResponse)
        assert len(result) == 3
        
        assert result[0].id == "exp_123abc"
        assert result[0].export == "contacts"
        assert result[0].state == "done"
        assert result[0].rows == 1000
        assert result[0].failed is False
        assert result[0].created_at == 1703066400000
        
        assert result[1].id == "exp_456def"
        assert result[1].state == "pending"
        
        assert result[2].id == "exp_789ghi"
        assert result[2].state == "failed"
        assert result[2].failed is True

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/exports",
            headers={"Content-Type": "application/json"}
        )

    def test_create_export(self, exports_resource, mock_client):
        """Test creating an export."""
        # Setup mock response
        mock_response = {
            "pagination": {
                "page": 1,
                "pageSize": 10,
                "totalRecord": 100,
                "returnedRecord": 10,
                "remainingRecord": 90
            },
            "contacts": [
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
        result = exports_resource.create(condition)

        # Verify the result
        assert isinstance(result, CreateExportResponse)
        assert result.pagination.total_record == 100
        assert len(result.contacts) == 2
        assert result.contacts[0].nx_id == "cnt_123abc"
        assert result.contacts[0].country == "US"
        assert result.contacts[1].nx_id == "cnt_456def"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/people/exports"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}

    def test_get_export(self, exports_resource, mock_client):
        """Test getting an export."""
        # Setup mock response
        mock_response = {
            "id": "exp_123abc",
            "userId": "user_123abs",
            "export": "Contacts",
            "state": "done",
            "rows": 1000,
            "failed": False,
            "created_at": 1703066400000
        }
        mock_client._request.return_value = mock_response

        # Call the method
        export_id = "exp_123abc"
        result = exports_resource.get(export_id)

        # Verify the result
        assert isinstance(result, GetExportResponse)
        assert result.id == "exp_123abc"
        assert result.export == "Contacts"
        assert result.state == "done"
        assert result.rows == 1000
        assert result.failed is False
        assert result.created_at == 1703066400000

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/exports/exp_123abc",
            headers={"Content-Type": "application/json"}
        )

    def test_get_download_url(self, exports_resource, mock_client):
        """Test getting an export download URL."""
        # Setup mock response
        mock_response = {
            "url": "https://example.com/download/exp_123abc"
        }
        mock_client._request.return_value = mock_response

        # Call the method
        export_id = "exp_123abc"
        result = exports_resource.get_download_url(export_id)

        # Verify the result
        assert isinstance(result, GetExportDownloadUrlResponse)
        assert result.url == "https://example.com/download/exp_123abc"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/exports/exp_123abc/download",
            headers={"Content-Type": "application/json"}
        )