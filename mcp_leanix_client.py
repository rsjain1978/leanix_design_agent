import asyncio
from typing import Dict, Any, List
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
from config import leanix_config

def build_connections_config() -> Dict[str, Dict[str, Any]]:
    conn: Dict[str, Any] = {"transport": leanix_config.transport}
    if leanix_config.transport in ("streamable_http", "sse"):
        conn["url"] = leanix_config.url
        headers = {}
        if leanix_config.auth_bearer:
            headers["Authorization"] = f"Bearer {leanix_config.auth_bearer}"
        if headers:
            conn["headers"] = headers
    return {leanix_config.server_name: conn}

async def get_leanix_tools() -> List[BaseTool]:
    connections = build_connections_config()
    async with MultiServerMCPClient(connections) as client:
        tools = await client.get_tools()
    print("=== LeanIX MCP tools loaded ===")
    for t in tools:
        print(f"- {t.name}: {t.description}")
    print("================================")
    return tools

if __name__ == "__main__":
    asyncio.run(get_leanix_tools())
