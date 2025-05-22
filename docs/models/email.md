# Email Models

This page documents the models used in the Email API of the Naxai SDK.

## Request Models

### SendTransactionalEmailRequest
Main model for sending transactional emails.

```python
class SendTransactionalEmailRequest(BaseModel):
    sender_email: str           # Sender's email address
    sender_name: str           # Sender's display name
    subject: str               # Email subject line
    to: List[DestinationObject] # List of recipients (max 1000)
    cc: Optional[List[CCObject]] = None  # CC recipients (max 50)
    bcc: Optional[List[BCCObject]] = None  # BCC recipients (max 50)
    reply_to: Optional[str] = None  # Reply-to email address
    text: Optional[str] = None  # Plain text content
    html: Optional[str] = None  # HTML content
    attachments: Optional[List[Attachment]] = None  # File attachments
    enable_tracking: Optional[bool] = None  # Enable open/click tracking
```

### DestinationObject
Model for email recipients.

```python
class DestinationObject(BaseModel):
    email: str                # Recipient email address
    name: Optional[str] = None  # Recipient display name
    metadata: Optional[Dict[str, Any]] = None  # Custom metadata
```

### CCObject and BCCObject
Models for CC and BCC recipients.

```python
class CCObject(BaseModel):
    email: str                # CC recipient email
    name: Optional[str] = None  # CC recipient name

class BCCObject(BaseModel):
    email: str                # BCC recipient email
    name: Optional[str] = None  # BCC recipient name
```

### Attachment
Model for email attachments.

```python
class Attachment(BaseModel):
    filename: str             # Attachment filename
    content: str             # Base64 encoded content
    type: str                # MIME type
    disposition: Optional[str] = "attachment"  # Content disposition
```

Example usage:
```python
# Creating a request with attachments
request = SendTransactionalEmailRequest(
    sender_email="sender@yourdomain.com",
    sender_name="Your Name",
    subject="Document Attached",
    to=[
        DestinationObject(
            email="recipient@example.com",
            name="Recipient Name",
            metadata={"user_id": "123"}
        )
    ],
    attachments=[
        Attachment(
            filename="document.pdf",
            content=base64_encoded_content,
            type="application/pdf"
        )
    ],
    enable_tracking=True
)
```

## Response Models

### EmailResponse
Response model for email sending operations.

```python
class EmailResponse(BaseModel):
    id: str                  # Message ID
    status: str             # Initial status
    created_at: int         # Creation timestamp
```

### EmailActivityLog
Model for email activity logs.

```python
class EmailActivityLog(BaseModel):
    message_id: str          # Message ID
    email: str              # Recipient email
    status: str             # Current status
    created_at: int         # Creation timestamp
    updated_at: Optional[int] # Last update timestamp
    error_code: Optional[str] # Error code if failed
    error_message: Optional[str] # Error description
    metadata: Optional[Dict[str, Any]] # Custom metadata
```

Example:
```python
# Checking email status
log = client.email.activity_logs.get(
    message_id="msg_123abc",
    email="recipient@example.com"
)
print(f"Status: {log.status}")
if log.error_code:
    print(f"Error: {log.error_message}")
```

## Metrics Models

### EmailMetrics
Model for email delivery and engagement metrics.

```python
class EmailMetrics(BaseModel):
    date: str               # Date in YYYY-MM-DD format
    sent: int              # Total emails sent
    delivered: int         # Successfully delivered
    failed: int           # Failed deliveries
    opened: int           # Total opens
    opened_unique: int    # Unique opens
    clicked: int          # Total clicks
    clicked_unique: int   # Unique clicks
    unsubscribed: int    # Unsubscribe count
    complained: int      # Spam complaints
```

### ClickedURLMetrics
Model for URL click tracking metrics.

```python
class ClickedURLMetrics(BaseModel):
    url: str              # Tracked URL
    clicks: int          # Total clicks
    unique_clicks: int   # Unique clicks
    first_click: int    # First click timestamp
    last_click: int     # Last click timestamp
```

Example:
```python
# Analyzing email metrics
metrics = client.email.reporting.metrics.list(
    start=start_time,
    stop=end_time,
    group="day"
)

for day in metrics:
    engagement_rate = day.opened_unique / day.delivered * 100
    print(f"Date: {day.date}")
    print(f"Delivery rate: {day.delivered/day.sent*100:.1f}%")
    print(f"Engagement rate: {engagement_rate:.1f}%")
```

## Constants

### Email Status
```python
EMAIL_STATUS = Literal[
    "queued",        # Email is queued for sending
    "sending",       # Currently being sent
    "delivered",     # Successfully delivered
    "opened",        # Email was opened
    "clicked",       # Links were clicked
    "failed",        # Delivery failed
    "bounced",       # Email bounced
    "complained",    # Marked as spam
    "unsubscribed"   # Recipient unsubscribed
]
```

## Best Practices

1. **Model Validation**
   - Always validate email addresses
   - Check attachment sizes
   - Verify required fields

2. **Error Handling**
   - Handle validation errors gracefully
   - Check for delivery failures
   - Monitor bounce rates

3. **Metadata Usage**
   - Use metadata for tracking
   - Include user identifiers
   - Add campaign information

Example with best practices:
```python
try:
    request = SendTransactionalEmailRequest(
        sender_email="sender@yourdomain.com",
        sender_name="Your Name",
        subject="Welcome!",
        to=[
            DestinationObject(
                email=email,
                name=name,
                metadata={
                    "user_id": user_id,
                    "campaign": "welcome_series",
                    "sequence": 1
                }
            )
        ],
        enable_tracking=True
    )
    response = client.email.send(data=request)
except ValidationError as e:
    logger.error(f"Invalid email request: {e}")
    # Handle validation error
except Exception as e:
    logger.error(f"Failed to send email: {e}")
    # Handle other errors
```

## Related Documentation

- [Email API Reference](../api/email.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 