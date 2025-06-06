#!/usr/bin/env python3
"""
MindsDB Credential Testing Script

This script tests the credential management system by:
1. Loading credentials from environment variables
2. Validating credential format
3. Testing the credential manager functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from mindsdb.utilities.credentials import credential_manager, get_credential
except ImportError as e:
    print(f"❌ Error importing credential manager: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


def test_credential_loading():
    """Test basic credential loading functionality."""
    print("🔍 Testing credential loading...")
    
    # Test credentials that are commonly used
    test_credentials = [
        'MINDS_API_KEY',
        'AIRTABLE_API_KEY', 
        'HUGGING_FACE_API_KEY',
        'OPENAI_API_KEY',
        'SUPABASE_POSTGRES_URL',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET',
        'S3_BUCKET_URL'
    ]
    
    found_credentials = []
    missing_credentials = []
    
    for cred in test_credentials:
        value = get_credential(cred)
        if value and value != f"your_{cred.lower()}_here":
            found_credentials.append(cred)
            # Don't print the actual value for security
            print(f"  ✅ {cred}: Found (length: {len(value)})")
        else:
            missing_credentials.append(cred)
            print(f"  ❌ {cred}: Not set or using placeholder value")
    
    return found_credentials, missing_credentials


def test_database_urls():
    """Test database URL retrieval."""
    print("\n🗄️  Testing database URL retrieval...")
    
    db_types = ['postgres', 'mysql', 'mongodb']
    
    for db_type in db_types:
        url = credential_manager.get_database_url(db_type)
        if url:
            print(f"  ✅ {db_type}: Found")
        else:
            print(f"  ❌ {db_type}: Not configured")


def test_api_credentials():
    """Test API credential retrieval."""
    print("\n🔑 Testing API credentials...")
    
    api_creds = credential_manager.get_api_credentials()
    
    if api_creds:
        print(f"  ✅ Found {len(api_creds)} API credentials:")
        for key in api_creds.keys():
            print(f"    - {key}")
    else:
        print("  ❌ No API credentials found")


def validate_credential_format():
    """Validate that credentials have reasonable formats."""
    print("\n🔍 Validating credential formats...")
    
    # Check for common placeholder values that indicate unconfigured credentials
    placeholder_patterns = [
        'your_',
        'placeholder',
        'example',
        'change_me',
        'replace_this'
    ]
    
    warnings = []
    
    # Test some key credentials
    minds_key = get_credential('MINDS_API_KEY')
    if minds_key:
        if any(pattern in minds_key.lower() for pattern in placeholder_patterns):
            warnings.append("MINDS_API_KEY appears to be a placeholder value")
        elif len(minds_key) < 10:
            warnings.append("MINDS_API_KEY seems too short")
    
    hf_key = get_credential('HUGGING_FACE_API_KEY')
    if hf_key:
        if not hf_key.startswith('hf_'):
            warnings.append("HUGGING_FACE_API_KEY should start with 'hf_'")
    
    openai_key = get_credential('OPENAI_API_KEY')
    if openai_key:
        if not openai_key.startswith('sk-'):
            warnings.append("OPENAI_API_KEY should start with 'sk-'")
    
    postgres_url = get_credential('SUPABASE_POSTGRES_URL')
    if postgres_url:
        if not postgres_url.startswith('postgresql://'):
            warnings.append("SUPABASE_POSTGRES_URL should start with 'postgresql://'")
    
    if warnings:
        print("  ⚠️  Validation warnings:")
        for warning in warnings:
            print(f"    - {warning}")
    else:
        print("  ✅ No format issues detected")


def main():
    """Main testing function."""
    print("🧪 MindsDB Credential Testing")
    print("=" * 40)
    
    # Check if .env file exists
    env_path = project_root / '.env'
    if env_path.exists():
        print(f"📁 Found .env file at: {env_path}")
    else:
        print("⚠️  No .env file found. Using system environment variables only.")
        print("   Run 'python scripts/setup-credentials.py' to create one.")
    
    print()
    
    # Run tests
    found_creds, missing_creds = test_credential_loading()
    test_database_urls()
    test_api_credentials()
    validate_credential_format()
    
    # Summary
    print("\n📊 Summary")
    print("-" * 20)
    print(f"✅ Configured credentials: {len(found_creds)}")
    print(f"❌ Missing credentials: {len(missing_creds)}")
    
    if missing_creds:
        print("\n💡 To configure missing credentials:")
        print("1. Edit your .env file:")
        print(f"   nano {env_path}")
        print("2. Set the missing credentials:")
        for cred in missing_creds[:3]:  # Show first 3
            print(f"   {cred}=your_actual_value_here")
        if len(missing_creds) > 3:
            print(f"   ... and {len(missing_creds) - 3} more")
    
    print("\n📚 For more help, see: CREDENTIAL_MANAGEMENT.md")
    
    # Exit with appropriate code
    if found_creds:
        print("\n🎉 Credential system is working!")
        sys.exit(0)
    else:
        print("\n⚠️  No credentials configured yet.")
        sys.exit(1)


if __name__ == "__main__":
    main()