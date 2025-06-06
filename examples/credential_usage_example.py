"""
Example: Using MindsDB Credential Manager

This example demonstrates how to use the credential management system
to securely access API keys and database credentials.
"""

from mindsdb.utilities.credentials import (
    get_credential,
    get_required_credential,
    get_database_url,
    credential_manager
)


def example_basic_usage():
    """Example of basic credential usage."""
    print("=== Basic Credential Usage ===")
    
    # Get an optional credential with a default value
    api_key = get_credential('MINDS_API_KEY', 'default_key')
    print(f"MindsDB API Key: {'Set' if api_key != 'default_key' else 'Using default'}")
    
    # Get a credential that might not exist
    optional_key = get_credential('OPTIONAL_API_KEY')
    if optional_key:
        print(f"Optional key found: {optional_key[:10]}...")
    else:
        print("Optional key not set")


def example_required_credentials():
    """Example of handling required credentials."""
    print("\n=== Required Credentials ===")
    
    try:
        # This will raise an error if the credential is not set
        hf_key = get_required_credential('HUGGING_FACE_API_KEY')
        print(f"Hugging Face key found: {hf_key[:10]}...")
    except ValueError as e:
        print(f"Error: {e}")


def example_database_connections():
    """Example of database credential usage."""
    print("\n=== Database Connections ===")
    
    # Get database URLs
    postgres_url = get_database_url('postgres')
    if postgres_url:
        # Don't print the full URL for security
        print(f"PostgreSQL: Connected (URL length: {len(postgres_url)})")
    else:
        print("PostgreSQL: Not configured")
    
    mysql_url = get_database_url('mysql')
    if mysql_url:
        print(f"MySQL: Connected (URL length: {len(mysql_url)})")
    else:
        print("MySQL: Not configured")


def example_api_credentials():
    """Example of getting all API credentials."""
    print("\n=== API Credentials Summary ===")
    
    api_creds = credential_manager.get_api_credentials()
    
    if api_creds:
        print(f"Found {len(api_creds)} API credentials:")
        for key, value in api_creds.items():
            # Show only that the credential exists, not its value
            print(f"  - {key}: {'✓' if value else '✗'}")
    else:
        print("No API credentials configured")


def example_credential_validation():
    """Example of validating required credentials."""
    print("\n=== Credential Validation ===")
    
    # Define what credentials your application needs
    required_credentials = [
        'MINDS_API_KEY',
        'HUGGING_FACE_API_KEY'
    ]
    
    try:
        result = credential_manager.validate_credentials(required_credentials)
        print("✅ All required credentials are available!")
        print(f"Available: {result['available_keys']}")
    except ValueError as e:
        print(f"❌ Validation failed: {e}")


def example_integration_pattern():
    """Example of a typical integration pattern."""
    print("\n=== Integration Pattern Example ===")
    
    class HuggingFaceIntegration:
        """Example integration class using secure credentials."""
        
        def __init__(self):
            # Get required credentials during initialization
            try:
                self.api_key = get_required_credential('HUGGING_FACE_API_KEY')
                self.initialized = True
                print("✅ HuggingFace integration initialized successfully")
            except ValueError as e:
                print(f"❌ Failed to initialize HuggingFace integration: {e}")
                self.initialized = False
        
        def make_request(self):
            """Example method that uses the credential."""
            if not self.initialized:
                raise RuntimeError("Integration not properly initialized")
            
            # Use self.api_key for API requests
            print(f"Making API request with key: {self.api_key[:10]}...")
            # ... actual API call would go here
    
    # Try to create the integration
    integration = HuggingFaceIntegration()
    if integration.initialized:
        try:
            integration.make_request()
        except RuntimeError as e:
            print(f"Error: {e}")


def main():
    """Run all examples."""
    print("🔐 MindsDB Credential Manager Examples")
    print("=" * 50)
    
    example_basic_usage()
    example_required_credentials()
    example_database_connections()
    example_api_credentials()
    example_credential_validation()
    example_integration_pattern()
    
    print("\n" + "=" * 50)
    print("💡 Tips:")
    print("- Set up your .env file with: python scripts/setup-credentials.py")
    print("- Test your credentials with: python scripts/test-credentials.py")
    print("- See CREDENTIAL_MANAGEMENT.md for full documentation")


if __name__ == "__main__":
    main()