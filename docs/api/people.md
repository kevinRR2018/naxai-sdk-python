# People API Reference

The People API allows you to manage contacts, custom attributes, and segments in your Naxai account. It provides comprehensive customer data management capabilities including contact profiles, custom attributes, segmentation, and contact events tracking.

## Attributes Resource

The Attributes resource allows you to manage custom attributes that define the structure of contact profiles.

### Create Attribute
```python
client.people.attributes.create(
    name: str    # Name of the attribute to create
)
```

Returns: [CreateAttributeResponse](../models/people.md#createattributeresponse)

Example:
```python
# Create a custom attribute
attribute = client.people.attributes.create(name="loyalty_tier")
print(f"Created attribute: {attribute.name}")
```

### Get Attribute
```python
client.people.attributes.get(
    name: str    # Name of the attribute to retrieve
)
```

Returns: [CreateAttributeResponse](../models/people.md#createattributeresponse)

Example:
```python
# Get attribute details
attribute = client.people.attributes.get(name="loyalty_tier")
print(f"Attribute: {attribute.name}")
if attribute.segment_ids:
    print(f"Used in {len(attribute.segment_ids)} segments")
```

### List Attributes
```python
client.people.attributes.list()
```

Returns: [ListAttributesResponse](../models/people.md#listattributesresponse)

Example:
```python
# List all attributes
attributes = client.people.attributes.list()
print(f"Found {len(attributes)} attributes")

# Group by type
system_attrs = []
custom_attrs = []
for attr in attributes:
    if attr.name.startswith("system_"):
        system_attrs.append(attr.name)
    else:
        custom_attrs.append(attr.name)

print(f"\n{len(system_attrs)} System Attributes:")
for name in sorted(system_attrs):
    print(f"- {name}")

print(f"\n{len(custom_attrs)} Custom Attributes:")
for name in sorted(custom_attrs):
    print(f"- {name}")
```

### Delete Attribute
```python
client.people.attributes.delete(
    name: str    # Name of the attribute to delete
)
```

Returns: None

Example:
```python
# Delete a custom attribute
client.people.attributes.delete(name="old_attribute")
```

## Contacts Resource

The Contacts resource provides methods for managing contact profiles and their data.

### Search Contacts
```python
client.people.contacts.search(
    page: Optional[int] = 1,                # Page number (default: 1)
    page_size: Optional[int] = 50,          # Items per page (default: 50)
    sort: Optional[str] = "createdAt:desc", # Sort order
    condition: Optional[SearchCondition] = None  # Search conditions
)
```

Request: [SearchCondition](../models/people.md#searchcondition)  
Returns: [SearchContactsResponse](../models/people.md#searchcontactsresponse)

Example:
```python
from naxai.models.people.helper_models.search_condition import SearchCondition

# Search for active US customers
condition = SearchCondition(
    all=[
        {"attribute": {"field": "country", "operator": "eq", "value": "US"}},
        {"attribute": {"field": "status", "operator": "eq", "value": "active"}}
    ]
)

results = client.people.contacts.search(
    page=1,
    page_size=25,
    sort="email:asc",
    condition=condition
)

print(f"Found {results.pagination.total_items} matching contacts")
for contact in results.contacts:
    print(f"- {contact.email} (ID: {contact.nx_id})")
```

### Count Contacts
```python
client.people.contacts.count()
```

Returns: [CountContactsResponse](../models/people.md#countcontactsresponse)

Example:
```python
# Get total number of contacts
total_contacts = client.people.contacts.count()
print(f"Total contacts: {total_contacts}")
```

### Create or Update Contact
```python
client.people.contacts.create_or_update(
    identifier: str,              # Contact identifier (email/phone/external_id)
    email: Optional[str] = None,  # Email address
    external_id: Optional[str] = None,  # External identifier
    unsubscribe: Optional[bool] = None,  # Unsubscribe status
    language: Optional[str] = None,  # Preferred language code
    created_at: Optional[int] = None,  # Creation timestamp
    **kwargs  # Additional custom attributes
)
```

Request: [CreateOrUpdateContactRequest](../models/people.md#createorupdatecontactrequest)  
Returns: [CreateOrUpdateContactResponse](../models/people.md#createorupdatecontactresponse)

Example:
```python
# Create or update a contact
response = client.people.contacts.create_or_update(
    identifier="john.doe@example.com",
    email="john.doe@example.com",
    external_id="CUST_123",
    language="en",
    first_name="John",
    last_name="Doe",
    company="Acme Inc",
    loyalty_tier="Gold"
)

print(f"Contact {'created' if response.created else 'updated'}: {response.email}")
```

### Get Contact
```python
client.people.contacts.get(
    identifier: str    # Contact identifier
)
```

Returns: [ContactBaseModel](../models/people.md#contactbasemodel)

Example:
```python
# Get contact details
contact = client.people.contacts.get(identifier="john.doe@example.com")
print(f"Contact: {contact.email} (ID: {contact.nx_id})")
print(f"Created: {contact.created_at}")
```

### Delete Contact
```python
client.people.contacts.delete(
    identifier: str    # Contact identifier
)
```

Returns: None

Example:
```python
# Delete a contact
client.people.contacts.delete(identifier="old.contact@example.com")
```

### Contact Events

Track customer interactions and behaviors.

```python
client.people.contacts.events.send(
    identifier: str,           # Contact identifier
    name: Optional[str],       # Event name
    type_: Optional[str],      # Event type
    timestamp: Optional[int],  # Event timestamp
    idempotency_key: Optional[str],  # Unique key to prevent duplicates
    data: Optional[dict]       # Additional event data
)
```

Request: [SendContactEventRequest](../models/people.md#sendcontacteventrequest)  
Returns: None

Example:
```python
# Record a purchase event
client.people.contacts.events.send(
    identifier="customer@example.com",
    name="purchase_completed",
    idempotency_key="order_123",
    data={
        "product_id": "PROD_456",
        "amount": "99.99",
        "currency": "USD"
    }
)
```

### Contact Identifier

Manage the primary identifier type for contacts.

```python
# Get current identifier type
identifier = client.people.contacts.identifier.get()
print(f"Current identifier type: {identifier.identifier}")

# Update identifier type
updated = client.people.contacts.identifier.update()
print(f"Updated to: {updated.identifier}")
```

Returns: [GetContactIdentifierResponse](../models/people.md#getcontactidentifierresponse)

## Segments Resource

The Segments resource allows you to manage contact segments and analyze segment membership.

### List Segments
```python
client.people.segments.list(
    type_: Optional[str] = None,           # Filter by type ("manual" or "dynamic")
    exclude_predefined: Optional[bool] = False,  # Exclude predefined segments
    attribute: Optional[str] = None         # Filter by attribute usage
)
```

Example:
```python
# List all custom segments
segments = client.people.segments.list(exclude_predefined=True)
print(f"Found {len(segments)} custom segments")

# List dynamic segments
dynamic_segments = client.people.segments.list(type_="dynamic")
print(f"Found {len(dynamic_segments)} dynamic segments")
```

### Get Segment
```python
client.people.segments.get(
    segment_id: str    # Segment identifier
)
```

Example:
```python
# Get segment details
segment = client.people.segments.get(segment_id="seg_123")
print(f"Segment: {segment.name}")
print(f"Type: {'Dynamic' if segment.type_ == 'dynamic' else 'Manual'}")
```

### Create Segment
```python
client.people.segments.create(
    data: CreateSegmentRequest    # Segment configuration
)
```

Request: [CreateSegmentRequest](../models/people.md#createsegmentrequest)  
Returns: [SegmentBaseModel](../models/people.md#segmentbasemodel)

Example:
```python
from naxai.models.people.requests.segments_requests import CreateSegmentRequest
from naxai.models.people.search_condition import Condition, AttributeCondSimple, AttributeObject

# Create a dynamic segment for high-value customers
condition = Condition(
    all=[
        AttributeCondSimple(
            attribute=AttributeObject(
                field="customer_value",
                operator="gt",
                value=1000
            )
        )
    ]
)

segment = client.people.segments.create(
    data=CreateSegmentRequest(
        name="High Value Customers",
        description="Customers with value over $1000",
        type_="dynamic",
        condition=condition
    )
)

print(f"Created segment: {segment.name} (ID: {segment.id})")
```

### Update Segment
```python
client.people.segments.update(
    segment_id: str,              # Segment identifier
    data: CreateSegmentRequest    # Updated configuration
)
```

Request: [CreateSegmentRequest](../models/people.md#createsegmentrequest)  
Returns: [SegmentBaseModel](../models/people.md#segmentbasemodel)

### Delete Segment
```python
client.people.segments.delete(
    segment_id: str    # Segment identifier
)
```

### Segment History
```python
client.people.segments.history(
    segment_id: str,    # Segment identifier
    start: Optional[int],  # Start timestamp
    stop: Optional[int]    # End timestamp
)
```

Example:
```python
import datetime

# Get segment history for last 30 days
now = datetime.datetime.now(tz=datetime.timezone.utc)
start_date = now - datetime.timedelta(days=30)

history = client.people.segments.history(
    segment_id="seg_123",
    start=start_date,
    stop=now
)

print(f"Segment size changes over {len(history.history)} days:")
for day in history.history:
    date = datetime.datetime.fromtimestamp(day.date / 1000).strftime('%Y-%m-%d')
    print(f"{date}: {day.added} added, {day.removed} removed (total: {day.current})")
```

### Segment Usage
```python
client.people.segments.usage(
    segment_id: str    # Segment identifier
)
```

Example:
```python
# Check segment usage
usage = client.people.segments.usage(segment_id="seg_123")
if usage.campaign_ids:
    print(f"Used in {len(usage.campaign_ids)} campaigns")
if usage.broadcast_ids:
    print(f"Used in {len(usage.broadcast_ids)} broadcasts")
```

### Segment Contacts

Manage contacts within segments.

#### Add Contacts to Segment
```python
client.people.segments.contacts.add(
    segment_id: str,        # Segment identifier
    contact_ids: list[str]  # List of contact IDs to add
)
```

#### Remove Contacts from Segment
```python
client.people.segments.contacts.delete(
    segment_id: str,        # Segment identifier
    contact_ids: list[str]  # List of contact IDs to remove
)
```

#### Count Contacts in Segment
```python
client.people.segments.contacts.count(
    segment_id: str    # Segment identifier
)
```

#### List Contacts in Segment
```python
client.people.segments.contacts.list(
    segment_id: str,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    sort: Optional[str] = "createdAt:desc"
)
```

Example:
```python
# Add contacts to a manual segment
segment_id = "seg_123"
contact_ids = ["cnt_456", "cnt_789"]
client.people.segments.contacts.add(segment_id=segment_id, contact_ids=contact_ids)

# Get count of contacts in segment
count = client.people.segments.contacts.count(segment_id=segment_id)
print(f"Segment has {count} contacts")

# List contacts in segment
contacts = client.people.segments.contacts.list(
    segment_id=segment_id,
    page=1,
    page_size=25
)
print(f"Showing {len(contacts.contacts)} of {contacts.pagination.total_items} contacts")
```

## Best Practices

1. **Contact Management**
   - Use consistent identifiers across your system
   - Keep contact data up to date
   - Handle unsubscribe requests promptly
   - Validate email addresses and phone numbers

2. **Custom Attributes**
   - Use descriptive attribute names
   - Plan attribute structure before implementation
   - Consider data types and validation
   - Document attribute meanings and usage

3. **Segmentation**
   - Use dynamic segments for automated targeting
   - Keep segment conditions focused and clear
   - Monitor segment sizes and changes
   - Test segment conditions before use

4. **Performance**
   - Use pagination for large data sets
   - Implement proper error handling
   - Cache frequently accessed data
   - Monitor API rate limits

## Related Documentation

- [People Models](../models/people.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 