# Email Models

This page documents the models used in the Email API of the Naxai SDK.

## Request Models

### SendTransactionalEmailRequest
Main model for sending transactional emails.

```python
class SendTransactionalEmailRequest(BaseModel):
    sender: SenderObject           # Sender information
    to: list[DestinationObject]   # List of recipients
    cc: Optional[list[CCObject]] = None  # CC recipients
    bcc: Optional[list[BCCObject]] = None  # BCC recipients
    reply_to: Optional[str] = None  # Reply-to email address
    subject: str                  # Email subject line
    text: Optional[str] = None    # Plain text content
    html: Optional[str] = None    # HTML content
    attachments: Optional[list[Attachment]] = None  # File attachments
    enable_tracking: Optional[bool] = None  # Enable open/click tracking
```

### SenderObject
Model for email sender information.

```python
class SenderObject(BaseObject):
    email: str                # Sender's email address
    name: str                # Sender's display name
```

### DestinationObject, CCObject, BCCObject
Models for email recipients.

```python
class BaseObject(BaseModel):
    email: str                # Email address
    name: str                # Display name

class DestinationObject(BaseObject):
    # Inherits email and name from BaseObject
    pass

class CCObject(BaseObject):
    # Inherits email and name from BaseObject
    pass

class BCCObject(BaseObject):
    # Inherits email and name from BaseObject
    pass
```

### Attachment
Model for email attachments.

```python
class Attachment(BaseModel):
    id: str                  # Unique attachment identifier
    name: str               # Attachment filename
    content_type: str       # MIME type
    data: str              # Base64 encoded content
```

Example usage:
```python
# Creating a request with attachments
request = SendTransactionalEmailRequest(
    sender=SenderObject(
        email="sender@yourdomain.com",
        name="Your Name"
    ),
    to=[
        DestinationObject(
            email="recipient@example.com",
            name="Recipient Name"
        )
    ],
    subject="Document Attached",
    html="<h1>Hello</h1><p>Please find the document attached.</p>",
    text="Hello\n\nPlease find the document attached.",
    attachments=[
        Attachment(
            id="att_123",
            name="document.pdf",
            content_type="application/pdf",
            data=base64_encoded_content
        )
    ],
    enable_tracking=True
)
```

## Response Models

### SendTransactionalEmailResponse
Response model for email sending operations.

```python
class SendTransactionalEmailResponse(BaseModel):
    id: str                  # Unique email identifier
```

### BaseActivityLogs
Base model for email activity tracking.

```python
class BaseActivityLogs(BaseModel):
    message_id: str          # Message ID
    from_email: str         # Sender email
    to_email: Optional[str] # Recipient email
    subject: Optional[str]  # Email subject
    status: Optional[Literal["sent", "delivered", "failed"]]  # Current status
    created_at: Optional[int] # Creation timestamp (ms)
    updated_at: Optional[int] # Last update timestamp (ms)
    opens: Optional[int]    # Number of opens
    clicks: Optional[int]   # Number of clicks
```

### EmailEvents
Model for detailed email event tracking.

```python
class EmailEvents(BaseModel):
    name: Optional[str]     # Event name
    processed: Optional[int] # Event timestamp
    reason: Optional[Union[dict, str]] # Additional event details
```

### GetEmailActivityLogsResponse
Detailed activity log response model.

```python
class GetEmailActivityLogsResponse(BaseActivityLogs):
    events: Optional[list[EmailEvents]] = None  # Event history
    email: Optional[str] = None        # Alternative recipient email
    client_id: Optional[str] = None    # Client identifier
    campaign_id: Optional[str] = None  # Campaign identifier
```

### ListEmailActivityLogsResponse
Model for paginated activity logs.

```python
class ListEmailActivityLogsResponse(BaseModel):
    pagination: Pagination  # Pagination information
    messages: list[BaseActivityLogs]  # List of activity logs
```

## Metrics Models

### BaseStats
Model for email engagement metrics.

```python
class BaseStats(BaseModel):
    date: Optional[int]     # Timestamp for stats period
    sent: Optional[int]     # Emails sent
    delivered: Optional[int] # Successfully delivered
    opened: Optional[int]   # Total opens
    opened_unique: Optional[int] # Unique opens
    clicked: Optional[int]  # Total clicks
    clicked_unique: Optional[int] # Unique clicks
    failed: Optional[int]   # Failed deliveries
    suppress_bound: Optional[int] # Suppressed (bounces)
    suppress_unsubscribe: Optional[int] # Suppressed (unsubscribes)
    bounced: Optional[int]  # Bounced emails
    rejected: Optional[int] # Rejected emails
    complained: Optional[int] # Spam complaints
    unsubscribed: Optional[int] # Unsubscribe requests
```

### BaseClickedUrlsStats
Model for URL click tracking.

```python
class BaseClickedUrlsStats(BaseModel):
    url: Optional[str]      # Tracked URL
    clicked: Optional[int]  # Total clicks
    clicked_unique: Optional[int] # Unique clicks
```

### ListMetricsResponse
Response model for time-based metrics.

```python
class ListMetricsResponse(BaseModel):
    start: Optional[int]    # Start timestamp
    stop: Optional[int]     # End timestamp
    group: Optional[str]    # Grouping interval
    stats: list[BaseStats]  # List of stats entries
```

### ListClickedUrlsMetricsResponse
Response model for URL metrics.

```python
class ListClickedUrlsMetricsResponse(BaseModel):
    start: Optional[int]    # Start timestamp
    stop: Optional[int]     # End timestamp
    stats: list[BaseClickedUrlsStats]  # URL stats list
```

## Best Practices

1. **Email Content**
   - Provide both HTML and text versions
   - Keep HTML content responsive
   - Follow email design best practices
   - Test content rendering in various clients

2. **Attachments**
   - Use appropriate MIME types
   - Keep attachments under size limits
   - Base64 encode attachment data
   - Consider attachment compatibility

3. **Tracking and Metrics**
   - Monitor delivery rates
   - Track engagement metrics
   - Analyze click patterns
   - Use unique tracking for accurate stats

4. **Error Handling**
   - Check response status
   - Monitor bounce rates
   - Handle failed deliveries
   - Track spam complaints

Example with best practices:
```python
from naxai.models.email import (
    SendTransactionalEmailRequest,
    SenderObject,
    DestinationObject,
    Attachment
)

try:
    # Create email request with tracking
    request = SendTransactionalEmailRequest(
        sender=SenderObject(
            email="notifications@yourdomain.com",
            name="Your Service"
        ),
        to=[
            DestinationObject(
                email=recipient_email,
                name=recipient_name
            )
        ],
        subject="Welcome to Our Service",
        html="""
        <html>
            <body>
                <h1>Welcome!</h1>
                <p>Thank you for joining our service.</p>
                <p><a href="https://example.com/start">Get Started</a></p>
            </body>
        </html>
        """,
        text="""
        Welcome!
        
        Thank you for joining our service.
        
        Get started: https://example.com/start
        """,
        enable_tracking=True
    )
    
    # Send email and get response
    response = client.email.send(request)
    
    # Track delivery status
    status = client.email.activity_logs.get(
        message_id=response.id,
        email=recipient_email
    )
    
except Exception as e:
    logger.error(f"Failed to send email: {e}")
    # Handle error appropriately
```

## Related Documentation

- [Email API Reference](../api/email.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 