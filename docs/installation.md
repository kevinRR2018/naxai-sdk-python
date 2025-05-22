# Installation & Authentication

This guide covers installing the Naxai SDK and setting up authentication for your application.

## Installation

### Using pip

```bash
pip install naxai
```

### Using poetry

```bash
poetry add naxai
```

### Requirements

- Python 3.7 or higher
- aiohttp (for async client)
- requests (for sync client)
- pydantic (for data validation)

## Authentication

The SDK supports two authentication methods:

### 1. Environment Variables (Recommended)

Set your credentials as environment variables:

```bash
# Linux/macOS
export NAXAI_CLIENT_ID="your_client_id"
export NAXAI_SECRET="your_client_secret"

# Windows (PowerShell)
$env:NAXAI_CLIENT_ID="your_client_id"
$env:NAXAI_SECRET="your_client_secret"

# Windows (Command Prompt)
set NAXAI_CLIENT_ID=your_client_id
set NAXAI_SECRET=your_client_secret
```

Then initialize the client:

```python
from naxai import NaxaiClient

# Client automatically uses environment variables
client = NaxaiClient()
```

### 2. Explicit Configuration

Pass credentials directly when creating the client:

```python
from naxai import NaxaiClient

client = NaxaiClient(
    api_client_id="your_client_id",
    api_client_secret="your_client_secret"
)
```

## Async vs Sync Clients

### Synchronous Client

```python
from naxai import NaxaiClient

with NaxaiClient() as client:
    response = client.voice.call.create(
        to=["1234567890"],
        from_="0987654321",
        welcome={"say": "Hello!"}
    )
```

### Asynchronous Client

```python
from naxai import NaxaiAsyncClient
import asyncio

async def main():
    async with NaxaiAsyncClient() as client:
        response = await client.voice.call.create(
            to=["1234567890"],
            from_="0987654321",
            welcome={"say": "Hello!"}
        )

asyncio.run(main())
```

## Client Configuration

### Timeout Settings

```python
client = NaxaiClient(
    timeout=30,  # Request timeout in seconds
    connect_timeout=10  # Connection timeout in seconds
)
```

### Custom Base URL

```python
client = NaxaiClient(
    base_url="https://api.custom-domain.com"
)
```

### Proxy Configuration

```python
client = NaxaiClient(
    proxy="http://proxy.example.com:8080"
)
```

## Best Practices

1. **Environment Variables**
   - Use environment variables in production
   - Keep credentials out of version control
   - Use different credentials for development and production

2. **Client Lifecycle**
   - Always use context managers (`with` statement)
   - Close clients when done to release resources
   - Create separate clients for long-running processes

3. **Error Handling**
   - Handle authentication errors gracefully
   - Implement proper retry logic for token expiration
   - Log authentication failures appropriately

Example with best practices:

```python
import os
from naxai import NaxaiClient
from naxai.base.exceptions import NaxaiAuthError

# Load configuration from environment
client_id = os.getenv("NAXAI_CLIENT_ID")
client_secret = os.getenv("NAXAI_SECRET")

if not all([client_id, client_secret]):
    raise ValueError("Missing required environment variables")

try:
    with NaxaiClient(
        api_client_id=client_id,
        api_client_secret=client_secret,
        timeout=30
    ) as client:
        # Your code here
        response = client.voice.call.create(...)
except NaxaiAuthError as e:
    logger.error(f"Authentication failed: {e}")
    # Handle authentication error
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle other errors
```

## Security Considerations

1. Never hardcode credentials in your code
2. Use environment variables or secure credential storage
3. Rotate credentials regularly
4. Use different credentials for different environments
5. Monitor authentication failures for security issues

## Troubleshooting

### Common Issues

1. **Invalid Credentials**
   ```python
   NaxaiAuthError: Invalid client credentials
   ```
   - Check if credentials are correct
   - Verify environment variables are set
   - Ensure credentials have necessary permissions

2. **Token Expiration**
   ```python
   NaxaiAuthError: Token expired
   ```
   - The SDK automatically handles token refresh
   - If persistent, check system clock synchronization

3. **Connection Issues**
   ```python
   NaxaiConnectionError: Failed to connect
   ```
   - Check network connectivity
   - Verify proxy settings if using a proxy
   - Check firewall rules

## Related Documentation

- [Quick Start Guide](./quick-start.md)
- [Error Handling](./error-handling.md)
- [Best Practices](./best-practices.md) 