from typing import Optional, Literal
from naxai.base.exceptions import NaxaiValueError

class OutboundResource:
    """
    Outbound Resource for reporting resource
    """
    
    def __init__(self, client, root_path):
        self._client = client
        self.previous_path = root_path
        self.root_path = root_path + "/outbound"
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}
        
    async def list(self,
             group: Literal["hour", "day", "month"],
             start_date: Optional[str] = None,
             stop_date: Optional[str] = None,
             number: Optional[str] = None
             ):
        """
        List outbound calls
        :param group: The group by period for the report. Possible values are 'hour', 'day', 'month'
        :param start_date: The start date for the report. Required if group is 'hour' or 'day'. Format: 'YYYY-MM-DD' or 'YY-MM-DD'
        :param stop_date: The stop date for the report. Required if group is 'hour' or 'day'. Format: 'YYYY-MM-DD' or 'YY-MM-DD'
        :param number: The number to filter the report by. Optional
        :return: The report
        """
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
    
    async def list_by_country(self,
                              start_date: str,
                              stop_date: str,
                              number: Optional[str] = None
                              ):
        """List country, nbr of outbound calls
        :param start_date: The start date for the report. 'YYYY-MM-DD'
        :param stop_date: The stop date for the report. 'YYYY-MM-DD'
        :param number: The number to filter the report by. Optional
        :return: The report
        """
        if len(start_date) != 10:
            raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD'")
        if len(stop_date) != 10:
            raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD'")
        
        params = {"startDate": start_date,
                  "stopDate": stop_date}
        
        if number:
            params["number"] = number

        return await self._client._request("GET", self.previous_path + "/outbound-by-country", params=params, headers=self.headers)