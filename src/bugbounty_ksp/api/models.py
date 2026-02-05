"""
Data models for API requests/responses
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class ArticleMetadata:
    """Article metadata from frontmatter"""

    title: str
    tags: List[str]
    category: str
    difficulty: str
    author: str
    frontmatter: Dict


@dataclass
class PublishResponse:
    """Response from successful article publish"""

    success: bool
    article_id: str
    published_id: str
    web_url: str
    images: Dict[str, str]  # {'filename': 'https://cdn/...'}
    created_at: str


@dataclass
class DeleteResponse:
    """Response from successful article deletion"""

    success: bool
    article_id: str
    published_id: str
    deleted_at: str
    archived: bool  # True = soft delete, False = permanent
