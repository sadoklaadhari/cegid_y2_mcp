# Cegid Y2 MCP Server - Deployment Guide

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Configuration](#configuration)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)
8. [Scaling](#scaling)

---

## Prerequisites

### System Requirements

- **OS**: Linux, macOS, or Windows
- **CPU**: 2+ cores
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 500MB free space
- **Network**: Outbound HTTPS access to Cegid API

### Software Requirements

- Python 3.11+ OR Docker 20.10+
- pip (if using local installation)
- Git
- Optional: Redis 6.0+, PostgreSQL 12+

### Cegid Y2 Requirements

- Valid Cegid Y2 subscription
- API credentials (API Key or OAuth2)
- API key with required permissions
- Network access to Cegid API (api.cegid.com)

---

## Local Development

### 1. Install Python Dependencies

```bash
# Clone repository
git clone <repo-url>
cd cegid_y2_mcp

# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp config/.env.example config/.env

# Edit with your credentials
nano config/.env
# or Windows:
notepad config\.env
```

### 3. Update Configuration

Edit `config/config.json` with:
- Cegid API credentials
- JWT secret key
- Redis settings (optional)
- CORS origins
- Rate limits

### 4. Start Development Server

```bash
# Linux/macOS
./start.sh

# Windows
start.bat

# Or directly:
python src/mcp_server.py
```

### 5. Verify Installation

```bash
# Check server health
curl http://localhost:8000/health

# View API documentation
# Open browser: http://localhost:8000/docs
```

---

## Docker Deployment

### 1. Build Docker Image

```bash
# Using provided Dockerfile
docker build -f docker/Dockerfile -t cegid-mcp-server:1.0 .

# Or use docker-compose (builds automatically)
docker-compose -f docker/docker-compose.yml up --build
```

### 2. Run Container

```bash
# Copy environment file
cp config/.env.example config/.env

# Edit environment file
nano config/.env

# Start with docker-compose (recommended)
docker-compose -f docker/docker-compose.yml up -d

# Or run individual container
docker run -d \
  --name cegid-mcp \
  -p 8000:8000 \
  -p 8001:8001 \
  -e CEGID_API_KEY=$CEGID_API_KEY \
  -e JWT_SECRET_KEY=$JWT_SECRET_KEY \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config:/app/config \
  cegid-mcp-server:1.0
```

### 3. Verify Docker Deployment

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f mcp-server

# Health check
curl http://localhost:8000/health

# Inspect running container
docker-compose exec mcp-server bash
```

### 4. Docker-Compose Services

Services automatically deployed:

- **mcp-server**: FastAPI application on port 8000
- **redis**: Caching layer on port 6379
- **postgres**: Optional database on port 5432

---

## Production Deployment

### 1. Cloud Deployment (AWS/Azure/GCP)

#### AWS ECS (Elastic Container Service)

```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag cegid-mcp-server:1.0 <account-id>.dkr.ecr.us-east-1.amazonaws.com/cegid-mcp:1.0

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/cegid-mcp:1.0
```

#### Azure Container Instances

```bash
# Create registry
az acr create --resource-group mygroup --name cegidmcp --sku Basic

# Build and push
az acr build --registry cegidmcp --image cegid-mcp:1.0 .

# Deploy
az container create \
  --resource-group mygroup \
  --name cegid-mcp \
  --image cegidmcp.azurecr.io/cegid-mcp:1.0 \
  --ports 8000 \
  --environment-variables \
    CEGID_API_KEY=$CEGID_API_KEY \
    JWT_SECRET_KEY=$JWT_SECRET_KEY
```

### 2. Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cegid-mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cegid-mcp
  template:
    metadata:
      labels:
        app: cegid-mcp
    spec:
      containers:
      - name: mcp-server
        image: cegid-mcp-server:1.0
        ports:
        - containerPort: 8000
        env:
        - name: CEGID_API_KEY
          valueFrom:
            secretKeyRef:
              name: cegid-secrets
              key: api-key
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: cegid-secrets
              key: jwt-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

Deploy with kubectl:
```bash
kubectl apply -f deployment.yaml
kubectl expose deployment cegid-mcp-server --type=LoadBalancer --port=80 --target-port=8000
```

### 3. Traditional VM Deployment (Linux)

```bash
# Install Python and dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Clone and setup
git clone <repo-url> /opt/cegid-mcp
cd /opt/cegid-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp config/.env.example config/.env
sudo nano config/.env  # Edit with your credentials

# Create systemd service
sudo tee /etc/systemd/system/cegid-mcp.service <<EOF
[Unit]
Description=Cegid Y2 MCP Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/cegid-mcp
Environment="PATH=/opt/cegid-mcp/venv/bin"
ExecStart=/opt/cegid-mcp/venv/bin/python /opt/cegid-mcp/src/mcp_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable cegid-mcp
sudo systemctl start cegid-mcp

# Check status
sudo systemctl status cegid-mcp

# View logs
sudo journalctl -u cegid-mcp -f
```

---

## Configuration

### Environment Variables Priority

1. System environment variables (highest priority)
2. .env file
3. config.json defaults
4. Built-in defaults (lowest priority)

### Key Configuration Parameters

```bash
# Cegid API
CEGID_API_KEY=your_key
CEGID_CLIENT_ID=your_client_id
CEGID_CLIENT_SECRET=your_secret

# Security
JWT_SECRET_KEY=very-long-random-string
DEFAULT_API_KEY=your_default_key

# Caching
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Server
SERVER_PORT=8000
DEBUG=false
LOG_LEVEL=INFO

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=cegid_user
DB_PASSWORD=secure_password
DB_NAME=cegid_y2
```

### SSL/TLS Configuration

For production HTTPS:

```python
# In config.json
{
  "server": {
    "ssl": true,
    "ssl_certfile": "/path/to/cert.pem",
    "ssl_keyfile": "/path/to/key.pem"
  }
}
```

Or with Docker:
```bash
docker run -d \
  -v /path/to/cert.pem:/app/cert.pem \
  -v /path/to/key.pem:/app/key.pem \
  cegid-mcp-server:1.0
```

---

## Monitoring

### Health Checks

```bash
# Server health
curl http://localhost:8000/health

# Server capabilities
curl http://localhost:8000/capabilities

# Metrics
curl http://localhost:8000/metrics

# Cegid API health
curl http://localhost:8000/mcp/request \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"method": "health"}'
```

### Logs

**Location**: `logs/mcp_server.log` or Docker logs

**Commands**:
```bash
# Docker logs (real-time)
docker-compose logs -f mcp-server

# Docker logs (last 100 lines)
docker-compose logs --tail=100 mcp-server

# Linux systemd logs
sudo journalctl -u cegid-mcp -f

# Linux file logs
tail -f logs/mcp_server.log

# Windows Event Viewer
eventvwr.msc
```

### Metrics Collection

Configure Prometheus scraping:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'cegid-mcp'
    static_configs:
      - targets: ['localhost:8001']
```

### Alerting

Setup alerts for:
- Server downtime
- High error rates
- Slow API response times
- Cache hit ratio drops
- Memory usage
- CPU usage

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Use different port
python src/mcp_server.py --port 8001
```

#### 2. Redis Connection Failed
```bash
# Check Redis is running
redis-cli ping

# Start Redis
redis-server  # macOS/Linux
redis-server.exe  # Windows

# Or disable Redis in config
# Falls back to in-memory cache automatically
```

#### 3. Cegid API Authentication Error
```bash
# Verify API key
echo $CEGID_API_KEY

# Check API endpoint connectivity
curl -I https://api.cegid.com/y2/v1/health

# Verify key has required permissions in Cegid dashboard
```

#### 4. Out of Memory
```bash
# Increase Docker memory limit
docker-compose.yml:
  services:
    mcp-server:
      mem_limit: 1g

# Or on Linux VM
free -h
# Monitor with:
watch -n 1 'free -h'
```

#### 5. Slow Performance
```bash
# Check cache hit ratio
curl http://localhost:8000/metrics

# Enable Redis if not enabled
REDIS_ENABLED=true

# Check API response times
# In logs, look for "duration" field

# Increase rate limits if needed
# Adjust in config.json
```

---

## Scaling

### Horizontal Scaling (Multiple Instances)

**With Docker Compose**:
```bash
# Scale to 3 instances
docker-compose up -d --scale mcp-server=3

# With load balancer (nginx)
upstream mcp_servers {
  server mcp-server:8000;
  server mcp-server-2:8000;
  server mcp-server-3:8000;
}
```

**With Kubernetes**:
```bash
# Scale replicas
kubectl scale deployment cegid-mcp-server --replicas=5

# Auto-scale based on CPU
kubectl autoscale deployment cegid-mcp-server \
  --min=2 --max=10 --cpu-percent=70
```

### Vertical Scaling (Larger Instance)

```bash
# Increase Docker resources
docker-compose.yml:
  services:
    mcp-server:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### Database Optimization

```sql
-- Index frequently queried fields
CREATE INDEX idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX idx_invoices_date ON invoices(issue_date);
CREATE INDEX idx_customers_email ON customers(email);

-- Monitor slow queries
EXPLAIN ANALYZE SELECT * FROM invoices WHERE customer_id = ?;
```

### Caching Strategy

```python
# Adjust TTL based on data volatility
{
  "redis": {
    "ttl_by_resource": {
      "invoices": 600,      # 10 minutes
      "customers": 3600,    # 1 hour
      "products": 86400,    # 24 hours
      "financial": 3600     # 1 hour
    }
  }
}
```

---

## Backup & Recovery

### Backup Data

```bash
# Backup database
pg_dump -U cegid_user -h localhost cegid_y2 > backup.sql

# Backup Redis
redis-cli --rdb /path/to/backup.rdb

# Backup configuration
tar -czf config_backup.tar.gz config/
```

### Restore Data

```bash
# Restore database
psql -U cegid_user -h localhost cegid_y2 < backup.sql

# Restore Redis
cp /path/to/backup.rdb /var/lib/redis/dump.rdb
redis-cli shutdown
redis-server

# Restore configuration
tar -xzf config_backup.tar.gz
```

---

## Upgrade Guide

### Version Upgrade

```bash
# 1. Backup current version
docker-compose down
cp -r cegid_y2_mcp cegid_y2_mcp_backup

# 2. Pull latest code
git pull origin main

# 3. Update dependencies
pip install --upgrade -r requirements.txt

# 4. Database migrations (if any)
python src/mcp_server.py --migrate

# 5. Rebuild Docker image
docker-compose build --no-cache

# 6. Start updated version
docker-compose up -d

# 7. Verify
curl http://localhost:8000/health
```

---

## Security Checklist

- [ ] Change JWT_SECRET_KEY from default
- [ ] Use strong API keys (min 32 characters)
- [ ] Enable HTTPS/TLS in production
- [ ] Restrict CORS origins to known domains
- [ ] Enable rate limiting
- [ ] Regular backups configured
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable audit logging
- [ ] Implement VPN/firewall for API access
- [ ] Regular security audits

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Response Time | < 200ms | 95th percentile |
| Availability | 99.9% | 8.7 hours downtime/month |
| CPU Usage | < 70% | Peak load |
| Memory Usage | < 80% | Configured limit |
| Cache Hit Ratio | > 80% | For read operations |
| Error Rate | < 0.1% | Per 10k requests |

---

## Support & Rollback

If deployment fails:

```bash
# Rollback to previous version
cd cegid_y2_mcp_backup
docker-compose up -d

# Or restore from backup
pg_restore backup.sql
redis-cli flushdb
```

---

**Last Updated**: January 14, 2026
**Built with ❤️ by TIMSOFT Société**
