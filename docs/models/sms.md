# SMS Models

This page documents the models used in the SMS API of the Naxai SDK.

## Message Models

### BaseMessageModel
Base model for SMS messages.

```python
class BaseMessageModel(BaseModel):
    to: str                  # Recipient phone number
    message_id: Optional[str] # Unique message identifier
```

### SendSMSResponse
Response model for SMS sending operations.

```python
class SendSMSResponse(BaseModel):
    messages: list[BaseMessageModel]  # List of sent messages
```

Example:
```python
response = client.sms.send(
    to=["1234567890", "1234567891"],
    from_="0987654321",
    text="Hello!"
)

for msg in response.messages:
    print(f"Message to {msg.to} has ID: {msg.message_id}")
```

## Activity Log Models

### SMSActivityLog
Model representing a message's activity log.

```python
class SMSActivityLog(BaseModel):
    message_id: str          # Unique message identifier
    from_: str              # Sender number
    to: str                 # Recipient number
    status: str             # Message status
    direction: str          # "inbound" or "outbound"
    created_at: int         # Creation timestamp
    updated_at: Optional[int] # Last update timestamp
    error_code: Optional[str] # Error code if failed
    error_message: Optional[str] # Error description
```

Example:
```python
log = client.sms.activity_logs.get("msg_123abc")
print(f"Status: {log.status}")
if log.error_code:
    print(f"Error: {log.error_message}")
```

## Metrics Models

### SMSMetrics
Base model for SMS metrics data.

```python
class SMSMetrics(BaseModel):
    date: Optional[str]      # Date in YYYY-MM-DD format
    sent: int               # Total messages sent
    delivered: int          # Successfully delivered
    failed: int            # Failed deliveries
    cost: Optional[float]   # Total cost if available
```

### DeliveryError
Model for delivery error statistics.

```python
class DeliveryError(BaseModel):
    error_code: str         # Error code
    count: int             # Number of occurrences
    description: str       # Error description
```

### CountryMetrics
Model for country-specific metrics.

```python
class CountryMetrics(BaseModel):
    country: str           # Country code
    sent: int             # Messages sent
    delivered: int        # Messages delivered
    failed: int          # Failed deliveries
    cost: Optional[float] # Cost for this country
```

Example:
```python
# Get metrics by country
metrics = client.sms.reporting.list_by_country(
    start=start_time,
    stop=end_time,
    group="day"
)

for country in metrics:
    print(f"Country: {country.country}")
    print(f"Sent: {country.sent}")
    print(f"Delivery rate: {country.delivered/country.sent*100:.1f}%")
```

## Constants

### Message Status
```python
MESSAGE_STATUS = Literal[
    "accepted",      # Message accepted for delivery
    "scheduled",     # Scheduled for future delivery
    "sending",       # Currently being sent
    "delivered",     # Successfully delivered
    "failed",        # Delivery failed
    "undelivered",   # Could not be delivered
    "rejected"       # Rejected by carrier
]
```

### Direction Types
```python
DIRECTION_TYPES = Literal[
    "inbound",      # Incoming message
    "outbound"      # Outgoing message
]
```

## Best Practices

1. Always handle all possible message statuses in your application
2. Store message_id for future status queries
3. Use appropriate error handling for failed deliveries
4. Monitor metrics regularly for delivery performance

## Related Documentation

- [SMS API Reference](../api/sms.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 