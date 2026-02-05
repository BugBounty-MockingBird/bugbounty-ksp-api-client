"""
Custom exceptions for BugBountyKE-KSP API client
"""


class APIError(Exception):
    """Base exception for API errors"""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(APIError):
    """Raised when authentication fails (invalid API key, 2FA required, etc.)"""

    pass


class ValidationError(APIError):
    """Raised when request validation fails"""

    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded"""

    pass


class NotFoundError(APIError):
    """Raised when resource is not found (404)"""

    pass


class NetworkError(APIError):
    """Raised when network request fails"""

    pass
