from typing import Optional, Literal, Annotated
from pydantic import Field, validate_call

class ActivityLogsResource:
    """ activity_logs resource for voice resource """


    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/activity-logs"
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    async def list(self,
                   page: Optional[int] = 1,
                   page_size: Annotated[Optional[int], Field(ge=1, le=100)] = 25,
                   start: Optional[int] = None,
                   stop: Optional[int] = None,
                   direction: Optional[Literal["inbound", "outbound", "transfer"]] = None,
                   status: Optional[Literal["delivered", "failed"]] = None,
                   from_: Annotated[Optional[str], Field(alias="from")] = None,
                   to: Optional[str] = None,
                   client_id: Optional[str] = None,
                   survey_id: Optional[str] = None,
                   campaign_id: Optional[str] = None,
                   broadcast_id: Optional[str] = None
                   ):
        """
        Retrieves a list of activity logs based on specified filters.

        Args:
            page (int, optional): The page number for pagination. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.
            order_by (str, optional): The order of the results, either "asc" or "desc". Defaults to "desc".
            order_by_field (str, optional): The field to order the results by, either "created_at" or "updated_at". Defaults to "created_at".
            from_date (str, optional): The start date for filtering activity logs in ISO format (YYYY-MM-DD).
            to_date (str, optional): The end date for filtering activity logs in ISO format (YYYY-MM-DD).

        Returns:
            dict: The API response containing the list of activity logs.

        Example:
            >>> activity_logs = await client.voice.activity_logs.list(
            ...     page=1,
            ...     page_size=10,
            ...     order_by="desc",
            ...     order_by_field="created_at",
            ...     from_date="2023-01-01",
            ...     to_date="2023-12-31"
            ... )
        """
        params = {
            "page": page,
            "page_size": page_size,
        }

        if start:
            params["start"] = start
        if stop:
            params["stop"] = stop
        if direction:
            params["direction"] = direction
        if status:
            params["status"] = status
        if from_:
            params["from"] = from_
        if to:
            params["to"] = to
        if client_id:
            params["clientId"] = client_id
        if survey_id:
            params["surveyId"] = survey_id
        if campaign_id:
            params["campaignId"] = campaign_id
        if broadcast_id:
            params["broadcastId"] = broadcast_id

        return await self._client._request("GET", self.root_path, params=params, headers=self.headers)
    
    async def get(self, call_id:str):
        """
        Retrieves a specific activity log by call ID.

        Args:
            call_id (str): The unique identifier of the call to retrieve.

        Returns:
            dict: The API response containing the activity log details.

        Example:
            >>> activity_log = await client.voice.activity_logs.get(
            ...     call_id="XXXXXXXXX"
            ... )
        """
        
        return await self._client._request("GET", self.root_path + "/" + call_id, headers=self.headers)
