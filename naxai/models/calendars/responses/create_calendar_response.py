from typing import Optional
from pydantic import BaseModel
from naxai.models.calendars.schedule_object import ScheduleObject

class CreateCalendarResponse(BaseModel):
    """Model for the response of calendars.create"""
    id: str
    name: str
    timezone: Optional[str] = None
    schedule: list[ScheduleObject]
    exclusions: Optional[list] = None
