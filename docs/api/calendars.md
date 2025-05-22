# Calendars API Reference

The Calendars API allows you to manage scheduling and time-based operations for voice calls, SMS, and emails.

## Calendar Resource

### Create Calendar
```python
client.calendars.create(
    data: Union[dict, CreateCalendarRequest],
    # Required fields in data:
    # - name: str
    # - timezone: str  # IANA timezone (e.g., "America/New_York")
    #
    # Optional fields:
    # - description: str
    # - working_hours: List[WorkingHours]
    # - holidays: List[Holiday]
    # - metadata: Dict[str, Any]
)
```

Example:
```python
response = client.calendars.create(data={
    "name": "Customer Support Hours",
    "timezone": "America/New_York",
    "description": "Support team availability",
    "working_hours": [
        {
            "day": "monday",
            "intervals": [
                {"start": "09:00", "end": "17:00"}
            ]
        },
        {
            "day": "tuesday",
            "intervals": [
                {"start": "09:00", "end": "17:00"}
            ]
        }
        # ... other days
    ],
    "holidays": [
        {
            "name": "New Year's Day",
            "date": "2024-01-01"
        }
    ],
    "metadata": {
        "department": "support",
        "region": "east_coast"
    }
})
print(f"Calendar ID: {response.calendar_id}")
```

### Update Calendar
```python
client.calendars.update(
    calendar_id: str,
    data: Union[dict, UpdateCalendarRequest]
)
```

### Get Calendar
```python
client.calendars.get(calendar_id: str)
```

### List Calendars
```python
client.calendars.list(
    page: Optional[int] = None,
    page_size: Optional[int] = None
)
```

### Delete Calendar
```python
client.calendars.delete(calendar_id: str)
```

## Working Hours Resource

### Update Working Hours
```python
client.calendars.working_hours.update(
    calendar_id: str,
    data: Union[dict, UpdateWorkingHoursRequest],
    # Required fields in data:
    # - working_hours: List[WorkingHours]
)
```

Example:
```python
# Update working hours
client.calendars.working_hours.update(
    calendar_id="cal_123",
    data={
        "working_hours": [
            {
                "day": "monday",
                "intervals": [
                    {"start": "09:00", "end": "12:00"},
                    {"start": "13:00", "end": "17:00"}
                ]
            },
            {
                "day": "tuesday",
                "intervals": [
                    {"start": "09:00", "end": "17:00"}
                ]
            }
            # ... other days
        ]
    }
)
```

## Holidays Resource

### Add Holiday
```python
client.calendars.holidays.add(
    calendar_id: str,
    data: Union[dict, AddHolidayRequest],
    # Required fields in data:
    # - name: str
    # - date: str  # YYYY-MM-DD format
    #
    # Optional fields:
    # - description: str
    # - recurring: bool
)
```

### Remove Holiday
```python
client.calendars.holidays.remove(
    calendar_id: str,
    holiday_id: str
)
```

### List Holidays
```python
client.calendars.holidays.list(
    calendar_id: str,
    start_date: Optional[str] = None,  # YYYY-MM-DD
    end_date: Optional[str] = None     # YYYY-MM-DD
)
```

Example:
```python
# Add holidays
response = client.calendars.holidays.add(
    calendar_id="cal_123",
    data={
        "name": "Company Anniversary",
        "date": "2024-03-15",
        "description": "Annual company celebration",
        "recurring": True
    }
)

# List upcoming holidays
holidays = client.calendars.holidays.list(
    calendar_id="cal_123",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

## Schedule Checking

### Check Available Time
```python
client.calendars.check_availability(
    calendar_id: str,
    timestamp: int,  # Unix timestamp in milliseconds
    duration: Optional[int] = None  # Duration in minutes
)
```

### Get Next Available Time
```python
client.calendars.get_next_available(
    calendar_id: str,
    after: int,  # Unix timestamp in milliseconds
    duration: Optional[int] = None  # Duration in minutes
)
```

Example:
```python
from datetime import datetime, timedelta

# Check if a specific time is available
timestamp = int(datetime.now().timestamp() * 1000)
is_available = client.calendars.check_availability(
    calendar_id="cal_123",
    timestamp=timestamp,
    duration=30  # 30 minutes
)

# Get next available slot
next_slot = client.calendars.get_next_available(
    calendar_id="cal_123",
    after=timestamp,
    duration=60  # 60 minutes
)
```

## Using with Other APIs

### Schedule Voice Call
```python
# Schedule a call during working hours
next_available = client.calendars.get_next_available(
    calendar_id="cal_123",
    after=int(datetime.now().timestamp() * 1000),
    duration=15
)

if next_available:
    response = client.voice.call.create(
        to=["1234567890"],
        from_="0987654321",
        welcome={"say": "Hello!"},
        calendar_id="cal_123",
        scheduled_at=next_available.timestamp
    )
```

### Schedule Email Campaign
```python
# Schedule email sending for working hours
client.email.send(data={
    "sender_email": "sender@yourdomain.com",
    "sender_name": "Your Name",
    "subject": "Important Update",
    "to": [{"email": "recipient@example.com"}],
    "html": "<p>Your important message here.</p>",
    "calendar_id": "cal_123"  # Will send during next working hours
})
```

## Best Practices

1. **Time Zone Management**
   - Always specify explicit timezones
   - Handle DST transitions
   - Use IANA timezone names

2. **Working Hours**
   - Define clear business hours
   - Account for lunch breaks
   - Consider multiple shifts

3. **Holiday Planning**
   - Include recurring holidays
   - Plan for regional differences
   - Update annually

4. **Schedule Optimization**
   - Check availability before scheduling
   - Include buffer times
   - Consider time zone differences

## Related Documentation

- [Calendar Models](../models/calendars.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 