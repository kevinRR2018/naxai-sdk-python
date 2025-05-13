import asyncio
from naxai.async_client import NaxaiAsyncClient
from naxai.models.calendars.requests import CreateCalendarRequest
from naxai.models.calendars.responses import CreateCalendarResponse
from naxai.models.calendars.schedule_object import ScheduleObject
from naxai.models.calendars.calendar import Calendar

async def main():

    async with NaxaiAsyncClient() as client:

        # Open every work day from 8AM to 4PM
        schedules = [
            ScheduleObject(
                day=1,
                open=True,
                start="08:00",
                stop="16:00" 
            ),
            ScheduleObject(
                day=2,
                open=True,
                start="08:00",
                stop="16:00"
            ),
            ScheduleObject(
                day=3,
                open=True,
                start="08:00",
                stop="16:00"
            ),
            ScheduleObject(
                day=4,
                open=True,
                start="08:00",
                stop="16:00"
            ),
            ScheduleObject(
                day=5,
                open=True,
                start="08:00",
                stop="16:00"
            ),
            ScheduleObject(
                day=6,
                open=False,
            ),
            ScheduleObject(
                day=7,
                open=False,
            )
        ]

        response: CreateCalendarResponse = await client.calendars.create(data=CreateCalendarRequest(name="My Calendar",
                                                                                            description="This is a test calendar from Naxai SDK!",
                                                                                            schedule=schedules))
        print(f"Calendar with id: {response.id} created.")

        calendar: Calendar = await client.calendars.get(response.id)

        print(calendar.model_dump_json(indent=2, by_alias=True, exclude_none=True))

asyncio.run(main())