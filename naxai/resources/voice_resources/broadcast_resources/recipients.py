from typing import Annotated, Literal, Optional
from pydantic import Field
from .recipients_resources.calls import CallsResource

class RecipientsResource:
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.calls = CallsResource(client, root_path)
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}
        
    async def list(self,
                    broadcast_id: str,
                    page: Optional[int] = 1,
                    page_size: Annotated[Optional[int], Field(ge=1, le=100)] = 25,
                    phone: Optional[str] = None,
                    completed: Optional[bool] = None,
                    status: Optional[Literal["delivered", "failed", "in-progress", "canceled", "invalid", "paused"]] = None):
        
        """
        Get the recipients for a voice broadcast by id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast to cancel.
            
        Returns:
            dict: The API response confirming the cancellation of the broadcast.
            
        Example:
            >>> metrics_result = await client.broadcasts.list_recipients(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """
        params = {"page": page, "pagesize": page_size}
        if phone is not None:
            params["phone"] = phone
        if completed is not None:
            params["completed"] = completed
        if status is not None:
            params["status"] = status
        return await self._client._request("GET",self.root_path + "/" + broadcast_id + "/recipients", params=params, headers=self.headers)
    
    async def get(self, broadcast_id: str, recipient_id: str):
        """
        Get the recipient details for a voice broadcast by broadcast id and recipient id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast to cancel.
            recipients_id (str): The unique identifier of the recipient
            
        Returns:
            dict: The API response confirming the cancellation of the broadcast.
            
        Example:
            >>> recipients_result = await client.broadcasts.get_recipient_details(
            ...     broadcast_id="XXXXXXXXX",
            ...     recipient_id="XXXXXXXXX"
            ... )
        """

        return await self._client._request("GET",self.root_path + "/" + broadcast_id + "/recipients/" + recipient_id, headers=self.headers )
    
