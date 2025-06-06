"""
Secure credential management utility for MindsDB.

This module provides secure handling of API keys, database credentials,
and other sensitive configuration data using environment variables.
"""

import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class CredentialManager:
    """
    Manages secure credential loading from environment variables.
    
    This class provides a centralized way to access credentials while
    ensuring they are loaded securely from environment variables rather
    than being hardcoded in the application.
    """
    
    def __init__(self):
        """Initialize the credential manager."""
        self._load_env_file()
    
    def _load_env_file(self) -> None:
        """
        Load environment variables from .env file if it exists.
        
        This method looks for a .env file in the project root and loads
        any environment variables defined in it.
        """
        try:
            # Try to import python-dotenv for .env file support
            from dotenv import load_dotenv
            
            # Look for .env file in project root
            env_path = Path(__file__).parent.parent.parent / '.env'
            if env_path.exists():
                load_dotenv(env_path)
                logger.info("Loaded environment variables from .env file")
            else:
                logger.info("No .env file found, using system environment variables")
                
        except ImportError:
            logger.warning(
                "python-dotenv not installed. Install it with 'pip install python-dotenv' "
                "to support .env files for local development"
            )
    
    def get_credential(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get a credential from environment variables.
        
        Args:
            key: The environment variable name
            default: Default value if the credential is not found
            
        Returns:
            The credential value or default if not found
        """
        value = os.getenv(key, default)
        if value is None:
            logger.warning(f"Credential '{key}' not found in environment variables")
        return value
    
    def get_required_credential(self, key: str) -> str:
        """
        Get a required credential from environment variables.
        
        Args:
            key: The environment variable name
            
        Returns:
            The credential value
            
        Raises:
            ValueError: If the credential is not found
        """
        value = self.get_credential(key)
        if value is None:
            raise ValueError(
                f"Required credential '{key}' not found in environment variables. "
                f"Please set the {key} environment variable or add it to your .env file."
            )
        return value
    
    def get_database_url(self, db_type: str) -> Optional[str]:
        """
        Get a database connection URL for a specific database type.
        
        Args:
            db_type: The database type (e.g., 'postgres', 'mysql', 'mongodb')
            
        Returns:
            The database connection URL or None if not found
        """
        # Try specific database URL first
        url_key = f"{db_type.upper()}_URL"
        url = self.get_credential(url_key)
        
        if url:
            return url
        
        # Try legacy format for backward compatibility
        if db_type.lower() == 'postgres':
            return self.get_credential('SUPABASE_POSTGRES_URL')
        
        return None
    
    def get_api_credentials(self) -> Dict[str, Optional[str]]:
        """
        Get all API credentials as a dictionary.
        
        Returns:
            Dictionary containing all available API credentials
        """
        credentials = {
            'minds_api_key': self.get_credential('MINDS_API_KEY'),
            'airtable_api_key': self.get_credential('AIRTABLE_API_KEY'),
            'hugging_face_api_key': self.get_credential('HUGGING_FACE_API_KEY'),
            'openai_api_key': self.get_credential('OPENAI_API_KEY'),
            'google_client_id': self.get_credential('GOOGLE_CLIENT_ID'),
            'google_client_secret': self.get_credential('GOOGLE_CLIENT_SECRET'),
            's3_bucket_url': self.get_credential('S3_BUCKET_URL'),
        }
        
        # Filter out None values
        return {k: v for k, v in credentials.items() if v is not None}
    
    def validate_credentials(self, required_keys: list) -> Dict[str, Any]:
        """
        Validate that all required credentials are available.
        
        Args:
            required_keys: List of required environment variable names
            
        Returns:
            Dictionary with validation results
            
        Raises:
            ValueError: If any required credentials are missing
        """
        missing_keys = []
        available_keys = []
        
        for key in required_keys:
            if self.get_credential(key) is not None:
                available_keys.append(key)
            else:
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(
                f"Missing required credentials: {', '.join(missing_keys)}. "
                f"Please set these environment variables or add them to your .env file."
            )
        
        return {
            'status': 'valid',
            'available_keys': available_keys,
            'missing_keys': missing_keys
        }


# Global credential manager instance
credential_manager = CredentialManager()


def get_credential(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Convenience function to get a credential.
    
    Args:
        key: The environment variable name
        default: Default value if not found
        
    Returns:
        The credential value or default
    """
    return credential_manager.get_credential(key, default)


def get_required_credential(key: str) -> str:
    """
    Convenience function to get a required credential.
    
    Args:
        key: The environment variable name
        
    Returns:
        The credential value
        
    Raises:
        ValueError: If the credential is not found
    """
    return credential_manager.get_required_credential(key)


def get_database_url(db_type: str) -> Optional[str]:
    """
    Convenience function to get a database URL.
    
    Args:
        db_type: The database type
        
    Returns:
        The database connection URL or None
    """
    return credential_manager.get_database_url(db_type)