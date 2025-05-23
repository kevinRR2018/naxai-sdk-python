# Models Reference

The Naxai SDK uses Pydantic models for data validation and serialization. This section provides detailed documentation for all models used in the SDK.

## Common Features

All models in the SDK:
- Inherit from `pydantic.BaseModel`
- Support both snake_case and camelCase field names through field aliases
- Provide automatic validation and type checking
- Include JSON serialization/deserialization
- Support optional fields with default values
- Use type hints for better IDE support

## Model Categories

### [Voice Models](./voice.md)
Models for voice calls, broadcasts, and reporting:
- Call flow configuration (VoiceFlow, Welcome, Menu, Transfer)
- Broadcast campaign management
- Activity logs and metrics
- Reporting and statistics

### [SMS Models](./sms.md)
Models for SMS messaging and reporting:
- Message sending and tracking
- Activity logs with detailed status information
- Comprehensive metrics (outgoing, incoming, country-based)
- Delivery error tracking

### [Email Models](./email.md)
Models for email operations and analytics:
- Transactional email composition
- Recipient management (To, CC, BCC)
- Activity tracking and metrics
- URL click tracking and engagement analytics

### [People Models](./people.md)
Models for contact and segment management:
- Contact information and preferences
- Segment definition and tracking
- Advanced search conditions
- Attribute management

### [Calendar Models](./calendars.md)
Models for managing business hours and schedules:
- Calendar configuration with timezone support
- Daily schedule management
- Exclusion date handling
- Availability checking

### [Webhook Models](./webhooks.md)
Models for webhook configuration and events:
- Multiple authentication methods (None, Basic, OAuth2, Header)
- Event filtering and routing
- Event tracking and history
- JSON Patch operations for updates

## Using Models

### Basic Usage

```python
from naxai.models.email import SendTransactionalEmailRequest, SenderObject, DestinationObject

# Create model instances
request = SendTransactionalEmailRequest(
    sender=SenderObject(
        email="sender@domain.com",
        name="Sender Name"
    ),
    to=[
        DestinationObject(
            email="recipient@domain.com",
            name="Recipient Name"
        )
    ],
    subject="Hello",
    html="<p>Hello World!</p>",
    text="Hello World!"
)

# Use in API calls
response = client.email.transactional.send(request)
```

### Model Validation

Models automatically validate data:
```python
from naxai.models.calendars import Calendar, ScheduleObject

# This will validate the schedule format and timezone
calendar = Calendar(
    name="Business Hours",
    timezone="America/New_York",
    schedule=[
        ScheduleObject(
            day=1,  # Monday
            open=True,
            start="09:00",
            stop="17:00",
            extended=False,
            extension_start="",
            extension_stop=""
        )
        # ... other days required
    ]
)
```

### JSON Serialization

Models support JSON operations with proper field mapping:
```python
# To JSON with camelCase fields
json_data = calendar.model_dump_json(by_alias=True)

# From JSON with either camelCase or snake_case
calendar = Calendar.model_validate_json(json_data)
```

## Best Practices

1. Always use the appropriate model for your use case
2. Take advantage of type hints and validation
3. Handle optional fields appropriately
4. Use the model's built-in methods for data conversion
5. Follow the examples in each model's documentation

## Related Documentation

For detailed documentation of each model category, see the specific pages linked above. Each page includes:
- Complete model definitions
- Field descriptions and types
- Usage examples
- Best practices
- Related API documentation 