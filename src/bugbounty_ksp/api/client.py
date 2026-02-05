"""
Main API client for BugBountyKE-KSP platform
"""

import requests
import json
from typing import Dict, Optional, Tuple
from pathlib import Path

from .exceptions import (
    APIError,
    AuthenticationError,
    ValidationError,
    NetworkError,
    RateLimitError,
    NotFoundError,
)
from .models import ArticleMetadata, PublishResponse, DeleteResponse


class BugBountyKSPAPIClient:
    """
    Official Python SDK for BugBountyKE-KSP Platform

    Handles:
    - Authentication with API keys
    - Article publishing (create/update)
    - Image uploads
    - Error handling and retries
    """

    DEFAULT_API_URL = "https://api.bugbounty-ksp.com"
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3

    def __init__(
        self,
        api_key: str,
        api_url: str = DEFAULT_API_URL,
        verify_ssl: bool = True,
    ):
        """
        Initialize API client.

        Args:
            api_key: Bearer token for authentication
            api_url: Base API URL (default: production)
            verify_ssl: Verify SSL certificates (default: True)

        Raises:
            ValidationError: If API key is invalid
        """
        if not api_key or not isinstance(api_key, str):
            raise ValidationError("API key must be a non-empty string")

        if not api_key.startswith("sk_"):
            raise ValidationError("Invalid API key format. Must start with 'sk_'")

        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.verify_ssl = verify_ssl

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "BugBountyKSP-SDK/1.0",
            "Accept": "application/json",
        }

        self._session = requests.Session()
        self._session.headers.update(self.headers)

        # Verify authentication on init
        self._verify_authentication()

    def _verify_authentication(self) -> None:
        """
        Verify API key is valid.

        Raises:
            AuthenticationError: If API key is invalid
        """
        try:
            response = self._request("GET", "/api/auth/verify", timeout=5)
            if response.status_code != 200:
                raise AuthenticationError(
                    "Invalid API key. Verify at: https://bugbounty-ksp.com/settings/api-keys"
                )
        except requests.RequestException as e:
            raise NetworkError(f"Failed to verify authentication: {e}")

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        timeout: int = REQUEST_TIMEOUT,
        **kwargs,
    ) -> requests.Response:
        """
        Make authenticated request to API.

        Args:
            method: HTTP method (GET, POST, PUT, etc.)
            endpoint: API endpoint (e.g., '/api/articles/publish')
            data: Request body
            files: Files for multipart upload
            timeout: Request timeout in seconds
            **kwargs: Additional arguments for requests

        Returns:
            Response object

        Raises:
            APIError: If request fails
        """
        url = f"{self.api_url}{endpoint}"

        try:
            if files:
                # Multipart upload - don't set Content-Type
                headers = self.headers.copy()
                response = self._session.request(
                    method,
                    url,
                    data=data,
                    files=files,
                    timeout=timeout,
                    verify=self.verify_ssl,
                    **kwargs,
                )
            else:
                # Regular JSON request
                response = self._session.request(
                    method,
                    url,
                    json=data,
                    timeout=timeout,
                    verify=self.verify_ssl,
                    **kwargs,
                )

            # Handle errors based on status code
            self._handle_response_errors(response)

            return response

        except requests.Timeout:
            raise NetworkError(f"Request timeout after {timeout}s")
        except requests.ConnectionError as e:
            raise NetworkError(f"Connection failed: {e}")
        except requests.RequestException as e:
            raise NetworkError(f"Request failed: {e}")

    def _handle_response_errors(self, response: requests.Response) -> None:
        """
        Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object

        Raises:
            AuthenticationError: 401/403
            NotFoundError: 404
            ValidationError: 400/422
            RateLimitError: 429
            APIError: Other error responses
        """
        if response.status_code < 400:
            return  # Success

        try:
            error_data = response.json()
        except:
            error_data = {"error": response.text}

        error_message = error_data.get("error", f"HTTP {response.status_code}")

        if response.status_code == 401:
            raise AuthenticationError(
                f"Unauthorized: {error_message}. Check your API key.",
                status_code=401,
                response=error_data,
            )
        elif response.status_code == 403:
            raise AuthenticationError(
                f"Forbidden: {error_message}. Check your permissions.",
                status_code=403,
                response=error_data,
            )
        elif response.status_code == 404:
            raise NotFoundError(
                f"Not found: {error_message}",
                status_code=404,
                response=error_data,
            )
        elif response.status_code in [400, 422]:
            raise ValidationError(
                f"Validation error: {error_message}",
                status_code=response.status_code,
                response=error_data,
            )
        elif response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded. Please try again later.",
                status_code=429,
                response=error_data,
            )
        else:
            raise APIError(
                f"API error: {error_message}",
                status_code=response.status_code,
                response=error_data,
            )

    def publish_article(
        self,
        title: str,
        content: str,
        frontmatter: Dict,
        images: Dict[str, bytes],
        file_path: str,
    ) -> PublishResponse:
        """
        Publish new article to platform.

        Args:
            title: Article title
            content: Processed markdown content (with relative image paths)
            frontmatter: Article metadata (YAML parsed as dict)
            images: Dict of {'filename': file_bytes}
            file_path: Original file path (for tracking)

        Returns:
            PublishResponse with article_id, published_id, web_url, image URLs

        Raises:
            ValidationError: If required fields missing
            AuthenticationError: If API key invalid
            NetworkError: If request fails
            APIError: If publication fails
        """
        # Validate required fields
        if not title or not content:
            raise ValidationError("Title and content are required")

        if not isinstance(frontmatter, dict):
            raise ValidationError("Frontmatter must be a dictionary")

        # Prepare request data
        data = {
            "title": title,
            "content": content,
            "frontmatter": json.dumps(frontmatter),
            "file_path": file_path,
        }

        # Prepare files for multipart upload
        files = {}
        for filename, file_bytes in (images or {}).items():
            files[f"images[{filename}]"] = (filename, file_bytes)

        # Make request
        response = self._request(
            "POST", "/api/articles/publish", data=data, files=files if files else None
        )

        # Parse response
        result = response.json()

        return PublishResponse(
            success=True,
            article_id=result["article_id"],
            published_id=result["published_id"],
            web_url=result["web_url"],
            images=result.get("images", {}),
            created_at=result["created_at"],
        )

    def get_article(self, published_id: str) -> Dict:
        """Get article details"""
        response = self._request("GET", f"/api/articles/{published_id}")
        return response.json()

    def delete_article(self, published_id: str) -> DeleteResponse:
        """
        Delete/archive an article.
        
        Note: Only the article owner or moderators can delete articles.
        Articles are soft-deleted (archived), not permanently removed.

        Args:
            published_id: Article's published_id

        Returns:
            DeleteResponse with deletion confirmation

        Raises:
            NotFoundError: If article not found
            AuthenticationError: If no permission to delete
            APIError: If deletion fails
        """
        response = self._request("DELETE", f"/api/articles/{published_id}")
        result = response.json()

        return DeleteResponse(
            success=True,
            article_id=result["article_id"],
            published_id=result["published_id"],
            deleted_at=result["deleted_at"],
            archived=result.get("archived", True),
        )

    def close(self) -> None:
        """Close the session"""
        if self._session:
            self._session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
