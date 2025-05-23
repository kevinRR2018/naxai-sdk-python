# Best Practices

This guide outlines best practices for using the Naxai SDK effectively, securely, and efficiently.

## SDK Initialization

### Client Configuration

```python
from naxai import Client

# Best Practice: Use environment variables for sensitive data
client = Client(
    api_key=os.environ.get("NAXAI_API_KEY"),
    environment="production",  # or "sandbox" for testing
    timeout=30,  # Set reasonable timeouts
    max_retries=3  # Configure retry behavior
)
```

### Async Client Configuration

```python
from naxai import AsyncClient

async def initialize_client():
    client = AsyncClient(
        api_key=os.environ.get("NAXAI_API_KEY"),
        environment="production",
        max_connections=10  # Limit concurrent connections
    )
    return client
```

## Performance Optimization

### 1. Connection Pooling

```python
# Reuse client instances
client = Client(
    api_key=os.environ.get("NAXAI_API_KEY"),
    pool_connections=10,
    pool_maxsize=10
)

# Don't do this
def bad_practice():
    client = Client(api_key="...")  # Creates new connection pool each time
    client.email.send(...)
```

### 2. Batch Operations

```python
# Good: Use batch operations when possible
contacts = client.people.create_batch(data=[
    {"email": "user1@example.com", "name": "User 1"},
    {"email": "user2@example.com", "name": "User 2"},
    {"email": "user3@example.com", "name": "User 3"}
])

# Bad: Multiple individual requests
def bad_practice():
    for user in users:
        client.people.create(data=user)  # Creates separate request for each
```

### 3. Async Operations

```python
async def process_contacts(contacts):
    async with AsyncClient(api_key=os.environ.get("NAXAI_API_KEY")) as client:
        tasks = [
            client.people.get(contact_id)
            for contact_id in contacts
        ]
        results = await asyncio.gather(*tasks)
        return results
```

## Security Best Practices

### 1. API Key Management

```python
# Good: Use environment variables
api_key = os.environ.get("NAXAI_API_KEY")

# Good: Use secrets manager
from aws_secretsmanager_caching import SecretCache
secret_cache = SecretCache()
api_key = secret_cache.get_secret_string("NAXAI_API_KEY")

# Bad: Hardcoded credentials
api_key = "sk_live_..."  # Never do this
```

### 2. Webhook Security

```python
def verify_webhook(request):
    payload = request.get_data()
    signature = request.headers.get("X-Naxai-Signature")
    
    # Always verify webhook signatures
    if not client.webhooks.verify_signature(
        payload=payload,
        signature=signature,
        secret=os.environ.get("WEBHOOK_SECRET")
    ):
        raise SecurityError("Invalid webhook signature")
```

### 3. Data Validation

```python
# Validate input data before sending
def send_email(recipient, subject, content):
    if not is_valid_email(recipient):
        raise ValidationError("Invalid email address")
        
    if len(content) > MAX_CONTENT_LENGTH:
        raise ValidationError("Content exceeds maximum length")
        
    return client.email.send(data={
        "to": recipient,
        "subject": subject,
        "content": content
    })
```

## Error Handling

### 1. Proper Exception Handling

```python
try:
    result = client.email.send(data=email_data)
except ValidationError as e:
    # Handle validation errors
    logger.error(f"Validation error: {e.errors}")
    raise
except RateLimitError as e:
    # Implement backoff and retry
    logger.warning(f"Rate limit hit, retry after {e.retry_after}s")
    time.sleep(e.retry_after)
    retry_request()
except APIError as e:
    # Handle API errors
    logger.error(f"API error: {e.error_code}")
    handle_api_error(e)
```

### 2. Retry Strategy

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((RateLimitError, NetworkError))
)
def send_with_retry(client, data):
    return client.email.send(data=data)
```

## Resource Management

### 1. Context Managers

```python
# Use context managers for proper cleanup
async with AsyncClient(api_key=api_key) as client:
    await client.email.send(data=email_data)
```

### 2. Connection Cleanup

```python
# Ensure proper cleanup of resources
client = Client(api_key=api_key)
try:
    # Use client
    client.email.send(data=email_data)
finally:
    client.close()  # Always close when done
```

## Testing Best Practices

### 1. Use Test Environment

```python
# Use sandbox environment for testing
test_client = Client(
    api_key=os.environ.get("NAXAI_TEST_API_KEY"),
    environment="sandbox"
)
```

### 2. Mock API Responses

```python
from unittest.mock import patch

def test_send_email():
    with patch("naxai.resources.EmailResource.send") as mock_send:
        mock_send.return_value = {"message_id": "msg_123"}
        result = client.email.send(data=email_data)
        assert result["message_id"] == "msg_123"
```

### 3. Integration Tests

```python
def test_email_workflow():
    # Create test contact
    contact = client.people.create(data={
        "email": "test@example.com",
        "name": "Test User"
    })
    
    # Send test email
    email = client.email.send(data={
        "to": contact["email"],
        "subject": "Test Email",
        "content": "Hello World"
    })
    
    # Verify delivery
    status = client.email.get_status(email["message_id"])
    assert status["delivered"] is True
```

## Logging and Monitoring

### 1. Request Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("naxai")

def log_request(method, path, response):
    logger.info({
        "method": method,
        "path": path,
        "status": response.status_code,
        "duration": response.elapsed.total_seconds()
    })
```

### 2. Error Tracking

```python
def track_error(e: APIError):
    logger.error({
        "error_code": e.error_code,
        "status_code": e.status_code,
        "request_id": e.request_id,
        "timestamp": datetime.utcnow().isoformat()
    })
```

## Related Documentation

- [Error Handling](error-handling.md)
- [Response Types](response-types.md)
- [Version Compatibility](version-compatibility.md) 