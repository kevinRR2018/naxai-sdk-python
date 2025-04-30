from .broadcast_metrics_resources.input import InputResource

class MetricsResource:
    """
    A class for handling metrics-related operations for voice broadcasts.
    """
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.input = InputResource(client, root_path)
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}
        
    def get(self, broadcast_id: str):
        """
        Get the metrics for a voice broadcast by id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast.
            
        Returns:
            dict: The API response.
            
        Example:
            >>> metrics_result = client.voice.broadcasts.metrics.get(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """

        return self._client._request("GET", self.root_path + "/" + broadcast_id + "/metrics", headers=self.headers)