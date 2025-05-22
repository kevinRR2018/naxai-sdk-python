# SMS API Reference

The SMS API allows you to send text messages and track their delivery status.

## SMS Resource

### Send SMS
```python
client.sms.send(
    to: Union[str, list[str]],     # Single number or list of numbers
    from_: str,                     # Sender number
    text: str,                      # Message content
    idempotency_key: Optional[str] = None,  # Prevent duplicate sends
    scheduled_at: Optional[int] = None,     # Schedule timestamp
    calendar_id: Optional[str] = None,      # Calendar for scheduling
    batch_id: Optional[str] = None          # Batch identifier
)
```

Example:
```python
# Send to single recipient
response = client.sms.send(
    to="1234567890",
    from_="0987654321",
    text="Hello from Naxai SDK!"
)
print(f"Message ID: {response.message_id}")

# Send to multiple recipients
response = client.sms.send(
    to=["1234567890", "1234567891"],
    from_="0987654321",
    text="Bulk message from Naxai SDK!",
    batch_id="batch_123"
)
print(f"Messages sent: {len(response.messages)}")
```

## Activity Logs

### List Activity Logs
```python
client.sms.activity_logs.list(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    start: Optional[int] = None,
    stop: Optional[int] = None,
    status: Optional[str] = None,
    from_: Optional[str] = None,
    to: Optional[str] = None,
    batch_id: Optional[str] = None,
    direction: Optional[Literal["inbound", "outbound"]] = None
)
```

Example:
```python
# Get all failed messages from last 24 hours
from datetime import datetime, timedelta

stop = int(datetime.now().timestamp() * 1000)
start = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)

logs = client.sms.activity_logs.list(
    start=start,
    stop=stop,
    status="failed"
)
```

### Get Message Details
```python
client.sms.activity_logs.get(message_id: str)
```

## Reporting Resource

### Outgoing Metrics
```python
client.sms.reporting.list_outgoing_metrics(
    start: Optional[int] = None,
    stop: Optional[int] = None,
    group: Optional[Literal["hour", "day", "month"]] = None,
    from_: Optional[str] = None,
    to: Optional[str] = None
)
```

### Incoming Metrics
```python
client.sms.reporting.list_incoming_metrics(
    start: Optional[int] = None,
    stop: Optional[int] = None,
    group: Optional[Literal["hour", "day", "month"]] = None,
    from_: Optional[str] = None,
    to: Optional[str] = None
)
```

### Delivery Errors
```python
client.sms.reporting.list_delivery_errors(
    start: Optional[int] = None,
    stop: Optional[int] = None,
    group: Optional[Literal["hour", "day", "month"]] = None,
    error_code: Optional[str] = None
)
```

### Country Metrics
```python
client.sms.reporting.list_by_country(
    start: Optional[int] = None,
    stop: Optional[int] = None,
    group: Optional[Literal["hour", "day", "month"]] = None,
    country: Optional[str] = None
)
```

Example:
```python
# Get daily metrics for the last 7 days
from datetime import datetime, timedelta

stop = int(datetime.now().timestamp() * 1000)
start = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)

metrics = client.sms.reporting.list_outgoing_metrics(
    start=start,
    stop=stop,
    group="day"
)

for stat in metrics:
    print(f"Date: {stat.date}")
    print(f"Sent: {stat.sent}")
    print(f"Delivered: {stat.delivered}")
```

## Best Practices

1. Always use `idempotency_key` for important messages to prevent duplicates
2. Use batch_id for tracking groups of related messages
3. Monitor delivery errors regularly
4. Use appropriate time ranges for metrics to avoid timeout issues

## Related Documentation

- [SMS Models](../models/sms.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 