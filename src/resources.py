#!/usr/bin/env python3
"""
MCP Resources - Defines read-only resources for Cegid Y2 data
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Resource:
    """MCP Resource definition"""
    uri: str
    name: str
    description: str
    mimeType: str = "application/json"


class ResourceManager:
    """Manage MCP resources"""
    
    def __init__(self, api_client, cache_manager=None):
        """Initialize resource manager"""
        self.api_client = api_client
        self.cache_manager = cache_manager
        
        # Define available resources
        self.resources = [
            Resource(
                uri="cegid://invoices/{id}",
                name="Invoice",
                description="Get invoice details by ID"
            ),
            Resource(
                uri="cegid://invoices",
                name="Invoices List",
                description="List all invoices"
            ),
            Resource(
                uri="cegid://customers/{id}",
                name="Customer",
                description="Get customer details by ID"
            ),
            Resource(
                uri="cegid://customers",
                name="Customers List",
                description="List all customers"
            ),
            Resource(
                uri="cegid://products/{id}",
                name="Product",
                description="Get product details by ID"
            ),
            Resource(
                uri="cegid://products",
                name="Products List",
                description="List all products"
            ),
            Resource(
                uri="cegid://orders/{id}",
                name="Order",
                description="Get order details by ID"
            ),
            Resource(
                uri="cegid://orders",
                name="Orders List",
                description="List all orders"
            ),
            Resource(
                uri="cegid://financial/{period}",
                name="Financial Summary",
                description="Get financial summary for period (YYYY-MM)"
            ),
            Resource(
                uri="cegid://dashboard",
                name="Dashboard",
                description="Get dashboard data with key metrics"
            ),
        ]
    
    def list_resources(self) -> List[Resource]:
        """List all available resources"""
        return self.resources
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read resource by URI"""
        
        # Parse URI
        parts = uri.replace("cegid://", "").split("/")
        resource_type = parts[0]
        resource_id = parts[1] if len(parts) > 1 else None
        
        try:
            if resource_type == "invoices":
                if resource_id:
                    return await self.api_client.get_invoice(resource_id)
                else:
                    result = await self.api_client.list_invoices(limit=50)
                    return result
            
            elif resource_type == "customers":
                if resource_id:
                    return await self.api_client.get_customer(resource_id)
                else:
                    result = await self.api_client.list_customers(limit=50)
                    return result
            
            elif resource_type == "products":
                if resource_id:
                    return await self.api_client.get_product(resource_id)
                else:
                    result = await self.api_client.list_products(limit=50)
                    return result
            
            elif resource_type == "orders":
                if resource_id:
                    return await self.api_client.get_order(resource_id)
                else:
                    result = await self.api_client.list_orders(limit=50)
                    return result
            
            elif resource_type == "financial":
                period = resource_id or "2025-01"
                return await self.api_client.get_financial_summary(period)
            
            elif resource_type == "dashboard":
                return await self._get_dashboard_data()
            
            else:
                raise ValueError(f"Unknown resource type: {resource_type}")
        
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            return {"error": str(e), "uri": uri}
    
    async def _get_dashboard_data(self) -> Dict[str, Any]:
        """Get aggregated dashboard data"""
        try:
            # Fetch data in parallel
            invoices = await self.api_client.list_invoices(limit=10)
            customers = await self.api_client.list_customers(limit=10)
            products = await self.api_client.list_products(limit=10)
            
            return {
                "dashboard": {
                    "invoices_summary": invoices,
                    "customers_summary": customers,
                    "products_summary": products,
                    "timestamp": "2025-01-14T14:00:00Z"
                }
            }
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {"error": str(e)}
