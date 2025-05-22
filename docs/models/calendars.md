# Calendar Models

This page documents the models used in the Calendars API of the Naxai SDK.

## Calendar Models

### BaseCalendarModel
Base model for calendar information.

```python
class BaseCalendarModel(BaseModel):
    name: str                # Calendar name
    timezone: str           # IANA timezone name
    description: Optional[str] = None  # Calendar description
    working_hours: Optional[List[WorkingHours]] = None  # Working hours config
    holidays: Optional[List[Holiday]] = None  # Holiday list
    metadata: Optional[Dict[str, Any]] = None  # Custom metadata
```

### CreateCalendarRequest
Model for creating new calendars.

```python
class CreateCalendarRequest(BaseCalendarModel):
    pass  # Inherits all fields from BaseCalendarModel
```

### UpdateCalendarRequest
Model for updating existing calendars.

```python
class UpdateCalendarRequest(BaseModel):
    name: Optional[str] = None
    timezone: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

### CalendarResponse
Response model for calendar operations.

```python
class CalendarResponse(BaseCalendarModel):
    calendar_id: str        # Unique calendar identifier
    created_at: int        # Creation timestamp
    updated_at: int        # Last update timestamp
```

Example:
```python
# Creating a new calendar
calendar = CreateCalendarRequest(
    name="Sales Team Hours",
    timezone="Europe/London",
    description="Sales team availability schedule",
    working_hours=[
        WorkingHours(
            day="monday",
            intervals=[
                TimeInterval(start="09:00", end="17:30")
            ]
        )
    ],
    metadata={
        "team": "sales",
        "region": "europe"
    }
)
```

## Working Hours Models

### TimeInterval
Model for time intervals.

```python
class TimeInterval(BaseModel):
    start: str             # Start time (HH:MM format)
    end: str              # End time (HH:MM format)
```

### WorkingHours
Model for daily working hours.

```python
class WorkingHours(BaseModel):
    day: str              # Day of week (lowercase)
    intervals: List[TimeInterval]  # Time intervals
```

### UpdateWorkingHoursRequest
Model for updating working hours.

```python
class UpdateWorkingHoursRequest(BaseModel):
    working_hours: List[WorkingHours]  # New working hours configuration
```

Example:
```python
# Defining working hours with breaks
working_hours = UpdateWorkingHoursRequest(
    working_hours=[
        WorkingHours(
            day="monday",
            intervals=[
                TimeInterval(start="09:00", end="12:00"),
                TimeInterval(start="13:00", end="17:30")
            ]
        ),
        WorkingHours(
            day="tuesday",
            intervals=[
                TimeInterval(start="09:00", end="12:00"),
                TimeInterval(start="13:00", end="17:30")
            ]
        )
    ]
)
```

## Holiday Models

### Holiday
Model for holiday entries.

```python
class Holiday(BaseModel):
    name: str             # Holiday name
    date: str            # Date (YYYY-MM-DD format)
    description: Optional[str] = None  # Holiday description
    recurring: Optional[bool] = False  # Whether holiday repeats annually
```

### AddHolidayRequest
Model for adding holidays.

```python
class AddHolidayRequest(Holiday):
    pass  # Inherits all fields from Holiday
```

### HolidayResponse
Response model for holiday operations.

```python
class HolidayResponse(Holiday):
    holiday_id: str       # Unique holiday identifier
    calendar_id: str     # Associated calendar ID
```

Example:
```python
# Adding holidays
holidays = [
    AddHolidayRequest(
        name="Christmas Day",
        date="2024-12-25",
        description="Christmas Day celebration",
        recurring=True
    ),
    AddHolidayRequest(
        name="Summer Party",
        date="2024-07-15",
        description="Annual summer celebration",
        recurring=False
    )
]
```

## Availability Models

### AvailabilityCheck
Model for availability check responses.

```python
class AvailabilityCheck(BaseModel):
    available: bool       # Whether time is available
    next_available: Optional[int] = None  # Next available timestamp
    conflicts: Optional[List[str]] = None  # Conflict reasons if not available
```

### NextAvailableSlot
Model for next available time slot responses.

```python
class NextAvailableSlot(BaseModel):
    timestamp: int       # Available time timestamp
    duration: int       # Slot duration in minutes
    working_hours: bool  # Whether within working hours
```

Example:
```python
from datetime import datetime, timedelta

# Check availability for tomorrow
tomorrow = datetime.now() + timedelta(days=1)
timestamp = int(tomorrow.replace(hour=9, minute=0).timestamp() * 1000)

availability = client.calendars.check_availability(
    calendar_id="cal_123",
    timestamp=timestamp,
    duration=60
)

if not availability.available:
    next_slot = client.calendars.get_next_available(
        calendar_id="cal_123",
        after=timestamp,
        duration=60
    )
    print(f"Next available slot: {datetime.fromtimestamp(next_slot.timestamp/1000)}")
```

## Constants

### Days of Week
```python
DAYS_OF_WEEK = Literal[
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"
]
```

## Best Practices

1. **Time Handling**
   - Use UTC for internal storage
   - Convert to local time for display
   - Validate time formats

2. **Working Hours**
   - Define complete weekly schedules
   - Handle timezone conversions
   - Consider business rules

3. **Holiday Management**
   - Maintain holiday calendars
   - Handle recurring holidays
   - Consider regional variations

Example with best practices:
```python
from datetime import datetime
import pytz

try:
    # Create calendar with proper timezone handling
    local_tz = pytz.timezone("America/New_York")
    
    calendar = CreateCalendarRequest(
        name="Business Hours",
        timezone=str(local_tz),
        working_hours=[
            WorkingHours(
                day=day,
                intervals=[
                    TimeInterval(
                        start="09:00",
                        end="17:00"
                    )
                ]
            )
            for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]
        ]
    )
    
    response = client.calendars.create(data=calendar)
    
    # Add holidays with timezone consideration
    holiday_date = local_tz.localize(
        datetime(2024, 12, 25)
    ).strftime("%Y-%m-%d")
    
    client.calendars.holidays.add(
        calendar_id=response.calendar_id,
        data=AddHolidayRequest(
            name="Christmas Day",
            date=holiday_date,
            recurring=True
        )
    )
except ValidationError as e:
    logger.error(f"Invalid calendar data: {e}")
    # Handle validation error
except Exception as e:
    logger.error(f"Failed to create calendar: {e}")
    # Handle other errors
```

## Related Documentation

- [Calendars API Reference](../api/calendars.md)
- [Error Handling](../error-handling.md)
- [Best Practices](../best-practices.md) 