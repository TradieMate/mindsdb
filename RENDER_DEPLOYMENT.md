# MindsDB Render Deployment Guide

## 🚀 **Direct GitHub Deployment on Render**

Yes, you can deploy directly from GitHub! Here's the complete configuration:

### **1. Render Service Configuration**

**Service Type**: Web Service  
**Repository**: `https://github.com/TradieMate/mindsdb`  
**Branch**: `cleanup/remove-unused-components-and-folders`  
**Build Command**: `pip install -e .`  
**Start Command**: `python -m mindsdb --api=http,mysql,postgres --host=0.0.0.0 --port=$PORT`

### **2. Complete Environment Variables**

#### **🔧 Required - Supabase Connection**
```bash
SUPABASE_USER=your_supabase_username
SUPABASE_PASSWORD=your_supabase_password
SUPABASE_HOST=your_project_id.supabase.co
SUPABASE_PORT=5432
SUPABASE_DATABASE=postgres
```

#### **🔧 Required - MindsDB Core**
```bash
# Database backend (Render provides PostgreSQL automatically)
MINDSDB_DB_CON=postgresql://user:password@host:port/database

# Storage directory
MINDSDB_STORAGE_DIR=/opt/render/project/src/var

# Docker environment
MINDSDB_DOCKER_ENV=True

# APIs to enable
MINDSDB_APIS=http,mysql,postgres

# Log level
MINDSDB_LOG_LEVEL=INFO

# Flask secret (auto-generated if not set)
FLASK_SECRET_KEY=your_secret_key_here
```

#### **🤖 Required - AI/ML APIs**
```bash
# OpenAI (required for many ML features)
OPENAI_API_KEY=sk-your_openai_api_key

# Default LLM API key (often same as OpenAI)
MINDSDB_DEFAULT_LLM_API_KEY=sk-your_openai_api_key

# Default embedding model API key
MINDSDB_DEFAULT_EMBEDDING_MODEL_API_KEY=sk-your_openai_api_key
```

#### **📊 Optional - Monitoring & Analytics**
```bash
# Sentry error tracking
SENTRY_IO_DSN=https://your_sentry_dsn@sentry.io/project_id
SENTRY_IO_ENVIRONMENT=production

# Langfuse LLM observability
LANGFUSE_HOST=https://your_langfuse_host.com
LANGFUSE_PUBLIC_KEY=pk-lf-your_public_key
LANGFUSE_SECRET_KEY=sk-lf-your_secret_key
LANGFUSE_ENVIRONMENT=production

# OpenTelemetry
OTEL_SERVICE_NAME=mindsdb-render
OTEL_SERVICE_ENVIRONMENT=production
OTEL_EXPORTER_TYPE=console
```

#### **🔐 Optional - Additional AI Providers**
```bash
# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key

# Hugging Face
HUGGINGFACE_API_KEY=hf_your_huggingface_token

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your_resource.openai.azure.com/

# Google AI
GOOGLE_API_KEY=your_google_ai_key

# Cohere
COHERE_API_KEY=your_cohere_api_key
```

### **3. Render Configuration File (render.yaml)**

Create this in your repository root:

```yaml
services:
  - type: web
    name: mindsdb-analytics
    env: python
    region: oregon
    plan: standard
    buildCommand: pip install -e .
    startCommand: python -m mindsdb --api=http,mysql,postgres --host=0.0.0.0 --port=$PORT
    envVars:
      # Supabase Connection
      - key: SUPABASE_USER
        value: your_supabase_username
      - key: SUPABASE_PASSWORD
        value: your_supabase_password
      - key: SUPABASE_HOST
        value: your_project_id.supabase.co
      - key: SUPABASE_PORT
        value: "5432"
      - key: SUPABASE_DATABASE
        value: postgres
      
      # MindsDB Core
      - key: MINDSDB_DB_CON
        fromDatabase:
          name: mindsdb-postgres
          property: connectionString
      - key: MINDSDB_STORAGE_DIR
        value: /opt/render/project/src/var
      - key: MINDSDB_DOCKER_ENV
        value: "True"
      - key: MINDSDB_APIS
        value: http,mysql,postgres
      - key: MINDSDB_LOG_LEVEL
        value: INFO
      
      # AI APIs (add your actual keys)
      - key: OPENAI_API_KEY
        value: sk-your_openai_api_key
      - key: MINDSDB_DEFAULT_LLM_API_KEY
        value: sk-your_openai_api_key
      
      # Optional monitoring
      - key: SENTRY_IO_ENVIRONMENT
        value: production
      - key: OTEL_SERVICE_NAME
        value: mindsdb-render

databases:
  - name: mindsdb-postgres
    databaseName: mindsdb
    user: mindsdb
    plan: starter
```

### **4. Post-Deployment Setup**

After successful deployment, run the analytics models setup:

```bash
# Via Render shell or add to startCommand
python3 scripts/setup_models.py
```

### **5. Render Resource Requirements**

**Minimum:**
- **Plan**: Standard ($25/month)
- **Memory**: 2GB
- **CPU**: 1 vCPU
- **Storage**: 10GB

**Recommended:**
- **Plan**: Pro ($85/month)
- **Memory**: 4GB
- **CPU**: 2 vCPU
- **Storage**: 20GB

### **6. Health Check Endpoint**

Render will automatically monitor: `https://your-app.onrender.com/api/util/ping`

### **7. Access Your MindsDB**

After deployment:
- **HTTP API**: `https://your-app.onrender.com`
- **MySQL**: Connect via Render's external connection
- **PostgreSQL**: Connect via Render's external connection

### **8. Troubleshooting**

**Common Issues:**
1. **Build fails**: Check Python version compatibility
2. **Models don't load**: Verify Supabase credentials
3. **Out of memory**: Upgrade to Pro plan
4. **API timeouts**: Check OpenAI API key validity

**Logs Access:**
```bash
# View logs in Render dashboard or via CLI
render logs -s your-service-name
```

### **9. Security Notes**

- Never commit API keys to GitHub
- Use Render's environment variables for all secrets
- Enable Render's automatic HTTPS
- Consider IP whitelisting for production

This configuration will deploy MindsDB with all your analytics optimization models ready to use!