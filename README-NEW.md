# Naxai Python SDK

[![PyPI version](https://badge.fury.io/py/naxai.svg)](https://badge.fury.io/py/naxai)
[![Python Versions](https://img.shields.io/pypi/pyversions/naxai.svg)](https://pypi.org/project/naxai/)

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Authentication](#authentication)
- [Resource Hierarchy](#resource-hierarchy)
- [Detailed Examples](#detailed-examples)
- [API Reference](#api-reference)
  - [Voice API](#voice-api)
  - [SMS API](#sms-api)
  - [Email API](#email-api)
  - [People API](#people-api)
  - [Calendars API](#calendars-api)
  - [Webhooks API](#webhooks-api)
- [Type Definitions](#type-definitions)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Version Compatibility](#version-compatibility)
- [Response Types](#response-types)

## Overview

The Naxai Python SDK provides a simple and intuitive way to interact with Naxai's APIs. This SDK offers both synchronous and asynchronous clients for accessing various Naxai services including Voice, SMS, Email, Calendars, and People APIs.

⚠️ This SDK is a work in progress. Features and APIs may change until the release of version 1.0.0.

## Quick Start

```python
from naxai import NaxaiClient

# Initialize the client
client = NaxaiClient(
    api_client_id="your_client_id",
    api_client_secret="your_client_secret"
)

# Make a simple voice call
welcome = {"say": "Hello from Naxai!"}
response = client.voice.call.create(
    to=["1234567890"],
    from_="0987654321",
    language="en-GB",
    welcome=welcome
)

# Don't forget to close the client
client.close()
```

## Installation

```bash
pip install naxai
```

## Authentication

The SDK supports two authentication methods:

### Environment Variables (Recommended)
```bash
export NAXAI_CLIENT_ID="your_client_id"
export NAXAI_SECRET="your_client_secret"
```

```python
from naxai import NaxaiClient
client = NaxaiClient()  # Automatically uses environment variables
```

### Explicit Configuration
```python
from naxai import NaxaiClient

client = NaxaiClient(
    api_client_id="your_client_id",
    api_client_secret="your_client_secret"
)
```

## Resource Hierarchy

<details>
<summary>Voice</summary>

- **Call**
  - `create` - Create a new voice call
  
- **Broadcasts**
  - `create` - Create a new broadcast campaign
  - `list` - List all broadcasts
  - `get` - Get broadcast details
  - `update` - Update a broadcast
  - `start` - Start a broadcast
  - `pause` - Pause a broadcast
  - `resume` - Resume a broadcast
  - `cancel` - Cancel a broadcast
  - `delete` - Delete a broadcast
  
  - **Metrics**
    - `get` - Get broadcast metrics
    - **Input**
      - `get` - Get DTMF input metrics
  
  - **Recipients**
    - `list` - List broadcast recipients
    - `get` - Get recipient details
    - **Calls**
      - `list` - List recipient call attempts

- **Reporting**
  - **Inbound**
    - `list` - List inbound call metrics
  - **Outbound**
    - `list` - List outbound call metrics
    - `list_by_country` - List outbound metrics by country
  - **Transfer**
    - `list` - List transfer call metrics

- **Activity Logs**
  - `list` - List voice activity logs
</details>

<details>
<summary>SMS</summary>

- **Send**
  - `send` - Send SMS messages to one or more recipients

- **Activity Logs**
  - `list` - List SMS activity logs with filtering options
  - `get` - Get specific SMS activity details

- **Reporting**
  - **Outgoing**
    - `list_outgoing_metrics` - List outgoing SMS metrics
  - **Incoming**
    - `list_incoming_metrics` - List incoming SMS metrics
  - **Delivery Errors**
    - `list_delivery_errors` - List delivery error metrics
  - **By Country**
    - `list_by_country` - List metrics by country
</details>

<details>
<summary>Email</summary>

- **Send**
  - `send` - Send an email (convenience method)

- **Transactional**
  - `send` - Send transactional emails

- **Activity Logs**
  - `get` - Get email activity details
  - `list` - List email activity logs with filtering

- **Reporting**
  - **Metrics**
    - `list` - List email metrics
  - **Clicked URLs**
    - `list` - List clicked URL metrics
</details>

<details>
<summary>People</summary>

- **Contacts**
  - `search` - Search contacts
  - `count` - Count contacts
  - `create_or_update` - Create or update a contact
  - `get` - Get contact details
  - `delete` - Delete a contact
  
  - **Events**
    - `list` - List contact events
  - **Identifier**
    - `get` - Get contact by identifier
    - `update` - Update contact identifier
  - **Segments**
    - `list` - List contact segments

- **Attributes**
  - `create` - Create a new attribute
  - `get` - Get attribute details
  - `list` - List all attributes
  - `delete` - Delete an attribute

- **Segments**
  - `list` - List segments
  - `get` - Get segment details
  - `create` - Create a new segment
  - `update` - Update a segment
  - `delete` - Delete a segment
  - `get_history` - Get segment history
  - `get_usage` - Get segment usage
  
  - **Contacts**
    - `add` - Add contacts to segment
    - `delete` - Remove contacts from segment
    - `count` - Count contacts in segment
    - `list` - List contacts in segment
</details>

<details>
<summary>Calendars</summary>

- **Calendar**
  - `check` - Check calendar availability
  - `create` - Create a new calendar
  - `update` - Update a calendar
  - `get` - Get calendar details
  - `list` - List all calendars
  - `add_exclusions` - Add exclusion dates
  - `delete_exclusions` - Remove exclusion dates
  - `delete` - Delete a calendar

- **Holidays Templates**
  - `list` - List holiday templates
  - `get` - Get template details
</details>

<details>
<summary>Webhooks</summary>

- **Webhooks**
  - `list` - List all configured webhooks
  - `create` - Create a new webhook
  - `get` - Get webhook details
  - `update` - Update webhook configuration
  - `delete` - Delete a webhook
  - `list_last_events` - List recent events sent to webhook
  - `list_events` - List available event types
</details>

## Detailed Examples

<details>
<summary>Basic Usage Examples</summary>

### Voice Call
```python
from naxai import NaxaiClient
from naxai.models.voice.voice_flow import Welcome, End

async with NaxaiAsyncClient() as client:
    # Create welcome and end messages
    welcome = Welcome(say="Welcome to Naxai!")
    end = End(say="Goodbye!")
    
    # Make the call
    response = await client.voice.call.create(
        to=["1234567890"],
        from_="0987654321",
        language="en-GB",
        welcome=welcome,
        end=end
    )
    print(f"Call initiated with ID: {response.call_id}")
```

### Calendar Management
```python
from naxai import NaxaiClient
from naxai.models.calendars.requests import CreateCalendarRequest, ScheduleObject

with NaxaiClient() as client:
    # Create a business hours calendar
    schedule = [
        ScheduleObject(
            day=1,  # Monday
            open=True,
            start="09:00",
            stop="17:00"
        ),
        # ... repeat for all days
    ]
    
    calendar = CreateCalendarRequest(
        name="Business Hours",
        timezone="Europe/London",
        schedule=schedule
    )
    
    response = client.calendars.create(data=calendar)
    print(f"Calendar created with ID: {response.id}")
```

### Email Sending
```python
from naxai import NaxaiClient

with NaxaiClient() as client:
    email_data = {
        "to": ["recipient@example.com"],
        "from": "sender@yourdomain.com",
        "subject": "Hello from Naxai",
        "text": "This is a test email",
        "html": "<p>This is a test email</p>"
    }
    
    response = client.email.send(data=email_data)
    print(f"Email sent with ID: {response.message_id}")
```
</details>

<details>
<summary>Advanced Usage Examples</summary>

### Error Handling and Retries
```python
import asyncio
from naxai import NaxaiAsyncClient
from naxai.base.exceptions import NaxaiRateLimitExceeded

async def send_with_retry(client, data, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await client.email.send(data=data)
        except NaxaiRateLimitExceeded:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

async with NaxaiAsyncClient() as client:
    try:
        response = await send_with_retry(client, email_data)
    except NaxaiRateLimitExceeded:
        print("Failed after max retries")
```

### Batch Processing
```python
from naxai import NaxaiClient
import uuid

with NaxaiClient() as client:
    # Create a broadcast
    batch_id = str(uuid.uuid4())
    recipients = ["1234567890", "0987654321"]
    
    response = client.voice.broadcasts.create(data={
        "batchId": batch_id,
        "to": recipients,
        "from": "1111111111",
        "language": "en-GB",
        "welcome": {"say": "Welcome to our service"}
    })
    
    # Monitor progress
    metrics = client.voice.broadcasts.metrics.get(
        broadcast_id=response.broadcast_id
    )
    print(f"Completed: {metrics.completed}/{metrics.total}")
```
</details>

## API Reference

<details>
<summary>Voice API</summary>

### Call Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `create` | Create a new voice call | - `welcome: Welcome` (required)<br>- `language: Literal["fr-BE"...]` (required)<br>- `to: list[str]` (required)<br>- `from_: str` (required)<br>- `batch_id?: str`<br>- `voice?: Literal["man", "woman"]`<br>- `idempotency_key?: str`<br>- `calendar_id?: str`<br>- `scheduled_at?: int`<br>- `machine_detection?: bool`<br>- `voicemail?: VoiceMail`<br>- `menu?: Menu`<br>- `end?: End` | `CreateCallResponse` |

### Broadcasts Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `create` | Create a new broadcast campaign | `data: CreateBroadcastRequest` | `CreateBroadcastResponse` |
| `list` | List all broadcasts | None | `ListBroadcastResponse` |
| `get` | Get broadcast details | `broadcast_id: str` | `GetBroadcastResponse` |
| `update` | Update a broadcast | `broadcast_id: str, data: CreateBroadcastRequest` | `UpdateBroadcastResponse` |
| `start` | Start a broadcast | `broadcast_id: str` | None |
| `pause` | Pause a broadcast | `broadcast_id: str` | None |
| `resume` | Resume a broadcast | `broadcast_id: str` | None |
| `cancel` | Cancel a broadcast | `broadcast_id: str` | None |

#### Broadcasts Metrics Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get` | Get broadcast metrics | `broadcast_id: str` | `GetBroadcastMetricsResponse` |

#### Broadcasts Recipients Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List broadcast recipients | - `broadcast_id: str`<br>- `page?: int`<br>- `page_size?: int`<br>- `phone?: str`<br>- `completed?: bool`<br>- `status?: str` | `ListBroadcastRecipientsResponse` |

##### Recipients Calls Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get` | Get recipient call details | `broadcast_id: str, recipient_id: str` | `GetBroadcastRecipientCallsResponse` |

### Reporting Resource

#### Inbound Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List inbound call metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["hour", "day", "month"]`<br>- `phone?: str` | `ListInboundMetricsResponse` |

#### Outbound Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List outbound call metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["hour", "day", "month"]`<br>- `phone?: str` | `ListOutboundMetricsResponse` |
| `list_by_country` | List outbound metrics by country | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["hour", "day", "month"]` | `ListOutboundByCountryMetricsResponse` |

#### Transfer Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List transfer call metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["hour", "day", "month"]`<br>- `phone?: str` | `ListTransferMetricsResponse` |

### Activity Logs Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List voice activity logs | - `page?: int`<br>- `page_size?: int`<br>- `start?: int`<br>- `stop?: int`<br>- `direction?: Literal["inbound", "outbound", "transfer"]`<br>- `status?: Literal["delivered", "failed"]`<br>- `from_?: str`<br>- `to?: str`<br>- `client_id?: str`<br>- `campaign_id?: str`<br>- `broadcast_id?: str` | `ListVoiceActivityLogsResponse` |
</details>

<details>
<summary>Email API</summary>

### Transactional Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `send` | Send a transactional email | `data: SendTransactionalEmailRequest` | `SendTransactionalEmailResponse` |

### Activity Logs Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get` | Get email activity details | `message_id: str, email: str` | `GetEmailActivityLogsResponse` |
| `list` | List email activity logs | - `page?: int`<br>- `page_size?: int`<br>- `start?: int`<br>- `stop?: int`<br>- `sort?: str`<br>- `email?: str`<br>- `client_id?: str`<br>- `campaign_id?: str`<br>- `status?: Literal["sent", "delivered", "failed"]` | `ListEmailActivityLogsResponse` |

### Reporting Resource

#### Metrics Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List email metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["day", "month"]` | `ListMetricsResponse` |

#### Clicked URLs Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List clicked URL metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["day", "month"]` | `ListClickedUrlsMetricsResponse` |
</details>

<details>
<summary>SMS Types</summary>

### SendSMSRequest
```typescript
{
    to: string[];         // List of recipient phone numbers (max 1000)
    body: string;         // Message content (max 1530 chars)
    from?: string;        // Sender's phone number (8-15 chars)
    sender_service_id?: string;  // Alternative to from field
    type?: "text" | "unicode" | "auto";  // Message encoding (default: "text")
    scheduled_at?: string;  // ISO 8601 timestamp for scheduled delivery
    validity?: number;    // Message validity period in minutes (5-4320)
    idempotency_key?: string;  // Prevent duplicates (max 200 chars)
    reference?: string;   // Custom tracking reference (max 128 chars)
    calendar_id?: string; // Calendar ID for delivery constraints
    max_parts?: number;   // Maximum message parts (1-10)
    truncate?: boolean;   // Whether to truncate long messages
}
```

### SendSMSResponse
```typescript
{
    batch_id: string;     // Unique batch identifier
    count: number;        // Number of messages in batch
    messages: Array<{
        to: string;       // Recipient phone number
        message_id: string;  // Unique message identifier
    }>;
}
```

### SMSActivityLog
```typescript
{
    message_id: string;   // Unique message identifier
    direction: "inbound" | "outbound";
    status: "delivered" | "failed";
    from: string;         // Sender phone number
    to: string;          // Recipient phone number
    body: string;        // Message content
    created_at: number;  // Timestamp in milliseconds
    updated_at: number;  // Timestamp in milliseconds
    client_id?: string;
    campaign_id?: string;
    broadcast_id?: string;
}
```

### SMSMetrics
```typescript
{
    group: "hour" | "day" | "month";
    start_date?: string;  // ISO 8601 date
    stop_date?: string;   // ISO 8601 date
    metrics: Array<{
        timestamp: number;
        total: number;
        delivered: number;
        failed: number;
    }>;
}
```