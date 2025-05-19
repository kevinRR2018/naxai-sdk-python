"""
Models for handling call-related webhook events.

This module defines the data models for various call events, including:
- Call transfers
- Base call event data
- Delivered call events
- Failed call events
- Call attempts

Each model uses Pydantic for data validation and serialization, with proper field aliases
for JSON compatibility.
"""

from typing import Optional, Literal, Union, List
from pydantic import BaseModel, Field

class Transfer(BaseModel):
    """Model representing a call transfer event."""
    call_id: str = Field(alias="callId")
    call_duration: int = Field(alias="callDuration")
    destination: str
    attempts: int
    status: str
    reason: str


class BaseCallEventData(BaseModel):
    """Base model for all call event data."""
    batch_id: str = Field(default=None, alias="batchId")
    call_id: str = Field(alias="callId")
    to: str
    from_: str = Field(alias="from")
    status: str
    reason: str
    details: str
    scheduled_at: int = Field(default=None, alias="scheduledAt")
    country: str
    network: Literal["mobile", "landline"] = Field(default=None)
    api_client_id: str = Field(default=None, alias="apiClientId")


class CallDeliveredEventData(BaseCallEventData):
    """Model representing the data for a delivered call event."""
    status: Literal["delivered"]
    reason: Literal["success", "voicemail"]
    started_at: int = Field(default=None, alias="startedAt")
    call_duration: int = Field(default=None, alias="callDuration")
    input: Optional[str] = None
    transferred: bool
    transfer: Optional[Transfer] = None


class CallFailedEventData(BaseCallEventData):
    """Model representing the data for a failed call event."""
    status: Literal["failed"]
    reason: Literal["busy", "no-answer", "rejected"]
    details: str
    started_at: int = Field(alias="startedAt")
    call_duration: int = Field(alias="callDuration", default=0)


class CallAttempt(BaseModel):
    """Model representing a single call attempt within a broadcast campaign."""
    call_id: str = Field(alias="callId")
    attempt_order: int = Field(alias="attemptOrder")
    status: Literal["delivered", "failed"]
    reason: str
    scheduled_at: int = Field(alias="scheduledAt")
    call_at: int = Field(alias="callAt")
    duration: int


class CallRecipientCompletedEventData(BaseModel):
    """Model representing the data for a recipient completion event in a broadcast campaign."""
    broadcast_id: str = Field(alias="broadcastId")
    recipient_id: str = Field(alias="recipientId")
    contact_id: str = Field(alias="contactId")
    phone: str
    attempts: int
    completed: bool
    status: Literal["delivered", "failed"]
    input: Optional[str] = None
    transferred: bool
    last_updated_at: int = Field(alias="lastUpdatedAt")
    calls: List[CallAttempt]


class CallWebhookEvent(BaseModel):
    """Model representing a call webhook event."""
    event_id: str = Field(alias="eventId")
    event_name: Literal["call.delivered.v1", "call.failed.v1", "call.recipient-completed.v1"]
    event_timestamp: int = Field(alias="eventTimestamp")
    event_webhook_id: str = Field(alias="eventWebhookId")
    event_data: Union[
        CallDeliveredEventData,
        CallFailedEventData,
        CallRecipientCompletedEventData
    ] = Field(alias="eventData")


# Type aliases for documentation
CallDeliveredWebhookEvent = CallWebhookEvent
CallFailedWebhookEvent = CallWebhookEvent
CallRecipientCompletedWebhookEvent = CallWebhookEvent
