📚 Naxai Python SDK Documentation
Welcome to the official Naxai Python SDK!

This SDK provides easy, Pythonic, and asynchronous access to Naxai's APIs, including Voice, SMS, Email, and RCS services (only Voice is currently implemented).

📦 Installation
```bash
pip install naxai
```


🚀 Quick Start
```python
import asyncio
from naxai import NaxaiAsyncClient
from naxai.models.voice.voice_flow import Welcome, End
from naxai.models.voice.create_call_request import CreateCallRequest

async def main():
    client = NaxaiAsyncClient(
        api_client_id="your_client_id",
        api_client_secret="your_client_secret",
        auth_url="https://auth.naxai.com/oauth2/token",
        api_base_url="https://api.naxai.com"
    )

    # Example: Create a voice call
    welcome = Welcome(say="Welcome to the Naxai demo")
    end = End(say="Thank you to have used the Naxai demo")
    call_request = CreateCallRequest(
        batchId=str(uuid.uuid4()),
        to=["123456789"],
        from_="123456789",
        language="en-GB",
        voice="man",
        idempotencyKey=str(uuid.uuid4()),
        machineDetection=False,
        welcome=welcome,
        end=end,
        scheduledAt=int(datetime.datetime.now(tz=datetime.timezone.utc)).timestamp()
    )

    response = await client.voice.call.create(data=call_request)
    print(response)

    await client.aclose()

asyncio.run(main())
```
🏗 Client Structure
The main entrypoint are:

```python
from naxai import NaxaiAsyncClient
from naxai import NaxaiClient
```
NaxaiAsyncClient is an async client, using httpx.AsyncClient under the hood.
NaxaiClient is synchronous client, using httpx.Client under the hood.

Resources are available as properties:
(e.g., client.voice, client.sms, client.email, client.rcs — only voice currently implemented.)

📋 Current Supported Resources

| Resource | Status | Example Access |
|----------|--------|----------------|
| Voice | ✅ Implemented | client.voice.call.create(...) |
| SMS | 🚧 | Not yet |	
| Email | 🚧 | Not yet |
| RCS | 🚧 | Not yet |

📖 API Methods
Inside voice, you can:

Method	Description
client.voice.call.create(data)	Create a new voice call.
client.voice.call.cancel(call_id)	Cancel a scheduled voice call.

⚙ Authentication
Authentication is automatic:

When you first perform an action, the SDK will authenticate using the provided client_id and client_secret.
If no client_id or client_secret are provided, environment variables NAXAI_CLIENT_ID and NAXAI_SECRET will be used.

The access token is automatically stored and refreshed when needed (valid for 24 hours).

🧹 Closing the client
Always close the HTTP session after usage:

```python
# Async client
await client.aclose()
# Synchronous client
client.close()
```
(This properly releases network resources.)

🛠 Error Handling
All exceptions inherit from NaxaiException, found under naxai.base.exceptions.

Common exceptions:


| Exception | When it Happens |
|-----------|-----------------|
| NaxaiAuthenticationError | Authentication failed |
| NaxaiAuthorizationError | Access forbidden |
| NaxaiResourceNotFound | Resource not found (404) |
| NaxaiRateLimitExceeded | Rate limit hit |
| NaxaiAPIRequestError | Generic API error |
| NaxaiValueError | Incorrect parameter value |

Example:
```python
try:
    await client.voice.call.create(data={...})
except NaxaiException as e:
    print(f"API call failed: {e}")
```
📓 Logging
The SDK supports custom logging.

Pass your own logger into NaxaiAsyncClient to integrate with your application's logging system.

Example:
```python
import logging

logger = logging.getLogger("naxai")
logger.setLevel(logging.DEBUG)

client = NaxaiAsyncClient(
    api_client_id="xxx",
    api_client_secret="xxx",
    auth_url="xxx",
    api_base_url="xxx",
    logger=logger
)
```
⏳ Roadmap
 🚧 Add SMS resource

 🚧 Add Email resource

 🚧 Add RCS resource

 🚧 Add Webhook resource

 ✅ Provide a client for synchronous code

 ✅ Publish SDK on PyPI

 🚧 Improve type hints for auto-completion and IDE support

🤝 Contributing
Coming soon!

📜 License
MIT License (or your preferred license)
