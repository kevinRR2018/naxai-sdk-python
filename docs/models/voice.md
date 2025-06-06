# Voice Models

This page documents the models used in the Voice API of the Naxai SDK.

## Call Flow Models

### VoiceFlow
Main model for configuring voice call interactions.

```python
class VoiceFlow(BaseModel):
    machine_detection: bool = False # Enable answering machine detection
    voicemail: Optional[VoiceMail]  # Message for answering machines
    welcome: Welcome                # Initial greeting configuration
    menu: Optional[Menu]            # Interactive menu configuration
    end: Optional[End]              # Call ending configuration
```

### Welcome
Model for initial greeting messages.

```python
class Welcome(BaseModel):
    say: Optional[str]          # Text to speak
    prompt: Optional[str]       # Audio file URL
    replay: Optional[int] = 0   # Number of replays
```

### Menu
Model for interactive voice menus.

```python
class Menu(BaseModel):
    say: Optional[str]          # Menu prompt text
    prompt: Optional[str]       # Menu prompt audio URL
    replay: Optional[int] = 0   # Replay count if no input
    choices: list[Choice]       # Available menu options
```

### Choice
Model for menu options.

```python
class Choice(BaseModel):
    key: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#"]
    say: Optional[str]              # Response text
    prompt: Optional[str]           # Response audio URL
    replay: Optional[int] = 0       # Replay count
    transfer: Optional[Transfer]    # Transfer configuration
```

### Transfer
Model for call transfers.

```python
class Transfer(BaseModel):
    destination: str            # Transfer phone number/SIP
    attempts: int = 1           # Number of attempts (1-3)
    timeout: int = 15           # Pickup timeout (5-30 seconds)
    whisper: Optional[Whisper]  # Message for recipient
```

### End
Model for call ending messages.

```python
class End(BaseModel):
    say: Optional[str]      # Ending text
    prompt: Optional[str]   # Ending audio URL
```

### VoiceMail
Model for voicemail messages.

```python
class VoiceMail(BaseModel):
    say: Optional[str]      # Voicemail text
    prompt: Optional[str]   # Voicemail audio URL
```

## Call Models

### CreateCallRequest
Model for initiating voice calls.

```python
class CreateCallRequest(BaseModel):
    batch_id: Optional[str]             # Batch identifier (max 64 chars)
    to: list[str]                       # Recipients (max 1000)
    from_: str                          # Sender number (8-15 chars)
    language: Literal["fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE"]
    voice: Literal["woman", "man"]
    idempotency_key: Optional[str]      # Duplicate prevention key
    calendar_id: Optional[str]          # Scheduling calendar
    scheduled_at: Optional[int]         # Schedule timestamp
    machine_detection: bool = False     # Detect answering machines
    voicemail: Optional[VoiceMail]      # Voicemail configuration
    welcome: Welcome                    # Initial greeting
    menu: Optional[Menu]                # Interactive menu
    end: Optional[End]                  # Ending message
```

### CreateCallResponse
Response model for call creation.

```python
class CreateCallResponse(BaseModel):
    batch_id: str           # Batch identifier
    count: int              # Number of calls
    calls: list[Call]       # Call references
```

### Call
Model for call references.

```python
class Call(BaseModel):
    call_id: str           # Call identifier
    to: str                # Recipient number
```

## Activity Log Models

### CallBaseModel
Base model for call details.

```python
class CallBaseModel(BaseModel):
    call_id: str
    from_: str
    to: str
    from_app: Optional[str]
    direction: Literal["outbound", "transfer", "inbound"]
    call_type: Literal["default", "marketing", "transactional", "otp", "crisis"]
    call_date: int
    status: Literal["delivered", "failed"]
    reason: Literal["success", "rejected", "busy", "canceled-by-contact",
                   "no-answer", "canceled-by-user", "canceled-by-system",
                   "scheduled", "inbound", "voicemail"]
    details: str
    input_: Optional[str]
    call_duration: int
    country: str
    network: Literal["landline", "mobile"]
    transferred: bool
    transfer_call_id: Optional[str]
    transfer_status: Optional[Literal["delivered", "failed"]]
    transfer_duration: Optional[int]
    transfer_reason: Optional[Literal["success", "busy", "no-answer", "rejected"]]
    transfer_details: Optional[str]
    transfer_attempts: Optional[int]
    client_id: Optional[str]
    campaign_id: Optional[str]
    broadcast_id: Optional[str]
```

### ListActivityLogsResponse
Model for paginated call logs.

```python
class ListActivityLogsResponse(BaseModel):
    pagination: Pagination
    items: list[CallBaseModel]
```

### GetActivityLogResponse
Model for single call log.

```python
class GetActivityLogResponse(CallBaseModel):
    # Inherits all fields from CallBaseModel
    pass
```

## Broadcast Models

### CreateBroadcastRequest
Model for creating voice broadcasts.

```python
class CreateBroadcastRequest(BaseModel):
    name: str
    from_: str                              # Sender number (8-15 chars)
    source: str = "people"                  # Contact source
    segment_ids: list[str]                  # Target segments (max 1)
    inclube_unsubscribed: bool = False      # Include unsubscribed
    language: Literal["fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE"] = "fr-BE"
    voice: Literal["woman", "man"] = "woman"
    scheduled_at: Optional[str]             # Schedule timestamp
    retries: int = 0                        # Retry attempts (0-3)
    retry_on_no_input: bool = False         # Retry on no input
    retry_on_failed: bool = False           # Retry on failure
    retry_delays: Optional[list[int]]       # Delay between retries
    calendar_id: Optional[str]              # Scheduling calendar
    distribution: Literal["none", "dynamic"] = "none"
    dynamic_name: Optional[str]             # Dynamic distribution name
    voice_flow: VoiceFlow                   # Call flow configuration
    actions: Optional[Actions]              # Response actions
```

### BroadcastStatusResponse
Model for broadcast status updates.

```python
class BroadcastStatusResponse(BaseModel):
    broadcast_id: str
    state: Literal["starting", "pausing", "resuming", "canceling"]
```

### GetBroadcastMetricsResponse
Model for broadcast metrics.

```python
class GetBroadcastMetricsResponse(BaseModel):
    total: int          # Total calls
    completed: int      # Completed calls
    delivered: int      # Delivered calls
    failed: int         # Failed calls
    canceled: int       # Canceled calls
    paused: int         # Paused calls
    invalid: int        # Invalid calls
    in_progress: int    # Active calls
    transferred: int    # Transferred calls
    calls: int          # Total attempts
```

## Reporting Models

### BaseStatsFields
Base model for call statistics.

```python
class BaseStatsFields(BaseModel):
    date: Optional[str] # ISO date (YYYY-MM-DD)
    calls: int          # Total calls
    duration: int       # Total duration (seconds)
```

### OutboundStatsFields
Model for outbound call statistics.

```python
class OutboundStatsFields(BaseStatsFields):
    delivered: int      # Delivered calls
    failed: int         # Failed calls
    no_answer: int      # Unanswered calls
    busy: int           # Busy signals
    rejected: int       # Rejected calls
    invalid: int        # Invalid numbers
    transferred: int    # Transferred calls
```

### InboundStats
Model for inbound call statistics.

```python
class InboundStats(BaseStatsFields):
    received: int      # Received calls
    transferred: int   # Transferred calls
```

### CountryStats
Model for country-based statistics.

```python
class CountryStats(OutboundStatsFields):
    country: str       # Country code
```

## Best Practices

1. **Call Flow Design**
   - Provide either `say` or `prompt` in voice components
   - Set appropriate replay counts for menus
   - Configure reasonable transfer timeouts
   - Handle answering machines appropriately

2. **Call Management**
   - Use batch_id for grouping related calls
   - Monitor call status through activity logs
   - Handle all possible call reasons
   - Track transfer success rates

3. **Broadcast Management**
   - Configure appropriate retry strategies
   - Monitor broadcast metrics
   - Use appropriate distribution strategies
   - Handle recipient responses

Example:
```python
# Create a voice call with menu
call_request = CreateCallRequest(
    to=["+1234567890"],
    from_="+0987654321",
    language="en-GB",
    voice="woman",
    welcome=Welcome(say="Welcome to our service"),
    menu=Menu(
        say="Press 1 for sales, 2 for support",
        choices=[
            Choice(key="1", transfer=Transfer(destination="+1111111111")),
            Choice(key="2", transfer=Transfer(destination="+2222222222"))
        ]
    ),
    end=End(say="Thank you for calling")
)

# Create a broadcast campaign
broadcast = CreateBroadcastRequest(
    name="Customer Survey",
    from_="+0987654321",
    segment_ids=["seg_123"],
    language="en-GB",
    retries=2,
    retry_delays=[300, 600],  # 5 and 10 minutes
    voice_flow=VoiceFlow(
        welcome=Welcome(say="Please take our survey"),
        menu=Menu(
            say="Press 1 for yes, 2 for no",
            choices=[
                Choice(key="1", say="Thank you for your positive response"),
                Choice(key="2", say="We appreciate your feedback")
            ]
        )
    )
)
```

## Related Documentation

- [Voice API Reference](../api/voice.md)
- [Call Flow Guide](../guides/call-flow.md)
- [Broadcast Management](../guides/broadcasts.md) 