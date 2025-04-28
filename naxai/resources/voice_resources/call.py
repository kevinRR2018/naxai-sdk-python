import json
from naxai.models.voice.create_call_request import CreateCallRequest

class CallResource:
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/call"


    async def create(self, data: CreateCallRequest):
        return await self._client._request("POST", "/voice/call", json=data.model_dump(by_alias=True, exclude_none=True))

