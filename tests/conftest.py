"""
Pytest configuration and shared fixtures for all tests
"""

import pytest
from unittest.mock import Mock


# ============================================================================
# Fixtures - Reusable test data and mocks
# ============================================================================


@pytest.fixture
def valid_api_key():
    """Valid test API key"""
    return "sk_test_123456789abcdef"


@pytest.fixture
def staging_api_url():
    """Staging API URL for testing"""
    return "https://staging-api.bugbounty-ksp.com"


@pytest.fixture
def mock_auth_response():
    """Mock successful authentication response"""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"authenticated": True}
    return response


@pytest.fixture
def mock_publish_response():
    """Mock successful publish response"""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "article_id": "art_123abc",
        "published_id": "pub_456def",
        "web_url": "https://bugbounty-ksp.com/articles/pub_456def",
        "images": {
            "screenshot1.png": "https://cdn.bugbounty-ksp.com/images/pub_456def/screenshot1.png",
            "screenshot2.png": "https://cdn.bugbounty-ksp.com/images/pub_456def/screenshot2.png",
        },
        "created_at": "2024-02-04T12:00:00Z",
    }
    return response


@pytest.fixture
def mock_delete_response():
    """Mock successful delete response"""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "article_id": "art_123abc",
        "published_id": "pub_456def",
        "deleted_at": "2024-02-04T13:00:00Z",
        "archived": True,
    }
    return response


@pytest.fixture
def mock_get_response():
    """Mock successful get article response"""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "article_id": "art_123abc",
        "published_id": "pub_456def",
        "title": "Test Article",
        "content": "# Test Content",
        "author": "test_author",
        "created_at": "2024-02-04T12:00:00Z",
        "views": 42,
        "likes": 5,
        "images": {},
    }
    return response


@pytest.fixture
def mock_auth_error_response():
    """Mock authentication error response (401)"""
    response = Mock()
    response.status_code = 401
    response.json.return_value = {
        "error": "Invalid API key",
        "error_code": "INVALID_API_KEY",
    }
    return response


@pytest.fixture
def mock_validation_error_response():
    """Mock validation error response (400)"""
    response = Mock()
    response.status_code = 400
    response.json.return_value = {
        "error": "Missing required field: title",
        "error_code": "VALIDATION_ERROR",
        "fields": ["title"],
    }
    return response


@pytest.fixture
def mock_not_found_response():
    """Mock not found error response (404)"""
    response = Mock()
    response.status_code = 404
    response.json.return_value = {
        "error": "Article not found",
        "error_code": "ARTICLE_NOT_FOUND",
    }
    return response


@pytest.fixture
def mock_rate_limit_response():
    """Mock rate limit error response (429)"""
    response = Mock()
    response.status_code = 429
    response.json.return_value = {
        "error": "Rate limit exceeded",
        "error_code": "RATE_LIMIT_EXCEEDED",
        "retry_after": 60,
    }
    return response


# ============================================================================
# Test Data
# ============================================================================


@pytest.fixture
def valid_frontmatter():
    """Valid article frontmatter"""
    return {
        "title": "Test Article Title",
        "tags": ["test", "security", "bug-bounty"],
        "category": "web",
        "difficulty": "intermediate",
        "author": "test_author",
    }


@pytest.fixture
def valid_article_content():
    """Valid article markdown content"""
    return """# Test Article

## Introduction

This is a test article about security vulnerabilities.

## Vulnerability Details

Found a critical vulnerability...

## Proof of Concept

```
vulnerable code
```

## Remediation

Use secure coding practices...
"""


@pytest.fixture
def valid_images():
    """Valid image bytes for testing"""
    return {
        "screenshot1.png": b"fake_png_data_1",
        "screenshot2.png": b"fake_png_data_2",
    }


# ============================================================================
# Markers
# ============================================================================


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests (fast, isolated)")
    config.addinivalue_line("markers", "integration: Integration tests (may need API)")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "mock: Tests using mocks")
