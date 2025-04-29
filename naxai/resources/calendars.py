import datetime
from typing import Optional
from naxai.models.calendars.create_calendars_request import CreateCalendarRequest
from naxai.base.exceptions import NaxaiValueError
from .calendars_resources import RESOURCE_CLASSES
from .calendars_resources.holidays_templates import HolidaysTemplatesResource


class CalendarsResource:
    """
    Provides access to calendars related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.holidays_templates: HolidaysTemplatesResource
        self.root_path = "/calendars"
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}

        for name, cls in RESOURCE_CLASSES.items():
            self._client.logger.debug("Setting up resource %s. Resource class: %s", name, cls)
            setattr(self, name, cls(client, self.root_path))

    def check(self,
              calendar_id: str,
              timestamp: Optional[int] = datetime.datetime.now(tz=datetime.timezone.utc),
              ):
        """
        Checks the opening of a calendar.

        Args:
            calendar_id (str): The ID of the calendar to check.
            timestamp (Optional[int], optional): The timestamp to check for availability. Defaults to current timestamp utc.

        Returns:
            dict: The API response containing the availability status.

        Example:
            >>> response = client.calendars.check("calendar_id", 1672531200)
        """
        params = {"timestamp": timestamp}
        return self._client._request("GET", self.root_path + "/" + calendar_id + "/check", params=params, headers=self.headers)
        

    def delete_exclusions(self, calendar_id: str, exclusions: list[str]):
        """
        Deletes exclusions from a calendar.

        Args:
            calendar_id (str): The ID of the calendar to delete exclusions from.
            exclusions (list[str]): A list of dates to remove from the calendar's exclusions.

        Returns:
            dict: The API response indicating the success of the operation.

        Example:
            >>> response = client.calendars.delete_exclusion("calendar_id", ["2023-01-01", "2023-01-02"])
        """
        if len(exclusions) > 1000:
            raise NaxaiValueError("You can only delete up to 1000 exclusions at a time.")

        return self._client._request("POST", self.root_path + "/" + calendar_id + "/exclusions/remove", json={"exclusions": exclusions}, headers=self.headers)

    def add_exclusions(self, calendar_id: str, exclusions: list[str]):
        """
        Adds exclusions to a calendar.

        Args:
            calendar_id (str): The ID of the calendar to add exclusions to.
            exclusions (list[str]): A list of dates to exclude from the calendar.

        Returns:
            dict: The API response indicating the success of the operation.

        Example:
            >>> response = client.calendars.add_exclusion("calendar_id", ["2023-01-01", "2023-01-02"])
        """
        if len(exclusions) > 1000:
            raise NaxaiValueError("You can only add up to 1000 exclusions at a time.")
        
        return self._client._request("POST", self.root_path + "/" + calendar_id + "/exclusions/add", json={"exclusions": exclusions}, headers=self.headers)


    def delete(self, calendar_id):
        """
        Deletes a calendar by its ID.

        Args:
            calendar_id (str): The ID of the calendar to delete.

        Returns:
            dict: The API response indicating the success of the deletion.

        Example:
            >>> response = client.calendars.delete("calendar_id")
        """
        return self._client._request("DELETE", self.root_path + "/" + calendar_id, headers=self.headers)


    def update(self, calendar_id: str, data: CreateCalendarRequest):
        """
        Updates an existing calendar.

        Args:
            calendar_id (str): The ID of the calendar to update.
            data (CreateCalendarRequest): The request body containing the updated details of the calendar.

        Returns:
            dict: The API response containing the details of the updated calendar.

        Example:
            >>> updated_calendar = client.calendars.update("calendar_id", CreateCalendarRequest(
            ...     name="Updated Calendar",
            ...     ...
            ... ))
        """
        return self._client._request("PUT", self.root_path + "/" + calendar_id, json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)

    def get(self, calendar_id: str):
        """
        Retrieves a specific calendar by its ID.

        Args:
            calendar_id (str): The ID of the calendar to retrieve.

        Returns:
            dict: The API response containing the details of the requested calendar.

        Example:
            >>> calendar = client.calendars.get("calendar_id")
        """
        return self._client._request("GET", self.root_path + "/" + calendar_id, headers=self.headers)

    def list(self):
        """
        Retrieves a list of calendars.

        Returns:
            dict: The API response containing the list of calendars.

        Example:
            >>> calendars = client.calendars.list()
        """
        return self._client._request("GET", self.root_path, headers=self.headers)

    def create(self,
               data: CreateCalendarRequest):
        """
        Creates a new calendar.

        Args:
            data (CreateCalendarRequest): The request body containing the details of the calendar to be created.

        Returns:
            dict: The API response containing the details of the created calendar.

        Example:
            >>> new_calendar = client.calendars.create(
            ...     CreateCalendarRequest(
            ...         name="My Calender",
            ...         ...
            ...     )
            ... )
        """
        return self._client._request("POST", self.root_path, json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)