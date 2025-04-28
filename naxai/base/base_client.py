import logging
import time

class BaseClient:
    """
    Base logic shared between sync and async clients.
    """

    def __init__(self, api_client_id: str, api_client_secret: str, auth_url: str, logger: logging.Logger = None):
        self.api_client_id = api_client_id
        self.api_client_secret = api_client_secret
        self.auth_url = auth_url
        self.token: str = None
        self.token_expiry: int = 0
        self.logger = logger or logging.getLogger("naxai")
    
    def _is_token_valid(self) -> bool:
        return self.token and (self.token_expiry - time.time()) > 60  # 1 min buffer