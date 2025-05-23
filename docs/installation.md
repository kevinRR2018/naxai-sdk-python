# Installation & Authentication

This guide covers installing the Naxai SDK and setting up authentication for your application.

## Installation

### Using pip

```bash
pip install naxai
```

### Requirements

- httpx
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
    api_client_id="api_client_id",
    api_client_secret="api_client_secret",
    api_version="2023-03-25",                       # has default value
    auth_url="https://auth.naxai.com/oauth2/token", # has default value
    api_base_url="https://api.naxai.com"            # has default value
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
        api_client_secret=client_secret
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

## Related Documentation

- [Quick Start Guide](./quick-start.md)
- [Error Handling](./error-handling.md)
- [Best Practices](./best-practices.md) 