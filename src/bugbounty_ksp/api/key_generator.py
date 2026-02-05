"""
API Key Generation and Management Module

Provides secure generation, validation, and management of API keys.
"""

import secrets
import string
from datetime import datetime
from typing import Optional, Dict, List


class APIKeyGenerator:
    """Generate and validate API keys with security best practices"""
    
    # Constants
    PREFIX = "sk_"
    TEST_PREFIX = "sk_test_"
    KEY_LENGTH = 32
    CHARSET = string.ascii_letters + string.digits
    
    @staticmethod
    def generate(test: bool = True) -> str:
        """
        Generate a secure random API key.
        
        Args:
            test: If True, generates test key (sk_test_*), else production key (sk_*)
            
        Returns:
            Secure random API key string
        """
        prefix = APIKeyGenerator.TEST_PREFIX if test else APIKeyGenerator.PREFIX
        random_part = ''.join(
            secrets.choice(APIKeyGenerator.CHARSET)
            for _ in range(APIKeyGenerator.KEY_LENGTH)
        )
        return prefix + random_part
    
    @staticmethod
    def generate_batch(count: int = 5, test: bool = True) -> List[str]:
        """
        Generate multiple API keys.
        
        Args:
            count: Number of keys to generate
            test: If True, generates test keys, else production keys
            
        Returns:
            List of generated API keys
        """
        return [APIKeyGenerator.generate(test=test) for _ in range(count)]
    
    @staticmethod
    def is_valid_format(key: Optional[str]) -> bool:
        """
        Validate if key matches expected format.
        
        Args:
            key: Key to validate
            
        Returns:
            True if key format is valid
        """
        if not isinstance(key, str):
            return False
        
        if not key:
            return False
        
        # Check prefix
        if not (key.startswith(APIKeyGenerator.PREFIX)):
            return False
        
        # Check minimum length (prefix + at least 8 chars)
        if len(key) < len(APIKeyGenerator.PREFIX) + 8:
            return False
        
        # Check that after prefix, only alphanumeric characters
        random_part = key[len(APIKeyGenerator.PREFIX):]
        if not all(c.isalnum() for c in random_part):
            return False
        
        return True
    
    @staticmethod
    def mask_key(key: str, visible_chars: int = 4) -> str:
        """
        Mask key for safe logging (show only last N characters).
        
        Args:
            key: API key to mask
            visible_chars: Number of characters to show at end
            
        Returns:
            Masked key string (e.g., "sk_test_****...****abcd")
        """
        if not key:
            return ""
        
        if len(key) <= visible_chars:
            return "*" * len(key)
        
        # Keep prefix visible
        prefix_len = len(APIKeyGenerator.PREFIX)
        if len(key) <= prefix_len + visible_chars:
            return key
        
        # Show prefix + stars + last N chars
        visible_end = key[-visible_chars:]
        hidden_len = len(key) - prefix_len - visible_chars
        masked_part = "*" * hidden_len
        
        return APIKeyGenerator.PREFIX + masked_part + visible_end
    
    @staticmethod
    def get_key_info(key: str) -> Dict:
        """
        Extract information about a key.
        
        Args:
            key: API key to analyze
            
        Returns:
            Dictionary with key information
        """
        is_valid = APIKeyGenerator.is_valid_format(key)
        
        info = {
            "is_valid": is_valid,
            "length": len(key),
            "masked": APIKeyGenerator.mask_key(key),
            "created_at": datetime.now().isoformat(),
        }
        
        if is_valid:
            info["prefix"] = APIKeyGenerator.PREFIX
            info["type"] = "secret_key"
            
            # Determine if test or production
            if key.startswith(APIKeyGenerator.TEST_PREFIX):
                info["environment"] = "test"
            else:
                info["environment"] = "production"
        else:
            info["type"] = "invalid"
            info["prefix"] = None
        
        return info


def generate_api_key(test: bool = True) -> str:
    """
    Convenience function to generate a single API key.
    
    Args:
        test: If True, generates test key, else production key
        
    Returns:
        Generated API key
    """
    return APIKeyGenerator.generate(test=test)


def generate_api_keys(count: int = 5, test: bool = True) -> List[str]:
    """
    Convenience function to generate multiple API keys.
    
    Args:
        count: Number of keys to generate
        test: If True, generates test keys, else production keys
        
    Returns:
        List of generated API keys
    """
    return APIKeyGenerator.generate_batch(count=count, test=test)
