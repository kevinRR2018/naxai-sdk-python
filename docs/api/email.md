# Email API Reference

The Email API allows you to send transactional emails and track their delivery and engagement metrics.

## Email Resource

### Send Email
```python
client.email.send(
    sender_email: str,                      # Verified sender email address
    sender_name: str,                       # Display name of the sender
    subject: str,                           # Email subject line
    to: List[DestinationObject],            # List of recipients (1-1000)
    cc: Optional[List[CCObject]] = None,    # CC recipients (max 50)
    bcc: Optional[List[BCCObject]] = None,  # BCC recipients (max 50)
    reply_to: Optional[str] = None,         # Reply-to email address
    text: Optional[str] = None,             # Plain text email body
    html: Optional[str] = None,             # HTML email body
    attachments: List[Attachment] = None,    # File attachments
    enable_tracking: Optional[bool] = None   # Enable open/click tracking
)
```

Request Models:
- [DestinationObject](../models/email.md#destinationobject)
- [CCObject](../models/email.md#ccobject)
- [BCCObject](../models/email.md#bccobject)
- [Attachment](../models/email.md#attachment)

Returns: [SendTransactionalEmailResponse](../models/email.md#sendtransactionalemailresponse)

Example:
```python
# Basic email with both HTML and text content
response = client.email.send(
    sender_email="sender@example.com",
    sender_name="Sender Name",
    subject="Your Account Verification",
    to=[{"email": "recipient@example.com", "name": "Recipient Name"}],
    html="<html><body><h1>Verify Your Account</h1><p>Click the link to verify your account.</p></body></html>",
    text="Verify Your Account\n\nClick the link to verify your account.",
    enable_tracking=True
)
print(f"Email sent with ID: {response.id}")

# Email with multiple recipients and an attachment
from base64 import b64encode
pdf_content = b64encode(open("document.pdf", "rb").read()).decode()

response = client.email.send(
    sender_email="support@example.com",
    sender_name="Customer Support",
    subject="Your Monthly Statement",
    to=[{"email": "customer@example.com", "name": "Customer Name"}],
    cc=[{"email": "accounting@example.com"}],
    reply_to="no-reply@example.com",
    html="<html><body><p>Please find your monthly statement attached.</p></body></html>",
    attachments=[{
        "filename": "statement.pdf",
        "content_type": "application/pdf",
        "data": pdf_content
    }]
)
print(f"Email with attachment sent with ID: {response.id}")
```

Notes:
- The `sender_email` must be a verified sender in your Naxai account
- At least one of `text` or `html` must be provided
- Recipients are specified using DestinationObject format: `{"email": "address", "name": "optional_name"}`
- The total size of all attachments should not exceed 10MB
- For high deliverability, ensure your sender domain is properly configured with SPF and DKIM
- This is a convenience wrapper around `transactional.send()`

## Transactional Resource

### Send Transactional Email
```python
client.email.transactional.send(
    data: SendTransactionalEmailRequest
)
```

Request: [SendTransactionalEmailRequest](../models/email.md#sendtransactionalemailrequest)  
Returns: [SendTransactionalEmailResponse](../models/email.md#sendtransactionalemailresponse)

Example:
```python
request = SendTransactionalEmailRequest.model_validate(
    {
        "sender": {
            "email": "sender@yourdomain.com",
            "name": "Your Name"
            },
            "subject": "Team Update",
            "to": [{"email": "team@example.com", "name": "Team"}],
            "cc": [{"email": "manager@example.com", "name": "Manager"}],
            "bcc": [{"email": "archive@example.com", "name": "Archive"}],
            "html": "<p>Monthly team update...</p>",
            "text": "Monthly team update...",
            "reply_to": "replies@yourdomain.com",
            "enable_tracking": True
    })
#Send an email
response = client.email.transactional.send(data=request)

print(f"Email sent with ID: {response.id}")
```

## Activity Logs

The Activity Logs API allows you to track and analyze the delivery status and engagement metrics of your sent emails.

### List Activity Logs
```python
client.email.activity_logs.list(
    page: Optional[int] = 1,                                      # Page number (default: 1)
    page_size: Optional[int] = 50,                               # Items per page (1-100, default: 50)
    start: Optional[int] = None,                                 # Start timestamp (milliseconds)
    stop: Optional[int] = None,                                  # End timestamp (milliseconds)
    sort: Optional[str] = "updatedAt:desc",                      # Sort order (field:direction)
    email: Optional[str] = None,                                 # Filter by recipient email
    client_id: Optional[str] = None,                             # Filter by client ID
    campaign_id: Optional[str] = None,                           # Filter by campaign ID
    status: Optional[Literal["sent", "delivered", "failed"]] = None  # Filter by status
)
```

Returns: [ListEmailActivityLogsResponse](../models/email.md#listemailactivitylogsresponse)

Example:
```python
# Basic usage with pagination
activity_logs = client.email.activity_logs.list(
    page=1,
    page_size=25
)
print(f"Found {activity_logs.pagination.total_record} emails")
print(f"Showing page {activity_logs.pagination.page} of {activity_logs.pagination.last}")
for msg in activity_logs.messages:
    print(f"Email: {msg.subject} - Status: {msg.status}")

# Filtering by date range, status, and recipient
import time
one_week_ago = int(time.time()) - (7 * 24 * 60 * 60)
now = int(time.time())

delivered_emails = client.email.activity_logs.list(
    start=one_week_ago,
    stop=now,
    status="delivered",
    email="customer@example.com",
    sort="createdAt:asc"
)

# Calculate engagement metrics
if delivered_emails.messages:
    opened = sum(1 for msg in delivered_emails.messages if msg.opens and msg.opens > 0)
    clicked = sum(1 for msg in delivered_emails.messages if msg.clicks and msg.clicks > 0)
    open_rate = opened / len(delivered_emails.messages) * 100
    click_rate = clicked / len(delivered_emails.messages) * 100
    print(f"Found {len(delivered_emails.messages)} delivered emails")
    print(f"Open rate: {open_rate:.1f}%")
    print(f"Click rate: {click_rate:.1f}%")

# Filtering by campaign
campaign_emails = client.email.activity_logs.list(
    campaign_id="camp_123abc",
    page_size=100
)

# Count emails by status
status_counts = {"sent": 0, "delivered": 0, "failed": 0}
for msg in campaign_emails.messages:
    if msg.status in status_counts:
        status_counts[msg.status] += 1

print(f"Campaign Status:")
print(f"- Sent: {status_counts['sent']}")
print(f"- Delivered: {status_counts['delivered']}")
print(f"- Failed: {status_counts['failed']}")
```

Notes:
- The `page_size` parameter must be between 1 and 100
- Timestamps (`start`, `stop`) are in milliseconds since epoch
- Sort options include:
  * `createdAt:asc/desc`: Sort by creation time
  * `updatedAt:asc/desc`: Sort by last update time (default)
  * `status:asc/desc`: Sort by delivery status
- Status filters:
  * `sent`: Email has been accepted for delivery
  * `delivered`: Email has reached the recipient's inbox
  * `failed`: Email delivery has failed

### Get Email Details
```python
client.email.activity_logs.get(
    message_id: str,  # Email message ID
    email: str        # Recipient email address
)
```

Returns: [GetEmailActivityLogsResponse](../models/email.md#getemailactivitylogsresponse)

Example:
```python
# Get detailed activity for a specific email
message_details = client.email.activity_logs.get(
    message_id="msg_123abc456def",
    email="recipient@example.com"
)

print(f"Email: {message_details.subject}")
print(f"From: {message_details.from_email} to: {message_details.to_email}")
print(f"Status: {message_details.status}")
print(f"Engagement: {message_details.opens or 0} opens, {message_details.clicks or 0} clicks")

# Display event timeline
if message_details.events:
    print("\nEvent Timeline:")
    for event in message_details.events:
        details = f" - {event.reason}" if event.reason else ""
        print(f"- {event.processed}: {event.name}{details}")
```

The response includes:
- Basic email information (subject, sender, recipient)
- Current delivery status
- Engagement metrics (opens, clicks)
- Complete event timeline, including:
  * `sent`: Email accepted for delivery
  * `delivered`: Email reached recipient's inbox
  * `opened`: Recipient opened the email
  * `clicked`: Recipient clicked a link
  * `failed`: Delivery failed
  * `bounced`: Email bounced from recipient's server
  * `complained`: Marked as spam
  * `unsubscribed`: Recipient unsubscribed

## Reporting Resource

The Reporting Resource provides comprehensive analytics and metrics for your email campaigns, helping you track delivery rates, engagement statistics, and performance indicators.

### Email Metrics
```python
client.email.reporting.metrics.list(
    start: Optional[int] = (now - 7 days),     # Start timestamp in seconds since epoch
    stop: Optional[int] = now,                 # End timestamp in seconds since epoch
    group: Optional[Literal["day", "month"]] = "day"  # Time interval grouping
)
```

The response includes detailed statistics for each time interval:
- `date`: Timestamp for the interval (milliseconds)
- `sent`: Number of emails sent
- `delivered`: Successfully delivered emails
- `opened`: Total number of opens
- `opened_unique`: Unique recipients who opened
- `clicked`: Total number of link clicks
- `clicked_unique`: Unique recipients who clicked
- `failed`: Failed deliveries
- `suppress_bound`: Suppressed due to hard bounces
- `suppress_unsubscribe`: Suppressed due to unsubscribes
- `bounced`: Bounced emails
- `rejected`: Rejected by recipient servers
- `complained`: Spam complaints
- `unsubscribed`: Unsubscribe requests

Example:
```python
import time
from datetime import datetime, timedelta

# Get email metrics for the past 30 days
thirty_days_ago = int(time.time()) - (30 * 24 * 60 * 60)
current_time = int(time.time())

metrics = client.email.reporting.metrics.list(
    start=thirty_days_ago,
    stop=current_time,
    group="day"
)

print(f"Email metrics from {datetime.fromtimestamp(metrics.start/1000)}")
print(f"to {datetime.fromtimestamp(current_time)}")
print(f"Grouped by: {metrics.group}")
print(f"Data points: {len(metrics.stats)}")

# Calculate overall metrics
total_sent = sum(day.sent for day in metrics.stats if day.sent is not None)
total_delivered = sum(day.delivered for day in metrics.stats if day.delivered is not None)
total_opened = sum(day.opened_unique for day in metrics.stats if day.opened_unique is not None)
total_clicked = sum(day.clicked_unique for day in metrics.stats if day.clicked_unique is not None)

# Calculate key performance indicators
if total_sent > 0:
    delivery_rate = total_delivered / total_sent * 100
    print(f"Overall delivery rate: {delivery_rate:.1f}%")

if total_delivered > 0:
    open_rate = total_opened / total_delivered * 100
    click_rate = total_clicked / total_delivered * 100
    print(f"Overall open rate: {open_rate:.1f}%")
    print(f"Overall click rate: {click_rate:.1f}%")

if total_opened > 0:
    click_to_open_rate = total_clicked / total_opened * 100
    print(f"Click-to-open rate: {click_to_open_rate:.1f}%")

# Find the day with highest engagement
if metrics.stats:
    best_day = max(metrics.stats, key=lambda day: day.opened_unique or 0)
    print(f"\nBest performing day: {datetime.fromtimestamp(best_day.date/1000)}")
    print(f"Sent: {best_day.sent}, Opened: {best_day.opened_unique}, "
          f"Clicked: {best_day.clicked_unique}")

```

Notes:
- Timestamps:
  * Input parameters (`start`, `stop`) are in seconds since epoch
  * Response timestamps are in milliseconds since epoch
  * Default range is the past 7 days if no parameters provided
- Key metrics to monitor:
  * Delivery rate = delivered / sent
  * Open rate = opened_unique / delivered
  * Click rate = clicked_unique / delivered
  * Click-to-open rate = clicked_unique / opened_unique
- Negative metrics to watch:
  * Bounce rate = bounced / sent
  * Complaint rate = complained / sent
  * Unsubscribe rate = unsubscribed / delivered
- High bounce or complaint rates may indicate issues with email quality or recipient targeting
- For best results, use a time range that matches your email sending frequency

### Clicked URLs Metrics
```python
client.email.reporting.clicked_urls.list(
    start: Optional[int] = (now - 7 days),     # Start timestamp in seconds since epoch
    stop: Optional[int] = now,                 # End timestamp in seconds since epoch
    group: Optional[Literal["day", "month"]] = "day"  # Time interval grouping
)
```

The response includes URL-specific click statistics:
- `url`: The URL that was clicked
- `clicked`: Total number of clicks on this URL
- `clicked_unique`: Number of unique recipients who clicked this URL

Example:
```python
import time
from datetime import datetime

# Get URL click metrics for the past 30 days
thirty_days_ago = int(time.time()) - (30 * 24 * 60 * 60)
current_time = int(time.time())

metrics = client.email.reporting.clicked_urls.list(
    start=thirty_days_ago,
    stop=current_time,
    group="day"
)

print(f"URL click metrics from {datetime.fromtimestamp(metrics.start/1000)}")
print(f"to {datetime.fromtimestamp(metrics.stop/1000)}")
print(f"Found data for {len(metrics.stats)} URLs")

# Find and display the most clicked URLs
sorted_urls = sorted(
    metrics.stats,
    key=lambda x: x.clicked_unique or 0,
    reverse=True
)

print("\nTop 3 most clicked URLs:")
for i, url_stats in enumerate(sorted_urls[:3], 1):
    print(f"{i}. {url_stats.url}")
    print(f"   Total clicks: {url_stats.clicked}")
    print(f"   Unique clicks: {url_stats.clicked_unique}")
    if url_stats.clicked > 0:
        repeat_rate = (url_stats.clicked - url_stats.clicked_unique) / url_stats.clicked * 100
        print(f"   Repeat click rate: {repeat_rate:.1f}%")

# Get monthly click metrics for the current year
year_start = int(datetime(datetime.now().year, 1, 1).timestamp())
monthly_metrics = client.email.reporting.clicked_urls.list(
    start=year_start,
    stop=current_time,
    group="month"
)
print(f"\nMonthly URL click metrics for {datetime.now().year}")

# Analyze URL patterns and engagement
domains = {}
for url_stat in metrics.stats:
    domain = url_stat.url.split('/')[2]  # Extract domain from URL
    if domain not in domains:
        domains[domain] = {
            'total_clicks': 0,
            'unique_clicks': 0,
            'urls': 0
        }
    domains[domain]['total_clicks'] += url_stat.clicked
    domains[domain]['unique_clicks'] += url_stat.clicked_unique
    domains[domain]['urls'] += 1

print("\nDomain-level engagement:")
for domain, stats in sorted(domains.items(), key=lambda x: x[1]['unique_clicks'], reverse=True):
    print(f"\nDomain: {domain}")
    print(f"URLs: {stats['urls']}")
    print(f"Total clicks: {stats['total_clicks']}")
    print(f"Unique clicks: {stats['unique_clicks']}")
```

Notes:
- Timestamps:
  * Input parameters (`start`, `stop`) are in seconds since epoch
  * Response timestamps are in milliseconds since epoch
  * Default range is the past 7 days if no parameters provided
- Click metrics analysis:
  * High total clicks with low unique clicks suggests repeated engagement
  * URLs with high click rates but low conversion might indicate misleading content
  * Analyzing click patterns can help optimize email content and CTA placement
- Best practices:
  * Use meaningful URLs that indicate the content
  * Monitor click-through rates for different types of content
  * Track engagement patterns across different time periods
  * Consider the placement and context of links in your emails
- The difference between `clicked` and `clicked_unique` indicates how many recipients clicked multiple times on the same URL

## Error Handling

The Email API can raise the following exceptions:
- `NaxaiAPIRequestError`: Invalid parameters or server issues
- `NaxaiAuthenticationError`: Authentication failure
- `NaxaiAuthorizationError`: Insufficient permissions
- `NaxaiRateLimitExceeded`: Rate limit exceeded
- `ValidationError`: Invalid parameter values

## Best Practices

1. **Content Best Practices**
   - Always provide both HTML and text versions for better deliverability
   - Use inline CSS for HTML emails
   - Test emails across different email clients
   - Keep subject lines concise and relevant

2. **Attachment Guidelines**
   - Keep individual attachments under 10MB
   - Use appropriate MIME types
   - Base64 encode all binary content
   - Consider using links for large files instead of attachments

3. **Tracking and Analytics**
   - Enable tracking for marketing and important transactional emails
   - Monitor bounce rates and delivery issues
   - Track engagement metrics (opens, clicks)
   - Use unique tracking references for important emails

4. **Compliance and Security**
   - Include unsubscribe links in marketing emails
   - Honor recipient preferences and opt-outs
   - Follow email regulations (GDPR, CAN-SPAM)
   - Verify sender domains with SPF and DKIM
   - Use TLS for secure email transmission

## Related Documentation

- [Email Models](../models/email.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 