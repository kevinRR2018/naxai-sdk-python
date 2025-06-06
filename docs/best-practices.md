# Best Practices

This guide outlines best practices for using the Naxai SDK effectively, securely, and efficiently.

## Client Configuration

### Synchronous Client

```python
from naxai import NaxaiClient

# Use environment variables for credentials
client = NaxaiClient(
    api_client_id=os.environ.get("NAXAI_CLIENT_ID"),
    api_client_secret=os.environ.get("NAXAI_SECRET"),
    api_version=os.environ.get("NAXAI_API_VERSION"),  # Optional, defaults to latest
    auth_url=os.environ.get("NAXAI_AUTH_URL"),       # Optional, defaults to standard URL
    api_base_url=os.environ.get("NAXAI_API_URL")     # Optional, defaults to standard URL
)
```

### Asynchronous Client

```python
from naxai import NaxaiAsyncClient

async def initialize_client():
    client = NaxaiAsyncClient(
        api_client_id=os.environ.get("NAXAI_CLIENT_ID"),
        api_client_secret=os.environ.get("NAXAI_SECRET")
    )
    return client
```

## Resource Management

### Using Context Managers

Always use context managers to ensure proper resource cleanup:

```python
# Synchronous usage
with NaxaiClient(api_client_id="id", api_client_secret="secret") as client:
    response = client.email.send(
        sender={"email": "sender@domain.com", "name": "Sender"},
        to=[{"email": "recipient@domain.com", "name": "Recipient"}],
        subject="Hello",
        text="Hello World!"
    )

# Asynchronous usage
async with NaxaiAsyncClient(api_client_id="id", api_client_secret="secret") as client:
    response = await client.email.send(
        sender={"email": "sender@domain.com", "name": "Sender"},
        to=[{"email": "recipient@domain.com", "name": "Recipient"}],
        subject="Hello",
        text="Hello World!"
    )
```

### Manual Resource Cleanup

If not using context managers, ensure proper cleanup:

```python
# Synchronous
client = NaxaiClient(api_client_id="id", api_client_secret="secret")
try:
    # Use client
    response = client.sms.send(...)
finally:
    client.close()

# Asynchronous
client = NaxaiAsyncClient(api_client_id="id", api_client_secret="secret")
try:
    # Use client
    response = await client.sms.send(...)
finally:
    await client.aclose()
```

## Error Handling

### Comprehensive Exception Handling

```python
from naxai.base.exceptions import (
    NaxaiAuthenticationError,
    NaxaiAuthorizationError,
    NaxaiResourceNotFound,
    NaxaiRateLimitExceeded,
    NaxaiInvalidRequestError,
    NaxaiException
)

try:
    response = client.voice.call.create(
        to=["1234567890"],
        from_="0987654321",
        welcome={"say": "Welcome message"},
        language="en-GB"
    )
except NaxaiAuthenticationError as e:
    # Handle authentication failures
    logger.error(f"Authentication failed: {e.message}")
    refresh_credentials()
except NaxaiRateLimitExceeded as e:
    # Handle rate limiting
    retry_after = e.details.get('retry_after', 60)
    logger.warning(f"Rate limit exceeded, retry after {retry_after}s")
    time.sleep(retry_after)
except NaxaiResourceNotFound as e:
    # Handle missing resources
    logger.error(f"Resource not found: {e.message}")
    cleanup_invalid_reference()
except NaxaiException as e:
    # Handle all other API errors
    logger.error(f"API error: {e.message}", extra={
        "status_code": e.status_code,
        "error_code": e.error_code,
        "details": e.details
    })
```

### Implementing Retries

```python
import time
from naxai.base.exceptions import NaxaiRateLimitExceeded

def send_with_retry(client, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return client.sms.send(...)
        except NaxaiRateLimitExceeded as e:
            if attempt == max_retries - 1:
                raise
            delay = e.details.get('retry_after', base_delay * (2 ** attempt))
            time.sleep(delay)
```

## Authentication Best Practices

### Token Management

The SDK handles token management automatically:
- Tokens are acquired during the first API request
- Tokens are refreshed automatically when expired
- Token expiration is checked with a 60-second buffer

```python
# Token is managed automatically
with NaxaiClient(api_client_id="id", api_client_secret="secret") as client:
    # Token acquired on first request
    response1 = client.sms.send(...)
    
    # Same token reused if valid
    response2 = client.email.transactional.send(...)
    
    # Token refreshed automatically if expired
    response3 = client.voice.call.create(...)
```

### Secure Credential Storage

```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

client = NaxaiClient(
    api_client_id=os.environ["NAXAI_CLIENT_ID"],
    api_client_secret=os.environ["NAXAI_SECRET"]
)

# Or use a secrets manager
from aws_secretsmanager_caching import SecretCache

secret_cache = SecretCache()
credentials = secret_cache.get_secret_string("naxai/credentials")

client = NaxaiClient(
    api_client_id=credentials["client_id"],
    api_client_secret=credentials["client_secret"]
)
```

## Logging

The SDK includes built-in logging:

```python
import logging

# Configure logging
logger = logging.getLogger("naxai")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Create client with configured logger
client = NaxaiClient(
    api_client_id="id",
    api_client_secret="secret",
    logger=logger
)
```

## Model Validation

Use Pydantic models for request validation:

```python
from naxai.models.email import SendTransactionalEmailRequest
from pydantic import ValidationError

try:
    request = SendTransactionalEmailRequest.model_validate(
        sender={
            "email": "sender@domain.com",
            "name": "Sender Name"
        },
        to=[{
            "email": "recipient@domain.com",
            "name": "Recipient Name"
        }],
        subject="Hello",
        text="Hello World!",
        html="<p>Hello World!</p>"
    )
    response = client.email.transactional.send(request)
except ValidationError as e:
    logger.error("Invalid request data:", e.errors())
```

## Testing

### Using Environment Variables

```python
# test_config.py
import os
os.environ["NAXAI_CLIENT_ID"] = "test_client_id"
os.environ["NAXAI_SECRET"] = "test_client_secret"
os.environ["NAXAI_API_URL"] = "https://api.test.naxai.com"
```

### Mocking API Responses

```python
from unittest.mock import patch

def test_send_sms():
    with patch("naxai.client.NaxaiClient._request") as mock_request:
        mock_request.return_value = {
            "batch_id": "batch_123",
            "messages": [{"message_id": "msg_123"}]
        }
        
        with NaxaiClient(api_client_id="test", api_client_secret="test") as client:
            response = client.sms.send(
                to=["+1234567890"],
                text="Test message"
            )
            
        assert response["batch_id"] == "batch_123"
```

## Related Documentation

- [API Reference](./api-reference.md)
- [Error Handling](./error-handling.md)
- [Models Reference](./models/README.md) 