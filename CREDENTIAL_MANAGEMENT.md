# Credential Management Guide

This document outlines the secure credential handling system implemented in MindsDB to protect sensitive information like API keys, database credentials, and other configuration data.

## Overview

MindsDB now uses environment variables and `.env` files for secure credential management, ensuring that sensitive information is never committed to version control.

## Quick Start

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your actual credentials:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Set your credentials in the `.env` file:**
   ```env
   MINDS_API_KEY=your_actual_api_key_here
   AIRTABLE_API_KEY=your_airtable_key_here
   # ... etc
   ```

## Supported Credentials

### API Keys
- `MINDS_API_KEY` - MindsDB API key for authentication
- `AIRTABLE_API_KEY` - Airtable integration API key
- `HUGGING_FACE_API_KEY` - Hugging Face model access key
- `OPENAI_API_KEY` - OpenAI API key for GPT models and other services

### Database Connections
- `SUPABASE_POSTGRES_URL` - Supabase PostgreSQL connection string
- `MYSQL_URL` - MySQL database connection string
- `MONGODB_URL` - MongoDB connection string

### Cloud Storage
- `S3_BUCKET_URL` - S3 or CloudFlare R2 bucket URL

### OAuth Configuration
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret

## Usage in Code

### Basic Usage

```python
from mindsdb.utilities.credentials import get_credential, get_required_credential

# Get an optional credential with default
api_key = get_credential('MINDS_API_KEY', 'default_key')

# Get a required credential (raises error if missing)
required_key = get_required_credential('HUGGING_FACE_API_KEY')
```

### Database Connections

```python
from mindsdb.utilities.credentials import get_database_url

# Get database URL by type
postgres_url = get_database_url('postgres')
mysql_url = get_database_url('mysql')
```

### Advanced Usage

```python
from mindsdb.utilities.credentials import credential_manager

# Get all available API credentials
api_creds = credential_manager.get_api_credentials()

# Validate required credentials
try:
    credential_manager.validate_credentials([
        'MINDS_API_KEY',
        'HUGGING_FACE_API_KEY'
    ])
    print("All required credentials are available")
except ValueError as e:
    print(f"Missing credentials: {e}")
```

## Security Best Practices

### 1. Never Commit Credentials
- The `.env` file is automatically ignored by Git
- Always use the `.env.example` template for documentation
- Never hardcode credentials in source code

### 2. Environment-Specific Configuration
- Use different `.env` files for different environments
- Production credentials should be set directly in the deployment environment
- Development credentials can use the local `.env` file

### 3. Credential Rotation
- Regularly rotate API keys and passwords
- Update credentials in your `.env` file when they change
- Test credential changes in development before deploying

## Deployment Considerations

### Local Development
1. Copy `.env.example` to `.env`
2. Fill in your development credentials
3. The `.env` file will be automatically loaded

### Production Deployment

#### Docker
Set environment variables in your Docker configuration:
```yaml
# docker-compose.yml
services:
  mindsdb:
    environment:
      - MINDS_API_KEY=${MINDS_API_KEY}
      - HUGGING_FACE_API_KEY=${HUGGING_FACE_API_KEY}
```

#### Kubernetes
Use Kubernetes secrets:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mindsdb-credentials
type: Opaque
stringData:
  MINDS_API_KEY: "your_api_key_here"
  HUGGING_FACE_API_KEY: "your_hf_key_here"
```

#### Cloud Platforms
- **AWS**: Use AWS Systems Manager Parameter Store or Secrets Manager
- **Google Cloud**: Use Google Secret Manager
- **Azure**: Use Azure Key Vault
- **Heroku**: Set config vars in the dashboard

## Troubleshooting

### Common Issues

1. **Credential not found error:**
   ```
   ValueError: Required credential 'MINDS_API_KEY' not found
   ```
   **Solution**: Check that the environment variable is set in your `.env` file or system environment.

2. **`.env` file not loading:**
   **Solution**: Install python-dotenv: `pip install python-dotenv`

3. **Permission denied errors:**
   **Solution**: Ensure your `.env` file has appropriate read permissions.

### Debugging

Enable debug logging to see credential loading:
```python
import logging
logging.basicConfig(level=logging.INFO)

from mindsdb.utilities.credentials import credential_manager
# Will show info about .env file loading
```

## Migration from Hardcoded Credentials

If you're migrating from hardcoded credentials:

1. **Identify hardcoded credentials** in your codebase
2. **Replace with credential manager calls:**
   ```python
   # Before
   api_key = "hardcoded_key_here"
   
   # After
   from mindsdb.utilities.credentials import get_required_credential
   api_key = get_required_credential('MINDS_API_KEY')
   ```
3. **Add credentials to `.env.example`** for documentation
4. **Set actual values in your `.env` file**

## Dependencies

The credential management system has minimal dependencies:

- **Required**: Python standard library (`os`, `pathlib`, `logging`)
- **Optional**: `python-dotenv` for `.env` file support

Install the optional dependency:
```bash
pip install python-dotenv
```

## Contributing

When adding new credential requirements:

1. **Update `.env.example`** with the new credential
2. **Document the credential** in this guide
3. **Use the credential manager** in your code
4. **Test with missing credentials** to ensure proper error handling

## Security Considerations

- **Never log credential values** - the credential manager only logs keys, not values
- **Use HTTPS** for all API communications
- **Implement credential validation** before using them
- **Consider credential expiration** and rotation policies
- **Monitor for credential leaks** in logs and error messages

## Support

For questions about credential management:

1. Check this documentation first
2. Review the `.env.example` file for credential format
3. Check the credential manager source code in `mindsdb/utilities/credentials.py`
4. Open an issue if you encounter problems