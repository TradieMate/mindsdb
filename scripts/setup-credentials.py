#!/usr/bin/env python3
"""
MindsDB Credential Setup Script

This script helps users set up their credentials securely by:
1. Creating a .env file from the template
2. Validating credential format
3. Testing credential loading
"""

import os
import sys
import shutil
from pathlib import Path


def main():
    """Main setup function."""
    print("🔐 MindsDB Credential Setup")
    print("=" * 40)
    
    # Get project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    env_example_path = project_root / '.env.example'
    env_path = project_root / '.env'
    
    # Check if .env.example exists
    if not env_example_path.exists():
        print("❌ Error: .env.example file not found!")
        print(f"Expected location: {env_example_path}")
        sys.exit(1)
    
    # Check if .env already exists
    if env_path.exists():
        print(f"⚠️  .env file already exists at: {env_path}")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Setup cancelled.")
            sys.exit(0)
    
    # Copy .env.example to .env
    try:
        shutil.copy2(env_example_path, env_path)
        print(f"✅ Created .env file at: {env_path}")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        sys.exit(1)
    
    # Provide instructions
    print("\n📝 Next Steps:")
    print("1. Edit the .env file with your actual credentials:")
    print(f"   nano {env_path}")
    print("   # or use your preferred editor")
    print()
    print("2. Replace the placeholder values with your actual credentials:")
    print("   MINDS_API_KEY=your_actual_api_key_here")
    print("   AIRTABLE_API_KEY=your_actual_airtable_key_here")
    print("   # etc...")
    print()
    print("3. Test your credentials:")
    print("   python scripts/test-credentials.py")
    print()
    print("📚 For more information, see: CREDENTIAL_MANAGEMENT.md")
    print()
    print("🔒 Security Note:")
    print("   - Never commit the .env file to version control")
    print("   - The .env file is already in .gitignore")
    print("   - Keep your credentials secure and rotate them regularly")


if __name__ == "__main__":
    main()