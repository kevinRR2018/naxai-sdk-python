# Calendar Models

This page documents the models used in the Calendars API of the Naxai SDK.

## Calendar Models

### Calendar
Base model for calendar configuration.

```python
class Calendar(BaseModel):
    id: Optional[str] = None           # Unique calendar identifier
    name: str                          # Calendar name
    timezone: Optional[str] = "Europe/Brussels"  # IANA timezone name
    schedule: list[ScheduleObject]     # List of exactly 7 schedule objects
    exclusions: Optional[list[str]] = None  # List of excluded dates
```

### ScheduleObject
Model for daily schedule configuration.

```python
class ScheduleObject(BaseModel):
    day: int                  # Day of week (1-7, Monday to Sunday)
    open: bool                # Whether the schedule is open
    start: str                # Opening time ("HH:MM")
    stop: str                 # Closing time ("HH:MM")
    extended: bool            # Whether extended hours are enabled
    extension_start: str      # Extended hours start time ("HH:MM")
    extension_stop: str       # Extended hours end time ("HH:MM")
```

Example:
```python
from naxai.models.calendars.calendar import Calendar
from naxai.models.calendars.schedule_object import ScheduleObject

# Create a calendar with business hours
calendar = Calendar(
    name="Customer Support Hours",
    timezone="America/New_York",
    schedule=[
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
            stop="17:00",
            extended=False,
            extension_start="",
            extension_stop=""
        ),
        # ... repeat for all 7 days
    ]
)
```

## Request Models

### CreateCalendarRequest
Model for creating new calendars.

```python
class CreateCalendarRequest(BaseModel):
    name: str                          # Calendar name
    timezone: Optional[str] = "Europe/Brussels"  # IANA timezone
    schedule: list[ScheduleObject]     # List of exactly 7 schedule objects
    exclusions: Optional[list[str]] = None  # List of excluded dates
```

Example:
```python
from naxai.models.calendars.requests.calendar_requests import CreateCalendarRequest

request = CreateCalendarRequest(
    name="Business Hours",
    timezone="America/New_York",
    schedule=[
        ScheduleObject(
            day=1,  # Monday
            open=True,
            start="09:00",
            stop="17:00",
            extended=False,
            extension_start="",
            extension_stop=""
        ),
        # ... repeat for all 7 days
    ],
    exclusions=["2024-12-25", "2024-12-26"]
)
```

## Response Models

### CreateCalendarResponse
Response model for calendar creation.

```python
class CreateCalendarResponse(BaseModel):
    id: str                           # Unique calendar identifier
    name: str                         # Calendar name
    timezone: Optional[str] = None    # IANA timezone
    schedule: list[ScheduleObject]    # List of schedule objects
    exclusions: Optional[list] = None # List of excluded dates
```

### GetCalendarResponse
Response model for retrieving a calendar.

```python
class GetCalendarResponse(Calendar):
    # Inherits all fields from Calendar base model
    pass
```

### UpdateCalendarResponse
Response model for updating a calendar.

```python
class UpdateCalendarResponse(Calendar):
    # Inherits all fields from Calendar base model
    pass
```

### ListCalendarsResponse
Response model for listing calendars.

```python
class ListCalendarsResponse(BaseModel):
    root: list[Calendar]  # List of calendar objects
    
    def __len__(self) -> int         # Get number of calendars
    def __getitem__(self, index)     # Access calendar by index
    def __iter__(self)               # Iterate through calendars
```

### ExclusionResponse
Base response model for exclusion operations.

```python
class ExclusionResponse(BaseModel):
    exclusions: list[str]  # List of exclusion dates
```

### AddExclusionsResponse
Response model for adding exclusions.

```python
class AddExclusionsResponse(ExclusionResponse):
    # Inherits exclusions field from ExclusionResponse
    pass
```

### DeleteExclusionsResponse
Response model for removing exclusions.

```python
class DeleteExclusionsResponse(ExclusionResponse):
    # Inherits exclusions field from ExclusionResponse
    pass
```

### CheckCalendarResponse
Response model for availability checks.

```python
class CheckCalendarResponse(BaseModel):
    match_: bool                # Whether time matches schedule
    next_: Optional[int] = None # Next available timestamp if no match
```

## Best Practices

1. **Schedule Configuration**
   - Always provide exactly 7 schedule objects (one per day)
   - Use 24-hour format for times ("HH:MM")
   - Set `open=False` for closed days
   - Use extended hours for flexible schedules

2. **Time Handling**
   - Default timezone is "Europe/Brussels"
   - Always use IANA timezone identifiers
   - Times are in "HH:MM" format
   - Timestamps are in milliseconds since epoch

3. **Exclusion Management**
   - Use ISO 8601 date format (YYYY-MM-DD)
   - Maintain consistent date formatting
   - Consider timezone implications
   - Handle recurring exclusions appropriately

Example with best practices:
```python
from datetime import datetime
from naxai.models.calendars.requests.calendar_requests import CreateCalendarRequest
from naxai.models.calendars.schedule_object import ScheduleObject

# Create a calendar with proper configuration
schedule = []
for day in range(1, 8):  # 1-7 (Monday to Sunday)
    if day <= 5:  # Weekdays
        schedule.append(ScheduleObject(
            day=day,
            open=True,
            start="09:00",
            stop="17:00",
            extended=True,
            extension_start="08:00",
            extension_stop="18:00"
        ))
    else:  # Weekend
        schedule.append(ScheduleObject(
            day=day,
            open=False,
            start="",
            stop="",
            extended=False,
            extension_start="",
            extension_stop=""
        ))

calendar = CreateCalendarRequest(
    name="Business Hours",
    timezone="America/New_York",
    schedule=schedule,
    exclusions=[
        "2024-12-25",  # Christmas
        "2024-01-01"   # New Year's Day
    ]
)
```

## Related Documentation

- [Calendars API Reference](../api/calendars.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 