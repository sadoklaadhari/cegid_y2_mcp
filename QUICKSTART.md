# Cegid Y2 MCP Server - Quick Reference

## 📁 Project Structure

```
cegid_y2_mcp/
├── src/                          # Source code
│   ├── mcp_server.py            # Main FastAPI application
│   ├── api_client.py            # Cegid Y2 API client
│   ├── resources.py             # MCP Resources definitions
│   ├── tools.py                 # MCP Tools definitions
│   ├── prompts.py               # MCP Prompts definitions
│   ├── auth.py                  # Authentication & Authorization
│   ├── cache.py                 # Redis cache management
│   └── utils.py                 # Helper utilities
│
├── config/                       # Configuration
│   ├── config.json              # Main configuration
│   └── .env.example             # Environment template
│
├── tests/                       # Unit tests
│   ├── test_tools.py           # Tools tests
│   ├── test_api_client.py       # API client tests
│   └── test_mcp_server.py       # Server tests
│
├── docker/                      # Docker configuration
│   ├── Dockerfile               # Container image
│   └── docker-compose.yml       # Multi-container setup
│
├── logs/                        # Application logs (generated)
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── start.sh                     # Linux/macOS startup script
├── start.bat                    # Windows startup script
└── README.md                    # Documentation
```

## 🚀 Quick Start Guide

### 1. **Clone/Setup**
```bash
cd cegid_y2_mcp
cp config/.env.example config/.env
```

### 2. **Edit Configuration**
```bash
# Update with your Cegid credentials
nano config/.env
# Or on Windows:
notepad config\.env
```

### 3. **Start Server (Option A - Docker)**
```bash
docker-compose -f docker/docker-compose.yml up -d
curl http://localhost:8000/health
```

### 4. **Start Server (Option B - Local)**
```bash
# Linux/macOS
chmod +x start.sh
./start.sh

# Windows
start.bat
```

### 5. **Test API**
```bash
# List resources
curl http://localhost:8000/resources

# List tools
curl http://localhost:8000/tools

# Call tool
curl -X POST http://localhost:8000/tools/list_invoices \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}'
```

## 🔑 Environment Variables (config/.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `CEGID_API_KEY` | Your Cegid API key | `abc123xyz789` |
| `CEGID_CLIENT_ID` | Cegid OAuth client ID | `client_id` |
| `CEGID_CLIENT_SECRET` | Cegid OAuth secret | `secret_key` |
| `JWT_SECRET_KEY` | Secret for JWT tokens | `super-secret-key` |
| `DEFAULT_API_KEY` | API key for auth | `api_key_123` |
| `REDIS_HOST` | Redis server host | `localhost` |
| `REDIS_PASSWORD` | Redis password | `password` |

## 📊 API Endpoints

### Core Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/capabilities` | Server capabilities |
| GET | `/resources` | List all resources |
| POST | `/mcp/request` | Process MCP request |
| GET | `/metrics` | Server metrics |

### Resource Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/resources` | List resources |
| GET | `/resources/{type}/{id}` | Read resource |

### Tool Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tools` | List tools |
| POST | `/tools/{tool_name}` | Call tool |

### Prompt Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prompts` | List prompts |
| GET | `/prompts/{prompt_name}` | Get prompt |

## 🛠️ Available Tools

- `list_invoices` - List invoices
- `get_invoice_details` - Get invoice by ID
- `create_invoice` - Create new invoice
- `update_invoice` - Update invoice
- `delete_invoice` - Delete invoice
- `list_customers` - List customers
- `get_customer_details` - Get customer by ID
- `create_customer` - Create customer
- `update_customer` - Update customer
- `list_products` - List products
- `get_product_details` - Get product by ID
- `list_orders` - List orders
- `get_order_details` - Get order by ID
- `get_financial_summary` - Get financial summary
- `validate_qr_code` - Validate QR code

## 📚 Available Resources

- `cegid://invoices` - List invoices
- `cegid://invoices/{id}` - Invoice details
- `cegid://customers` - List customers
- `cegid://customers/{id}` - Customer details
- `cegid://products` - List products
- `cegid://products/{id}` - Product details
- `cegid://orders` - List orders
- `cegid://orders/{id}` - Order details
- `cegid://financial/{period}` - Financial summary
- `cegid://dashboard` - Dashboard data

## 🤖 Available Prompts

- `analyze_invoice` - Analyze invoice
- `customer_report` - Generate customer report
- `financial_analysis` - Analyze financials
- `fraud_detection` - Detect fraud
- `compliance_check` - Check compliance

## 🔐 Authentication

**API Key** (Recommended for testing)
```bash
curl -H "X-API-Key: your_api_key" http://localhost:8000/tools/list_invoices
```

**JWT Token**
```bash
# Token will be generated with API calls
curl -H "Authorization: Bearer token" http://localhost:8000/tools/list_invoices
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Stop services
docker-compose -f docker/docker-compose.yml down

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Restart service
docker-compose -f docker/docker-compose.yml restart mcp-server

# Execute command in container
docker-compose exec mcp-server python src/mcp_server.py
```

## 📝 Log Files

- **Console**: Displayed in terminal/Docker logs
- **File**: `logs/mcp_server.log` (if configured)
- **Docker**: `docker-compose logs -f mcp-server`

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src

# Run specific test
pytest tests/test_tools.py::test_list_invoices -v
```

## 🔄 Performance Tips

1. **Enable Redis** for caching
2. **Increase TTL** for stable data
3. **Adjust rate limits** based on load
4. **Use batch operations** for multiple items
5. **Monitor metrics** endpoint
6. **Check logs** for errors

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `docker-compose up -d -p 8001:8000` |
| Redis connection error | Check Redis is running, falls back to memory |
| API key rejected | Verify key in .env matches Cegid |
| Slow response | Enable Redis caching, check API health |
| Docker build fails | Update Docker, check dependencies |

## 📞 Support

- **Documentation**: Read README.md
- **Logs**: Check `logs/mcp_server.log`
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## 🔄 Workflow Example

```
Client Request
    ↓
Authentication Check
    ↓
Rate Limiting Check
    ↓
Input Validation
    ↓
Cache Check
    ↓
API Call (if needed)
    ↓
Response Caching
    ↓
Return Response
```

## 📈 Monitoring

```bash
# Health check
curl http://localhost:8000/health

# Server capabilities
curl http://localhost:8000/capabilities

# Metrics
curl http://localhost:8000/metrics

# Logs
docker-compose logs -f mcp-server
```

## 🎯 Next Steps

1. ✅ Configure credentials in `.env`
2. ✅ Start server (Docker or local)
3. ✅ Test with `curl` or Postman
4. ✅ Integrate with your application
5. ✅ Monitor logs and metrics
6. ✅ Scale with Docker Compose

## 📚 Additional Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- MCP Specification: https://modelcontextprotocol.io/
- Cegid Y2 API: https://cegid.com/api-docs/
- Docker: https://docs.docker.com/
- Redis: https://redis.io/documentation

---

**Version**: 1.0.0  
**Last Updated**: January 14, 2026  
**Built with ❤️ by TIMSOFT Société**
