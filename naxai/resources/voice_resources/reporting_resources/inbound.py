from typing import Literal, Optional
from naxai.base.exceptions import NaxaiValueError

class InboundResource:
    
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/inbound"
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}
        
    async def list(self,
                    group: Literal["hour", "day", "month"],
                    start_date: Optional[str] = None,
                    stop_date: Optional[str] = None,
                    number: Optional[str] = None
                    ):
        #TODO: verify the validation of start_date and stop_date
        if group == "hour":
            if start_date is None:
                raise NaxaiValueError("startDate must be provided when group is 'hour'")

            if len(start_date) < 17 or len(start_date) > 19:
                raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS' when group is 'hour'")
            
            if stop_date is not None and (len(stop_date) < 17 or len(stop_date) > 19):
                raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS' when group is 'hour'")
        else:
            if start_date is None:
                raise NaxaiValueError("startDate must be provided when group is 'day' or 'month'")
            
            if len(start_date) < 8 or len(start_date) > 10:
                raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD' or 'YY-MM-DD'")
            
            if stop_date is None:
                raise NaxaiValueError("stopDate must be provided when group is 'day' or 'month'")
            
            if len(stop_date) < 8 or len(stop_date) > 10:
                raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD' or 'YY-MM-DD'")
            
        params = {"group": group}
        if start_date:
            params["startDate"] = start_date
        if stop_date:
            params["stopDate"] = stop_date
        if number:
            params["number"] = number

        return await self._client._request("GET", self.root_path, params=params, headers=self.headers)