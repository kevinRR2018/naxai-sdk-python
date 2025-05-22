# Voice Models

This page documents the models used in the Voice API of the Naxai SDK.

## Call Flow Models

### Welcome Model
Model for configuring the initial message of a call.

```python
class Welcome(BaseModel):
    say: Optional[str]  # Text to be spoken
    prompt: Optional[str]  # URL to audio file
```

Example:
```python
from naxai.models.voice import Welcome

welcome = Welcome(say="Welcome to our service!")
# Or with audio file
welcome = Welcome(prompt="https://example.com/welcome.wav")
```

### End Model
Model for configuring the final message of a call.

```python
class End(BaseModel):
    say: Optional[str]  # Text to be spoken
    prompt: Optional[str]  # URL to audio file
```

Example:
```python
from naxai.models.voice import End

end = End(say="Thank you for calling. Goodbye!")
```

## Call Types and Status

### Call Types
Available call types for classification:
```python
CALL_TYPES = Literal[
    "default",      # Standard call
    "marketing",    # Marketing campaign call
    "transactional",# Transaction-related call
    "otp",         # One-time password call
    "crisis"       # Emergency/crisis call
]
```

### Call Status Reasons
Possible call completion reasons:
```python
LITERAL_REASONS = Literal[
    "success",           # Call completed successfully
    "rejected",          # Call was rejected
    "busy",             # Recipient was busy
    "canceled-by-contact", # Recipient canceled
    "no-answer",        # No answer from recipient
    "canceled-by-user", # Canceled by API user
    "canceled-by-system", # System canceled
    "scheduled",        # Call is scheduled
    "inbound",          # Inbound call
    "voicemail"         # Reached voicemail
]
```

## Statistics Models

### BaseStatsFields
Base model for call statistics.

```python
class BaseStatsFields(BaseModel):
    date: Optional[str]  # ISO format (YYYY-MM-DD)
    calls: int          # Total calls count
    duration: int       # Total duration in seconds
```

Example:
```python
stats = client.voice.reporting.inbound.list()
for stat in stats:
    print(f"Date: {stat.date}")
    print(f"Total calls: {stat.calls}")
    print(f"Total duration: {stat.duration} seconds")
```

## Broadcast Models

### CreateBroadcastRequest
Model for creating a new broadcast campaign.

```python
class CreateBroadcastRequest(BaseModel):
    batch_id: str
    from_: str
    language: str
    welcome: Welcome
    segment_id: Optional[str]
    calendar_id: Optional[str]
    scheduled_at: Optional[int]
```

Example:
```python
from naxai.models.voice import CreateBroadcastRequest, Welcome

request = CreateBroadcastRequest(
    batch_id="batch_123",
    from_="1234567890",
    language="en-GB",
    welcome=Welcome(say="Welcome to our campaign!"),
    segment_id="segment_456",
    scheduled_at=1703066400000  # Unix timestamp in milliseconds
)

broadcast = client.voice.broadcasts.create(data=request)
```

## Best Practices

1. Always provide either `say` or `prompt` in Welcome/End models, not both
2. Use appropriate call types for better analytics and compliance
3. Monitor call statistics regularly using the BaseStatsFields model
4. Handle all possible call status reasons in your application logic

## Related Documentation

- [Voice API Reference](../api/voice.md)
- [Call Flow Guide](../guides/call-flow.md)
- [Broadcast Management](../guides/broadcasts.md) 