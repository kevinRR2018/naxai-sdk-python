# People Models

This page documents the models used in the People API of the Naxai SDK.

## Contact Models

### ContactBaseModel
Base model for contact information.

```python
class ContactBaseModel(BaseModel):
    nx_id: str                # Unique Naxai identifier
    email: Optional[str]      # Email address
    phone: Optional[str]      # Phone number
    sms_capable: Optional[bool]  # Can receive SMS
    external_id: Optional[str]   # External identifier
    unsubscribed: Optional[bool] # Unsubscribed status
    language: Optional[str]      # Preferred language
    created_at: Optional[int]    # Creation timestamp
    created_at_naxai: Optional[int]  # Naxai creation timestamp
```

### SearchContactsResponse
Model for contact search results.

```python
class SearchContactsResponse(BaseModel):
    pagination: Pagination           # Pagination information
    items: list[ContactBaseModel]    # List of matching contacts
```

### CountContactsResponse
Model for contact count operations.

```python
class CountContactsResponse(BaseModel):
    count: int  # Number of contacts matching criteria
```

### GetContactIdentifierResponse
Model for contact identifier type.

```python
class GetContactIdentifierResponse(BaseModel):
    identifier: Literal["phone", "email", "externalId"]  # Primary identifier type
```

### CreateOrUpdateContactResponse
Response model for contact creation/update.

```python
class CreateOrUpdateContactResponse(ContactBaseModel):
    # Inherits all fields from ContactBaseModel
    pass
```

Example:
```python
# Creating a new contact
contact = CreateOrUpdateContactResponse(
    nx_id="cnt_123abc",
    email="jane.smith@example.com",
    phone="+1234567890",
    sms_capable=True,
    external_id="cust_456",
    language="en",
    created_at=1703066400000
)
```

## Segment Models

### SegmentBaseModel
Base model for segments.

```python
class SegmentBaseModel(BaseModel):
    id: str                   # Unique segment identifier
    name: str                 # Segment name
    description: Optional[str]  # Segment description
    state: Optional[Literal["ready", "building"]]  # Current state
    predefined: Optional[bool]  # Is predefined segment
    condition: Optional[Condition]  # Segment criteria
    modified_by: Optional[str]  # Last modifier ID
    modified_at: Optional[int]  # Last modification timestamp
    type_: Optional[Literal["manual", "dynamic"]]  # Segment type
```

### ListSegmentsResponse
Model for listing segments.

```python
class ListSegmentsResponse(BaseModel):
    root: List[SegmentBaseModel]  # List of segments

    def __len__(self) -> int      # Get number of segments
    def __getitem__(self, index)  # Access segment by index
    def __iter__(self)            # Iterate through segments
```

### SegmentHistoryDay
Model for segment history entries.

```python
class SegmentHistoryDay(BaseModel):
    date: Optional[int]      # Day timestamp
    added: Optional[int]     # Contacts added
    removed: Optional[int]   # Contacts removed
    change: Optional[int]    # Net change
    current: Optional[int]   # Total contacts
```

### GetSegmentsHistoryResponse
Model for segment history.

```python
class GetSegmentsHistoryResponse(BaseModel):
    history: list[SegmentHistoryDay]  # List of daily history records
```

## Attribute Models

### BaseListObject
Base model for attributes.

```python
class BaseListObject(BaseModel):
    name: str  # Attribute name
```

### CreateAttributeResponse
Response model for attribute creation.

```python
class CreateAttributeResponse(BaseModel):
    name: str           # Attribute name
    segment_ids: list[str]  # Associated segment IDs
```

### ListAttributesResponse
Model for listing attributes.

```python
class ListAttributesResponse(BaseModel):
    root: List[BaseListObject]  # List of attributes

    def __len__(self) -> int      # Get number of attributes
    def __getitem__(self, index)  # Access attribute by index
    def __iter__(self)            # Iterate through attributes
```

## Search and Segment Conditions

### SearchCondition
Model for complex contact search queries.

```python
class SearchCondition(BaseModel):
    all: Optional[list[Union[
        AttributeCondSimple,
        AttributeCondArray,
        EventCond,
        AllCondGroup,
        AnyCondGroup
    ]]]  # AND conditions
    any: Optional[list[Union[
        AttributeCondSimple,
        AttributeCondArray,
        EventCond,
        AllCondGroup,
        AnyCondGroup
    ]]]  # OR conditions
```

### EventObject
Model for event-based conditions.

```python
class EventObject(BaseModel):
    name: str                # Event name
    count: int = 1          # Occurrence count
    count_boundary: Literal["at-least", "at-most"] = "at-least"
    time_boundary: Literal["all-time", "within-last", "before", "after"] = "all-time"
    period_boundary: Literal["day", "month"] = "day"
    interval_boundary: int = 1  # Time period value (1-366)
    date: Optional[int]     # Reference timestamp
    properties: EventProperties  # Event property conditions
```

### AttributeObject
Model for attribute conditions.

```python
class AttributeObject(BaseModel):
    operator: CONDITIONS    # Comparison operator
    field: str            # Field name
    value: Optional[Union[str, int, bool]]  # Comparison value
```

## Constants

### Condition Operators
```python
CONDITIONS = Literal[
    "eq", "not-eq", "gt", "lt", "exists", "not-exists", 
    "contains", "not-contains", "is-true", "is-false",
    "is-timestamp", "is-timestamp-before", "is-timestamp-after",
    "is-mobile", "is-not-mobile"
]
```

## Best Practices

1. **Contact Management**
   - Use appropriate identifier types
   - Handle unsubscribe status
   - Consider SMS capabilities
   - Respect language preferences

2. **Segment Operations**
   - Monitor segment building state
   - Track membership changes
   - Use appropriate condition types
   - Consider performance impact

3. **Search and Filtering**
   - Build efficient conditions
   - Use appropriate operators
   - Combine conditions logically
   - Consider pagination

Example with best practices:
```python
from naxai.models.people import (
    SearchCondition,
    AttributeCondSimple,
    AttributeObject,
    EventCond,
    EventObject,
    EventProperties
)

# Create a search condition for active US customers
condition = SearchCondition(
    all=[
        AttributeCondSimple(
            attribute=AttributeObject(
                operator="eq",
                field="country",
                value="US"
            )
        ),
        EventCond(
            event=EventObject(
                name="login",
                count=1,
                time_boundary="within-last",
                period_boundary="day",
                interval_boundary=30,
                properties=EventProperties(all=[])
            )
        )
    ]
)

try:
    # Search for contacts
    response = client.people.contacts.search(condition)
    
    # Process results with pagination
    while response.items:
        for contact in response.items:
            process_contact(contact)
            
        if response.pagination.has_more:
            response = client.people.contacts.search(
                condition,
                page=response.pagination.next_page
            )
        else:
            break
            
except Exception as e:
    logger.error(f"Search failed: {e}")
    # Handle error appropriately
```

## Related Documentation

- [People API Reference](../api/people.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 