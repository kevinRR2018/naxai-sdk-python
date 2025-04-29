import json
from naxai.models.voice.create_call_request import CreateCallRequest

class CallResource:
    """ call resource for the voice resource """
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/call"


    async def create(self, data: CreateCallRequest):
        """
        Creates a new call.

        Args:
            data (CreateCallRequest): The request body containing the details of the call to be created.

        Returns:
            dict: The API response containing the details of the created call.

        Example:
            >>> new call = await client.voice.call.create(
            ...     CreateCallRequest(
            ...         from_="123456789",
            ...         to="1234567890",
            ...         ...
            ...     )
            ... )
        """
        return await self._client._request("POST", "/voice/call", json=data.model_dump(by_alias=True, exclude_none=True))

