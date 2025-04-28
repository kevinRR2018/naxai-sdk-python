import time
import os
import httpx
from typing import Any, Optional
from naxai.base.base_client import BaseClient
from naxai.base.exceptions import *
from naxai.models.token_response import TokenResponse
from naxai.resources import RESOURCE_CLASSES
from naxai.resources.voice import VoiceResource
from .config import API_BASE_URL, AUTH_URL

class NaxaiAsyncClient(BaseClient):
    """
    Async Naxai Client for interacting with Voice, SMS, Email and RCS APIs.
    """

    voice: Optional[VoiceResource]

    def __init__(self,
                 api_client_id: Optional[str] = os.getenv("NAXAI_CLIENT_ID"),
                 api_client_secret: Optional[str] = os.getenv("NAXAI_SECRET"),
                 auth_url: Optional[str] = AUTH_URL,
                 api_base_url: Optional[str] = API_BASE_URL,
                 logger=None):
        if not api_client_id or not api_client_secret:
            raise NaxaiValueError("api_client_id and api_client_secret must be provided.")
        super().__init__(api_client_id, api_client_secret, auth_url, logger)
        self.api_base_url = api_base_url
        self._http = httpx.AsyncClient()
        self.voice = VoiceResource(self)
        # Dynamically load resources
        for resource_name, resource_class in RESOURCE_CLASSES.items():
            setattr(self, resource_name, resource_class(self))

    async def _authenticate(self):
        if self._is_token_valid():
            return

        payload = {
            "client_id": self.api_client_id,
            "client_secret": self.api_client_secret,
            "grant_type": "client_credentials",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = await self._http.post(self.auth_url, data=payload, headers=headers)
        
        if response.is_error:
            raise NaxaiAuthenticationError(f"Authentication failed: {response.text}", status_code=response.status_code)
        
        data = TokenResponse.model_validate(response.json())
        self.token = data.access_token
        self.token_expiry = time.time() + data.expires_in
        self.logger.info("Authenticated successfully, token valid for 24h.")

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        await self._authenticate()

        headers = kwargs.pop("headers", {})
        headers.update({"Authorization": f"Bearer {self.token}"})

        url = f"{self.api_base_url.rstrip('/')}/{path.lstrip('/')}"


        response = await self._http.request(method, url, headers=headers, **kwargs)
        
        if response.is_error:
            await self._handle_error(response)

        if response.status_code == 204:
            return None

        return response.json()

    async def _handle_error(self, response: httpx.Response):
        try:
            error_data = response.json().get("error", {})
        except Exception:
            error_data = {}

        code = error_data.get("code")
        message = error_data.get("message", response.text)
        details = error_data.get("details")

        exc_args = {"message": message, "status_code": response.status_code, "error_code": code, "details": details}

        if response.status_code == 401:
            raise NaxaiAuthenticationError(**exc_args)
        elif response.status_code == 403:
            raise NaxaiAuthorizationError(**exc_args)
        elif response.status_code == 404:
            raise NaxaiResourceNotFound(**exc_args)
        elif response.status_code == 429:
            raise NaxaiRateLimitExceeded(**exc_args)
        else:
            raise NaxaiAPIRequestError(**exc_args)
        
    async def aclose(self):
        await self._http.aclose()