# MindsDB Streamlined Docker Deployment Guide

This guide covers deploying MindsDB with a streamlined configuration using Docker, focusing on essential handlers and optimized performance.

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/TradieMate/mindsdb.git
cd mindsdb
```

### 2. Configure Credentials

```bash
# Copy the Docker environment template
cp .env.docker.example .env.docker

# Edit with your actual credentials
nano .env.docker
```

### 3. Deploy with Docker Compose

```bash
# Build and start the container
docker-compose -f docker-compose.streamlined.yml up -d

# Check logs
docker-compose -f docker-compose.streamlined.yml logs -f
```

### 4. Access MindsDB

- **HTTP API**: http://localhost:47334
- **Health Check**: http://localhost:47334/api/status

## 📋 Configuration

### Enabled Handlers

The streamlined deployment includes only essential handlers:

- **Data Sources**: Airtable, Supabase, PostgreSQL, Sheets, S3
- **AI/ML**: Lightwood, Hugging Face, OpenAI, LangChain
- **Communication**: Gmail, Google Analytics
- **Vector/RAG**: PGVector, RAG, LangChain Embedding
- **Custom**: Minds Endpoint

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MINDS_API_KEY` | MindsDB API key | ✅ |
| `OPENAI_API_KEY` | OpenAI API key | ✅ |
| `HUGGING_FACE_API_KEY` | Hugging Face API key | ✅ |
| `AIRTABLE_API_KEY` | Airtable API key | ⚠️ |
| `SUPABASE_POSTGRES_URL` | Supabase PostgreSQL URL | ⚠️ |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | ⚠️ |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | ⚠️ |
| `S3_BUCKET_URL` | S3/CloudFlare R2 bucket URL | ⚠️ |

✅ = Required for core functionality  
⚠️ = Required for specific integrations

## 🔧 Advanced Configuration

### Custom Handler Selection

Modify the `MINDSDB_ENABLED_HANDLERS` environment variable:

```bash
# In .env.docker
MINDSDB_ENABLED_HANDLERS=lightwood,openai,postgres,airtable
```

### Resource Limits

Add resource constraints to `docker-compose.streamlined.yml`:

```yaml
services:
  mindsdb-streamlined:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
        reservations:
          memory: 2G
          cpus: '1.0'
```

### Persistent Storage

Data is automatically persisted in the `mindsdb_data` Docker volume. To backup:

```bash
# Create backup
docker run --rm -v mindsdb_data:/data -v $(pwd):/backup alpine tar czf /backup/mindsdb-backup.tar.gz -C /data .

# Restore backup
docker run --rm -v mindsdb_data:/data -v $(pwd):/backup alpine tar xzf /backup/mindsdb-backup.tar.gz -C /data
```

## 🛠️ Development

### Building Custom Images

```bash
# Build with custom tag
./scripts/build-streamlined.sh v1.0.0

# Build with development dependencies
docker build -f Dockerfile.streamlined -t mindsdb-dev --target builder .
```

### Local Development

```bash
# Start with local source code mounting
docker-compose -f docker-compose.streamlined.yml -f docker-compose.dev.yml up -d
```

## 🔍 Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   # Check logs
   docker-compose -f docker-compose.streamlined.yml logs mindsdb-streamlined
   
   # Check configuration
   docker-compose -f docker-compose.streamlined.yml config
   ```

2. **Handler not loading**
   ```bash
   # Verify handler is in enabled list
   docker exec mindsdb-streamlined env | grep MINDSDB_ENABLED_HANDLERS
   
   # Check handler-specific dependencies
   docker exec mindsdb-streamlined pip list | grep -i handler_name
   ```

3. **Credential issues**
   ```bash
   # Test credential loading
   docker exec mindsdb-streamlined python -c "
   from mindsdb.utilities.credentials import CredentialManager
   cm = CredentialManager()
   print('Available credentials:', cm.get_api_credentials())
   "
   ```

### Health Checks

```bash
# Container health
docker-compose -f docker-compose.streamlined.yml ps

# API health
curl -f http://localhost:47334/api/status

# Handler status
curl -f http://localhost:47334/api/handlers
```

## 🚀 Production Deployment

### Docker Swarm

```yaml
version: '3.8'
services:
  mindsdb-streamlined:
    image: mindsdb-streamlined:latest
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    networks:
      - mindsdb-network
    secrets:
      - mindsdb-credentials

secrets:
  mindsdb-credentials:
    external: true

networks:
  mindsdb-network:
    driver: overlay
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mindsdb-streamlined
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mindsdb-streamlined
  template:
    metadata:
      labels:
        app: mindsdb-streamlined
    spec:
      containers:
      - name: mindsdb
        image: mindsdb-streamlined:latest
        ports:
        - containerPort: 47334
        env:
        - name: MINDS_API_KEY
          valueFrom:
            secretKeyRef:
              name: mindsdb-secrets
              key: minds-api-key
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

### Security Best Practices

1. **Use secrets management**
   ```bash
   # Docker secrets
   echo "your_api_key" | docker secret create minds_api_key -
   ```

2. **Network isolation**
   ```yaml
   networks:
     mindsdb-internal:
       driver: bridge
       internal: true
   ```

3. **Read-only filesystem**
   ```yaml
   security_opt:
     - no-new-privileges:true
   read_only: true
   tmpfs:
     - /tmp
     - /var/tmp
   ```

## 📊 Monitoring

### Prometheus Metrics

MindsDB exposes metrics on `/metrics` endpoint:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'mindsdb'
    static_configs:
      - targets: ['mindsdb-streamlined:47334']
    metrics_path: '/metrics'
```

### Logging

Configure structured logging:

```bash
# In .env.docker
MINDSDB_LOG_LEVEL=INFO
MINDSDB_LOG_FORMAT=json
```

## 🔗 Integration Examples

### With Nginx Reverse Proxy

```nginx
upstream mindsdb {
    server localhost:47334;
}

server {
    listen 80;
    server_name mindsdb.yourdomain.com;
    
    location / {
        proxy_pass http://mindsdb;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### With Traefik

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.mindsdb.rule=Host(`mindsdb.yourdomain.com`)"
  - "traefik.http.services.mindsdb.loadbalancer.server.port=47334"
```

## 📚 Additional Resources

- [MindsDB Documentation](https://docs.mindsdb.com/)
- [Handler Documentation](https://docs.mindsdb.com/integrations/overview)
- [API Reference](https://docs.mindsdb.com/rest/overview)
- [Credential Management Guide](./CREDENTIAL_MANAGEMENT.md)