# Webhook Models

This page documents the models used in the Webhooks API of the Naxai SDK.

## Webhook Models

### BaseWebhookModel
Base model for webhook configuration.

```python
class BaseWebhookModel(BaseModel):
    url: str                # Webhook endpoint URL
    events: List[str]      # Event types to subscribe to
    description: Optional[str] = None  # Webhook description
    secret: Optional[str] = None  # Signing secret
    metadata: Optional[Dict[str, Any]] = None  # Custom metadata
    active: Optional[bool] = True  # Whether webhook is active
```

### CreateWebhookRequest
Model for creating new webhooks.

```python
class CreateWebhookRequest(BaseWebhookModel):
    pass  # Inherits all fields from BaseWebhookModel
```

### UpdateWebhookRequest
Model for updating existing webhooks.

```python
class UpdateWebhookRequest(BaseModel):
    url: Optional[str] = None
    events: Optional[List[str]] = None
    description: Optional[str] = None
    secret: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    active: Optional[bool] = None
```

### WebhookResponse
Response model for webhook operations.

```python
class WebhookResponse(BaseWebhookModel):
    webhook_id: str        # Unique webhook identifier
    created_at: int       # Creation timestamp
    updated_at: int       # Last update timestamp
    last_error: Optional[str] = None  # Last delivery error
```

Example:
```python
# Creating a new webhook
webhook = CreateWebhookRequest(
    url="https://api.your-domain.com/webhooks",
    events=[
        "voice.call.ended",
        "sms.message.delivered",
        "email.opened"
    ],
    description="Production notifications endpoint",
    secret="your-webhook-secret",
    metadata={
        "environment": "production",
        "team": "communications"
    }
)
```

## Event Models

### BaseEventModel
Base model for webhook events.

```python
class BaseEventModel(BaseModel):
    id: str               # Event identifier
    type: str            # Event type
    created_at: int      # Event timestamp
    data: Dict[str, Any]  # Event-specific data
```

### VoiceEventData
Model for voice call events.

```python
class VoiceEventData(BaseModel):
    call_id: str          # Call identifier
    duration: Optional[int] = None  # Call duration in seconds
    from_: str           # Caller number
    to: str             # Recipient number
    status: str         # Call status
    direction: str      # Call direction
    recording_url: Optional[str] = None  # Recording URL if available
```

### EmailEventData
Model for email events.

```python
class EmailEventData(BaseModel):
    message_id: str       # Message identifier
    recipient: str       # Recipient email
    subject: str        # Email subject
    opened_at: Optional[int] = None  # Open timestamp
    clicked_at: Optional[int] = None  # Click timestamp
    user_agent: Optional[str] = None  # User agent string
    ip_address: Optional[str] = None  # IP address
```

### SMSEventData
Model for SMS events.

```python
class SMSEventData(BaseModel):
    message_id: str       # Message identifier
    from_: str          # Sender number
    to: str            # Recipient number
    status: str        # Message status
    error_code: Optional[str] = None  # Error code if failed
    delivered_at: Optional[int] = None  # Delivery timestamp
```

### ContactEventData
Model for contact events.

```python
class ContactEventData(BaseModel):
    contact_id: str      # Contact identifier
    email: Optional[str] = None  # Contact email
    phone: Optional[str] = None  # Contact phone
    changes: Optional[Dict[str, Any]] = None  # Changed fields
    group_id: Optional[str] = None  # Group identifier
```

Example:
```python
# Processing different event types
def handle_event(event: BaseEventModel):
    if event.type.startswith("voice."):
        data = VoiceEventData(**event.data)
        process_voice_event(data)
    elif event.type.startswith("email."):
        data = EmailEventData(**event.data)
        process_email_event(data)
    elif event.type.startswith("sms."):
        data = SMSEventData(**event.data)
        process_sms_event(data)
    elif event.type.startswith("contact."):
        data = ContactEventData(**event.data)
        process_contact_event(data)
```

## Test Models

### WebhookTestRequest
Model for testing webhooks.

```python
class WebhookTestRequest(BaseModel):
    event_type: str      # Event type to simulate
    custom_data: Optional[Dict[str, Any]] = None  # Custom event data
```

### WebhookTestResponse
Response model for test events.

```python
class WebhookTestResponse(BaseModel):
    success: bool       # Whether test was successful
    delivery_id: str   # Test delivery identifier
    timestamp: int     # Delivery timestamp
```

## Constants

### Event Types
```python
EVENT_TYPES = Literal[
    # Voice Events
    "voice.call.queued",
    "voice.call.started",
    "voice.call.answered",
    "voice.call.ended",
    "voice.call.failed",
    "voice.broadcast.started",
    "voice.broadcast.completed",
    "voice.broadcast.failed",
    
    # SMS Events
    "sms.message.sent",
    "sms.message.delivered",
    "sms.message.failed",
    "sms.message.received",
    "sms.opt_out",
    
    # Email Events
    "email.sent",
    "email.delivered",
    "email.opened",
    "email.clicked",
    "email.bounced",
    "email.complained",
    "email.unsubscribed",
    
    # Contact Events
    "contact.created",
    "contact.updated",
    "contact.deleted",
    "contact.preferences_updated",
    "contact.group_added",
    "contact.group_removed"
]
```

## Best Practices

1. **Model Validation**
   - Validate webhook URLs
   - Verify event types
   - Check required fields

2. **Error Handling**
   - Handle validation errors
   - Process unknown events gracefully
   - Log validation failures

3. **Security**
   - Validate webhook secrets
   - Verify signatures
   - Handle sensitive data

Example with best practices:
```python
from urllib.parse import urlparse
from typing import List

def validate_webhook_url(url: str) -> bool:
    """Validate webhook URL."""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ["http", "https"],
                   parsed.netloc])
    except Exception:
        return False

def validate_event_types(events: List[str]) -> bool:
    """Validate event types."""
    return all(event in EVENT_TYPES.__args__ for event in events)

try:
    # Create webhook with validation
    webhook = CreateWebhookRequest(
        url=url if validate_webhook_url(url) else None,
        events=events if validate_event_types(events) else None,
        secret=generate_secure_secret(),
        metadata={"validated_at": int(time.time() * 1000)}
    )
    response = client.webhooks.create(data=webhook)
    
    # Set up monitoring
    monitor_webhook_health(response.webhook_id)
except ValidationError as e:
    logger.error(f"Invalid webhook data: {e}")
    # Handle validation error
except Exception as e:
    logger.error(f"Failed to create webhook: {e}")
    # Handle other errors
```

## Related Documentation

- [Webhooks API Reference](../api/webhooks.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 