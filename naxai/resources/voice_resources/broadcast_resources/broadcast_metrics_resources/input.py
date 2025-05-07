class InputResource:
    """
    This class provides methods to interact with the Voice Broadcast Metrics Input resource in the API.

    """
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    def get(self, broadcast_id: str):
        """
        Get the inputs for a voice broadcast by id.
        https://docs.naxai.com/reference/voicebroadcastmetricsinputgetbyid

        Args:
            broadcast_id (str): The unique identifier of the broadcast to get the inputs.
            
        Returns:
            dict: The API response containing the input counts for given broadcast.
            
        Example:
            >>> input_result = client.voice.broadcasts.metrics.inputs.get(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """

        return self._client._request("GET", self.root_path + "/" + broadcast_id + "/metrics/input", headers=self.headers)