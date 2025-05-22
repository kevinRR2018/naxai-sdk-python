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
  - `get` - Get specific call details
</details>

<details>
<summary>SMS</summary>

- `send` - Send SMS messages to one or more recipients

- **Activity Logs**
  - `list` - List SMS activity logs with filtering options
  - `get` - Get specific SMS activity details

- **Reporting**
  - `list_outgoing_metrics` - List outgoing SMS metrics
  - `list_incoming_metrics` - List incoming SMS metrics
  - `list_delivery_errors` - List delivery error metrics
  - `list_by_country` - List metrics by country
</details>

<details>
<summary>Email</summary>

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
    - `send` - Send an event for a specific contact.
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

### SMS Sending
```python
from naxai import NaxaiClient

with NaxaiClient() as client:
    # Send a simple SMS
    response = client.sms.send(
        to="1234567890",
        from_="0987654321",
        text="Hello from Naxai SDK!"
    )
    print(f"Message sent with ID: {response.message_id}")

    # Send SMS to multiple recipients
    response = client.sms.send(
        to=["1234567890", "1234567891", "1234567892"],
        from_="0987654321",
        text="Bulk message from Naxai SDK!",
        idempotency_key="unique-key-123"  # Optional: prevent duplicate sends
    )
    print(f"Bulk message sent to {len(response.messages)} recipients")

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
    segment_id = "<my_segment_id>"
    
    response = client.voice.broadcasts.create(data={
        "batchId": batch_id,
        "from": "1111111111",
        "language": "en-GB",
        "welcome": {"say": "Welcome to our service"},
        "segmentId": segment_id
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
| `delete` | Delete a broadcast | `broadcast_id: str` | None |

#### Broadcasts Metrics Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get` | Get broadcast metrics | `broadcast_id: str` | `GetBroadcastMetricsResponse` |

##### Metrics Input Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get` | Get DTMF input metrics | `broadcast_id: str` | `GetBroadcastInputMetricsResponse` |

#### Broadcasts Recipients Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List broadcast recipients | - `broadcast_id: str`<br>- `page?: int`<br>- `page_size?: int`<br>- `phone?: str`<br>- `completed?: bool`<br>- `status?: str` | `ListBroadcastRecipientsResponse` |
| `get` | Get recipient details | `broadcast_id: str, recipient_id: str` | `GetBroadcastRecipientResponse` |

##### Recipients Calls Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List recipient call attempts | `broadcast_id: str, recipient_id: str` | `ListBroadcastRecipientCallsResponse` |

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
| `get` | Get specific call details | `call_id: str` | `GetVoiceActivityLogResponse` |
</details>

<details><summary>SMS API</summary>

### SMS Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `send` | Send SMS messages | - `to: str \| list[str]` (required)<br>- `from_: str` (required)<br>- `text: str` (required)<br>- `idempotency_key?: str`<br>- `scheduled_at?: int`<br>- `calendar_id?: str`<br>- `batch_id?: str` | `SendSMSResponse` |

### Activity Logs Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List SMS activity logs | - `page?: int`<br>- `page_size?: int`<br>- `start?: int`<br>- `stop?: int`<br>- `status?: str`<br>- `from_?: str`<br>- `to?: str`<br>- `batch_id?: str`<br>- `direction?: Literal["inbound", "outbound"]` | `ListSMSActivityLogsResponse` |
| `get` | Get specific SMS details | `message_id: str` | `GetSMSActivityLogResponse` |

### Reporting Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list_outgoing_metrics` | List outgoing SMS metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["hour", "day", "month"]`<br>- `from_?: str`<br>- `to?: str` | `ListOutgoingMetricsResponse` |
| `list_incoming_metrics` | List incoming SMS metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["hour", "day", "month"]`<br>- `from_?: str`<br>- `to?: str` | `ListIncomingMetricsResponse` |
| `list_delivery_errors` | List delivery error metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["hour", "day", "month"]`<br>- `error_code?: str` | `ListDeliveryErrorsResponse` |
| `list_by_country` | List metrics by country | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["hour", "day", "month"]`<br>- `country?: str` | `ListByCountryMetricsResponse` |
</details>

<details>
<summary>Email API</summary>

### Email Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `send` | Send an email (convenience method) | - `sender_email: str` (required)<br>- `sender_name: str` (required)<br>- `subject: str` (required)<br>- `to: List[DestinationObject]` (required, max 1000)<br>- `cc?: List[CCObject]` (max 50)<br>- `bcc?: List[BCCObject]` (max 50)<br>- `reply_to?: str`<br>- `text?: str`<br>- `html?: str`<br>- `attachments?: List[Attachment]`<br>- `enable_tracking?: bool` | `SendTransactionalEmailResponse` |

### Transactional Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `send` | Send a transactional email | `data: SendTransactionalEmailRequest` | `SendTransactionalEmailResponse` |

### Activity Logs Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List email activity logs | - `email: str`<br>- `status?: str`<br>- `page?: int`<br>- `limit?: int` | `ListEmailActivityLogsResponse` |
| `get` | Get specific email details | - `message_id: str`<br>- `email: str` | `GetEmailActivityLogResponse` |

### Reporting Resource

#### Metrics Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List email metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["day", "month"]` | `ListMetricsResponse` |

#### Clicked URLs Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List clicked URL metrics | - `start?: int`<br>- `stop?: int`<br>- `group?: Literal["day", "month"]` | `ListClickedURLMetricsResponse` |
</details>

<details>
<summary>People API</summary>

### Contacts Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `search` | Search contacts | - `page?: int` (default=1)<br>- `page_size?: int` (default=50)<br>- `sort?: str` (default="createdAt:desc")<br>- `condition?: Union[dict, SearchCondition]` | `SearchContactsResponse` |
| `count` | Count total contacts | None | `CountContactsResponse` |
| `create_or_update` | Create or update a contact | - `identifier: str` (required)<br>- `email?: str`<br>- `external_id?: str`<br>- `unsubscribe?: bool`<br>- `language?: str`<br>- `created_at?: int`<br>- `**kwargs` | `CreateOrUpdateContactResponse` |
| `get` | Get contact details | `identifier: str` | `GetContactResponse` |
| `delete` | Delete a contact | `identifier: str` | None |

#### Events Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `send` | Send an event for a contact | - `identifier: str` (required)<br>- `name?: str`<br>- `type_?: str`<br>- `timestamp?: int`<br>- `idempotency_key?: str`<br>- `data?: dict[str,str]` | None |

#### Identifier Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get` | Get contact by identifier | `identifier: str` | `GetContactResponse` |
| `update` | Update contact identifier | - `identifier: str` (required)<br>- `new_identifier: str` (required) | None |

#### Segments Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list` | List contact segments | `identifier: str` | `ListContactSegmentsResponse` |

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
| `list` | List segments | - `type_?: str`<br>- `exclude_predefined?: bool` (default=False)<br>- `attribute?: str` | `ListSegmentsResponse` |
| `get` | Get segment details | `segment_id: str` | `GetSegmentResponse` |
| `create` | Create a new segment | `data: CreateSegmentRequest` | `CreateSegmentResponse` |
| `update` | Update a segment | - `segment_id: str`<br>- `data: CreateSegmentRequest` | `UpdateSegmentResponse` |
| `delete` | Delete a segment | `segment_id: str` | None |
| `get_history` | Get segment history | - `segment_id: str`<br>- `start?: int` (default=30 days ago)<br>- `stop?: int` (default=now) | `GetSegmentsHistoryResponse` |
| `get_usage` | Get segment usage | `segment_id: str` | `GetSegmentUsageResponse` |

#### Segments Contacts Resource
| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `add` | Add contacts to segment | - `segment_id: str`<br>- `contact_ids: list[str]` (min length=1) | None |
| `delete` | Remove contacts from segment | - `segment_id: str`<br>- `contact_ids: list[str]` | None |
| `count` | Count contacts in segment | `segment_id: str` | `CountSegmentContactsResponse` |
| `list` | List contacts in segment | - `segment_id: str`<br>- `page?: int` (default=1)<br>- `page_size?: int` (default=50)<br>- `sort?: str` (default="createdAt:desc") | `ListSegmentContactsResponse` |
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
| `list` | List all webhooks | None | `ListWebhooksResponse` |
| `create` | Create a new webhook | `data: CreateWebhookRequest` | `CreateWebhookResponse` |
| `get` | Get webhook details | `webhook_id: str` | `GetWebhookResponse` |
| `update` | Update webhook configuration | - `webhook_id: str`<br>- `data: UpdateWebhookRequest` | `UpdateWebhookResponse` |
| `delete` | Delete a webhook | `webhook_id: str` | None |
| `list_last_events` | List recent webhook events | `webhook_id: str` | `ListWebhookEventsResponse` |
| `list_events` | List available event types | None | `ListEventTypesResponse` |
</details>

## Type Definitions

## Error Handling

## Best Practices

## Version Compatibility

## Response Types
