import asyncio
from naxai.async_client import NaxaiAsyncClient
from naxai.models.calendars.responses.calendars_responses import ListCalendarsResponse

# Assuming NAXAI_CLIENT_ID and NAXAI_SECRET are set in environment.

async def main():
    async with NaxaiAsyncClient() as client:
        response: ListCalendarsResponse = client.calendars.list()

        print(f"Total calendars: {len(response)}")

        for calendar in response:
            print(f"Calendar: {calendar.name} ({calendar.id})")

asyncio.run(main())
