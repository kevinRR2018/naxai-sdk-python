# Error Handling

This guide covers error handling in the Naxai SDK, including exception types, error handling strategies, and best practices.

## Exception Hierarchy

### NaxaiException
Base exception class for all Naxai SDK errors.

```python
class NaxaiException(Exception):
    def __init__(self, message: str,
                 status_code: Optional[int] = None,
                 error_code: Optional[str] = None,
                 details: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
```

### Specific Exception Types

#### NaxaiAuthenticationError
Raised for authentication failures (401 errors).
```python
class NaxaiAuthenticationError(NaxaiException):
    """Raised when API credentials are invalid or expired."""
```

#### NaxaiAuthorizationError
Raised for authorization failures (403 errors).
```python
class NaxaiAuthorizationError(NaxaiException):
    """Raised when the request lacks sufficient permissions."""
```

#### NaxaiResourceNotFound
Raised when requested resources don't exist (404 errors).
```python
class NaxaiResourceNotFound(NaxaiException):
    """Raised when the requested resource is not found."""
```

#### NaxaiRateLimitExceeded
Raised when API rate limits are exceeded (429 errors).
```python
class NaxaiRateLimitExceeded(NaxaiException):
    """Raised when too many requests are made in a given time period."""
```

#### NaxaiInvalidRequestError
Raised for invalid request data (422 errors).
```python
class NaxaiInvalidRequestError(NaxaiException):
    """Raised when the request contains invalid data."""
```

#### NaxaiAPIRequestError
Raised for other API errors.
```python
class NaxaiAPIRequestError(NaxaiException):
    """Raised for general API errors not covered by other exceptions."""
```

#### NaxaiValueError
Raised for invalid client configuration.
```python
class NaxaiValueError(NaxaiException):
    """Raised when client initialization parameters are invalid."""
```

## Error Response Structure

API errors follow this structure:
```python
{
    "error": {
        "code": "error_code",        # Error type identifier
        "message": "Error message",   # Human-readable description
        "details": {                  # Additional error context
            "field1": "detail1",
            "field2": "detail2"
        }
    }
}
```

## Handling Errors

### Synchronous Usage

```python
from naxai import NaxaiClient
from naxai.base.exceptions import (
    NaxaiAuthenticationError,
    NaxaiRateLimitExceeded,
    NaxaiException
)
from naxai.models.email.requests import SendTransactionalEmailRequest, SenderObject, DestinationObject

try:
    with NaxaiClient(
            api_client_id="your_client_id",
            api_client_secret="your_client_secret"
    ) as client:
        response = client.email.transactional.send(
            SendTransactionalEmailRequest(
                sender=SenderObject(
                    email="sender@domain.com",
                    name="Sender"
                ),
                to=[
                    DestinationObject(
                        email="recipient@domain.com",
                        name="Recipient"
                    )
                ],
                subject="Test Email",
                text="Hello World")
        )
except NaxaiAuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    print(f"Status code: {e.status_code}")
    print(f"Error code: {e.error_code}")
except NaxaiRateLimitExceeded as e:
    print(f"Rate limit exceeded: {e.message}")
    print(f"Details: {e.details}")  # May contain retry_after information
except NaxaiException as e:
    print(f"API error: {e.message}")
    print(f"Status: {e.status_code}")
    print(f"Error code: {e.error_code}")
    print(f"Details: {e.details}")
```

### Asynchronous Usage

```python
from naxai import NaxaiAsyncClient
from naxai.base.exceptions import NaxaiException
import asyncio

async def send_email():
    try:
        async with NaxaiAsyncClient(
            api_client_id="your_client_id",
            api_client_secret="your_client_secret"
        ) as client:
            return await client.email.transactional.send(
                sender={"email": "sender@domain.com", "name": "Sender"},
                to=[{"email": "recipient@domain.com", "name": "Recipient"}],
                subject="Test Email",
                text="Hello World"
            )
    except NaxaiException as e:
        print(f"Error: {e.message} (Status: {e.status_code}, Code: {e.error_code})")
        raise

# Run the async function
asyncio.run(send_email())
```

## Best Practices

### 1. Use Context Managers

Always use the client with context managers to ensure proper resource cleanup:

```python
# Synchronous
with NaxaiClient(...) as client:
    client.sms.send(...)

# Asynchronous
async with NaxaiAsyncClient(...) as client:
    await client.sms.send(...)
```

### 2. Implement Retries for Rate Limits

```python
import time
from naxai.base.exceptions import NaxaiRateLimitExceeded

def send_with_retry(client, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.sms.send(...)
        except NaxaiRateLimitExceeded as e:
            if attempt == max_retries - 1:
                raise
            retry_after = e.details.get('retry_after', 60)
            time.sleep(retry_after)
```

### 3. Handle Authentication Errors

```python
from naxai.base.exceptions import NaxaiAuthenticationError

try:
    client.voice.call.create(...)
except NaxaiAuthenticationError as e:
    if e.status_code == 401:
        # Token expired, client will automatically refresh
        retry_request()
    else:
        # Invalid credentials
        log_authentication_failure(e)
        raise
```

### 4. Log Error Details

```python
import logging

logger = logging.getLogger(__name__)

try:
    client.webhooks.create(...)
except NaxaiException as e:
    logger.error(
        "API error occurred",
        extra={
            "status_code": e.status_code,
            "error_code": e.error_code,
            "message": e.message,
            "details": e.details
        }
    )
```

### 5. Validate Input Before Sending

```python
from pydantic import ValidationError

try:
    request = SendTransactionalEmailRequest(
        sender=sender_data,
        to=recipient_data,
        subject=subject,
        text=text_content
    )
    client.email.transactional.send(request)
except ValidationError as e:
    # Handle validation error before API call
    print(f"Invalid request data: {e.errors()}")
except NaxaiInvalidRequestError as e:
    # Handle API validation error
    print(f"API rejected request: {e.message}")
```

## Common Error Codes

| HTTP Status | Error Code | Description | Handling Strategy |
|------------|------------|-------------|-------------------|
| 401 | authentication_failed | Invalid or expired credentials | Refresh credentials or re-authenticate |
| 403 | permission_denied | Insufficient permissions | Check API key permissions |
| 404 | resource_not_found | Resource doesn't exist | Verify resource IDs and paths |
| 422 | invalid_request | Invalid request data | Validate input data |
| 429 | rate_limit_exceeded | Too many requests | Implement backoff and retry |
| 500 | server_error | Internal server error | Retry with exponential backoff |

## Related Documentation

- [API Reference](./api-reference.md)
- [Client Configuration](./configuration.md)
- [Best Practices](./best-practices.md) 