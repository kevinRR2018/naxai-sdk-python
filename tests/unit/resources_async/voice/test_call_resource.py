"""
Unit tests for the asynchronous CallResource class.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from naxai.resources_async.voice_resources.call import CallResource
from naxai.models.voice.requests.call_requests import CreateCallRequest
from naxai.models.voice.voice_flow import (
    Welcome,
    End,
    Menu,
    VoiceMail,
    Choice,
    Transfer,
    Whisper
)
from naxai.models.voice.responses.call_responses import (
    CreateCallResponse,
    Call
)


class TestCallResource:
    """Test suite for the asynchronous CallResource class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = AsyncMock()
        return client

    @pytest.fixture
    def call_resource(self, mock_client):
        """Create a CallResource instance with a mock client."""
        return CallResource(mock_client, "/voice")

    def test_initialization(self, call_resource):
        """Test that the CallResource initializes correctly."""
        assert call_resource.root_path == "/voice/call"
        assert call_resource.headers == {"Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_create_call(self, call_resource, mock_client):
        """Test creating a call."""
        # Setup mock response with all required fields using aliases
        mock_response = {
            "batchId": "batch_123abc",
            "count": 1,
            "calls": [
                {
                    "callId": "call_123abc",
                    "to": "1234567890"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Create request data
        welcome = Welcome(say="Hello, this is a test call.")
        language = "en-GB"
        to = ["1234567890"]
        from_ = "9876543210"
        voice = "woman"

        # Call the method
        result = await call_resource.create(
            welcome=welcome,
            language=language,
            to=to,
            from_=from_,
            voice=voice
        )

        # Verify the result
        assert isinstance(result, CreateCallResponse)
        assert result.batch_id == "batch_123abc"
        assert result.count == 1
        assert len(result.calls) == 1
        assert result.calls[0].call_id == "call_123abc"
        assert result.calls[0].to == "1234567890"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/voice/call"
        assert "json" in kwargs
        assert kwargs["headers"] == {"Content-Type": "application/json"}
        
        # Verify the request data
        request_data = kwargs["json"]
        assert "to" in request_data
        assert request_data["to"] == to
        assert "from" in request_data
        assert request_data["from"] == from_
        assert "language" in request_data
        assert request_data["language"] == language
        assert "welcome" in request_data
        assert "voice" in request_data
        assert request_data["voice"] == voice

    @pytest.mark.asyncio
    async def test_create_call_with_optional_params(self, call_resource, mock_client):
        """Test creating a call with optional parameters."""
        # Setup mock response with all required fields using aliases
        mock_response = {
            "batchId": "batch_456def",
            "count": 1,
            "calls": [
                {
                    "callId": "call_456def",
                    "to": "1234567890"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Create request data
        welcome = Welcome(say="Hello, this is a test call.")
        language = "en-GB"
        to = ["1234567890"]
        from_ = "9876543210"
        voice = "man"
        batch_id = "batch_123"
        idempotency_key = "idem_key_123"
        calendar_id = "cal_123"
        scheduled_at = 1672660800000  # 2023-01-02T12:00:00Z in milliseconds
        machine_detection = True
        voicemail = VoiceMail(say="Please leave a message")
        
        # Create menu with proper choices structure
        transfer = Transfer(destination="1234567891")
        choices = [
            Choice(key="1", say="Transferring to sales", transfer=transfer),
            Choice(key="2", say="Recording voicemail"),
            Choice(key="3", say="Ending call")
        ]
        menu = Menu(say="Press 1 for sales, 2 for voicemail, or 3 to end the call", choices=choices)
        end = End(say="Thank you for calling")

        # Call the method
        result = await call_resource.create(
            welcome=welcome,
            language=language,
            to=to,
            from_=from_,
            voice=voice,
            batch_id=batch_id,
            idempotency_key=idempotency_key,
            calendar_id=calendar_id,
            scheduled_at=scheduled_at,
            machine_detection=machine_detection,
            voicemail=voicemail,
            menu=menu,
            end=end
        )

        # Verify the result
        assert isinstance(result, CreateCallResponse)
        assert result.batch_id == "batch_456def"
        assert result.count == 1
        assert len(result.calls) == 1
        assert result.calls[0].call_id == "call_456def"
        assert result.calls[0].to == "1234567890"

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "POST"
        assert args[1] == "/voice/call"
        
        # Verify the request data
        request_data = kwargs["json"]
        assert request_data["batchId"] == batch_id
        assert request_data["idempotencyKey"] == idempotency_key
        assert request_data["calendarId"] == calendar_id
        assert request_data["scheduledAt"] == scheduled_at
        assert request_data["machineDetection"] == machine_detection
        
        # Verify voicemail
        assert "voicemail" in request_data
        assert request_data["voicemail"]["say"] == "Please leave a message"
        
        # Verify menu and its choices
        assert "menu" in request_data
        assert request_data["menu"]["say"] == "Press 1 for sales, 2 for voicemail, or 3 to end the call"
        assert len(request_data["menu"]["choices"]) == 3
        
        # Check first menu choice
        assert request_data["menu"]["choices"][0]["key"] == "1"
        assert request_data["menu"]["choices"][0]["say"] == "Transferring to sales"
        assert request_data["menu"]["choices"][0]["transfer"]["destination"] == "1234567891"
        
        # Check second menu choice
        assert request_data["menu"]["choices"][1]["key"] == "2"
        assert request_data["menu"]["choices"][1]["say"] == "Recording voicemail"
        
        # Check third menu choice
        assert request_data["menu"]["choices"][2]["key"] == "3"
        assert request_data["menu"]["choices"][2]["say"] == "Ending call"
        
        # Verify end
        assert "end" in request_data
        assert request_data["end"]["say"] == "Thank you for calling"

    @pytest.mark.asyncio
    async def test_create_internal_method(self, call_resource, mock_client):
        """Test the internal _create method."""
        # Setup mock response with all required fields using aliases
        mock_response = {
            "batchId": "XXXX-XXXXX-XXXXX",
            "count": 1,
            "calls": [
                {
                    "callId": "call_123abc",
                    "to": "1234567890"
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Create menu choices properly
        transfer = Transfer(destination="1234567891")
        choices = [
            Choice(key="1", say="Transferring to sales", transfer=transfer),
            Choice(key="2", say="Recording voicemail")
        ]
        
        # Create request data with proper menu structure
        request_data = CreateCallRequest(
            to=["1234567890"],
            from_="9876543210",
            language="en-GB",
            welcome=Welcome(say="Hello, this is a test call."),
            voice="woman",
            batchId="XXXX-XXXXX-XXXXX",
            idempotencyKey="YYYY-YYYYY-YYYYY",
            menu=Menu(say="Press 1 for sales or 2 for voicemail", choices=choices)
        )

        # Call the internal method
        result = await call_resource._create(request_data)

        # Verify the result
        assert result == mock_response

        # Verify the client was called correctly
        mock_client._request.assert_called_once_with(
            "POST",
            "/voice/call",
            json=request_data.model_dump(by_alias=True, exclude_none=True),
            headers={"Content-Type": "application/json"}
        )