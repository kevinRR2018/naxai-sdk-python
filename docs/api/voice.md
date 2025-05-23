# Voice API Reference

The Voice API allows you to make calls, manage broadcasts, and access call reporting features.

## Call Resource

### Create a Call
```python
client.voice.call.create(
    welcome: Welcome,                           # Welcome message configuration
    language: Literal["fr-BE", "fr-FR", "nl-BE", "nl-NL", "en-GB", "de-DE"],  # Voice language
    to: list[str] = Field(min_length=1, max_length=1000),  # List of recipient phone numbers
    from_: str = Field(min_length=8, max_length=15),  # Sender phone number
    batch_id: Optional[str] = Field(max_length=64),  # Batch identifier
    voice: Optional[Literal["man", "woman"]] = "woman",  # Voice type
    idempotency_key: Optional[str] = Field(max_length=128, min_length=1),  # Prevent duplicates
    calendar_id: Optional[str] = Field(max_length=64),  # Calendar for scheduling
    language: Literal["fr-BE", "fr-FR", "nl-BE", "nl-NL", "en-GB", "de-DE"],  # Voice language
    to: list[str] = Field(min_length=1, max_length=1000),  # List of recipient phone numbers
    from_: str = Field(min_length=8, max_length=15),  # Sender phone number
    batch_id: Optional[str] = Field(max_length=64),  # Batch identifier
    voice: Optional[Literal["man", "woman"]] = "woman",  # Voice type
    idempotency_key: Optional[str] = Field(max_length=128, min_length=1),  # Prevent duplicates
    calendar_id: Optional[str] = Field(max_length=64),  # Calendar for scheduling
    scheduled_at: Optional[int] = None,         # Schedule timestamp
    machine_detection: Optional[bool] = False,  # Enable answering machine detection
    voicemail: Optional[VoiceMail] = None,     # Voicemail configuration
    menu: Optional[Menu] = None,               # Interactive menu configuration
    end: Optional[End] = None                  # End message configuration
)
```

Request Models:
- [Welcome](../models/voice.md#welcome)
- [VoiceMail](../models/voice.md#voicemail)
- [Menu](../models/voice.md#menu)
- [End](../models/voice.md#end)

Returns: [CreateCallResponse](../models/voice.md#createcallresponse)

Example:
```python
response = client.voice.call.create(
    welcome={"say": "Hello!"},
    language="en-GB",
    to=["1234567890"],
    from_="0987654321",
    voice="woman",
    end={"say": "Goodbye!"}
)
print(f"Call ID: {response.calls[0].call_id}")
```

## Broadcasts Resource

### Create a Broadcast
```python
client.voice.broadcasts.create(data: CreateBroadcastRequest)
```

Request: [CreateBroadcastRequest](../models/voice.md#createbroadcastrequest)  
Returns: [BroadcastStatusResponse](../models/voice.md#broadcaststatusresponse)

### List Broadcasts
```python
client.voice.broadcasts.list()
```

Returns: [ListBroadcastsResponse](../models/voice.md#listbroadcastsresponse)

### Get Broadcast Details
```python
client.voice.broadcasts.get(broadcast_id: str)
```

Returns: [GetBroadcastResponse](../models/voice.md#getbroadcastresponse)

### Update a Broadcast
```python
client.voice.broadcasts.update(
    broadcast_id: str,
    data: CreateBroadcastRequest
)
```

Request: [CreateBroadcastRequest](../models/voice.md#createbroadcastrequest)  
Returns: [BroadcastStatusResponse](../models/voice.md#broadcaststatusresponse)

### Control Broadcast
```python
# Start broadcast
client.voice.broadcasts.start(broadcast_id: str)

# Pause broadcast
client.voice.broadcasts.pause(broadcast_id: str)

# Resume broadcast
client.voice.broadcasts.resume(broadcast_id: str)

# Cancel broadcast
client.voice.broadcasts.cancel(broadcast_id: str)

# Delete broadcast
client.voice.broadcasts.delete(broadcast_id: str)
```

All control operations return: [BroadcastStatusResponse](../models/voice.md#broadcaststatusresponse)

## Broadcast Metrics

### Get Metrics
```python
client.voice.broadcasts.metrics.get(broadcast_id: str)
```

Returns: [GetBroadcastMetricsResponse](../models/voice.md#getbroadcastmetricsresponse)

### Get Input Metrics
```python
client.voice.broadcasts.metrics.input.get(broadcast_id: str)
```

Returns: [GetBroadcastInputMetricsResponse](../models/voice.md#getbroadcastinputmetricsresponse)

## Recipients Resource

### List Recipients
```python
client.voice.broadcasts.recipients.list(
    broadcast_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    phone: Optional[str] = None,
    completed: Optional[bool] = None,
    status: Optional[str] = None
)
```

Returns: [ListBroadcastRecipientsResponse](../models/voice.md#listbroadcastrecipientsresponse)

### Get Recipient Details
```python
client.voice.broadcasts.recipients.get(
    broadcast_id: str,
    recipient_id: str
)
```

Returns: [GetBroadcastRecipientResponse](../models/voice.md#getbroadcastrecipientresponse)

### List Recipient Calls
```python
client.voice.broadcasts.recipients.calls.list(
    broadcast_id: str,
    recipient_id: str
)
```

Returns: [ListBroadcastRecipientCallsResponse](../models/voice.md#listbroadcastrecipientcallsresponse)

## Reporting Resource

### Inbound Metrics
```python
client.voice.reporting.inbound.list(
    group: Literal["hour", "day", "month"],     # Time interval grouping
    start_date: Optional[str] = None,           # Start date for filtering
    stop_date: Optional[str] = None,            # End date for filtering
    number: Optional[str] = None                # Filter by phone number
)
```

Notes:
- For "hour" grouping:
  - start_date/stop_date format: 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
  - start_date is required
  - stop_date is optional
- For "day"/"month" grouping:
  - start_date/stop_date format: 'YYYY-MM-DD' or 'YY-MM-DD'
  - Both start_date and stop_date are required

Returns: [ListInboundMetricsResponse](../models/voice.md#listinboundmetricsresponse)

### Outbound Metrics
```python
client.voice.reporting.outbound.list(
    group: Literal["hour", "day", "month"],     # Time interval grouping
    start_date: Optional[str] = None,           # Start date for filtering
    stop_date: Optional[str] = None,            # End date for filtering
    number: Optional[str] = None                # Filter by phone number
)
```

Notes:
- For "hour" grouping:
  - start_date/stop_date format: 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
  - start_date is required
  - stop_date is optional
- For "day"/"month" grouping:
  - start_date/stop_date format: 'YYYY-MM-DD' or 'YY-MM-DD'
  - Both start_date and stop_date are required

Returns: [ListOutboundMetricsResponse](../models/voice.md#listoutboundmetricsresponse)

### Transfer Metrics
```python
client.voice.reporting.transfer.list(
    group: Literal["hour", "day", "month"],     # Time interval grouping
    start_date: Optional[str] = None,           # Start date for filtering
    stop_date: Optional[str] = None,            # End date for filtering
    number: Optional[str] = None                # Filter by phone number
)
```

Notes:
- For "hour" grouping:
  - start_date/stop_date format: 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
  - start_date is required
  - stop_date is optional
- For "day"/"month" grouping:
  - start_date/stop_date format: 'YYYY-MM-DD' or 'YY-MM-DD'
  - Both start_date and stop_date are required

Returns: [ListTransferMetricsResponse](../models/voice.md#listtransfermetricsresponse)

## Activity Logs

### List Activity Logs
```python
client.voice.activity_logs.list(
    page: Optional[int] = 1,                    # Page number (default: 1)
    page_size: Optional[int] = 50,             # Items per page (1-100, default: 50)
    start: Optional[int] = None,               # Start timestamp (milliseconds)
    stop: Optional[int] = None,                # End timestamp (milliseconds)
    direction: Optional[Literal["inbound", "outbound", "transfer"]] = None,  # Call direction
    status: Optional[Literal["delivered", "failed"]] = None,  # Call status
    from_: Optional[str] = None,               # Filter by originating number
    to: Optional[str] = None,                  # Filter by destination number
    client_id: Optional[str] = None,           # Filter by client ID
    campaign_id: Optional[str] = None,         # Filter by campaign ID
    broadcast_id: Optional[str] = None         # Filter by broadcast ID
)
```

Returns: [ListVoiceActivityLogsResponse](../models/voice.md#listvoiceactivitylogsresponse)

Example:
```python
# Get recent failed calls
logs = client.voice.activity_logs.list(
    page=1,
    page_size=25,
    status="failed"
)
print(f"Found {logs.pagination.total_record} failed calls")
for call in logs.items:
    print(f"Call {call.call_id}: {call.from_} → {call.to}")
    print(f"Failed at: {call.call_date}, Reason: {call.reason}")
```

### Get Call Details
```python
client.voice.activity_logs.get(call_id: str)
```

Returns: [GetVoiceActivityLogResponse](../models/voice.md#getvoiceactivitylogresponse)

Example:
```python
# Get detailed call information
call = client.voice.activity_logs.get("call_123abc")
print(f"Call from {call.from_} to {call.to}")
print(f"Status: {call.status}")
print(f"Duration: {call.call_duration} seconds")
if call.transferred:
    transfer_call = client.voice.activity_logs.get(call.transfer_call_id)
    print(f"Transfer from {transfer_call.from_} to {transfer_call.to}")
    print(f"Transfer Status: {transfer_call.status}")
    print(f"Transfer Duration: {transfer_call.call_duration} seconds")
```

## Related Documentation

- [Voice Models](../models/voice.md)
- [Call Flow Guide](../guides/call-flow.md)
- [Error Handling](../error-handling.md) 