# People Models

This page documents the models used in the People API of the Naxai SDK.

## Contact Models

### BaseContactModel
Base model for contact information.

```python
class BaseContactModel(BaseModel):
    email: str                # Contact email address
    phone: str               # Contact phone number
    first_name: Optional[str] = None  # First name
    last_name: Optional[str] = None   # Last name
    company: Optional[str] = None     # Company name
    title: Optional[str] = None       # Job title
    custom_fields: Optional[Dict[str, Any]] = None  # Custom field values
    groups: Optional[List[str]] = None  # Group IDs
    preferences: Optional[Dict[str, bool]] = None  # Communication preferences
```

### CreateContactRequest
Model for creating new contacts.

```python
class CreateContactRequest(BaseContactModel):
    pass  # Inherits all fields from BaseContactModel
```

### UpdateContactRequest
Model for updating existing contacts.

```python
class UpdateContactRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    groups: Optional[List[str]] = None
    preferences: Optional[Dict[str, bool]] = None
```

### ContactResponse
Response model for contact operations.

```python
class ContactResponse(BaseContactModel):
    contact_id: str          # Unique contact identifier
    created_at: int         # Creation timestamp
    updated_at: int         # Last update timestamp
```

Example:
```python
# Creating a new contact
contact = CreateContactRequest(
    email="jane.smith@example.com",
    phone="+1234567890",
    first_name="Jane",
    last_name="Smith",
    company="Tech Corp",
    title="Product Manager",
    custom_fields={
        "industry": "Technology",
        "lead_source": "Website"
    },
    preferences={
        "email_marketing": True,
        "sms_notifications": False
    }
)
```

## Group Models

### BaseGroupModel
Base model for contact groups.

```python
class BaseGroupModel(BaseModel):
    name: str               # Group name
    description: Optional[str] = None  # Group description
    metadata: Optional[Dict[str, Any]] = None  # Custom metadata
```

### CreateGroupRequest
Model for creating new groups.

```python
class CreateGroupRequest(BaseGroupModel):
    pass  # Inherits all fields from BaseGroupModel
```

### UpdateGroupRequest
Model for updating existing groups.

```python
class UpdateGroupRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

### GroupResponse
Response model for group operations.

```python
class GroupResponse(BaseGroupModel):
    group_id: str           # Unique group identifier
    contact_count: int     # Number of contacts in group
    created_at: int        # Creation timestamp
    updated_at: int        # Last update timestamp
```

Example:
```python
# Creating a new group
group = CreateGroupRequest(
    name="VIP Customers",
    description="High-value customers with premium support",
    metadata={
        "priority_level": "high",
        "support_tier": "premium"
    }
)
```

## Preference Models

### UpdatePreferencesRequest
Model for updating contact preferences.

```python
class UpdatePreferencesRequest(BaseModel):
    email_marketing: Optional[bool] = None  # Email marketing consent
    sms_notifications: Optional[bool] = None  # SMS notifications consent
    voice_calls: Optional[bool] = None  # Voice calls consent
    custom_preferences: Optional[Dict[str, bool]] = None  # Custom preferences
```

### PreferencesResponse
Response model for preference operations.

```python
class PreferencesResponse(BaseModel):
    contact_id: str         # Contact identifier
    preferences: Dict[str, bool]  # All preferences
    updated_at: int        # Last update timestamp
```

## Custom Field Models

### CustomFieldDefinition
Model for custom field definitions.

```python
class CustomFieldDefinition(BaseModel):
    name: str              # Field name
    type: str             # Field type
    description: Optional[str] = None  # Field description
    required: bool = False  # Whether field is required
    default_value: Optional[Any] = None  # Default value
```

### CreateCustomFieldRequest
Model for creating custom fields.

```python
class CreateCustomFieldRequest(CustomFieldDefinition):
    pass  # Inherits all fields from CustomFieldDefinition
```

Example:
```python
# Creating a custom field
field = CreateCustomFieldRequest(
    name="account_balance",
    type="number",
    description="Current account balance in USD",
    required=False,
    default_value=0.0
)
```

## Activity Models

### ContactActivity
Model for contact activity logs.

```python
class ContactActivity(BaseModel):
    activity_id: str        # Unique activity identifier
    contact_id: str        # Contact identifier
    type: str             # Activity type
    timestamp: int        # Activity timestamp
    details: Dict[str, Any]  # Activity details
```

## Constants

### Activity Types
```python
ACTIVITY_TYPES = Literal[
    "email_sent",      # Email was sent
    "email_opened",    # Email was opened
    "email_clicked",   # Email link was clicked
    "sms_sent",        # SMS was sent
    "sms_delivered",   # SMS was delivered
    "voice_call",      # Voice call was made
    "preference_update",  # Preferences were updated
    "group_added",     # Added to group
    "group_removed"    # Removed from group
]
```

### Field Types
```python
FIELD_TYPES = Literal[
    "text",     # Text field
    "number",   # Numeric field
    "boolean",  # Boolean field
    "date"      # Date field
]
```

## Best Practices

1. **Model Validation**
   - Validate email and phone formats
   - Check required fields
   - Validate custom field types

2. **Error Handling**
   - Handle validation errors
   - Check for duplicate contacts
   - Validate group operations

3. **Data Management**
   - Keep custom fields consistent
   - Maintain clean group structure
   - Regular data cleanup

Example with best practices:
```python
try:
    # Create contact with validation
    contact = CreateContactRequest(
        email=validate_email(email),
        phone=validate_phone(phone),
        first_name=first_name,
        last_name=last_name,
        custom_fields=validate_custom_fields(custom_fields)
    )
    response = client.people.contacts.create(data=contact)
    
    # Add to appropriate groups
    if response.contact_id:
        client.people.groups.add_contacts(
            group_id="new_customers",
            contact_ids=[response.contact_id]
        )
except ValidationError as e:
    logger.error(f"Invalid contact data: {e}")
    # Handle validation error
except Exception as e:
    logger.error(f"Failed to create contact: {e}")
    # Handle other errors
```

## Related Documentation

- [People API Reference](../api/people.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 