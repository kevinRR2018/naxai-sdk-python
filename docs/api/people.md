# People API Reference

The People API allows you to manage contacts, groups, and contact preferences in your Naxai account.

## Contacts Resource

### Create Contact
```python
client.people.contacts.create(
    data: Union[dict, CreateContactRequest],
    # Required fields in data:
    # - email: str
    # - phone: str
    #
    # Optional fields:
    # - first_name: str
    # - last_name: str
    # - company: str
    # - title: str
    # - custom_fields: Dict[str, Any]
    # - groups: List[str]  # Group IDs
    # - preferences: Dict[str, bool]  # Communication preferences
)
```

Example:
```python
response = client.people.contacts.create(data={
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Acme Inc",
    "title": "Software Engineer",
    "custom_fields": {
        "department": "Engineering",
        "location": "New York"
    },
    "groups": ["grp_123", "grp_456"],
    "preferences": {
        "email_marketing": True,
        "sms_notifications": True
    }
})
print(f"Contact ID: {response.contact_id}")
```

### Update Contact
```python
client.people.contacts.update(
    contact_id: str,
    data: Union[dict, UpdateContactRequest]
)
```

### Get Contact
```python
client.people.contacts.get(contact_id: str)
```

### List Contacts
```python
client.people.contacts.list(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    group_id: Optional[str] = None,
    created_after: Optional[int] = None,
    created_before: Optional[int] = None,
    updated_after: Optional[int] = None,
    updated_before: Optional[int] = None
)
```

### Delete Contact
```python
client.people.contacts.delete(contact_id: str)
```

## Groups Resource

### Create Group
```python
client.people.groups.create(
    data: Union[dict, CreateGroupRequest],
    # Required fields in data:
    # - name: str
    #
    # Optional fields:
    # - description: str
    # - metadata: Dict[str, Any]
)
```

### Update Group
```python
client.people.groups.update(
    group_id: str,
    data: Union[dict, UpdateGroupRequest]
)
```

### List Groups
```python
client.people.groups.list(
    page: Optional[int] = None,
    page_size: Optional[int] = None
)
```

### Delete Group
```python
client.people.groups.delete(group_id: str)
```

### Add Contacts to Group
```python
client.people.groups.add_contacts(
    group_id: str,
    contact_ids: List[str]
)
```

### Remove Contacts from Group
```python
client.people.groups.remove_contacts(
    group_id: str,
    contact_ids: List[str]
)
```

Example:
```python
# Create a new group
group = client.people.groups.create(data={
    "name": "Newsletter Subscribers",
    "description": "Active newsletter subscribers",
    "metadata": {
        "category": "marketing",
        "region": "global"
    }
})

# Add contacts to the group
client.people.groups.add_contacts(
    group_id=group.group_id,
    contact_ids=["cnt_123", "cnt_456"]
)
```

## Preferences Resource

### Get Contact Preferences
```python
client.people.preferences.get(contact_id: str)
```

### Update Contact Preferences
```python
client.people.preferences.update(
    contact_id: str,
    data: Union[dict, UpdatePreferencesRequest],
    # Fields in data:
    # - email_marketing: bool
    # - sms_notifications: bool
    # - voice_calls: bool
    # - custom_preferences: Dict[str, bool]
)
```

Example:
```python
# Update contact preferences
response = client.people.preferences.update(
    contact_id="cnt_123",
    data={
        "email_marketing": True,
        "sms_notifications": False,
        "voice_calls": True,
        "custom_preferences": {
            "product_updates": True,
            "event_invitations": False
        }
    }
)
```

## Custom Fields Resource

### Create Custom Field
```python
client.people.custom_fields.create(
    data: Union[dict, CreateCustomFieldRequest],
    # Required fields in data:
    # - name: str
    # - type: str  # "text", "number", "boolean", "date"
    #
    # Optional fields:
    # - description: str
    # - required: bool
    # - default_value: Any
)
```

### List Custom Fields
```python
client.people.custom_fields.list()
```

### Delete Custom Field
```python
client.people.custom_fields.delete(field_name: str)
```

Example:
```python
# Create a custom field
field = client.people.custom_fields.create(data={
    "name": "loyalty_points",
    "type": "number",
    "description": "Customer loyalty program points",
    "required": False,
    "default_value": 0
})
```

## Activity Logs

### List Contact Activity
```python
client.people.activity_logs.list(
    contact_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    activity_type: Optional[str] = None,  # "email", "sms", "voice"
    start: Optional[int] = None,
    stop: Optional[int] = None
)
```

Example:
```python
# Get contact's recent activity
logs = client.people.activity_logs.list(
    contact_id="cnt_123",
    activity_type="email",
    page=1,
    page_size=50
)

for activity in logs:
    print(f"Type: {activity.type}")
    print(f"Timestamp: {activity.timestamp}")
    print(f"Details: {activity.details}")
```

## Best Practices

1. **Contact Management**
   - Validate email and phone formats
   - Use meaningful group names
   - Keep custom fields organized

2. **Data Privacy**
   - Honor unsubscribe requests
   - Implement preference centers
   - Follow data protection regulations

3. **Performance**
   - Use pagination for large lists
   - Batch group operations
   - Cache frequently accessed data

4. **Integration**
   - Link contacts across channels
   - Maintain consistent metadata
   - Track engagement history

## Related Documentation

- [People Models](../models/people.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 