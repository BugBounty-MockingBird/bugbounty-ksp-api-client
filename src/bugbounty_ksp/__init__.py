"""
BugBountyKE-KSP Official Python SDK
"""

__version__ = "1.0.0"
__author__ = "BugBountyKE-KSP Team"

from .api.client import BugBountyKSPAPIClient
from .api.exceptions import (
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    NotFoundError,
)

__all__ = [
    "BugBountyKSPAPIClient",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "NotFoundError",
]
