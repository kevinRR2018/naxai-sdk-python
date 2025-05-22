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
  
  - **Metrics**
    - `get` - Get broadcast metrics
  
  - **Recipients**
    - `list` - List broadcast recipients
    - **Calls**
      - `get` - Get recipient call details

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
  
  - **Events**
    - `list` - List contact events
  - **Identifier**
    - `get` - Get contact by identifier
  - **Segments**
    - `list` - List contact segments

- **Segments**
  - `list` - List segments
  - `get` - Get segment details
  - `create` - Create a new segment
  - `update` - Update a segment
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
  - `create` - Create a webhook
  - `get` - Get webhook details
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

### SMSDeliveryError
```typescript
{
    code: string;        // Error code
    description: string; // Error description
    count: number;      // Number of occurrences
    percentage: number; // Percentage of total errors
}
```
</details>

<details>
<summary>Email Types</summary>

### BaseObject
```typescript
{
    email: string;        // Email address
    name: string;         // Display name
}
```

### SenderObject extends BaseObject
```typescript
{
    email: string;        // Verified sender email
    name: string;         // Sender display name
}
```

### DestinationObject extends BaseObject
```typescript
{
    email: string;        // Recipient email
    name: string;         // Recipient display name
}
```

### Attachment
```typescript
{
    id: string;           // Unique attachment ID
    name: string;         // Filename
    content_type: string; // MIME type
    data: string;         // Base64 encoded file content
}
```

### SendTransactionalEmailRequest
```typescript
{
    sender: SenderObject;
    to: DestinationObject[];  // Max 1000 recipients
    cc?: CCObject[];         // Max 50 recipients
    bcc?: BCCObject[];       // Max 50 recipients
    reply_to?: string;       // Reply-to address (max 100 chars)
    subject: string;
    text?: string;          // Plain text content
    html?: string;          // HTML content
    attachments?: Attachment[];  // Max 10 attachments
    enable_tracking?: boolean;
}
```

### EmailActivityLogs
```typescript
{
    message_id: string;
    from_email: string;
    to_email: string;
    subject?: string;
    status?: "sent" | "delivered" | "failed";
    created_at?: number;  // Timestamp in ms
    updated_at?: number;  // Timestamp in ms
    opens?: number;
    clicks?: number;
    events?: EmailEvents[];
    client_id?: string;
    campaign_id?: string;
}
```
</details>

<details>
<summary>People Types</summary>

### CreateSegmentRequest
```typescript
{
    name: string;
    description?: string;
    condition?: Condition;  // Required for dynamic segments
    type: "manual" | "dynamic";
}
```

### CreateAttributeRequest
```typescript
{
    name: string;
}
```

### SearchContactsRequest
```typescript
{
    page?: number;
    page_size?: number;
    sort?: string;
    condition?: SearchCondition;
}
```
</details>

<details>
<summary>People API</summary>

### Contacts Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `search` | Search contacts | - `page?: int`<br>- `page_size?: int`<br>- `sort?: str`<br>- `condition?: Union[dict, SearchCondition]` | `SearchContactsResponse` |
| `count` | Count contacts | None | `CountContactsResponse` |
| `create_or_update` | Create or update a contact | - `identifier: str`<br>- `email?: str`<br>- `external_id?: str`<br>- `unsubscribe?: bool`<br>- `language?: str`<br>- `created_at?: int`<br>- `**kwargs` | `CreateOrUpdateContactResponse` |
| `get` | Get contact details | `identifier: str` | `GetContactResponse` |

#### Contacts Events Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List contact events | `identifier: str` | `ListContactEventsResponse` |

#### Contacts Identifier Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get` | Get contact by identifier | `identifier: str` | `GetContactIdentifierResponse` |

#### Contacts Segments Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List contact segments | `identifier: str` | `ListSegmentsOfContactResponse` |

### Attributes Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `create` | Create a new attribute | `name: str` | `CreateAttributeResponse` |
| `get` | Get attribute details | `name: str` | `GetAttributeResponse` |
| `list` | List all attributes | None | `ListAttributesResponse` |
| `delete` | Delete an attribute | `name: str` | None |

### Segments Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List segments | - `type_?: str`<br>- `exclude_predefined?: bool`<br>- `attribute?: str` | `ListSegmentsResponse` |
| `get` | Get segment details | `segment_id: str` | `GetSegmentResponse` |
| `create` | Create a new segment | `data: CreateSegmentRequest` | `CreateSegmentResponse` |
| `update` | Update a segment | `segment_id: str, data: dict` | `UpdateSegmentResponse` |
| `get_history` | Get segment history | - `segment_id: str`<br>- `start_date: datetime`<br>- `end_date: datetime` | `GetSegmentsHistoryResponse` |
| `get_usage` | Get segment usage | `segment_id: str` | `GetSegmentUsageResponse` |

#### Segments Contacts Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `add` | Add contacts to segment | - `segment_id: str`<br>- `contact_ids: list[str]` | None |
| `delete` | Remove contacts from segment | - `segment_id: str`<br>- `contact_ids: list[str]` | None |
| `count` | Count contacts in segment | `segment_id: str` | `CountContactsInSegmentResponse` |
| `list` | List contacts in segment | - `segment_id: str`<br>- `page?: int`<br>- `page_size?: int`<br>- `sort?: str` | `ListContactsOfSegmentResponse` |
</details>

<details>
<summary>Calendars API</summary>

### Calendar Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `check` | Check calendar availability | - `calendar_id: str`<br>- `timestamp?: int` | `CheckCalendarResponse` |
| `create` | Create a new calendar | `data: CreateCalendarRequest` | `CreateCalendarResponse` |
| `update` | Update a calendar | - `calendar_id: str`<br>- `data: CreateCalendarRequest` | `UpdateCalendarResponse` |
| `get` | Get calendar details | `calendar_id: str` | `GetCalendarResponse` |
| `list` | List all calendars | None | `ListCalendarsResponse` |
| `add_exclusions` | Add exclusion dates | - `calendar_id: str`<br>- `exclusions: list[str]` | `AddExclusionsResponse` |
| `delete_exclusions` | Remove exclusion dates | - `calendar_id: str`<br>- `exclusions: list[str]` | `DeleteExclusionsResponse` |
| `delete` | Delete a calendar | `calendar_id: str` | None |

### Holidays Templates Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List holiday templates | None | `ListHolidaysTemplatesResponse` |
| `get` | Get template details | `template_id: str` | `GetHolidaysTemplateResponse` |
</details>

<details>
<summary>Webhooks API</summary>

### Webhooks Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `create` | Create a webhook | - `name: str`<br>- `url: str`<br>- `authentication: Union[BasicAuthModel, OAuth2AuthModel, HeaderAuthModel, NoAuthModel]`<br>- `event_object: Literal["All", "People", "Sms", "Email", "Call"]`<br>- `event_filter: List[str]`<br>- `event_names: List[str]`<br>- `active?: bool` | `CreateWebhookResponse` |
| `get` | Get webhook details | `webhook_id: str` | `GetWebhookResponse` |
</details>

## Type Definitions

<details>
<summary>Voice Types</summary>

### Welcome
```typescript
{
    say?: string;          // Text to be spoken
    prompt?: string;       // URL to audio file to play
    replay?: number;       // Number of times to replay (default: 0)
}
```

### VoiceMail
```typescript
{
    say?: string;          // Text to be spoken for voicemail
    prompt?: string;       // URL to audio file for voicemail
}
```

### Menu
```typescript
{
    say?: string;          // Text to be spoken as menu prompt
    prompt?: string;       // URL to audio file for menu prompt
    replay?: number;       // Number of times to replay menu (default: 0)
    choices: Choice[];     // List of available menu choices
}
```

### End
```typescript
{
    say?: string;          // Text to be spoken at end
    prompt?: string;       // URL to audio file to play at end
}
```

### CreateCallRequest
```typescript
{
    batch_id?: string;     // Unique identifier for grouping calls (max 64 chars)
    to: string[];         // List of recipient phone numbers (max 1000)
    from: string;         // Sender's phone number (8-15 chars)
    language: "fr-FR" | "fr-BE" | "nl-NL" | "nl-BE" | "en-GB" | "de-DE";
    voice: "woman" | "man";
    idempotency_key?: string;  // Key to prevent duplicates (1-128 chars)
    calendar_id?: string;  // Associated calendar ID
    scheduled_at?: number; // Timestamp for scheduled calls
    machine_detection?: boolean;  // Whether to detect answering machines
    voicemail?: VoiceMail;
    welcome: Welcome;      // Initial greeting configuration
    menu?: Menu;          // Interactive menu configuration
    end?: End;            // Call ending configuration
}
```

### CreateBroadcastRequest
```typescript
{
    name: string;         // Campaign name
    from: string;         // Sender's phone number (8-15 chars)
    source?: string;      // Source of broadcast (default: "people")
    segment_ids: string[]; // Target segment IDs (max 1)
    include_unsubscribed?: boolean;  // Include unsubscribed contacts
    language?: "fr-FR" | "fr-BE" | "nl-NL" | "nl-BE" | "en-GB" | "de-DE";
    voice?: "woman" | "man";
    scheduled_at?: string;  // Scheduled start time
    retries?: number;      // Number of retry attempts (0-3)
    retry_on_no_input?: boolean;
    retry_on_failed?: boolean;
    retry_delays?: number[];  // Delays between retries (0-3 values)
    calendar_id?: string;
    distribution?: "none" | "dynamic";
    dynamic_name?: string;
    voice_flow: VoiceFlow;
    actions?: Actions;
}
```</details><details><summary>Email Types</summary>

### BaseObject
```typescript
{
    email: string;        // Email address
    name: string;         // Display name
}
```

### SenderObject extends BaseObject
```typescript
{
    email: string;        // Verified sender email
    name: string;         // Sender display name
}
```

### DestinationObject extends BaseObject
```typescript
{
    email: string;        // Recipient email
    name: string;         // Recipient display name
}
```

### Attachment
```typescript
{
    id: string;           // Unique attachment ID
    name: string;         // Filename
    content_type: string; // MIME type
    data: string;         // Base64 encoded file content
}
```

### SendTransactionalEmailRequest
```typescript
{
    sender: SenderObject;
    to: DestinationObject[];  // Max 1000 recipients
    cc?: CCObject[];         // Max 50 recipients
    bcc?: BCCObject[];       // Max 50 recipients
    reply_to?: string;       // Reply-to address (max 100 chars)
    subject: string;
    text?: string;          // Plain text content
    html?: string;          // HTML content
    attachments?: Attachment[];  // Max 10 attachments
    enable_tracking?: boolean;
}
```

### EmailActivityLogs
```typescript
{
    message_id: string;
    from_email: string;
    to_email: string;
    subject?: string;
    status?: "sent" | "delivered" | "failed";
    created_at?: number;  // Timestamp in ms
    updated_at?: number;  // Timestamp in ms
    opens?: number;
    clicks?: number;
    events?: EmailEvents[];
    client_id?: string;
    campaign_id?: string;
}
```
</details>

<details>
<summary>People Types</summary>

### CreateSegmentRequest
```typescript
{
    name: string;
    description?: string;
    condition?: Condition;  // Required for dynamic segments
    type: "manual" | "dynamic";
}
```

### CreateAttributeRequest
```typescript
{
    name: string;
}
```

### SearchContactsRequest
```typescript
{
    page?: number;
    page_size?: number;
    sort?: string;
    condition?: SearchCondition;
}
```
</details>

<details>
<summary>Webhooks Types</summary>

### CreateWebhookRequest
```typescript
{
    name: string;
    url: string;
    authentication?: NoAuthModel | BasicAuthModel | OAuth2AuthModel | HeaderAuthModel;
    active?: boolean;
    event_object: "All" | "People" | "Sms" | "Call" | "Email";
    event_filter: string[];
    event_names: string[];
}
```

### Authentication Models

#### NoAuthModel
```typescript
{
    type: "none";
}
```

#### BasicAuthModel
```typescript
{
    type: "basic";
    username: string;
    password: string;
}
```

#### OAuth2AuthModel
```typescript
{
    type: "oauth2";
    token_url: string;
    client_id: string;
    client_secret: string;
    scope?: string[];
}
```

#### HeaderAuthModel
```typescript
{
    type: "header";
    name: string;
    value: string;
}
```
</details>

<details>
<summary>Calendar Types</summary>

### CreateCalendarRequest
```typescript
{
    name: string;
    timezone: string;
    schedule: ScheduleObject[];
}
```

### ScheduleObject
```typescript
{
    day: number;         // 1-7 (Monday-Sunday)
    open: boolean;
    start: string;       // "HH:mm" format
    stop: string;        // "HH:mm" format
}
```
</details>

## Error Handling

<details>
<summary>Common Errors</summary>

| Error Class | HTTP Code | Description | Resolution |
|-------------|-----------|-------------|------------|
| `NaxaiAuthenticationError` | 401 | Invalid credentials | Check API credentials |
| `NaxaiAuthorizationError` | 403 | Insufficient permissions | Verify account permissions |
| `NaxaiRateLimitExceeded` | 429 | Too many requests | Implement backoff strategy |
| `NaxaiAPIRequestError` | Various | General API error | Check error details |

### Example Error Handling
```python
from naxai.base.exceptions import (
    NaxaiAuthenticationError,
    NaxaiRateLimitExceeded,
    NaxaiAPIRequestError
)

try:
    response = client.voice.call.create(...)
except NaxaiAuthenticationError:
    # Handle authentication error
    print("Please check your credentials")
except NaxaiRateLimitExceeded:
    # Implement backoff
    print("Rate limit exceeded, please retry later")
except NaxaiAPIRequestError as e:
    # Handle other API errors
    print(f"API error: {e.message}")
```
</details>

## Best Practices

<details>
<summary>Resource Management</summary>

### Use Context Managers
```python
async with NaxaiAsyncClient() as client:
    # Client is automatically closed after the block
    await client.voice.call.create(...)
```

### Implement Rate Limiting
```python
from asyncio import sleep
from naxai.base.exceptions import NaxaiRateLimitExceeded

async def with_rate_limit(func, *args, max_retries=3):
    for i in range(max_retries):
        try:
            return await func(*args)
        except NaxaiRateLimitExceeded:
            if i == max_retries - 1:
                raise
            await sleep(2 ** i)
```

### Proper Error Handling
```python
def handle_api_error(e: NaxaiAPIRequestError):
    if isinstance(e, NaxaiRateLimitExceeded):
        # Handle rate limiting
        pass
    elif isinstance(e, NaxaiAuthenticationError):
        # Handle auth errors
        pass
    else:
        # Handle other errors
        pass
```
</details>

## Version Compatibility

| SDK Version | API Version | Python Version | Release Date | Status |
|-------------|-------------|----------------|--------------|---------|
| 1.0.0 | 2023-03-25 | ≥3.7 | 2023-03-25 | Stable |
| 0.9.0 | 2023-02-15 | ≥3.7 | 2023-02-15 | Beta |
| 0.8.0 | 2023-01-10 | ≥3.7 | 2023-01-10 | Beta |

## Response Types

<details>
<summary>Voice API Responses</summary>

### CreateCallResponse
```typescript
{
    call_id: string;
    status: "queued" | "in-progress" | "completed" | "failed";
    created_at: number;  // Unix timestamp in milliseconds
    updated_at: number;  // Unix timestamp in milliseconds
    from: string;
    to: string[];
    // ...
}
```

### ListBroadcastResponse
```typescript
{
    broadcasts: Array<{
        id: string;
        status: string;
        total_recipients: number;
        completed: number;
        // ...
    }>;
    pagination: {
        page: number;
        total_pages: number;
        total_items: number;
    };
}
```

[View all response types](#)
</details>

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 