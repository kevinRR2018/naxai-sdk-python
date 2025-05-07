from .broadcast_metrics_resources.input import InputResource

class MetricsResource:
    """
    A class for handling metrics-related operations for voice broadcasts.
    """
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.input = InputResource(client, root_path)
        self.headers = {"Content-Type": "application/json"}
        
    async def get(self, broadcast_id: str):
        """
        Get the metrics for a voice broadcast by id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast.
            
        Returns:
            dict: The API response.
            
        Example:
            >>> metrics_result = await client.voice.broadcasts.metrics.get(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """

        return await self._client._request("GET", self.root_path + "/" + broadcast_id + "/metrics", headers=self.headers)