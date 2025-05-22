# Models Reference

The Naxai SDK uses Pydantic models for data validation and serialization. This section provides detailed documentation for all models used in the SDK.

## Common Features

All models in the SDK:
- Inherit from `pydantic.BaseModel`
- Support both snake_case and camelCase field names
- Provide automatic validation and type checking
- Include JSON serialization/deserialization
- Support optional fields with default values

## Model Categories

### [Voice Models](./voice.md)
Models for voice calls, broadcasts, and reporting:
- Call configuration models (Welcome, End, Menu)
- Broadcast models
- Call statistics and metrics

### [SMS Models](./sms.md)
Models for SMS messaging and reporting:
- Message sending models
- Delivery status models
- SMS metrics and statistics

### [Email Models](./email.md)
Models for email operations and analytics:
- Email composition models
- Delivery tracking models
- Email engagement metrics

### [People Models](./people.md)
Models for contact and segment management:
- Contact models
- Segment models
- Search and filter conditions

### [Calendar Models](./calendars.md)
Models for managing business hours and schedules:
- Calendar configuration models
- Schedule models
- Holiday template models

### [Webhook Models](./webhooks.md)
Models for webhook configuration and events:
- Webhook configuration models
- Event type models
- Authentication models

## Using Models

### Basic Usage

```python
from naxai.models.voice import Welcome, End

# Create model instances
welcome = Welcome(say="Welcome message")
end = End(say="Goodbye message")

# Validate and use in API calls
response = client.voice.call.create(
    to=["1234567890"],
    welcome=welcome,
    end=end
)
```

### Model Validation

Models automatically validate data:
```python
from naxai.models.people import ContactBaseModel

# This will raise a validation error if email is invalid
contact = ContactBaseModel(
    nx_id="contact_123",
    email="invalid-email",  # Will raise ValidationError
    phone="+1234567890"
)
```

### JSON Serialization

Models can be easily converted to/from JSON:
```python
contact_dict = contact.model_dump()  # To dict
contact_json = contact.model_dump_json()  # To JSON string

# From dict/JSON
contact = ContactBaseModel.model_validate(contact_dict)
```

## Detailed Documentation

For detailed documentation of each model, see the specific model category pages linked above, or use Python's built-in help:

```python
from naxai.models.people import ContactBaseModel
help(ContactBaseModel)
``` 