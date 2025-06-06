#!/bin/bash
set -e

# Load environment variables
if [ -f .env.streamlined ]; then
    export $(cat .env.streamlined | grep -v '#' | xargs)
fi

# Load Docker environment variables if available
if [ -f .env.docker ]; then
    export $(cat .env.docker | grep -v '#' | xargs)
fi

# Load standard .env file if available
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Set default environment variables if not provided
export MINDSDB_STORAGE_DIR=${MINDSDB_STORAGE_DIR:-"./data"}
export MINDSDB_CONFIG_PATH=${MINDSDB_CONFIG_PATH:-"./config.json"}
export MINDSDB_APIS=${MINDSDB_APIS:-"http"}
export MINDSDB_ENABLED_HANDLERS=${MINDSDB_ENABLED_HANDLERS:-"airtable,supabase,gmail,google_analytics,lightwood,huggingface,huggingface_api,langchain,langchain_embedding,pgvector,postgres,sheets,s3,minds_endpoint,rag"}

# Create directories
mkdir -p ${MINDSDB_STORAGE_DIR}
mkdir -p $(dirname ${MINDSDB_CONFIG_PATH})

# Generate config if not exists
if [ ! -f ${MINDSDB_CONFIG_PATH} ]; then
    cat > ${MINDSDB_CONFIG_PATH} << EOF
{
  "config_version": "1.4",
  "paths": {
    "root": "${MINDSDB_STORAGE_DIR}"
  },
  "integrations": {
    "default_handlers": {
      "airtable": {"enabled": true},
      "supabase": {"enabled": true},
      "gmail": {"enabled": true},
      "google_analytics": {"enabled": true},
      "lightwood": {"enabled": true},
      "huggingface": {"enabled": true},
      "huggingface_api": {"enabled": true},
      "langchain": {"enabled": true},
      "langchain_embedding": {"enabled": true},
      "pgvector": {"enabled": true},
      "postgres": {"enabled": true},
      "sheets": {"enabled": true},
      "s3": {"enabled": true},
      "minds_endpoint": {"enabled": true},
      "rag": {"enabled": true}
    }
  },
  "api": {
    "http": {"host": "0.0.0.0", "port": "47334"}
  }
}
EOF
fi

# Validate credentials if credential system is available
if [ -f "mindsdb/utilities/credentials.py" ]; then
    echo "Validating credentials..."
    python -c "
from mindsdb.utilities.credentials import CredentialManager
import sys
try:
    cm = CredentialManager()
    credentials = cm.get_api_credentials()
    print(f'✅ Found {len(credentials)} configured credentials')
    for name in credentials:
        print(f'  - {name}: ✓')
except Exception as e:
    print(f'⚠️  Credential validation failed: {e}')
    print('Continuing with startup...')
" 2>/dev/null || echo "⚠️  Credential validation skipped (dependencies not available)"
fi

# Display startup information
echo "=========================================="
echo "MindsDB Streamlined Installation Starting"
echo "=========================================="
echo "Storage Directory: ${MINDSDB_STORAGE_DIR}"
echo "Config Path: ${MINDSDB_CONFIG_PATH}"
echo "APIs: ${MINDSDB_APIS}"
echo "Enabled Handlers: ${MINDSDB_ENABLED_HANDLERS}"
echo "=========================================="

# Start MindsDB
echo "Starting MindsDB..."
python -m mindsdb --config ${MINDSDB_CONFIG_PATH} --api ${MINDSDB_APIS}