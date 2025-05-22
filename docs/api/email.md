# Email API Reference

The Email API allows you to send transactional emails and track their delivery and engagement metrics.

## Email Resource

### Send Email (Convenience Method)
```python
client.email.send(
    data: Union[dict, SendTransactionalEmailRequest],
    # Required fields in data:
    # - sender_email: str
    # - sender_name: str
    # - subject: str
    # - to: List[DestinationObject] (max 1000)
    #
    # Optional fields:
    # - cc: List[CCObject] (max 50)
    # - bcc: List[BCCObject] (max 50)
    # - reply_to: str
    # - text: str
    # - html: str
    # - attachments: List[Attachment]
    # - enable_tracking: bool
)
```

Example:
```python
# Simple email
response = client.email.send(data={
    "sender_email": "sender@yourdomain.com",
    "sender_name": "Your Name",
    "subject": "Hello from Naxai",
    "to": [{"email": "recipient@example.com", "name": "Recipient Name"}],
    "text": "This is a test email",
    "html": "<p>This is a test email</p>"
})
print(f"Email sent with ID: {response.id}")

# Email with attachments and tracking
response = client.email.send(data={
    "sender_email": "sender@yourdomain.com",
    "sender_name": "Your Name",
    "subject": "Document Attached",
    "to": [{"email": "recipient@example.com", "name": "Recipient Name"}],
    "html": "<p>Please find the document attached.</p>",
    "attachments": [{
        "filename": "document.pdf",
        "content": base64_encoded_content,
        "type": "application/pdf"
    }],
    "enable_tracking": True
})
```

## Transactional Resource

### Send Transactional Email
```python
client.email.transactional.send(
    data: SendTransactionalEmailRequest
)
```

Example with CC and BCC:
```python
response = client.email.transactional.send(data={
    "sender": {
        "email": "sender@yourdomain.com",
        "name": "Your Name"
    },
    "subject": "Team Update",
    "to": [
        {"email": "team@example.com", "name": "Team"}
    ],
    "cc": [
        {"email": "manager@example.com", "name": "Manager"}
    ],
    "bcc": [
        {"email": "archive@example.com", "name": "Archive"}
    ],
    "html": "<p>Monthly team update...</p>",
    "reply_to": "replies@yourdomain.com"
})
```

## Activity Logs

### List Activity Logs
```python
client.email.activity_logs.list(
    email: str,              # Required: Email address to filter by
    status: Optional[str] = None,  # Filter by status
    page: Optional[int] = None,    # Page number
    limit: Optional[int] = None    # Results per page
)
```

### Get Email Details
```python
client.email.activity_logs.get(
    message_id: str,  # Email message ID
    email: str        # Recipient email address
)
```

Example:
```python
# List recent activity for an email
logs = client.email.activity_logs.list(
    email="recipient@example.com",
    status="delivered",
    page=1,
    limit=50
)

# Get specific email details
details = client.email.activity_logs.get(
    message_id="msg_123abc",
    email="recipient@example.com"
)
```

## Reporting Resource

### Email Metrics
```python
client.email.reporting.metrics.list(
    start: Optional[int] = None,    # Start timestamp
    stop: Optional[int] = None,     # End timestamp
    group: Optional[Literal["day", "month"]] = None  # Grouping period
)
```

Example:
```python
from datetime import datetime, timedelta

# Get last 30 days metrics
stop = int(datetime.now().timestamp() * 1000)
start = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)

metrics = client.email.reporting.metrics.list(
    start=start,
    stop=stop,
    group="day"
)

for stat in metrics:
    print(f"Date: {stat.date}")
    print(f"Sent: {stat.sent}")
    print(f"Delivered: {stat.delivered}")
    print(f"Opened: {stat.opened_unique}")
    print(f"Clicked: {stat.cliqued_unique}")
```

### Clicked URLs Metrics
```python
client.email.reporting.clicked_urls.list(
    start: Optional[int] = None,    # Start timestamp
    stop: Optional[int] = None,     # End timestamp
    group: Optional[Literal["day", "month"]] = None  # Grouping period
)
```

Example:
```python
# Get URL click statistics
clicks = client.email.reporting.clicked_urls.list(
    start=start,
    stop=stop,
    group="day"
)

for url_stat in clicks:
    print(f"URL: {url_stat.url}")
    print(f"Total clicks: {url_stat.clicks}")
    print(f"Unique clicks: {url_stat.unique_clicks}")
```

## Best Practices

1. **Content Types**
   - Always provide both HTML and text versions
   - Use inline CSS for HTML emails
   - Test emails across different clients

2. **Attachments**
   - Keep attachments under 10MB
   - Use appropriate MIME types
   - Base64 encode binary content

3. **Tracking**
   - Enable tracking for marketing emails
   - Monitor bounce rates
   - Track engagement metrics

4. **Compliance**
   - Include unsubscribe links
   - Honor recipient preferences
   - Follow email regulations (GDPR, CAN-SPAM)

## Related Documentation

- [Email Models](../models/email.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 