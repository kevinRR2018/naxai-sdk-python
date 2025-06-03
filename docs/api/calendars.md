# Calendars API Reference

The Calendars API allows you to manage scheduling and time-based operations in your Naxai account. It provides comprehensive calendar management capabilities including working hours, schedules, exclusion dates, and holiday templates.

## Calendar Resource

### Create Calendar
```python
client.calendars.create(
    data: CreateCalendarRequest,
    # Required fields in data:
    # - name: str                           # Calendar name
    # - schedule: list[ScheduleObject]      # List of exactly 7 schedule objects
    #
    # Optional fields:
    # - timezone: str = "Europe/Brussels"   # IANA timezone
    # - exclusions: list[str] = None        # List of excluded dates (YYYY-MM-DD)
)
```

Request: [CreateCalendarRequest](../models/calendars.md#createcalendarrequest)  
Returns: [CreateCalendarResponse](../models/calendars.md#createcalendarresponse)

The `ScheduleObject` for each day contains:
```python
{
    "day": int,              # Day of week (1-7, Monday to Sunday)
    "open": bool,            # Whether the schedule is open
    "start": str,            # Opening time ("HH:MM")
    "stop": str,             # Closing time ("HH:MM")
    "extended": bool,        # Whether extended hours are enabled
    "extension_start": str,  # Extended hours start time ("HH:MM")
    "extension_stop": str    # Extended hours end time ("HH:MM")
}
```

Example:
```python
from naxai.models.calendars.requests.calendar_requests import (
    CreateCalendarRequest, ScheduleObject)

# Create a calendar with business hours
schedule = [
    ScheduleObject(  # Monday
        day=1,
        open=True,
        start="09:00",
        stop="17:00",
        extended=True,
        extension_start="17:00",
        extension_stop="20:00"
    ),
    ScheduleObject(  # Tuesday
        day=2,
        open=True,
        start="09:00",
        stop="17:00"
    ),
    # ... repeat for all 7 days
]

response = client.calendars.create(
    data=CreateCalendarRequest(
        name="Customer Support Hours",
        timezone="America/New_York",  # Optional, defaults to "Europe/Brussels"
        schedule=schedule,
        exclusions=["2024-12-25", "2024-12-26"]  # Optional holiday closures
    )
)
print(f"Calendar created with ID: {response.id}")
```

### Update Calendar
```python
client.calendars.update(
    calendar_id: str,              # Calendar identifier
    data: CreateCalendarRequest    # Updated configuration using same model as create
)
```

Request: [CreateCalendarRequest](../models/calendars.md#createcalendarrequest)  
Returns: [UpdateCalendarResponse](../models/calendars.md#updatecalendarresponse)

Example:
```python
# Update calendar configuration
updated = client.calendars.update(
    calendar_id="cal_123",
    data=CreateCalendarRequest(
        name="Updated Support Hours",
        timezone="Europe/London",
        schedule=[
            ScheduleObject(
                day=1,  # Monday
                open=True,
                start="08:00",
                stop="16:00"
            ),
            # ... repeat for all 7 days (must provide all 7 days)
        ]
    )
)
print(f"Updated calendar: {updated.name}")
```

### Get Calendar
```python
client.calendars.get(calendar_id: str)
```

Returns: [GetCalendarResponse](../models/calendars.md#getcalendarresponse)

Example:
```python
calendar = client.calendars.get("cal_123")
print(f"Calendar: {calendar.name}")
print(f"Timezone: {calendar.timezone}")
for day in calendar.schedule:
    print(f"Day {day.day}: {'Open' if day.open else 'Closed'} {day.start}-{day.stop}")
```

### List Calendars
```python
client.calendars.list()
```

Returns: [ListCalendarsResponse](../models/calendars.md#listcalendarsresponse)

Example:
```python
calendars = client.calendars.list()
for calendar in calendars:
    print(f"Calendar: {calendar.name} (ID: {calendar.id})")
```

### Delete Calendar
```python
client.calendars.delete(calendar_id: str)
```

Returns: None

## Best Practices

1. **Time Zone Management**
   - Default timezone is "Europe/Brussels" if not specified
   - Always use IANA timezone identifiers
   - Handle DST transitions appropriately
   - Consider recipient time zones when scheduling

2. **Working Hours**
   - Must provide schedule for all 7 days
   - Use extended hours for flexible coverage
   - Account for lunch breaks and regular closures
   - Days can be marked as closed using `open=False`

3. **Exclusion Dates**
   - Use ISO 8601 date format (YYYY-MM-DD)
   - Maintain up-to-date holiday lists
   - Consider regional variations
   - Limit to 1000 exclusions per request

4. **Schedule Optimization**
   - Check availability before scheduling
   - Include buffer times between activities
   - Consider load distribution
   - Use extended hours for peak periods

5. **Holiday Templates**
   - Use predefined templates for common holidays
   - Verify dates for your region
   - Update templates annually
   - Combine with custom exclusions as needed

## Availability Management

### Check Availability
```python
client.calendars.check(
    calendar_id: str,
    timestamp: Optional[int] = None  # Defaults to current UTC time
)
```

Returns:
- `match_`: Whether the timestamp falls within working hours
- `next_`: If not a match, provides the next available timestamp

Example:
```python
import time

# Check if current time is within working hours
result = client.calendars.check("cal_123")
if result.match_:
    print("Current time is within working hours")
else:
    next_time = datetime.fromtimestamp(result.next_ / 1000)
    print(f"Next available time: {next_time}")

# Check specific time
future_time = int(time.time() * 1000) + (24 * 60 * 60 * 1000)  # Tomorrow
result = client.calendars.check("cal_123", timestamp=future_time)
```

## Exclusion Management

### Add Exclusions
```python
client.calendars.add_exclusions(
    calendar_id: str,
    exclusions: list[str]  # List of dates in YYYY-MM-DD format (max 1000)
)
```

Example:
```python
# Add holiday closures
response = client.calendars.add_exclusions(
    "cal_123",
    exclusions=["2024-12-25", "2024-12-26", "2025-01-01"]
)
print("Updated exclusions:", response.exclusions)
```

### Remove Exclusions
```python
client.calendars.delete_exclusions(
    calendar_id: str,
    exclusions: list[str]  # List of dates to remove (max 1000)
)
```

Example:
```python
# Remove outdated exclusions
response = client.calendars.delete_exclusions(
    "cal_123",
    exclusions=["2023-12-25", "2023-12-26"]
)
print("Remaining exclusions:", response.exclusions)
```

## Holiday Templates

Holiday templates provide predefined sets of dates for common holidays in different regions.

### List Holiday Templates
```python
client.calendars.holidays_templates.list()
```

Example:
```python
templates = client.calendars.holidays_templates.list()
for template in templates:
    print(f"Template: {template.name}")
    print(f"Number of holidays: {len(template.dates)}")
```

### Get Holiday Template
```python
client.calendars.holidays_templates.get(template_id: str)
```

Example:
```python
template = client.calendars.holidays_templates.get("ht_123")
print(f"Template: {template.name}")
print("Holidays:")
for date in template.dates:
    print(f"- {date}")
```

## Related Documentation

- [Calendar Models](../models/calendars.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 