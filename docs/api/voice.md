# Voice API Reference

The Voice API allows you to make calls, manage broadcasts, and access call reporting features.

## Call Resource

### Create a Call
```python
client.voice.call.create(
    to: list[str],                              # List of recipient phone numbers
    from_: str,                                 # Sender phone number
    language: str,                              # Voice language (e.g., "en-GB")
    welcome: Welcome,                           # Welcome message configuration
    end: Optional[End] = None,                  # End message configuration
    voice: Optional[str] = None,                # Voice type ("man" or "woman")
    batch_id: Optional[str] = None,             # Batch identifier
    calendar_id: Optional[str] = None,          # Calendar for scheduling
    scheduled_at: Optional[int] = None,         # Schedule timestamp
    machine_detection: Optional[bool] = None    # Enable answering machine detection
)
```

Returns: [CreateCallResponse](../models/voice.md#createcallresponse)

Example:
```python
response = client.voice.call.create(
    to=["1234567890"],
    from_="0987654321",
    language="en-GB",
    welcome={"say": "Hello!"},
    end={"say": "Goodbye!"}
)
print(f"Call ID: {response.call_id}")
```

## Broadcasts Resource

### Create a Broadcast
```python
client.voice.broadcasts.create(data: CreateBroadcastRequest)
```

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
    start: Optional[int] = None,
    stop: Optional[int] = None,
    group: Optional[str] = None,  # "hour", "day", "month"
    phone: Optional[str] = None
)
```

Returns: [ListInboundMetricsResponse](../models/voice.md#listinboundmetricsresponse)

### Outbound Metrics
```python
client.voice.reporting.outbound.list(
    start: Optional[int] = None,
    stop: Optional[int] = None,
    group: Optional[str] = None,  # "hour", "day", "month"
    phone: Optional[str] = None
)
```

Returns: [ListOutboundMetricsResponse](../models/voice.md#listoutboundmetricsresponse)

### Transfer Metrics
```python
client.voice.reporting.transfer.list(
    start: Optional[int] = None,
    stop: Optional[int] = None,
    group: Optional[str] = None,  # "hour", "day", "month"
    phone: Optional[str] = None
)
```

Returns: [ListTransferMetricsResponse](../models/voice.md#listtransfermetricsresponse)

## Activity Logs

### List Activity Logs
```python
client.voice.activity_logs.list(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    start: Optional[int] = None,
    stop: Optional[int] = None,
    direction: Optional[str] = None,  # "inbound", "outbound", "transfer"
    status: Optional[str] = None,     # "delivered", "failed"
    from_: Optional[str] = None,
    to: Optional[str] = None,
    client_id: Optional[str] = None,
    campaign_id: Optional[str] = None,
    broadcast_id: Optional[str] = None
)
```

Returns: [ListVoiceActivityLogsResponse](../models/voice.md#listvoiceactivitylogsresponse)

### Get Call Details
```python
client.voice.activity_logs.get(call_id: str)
```

Returns: [GetVoiceActivityLogResponse](../models/voice.md#getvoiceactivitylogresponse)

## Related Documentation

- [Voice Models](../models/voice.md)
- [Call Flow Guide](../guides/call-flow.md)
- [Error Handling](../error-handling.md) 