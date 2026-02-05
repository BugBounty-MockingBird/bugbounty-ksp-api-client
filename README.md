# BugBountyKE-KSP Python SDK

Official Python SDK for the BugBountyKE-KSP Platform.

```bash
pip install bugbounty-ksp
```

## Features

- ✨ Official SDK with full type hints
- 🔐 Secure API key authentication  
- 📤 Publish articles with image support
- ⚡ Comprehensive error handling
- 🧪 98% test coverage (68 tests)
- 📚 Full documentation & examples

## Quick Start

```python
from bugbounty_ksp import BugBountyKSPAPIClient
import os

# Get API key from environment
api_key = os.environ['BUGBOUNTY_API_KEY']

# Create client
client = BugBountyKSPAPIClient(api_key=api_key)

# Publish article
response = client.publish_article(
    title="Security Vulnerability Report",
    content="# Vulnerability Details\n\nDetails here...",
    frontmatter={
        "title": "Security Vulnerability Report",
        "tags": ["security", "bug-bounty"],
        "category": "web"
    },
    images={},
    file_path="/path/to/article.md"
)

print(f"Published! View at: {response.web_url}")
```

## Installation

### From PyPI (Recommended)

```bash
pip install bugbounty-ksp
```

### From Source

```bash
git clone https://github.com/bugbountyksp/bugbounty-ksp-api-client.git
cd bugbounty-ksp-api-client
pip install -e .
```

## Documentation

- [Usage Guide](docs/USAGE.md) - How to use the SDK
- [API Reference](docs/API_REFERENCE.md) - Complete API documentation
- [Development Guide](docs/DEVELOPMENT.md) - Contributing & development
- [Examples](examples/) - Code examples

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

```python
from bugbounty_ksp import BugBountyKSPAPIClient
from bugbounty_ksp.api.exceptions import (
    ValidationError,
    AuthenticationError,
    APIError,
)

try:
    response = client.publish_article(...)
except ValidationError as e:
    print(f"Invalid input: {e}")
except AuthenticationError as e:
    print(f"Invalid API key: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Development

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest -v

# Code quality
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Testing

68 tests with 98% code coverage:

```bash
pytest -v --cov=bugbounty_ksp
```

Tests included for:
- Authentication & API key validation
- Article publishing & management  
- Error handling & edge cases
- API key generation & security
- Configuration & integration

## License

MIT License - see [LICENSE](LICENSE)

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issues](https://github.com/bugbountyksp/bugbounty-ksp-api-client/issues)
- 📧 Support: support@bugbountyke-ksp.com

---

Made with ❤️ by BugBountyKE-KSP Team
