class InputResource:
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}

    async def get(self, broadcast_id: str):
        """
        Get the input for a voice broadcast by id.
        
        Args:
            input_id (str): The unique identifier of the input to get.
            
        Returns:
            dict: The API response containing the input details.
            
        Example:
            >>> input_result = await client.inputs.get(
            ...     input_id="XXXXXXXXX"
            ... )
        """

        return await self._client._request("GET", self.root_path + "/" + broadcast_id + "/metrics/input", headers=self.headers)