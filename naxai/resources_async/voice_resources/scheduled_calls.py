from typing import Optional, Annotated
from pydantic import validate_call, Field, StringConstraints


class ScheduledCallsResource:
    """ scheduled_calls resource for voice resouce """
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/scheduled"
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    async def list(self,
                   to: Annotated[str, StringConstraints(min_length=8)],
                   page: Optional[int] = 1,
                   page_size: Annotated[Optional[int], Field(ge=1, le=100)] = 25
                   ):
        """
        Retrieves a list of scheduled calls filtered by the destination phone number.

        Args:
            to (str): The destination phone number to filter scheduled calls.
            page (Optional[int], optional): The page number for pagination. Defaults to 1.
            page_size (Optional[int], optional): Number of items per page. Defaults to 25.

        Returns:
            dict: The API response containing the list of scheduled calls.

        Example:
            >>> scheduled_calls = await client.voice.scheduled_calls.list(
            ...     to="1234567890",
            ...     page=1,
            ...     page_size=10
            ... )
        """

        params = {"to": to,
                  "page": page,
                  "pagesize": page_size}

        return await self._client._request("GET", self.root_path, headers=self.headers, params=params)

    
    async def get(self, call_id: str):
        """
        Retrieves a specific scheduled call by its ID.

        Args:
            call_id (str): The unique identifier of the scheduled call to retrieve.

        Returns:
            dict: The API response containing the scheduled call details.

        Example:
            >>> call_details = await client.voice.scheduled_calls.get(
            ...     call_id="abc123xyz"
            ... )
        """
        self._client.logger.debug("Getting call details for call_id: %s on %s", call_id, self.root_path + "/" + call_id)
        return await self._client._request("GET", self.root_path + "/" + call_id, headers=self.headers)

    async def cancel(self, call_id: str):
        """
        Cancels a specific scheduled call by its ID.

        Args:
            call_id (str): The unique identifier of the scheduled call to cancel.

        Returns:
            dict: The API response confirming the cancellation of the scheduled call.

        Example:
            >>> cancellation_result = await client.voice.scheduled_calls.cancel(
            ...     call_id="abc123xyz"
            ... )

        Note:
            This operation cannot be undone. Once a call is cancelled, it cannot be reinstated.
        """
        return await self._client._request("POST", self.root_path + "/cancel/call", json={"callId": call_id}, headers=self.headers)
    
    async def cancel_batch(self, batch_id: str):
        """
        Cancels all scheduled calls associated with a specific batch ID.

        Args:
            batch_id (str): The unique identifier of the batch to cancel.

        Returns:
            dict: The API response confirming the cancellation of the batch of scheduled calls.

        Example:
            >>> batch_cancellation_result = await client.voice.scheduled_calls.cancel_batch(
            ...     batch_id="batch123xyz"
            ... )

        Note:
            This operation cannot be undone. Once a batch is cancelled, all associated calls
            will be cancelled and cannot be reinstated. This is useful for cancelling multiple
            scheduled calls that were created as part of the same batch operation.
        """
        return await self._client._request("POST", self.root_path + "/cancel/batch", json={"batchId": batch_id}, headers=self.headers)