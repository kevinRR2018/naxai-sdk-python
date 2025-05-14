from naxai.client import NaxaiClient
from naxai.models.calendars.responses.calendars_responses import ListCalendarsResponse

# Assuming NAXAI_CLIENT_ID and NAXAI_SECRET are set in environment.

with NaxaiClient() as client:
    response: ListCalendarsResponse = client.calendars.list()

    print(f"Total calendars: {len(response)}")

    for calendar in response:
        print(f"Calendar: {calendar.name} ({calendar.id})")
