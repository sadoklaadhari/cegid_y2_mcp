# Cegid Y2 MCP Server

**Model Context Protocol Server for Cegid Y2 ERP Integration**

Version: 1.0.0  
Author: TIMSOFT Société  
License: MIT

## 📋 Overview

A production-ready Model Context Protocol (MCP) server that provides seamless integration with Cegid Y2 ERP system. This server exposes Cegid Y2 data through MCP resources, tools, and prompts, enabling AI models and applications to interact with ERP data securely.

### Key Features

✅ **Full MCP 1.0 Compliance**
- Resources (read-only data access)
- Tools (actionable operations)
- Prompts (AI-optimized templates)

✅ **Cegid Y2 Integration**
- All major API endpoints
- Invoices, Customers, Products, Orders, Financial data
- QR code validation
- Batch operations

✅ **Enterprise Security**
- OAuth2, API Key, JWT authentication
- Rate limiting
- CORS configuration
- Input sanitization

✅ **High Performance**
- Redis caching with configurable TTL
- Connection pooling
- Async/await architecture
- In-memory fallback

✅ **Production Ready**
- Docker & Docker Compose
- Comprehensive logging
- Health checks
- Monitoring endpoints

✅ **Developer Friendly**
- FastAPI documentation
- Multiple authentication options
- Extensive examples
- Unit tests

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (recommended)
- Redis (optional, for caching)
- PostgreSQL (optional, for data storage)

### Option 1: Docker (Recommended)

```bash
# Clone repository
cd cegid_y2_mcp

# Copy environment file
cp config/.env.example config/.env

# Edit .env with your credentials
nano config/.env

# Start services
docker-compose -f docker/docker-compose.yml up -d

# Check logs
docker-compose logs -f mcp-server

# Test API
curl http://localhost:8000/health
```

### Option 2: Local Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export CEGID_API_KEY="your_key_here"
export JWT_SECRET_KEY="your_secret_here"

# Run server
python src/mcp_server.py

# Access at http://localhost:8000
```

## 📚 API Documentation

### Health Check

```bash
curl http://localhost:8000/health
```

### List Resources

```bash
curl http://localhost:8000/resources
```

### Read Resource

```bash
curl http://localhost:8000/resources/invoices/INV-001
```

### List Tools

```bash
curl http://localhost:8000/tools
```

### Call Tool

```bash
curl -X POST http://localhost:8000/tools/list_invoices \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "offset": 0}'
```

### Get Prompts

```bash
curl http://localhost:8000/prompts
```

## 🔧 Configuration

### config.json

Main configuration file with:
- Server settings
- Cegid API credentials
- Authentication options
- Redis configuration
- Rate limiting
- CORS settings
- Logging

### .env File

Environment variables override config.json:
- `CEGID_API_KEY` - Your Cegid API key
- `JWT_SECRET_KEY` - Secret for JWT signing
- `REDIS_HOST` - Redis server host
- `DEFAULT_API_KEY` - Default API key for authentication

## 🛠️ Available Resources

### Invoices
- `cegid://invoices` - List all invoices
- `cegid://invoices/{id}` - Get invoice details

### Customers
- `cegid://customers` - List all customers
- `cegid://customers/{id}` - Get customer details

### Products
- `cegid://products` - List all products
- `cegid://products/{id}` - Get product details

### Orders
- `cegid://orders` - List all orders
- `cegid://orders/{id}` - Get order details

### Financial
- `cegid://financial/{period}` - Get financial summary
- `cegid://dashboard` - Get dashboard data

## 🛠️ Available Tools

### Invoice Operations
- `list_invoices` - List invoices with filters
- `get_invoice_details` - Get invoice by ID
- `create_invoice` - Create new invoice
- `update_invoice` - Update existing invoice
- `delete_invoice` - Delete invoice
- `search_invoices` - Search invoices by keyword
- `batch_get_invoices` - Get multiple invoices

### Customer Operations
- `list_customers` - List customers
- `get_customer_details` - Get customer by ID
- `create_customer` - Create new customer
- `update_customer` - Update customer

### Product Operations
- `list_products` - List products
- `get_product_details` - Get product by ID

### Order Operations
- `list_orders` - List orders
- `get_order_details` - Get order by ID

### Financial Operations
- `get_financial_summary` - Get financial summary
- `validate_qr_code` - Validate QR code

## 🤖 Available Prompts

### Analyze Invoice
Analyze invoice for anomalies and generate summary

```bash
curl http://localhost:8000/prompts/analyze_invoice \
  -d '{"invoice_id": "INV-001"}'
```

### Customer Report
Generate comprehensive customer report

```bash
curl http://localhost:8000/prompts/customer_report \
  -d '{"customer_id": "CUST-001", "period": "2025-01"}'
```

### Financial Analysis
Analyze financial data and trends

```bash
curl http://localhost:8000/prompts/financial_analysis \
  -d '{"period": "2025-01"}'
```

### Fraud Detection
Analyze transactions for fraud patterns

```bash
curl http://localhost:8000/prompts/fraud_detection \
  -d '{"threshold": 50}'
```

## 🔐 Authentication

### API Key Authentication

```bash
curl http://localhost:8000/tools/list_invoices \
  -H "X-API-Key: your_api_key_here"
```

### JWT Token Authentication

```bash
# Generate token (internal endpoint)
TOKEN=$(curl -X POST http://localhost:8000/auth/token \
  -d '{"user_id": "user123"}')

# Use token
curl http://localhost:8000/tools/list_invoices \
  -H "Authorization: Bearer $TOKEN"
```

### OAuth2 (Optional)

Configure OAuth2 in .env file for Cegid provider authentication.

## 📊 Monitoring & Metrics

### Health Check
```bash
curl http://localhost:8000/health
```

### Server Capabilities
```bash
curl http://localhost:8000/capabilities
```

### Metrics
```bash
curl http://localhost:8000/metrics
```

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 🐳 Docker Deployment

### Start Services

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### Stop Services

```bash
docker-compose -f docker/docker-compose.yml down
```

### View Logs

```bash
docker-compose -f docker/docker-compose.yml logs -f mcp-server
```

### Services Included

- **mcp-server**: FastAPI application
- **redis**: Caching layer
- **postgres**: Optional database

## 🔄 Integration Examples

### Python Client

```python
import requests

headers = {"X-API-Key": "your_api_key"}

# List invoices
response = requests.get(
    "http://localhost:8000/resources/invoices",
    headers=headers
)

invoices = response.json()
```

### curl Commands

```bash
# List invoices
curl -H "X-API-Key: your_key" \
  http://localhost:8000/resources/invoices

# Create invoice
curl -X POST http://localhost:8000/tools/create_invoice \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_key" \
  -d '{
    "customer_id": "CUST-001",
    "amount": 1000,
    "currency": "USD"
  }'
```

### JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

const headers = {
  'X-API-Key': 'your_api_key',
  'Content-Type': 'application/json'
};

// List invoices
const response = await fetch('http://localhost:8000/resources/invoices', {
  headers
});

const invoices = await response.json();
```

## 🐛 Troubleshooting

### Redis Connection Error
- Verify Redis is running: `redis-cli ping`
- Check Redis host/port in config
- Falls back to in-memory cache automatically

### Cegid API Error
- Verify API key is correct
- Check API URL is accessible
- Ensure API key has required permissions

### Port Already in Use
```bash
# Change port in config.json or via environment
docker-compose -f docker/docker-compose.yml up -d -p 8001:8000
```

### Permission Denied
```bash
# Fix file permissions
chmod -R 755 .
chmod 600 config/.env
```

## 📈 Performance Tuning

### Enable Redis Caching
```json
{
  "redis": {
    "enabled": true,
    "default_ttl": 300
  }
}
```

### Adjust Rate Limits
```json
{
  "rate_limit": {
    "requests_per_minute": 2000,
    "requests_per_hour": 100000
  }
}
```

### Increase Workers
```bash
# In docker-compose.yml or when running locally
export WORKERS=8
```

## 📚 Architecture

```
┌─────────────────┐
│   AI/Client     │
└────────┬────────┘
         │
    ┌────▼─────────────────┐
    │   FastAPI MCP Server  │
    │  ┌──────────────────┐ │
    │  │ Resources        │ │
    │  │ Tools            │ │
    │  │ Prompts          │ │
    │  │ Authentication   │ │
    │  └──────────────────┘ │
    └────┬────────┬────────┘
         │        │
    ┌────▼──┐  ┌──▼────┐
    │ Redis │  │Cegid  │
    │ Cache │  │ API   │
    └───────┘  └───────┘
```

## 🔄 Workflow Example

1. Client authenticates with API key
2. Client calls `list_invoices` tool
3. Server checks Redis cache
4. If not cached, queries Cegid API
5. Server caches result with TTL
6. Returns response to client
7. On next request, serves from cache
8. Cache invalidates after TTL expires

## 📝 Logging

Logs are written to:
- Console (stdout)
- File: `logs/mcp_server.log`

Configure in config.json:
```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/mcp_server.log",
    "max_bytes": 10485760,
    "backup_count": 10
  }
}
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Add tests
4. Submit pull request

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

- Documentation: See README.md and inline code comments
- Issues: Create GitHub issue with detailed description
- Email: support@timsoft.com

## 🚀 Next Steps

1. **Configure Credentials**: Edit `config/.env` with your Cegid credentials
2. **Start Server**: Run Docker Compose or Python server
3. **Test API**: Use curl or Postman
4. **Integrate Client**: Use provided SDKs or API
5. **Monitor**: Check logs and metrics

## 🎯 Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Webhook notifications
- [ ] Advanced reporting tools
- [ ] Machine learning models for fraud detection
- [ ] Multi-tenant support
- [ ] GraphQL endpoint

---

**Built with ❤️ by TIMSOFT Société**

Last Updated: January 14, 2026
