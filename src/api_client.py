#!/usr/bin/env python3
"""
Cegid Y2 API Client - Handles all API communications
"""

import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CegidAPIClient:
    """Client for Cegid Y2 REST API"""
    
    def __init__(self, config: Dict, cache_manager=None):
        """Initialize API client"""
        self.config = config
        self.cache_manager = cache_manager
        
        # API Configuration
        self.base_url = config.get("cegid", {}).get("base_url", "https://api.cegid.com/y2")
        self.api_key = config.get("cegid", {}).get("api_key", "")
        self.api_version = config.get("cegid", {}).get("api_version", "v1")
        
        self.session: Optional[aiohttp.ClientSession] = None
        
        logger.info(f"Cegid API Client initialized with base URL: {self.base_url}")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close API session"""
        if self.session:
            await self.session.close()
    
    def _get_headers(self, token: Optional[str] = None) -> Dict:
        """Get request headers"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Cegid-Y2-MCP-Client/1.0"
        }
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key
        
        return headers
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        token: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict:
        """Make HTTP request to Cegid API"""
        
        url = f"{self.base_url}/{self.api_version}/{endpoint}"
        
        # Check cache first
        if use_cache and self.cache_manager:
            cache_key = f"cegid:{method}:{endpoint}:{str(params)}"
            cached = self.cache_manager.get(cache_key)
            if cached:
                logger.debug(f"Cache hit: {endpoint}")
                return cached
        
        try:
            session = await self._get_session()
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=self._get_headers(token),
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    # Cache successful responses
                    if use_cache and self.cache_manager and method == "GET":
                        cache_key = f"cegid:{method}:{endpoint}:{str(params)}"
                        self.cache_manager.set(cache_key, result, ttl=300)
                    
                    return result
                
                elif response.status == 401:
                    raise Exception("Unauthorized: Check API credentials")
                elif response.status == 404:
                    return None
                else:
                    error = await response.text()
                    raise Exception(f"API Error {response.status}: {error}")
        
        except Exception as e:
            logger.error(f"API request error: {e}")
            raise
    
    # Invoice Operations
    
    async def list_invoices(
        self,
        filters: Optional[Dict] = None,
        limit: int = 100,
        offset: int = 0,
        token: Optional[str] = None
    ) -> Dict:
        """List invoices with optional filters"""
        params = {
            "limit": limit,
            "offset": offset,
            **(filters or {})
        }
        return await self._make_request("GET", "invoices", params=params, token=token)
    
    async def get_invoice(self, invoice_id: str, token: Optional[str] = None) -> Dict:
        """Get invoice details"""
        return await self._make_request("GET", f"invoices/{invoice_id}", token=token)
    
    async def create_invoice(self, invoice_data: Dict, token: Optional[str] = None) -> Dict:
        """Create new invoice"""
        return await self._make_request(
            "POST",
            "invoices",
            data=invoice_data,
            token=token,
            use_cache=False
        )
    
    async def update_invoice(
        self,
        invoice_id: str,
        update_data: Dict,
        token: Optional[str] = None
    ) -> Dict:
        """Update existing invoice"""
        return await self._make_request(
            "PUT",
            f"invoices/{invoice_id}",
            data=update_data,
            token=token,
            use_cache=False
        )
    
    async def delete_invoice(self, invoice_id: str, token: Optional[str] = None) -> Dict:
        """Delete invoice"""
        return await self._make_request(
            "DELETE",
            f"invoices/{invoice_id}",
            token=token,
            use_cache=False
        )
    
    # Customer Operations
    
    async def list_customers(
        self,
        filters: Optional[Dict] = None,
        limit: int = 100,
        offset: int = 0,
        token: Optional[str] = None
    ) -> Dict:
        """List customers"""
        params = {
            "limit": limit,
            "offset": offset,
            **(filters or {})
        }
        return await self._make_request("GET", "customers", params=params, token=token)
    
    async def get_customer(self, customer_id: str, token: Optional[str] = None) -> Dict:
        """Get customer details"""
        return await self._make_request("GET", f"customers/{customer_id}", token=token)
    
    async def create_customer(self, customer_data: Dict, token: Optional[str] = None) -> Dict:
        """Create new customer"""
        return await self._make_request(
            "POST",
            "customers",
            data=customer_data,
            token=token,
            use_cache=False
        )
    
    async def update_customer(
        self,
        customer_id: str,
        update_data: Dict,
        token: Optional[str] = None
    ) -> Dict:
        """Update customer"""
        return await self._make_request(
            "PUT",
            f"customers/{customer_id}",
            data=update_data,
            token=token,
            use_cache=False
        )
    
    # Product Operations
    
    async def list_products(
        self,
        category: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        token: Optional[str] = None
    ) -> Dict:
        """List products"""
        params = {
            "limit": limit,
            "offset": offset
        }
        if category:
            params["category"] = category
        
        return await self._make_request("GET", "products", params=params, token=token)
    
    async def get_product(self, product_id: str, token: Optional[str] = None) -> Dict:
        """Get product details"""
        return await self._make_request("GET", f"products/{product_id}", token=token)
    
    # Order Operations
    
    async def list_orders(
        self,
        filters: Optional[Dict] = None,
        limit: int = 100,
        offset: int = 0,
        token: Optional[str] = None
    ) -> Dict:
        """List orders"""
        params = {
            "limit": limit,
            "offset": offset,
            **(filters or {})
        }
        return await self._make_request("GET", "orders", params=params, token=token)
    
    async def get_order(self, order_id: str, token: Optional[str] = None) -> Dict:
        """Get order details"""
        return await self._make_request("GET", f"orders/{order_id}", token=token)
    
    # Financial Operations
    
    async def get_financial_summary(
        self,
        period: str,
        token: Optional[str] = None
    ) -> Dict:
        """Get financial summary for period"""
        return await self._make_request(
            "GET",
            f"financial/summary/{period}",
            token=token
        )
    
    async def get_financial_report(
        self,
        report_type: str,
        start_date: str,
        end_date: str,
        token: Optional[str] = None
    ) -> Dict:
        """Get financial report"""
        params = {
            "type": report_type,
            "start_date": start_date,
            "end_date": end_date
        }
        return await self._make_request(
            "GET",
            "financial/reports",
            params=params,
            token=token
        )
    
    # Batch Operations
    
    async def batch_get_invoices(self, invoice_ids: List[str], token: Optional[str] = None) -> Dict:
        """Get multiple invoices in batch"""
        return await self._make_request(
            "POST",
            "invoices/batch",
            data={"ids": invoice_ids},
            token=token,
            use_cache=False
        )
    
    async def batch_get_customers(self, customer_ids: List[str], token: Optional[str] = None) -> Dict:
        """Get multiple customers in batch"""
        return await self._make_request(
            "POST",
            "customers/batch",
            data={"ids": customer_ids},
            token=token,
            use_cache=False
        )
    
    # Validation Operations
    
    async def validate_qr_code(self, qr_hex: str, token: Optional[str] = None) -> Dict:
        """Validate QR code and retrieve associated data"""
        return await self._make_request(
            "POST",
            "qr/validate",
            data={"qr_code": qr_hex},
            token=token,
            use_cache=False
        )
    
    # Health & Status
    
    async def health_check(self) -> Dict:
        """Check API health"""
        try:
            return await self._make_request("GET", "health", use_cache=False)
        except Exception as e:
            return {"status": "error", "message": str(e)}
