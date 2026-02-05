"""
Validation utilities for API client
"""

from typing import Dict, List


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.

    Args:
        api_key: API key to validate

    Returns:
        True if valid format, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False
    return api_key.startswith("sk_") and len(api_key) > 10


def validate_frontmatter(frontmatter: Dict) -> tuple[bool, str]:
    """
    Validate article frontmatter has required fields.

    Args:
        frontmatter: Frontmatter dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a dictionary"

    required_fields = ["title", "tags", "category", "difficulty", "author"]

    missing = [field for field in required_fields if field not in frontmatter]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    if not isinstance(frontmatter.get("title"), str) or not frontmatter["title"].strip():
        return False, "Title must be a non-empty string"

    if not isinstance(frontmatter.get("tags"), list):
        return False, "Tags must be a list"

    if not all(isinstance(tag, str) for tag in frontmatter["tags"]):
        return False, "All tags must be strings"

    return True, ""
