# SMS Models

This page documents the models used in the SMS API of the Naxai SDK.

## Message Models

### BaseMessageModel
Base model for SMS messages.

```python
class BaseMessageModel(BaseModel):
    to: str                  # Recipient phone number (optional)
    message_id: str          # Unique message identifier (optional)
```

### SendSMSResponse
Response model for SMS sending operations.

```python
class SendSMSResponse(BaseModel):
    batch_id: str                    # Unique batch identifier (optional)
    count: int                       # Number of messages in batch (optional)
    messages: list[BaseMessageModel]  # List of sent messages (optional)
```

Example:
```python
response = SendSMSResponse(
    batch_id="batch_123abc",
    count=3,
    messages=[
        BaseMessageModel(to="+1234567890", message_id="msg_123abc"),
        BaseMessageModel(to="+2345678901", message_id="msg_456def"),
        BaseMessageModel(to="+3456789012", message_id="msg_789ghi")
    ]
)
```

## Activity Log Models

### BaseMessage
Detailed model for SMS message activity logs.

```python
class BaseMessage(BaseModel):
    message_id: str          # Unique message identifier
    from_: str              # Sender number (optional)
    to: str                 # Recipient number
    mcc: str               # Mobile Country Code (optional)
    mnc: str               # Mobile Network Code (optional)
    body: str              # Message content
    parts: int             # Number of message segments (optional)
    encoding: Literal["unicode", "text", "binary"]  # Message encoding
    direction: Literal["outgoing", "incoming"]      # Message direction
    sent_at: int           # Sending timestamp (optional)
    submitted_at: int      # Carrier submission timestamp (optional)
    delivered_at: int      # Delivery timestamp (optional)
    received_at: int       # Reception timestamp (optional)
    status: Literal["delivered", "failed"]  # Delivery status (optional)
    status_code: int       # Status code (optional)
    status_reason: str     # Status description (optional)
    status_details: str    # Detailed status info (optional)
    opt_out: bool         # Opt-out flag (optional)
    reference: str        # Custom reference (optional)
    client_id: str        # Client identifier (optional)
    campaign_id: str      # Campaign identifier (optional)
    broadcast_id: str     # Broadcast identifier (optional)
```

### ListSMSActivityLogsResponse
Model for paginated activity logs.

```python
class ListSMSActivityLogsResponse(BaseModel):
    pagination: Pagination      # Pagination information
    messages: list[BaseMessage] # List of message logs
```

### GetSMSActivityLogsResponse
Model for single message activity log.

```python
class GetSMSActivityLogsResponse(BaseMessage):
    # Inherits all fields from BaseMessage
    pass
```

## Metrics Models

### BaseStats
Base model for SMS statistics.

```python
class BaseStats(BaseModel):
    sms: int                # Total messages
    delivered: int          # Successfully delivered
    failed: int            # Failed deliveries
    expired: int           # Expired messages
    unknown: int           # Unknown status
    canceled: int          # Canceled messages
    rejected: int          # Rejected messages
    blocked: int           # Blocked messages (optional)
    avg_time_to_deliver: int  # Average delivery time (ms)
    avg_time_to_submit: int   # Average submission time (ms)
```

### OutgoingStats
Model for time-based outgoing metrics.

```python
class OutgoingStats(BaseStats):
    date: str  # Metrics date/timestamp
```

### OutgoingCountryStats
Model for country-based metrics.

```python
class OutgoingCountryStats(BaseStats):
    country: str  # Country code (optional)
    mcc: str     # Mobile Country Code
    mnc: str     # Mobile Network Code
```

### IncomingStats
Model for incoming message metrics.

```python
class IncomingStats(BaseModel):
    date: str  # Metrics date/timestamp
    sms: int   # Total incoming messages
```

### DeliveryErrorStats
Model for error statistics.

```python
class DeliveryErrorStats(BaseModel):
    status_category: str  # Error category
    status_code: str     # Error code
    sms: int            # Number of affected messages
```

### ListOutgoingSMSMetricsResponse
Response model for outgoing metrics.

```python
class ListOutgoingSMSMetricsResponse(BaseResponse):
    direction: Literal["outgoing"]
    group: Literal["hour", "day", "month"]
    stats: list[OutgoingStats]
```

### ListOutgoingSMSByCountryMetricsResponse
Response model for country-based metrics.

```python
class ListOutgoingSMSByCountryMetricsResponse(BaseResponse):
    direction: Literal["outgoing"]
    stats: list[OutgoingCountryStats]
```

### ListIncomingSMSMetricsResponse
Response model for incoming metrics.

```python
class ListIncomingSMSMetricsResponse(BaseResponse):
    direction: Literal["incoming"]
    group: Literal["hour", "day", "month"]
    stats: list[IncomingStats]
```

### ListDeliveryErrorMetricsResponse
Response model for error metrics.

```python
class ListDeliveryErrorMetricsResponse(BaseResponse):
    stats: list[DeliveryErrorStats]
```

## Best Practices

1. **Message Tracking**
   - Store message_id for future status queries
   - Use batch_id for tracking multiple messages
   - Monitor delivery status through activity logs

2. **Performance Monitoring**
   - Track delivery rates by country
   - Monitor error patterns
   - Analyze timing metrics
   - Use appropriate time groupings for metrics

3. **Error Handling**
   - Handle all possible message statuses
   - Check error categories and codes
   - Monitor blocked and rejected messages
   - Implement appropriate retry strategies

Example:
```python
# Send messages and track delivery
response = client.sms.send(
    to=["+1234567890", "+2345678901"],
    from_="SENDER",
    text="Hello!"
)

# Store message IDs for tracking
message_ids = [msg.message_id for msg in response.messages]

# Monitor delivery status
for msg_id in message_ids:
    status = client.sms.activity_logs.get(msg_id)
    print(f"Message {msg_id}: {status.status}")
    if status.status == "failed":
        print(f"Error: {status.status_reason}")

# Get delivery metrics
metrics = client.sms.reporting.list_by_country(
    start_date="2023-01-01",
    end_date="2023-01-31"
)

# Analyze delivery performance
for country in metrics.stats:
    delivery_rate = country.delivered / country.sms * 100
    print(f"{country.country}: {delivery_rate:.1f}% delivery rate")
```

## Related Documentation

- [SMS API Reference](../api/sms.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 