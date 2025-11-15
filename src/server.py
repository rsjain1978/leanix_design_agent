#!/usr/bin/env python3
"""
LeanIX Design Agent MCP Server

Exposes intelligent design standards querying as an MCP server via HTTP.
Connects to LeanIX MCP and provides AI-powered query understanding and synthesis.
"""

import os
import logging
from typing import List, Dict, Any
from fastmcp import FastMCP
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("leanix-design-agent")

# Import configuration
from config import openai_config, leanix_config

# Create FastMCP server
mcp = FastMCP("leanix-design-agent")


# ============================================================================
# LeanIX Client
# ============================================================================

def _build_leanix_connection() -> Dict[str, Dict[str, Any]]:
    """Build LeanIX MCP connection configuration."""
    conn: Dict[str, Any] = {"transport": leanix_config.transport}
    if leanix_config.transport in ("streamable_http", "sse"):
        conn["url"] = leanix_config.url
        headers = {}
        if leanix_config.auth_bearer:
            headers["Authorization"] = f"Bearer {leanix_config.auth_bearer}"
        if headers:
            conn["headers"] = headers
    return {leanix_config.server_name: conn}


async def _get_leanix_tools() -> List[BaseTool]:
    """Retrieve tools from LeanIX MCP server."""
    connections = _build_leanix_connection()
    async with MultiServerMCPClient(connections) as client:
        tools = await client.get_tools()
    logger.info(f"Loaded {len(tools)} tools from LeanIX MCP")
    return tools


def _filter_tools(tools: List[BaseTool]) -> List[BaseTool]:
    """Filter LeanIX tools to relevant ones for design standards."""
    if not tools:
        return tools
    keywords = ["search", "find", "get", "overview", "fact", "sheet"]
    filtered = [t for t in tools if any(k in t.name.lower() for k in keywords)]
    return filtered or tools


# ============================================================================
# AI Agent
# ============================================================================

async def _build_agent():
    """Build the AI agent with LeanIX tools."""
    leanix_tools = await _get_leanix_tools()
    design_tools = _filter_tools(leanix_tools)
    model = ChatOpenAI(model=openai_config.model, temperature=0.1)
    system_prompt = SystemMessage(
        content="You fetch Design Standards from LeanIX using MCP tools. "
                "Be concise and focus on the most relevant information."
    )
    return create_react_agent(
        model,
        design_tools,
        state_modifier=lambda s: {**s, "messages": [system_prompt] + s.get("messages", [])}
    )


async def _query_leanix(query: str) -> str:
    """Query LeanIX through the AI agent."""
    agent = await _build_agent()
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].content


# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool()
async def search_design_standards(topic: str) -> str:
    """
    Search for design standards, best practices, and architectural guidelines 
    from LeanIX.
    
    Args:
        topic: The topic to search for (e.g., 'event driven architecture', 
               'microservices', 'API security')
    
    Returns:
        Design standards and best practices from LeanIX
    """
    try:
        logger.info(f"Searching design standards for: {topic}")
        query = f"Search for design standards about: {topic}"
        result = await _query_leanix(query)
        logger.info("Query completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return f"Error querying LeanIX: {str(e)}"


@mcp.tool()
async def get_architecture_patterns(architecture_type: str) -> str:
    """
    Get architectural patterns and design guidelines for a specific architecture style.
    
    Args:
        architecture_type: Architecture type (e.g., 'microservices', 'event-driven', 
                          'serverless')
    
    Returns:
        Architectural patterns and guidelines from LeanIX
    """
    try:
        logger.info(f"Getting architecture patterns for: {architecture_type}")
        query = f"Get architectural patterns and guidelines for: {architecture_type}"
        result = await _query_leanix(query)
        logger.info("Query completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return f"Error querying LeanIX: {str(e)}"


@mcp.tool()
async def get_technology_standards(technology: str) -> str:
    """
    Get technology standards and guidelines for specific technologies or frameworks.
    
    Args:
        technology: Technology name (e.g., 'Kafka', 'React', 'Kubernetes')
    
    Returns:
        Technology standards and guidelines from LeanIX
    """
    try:
        logger.info(f"Getting technology standards for: {technology}")
        query = f"Get technology standards and guidelines for: {technology}"
        result = await _query_leanix(query)
        logger.info("Query completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return f"Error querying LeanIX: {str(e)}"


@mcp.tool()
async def get_security_guidelines(security_area: str) -> str:
    """
    Get security guidelines, best practices, and standards from LeanIX.
    
    Args:
        security_area: Security area (e.g., 'API security', 'authentication', 
                      'data encryption')
    
    Returns:
        Security guidelines and best practices from LeanIX
    """
    try:
        logger.info(f"Getting security guidelines for: {security_area}")
        query = f"Get security guidelines and best practices for: {security_area}"
        result = await _query_leanix(query)
        logger.info("Query completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return f"Error querying LeanIX: {str(e)}"


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    logger.info(f"Starting LeanIX Design Agent MCP Server")
    logger.info(f"Server URL: http://{host}:{port}")
    logger.info(f"OpenAI Model: {openai_config.model}")
    logger.info(f"LeanIX URL: {leanix_config.url}")
    
    mcp.run(transport="streamable_http", host=host, port=port)

