from .broadcast_metrics_resources.input import InputResource

class MetricsResource:
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.input = InputResource(client, root_path)
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}
        
    async def get(self, broadcast_id: str):
        """
        Get the metrics for a voice broadcast by id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast to cancel.
            
        Returns:
            dict: The API response confirming the cancellation of the broadcast.
            
        Example:
            >>> metrics_result = await client.broadcasts.get_metrics(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """

        return await self._client._request("GET", self.root_path + "/" + broadcast_id + "/metrics", headers=self.headers)