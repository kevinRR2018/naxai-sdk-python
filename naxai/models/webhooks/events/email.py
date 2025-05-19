"""
Models for handling email-related webhook events.

This module defines the data models for various email events, including:
- Base email event data
- Email sent events
- Email delivery events
- Email failure events
- Email tracking events (opens, clicks)
- Email complaint events
- Email unsubscribe events

Each model uses Pydantic for data validation and serialization, with proper field aliases
for JSON compatibility.
"""
from typing import Literal, Union
from pydantic import BaseModel, Field


class BaseEmailEventData(BaseModel):
    """Base model for all email event data."""
    message_id: str = Field(alias="messageId")
    email: str
    subject: str
    timestamp: int


class EmailSentEventData(BaseEmailEventData):
    """Model representing the data for an email sent event."""


class EmailDeliveredEventData(BaseEmailEventData):
    """Model representing the data for an email delivered event."""


class EmailFailedEventData(BaseEmailEventData):
    """Model representing the data for an email failed event."""
    reason: str
    error_code: str = Field(alias="errorCode")
    error_details: str = Field(alias="errorDetails")


class BaseEmailTrackingEventData(BaseEmailEventData):
    """Base model for email tracking events (opened, clicked)."""
    user_agent: str = Field(alias="userAgent")
    ip: str


class EmailOpenedEventData(BaseEmailTrackingEventData):
    """Model representing the data for an email opened event."""


class EmailClickedEventData(BaseEmailTrackingEventData):
    """Model representing the data for an email clicked event."""
    link_url: str = Field(alias="linkUrl")


class EmailComplainedEventData(BaseEmailEventData):
    """Model representing the data for an email complained event."""


class EmailUnsubscribedEventData(BaseEmailEventData):
    """Model representing the data for an email unsubscribed event."""


class EmailWebhookEvent(BaseModel):
    """Model representing an email webhook event."""
    event_id: str = Field(alias="eventId")
    event_name: Literal["email.sent.v1", "email.delivered.v1", "email.failed.v1",
                       "email.clicked.v1", "email.opened.v1", "email.complained.v1",
                       "email.unsubscribed.v1"]
    event_timestamp: int = Field(alias="eventTimestamp")
    event_webhook_id: str = Field(alias="eventWebhookId")
    event_data: Union[
        EmailSentEventData,
        EmailDeliveredEventData,
        EmailFailedEventData,
        EmailClickedEventData,
        EmailOpenedEventData,
        EmailComplainedEventData,
        EmailUnsubscribedEventData
    ] = Field(alias="eventData")


# Type aliases for documentation
EmailSentWebhookEvent = EmailWebhookEvent
EmailDeliveredWebhookEvent = EmailWebhookEvent
EmailFailedWebhookEvent = EmailWebhookEvent
EmailClickedWebhookEvent = EmailWebhookEvent
EmailOpenedWebhookEvent = EmailWebhookEvent
EmailComplainedWebhookEvent = EmailWebhookEvent
EmailUnsubscribedWebhookEvent = EmailWebhookEvent
