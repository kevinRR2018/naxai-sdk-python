from typing import Optional, Annotated, Literal
from pydantic import Field
from naxai.models.voice.create_broadcast_request import CreateBroadcastRequest
from naxai.resources.voice_resources.broadcast_resources.metrics import MetricsResource
from naxai.resources.voice_resources.broadcast_resources.recipients import RecipientsResource
from naxai.resources.voice_resources.broadcast_resources.settings import SettingsResource


class BroadcastsResource:
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/broadcasts"
        self.metrics = MetricsResource(self._client, self.root_path)
        self.recipients = RecipientsResource(self._client, self.root_path)
        self.settings = SettingsResource(self._client, self.root_path)
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}

    async def list(self,
                   page: Optional[int] = 1,
                   page_size: Annotated[Optional[int], Field(ge=1, le=100)] = 25):
        """
        Retrieves a list of all broadcast messages.

        Returns:
            dict: The API response containing the list of broadcast messages.

        Example:
            >>> broadcasts = await client.broadcasts.list()
        """
        params = {"page": page, "pagesize": page_size}
        return await self._client._request("GET", self.root_path, headers=self.headers, params=params)
    
    async def create(self, data: CreateBroadcastRequest):
        """
        Creates a new broadcast.

        Args:
            create_broadcast_request (CreateBroadcastRequest): The request body containing the details of the broadcast to be created.

        Returns:
            dict: The API response containing the details of the created broadcast.

        Example:
            >>> new_broadcast = await client.broadcasts.create(
            ...     CreateBroadcastRequest(
            ...         name="My Broadcast",
            ...         message="Hello, world!",
            ...         to="+1234567890"
            ...     )
            ... )
        """
        return await self._client._request("POST", self.root_path, json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)
    
    async def get(self, broadcast_id: str):
        """
        Retrieves a specific broadcast by its ID.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to retrieve.

        Returns:
            dict: The API response containing the details of the broadcast.

        Example:
            >>> broadcast_details = await client.broadcasts.get(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("GET", self.root_path + "/" + broadcast_id, headers=self.headers)
    
    async def delete(self, broadcast_id: str):
        """
        Deletes a specific broadcast by its ID.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to delete.

        Returns:
            dict: The API response confirming the deletion of the broadcast.

        Example:
            >>> deletion_result = await client.broadcasts.delete(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("DELETE", self.root_path + "/" + broadcast_id, headers=self.headers)

    async def update(self, broadcast_id: str, data: CreateBroadcastRequest):
        """
        Updates a specific broadcast by its ID.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to update.
            create_broadcast_request (CreateBroadcastRequest): The request body containing the updated details of the broadcast.

        Returns:
            dict: The API response containing the details of the updated broadcast.

        Example:
            >>> updated_broadcast = await client.broadcasts.update(
            ...     broadcast_id="XXXXXXXXX",
            ...     CreateBroadcastRequest(
            ...         name="Updated Broadcast",
            ...         message="Hello, world!",
            ...         to="+1234567890"
            ...     )
            ... )
        """
        return await self._client._request("PUT", self.root_path + "/" + broadcast_id, json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)

    async def start(self, broadcast_id: str):
        """
        Starts a broadcast.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to start.

        Returns:
            dict: The API response confirming the start of the broadcast.

        Example:
            >>> start_result = await client.broadcasts.start(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("POST", self.root_path + "/" + broadcast_id + "/start", headers=self.headers)
    
    async def pause(self, broadcast_id: str):
        """
        Pauses a broadcast.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to pause.

        Returns:
            dict: The API response confirming the pause of the broadcast.

        Example:
            >>> pause_result = await client.broadcasts.pause(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("POST", self.root_path + "/" + broadcast_id + "/pause", headers=self.headers)
    
    async def resume(self, broadcast_id: str):
        """
        Resumes a broadcast.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to resume.

        Returns:
            dict: The API response confirming the resume of the broadcast.

        Example:
            >>> resume_result = await client.broadcasts.resume(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("POST", self.root_path + "/" + broadcast_id + "/resume", headers=self.headers)
    
    async def cancel(self, broadcast_id: str):
        """
        Cancels a broadcast.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to cancel.

        Returns:
            dict: The API response confirming the cancellation of the broadcast.

        Example:
            >>> cancel_result = await client.broadcasts.cancel(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("POST", self.root_path + "/" + broadcast_id + "/cancel", headers=self.headers)
    