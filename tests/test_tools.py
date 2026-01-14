#!/usr/bin/env python3
"""
Tests for MCP Server Tools
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

# Mock the API client for testing
@pytest.fixture
def mock_api_client():
    """Create mock API client"""
    client = AsyncMock()
    client.list_invoices = AsyncMock(return_value={"invoices": []})
    client.get_invoice = AsyncMock(return_value={"id": "123", "amount": 1000})
    client.list_customers = AsyncMock(return_value={"customers": []})
    client.get_customer = AsyncMock(return_value={"id": "cust_123", "name": "Test"})
    return client


@pytest.mark.asyncio
async def test_list_invoices(mock_api_client):
    """Test list_invoices tool"""
    from src.tools import ToolManager
    
    cache = Mock()
    manager = ToolManager(mock_api_client, cache)
    
    result = await manager._list_invoices(limit=10)
    assert result is not None
    mock_api_client.list_invoices.assert_called_once()


@pytest.mark.asyncio
async def test_get_invoice_details(mock_api_client):
    """Test get_invoice_details tool"""
    from src.tools import ToolManager
    
    cache = Mock()
    manager = ToolManager(mock_api_client, cache)
    
    result = await manager._get_invoice_details("123")
    assert result is not None
    mock_api_client.get_invoice.assert_called_once_with("123")


@pytest.mark.asyncio
async def test_create_invoice(mock_api_client):
    """Test create_invoice tool"""
    from src.tools import ToolManager
    
    cache = Mock()
    manager = ToolManager(mock_api_client, cache)
    
    invoice_data = {
        "customer_id": "cust_123",
        "amount": 1000,
        "currency": "USD"
    }
    result = await manager._create_invoice(**invoice_data)
    mock_api_client.create_invoice.assert_called_once()


@pytest.mark.asyncio
async def test_list_customers(mock_api_client):
    """Test list_customers tool"""
    from src.tools import ToolManager
    
    cache = Mock()
    manager = ToolManager(mock_api_client, cache)
    
    result = await manager._list_customers(limit=10)
    assert result is not None
    mock_api_client.list_customers.assert_called_once()


def test_tool_manager_list_tools(mock_api_client):
    """Test listing tools"""
    from src.tools import ToolManager
    
    cache = Mock()
    manager = ToolManager(mock_api_client, cache)
    
    tools = manager.list_tools()
    assert len(tools) > 0
    assert any(t.name == "list_invoices" for t in tools)
    assert any(t.name == "list_customers" for t in tools)


@pytest.mark.asyncio
async def test_call_tool_success(mock_api_client):
    """Test calling tool successfully"""
    from src.tools import ToolManager
    
    cache = Mock()
    manager = ToolManager(mock_api_client, cache)
    
    result = await manager.call_tool("list_invoices", {"limit": 10})
    assert result["success"] is True
    assert "timestamp" in result


@pytest.mark.asyncio
async def test_call_tool_not_found(mock_api_client):
    """Test calling non-existent tool"""
    from src.tools import ToolManager
    
    cache = Mock()
    manager = ToolManager(mock_api_client, cache)
    
    result = await manager.call_tool("non_existent_tool", {})
    assert result["success"] is False
    assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
