#!/usr/bin/env python3
"""
MCP Tools - Defines callable tools for Cegid Y2 operations
"""

import logging
import json
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """MCP Tool definition"""
    name: str
    description: str
    inputSchema: Dict[str, Any]


class ToolManager:
    """Manage MCP tools"""
    
    def __init__(self, api_client, cache_manager=None):
        """Initialize tool manager"""
        self.api_client = api_client
        self.cache_manager = cache_manager
        
        # Register tools
        self.tools: Dict[str, Callable] = {
            "list_invoices": self._list_invoices,
            "get_invoice_details": self._get_invoice_details,
            "create_invoice": self._create_invoice,
            "update_invoice": self._update_invoice,
            "delete_invoice": self._delete_invoice,
            "list_customers": self._list_customers,
            "get_customer_details": self._get_customer_details,
            "create_customer": self._create_customer,
            "update_customer": self._update_customer,
            "list_products": self._list_products,
            "get_product_details": self._get_product_details,
            "list_orders": self._list_orders,
            "get_order_details": self._get_order_details,
            "get_financial_summary": self._get_financial_summary,
            "validate_qr_code": self._validate_qr_code,
            "search_invoices": self._search_invoices,
            "batch_get_invoices": self._batch_get_invoices,
        }
        
        self.tool_schemas = self._build_schemas()
    
    def _build_schemas(self) -> Dict[str, Tool]:
        """Build tool definitions"""
        return {
            "list_invoices": Tool(
                name="list_invoices",
                description="List invoices with optional filters",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters (customer_id, status, date_range)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of results (default: 100)",
                            "default": 100
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Offset for pagination (default: 0)",
                            "default": 0
                        }
                    }
                }
            ),
            "get_invoice_details": Tool(
                name="get_invoice_details",
                description="Get detailed information about a specific invoice",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "Invoice ID"
                        }
                    },
                    "required": ["invoice_id"]
                }
            ),
            "create_invoice": Tool(
                name="create_invoice",
                description="Create a new invoice",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "string"},
                        "amount": {"type": "number"},
                        "currency": {"type": "string"},
                        "due_date": {"type": "string"},
                        "items": {"type": "array"},
                        "notes": {"type": "string"}
                    },
                    "required": ["customer_id", "amount"]
                }
            ),
            "update_invoice": Tool(
                name="update_invoice",
                description="Update an existing invoice",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string"},
                        "data": {
                            "type": "object",
                            "description": "Fields to update"
                        }
                    },
                    "required": ["invoice_id", "data"]
                }
            ),
            "delete_invoice": Tool(
                name="delete_invoice",
                description="Delete an invoice",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string"}
                    },
                    "required": ["invoice_id"]
                }
            ),
            "list_customers": Tool(
                name="list_customers",
                description="List customers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filters": {"type": "object"},
                        "limit": {"type": "integer", "default": 100},
                        "offset": {"type": "integer", "default": 0}
                    }
                }
            ),
            "get_customer_details": Tool(
                name="get_customer_details",
                description="Get customer details",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "string"}
                    },
                    "required": ["customer_id"]
                }
            ),
            "create_customer": Tool(
                name="create_customer",
                description="Create new customer",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "phone": {"type": "string"},
                        "address": {"type": "string"}
                    },
                    "required": ["name", "email"]
                }
            ),
            "update_customer": Tool(
                name="update_customer",
                description="Update customer",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "string"},
                        "data": {"type": "object"}
                    },
                    "required": ["customer_id", "data"]
                }
            ),
            "list_products": Tool(
                name="list_products",
                description="List products",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "limit": {"type": "integer", "default": 100},
                        "offset": {"type": "integer", "default": 0}
                    }
                }
            ),
            "get_product_details": Tool(
                name="get_product_details",
                description="Get product details",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string"}
                    },
                    "required": ["product_id"]
                }
            ),
            "list_orders": Tool(
                name="list_orders",
                description="List orders",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filters": {"type": "object"},
                        "limit": {"type": "integer", "default": 100},
                        "offset": {"type": "integer", "default": 0}
                    }
                }
            ),
            "get_order_details": Tool(
                name="get_order_details",
                description="Get order details",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"}
                    },
                    "required": ["order_id"]
                }
            ),
            "get_financial_summary": Tool(
                name="get_financial_summary",
                description="Get financial summary",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "period": {
                            "type": "string",
                            "description": "Period (YYYY-MM)"
                        }
                    },
                    "required": ["period"]
                }
            ),
            "validate_qr_code": Tool(
                name="validate_qr_code",
                description="Validate QR code and retrieve associated data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "qr_hex": {"type": "string"}
                    },
                    "required": ["qr_hex"]
                }
            ),
            "search_invoices": Tool(
                name="search_invoices",
                description="Search invoices by keyword",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "limit": {"type": "integer", "default": 50}
                    },
                    "required": ["query"]
                }
            ),
            "batch_get_invoices": Tool(
                name="batch_get_invoices",
                description="Get multiple invoices in one request",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "invoice_ids": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["invoice_ids"]
                }
            ),
        }
    
    def list_tools(self) -> List[Tool]:
        """List all available tools"""
        return list(self.tool_schemas.values())
    
    async def call_tool(self, name: str, arguments: Dict) -> Dict[str, Any]:
        """Call a tool"""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        
        try:
            tool_func = self.tools[name]
            result = await tool_func(**arguments)
            return {
                "success": True,
                "tool": name,
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return {
                "success": False,
                "tool": name,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    # Tool Implementations
    
    async def _list_invoices(self, filters: Optional[Dict] = None, limit: int = 100, offset: int = 0) -> Dict:
        """List invoices"""
        return await self.api_client.list_invoices(filters, limit, offset)
    
    async def _get_invoice_details(self, invoice_id: str) -> Dict:
        """Get invoice details"""
        return await self.api_client.get_invoice(invoice_id)
    
    async def _create_invoice(self, **kwargs) -> Dict:
        """Create invoice"""
        return await self.api_client.create_invoice(kwargs)
    
    async def _update_invoice(self, invoice_id: str, data: Dict) -> Dict:
        """Update invoice"""
        return await self.api_client.update_invoice(invoice_id, data)
    
    async def _delete_invoice(self, invoice_id: str) -> Dict:
        """Delete invoice"""
        return await self.api_client.delete_invoice(invoice_id)
    
    async def _list_customers(self, filters: Optional[Dict] = None, limit: int = 100, offset: int = 0) -> Dict:
        """List customers"""
        return await self.api_client.list_customers(filters, limit, offset)
    
    async def _get_customer_details(self, customer_id: str) -> Dict:
        """Get customer details"""
        return await self.api_client.get_customer(customer_id)
    
    async def _create_customer(self, **kwargs) -> Dict:
        """Create customer"""
        return await self.api_client.create_customer(kwargs)
    
    async def _update_customer(self, customer_id: str, data: Dict) -> Dict:
        """Update customer"""
        return await self.api_client.update_customer(customer_id, data)
    
    async def _list_products(self, category: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict:
        """List products"""
        return await self.api_client.list_products(category, limit, offset)
    
    async def _get_product_details(self, product_id: str) -> Dict:
        """Get product details"""
        return await self.api_client.get_product(product_id)
    
    async def _list_orders(self, filters: Optional[Dict] = None, limit: int = 100, offset: int = 0) -> Dict:
        """List orders"""
        return await self.api_client.list_orders(filters, limit, offset)
    
    async def _get_order_details(self, order_id: str) -> Dict:
        """Get order details"""
        return await self.api_client.get_order(order_id)
    
    async def _get_financial_summary(self, period: str) -> Dict:
        """Get financial summary"""
        return await self.api_client.get_financial_summary(period)
    
    async def _validate_qr_code(self, qr_hex: str) -> Dict:
        """Validate QR code"""
        return await self.api_client.validate_qr_code(qr_hex)
    
    async def _search_invoices(self, query: str, limit: int = 50) -> Dict:
        """Search invoices"""
        filters = {"search": query}
        return await self.api_client.list_invoices(filters, limit)
    
    async def _batch_get_invoices(self, invoice_ids: List[str]) -> Dict:
        """Batch get invoices"""
        return await self.api_client.batch_get_invoices(invoice_ids)
