# MindsDB with MindsChat Deployment Guide

## 🤖 **MindsChat Chatbot Interface**

MindsChat is MindsDB's chatbot interface that connects to chat platforms (Slack, Teams, etc.) and provides conversational AI capabilities.

### **1. Render Service Configuration**

**Service Type**: Web Service  
**Repository**: `https://github.com/TradieMate/mindsdb`  
**Branch**: `cleanup/remove-unused-components-and-folders`  
**Build Command**: `pip install -e .`  
**Start Command**: `python -m mindsdb --api=http --host=0.0.0.0 --port=$PORT --no_studio`

### **2. Complete Environment Variables**

#### **🔧 Required - Supabase Connection**
```bash
SUPABASE_USER=your_supabase_username
SUPABASE_PASSWORD=your_supabase_password
SUPABASE_HOST=your_project_id.supabase.co
SUPABASE_PORT=5432
SUPABASE_DATABASE=postgres
```

#### **🔧 Required - MindsDB Core (ACTUAL Variables)**
```bash
# Database backend for MindsDB metadata (NOT your data)
MINDSDB_DB_CON=postgresql://user:password@host:port/database

# Storage directory for MindsDB files
MINDSDB_STORAGE_DIR=/opt/render/project/src/var

# Default LLM API key (for AI models)
MINDSDB_DEFAULT_LLM_API_KEY=sk-your_openai_key

# Optional: Authentication (if you want login protection)
MINDSDB_USERNAME=admin
MINDSDB_PASSWORD=your_secure_password
```

### **⚠️ IMPORTANT CLARIFICATION**

**For Self-Hosted MindsDB (what we're deploying):**
- ✅ Uses: `MINDSDB_DB_CON`, `MINDSDB_STORAGE_DIR`, `MINDSDB_DEFAULT_LLM_API_KEY`
- ❌ Does NOT use: `MINDSDB_API_KEY`, `MINDSDB_URL` (those are for MindsDB Cloud)

**For MindsDB Cloud (hosted service):**
- ✅ Uses: `MINDSDB_API_KEY`, `MINDSDB_URL` 
- ❌ Does NOT use the self-hosted variables

#### **🤖 Optional - Additional APIs**
```bash
# Google (for Google Ads integration)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Other AI providers (optional)
ANTHROPIC_API_KEY=your_anthropic_key
HUGGINGFACE_API_KEY=your_huggingface_key
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

#### **Step 1: Setup Analytics Models**
```bash
# Via Render shell or add to startCommand
python3 scripts/setup_models.py
```

#### **Step 2: Create a Chatbot**
Connect to your MindsDB instance and create a chatbot:

```sql
-- First, create an agent for your analytics
CREATE AGENT analytics_agent
USING
    model = 'google_ads_optimizer',
    provider = 'mindsdb',
    skills = ['analytics', 'google_ads', 'optimization'];

-- Then create a chatbot (requires chat platform connection)
CREATE CHATBOT analytics_chatbot
USING
    agent = 'analytics_agent',
    database = 'your_chat_platform',  -- e.g., slack, teams
    is_running = true;
```

#### **Step 3: Connect Chat Platform**
To use MindsChat, you need to connect a chat platform:

**For Slack:**
```sql
CREATE DATABASE slack_connection
WITH ENGINE = 'slack',
PARAMETERS = {
    "token": "xoxb-your-slack-bot-token"
};
```

**For Microsoft Teams:**
```sql
CREATE DATABASE teams_connection  
WITH ENGINE = 'teams',
PARAMETERS = {
    "app_id": "your-teams-app-id",
    "app_password": "your-teams-app-password"
};
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

### **7. Access Your MindsDB & MindsChat**

After deployment:
- **HTTP API**: `https://your-app.onrender.com`
- **MindsChat Chatbots**: Available through connected chat platforms (Slack, Teams)
- **Direct API Access**: Use HTTP API for programmatic access
- **SQL Interface**: Connect via MySQL/PostgreSQL protocols

#### **MindsChat Usage Examples:**
Once your chatbot is running, users can interact via chat:

```
User: "What's the performance of our Google Ads campaigns this month?"
Bot: "Based on your Google Ads data, here's the performance summary..."

User: "Optimize our ad spend for better ROI"  
Bot: "I recommend adjusting budgets based on these insights..."
```

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