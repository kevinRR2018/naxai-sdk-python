# Error Handling

This guide covers error handling in the Naxai SDK, including common exceptions, error types, and best practices for handling errors.

## Exception Types

### NaxaiError
Base exception class for all Naxai SDK errors.

```python
class NaxaiError(Exception):
    """Base exception for all Naxai SDK errors."""
    pass
```

### APIError
Raised when the API returns an error response.

```python
class APIError(NaxaiError):
    def __init__(self, message: str, status_code: int, error_code: str, request_id: str):
        self.status_code = status_code
        self.error_code = error_code
        self.request_id = request_id
        super().__init__(message)
```

### ValidationError
Raised when request validation fails.

```python
class ValidationError(NaxaiError):
    def __init__(self, message: str, errors: Dict[str, List[str]]):
        self.errors = errors
        super().__init__(message)
```

### AuthenticationError
Raised for authentication failures.

```python
class AuthenticationError(APIError):
    pass
```

### RateLimitError
Raised when API rate limits are exceeded.

```python
class RateLimitError(APIError):
    def __init__(self, message: str, retry_after: int, *args, **kwargs):
        self.retry_after = retry_after
        super().__init__(message, *args, **kwargs)
```

## Common Error Codes

| Error Code | Description | HTTP Status | Handling Strategy |
|------------|-------------|-------------|-------------------|
| `authentication_failed` | Invalid API credentials | 401 | Verify API key and permissions |
| `invalid_request` | Malformed request data | 400 | Check request parameters |
| `rate_limit_exceeded` | Too many requests | 429 | Implement backoff and retry |
| `resource_not_found` | Requested resource doesn't exist | 404 | Verify resource IDs |
| `permission_denied` | Insufficient permissions | 403 | Check account permissions |
| `service_error` | Internal service error | 500 | Retry with exponential backoff |

## Error Handling Best Practices

### 1. Use Try-Except Blocks

```python
try:
    response = client.email.send(data={
        "to": "recipient@example.com",
        "subject": "Test Email",
        "content": "Hello World"
    })
except ValidationError as e:
    logger.error(f"Invalid request data: {e.errors}")
    # Handle validation errors
except RateLimitError as e:
    logger.warning(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
    time.sleep(e.retry_after)
    # Retry request
except APIError as e:
    logger.error(f"API error: {e.error_code} ({e.status_code})")
    # Handle API errors
except NaxaiError as e:
    logger.error(f"Unexpected error: {e}")
    # Handle unexpected errors
```

### 2. Implement Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(RateLimitError)
)
def send_email_with_retry(client, data):
    return client.email.send(data=data)
```

### 3. Log Error Details

```python
def log_api_error(e: APIError):
    logger.error({
        "error": str(e),
        "status_code": e.status_code,
        "error_code": e.error_code,
        "request_id": e.request_id,
        "timestamp": datetime.utcnow().isoformat()
    })
```

### 4. Handle Async Errors

```python
async def handle_webhook_async(event_data):
    try:
        await process_event(event_data)
    except ValidationError as e:
        await log_validation_error(e)
        raise
    except APIError as e:
        await log_api_error(e)
        # Determine if event should be retried
        if is_retryable_error(e):
            await requeue_event(event_data)
```

## Error Response Structure

API errors follow this structure:

```python
{
    "error": {
        "code": "rate_limit_exceeded",
        "message": "API rate limit exceeded",
        "request_id": "req_abc123",
        "details": {
            "retry_after": 30
        }
    }
}
```

## Handling Specific Scenarios

### Rate Limiting

```python
def handle_rate_limit(e: RateLimitError):
    """Handle rate limit errors with exponential backoff."""
    retry_after = e.retry_after
    
    for attempt in range(3):
        try:
            time.sleep(retry_after)
            # Retry the request
            return make_request()
        except RateLimitError as e:
            retry_after *= 2
    
    # Max retries exceeded
    raise MaxRetriesExceeded()
```

### Validation Errors

```python
def handle_validation_error(e: ValidationError):
    """Handle validation errors with detailed logging."""
    for field, errors in e.errors.items():
        for error in errors:
            logger.error(f"Validation error in {field}: {error}")
    
    # Clean/fix data if possible
    if can_fix_data(e.errors):
        return fix_and_retry()
    else:
        raise DataValidationFailed()
```

### Network Errors

```python
def handle_network_error(e: RequestException):
    """Handle network-related errors."""
    if isinstance(e, ConnectTimeout):
        logger.warning("Connection timeout - retrying")
        return retry_with_backoff()
    elif isinstance(e, ReadTimeout):
        logger.warning("Read timeout - retrying")
        return retry_with_backoff()
    else:
        logger.error(f"Network error: {e}")
        raise NetworkError(str(e))
```

## Related Documentation

- [Best Practices](best-practices.md)
- [Response Types](response-types.md)
- [Version Compatibility](version-compatibility.md) 