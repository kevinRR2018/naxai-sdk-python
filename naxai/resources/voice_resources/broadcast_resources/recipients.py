from typing import Annotated, Literal, Optional
from pydantic import Field
from .recipients_resources.calls import CallsResource

class RecipientsResource:
    """
        A class for handling recipients-related operations for voice broadcasts.
    """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.calls = CallsResource(client, root_path)
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}
        
    def list(self,
            broadcast_id: str,
            page: Optional[int] = 1,
            page_size: Annotated[Optional[int], Field(ge=1, le=100)] = 25,
            phone: Optional[str] = None,
            completed: Optional[bool] = None,
            status: Optional[Literal["delivered", "failed", "in-progress", "canceled", "invalid", "paused"]] = None):
        
        """
        Get the recipients for a voice broadcast by broadcast id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast to cancel.
            page (Optional[int]): Page number to retrieve. Defaults to 1.
            page_size (Optional[int]): Number of items to list per page. Defaults to 25.
            phone (Optional[str]): If provided, only results for this phone number will be returned;
            completed (Optional[bool]): If set, only recipients who completed the broadcast will be returned.
            status (Optional[Literal["delivered", "failed", "in-progress", "canceled", "invalid", "paused"]]):
                    If provided, only recipients with provided status will be returned
            
        Returns:
            dict: The API response confirming recipients of the broadcast.
            
        Example:
            >>> metrics_result = client.voice.broadcasts.recipients.list(
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
        return self._client._request("GET",self.root_path + "/" + broadcast_id + "/recipients", params=params, headers=self.headers)
    
    def get(self, broadcast_id: str, recipient_id: str):
        """
        Get the recipient details for a voice broadcast by broadcast id and recipient id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast.
            recipients_id (str): The unique identifier of the recipient
            
        Returns:
            dict: The API response containing the recipient.
            
        Example:
            >>> recipients_result = client.voice.broadcasts.recipients.get(
            ...     broadcast_id="XXXXXXXXX",
            ...     recipient_id="XXXXXXXXX"
            ... )
        """

        return self._client._request("GET",self.root_path + "/" + broadcast_id + "/recipients/" + recipient_id, headers=self.headers )
    
