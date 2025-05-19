"""
Models for handling SMS-related webhook events.

This module defines the data models for various SMS events, including:
- Base SMS event data
- Incoming SMS events 
- SMS status events

Each model uses Pydantic for data validation and serialization, with proper field aliases
for JSON compatibility.
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field


class BaseSmsEventData(BaseModel):
    """Base model for all SMS event data."""
    message_id: str = Field(alias="messageId")
    reference: str
    encoding: Literal["text", "binary", "unicode"]
    from_: str = Field(alias="from")
    to: str
    mcc: str
    mnc: str
    message_parts: int = Field(alias="messageParts")


class SmsIncomingEventData(BaseSmsEventData):
    """Model representing the data for an incoming SMS event."""
    received_time: int = Field(alias="receivedTime")
    body: str  # At least one message part


class SmsStatusEventData(BaseSmsEventData):
    """Model representing the data for an SMS status event."""
    batch_id: Optional[str] = Field(default=None, alias="batchId")
    status_time: int = Field(alias="statusTime")
    status: str
    status_reason: str = Field(alias="statusReason")
    status_code: str = Field(alias="statusCode")


class SmsWebhookEvent(BaseModel):
    """Model representing an SMS webhook event."""
    event_id: str = Field(alias="eventId")
    event_name: Literal["sms.incoming.v1", "sms.status.v1"]
    event_timestamp: int = Field(alias="eventTimestamp")
    event_webhook_id: str = Field(alias="eventWebhookId")
    event_data: SmsIncomingEventData | SmsStatusEventData = Field(alias="eventData")


# Type aliases for documentation
SmsIncomingWebhookEvent = SmsWebhookEvent
SmsStatusWebhookEvent = SmsWebhookEvent
