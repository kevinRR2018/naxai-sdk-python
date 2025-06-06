# Webhook Models

This page documents the models used in the Webhooks API of the Naxai SDK.

## Authentication Models

### NoAuthModel
Model for webhooks that don't require authentication.

```python
class NoAuthModel(BaseModel):
    type_: str = "none"  # Authentication type, always "none"
```

### BasicAuthModel
Model for webhooks using HTTP Basic Authentication.

```python
class BasicAuthModel(BaseModel):
    type_: str = "basic"    # Authentication type, always "basic"
    user: str               # Username for basic auth
    password: str           # Password for basic auth
```

### OAuth2AuthModel
Model for webhooks using OAuth2 authentication.

```python
class OAuth2AuthModel(BaseModel):
    type_: str = "oauth2"   # Authentication type, always "oauth2"
    client_id: str          # OAuth2 client ID
    auth_url: str           # OAuth2 authorization URL
```

### HeaderAuthModel
Model for webhooks using custom header authentication.

```python
class HeaderAuthModel(BaseModel):
    type_: str = "header"   # Authentication type, always "header"
    header_key: str         # Custom header key name
```

## Request Models

### CreateWebhookRequest
Model for creating new webhooks.

```python
class CreateWebhookRequest(BaseModel):
    name: str                                                       # Descriptive name for the webhook
    url: str                                                        # Endpoint URL where events will be sent
    authentication: Union[
        NoAuthModel,
        BasicAuthModel,
        OAuth2AuthModel,
        HeaderAuthModel
    ] = None                                                        # Authentication configuration
    active: bool = True                                             # Whether webhook should be active
    event_object: Literal["All", "People", "Sms", "Call", "Email"]  # Object type for events
    event_filter: list[str]                                         # Additional filtering criteria
    event_names: list[str]                                          # Specific event names to subscribe to
```

### JSON Patch Operation Models
Models for updating webhooks using JSON Patch (RFC 6902).

```python
class UpdateWebhookJsonPathRequestRemove(BaseModel):
    path: str                # JSON path to remove
    op: Literal["remove"]    # Operation type

class UpdateWebhookJsonPathRequestAddReplace(BaseModel):
    path: str           # JSON path to modify
    value: str          # New value to set

class UpdateWebhookJsonPathRequestMoveCopy(BaseModel):
    path: str                   # JSON path destination
    op: Literal["move", "copy"] # Operation type
```

## Response Models

### WebhookBaseModel
Base model for webhook configurations.

```python
class WebhookBaseModel(BaseModel):
    id: str                                                                     # Unique webhook identifier
    name: str                                                                   # Descriptive name
    url: str                                                                    # Endpoint URL
    authentication: Union[
        NoAuthModel,
        BasicAuthModel,
        OAuth2AuthModel,
        HeaderAuthModel
    ] = None                                                                    # Authentication configuration
    active: bool = True                                                         # Whether webhook is active
    event_object: Literal["All", "People", "Sms", "Call", "Email", "Survey"]
    event_filter: list[str]                                                     # Event filtering criteria
    event_names: list[str]                                                      # Subscribed event names
    modified_at: Optional[int]                                                  # Last modification timestamp
    modified_by: Optional[str]                                                  # Last modifier identifier
```

### ListWebhooksResponse
Response model for listing webhooks.

```python
class ListWebhooksResponse(BaseModel):
    root: list[WebhookBaseModel]  # List of webhook configurations
```

### Event Models

#### EventDataBaseModel
Base model for webhook event data.

```python
class EventDataBaseModel(BaseModel):
    # Flexible model that allows additional fields
    model_config = {"extra": "allow"}
```

#### EventsBaseModel
Model for webhook events.

```python
class EventsBaseModel(BaseModel):
    event_name: Optional[str]                   # Event name
    event_webhook_id: Optional[str]             # Webhook ID
    event_timestamp: Optional[int]              # Event timestamp
    event_id: Optional[str]                     # Unique event ID
    event_data: Optional[EventDataBaseModel]    # Event payload
```

### ListLastWebhookEventsResponse
Response model for listing recent webhook events.

```python
class ListLastWebhookEventsResponse(BaseModel):
    root: list[EventsBaseModel]  # List of webhook events
```

### ListEventTypesResponse
Response model for available event types.

```python
class ListEventTypesResponse(BaseModel):
    events: list[str]  # List of available event type names
```

## Best Practices

1. **Authentication**
   - Choose the appropriate authentication method for your endpoint
   - Keep authentication credentials secure
   - Use OAuth2 for more complex authentication flows
   - Use header authentication for custom token schemes

2. **Event Handling**
   - Subscribe to specific event types using event_names
   - Use event_filter for additional filtering
   - Process events asynchronously
   - Implement proper error handling

3. **Webhook Management**
   - Use descriptive names for webhooks
   - Monitor webhook activity through events
   - Keep track of modifications using modified_at and modified_by
   - Maintain webhook status using the active flag

Example:
```python
# Create a webhook with basic authentication
webhook = CreateWebhookRequest(
    name="Customer Updates Endpoint",
    url="https://api.your-domain.com/webhooks",
    authentication=BasicAuthModel(
        user="webhook_user",
        password="3x@mo"
    ),
    event_object="People",
    event_filter=["status_change", "group_update"],
    event_names=[
        "contact.created",
        "contact.updated",
        "contact.deleted"
    ]
)

# Create a webhook with OAuth2
oauth_webhook = CreateWebhookRequest(
    name="Secure Integration Endpoint",
    url="https://secure-api.domain.com/hooks",
    authentication=OAuth2AuthModel(
        client_id="client_123",
        auth_url="https://auth.domain.com/oauth2"
    ),
    event_object="All",
    event_filter=[],
    event_names=["*"]  # Subscribe to all events
)
```

## Related Documentation

- [Webhooks API Reference](../api/webhooks.md)
- [Event Types Reference](../guides/event-types.md)
- [Security Best Practices](../guides/security.md) 