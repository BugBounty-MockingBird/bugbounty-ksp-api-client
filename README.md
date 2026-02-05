# BugBountyKE-KSP Python SDK

Official Python SDK for the BugBountyKE-KSP Platform API.

[![PyPI](https://img.shields.io/pypi/v/bugbounty-ksp-api-client.svg)](https://pypi.org/project/bugbounty-ksp-api-client/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-33%20passing-brightgreen.svg)](#testing)

```bash
pip install bugbounty-ksp-api-client
```

## Features

- ✨ Official SDK with full type hints & docstrings
- 🔐 Secure API key generation & validation
- 🔑 Authentication with API keys
- 📤 Article publishing & management
- ⚡ Comprehensive error handling
- 🧪 100% test coverage (33 tests)
- 📚 Full documentation & examples
- 🚀 Published on PyPI

## Quick Start

### 1. Install the SDK

```bash
pip install bugbounty-ksp-api-client
```

### 2. Generate an API Key

```python
from bugbounty_ksp.api import generate_api_key, APIKeyGenerator

# Generate a test API key
test_key = generate_api_key()  # Returns sk_test_*****
print(test_key)  # sk_test_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456

# Or generate multiple keys
keys = APIKeyGenerator.generate_batch(count=5, test=True)

# Validate a key
is_valid = APIKeyGenerator.is_valid_format(test_key)  # True

# Mask key for safe logging
masked = APIKeyGenerator.mask_key(test_key)  # sk_test_****...6
```

### 3. Create Client & Publish

```python
from bugbounty_ksp import BugBountyKSPAPIClient
import os

# Initialize client with API key
api_key = os.environ.get('BUGBOUNTY_API_KEY', 'sk_test_your_key')
client = BugBountyKSPAPIClient(api_key=api_key)

# Publish an article
response = client.publish_article(
    title="Security Vulnerability Report",
    content="# Vulnerability Details\n\nDetails here...",
    frontmatter={
        "title": "Security Vulnerability Report",
        "tags": ["security", "bug-bounty"],
        "category": "web"
    },
    file_path="/path/to/article.md"
)

print(f"Published! View at: {response.web_url}")
```

## Installation

### From PyPI (Recommended)

Latest version: **1.0.0** [![PyPI](https://img.shields.io/pypi/v/bugbounty-ksp-api-client.svg)](https://pypi.org/project/bugbounty-ksp-api-client/)

```bash
pip install bugbounty-ksp-api-client
```

### From Source

```bash
git clone https://github.com/BugBounty-MockingBird/bugbounty-ksp-api-client.git
cd bugbounty-ksp-api-client
pip install -e .
```

### Verify Installation

```python
from bugbounty_ksp import BugBountyKSPAPIClient
from bugbounty_ksp.api import generate_api_key
print("SDK installed successfully!")
```

## API Reference

### Core Classes

#### `BugBountyKSPAPIClient`

Main client for interacting with the API.

```python
client = BugBountyKSPAPIClient(
    api_key="sk_test_...",                  # Required: API key
    api_url="https://api.bugbounty-ksp.com", # Optional: Custom API URL
    verify_ssl=True,                         # Optional: SSL verification
    timeout=30                               # Optional: Request timeout
)
```

**Methods:**
- `publish_article(title, content, frontmatter, file_path)` - Publish article
- `delete_article(article_id)` - Delete article  
- `_verify_authentication()` - Check API key validity (called automatically)

#### `APIKeyGenerator`

Secure API key generation & validation.

```python
from bugbounty_ksp.api.key_generator import APIKeyGenerator

# Generate single key
key = APIKeyGenerator.generate(test=True)  # sk_test_*
prod_key = APIKeyGenerator.generate(test=False)  # sk_*

# Generate batch
keys = APIKeyGenerator.generate_batch(count=5, test=True)

# Validate format
is_valid = APIKeyGenerator.is_valid_format(key)

# Mask for logging
masked = APIKeyGenerator.mask_key(key, visible_chars=4)

# Get info
info = APIKeyGenerator.get_key_info(key)
# Returns: {is_valid, length, masked, environment, type, prefix}
```

**Convenience Functions:**

```python
from bugbounty_ksp.api import generate_api_key, generate_api_keys

# Generate test key
key = generate_api_key()  # sk_test_*

# Generate multiple test keys
keys = generate_api_keys(count=5)
```

### Exception Classes

```python
from bugbounty_ksp.api.exceptions import (
    APIError,                # Base exception
    AuthenticationError,     # Invalid/missing API key
    ValidationError,         # Invalid input
    RateLimitError,         # Too many requests
    NotFoundError,          # Resource not found
    NetworkError,           # Network/connection issues
)
```

## Getting Your API Key

1. Log in to https://bugbountyke-ksp.com
2. Go to Settings → API Keys
3. Click "Generate New Key"
4. Copy the key immediately (shown only once)
5. Store securely in environment variables

```bash
# .env or environment
export BUGBOUNTY_API_KEY="sk_test_your_key_here"
```

## Error Handling

All API errors inherit from `APIError` and provide helpful messages.

```python
from bugbounty_ksp import BugBountyKSPAPIClient
from bugbounty_ksp.api.exceptions import (
    ValidationError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
)

client = BugBountyKSPAPIClient(api_key="sk_test_invalid")

try:
    response = client.publish_article(
        title="",  # Invalid: empty title
        content="Test"
    )
except ValidationError as e:
    print(f"Invalid input: {e}")
    # Handle validation errors

except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Check API key

except RateLimitError as e:
    print(f"Rate limited: {e}")
    # Wait before retrying

except NetworkError as e:
    print(f"Network error: {e}")
    # Handle connection issues
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/BugBounty-MockingBird/bugbounty-ksp-api-client.git
cd bugbounty-ksp-api-client

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=bugbounty_ksp --cov-report=html

# Run specific test class
pytest tests/test.py::TestAPIKeyGenerator -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

### Project Structure

```
bugbounty-ksp-api-client/
├── src/bugbounty_ksp/
│   ├── __init__.py           # Package exports
│   ├── api/
│   │   ├── __init__.py       # API module exports
│   │   ├── client.py         # BugBountyKSPAPIClient class
│   │   ├── exceptions.py     # Custom exceptions
│   │   ├── key_generator.py  # APIKeyGenerator class
│   │   └── models.py         # Response models
│   └── utils/
│       ├── __init__.py
│       └── validators.py     # Input validation
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   └── test.py              # 33 comprehensive tests
├── docs/                    # Documentation
├── setup.py                 # Package setup
├── pyproject.toml          # Project config
└── README.md               # This file
```

## Configuration

### Environment Variables

```bash
# Required
export BUGBOUNTY_API_KEY="sk_test_your_key_here"

# Optional
export BUGBOUNTY_API_URL="https://api.bugbounty-ksp.com"  # Default
export BUGBOUNTY_VERIFY_SSL="true"  # Default
export BUGBOUNTY_TIMEOUT="30"  # Default (seconds)
```

### Custom Configuration

```python
client = BugBountyKSPAPIClient(
    api_key="sk_test_...",
    api_url="https://staging-api.bugbounty-ksp.com",  # Custom environment
    verify_ssl=False,  # Disable SSL for testing
    timeout=60  # Longer timeout for large uploads
)
```

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest tests/`)
5. Follow code style (`black`, `flake8`, `mypy`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

**Code Quality Requirements:**
- ✅ All tests passing
- ✅ Type hints on all functions
- ✅ Docstrings on public methods
- ✅ Code formatted with Black
- ✅ No linting errors with Flake8
- ✅ Type checking passes with MyPy

## License

MIT License - see [LICENSE](LICENSE)

## Support & Links

- 📦 **PyPI:** https://pypi.org/project/bugbounty-ksp-api-client/
- 🐛 **Issues:** https://github.com/BugBounty-MockingBird/bugbounty-ksp-api-client/issues
- 📚 **Docs:** https://docs.bugbounty-ksp.com/
- 🌐 **Website:** https://bugbountyke-ksp.com
- 📧 **Email:** team@bugbounty-ksp.com

## Changelog

### v1.0.0 (February 5, 2026) - Initial Release
- ✨ Official Python SDK release
- 🔐 API key generation & validation
- 📤 Article publishing & management
- ⚡ Comprehensive error handling
- 🧪 33 passing tests (100% coverage)
- 📦 Published to PyPI

---

Made with ❤️ by the **BugBountyKE-KSP Team**

*Part of the BugBountyKE-KSP initiative to centralize cybersecurity knowledge and bridge hunters' expertise.*
