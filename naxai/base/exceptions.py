from typing import Optional, Any

class NaxaiException(Exception):
    """Base exception for all Naxai SDK errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, error_code: Optional[str] = None, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message} (status_code={self.status_code}, error_code={self.error_code})"

class NaxaiAuthenticationError(NaxaiException): pass
class NaxaiAuthorizationError(NaxaiException): pass
class NaxaiResourceNotFound(NaxaiException): pass
class NaxaiRateLimitExceeded(NaxaiException): pass
class NaxaiAPIRequestError(NaxaiException): pass
class NaxaiValueError(NaxaiException): pass