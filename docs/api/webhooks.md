# Webhooks API Reference

The Webhooks API allows you to configure and manage real-time event notifications for your Naxai account.

## Webhook Resource

### Create Webhook
```python
client.webhooks.create(
    data: Union[dict, CreateWebhookRequest],
    # Required fields in data:
    # - url: str  # Endpoint URL to receive events
    # - events: List[str]  # List of event types to subscribe to
    #
    # Optional fields:
    # - description: str
    # - secret: str  # Secret for signature verification
    # - metadata: Dict[str, Any]
    # - active: bool = True
)
```

Example:
```python
response = client.webhooks.create(data={
    "url": "https://your-domain.com/webhooks/naxai",
    "events": [
        "voice.call.started",
        "voice.call.ended",
        "sms.message.delivered",
        "email.opened"
    ],
    "description": "Production webhook endpoint",
    "secret": "your-signing-secret",
    "metadata": {
        "environment": "production",
        "version": "1.0"
    }
})
print(f"Webhook ID: {response.webhook_id}")
```

### Update Webhook
```python
client.webhooks.update(
    webhook_id: str,
    data: Union[dict, UpdateWebhookRequest]
)
```

### Get Webhook
```python
client.webhooks.get(webhook_id: str)
```

### List Webhooks
```python
client.webhooks.list(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    active: Optional[bool] = None
)
```

### Delete Webhook
```python
client.webhooks.delete(webhook_id: str)
```

## Event Types

The following event types are available for subscription:

### Voice Events
- `voice.call.queued` - Call has been queued
- `voice.call.started` - Call has started
- `voice.call.answered` - Call was answered
- `voice.call.ended` - Call has ended
- `voice.call.failed` - Call failed
- `voice.broadcast.started` - Broadcast campaign started
- `voice.broadcast.completed` - Broadcast campaign completed
- `voice.broadcast.failed` - Broadcast campaign failed

### SMS Events
- `sms.message.sent` - Message has been sent
- `sms.message.delivered` - Message was delivered
- `sms.message.failed` - Message delivery failed
- `sms.message.received` - Inbound message received
- `sms.opt_out` - Contact opted out of messages

### Email Events
- `email.sent` - Email has been sent
- `email.delivered` - Email was delivered
- `email.opened` - Email was opened
- `email.clicked` - Email link was clicked
- `email.bounced` - Email bounced
- `email.complained` - Spam complaint received
- `email.unsubscribed` - Contact unsubscribed

### Contact Events
- `contact.created` - New contact created
- `contact.updated` - Contact details updated
- `contact.deleted` - Contact was deleted
- `contact.preferences_updated` - Contact preferences changed
- `contact.group_added` - Contact added to group
- `contact.group_removed` - Contact removed from group

## Webhook Delivery

### Retry Policy
Failed webhook deliveries are automatically retried with exponential backoff:
- 1st retry: 5 minutes
- 2nd retry: 15 minutes
- 3rd retry: 30 minutes
- 4th retry: 1 hour
- 5th retry: 2 hours

After 5 failed attempts, the webhook will be marked as failed and notifications will stop.

### Security

#### Signature Verification
Each webhook request includes a signature header for verification:
```python
from hmac import HMAC
from hashlib import sha256

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify the webhook signature."""
    expected = HMAC(
        key=secret.encode(),
        msg=payload,
        digestmod=sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)

# Example Flask webhook handler
@app.route("/webhooks/naxai", methods=["POST"])
def handle_webhook():
    payload = request.get_data()
    signature = request.headers.get("X-Naxai-Signature")
    
    if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
        return "Invalid signature", 401
        
    event = request.json
    # Process the event
    return "OK", 200
```

## Event Payloads

### Base Event Structure
All webhook events share this base structure:
```python
{
    "id": "evt_123abc",
    "type": "voice.call.started",
    "created_at": 1634567890000,
    "data": {
        # Event-specific data
    }
}
```

### Example Event Payloads

#### Voice Call Event
```python
{
    "id": "evt_123abc",
    "type": "voice.call.ended",
    "created_at": 1634567890000,
    "data": {
        "call_id": "call_456def",
        "duration": 120,
        "from": "+1234567890",
        "to": "+0987654321",
        "status": "completed",
        "direction": "outbound",
        "recording_url": "https://api.naxai.com/recordings/xyz"
    }
}
```

#### Email Event
```python
{
    "id": "evt_789ghi",
    "type": "email.opened",
    "created_at": 1634567890000,
    "data": {
        "message_id": "msg_456def",
        "recipient": "user@example.com",
        "subject": "Welcome to Naxai",
        "opened_at": 1634567890000,
        "user_agent": "Mozilla/5.0...",
        "ip_address": "192.0.2.1"
    }
}
```

## Testing Webhooks

### Send Test Event
```python
client.webhooks.test(
    webhook_id: str,
    event_type: str  # Event type to simulate
)
```

Example:
```python
# Send test event
response = client.webhooks.test(
    webhook_id="whk_123",
    event_type="email.opened"
)
```

## Best Practices

1. **Security**
   - Always verify webhook signatures
   - Use HTTPS endpoints
   - Rotate webhook secrets periodically

2. **Reliability**
   - Implement idempotency checks
   - Process events asynchronously
   - Store raw events before processing

3. **Performance**
   - Respond quickly (2xx) to webhook requests
   - Process events in background jobs
   - Monitor webhook health

4. **Error Handling**
   - Log failed deliveries
   - Set up monitoring alerts
   - Have a retry strategy

Example implementation:
```python
from flask import Flask, request
from hmac import HMAC
from hashlib import sha256
from typing import Dict
import json

app = Flask(__name__)

def process_event(event_data: Dict):
    """Process the webhook event asynchronously."""
    event_type = event_data["type"]
    
    if event_type.startswith("voice."):
        handle_voice_event(event_data)
    elif event_type.startswith("email."):
        handle_email_event(event_data)
    elif event_type.startswith("sms."):
        handle_sms_event(event_data)
    elif event_type.startswith("contact."):
        handle_contact_event(event_data)

@app.route("/webhooks/naxai", methods=["POST"])
def handle_webhook():
    payload = request.get_data()
    signature = request.headers.get("X-Naxai-Signature")
    
    # Verify signature
    if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
        return "Invalid signature", 401
    
    # Parse event
    try:
        event = request.json
        
        # Store raw event
        store_raw_event(event)
        
        # Process asynchronously
        process_event(event)
        
        return "OK", 200
    except Exception as e:
        logger.error(f"Failed to process webhook: {e}")
        return "Internal error", 500
```

## Related Documentation

- [Webhook Models](../models/webhooks.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 