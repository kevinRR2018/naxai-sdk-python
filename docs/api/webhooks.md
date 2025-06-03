# Webhooks API Reference

The Webhooks API allows you to configure and manage real-time event notifications for your Naxai account. Webhooks enable your application to receive push notifications for various events rather than polling the API.

## Webhook Resource

### Create Webhook
```python
client.webhooks.create(
    name: str,                # Descriptive name for the webhook
    url: str,                # Endpoint URL to receive events
    authentication: Union[    # Authentication configuration
        NoAuthModel,         # No authentication
        BasicAuthModel,      # Basic HTTP authentication
        OAuth2AuthModel,     # OAuth 2.0
        HeaderAuthModel      # Custom header authentication
    ],
    event_object: Literal[   # Event category to subscribe to
        "All",              # All events
        "People",           # Contact-related events
        "Sms",             # SMS-related events
        "Email",           # Email-related events
        "Call"             # Voice call events
    ],
    event_filter: List[str], # Additional filtering criteria
    event_names: List[str],  # Specific event names to subscribe to
    active: bool = True      # Whether webhook is active upon creation
)
```

Request: [CreateWebhookRequest](../models/webhooks.md#createwebhookrequest)  
Returns: [WebhookBaseModel](../models/webhooks.md#webhookbasemodel)

Example:
```python
from naxai.models.webhooks.helper_models.authentication import NoAuthModel

    # Create webhook with basic authentication
    response = client.webhooks.create(
        name="Production Notifications",
        url="https://your-domain.com/webhooks/naxai",
        authentication=NoAuthModel(),
        event_object="Sms",
        event_filter=["*"],  # Accept all events in category
        event_names=[
            "sms.incoming.v1",
            "sms.status.v1"
        ],
        active=False
    )
    print(f"Created webhook: {response.id}")
```

### Update Webhook
```python
client.webhooks.update(
    webhook_id: str,
    update_operations: List[Union[
        UpdateWebhookJsonPathRequestAddReplace,  # Add or replace fields
        UpdateWebhookJsonPathRequestMoveCopy,    # Move or copy fields
        UpdateWebhookJsonPathRequestRemove       # Remove fields
    ]]
)
```

Request Models:
- [UpdateWebhookJsonPathRequestAddReplace](../models/webhooks.md#updatewebhookjsonpathrequestaddreplace)
- [UpdateWebhookJsonPathRequestMoveCopy](../models/webhooks.md#updatewebhookjsonpathrequestmovecopy)
- [UpdateWebhookJsonPathRequestRemove](../models/webhooks.md#updatewebhookjsonpathrequestremove)

Returns: [WebhookBaseModel](../models/webhooks.md#webhookbasemodel)

The update method uses JSON Patch operations (RFC 6902) to modify webhook configurations:

```python
from naxai.models.webhooks.requests.webhooks_requests import (
    UpdateWebhookJsonPathRequestAddReplace
)

# Update webhook URL and remove a field
        updates = [
            UpdateWebhookJsonPathRequestAddReplace(
                path="/url",
                value="https://new-endpoint.example.com/webhooks"
            )
        ]

        updated = client.webhooks.update("992cbf38-53ce-415f-8479-d440775315bd", updates)
```

### Get Webhook
```python
client.webhooks.get(webhook_id: str)
```

Returns: [WebhookBaseModel](../models/webhooks.md#webhookbasemodel)

Example:
```python
webhook = client.webhooks.get("whk_123")
print(f"Webhook: {webhook.name}")
print(f"URL: {webhook.url}")
print(f"Active: {webhook.active}")
print(f"Event names: {webhook.event_names}")
```

### List Webhooks
```python
client.webhooks.list()
```

Returns: [ListWebhooksResponse](../models/webhooks.md#listwebhooksresponse)

Example:
```python
webhooks = client.webhooks.list()
for webhook in webhooks:
    print(f"Webhook: {webhook.name} ({webhook.id})")
    print(f"Event object: {webhook.event_object}")
    print(f"Active: {webhook.active}")
```

### Delete Webhook
```python
client.webhooks.delete(webhook_id: str)
```

Returns: None

## Event Management

### List Available Events
```python
client.webhooks.list_events()
```

Returns: [ListEventTypesResponse](../models/webhooks.md#listeventtypesresponse)

### List Recent Events
```python
client.webhooks.list_last_events(webhook_id: str)
```

Returns: [ListLastWebhookEventsResponse](../models/webhooks.md#listlastwebhookeventsresponse)

Example:
```python
events = client.webhooks.list_last_events("whk_123")
for event in events:
    print(f"Event: {event.event_name}")
    print(f"Timestamp: {event.event_timestamp}")
    print(f"Data: {event.event_data}")
```

## Event Types

Available event categories and their associated events:

### Voice Events (`event_object="Call"`)
- `call.delivered.v1` - Call has been delivered
- `call.failed.v1` - Call has failed
- `call.recipient-completed.v1` - When a recipient of broadcast was completed.


### SMS Events (`event_object="Sms"`)
- `sms.incoming.v1` - Inbound message received
- `sms.status.v1` - Status for message received

### Email Events (`event_object="Email"`)
- `email.sent.v1` - Email has been sent
- `email.delivered.v1` - Email was delivered
- `email.failed.v1` - Email was bounced
- `email.opened.v1` - Email was opened
- `email.clicked.v1` - Email link was clicked
- `email.bounced` - Email bounced
- `email.complained.v1` - Spam complaint received
- `email.unsubscribed.v1` - Contact unsubscribed

### Contact Events (`event_object="People"`)
No events for the moment

## Authentication Methods

### No Authentication
```python
from naxai.models.webhooks.helper_models.authentication import NoAuthModel

auth = NoAuthModel()
```

### Basic Authentication
```python
from naxai.models.webhooks.helper_models.authentication import BasicAuthModel

auth = BasicAuthModel(
    username="webhook_user",
    password="webhook_password"
)
```

### OAuth 2.0
```python
from naxai.models.webhooks.helper_models.authentication import OAuth2AuthModel

auth = OAuth2AuthModel(
    token_url="https://auth.example.com/token",
    client_id="client_123",
    client_secret="secret_456",
    scope=["webhook.read", "webhook.write"]
)
```

### Custom Header
```python
from naxai.models.webhooks.helper_models.authentication import HeaderAuthModel

auth = HeaderAuthModel(
    header_name="X-API-Key",
    header_value="your-api-key"
)
```

## Event Payloads

All webhook events share this base structure:
```python
{
    "event_name": str,           # Name of the event (e.g., "sms.message.delivered")
    "event_webhook_id": str,     # ID of the receiving webhook
    "event_timestamp": int,      # When the event occurred (milliseconds)
    "event_id": str,            # Unique event identifier
    "event_data": dict          # Event-specific payload data
}
```

## Best Practices

1. **Security**
   - Use HTTPS endpoints only
   - Implement authentication
   - Validate webhook signatures
   - Keep authentication credentials secure

2. **Reliability**
   - Respond quickly to webhook requests (2xx)
   - Process events asynchronously
   - Implement idempotency checks
   - Store raw events before processing

3. **Event Handling**
   - Subscribe only to needed events
   - Use appropriate event filters
   - Handle events idempotently
   - Process events in order

4. **Error Handling**
   - Implement proper error handling
   - Log failed webhook deliveries
   - Monitor webhook health
   - Set up failure alerts

## Related Documentation

- [Webhook Models](../models/webhooks.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 