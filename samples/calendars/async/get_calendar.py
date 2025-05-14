import asyncio
from naxai.async_client import NaxaiAsyncClient
from naxai.models.calendars.responses.calendars_responses import GetCalendarResponse

# Assuming NAXAI_CLIENT_ID and NAXAI_SECRET are set in environment.

CALENDAR_ID = "your_calendar_id"

async def main():
    async with NaxaiAsyncClient() as client:
        response: GetCalendarResponse = await client.calendars.get(calendar_id=CALENDAR_ID)

        print(f"calendar id: {response.id}. calendar name: {response.name}.")

asyncio.run(main())
