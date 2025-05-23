# SMS API Reference

The SMS API allows you to send text messages and track their delivery status.

## SMS Resource

### Send SMS
```python
client.sms.send(
    to: list[str],                          # List of recipient phone numbers in E.164 format (max 1000)
    body: str,                              # Text content of the SMS message (max 1530 chars)
    from_: str = None,                      # Sender phone number (max 15 chars)
    sender_service_id: str = None,          # Optional sender service ID
    type_: str = text,                      # Message encoding type ( text, unicode or auto )
    scheduled_at: str = None,               # ISO 8601 timestamp for scheduled delivery
    validity: int = None,                   # Validity period in minutes (5-4320)
    idempotency_key: str = None,            # Prevent duplicates (max 200 chars)
    reference: str = None,                  # Custom tracking reference (max 128 chars)
    calendar_id: str = None,                # Calendar ID for delivery constraints
    max_parts: int = None,                  # Maximum message parts (1-10)
    truncate: bool = False                  # Whether to truncate long messages
)
```

Request: [SendSMSRequest](../models/sms.md#sendsmsrequest)  
Returns: [SendSMSResponse](../models/sms.md#sendsmsresponse)

Example:
```python
# Send to single recipient
response = client.sms.send(
    to=["1234567890"],
    from_="0987654321",
    body="Hello from Naxai SDK!"
)
print(f"Message ID: {response.messages[0].message_id}")

# Send to multiple recipients
response = client.sms.send(
    to=["1234567890", "1234567891"],
    from_="0987654321",
    body="Bulk message from Naxai SDK!"
)
print(f"Messages sent: {len(response.messages)}")
```

## Activity Logs

### List Activity Logs
```python
client.sms.activity_logs.list(
    page: int = 1,                                      # Page number to retrieve
    page_size: int = 25,                               # Number of items per page
    start: Optional[int] = None,                       # Start timestamp (milliseconds)
    stop: Optional[int] = None,                        # End timestamp (milliseconds)
    direction: Literal["inbound", "outbound"] = None,  # Filter by message direction
    status: Literal["delivered", "failed"] = None,     # Filter by delivery status
    phone_number: str = None,                          # Filter by phone number (7-15 chars)
    client_id: str = None,                             # Filter by client identifier
    campaign_id: str = None,                           # Filter by campaign identifier
    broadcast_id: str = None                           # Filter by broadcast identifier
)
```

Returns: [ListSMSActivityLogsResponse](../models/sms.md#listsmsactivitylogsresponse)

Example:
```python
# Get all failed messages from last 24 hours
from datetime import datetime, timedelta

stop = int(datetime.now().timestamp() * 1000)
start = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)

logs = client.sms.activity_logs.list(
    page=1,
    page_size=25,
    start=start,
    stop=stop,
    status="failed"
)

print(f"Found {logs.pagination.total_record} failed SMS")
for log in logs.messages:
    print(f"SMS {log.message_id} from {log.from_} to {log.to}")
    print(f"Status: {log.status}")
    print(f"Details: {log.status_details}")
    print(f"Reason: {log.status_reason}")
```

### Get Message Details
```python
client.sms.activity_logs.get(message_id: str)
```

Returns: [GetSMSActivityLogsResponse](../models/sms.md#getsmsactivitylogsresponse)

## Reporting Resource

### Outgoing Metrics
```python
client.sms.reporting.list_outgoing_metrics(
    group: Literal["hour", "day", "month"],
    start_date: str = None,
    stop_date: str = None
)
```

Returns: [ListOutgoingSMSMetricsResponse](../models/sms.md#listoutgoingsmsmetricsresponse)

### Outgoing Metrics By Country
```python
client.sms.reporting.list_by_country(
    start_date: str,            # YYYY-MM-DD
    stop_date: str              # YYYY-MM-DD
)
```

Returns: [ListOutgoingSMSByCountryMetricsResponse](../models/sms.md#listoutgoingsmsbycountrymetricsresponse)

### Incoming Metrics
```python
client.sms.reporting.list_incoming_metrics(
    group: Literal["hour", "day", "month"],
    start_date: str = None,
    stop_date: str = None
)
```

Returns: [ListIncomingSMSMetricsResponse](../models/sms.md#listincomingsmsmetricsresponse)

### Delivery Errors
```python
client.sms.reporting.list_delivery_errors_metrics(
    start_date: str,           # YYYY-MM-DD
    stop_date: str             # YYYY-MM-DD
)
```

Returns: [ListDeliveryErrorMetricsResponse](../models/sms.md#listdeliveryerrormetricsresponse)

Example:
```python
# Get daily metrics for a specific day
# For hour grouping, use YYYY-MM-DD HH:MM:SS format
metrics = client.sms.reporting.list_outgoing_metrics(
    start_date="2025-05-23 00:00:00",
    stop_date="2025-05-23 23:59:59",
    group="hour"
)

for stat in metrics.stats:
    print(f"Date: {stat.date}")
    print(f"SMS sent: {stat.sms}")
    print(f"Delivered: {stat.delivered}")
    print(f"Average delivery time: {stat.avg_time_to_deliver} ms")

# Get country-based metrics
country_metrics = client.sms.reporting.list_outgoing_metrics_by_country(
    start_date="2023-05-23",  # YYYY-MM-DD format required
    stop_date="2023-05-23"
)

for stat in country_metrics.stats:
    if stat.sms > 0:
        delivery_rate = (stat.delivered / stat.sms) * 100
        print(f"Country: {stat.country} ({stat.mcc}-{stat.mnc})")
        print(f"Delivery rate: {delivery_rate:.1f}%")
        print(f"Average delivery time: {stat.avg_time_to_deliver} ms")
```

## Best Practices

1. Always use `idempotency_key` for important messages to prevent duplicates
2. Use E.164 format for phone numbers (e.g., "32477112233")
3. Monitor delivery errors regularly
4. Use appropriate time ranges for metrics to avoid timeout issues

## Related Documentation

- [SMS Models](../models/sms.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 