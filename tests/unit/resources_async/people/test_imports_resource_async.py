"""
Unit tests for the asynchronous ImportsResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.people_resources.imports import ImportsResource
from naxai.models.people.responses.imports_responses import (
    ListImportsResponse,
    GetImportResponse
)


class TestImportsResourceAsync:
    """Test suite for the asynchronous ImportsResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def imports_resource(self, mock_client):
        """Create an ImportsResource instance with a mock client."""
        return ImportsResource(mock_client, "/people")

    def test_initialization(self, imports_resource):
        """Test that the ImportsResource initializes correctly."""
        assert imports_resource.root_path == "/people/imports"
        assert imports_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_list_imports(self, imports_resource, mock_client):
        """Test listing imports."""
        # Setup mock response
        mock_response = [
            {
                "id": "imp_123abc",
                "name": "Monthly Import",
                "state": "imported",
                "type": "manual",
                "import_mode": "contacts",
                "rows_to_import": 1000,
                "rows_imported": 1000,
                "created_at": 1703066400000
            },
            {
                "id": "imp_456def",
                "name": "Weekly Import",
                "state": "importing",
                "type": "manual",
                "import_mode": "contacts",
                "rows_to_import": 500,
                "rows_imported": 250,
                "created_at": 1703066500000
            },
            {
                "id": "imp_789ghi",
                "name": "Failed Import",
                "state": "failed",
                "type": "ftp-template",
                "import_mode": "events",
                "rows_to_import": 100,
                "rows_imported": 0,
                "failed_reason": "Invalid data format",
                "created_at": 1703066600000
            }
        ]
        mock_client._request.return_value = mock_response

        # Call the method
        result = await imports_resource.list()

        # Verify the result
        assert isinstance(result, ListImportsResponse)
        assert len(result) == 3
        
        assert result[0].id == "imp_123abc"
        assert result[0].name == "Monthly Import"
        assert result[0].state == "imported"
        assert result[0].type_ == "manual"
        assert result[0].import_mode == "contacts"
        assert result[0].rows_to_import == 1000
        assert result[0].rows_imported == 1000
        assert result[0].created_at == 1703066400000
        
        assert result[1].id == "imp_456def"
        assert result[1].name == "Weekly Import"
        assert result[1].state == "importing"
        assert result[1].rows_to_import == 500
        assert result[1].rows_imported == 250
        
        assert result[2].id == "imp_789ghi"
        assert result[2].name == "Failed Import"
        assert result[2].state == "failed"
        assert result[2].failed_reason == "Invalid data format"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/imports",
            headers={"Content-Type": "application/json"}
        )

    @pytest.mark.asyncio
    async def test_get_import(self, imports_resource, mock_client):
        """Test getting an import."""
        # Setup mock response
        mock_response = {
            "id": "imp_123abc",
            "name": "Monthly Import",
            "state": "imported",
            "type": "manual",
            "import_mode": "contacts",
            "rows_to_import": 1000,
            "rows_imported": 1000,
            "created_at": 1703066400000,
            "file": {
                "separator": ",",
                "encoding": "UTF-8"
            },
            "mapping": [
                {
                    "header": "Email",
                    "attribute": "email",
                    "skip": False
                },
                {
                    "header": "First Name",
                    "attribute": "first_name",
                    "skip": False
                },
                {
                    "header": "Last Name",
                    "attribute": "last_name",
                    "skip": False
                },
                {
                    "header": "Notes",
                    "skip": True
                }
            ],
            "segment": {
                "segment_id": "seg_123abc",
                "name": "Imported Contacts"
            }
        }
        mock_client._request.return_value = mock_response

        # Call the method
        import_id = "imp_123abc"
        result = await imports_resource.get(import_id)

        # Verify the result
        assert isinstance(result, GetImportResponse)
        assert result.id == "imp_123abc"
        assert result.name == "Monthly Import"
        assert result.state == "imported"
        assert result.type_ == "manual"
        assert result.import_mode == "contacts"
        assert result.rows_to_import == 1000
        assert result.rows_imported == 1000
        assert result.created_at == 1703066400000
        
        # Check file information
        assert result.file is not None
        assert result.file.separator == ","
        
        # Check mapping information
        assert result.mapping is not None
        assert len(result.mapping) == 4
        assert result.mapping[0].header == "Email"
        assert result.mapping[0].attribute == "email"
        assert result.mapping[0].skip is False
        assert result.mapping[3].header == "Notes"
        assert result.mapping[3].skip is True
        
        # Check segment information
        assert result.segment is not None
        assert result.segment.segment_id == "seg_123abc"

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "GET",
            "/people/imports/imp_123abc",
            headers={"Content-Type": "application/json"}
        )