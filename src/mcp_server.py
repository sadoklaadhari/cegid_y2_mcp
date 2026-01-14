#!/usr/bin/env python3
"""
Cegid Y2 MCP Server - Main server implementation
Implements Model Context Protocol 1.0 for Cegid Y2 ERP integration
"""

import json
import logging
import asyncio
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from api_client import CegidAPIClient
from auth import AuthManager
from cache import CacheManager
from resources import ResourceManager
from tools import ToolManager
from prompts import PromptManager
from utils import sanitize_input, setup_logging

# Configure logging
logger = setup_logging(__name__)

# FastAPI app
app = FastAPI(
    title="Cegid Y2 MCP Server",
    description="Model Context Protocol server for Cegid Y2 ERP",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@dataclass
class MCPRequest:
    """MCP Request structure"""
    method: str
    params: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None


@dataclass
class MCPResponse:
    """MCP Response structure"""
    result: Any = None
    error: Optional[str] = None
    id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


class CegidMCPServer:
    """Main MCP Server implementation"""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize MCP server"""
        self.config = self._load_config(config_path)
        self.auth_manager = AuthManager(self.config)
        self.cache_manager = CacheManager(self.config.get("redis", {}))
        self.api_client = CegidAPIClient(self.config, self.cache_manager)
        self.resource_manager = ResourceManager(self.api_client, self.cache_manager)
        self.tool_manager = ToolManager(self.api_client, self.cache_manager)
        self.prompt_manager = PromptManager()
        
        logger.info("✓ Cegid Y2 MCP Server initialized")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in config file: {config_path}")
            raise
    
    async def handle_list_resources(self, params: Dict) -> Dict:
        """Handle MCP listResources request"""
        resources = self.resource_manager.list_resources()
        return {
            "resources": [asdict(r) for r in resources]
        }
    
    async def handle_read_resource(self, params: Dict) -> Dict:
        """Handle MCP readResource request"""
        uri = params.get("uri")
        if not uri:
            raise ValueError("URI parameter required")
        
        content = await self.resource_manager.read_resource(uri)
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps(content)
                }
            ]
        }
    
    async def handle_list_tools(self, params: Dict) -> Dict:
        """Handle MCP listTools request"""
        tools = self.tool_manager.list_tools()
        return {
            "tools": [asdict(t) for t in tools]
        }
    
    async def handle_call_tool(self, params: Dict) -> Dict:
        """Handle MCP callTool request"""
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not name:
            raise ValueError("Tool name required")
        
        # Sanitize inputs
        arguments = {k: sanitize_input(v) for k, v in arguments.items()}
        
        result = await self.tool_manager.call_tool(name, arguments)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result)
                }
            ]
        }
    
    async def handle_list_prompts(self, params: Dict) -> Dict:
        """Handle MCP listPrompts request"""
        prompts = self.prompt_manager.list_prompts()
        return {
            "prompts": [asdict(p) for p in prompts]
        }
    
    async def handle_get_prompt(self, params: Dict) -> Dict:
        """Handle MCP getPrompt request"""
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not name:
            raise ValueError("Prompt name required")
        
        prompt = await self.prompt_manager.get_prompt(name, arguments)
        return {
            "messages": prompt["messages"]
        }
    
    async def process_request(self, request: MCPRequest) -> MCPResponse:
        """Process incoming MCP request"""
        try:
            method = request.method
            params = request.params
            
            logger.debug(f"Processing MCP request: {method}")
            
            # Route to handler
            if method == "initialize":
                result = self._handle_initialize()
            elif method == "listResources":
                result = await self.handle_list_resources(params)
            elif method == "readResource":
                result = await self.handle_read_resource(params)
            elif method == "listTools":
                result = await self.handle_list_tools(params)
            elif method == "callTool":
                result = await self.handle_call_tool(params)
            elif method == "listPrompts":
                result = await self.handle_list_prompts(params)
            elif method == "getPrompt":
                result = await self.handle_get_prompt(params)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            return MCPResponse(result=result, id=request.id)
        
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return MCPResponse(error=str(e), id=request.id)
    
    def _handle_initialize(self) -> Dict:
        """Handle initialization request"""
        return {
            "protocolVersion": "1.0",
            "capabilities": {
                "resources": True,
                "tools": True,
                "prompts": True
            },
            "serverInfo": {
                "name": "Cegid Y2 MCP Server",
                "version": "1.0.0"
            }
        }


# Initialize server
mcp_server = None

def get_mcp_server() -> CegidMCPServer:
    """Get or initialize MCP server"""
    global mcp_server
    if mcp_server is None:
        mcp_server = CegidMCPServer()
    return mcp_server


# REST API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Cegid Y2 MCP Server"
    }


@app.get("/capabilities")
async def get_capabilities(server: CegidMCPServer = Depends(get_mcp_server)):
    """Get server capabilities"""
    return {
        "resources": server.resource_manager.list_resources(),
        "tools": server.tool_manager.list_tools(),
        "prompts": server.prompt_manager.list_prompts(),
        "authentication": "OAuth2, API Key, JWT",
        "caching": "Redis with TTL",
        "rateLimit": "1000 req/min"
    }


@app.post("/mcp/request")
async def mcp_request(
    request_data: Dict,
    server: CegidMCPServer = Depends(get_mcp_server)
):
    """Handle MCP protocol requests"""
    try:
        request = MCPRequest(
            method=request_data.get("method"),
            params=request_data.get("params", {}),
            id=request_data.get("id")
        )
        
        response = await server.process_request(request)
        return response.to_dict()
    
    except Exception as e:
        logger.error(f"MCP request error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/resources")
async def list_resources(server: CegidMCPServer = Depends(get_mcp_server)):
    """List all available resources"""
    result = await server.handle_list_resources({})
    return result


@app.get("/resources/{resource_type}/{resource_id}")
async def read_resource(
    resource_type: str,
    resource_id: str,
    server: CegidMCPServer = Depends(get_mcp_server)
):
    """Read specific resource"""
    uri = f"cegid://{resource_type}/{resource_id}"
    result = await server.handle_read_resource({"uri": uri})
    return result


@app.get("/tools")
async def list_tools(server: CegidMCPServer = Depends(get_mcp_server)):
    """List all available tools"""
    result = await server.handle_list_tools({})
    return result


@app.post("/tools/{tool_name}")
async def call_tool(
    tool_name: str,
    arguments: Dict,
    server: CegidMCPServer = Depends(get_mcp_server)
):
    """Call a tool with arguments"""
    result = await server.handle_call_tool({
        "name": tool_name,
        "arguments": arguments
    })
    return result


@app.get("/prompts")
async def list_prompts(server: CegidMCPServer = Depends(get_mcp_server)):
    """List all available prompts"""
    result = await server.handle_list_prompts({})
    return result


@app.get("/prompts/{prompt_name}")
async def get_prompt(
    prompt_name: str,
    server: CegidMCPServer = Depends(get_mcp_server)
):
    """Get a specific prompt"""
    result = await server.handle_get_prompt({"name": prompt_name})
    return result


@app.get("/metrics")
async def get_metrics(server: CegidMCPServer = Depends(get_mcp_server)):
    """Get server metrics"""
    return {
        "cache": server.cache_manager.get_stats(),
        "timestamp": datetime.utcnow().isoformat()
    }


def main():
    """Run the server"""
    logger.info("Starting Cegid Y2 MCP Server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )


if __name__ == "__main__":
    main()
