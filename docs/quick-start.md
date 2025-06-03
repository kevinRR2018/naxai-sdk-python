# Quick Start Guide

This guide will help you get started with the Naxai Python SDK quickly.

## Installation

```bash
pip install naxai
```

## Basic Usage

### Initialize the Client

```python
from naxai import NaxaiClient

# Using environment variables
client = NaxaiClient()  # Uses NAXAI_CLIENT_ID and NAXAI_SECRET

# Or explicit configuration
client = NaxaiClient(
    api_client_id="your_client_id",
    api_client_secret="your_client_secret"
)
```

### Make a Voice Call

```python
# Create welcome and end messages
welcome = {"say": "Hello from Naxai!"}
end = {"say": "Goodbye!"}

# Make the call
response = client.voice.call.create(
    to=["1234567890"],
    from_="0987654321",
    language="en-GB",
    welcome=welcome,
    end=end
)
print(f"Call initiated with ID: {response.calls[0].call_id}")
```

### Send an SMS

```python
# Send to single recipient
response = client.sms.send(
    to="1234567890",
    from_="0987654321",
    body="Hello from Naxai SDK!"
)

# Send to multiple recipients
response = client.sms.send(
    to=["1234567890", "1234567891"],
    from_="0987654321",
    body="Bulk message from Naxai SDK!"
)
```



### Send an Email

```python
# Send to recipient@example.com
response = client.email.send(
            sender_email="sender@yourdomain.com",
            sender_name="sender",
            subject="Hello from Naxai",
            text="This is a test email",
            to=[{"email": "recipient@example.com", "name": "Recipient"}])
print(f"Email sent with ID: {response.message_id}")
```

### Manage Contacts

```python
# Create or update a contact. Identifier = email
contact = client.people.contacts.create_or_update(
    identifier="user@example.com",
    email="user@example.com",
    phone="1234567890",
    language="en",
    external_id="USER_123"
)

# Search contacts
results = client.people.contacts.search(
    condition={
        "all": [
            {"attribute": {"field": "country", "operator": "eq", "value": "US"}},
            {"attribute": {"field": "language", "operator": "eq", "value": "en"}}
        ]
    }
)
```

## Next Steps

- Check the [Installation & Authentication](./installation.md) guide for detailed setup
- Explore the API Reference for each service:
  - [Voice API](./api/voice.md)
  - [SMS API](./api/sms.md)
  - [Email API](./api/email.md)
  - [People API](./api/people.md)
- Review [Best Practices](./best-practices.md) for production use 