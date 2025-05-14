from naxai.client import NaxaiClient
from naxai.models.calendars.responses.calendars_responses import GetCalendarResponse

# Assuming NAXAI_CLIENT_ID and NAXAI_SECRET are set in environment.

CALENDAR_ID = "your_calendar_id"

with NaxaiClient() as client:
    response: GetCalendarResponse = client.calendars.get(calendar_id=CALENDAR_ID)

    print(f"calendar id: {response.id}. calendar name: {response.name}.")